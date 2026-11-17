/**
 * Publish a post via the platform API (POST /api/posts).
 *
 * The post is always created as the logged-in user (JWT identity) - it is
 * impossible to publish on behalf of someone else.
 * The server enforces: JWT auth, device fingerprint, content moderation,
 * per-user/IP rate limits (10/hr per user), 30-day bubble expiry.
 *
 * If the draft references local images (powpow-local://N keys + a
 * <file>.manifest.json written by compose.js), they are uploaded HERE,
 * right before posting. Composition stays 100% local; upload progress is
 * persisted after each image so a failed run can be retried without
 * re-uploading what already succeeded.
 *
 * Usage: node publish.js <html-file-path>
 */
const fs = require('fs');
const { api, requireSession, SessionExpiredError, ApiError } = require('./lib/api-client');
const { extractDigitalHuman, extractLocation, validateEditorFormat } = require('./lib/html-formatter');
const { uploadPostImage } = require('./upload-image');

const LOCAL_IMG_KEY_RE = /powpow-local:\/\/\d+/g;

/**
 * Upload all local images referenced by the draft and substitute their URLs.
 * After each successful upload the HTML file and manifest are rewritten,
 * so a retry skips already-uploaded images.
 */
async function uploadLocalImages(content, htmlPath) {
  const keys = Array.from(new Set(content.match(LOCAL_IMG_KEY_RE) || []));
  if (keys.length === 0) return content;

  const manifestPath = `${htmlPath}.manifest.json`;
  let manifest = { localImages: [] };
  if (fs.existsSync(manifestPath)) {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8').replace(/^\uFEFF/, ''));
  }
  const byKey = new Map((manifest.localImages || []).map(e => [e.key, e.path]));

  for (const key of keys) {
    const filePath = byKey.get(key);
    if (!filePath || !fs.existsSync(filePath)) {
      throw new Error(
        `Local image ${key} has no manifest entry or its file was moved/deleted. ` +
        'Re-run compose.js to rebuild the draft.'
      );
    }
    console.log(`  Uploading ${key}: ${filePath}`);
    const url = await uploadPostImage(filePath);
    console.log(`  Uploaded: ${url}`);
    content = content.split(key).join(url);
    fs.writeFileSync(htmlPath, content, 'utf-8');
    byKey.delete(key);
    const rest = Array.from(byKey.entries()).map(([k, v]) => ({ key: k, path: v }));
    if (rest.length > 0) {
      fs.writeFileSync(manifestPath, JSON.stringify({ version: 1, localImages: rest }, null, 2), 'utf-8');
    } else if (fs.existsSync(manifestPath)) {
      fs.unlinkSync(manifestPath);
    }
  }
  return content;
}

async function publishWithRetry(postData, maxRetries = 3) {
  let lastError;
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const body = await api('POST', '/api/posts', postData);
      if (body && body.success && body.post) return body.post;
      throw new Error(body && body.error ? body.error : 'Unexpected response');
    } catch (err) {
      // Do not retry client errors (except explicit retry-after) or auth issues.
      if (err instanceof SessionExpiredError) throw err;
      if (err instanceof ApiError && err.status === 429) {
        const retryAfter = (err.body && err.body.retryAfter) || 60;
        if (attempt < maxRetries) {
          console.log(`  Rate limited. Retrying in ${retryAfter}s...`);
          await new Promise(r => setTimeout(r, Math.min(retryAfter, 120) * 1000));
          continue;
        }
      }
      if (err instanceof ApiError && err.status >= 400 && err.status < 500 && err.status !== 429) {
        throw err; // validation/moderation errors - fail fast
      }
      lastError = err;
      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000;
        console.log(`  Retry ${attempt}/${maxRetries} in ${delay}ms...`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  throw lastError;
}

async function main() {
  const [, , htmlPath] = process.argv;
  if (!htmlPath) {
    console.error('Usage: node publish.js <html-file-path>');
    process.exit(1);
  }

  let content = fs.readFileSync(htmlPath, 'utf-8');
  console.log(`Content length: ${content.length} chars`);

  let session;
  try {
    session = requireSession();
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    throw err;
  }
  console.log(`Publishing as: ${session.username}`);

  // Deferred local-image upload: this is the ONLY moment the images
  // leave the user's machine (compose.js keeps everything local).
  try {
    content = await uploadLocalImages(content, htmlPath);
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`\n❌ Image upload failed: ${err.message}`);
    console.error('   Nothing was posted. Fix the issue and re-run publish.js ' +
      '(already-uploaded images are reused, not re-uploaded).');
    process.exitCode = 1;
    return;
  }

  const dhInfo = extractDigitalHuman(content);
  if (dhInfo) console.log(`Digital Human: ${dhInfo.name} | ID: ${dhInfo.id}`);

  const locInfo = extractLocation(content);
  if (locInfo) console.log(`Location: ${locInfo.name} (${locInfo.lng}, ${locInfo.lat})`);

  // Guard: interactive components must use the editor's exact HTML structure,
  // otherwise the web frontend renders them as plain text.
  const formatIssues = validateEditorFormat(content);
  if (formatIssues.length > 0) {
    console.error('\n❌ Component HTML does not match the platform editor format:');
    formatIssues.forEach(i => console.error(`   - ${i}`));
    console.error('   Fix: build the post with html-formatter.js helpers (formatPostHTML /');
    console.error('   createDigitalHumanSpan / createLocationSpan), not hand-written spans.');
    process.exitCode = 1;
    return;
  }

  // Payload mirrors the web editor's confirmPublish() exactly:
  // interactive components live inside the rich `content` HTML only.
  // Do NOT send contentItems here - a partial items list makes the frontend
  // switch to structured rendering and drop the post text.
  const postData = {
    type: 'text',
    content,
    ...(locInfo
      ? {
          lng: locInfo.lng,
          lat: locInfo.lat,
          locationName: locInfo.name,
          isLocationExposed: true,
        }
      : { isLocationExposed: false }),
  };

  console.log('\nPublishing...');
  try {
    const post = await publishWithRetry(postData);
    console.log('\n✅ Published successfully!');
    console.log(`Post ID: ${post.id}`);
    console.log(`Created at: ${post.createdAt || new Date().toISOString()}`);
    const config = require('./lib/api-client').loadConfig();
    console.log(`\nView: ${config.platformUrl}/posts/${post.id}`);
    console.log(`\nVerify: node scripts/verify.js ${post.id}`);
    return post.id;
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`\n❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    const reason = err instanceof ApiError && err.body && err.body.error
      ? err.body.error
      : err.message;
    console.error(`\n❌ Publish failed: ${reason}`);
    process.exitCode = 1;
  }
}

main();
