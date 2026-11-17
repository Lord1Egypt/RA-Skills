/**
 * Delete one of your own posts (DELETE /api/posts/[id], JWT-scoped).
 * Useful for cleaning up test posts. You can only delete your own posts.
 *
 * Usage: node delete-post.js <post-id>
 */
const { api, SessionExpiredError, ApiError } = require('./lib/api-client');

async function main() {
  const [, , postId] = process.argv;
  if (!postId) {
    console.error('Usage: node delete-post.js <post-id>');
    process.exit(1);
  }

  try {
    const body = await api('DELETE', `/api/posts/${postId}`);
    console.log(`✅ Post deleted: ${postId}`);
    if (body && body.message) console.log(`   ${body.message}`);
  } catch (err) {
    if (err instanceof SessionExpiredError) {
      console.error(`❌ ${err.message}`);
      process.exitCode = 2;
      return;
    }
    if (err instanceof ApiError && err.status === 404) {
      console.error('❌ Post not found (already deleted?)');
      process.exitCode = 1;
      return;
    }
    console.error(`❌ Delete failed: ${err.message}`);
    process.exitCode = 1;
  }
}

main();
