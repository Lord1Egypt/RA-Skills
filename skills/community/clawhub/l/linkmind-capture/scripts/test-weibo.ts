/**
 * Weibo handler tests
 * Usage: npx tsx test-weibo.ts [--e2e]
 *
 * Without --e2e: runs unit tests only (no network)
 * With --e2e:    also runs a real API call against m.weibo.cn
 */

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import {
  base62ToMid,
  extractWeiboId,
  stripHtml,
  parseWeiboContent,
} from "./weibo.js";
import type { WeiboContent } from "./types.js";

const exec = promisify(execFile);

let passed = 0;
let failed = 0;

function assert(condition: boolean, label: string): void {
  if (condition) {
    passed++;
    console.log(`  ✓ ${label}`);
  } else {
    failed++;
    console.log(`  ✗ ${label}`);
  }
}

function assertEqual(actual: unknown, expected: unknown, label: string): void {
  const ok = actual === expected;
  if (!ok) {
    label += ` (got ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)})`;
  }
  assert(ok, label);
}

// ---------------------------------------------------------------------------
// Unit: base62ToMid
// ---------------------------------------------------------------------------

function testBase62ToMid(): void {
  console.log("\n[base62ToMid]");
  // Single group (< 4 chars)
  assertEqual(base62ToMid("a"), "10", "a → 10");
  assertEqual(base62ToMid("A"), "36", "A → 36");
  // Multi-group
  assertEqual(base62ToMid("N5WBGE0jf"), "4914169289534313", "N5WBGE0jf → 4914169289534313");
  assertEqual(base62ToMid("Ovkbt83PK"), "5074657591921364", "Ovkbt83PK → 5074657591921364");
}

// ---------------------------------------------------------------------------
// Unit: extractWeiboId
// ---------------------------------------------------------------------------

function testExtractWeiboId(): void {
  console.log("\n[extractWeiboId]");

  // Mobile detail URL
  assertEqual(
    extractWeiboId("https://m.weibo.cn/detail/4331051486294436"),
    "4331051486294436",
    "m.weibo.cn/detail/{mid}",
  );

  // Mobile status URL
  assertEqual(
    extractWeiboId("https://m.weibo.cn/status/4331051486294436"),
    "4331051486294436",
    "m.weibo.cn/status/{mid}",
  );

  // Desktop with numeric mid
  assertEqual(
    extractWeiboId("https://weibo.com/1234567890/4331051486294436"),
    "4331051486294436",
    "weibo.com/{uid}/{numeric_mid}",
  );

  // Desktop with base62
  assertEqual(
    extractWeiboId("https://weibo.com/1234567890/N5WBGE0jf"),
    "4914169289534313",
    "weibo.com/{uid}/{base62}",
  );

  // Invalid URL should throw
  let threw = false;
  try {
    extractWeiboId("not-a-url");
  } catch {
    threw = true;
  }
  assert(threw, "throws on invalid URL");

  // Unsupported host should throw
  threw = false;
  try {
    extractWeiboId("https://example.com/foo/bar");
  } catch {
    threw = true;
  }
  assert(threw, "throws on unsupported host");
}

// ---------------------------------------------------------------------------
// Unit: stripHtml
// ---------------------------------------------------------------------------

function testStripHtml(): void {
  console.log("\n[stripHtml]");

  assertEqual(
    stripHtml("hello<br>world"),
    "hello\nworld",
    "<br> → newline",
  );

  assertEqual(
    stripHtml('<a href="/n/test">#话题#</a>'),
    "#话题#",
    "topic link → #话题#",
  );

  assertEqual(
    stripHtml('<a href="/n/test">@用户</a>'),
    "@用户",
    "mention link → @用户",
  );

  assertEqual(
    stripHtml('<img alt="[笑哭]" src="...">'),
    "[笑哭]",
    "emoji img → alt text",
  );

  assertEqual(
    stripHtml('<span class="url-icon"><img src="..."></span>rest'),
    "rest",
    "url-icon span removed",
  );

  assertEqual(
    stripHtml("hello&#x4e16;&#x754c;"),
    "hello世界",
    "hex entities decoded",
  );

  assertEqual(
    stripHtml("a &lt; b &gt; c &amp; d"),
    "a < b > c & d",
    "HTML entities decoded",
  );
}

// ---------------------------------------------------------------------------
// Unit: parseWeiboContent
// ---------------------------------------------------------------------------

