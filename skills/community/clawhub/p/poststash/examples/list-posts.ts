/**
 * Example: List and filter posts via PostStash
 *
 * Run with:
 *   POSTSTASH_API_KEY=ps_live_... npx ts-node examples/list-posts.ts
 */

import { listPosts } from "../src/tools/list-posts";
import { getPost } from "../src/tools/get-post";

async function main() {
  // List the 10 most recent Ready posts
  const ready = await listPosts.execute({ status: "Ready", limit: 10 });
  console.log(`Ready posts (${ready.total} total):`);
  for (const post of ready.posts) {
    console.log(`  [${post.id}] ${post.content.slice(0, 60)}...`);
    console.log(`    Platforms: ${post.platforms.join(", ")} | Schedule: ${post.schedule}`);
  }

  // List already-published posts
  const published = await listPosts.execute({ published: true, limit: 5 });
  console.log(`\nPublished posts (${published.total} total):`);
  for (const post of published.posts) {
    console.log(`  [${post.id}] ${post.content.slice(0, 60)}...`);
  }

  // Fetch a specific post with analytics (use the first published post ID if available)
  if (published.posts.length > 0) {
    const postId = published.posts[0].id;
    const detail = await getPost.execute({ post_id: postId });
    console.log("\nPost detail:", detail.post);
    if (detail.analytics.length > 0) {
      console.log("Analytics:", detail.analytics);
    }
  }
}

main().catch(console.error);
