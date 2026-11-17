/**
 * Verify a published post is live, by fetching it directly by ID via the
 * platform API (no more "recent 50" heuristics).
 *
 * Usage: node verify.js <post-id>
 */
const { api, loadConfig, SessionExpiredError } = require('./lib/api-client');
const { extractDigitalHuman, extractLocation, countImages, countWords, validateEditorFormat } = require('./lib/html-formatter');

async function main() {
  const [, , postId] = process.argv;
  if (!postId) {
    console.error('Usage: node verify.js <post-id>');
    process.exit(1);
  }

  console.log(`=== Verifying Post ${postId} ===\n`);

  try {
    const body = await api('GET', `/api/posts/${postId}`);
    const post = body.post || body;
    if (!post || !post.id) {
      console.error('❌ Post not found');
      process.exitCode = 1;
      return;
    }

    const content = post.content || '';

    // Components are read from the post's own HTML, which is authoritative.
    // The top-level post fields can be absent (a location chip inside the
    // content is enough for the post to be on the map), so they are only a
    // fallback here.
    const dh = extractDigitalHuman(content);
    const loc = extractLocation(content);
    const imageCount = countImages(content);

    console.log('1. Post retrieval:');
    console.log('   ✅ Post exists and is accessible');
    const author = post.user || {};
    console.log(`   Author: ${author.nickname || author.username || (post.userId || post.user_id)}`);
    console.log(`   Created at: ${post.createdAt || post.created_at || 'unknown'}`);
    const locName = loc ? loc.name : (post.locationName || post.location_name || 'none');
    const locLng = loc ? loc.lng : post.lng;
    const locLat = loc ? loc.lat : post.lat;
    console.log(`   Location: ${locName} (${locLng}, ${locLat})`);

    console.log('\n2. HTML content components:');
    console.log(`   Digital Human: ${dh ? `✅ ${dh.name}` : '— (none)'}`);
    console.log(`   Location component: ${loc ? `✅ ${loc.name}` : '— (none)'}`);
    console.log(`   Images: ${imageCount}`);

    const formatIssues = validateEditorFormat(content);
    if (formatIssues.length > 0) {
      console.log('   ⚠️ Component format issues (may render as plain text):');
      formatIssues.forEach(i => console.log(`      - ${i}`));
      process.exitCode = 1;
    } else if (dh || loc) {
      console.log('   ✅ Components use interactive editor format (chips, not plain text)');
    }

    console.log('\n3. Word count (Latin words + CJK chars):');
    console.log(`   ${countWords(content)} (platform limit: 50000 chars, content is ${content.length} chars)`);

    console.log('\n=== Verification Complete ===');
    console.log(`Post URL: ${loadConfig().platformUrl}/posts/${post.id}`);
    console.log(`Post ID: ${post.id}`);
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    if (err.status === 404) {
      console.error('❌ Post not found (was it deleted, or is the ID wrong?)');
      process.exitCode = 1;
      return;
    }
    console.error(`❌ Verification failed: ${err.message}`);
    process.exitCode = 1;
  }
}

main();
