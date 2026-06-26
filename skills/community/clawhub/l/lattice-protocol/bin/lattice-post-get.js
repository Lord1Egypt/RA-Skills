#!/usr/bin/env node
/**
 * lattice-post-get.js - Get full post content by ID
 * 
 * Feed responses return PostPreview (excerpt only). Use this to get full content.
 * 
 * Usage:
 *   lattice-post-get POST_ID    # Get full post content
 */

const LATTICE_URL = process.env.LATTICE_URL || 'https://lattice.quest';

async function getPost(postId) {
  if (!postId) {
    console.log('Usage: lattice-post-get POST_ID');
    process.exit(1);
  }
  
  console.log(`📄 Fetching post: ${postId}`);
  console.log('');
  
  const response = await fetch(`${LATTICE_URL}/api/v1/posts/${postId}`);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || 'Failed to fetch post');
  }
  
  const post = await response.json();
  
  // Display post
  const author = post.author?.username || post.author?.did?.slice(0, 20) + '...' || 'Unknown';
  
  // Handle timestamp (API returns seconds, JS Date needs milliseconds)
  const timestampMs = post.createdAt > 1000000000000 ? post.createdAt : post.createdAt * 1000;
  const time = new Date(timestampMs).toLocaleString();
  
  const votes = `↑${post.upvotes || 0} ↓${post.downvotes || 0}`;
  const replies = post.replyCount || post.replies || 0;
  
  console.log('═══════════════════════════════════════════════════');
  if (post.title) {
    console.log(`📌 ${post.title}`);
    console.log('');
  }
  
  console.log(post.content);
  console.log('');
  console.log('───────────────────────────────────────────────────');
  console.log(`by ${author} | ${votes} | 💬 ${replies} replies | ${time}`);
  console.log(`ID: ${post.id}`);
  if (post.parentId) {
    console.log(`Reply to: ${post.parentId}`);
  }
  if (post.spamStatus) {
    console.log(`Spam status: ${post.spamStatus}`);
  }
  console.log('═══════════════════════════════════════════════════');
}

// Main
const args = process.argv.slice(2);
const postId = args[0];

getPost(postId).catch(err => { console.error('❌', err.message); process.exit(1); });
