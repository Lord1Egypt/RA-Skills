/**
 * Xiaohongshu handler tests
 * Usage: npx tsx test-xiaohongshu.ts [--e2e]
 *
 * Without --e2e: runs unit tests only (no network / no browser)
 * With --e2e:    also runs the handler against a real Xiaohongshu URL
 */

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { extractNoteId, parseXiaohongshuContent } from "./xiaohongshu.js";
import type { XiaohongshuContent } from "./types.js";

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
// Unit: extractNoteId
// ---------------------------------------------------------------------------

function testExtractNoteId(): void {
  console.log("\n[extractNoteId]");

  // xiaohongshu.com/explore/{noteId}
  assertEqual(
    extractNoteId("https://www.xiaohongshu.com/explore/6745abc0def1234567890abc"),
    "6745abc0def1234567890abc",
    "xiaohongshu.com/explore/{id}",
  );

  // xiaohongshu.com/discovery/item/{noteId}
  assertEqual(
    extractNoteId("https://www.xiaohongshu.com/discovery/item/6745abc0def1234567890abc"),
    "6745abc0def1234567890abc",
    "xiaohongshu.com/discovery/item/{id}",
  );

  // xiaohongshu.com/user/profile/{uid}/{noteId}
  assertEqual(
    extractNoteId("https://www.xiaohongshu.com/user/profile/5a1b2c3d/6745abc0def1234567890abc"),
    "6745abc0def1234567890abc",
    "xiaohongshu.com/user/profile/{uid}/{id}",
  );

  // xhslink.com/{shortId}
  assertEqual(
    extractNoteId("https://xhslink.com/a1B2cD"),
    "a1B2cD",
    "xhslink.com/{shortId}",
  );

  // With query parameters — should still extract the note ID
  assertEqual(
    extractNoteId("https://www.xiaohongshu.com/explore/6745abc0def1234567890abc?xsec_token=abc123"),
    "6745abc0def1234567890abc",
    "xiaohongshu.com/explore/{id} with query params",
  );

  // Invalid URL should throw
  let threw = false;
  try {
    extractNoteId("not-a-url");
  } catch {
    threw = true;
  }
  assert(threw, "throws on invalid URL");

  // Unsupported host should throw
  threw = false;
  try {
    extractNoteId("https://example.com/explore/abc123");
  } catch {
    threw = true;
  }
  assert(threw, "throws on unsupported host");
}

// ---------------------------------------------------------------------------
// Unit: parseXiaohongshuContent
// ---------------------------------------------------------------------------

function testParseXiaohongshuContent(): void {
  console.log("\n[parseXiaohongshuContent]");

  const mockData = {
    title: "测试标题：成都美食推荐",
    desc: "这是一篇关于成都美食的笔记。\n#成都美食 #旅行攻略",
    imageList: [
      {
        urlDefault: "https://sns-webpic.xhscdn.com/pic1.jpg",
        url: "https://sns-webpic.xhscdn.com/pic1_large.jpg",
        infoList: [
          { url: "https://sns-webpic.xhscdn.com/pic1_hd.jpg" },
        ],
      },
      {
        urlDefault: "//sns-webpic.xhscdn.com/pic2.jpg",
      },
    ],
    video: undefined,
    tagList: [{ name: "成都" }, { name: "美食" }],
    user: {
      nickname: "美食达人",
      avatar: "https://sns-avatar.xhscdn.com/avatar.jpg",
    },
    time: 1711065600000, // 2024-03-22
    interactInfo: {
      likedCount: "1234",
      collectedCount: "567",
      commentCount: "89",
    },
    type: "normal",
  };

  const result: XiaohongshuContent = parseXiaohongshuContent(
    mockData,
    "https://www.xiaohongshu.com/explore/abc123",
  );

  assertEqual(result.platform, "xiaohongshu", "platform is xiaohongshu");
  assertEqual(result.title, "测试标题：成都美食推荐", "title extracted");
  assertEqual(result.author, "美食达人", "author from user.nickname");
  assertEqual(result.date, "2024-03-22", "date formatted from timestamp");
  assert(result.text.includes("成都美食"), "text contains content");
  assertEqual(result.images.length, 2, "2 images extracted");
  assertEqual(
    result.images[0],
    "https://sns-webpic.xhscdn.com/pic1_hd.jpg",
    "prefers infoList last URL",
  );
  assert(
    result.images[1].startsWith("https://"),
    "protocol-relative URL gets https prefix",
  );
  assertEqual(result.videoUrl, null, "no video for normal note");
  assert(result.tags.includes("成都"), "tag from tagList");
  assert(result.tags.includes("美食"), "tag from tagList");
  assert(result.tags.includes("成都美食"), "tag from hashtag in text");
  assert(result.tags.includes("旅行攻略"), "tag from hashtag in text");
  assertEqual(result.stats.likes, 1234, "likes parsed");
  assertEqual(result.stats.collects, 567, "collects parsed");
  assertEqual(result.stats.comments, 89, "comments parsed");
  assertEqual(
    result.originalUrl,
    "https://www.xiaohongshu.com/explore/abc123",
    "originalUrl preserved",
  );
}