function testParseWeiboContent(): void {
  console.log("\n[parseWeiboContent]");

  const mockData = {
    text: "这是一条<br>测试微博",
    created_at: "Sun Mar 22 14:30:00 +0800 2026",
    user: {
      screen_name: "测试用户",
      profile_image_url: "https://example.com/avatar.jpg",
    },
    pics: [
      { url: "https://small.jpg", large: { url: "https://large.jpg" } },
      { url: "https://small2.jpg" },
    ],
    reposts_count: 10,
    comments_count: 20,
    attitudes_count: 30,
    page_info: {
      type: "video",
      urls: { mp4_hd_mp4: "https://video.mp4" },
    },
    retweeted_status: {
      text: "原始微博内容",
      user: { screen_name: "原作者" },
    },
  };

  const result: WeiboContent = parseWeiboContent(
    mockData,
    "https://weibo.com/test/123",
  );

  assertEqual(result.platform, "weibo", "platform is weibo");
  assertEqual(result.author, "测试用户", "author from user.screen_name");
  assertEqual(result.date, "2026-03-22", "date parsed correctly");
  assertEqual(result.text, "这是一条\n测试微博", "text with HTML stripped");
  assert(result.title.length > 0, "title generated from text");
  assertEqual(result.images.length, 2, "2 images extracted");
  assertEqual(result.images[0], "https://large.jpg", "prefers large image URL");
  assertEqual(result.images[1], "https://small2.jpg", "falls back to regular URL");
  assertEqual(result.videoUrl, "https://video.mp4", "video URL extracted");
  assert(result.repostOf !== null, "repost detected");
  assertEqual(result.repostOf!.author, "原作者", "repost author");
  assertEqual(result.repostOf!.text, "原始微博内容", "repost text");
  assertEqual(result.stats.reposts, 10, "reposts count");
  assertEqual(result.stats.comments, 20, "comments count");
  assertEqual(result.stats.likes, 30, "likes count");
  assertEqual(
    result.originalUrl,
    "https://weibo.com/test/123",
    "originalUrl preserved",
  );
}

// ---------------------------------------------------------------------------
// E2E: run the handler as a subprocess with a real Weibo URL
// ---------------------------------------------------------------------------

async function testE2E(): Promise<void> {
  console.log("\n[E2E] Running handler with real Weibo URL...");

  const testUrl = "https://m.weibo.cn/detail/5279012110206293";

  try {
    const { stdout } = await exec("npx", ["tsx", "weibo.ts", testUrl], {
      cwd: import.meta.dirname,
      timeout: 15_000,
    });

    let result: Record<string, any>;
    try {
      result = JSON.parse(stdout);
    } catch {
      assert(false, "stdout is valid JSON");
      console.log("  Raw stdout:", stdout.slice(0, 200));
      return;
    }

    if (result.error) {
      assert(false, `handler did not return error (got: ${result.error})`);
      return;
    }

    assert(true, "stdout is valid JSON");
    assertEqual(result.platform, "weibo", "platform is weibo");
    assert(typeof result.author === "string" && result.author.length > 0, "author is non-empty");
    assert(typeof result.text === "string" && result.text.length > 0, "text is non-empty");
    assert(typeof result.date === "string" && result.date.length > 0, "date is non-empty");
    assert(typeof result.title === "string" && result.title.length > 0, "title is non-empty");
    assert(typeof result.fetchedAt === "string", "fetchedAt present");
    assertEqual(result.originalUrl, testUrl, "originalUrl matches input");

    console.log(`  → Author: ${result.author}`);
    console.log(`  → Title: ${result.title}`);
    console.log(`  → Date: ${result.date}`);
    console.log(`  → Images: ${result.images?.length ?? 0}`);
    console.log(`  → Stats: reposts=${result.stats?.reposts} comments=${result.stats?.comments} likes=${result.stats?.likes}`);
  } catch (e: any) {
    assert(false, `handler executed without error (${e.message})`);
  }
}

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------

async function run(): Promise<void> {
  const runE2E = process.argv.includes("--e2e");

  console.log("=== Weibo Handler Tests ===");

  testBase62ToMid();
  testExtractWeiboId();
  testStripHtml();
  testParseWeiboContent();

  if (runE2E) {
    await testE2E();
  } else {
    console.log("\n[E2E] Skipped (pass --e2e to run)");
  }

  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

run();
