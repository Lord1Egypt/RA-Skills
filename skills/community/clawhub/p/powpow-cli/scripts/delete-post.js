/**
 * Delete one of your own posts (DELETE /api/posts/[id], JWT-scoped).
 * Useful for cleaning up test posts. You can only delete your own posts.
 *
 * CONFIRMATION GATE: without --confirm this only FETCHES the post and prints
 * what would be deleted (exit 3); the DELETE is never sent. The agent must
 * show the user the fetched summary and get an explicit YES first.
 *
 * Usage:
 *   node delete-post.js <post-id>             preview only, deletes NOTHING
 *   node delete-post.js <post-id> --confirm   actually delete (irreversible)
 */
const { api, SessionExpiredError, ApiError } = require('./lib/api-client');

function summarizeContent(content) {
  const text = String(content || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  return text.length > 120 ? `${text.slice(0, 120)}...` : text;
}

async function main() {
  const args = process.argv.slice(2);
  const confirmed = args.includes('--confirm');
  const postId = args.find(a => a !== '--confirm');
  if (!postId) {
    console.error('Usage: node delete-post.js <post-id> [--confirm]');
    process.exit(1);
  }

  try {
    if (!confirmed) {
      const body = await api('GET', `/api/posts/${postId}`);
      const post = body.post || body;
      if (!post || !post.id) {
        console.error('❌ Post not found (already deleted, or wrong ID?)');
        process.exitCode = 1;
        return;
      }
      const author = post.user || {};
      console.log('--- PREVIEW (nothing deleted) ---');
      console.log(`Post ID: ${post.id}`);
      console.log(`Author: ${author.nickname || author.username || post.userId || post.user_id || 'unknown'}`);
      console.log(`Created: ${post.createdAt || post.created_at || 'unknown'}`);
      console.log(`Content: ${summarizeContent(post.content)}`);
      console.log('\nDeletion is IRREVERSIBLE. Show the user this summary and ask for explicit confirmation,');
      console.log(`then re-run: node delete-post.js ${postId} --confirm`);
      process.exitCode = 3;
      return;
    }

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
