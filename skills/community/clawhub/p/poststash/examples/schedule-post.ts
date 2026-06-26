/**
 * Example: Schedule a single post to Threads and X via PostStash
 *
 * Run with:
 *   POSTSTASH_API_KEY=ps_live_... npx ts-node examples/schedule-post.ts
 */

import { scheduleToThreads, scheduleToX } from "../src/tools/schedule-post";

async function main() {
  // Schedule a post to Threads now
  const threadsResult = await scheduleToThreads.execute({
    text: "AI agents can now schedule posts via PostStash 🤖",
  });
  console.log("Scheduled to Threads:", threadsResult);

  // Schedule a post to X for 1 hour from now
  const inOneHour = new Date(Date.now() + 3_600_000).toISOString();
  const xResult = await scheduleToX.execute({
    text: "AI agents can now schedule posts via PostStash 🤖",
    scheduled_at: inOneHour,
  });
  console.log("Scheduled to X:", xResult);

  // Save as draft (won't publish automatically)
  const draftResult = await scheduleToThreads.execute({
    text: "This is a draft post — not yet scheduled",
    status: "Draft",
  });
  console.log("Saved draft:", draftResult);
}

main().catch(console.error);
