/**
 * Upload a local image to the platform (POST /api/upload/post-image)
 * and return its public URL.
 *
 * Server contract (api/upload/post-image/route.ts):
 *   - multipart/form-data, field name "file"
 *   - JWT required (account must be activated)
 *   - image/* only, SVG rejected, max 10MB, auto-compressed server-side
 *   - response: { success, imageUrl, compressedSize, originalSize }
 *
 * Usage: node upload-image.js <local-image-path>
 */
const fs = require('fs');
const path = require('path');
const { loadConfig, requireSession, clearSession, SessionExpiredError, ApiError, DEFAULT_USER_AGENT, DEFAULT_ACCEPT_LANGUAGE } = require('./lib/api-client');

const MIME_BY_EXT = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.bmp': 'image/bmp',
  '.heic': 'image/heic',
};

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB, enforced server-side too

/**
 * Upload a local image file and resolve to its public URL.
 * @param {string} filePath local image path
 * @returns {Promise<string>} public image URL
 */
async function uploadPostImage(filePath) {
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    throw new Error(`Image file not found: ${filePath}`);
  }
  const ext = path.extname(filePath).toLowerCase();
  const mime = MIME_BY_EXT[ext];
  if (!mime) {
    throw new Error(`Unsupported image type "${ext}". Supported: ${Object.keys(MIME_BY_EXT).join(' ')}`);
  }
  if (mime === 'image/svg+xml') {
    throw new Error('SVG is rejected by the platform (scriptable content).');
  }
  const size = fs.statSync(filePath).size;
  if (size > MAX_FILE_SIZE) {
    throw new Error(`Image is ${(size / 1048576).toFixed(1)}MB; the platform limit is 10MB.`);
  }

  const config = loadConfig();
  const session = requireSession();

  const buffer = fs.readFileSync(filePath);
  const form = new FormData();
  form.append('file', new Blob([buffer], { type: mime }), path.basename(filePath));

  let resp;
  try {
    resp = await fetch(`${config.platformUrl}/api/upload/post-image`, {
      method: 'POST',
      headers: {
        // Content-Type is set automatically by FormData (multipart boundary).
        'User-Agent': session.userAgent || DEFAULT_USER_AGENT,
        'Accept-Language': session.acceptLanguage || DEFAULT_ACCEPT_LANGUAGE,
        Authorization: `Bearer ${session.token}`,
      },
      body: form,
      signal: AbortSignal.timeout(60000),
    });
  } catch (err) {
    // one retry on transient network failure
    await new Promise(r => setTimeout(r, 2000));
    resp = await fetch(`${config.platformUrl}/api/upload/post-image`, {
      method: 'POST',
      headers: {
        'User-Agent': session.userAgent || DEFAULT_USER_AGENT,
        'Accept-Language': session.acceptLanguage || DEFAULT_ACCEPT_LANGUAGE,
        Authorization: `Bearer ${session.token}`,
      },
      body: form,
      signal: AbortSignal.timeout(60000),
    }).catch(() => { throw err; });
  }

  if (resp.status === 401) {
    clearSession();
    throw new SessionExpiredError();
  }
  const body = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    throw new ApiError(resp.status, body.error || body || 'Upload failed');
  }
  if (!body.success || !body.imageUrl) {
    throw new Error('Upload succeeded but the response is missing imageUrl.');
  }
  return body.imageUrl;
}

async function main() {
  const [, , filePath] = process.argv;
  if (!filePath) {
    console.error('Usage: node upload-image.js <local-image-path>');
    process.exit(1);
  }
  try {
    const url = await uploadPostImage(filePath);
    console.log(`✅ Image uploaded: ${url}`);
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    console.error(`❌ Upload failed: ${err.message}`);
    process.exitCode = 1;
  }
}

if (require.main === module) {
  main();
}

module.exports = { uploadPostImage };