// ---------------------------------------------------------------------------
// Unit: parseXiaohongshuContent — video note
// ---------------------------------------------------------------------------

function testParseVideoContent(): void {
  console.log("\n[parseXiaohongshuContent — video]");

  const mockVideoData = {
    title: "视频笔记",
    desc: "这是一个视频笔记",
    imageList: [],
    video: {
      consumer: { originVideoKey: "video_key_abc123" },
      media: {
        stream: {
          h264: [{ masterUrl: "https://sns-video-bd.xhscdn.com/stream.m3u8" }],
        },
      },
    },
    tagList: [],
    user: { nickname: "视频博主" },
    time: 0,
    interactInfo: {
      likedCount: "1.2w",
      collectedCount: "3000",
      commentCount: "500",
    },
    type: "video",
  };

  const result = parseXiaohongshuContent(
    mockVideoData,
    "https://www.xiaohongshu.com/explore/video123",
  );

  assertEqual(
    result.videoUrl,
    "https://sns-video-bd.xhscdn.com/stream.m3u8",
    "video URL from h264 stream",
  );
  assertEqual(result.stats.likes, 12000, "万/w suffix parsed as *10000");
}

// ---------------------------------------------------------------------------
// Unit: parseXiaohongshuContent — stat count edge cases
// ---------------------------------------------------------------------------

function testStatCountParsing(): void {
  console.log("\n[parseXiaohongshuContent — stat edge cases]");

  const base = {
    title: "T",
    desc: "D",
    imageList: [],
    video: undefined,
    tagList: [],
    user: { nickname: "U" },
    time: 0,
    type: "normal",
  };

  const r1 = parseXiaohongshuContent(
    { ...base, interactInfo: { likedCount: "0", collectedCount: "", commentCount: "abc" } },
    "https://example.com",
  );
  assertEqual(r1.stats.likes, 0, "0 string → 0");
  assertEqual(r1.stats.collects, 0, "empty string → 0");
  assertEqual(r1.stats.comments, 0, "non-numeric string → 0");

  const r2 = parseXiaohongshuContent(
    { ...base, interactInfo: { likedCount: "2.5万", collectedCount: "1w", commentCount: "100" } },
    "https://example.com",
  );
  assertEqual(r2.stats.likes, 25000, "2.5万 → 25000");
  assertEqual(r2.stats.collects, 10000, "1w → 10000");
  assertEqual(r2.stats.comments, 100, "plain number");
}

// ---------------------------------------------------------------------------
// E2E: run the handler as a subprocess with a real Xiaohongshu URL
// ---------------------------------------------------------------------------

async function testE2E(): Promise<void> {
  console.log("\n[E2E] Running handler with real Xiaohongshu URL (Chrome CDP)...");

  const testUrl =
    "https://www.xiaohongshu.com/explore/6458c890000000001300e52b";

  try {
    const { stdout } = await exec("npx", ["tsx", "xiaohongshu.ts", testUrl], {
      cwd: import.meta.dirname,
      timeout: 60_000,
    });

    let result: Record<string, any>;
    try {
      result = JSON.parse(stdout);
    } catch {
      assert(false, "stdout is valid JSON");
      console.log("  Raw stdout:", stdout.slice(0, 300));
      return;
    }

    if (result.error) {
      assert(false, `handler did not return error (got: ${result.error})`);
      return;
    }

    assert(true, "stdout is valid JSON");
    assertEqual(result.platform, "xiaohongshu", "platform is xiaohongshu");
    assert(
      typeof result.author === "string" && result.author.length > 0,
      "author is non-empty",
    );
    assert(
      typeof result.text === "string" && result.text.length > 0,
      "text is non-empty",
    );
    assert(
      typeof result.title === "string" && result.title.length > 0,
      "title is non-empty",
    );
    assert(typeof result.fetchedAt === "string", "fetchedAt present");
    assertEqual(result.originalUrl, testUrl, "originalUrl matches input");
    assert(Array.isArray(result.images), "images is array");
    assert(Array.isArray(result.tags), "tags is array");
    assert(
      typeof result.stats === "object" && result.stats !== null,
      "stats is object",
    );

    console.log(`  → Author: ${result.author}`);
    console.log(`  → Title: ${result.title}`);
    console.log(`  → Date: ${result.date}`);
    console.log(`  → Images: ${result.images?.length ?? 0}`);
    console.log(`  → Tags: ${result.tags?.join(", ") ?? "none"}`);
    console.log(
      `  → Stats: likes=${result.stats?.likes} collects=${result.stats?.collects} comments=${result.stats?.comments}`,
    );
  } catch (e: any) {
    assert(false, `handler executed without error (${e.message})`);
  }
}

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------

async function run(): Promise<void> {
  const runE2E = process.argv.includes("--e2e");

  console.log("=== Xiaohongshu Handler Tests ===");

  testExtractNoteId();
  testParseXiaohongshuContent();
  testParseVideoContent();
  testStatCountParsing();

  if (runE2E) {
    await testE2E();
  } else {
    console.log("\n[E2E] Skipped (pass --e2e to run)");
  }

  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

run();
