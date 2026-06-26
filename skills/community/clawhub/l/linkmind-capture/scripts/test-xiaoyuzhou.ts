/**
 * Xiaoyuzhou handler tests
 * Usage: npx tsx test-xiaoyuzhou.ts [--e2e]
 */

import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { parseEpisodeUrl, parseSubtitleEntries, filterByTimeWindow, formatSubtitleSegment } from "./xiaoyuzhou.js";

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
// Unit: parseEpisodeUrl
// ---------------------------------------------------------------------------

function testParseEpisodeUrl(): void {
  console.log("\n[parseEpisodeUrl]");

  // 带时间戳的完整链接（#ts 在 ? 前）
  const r1 = parseEpisodeUrl(
    "https://www.xiaoyuzhoufm.com/episode/69b4d2f9f8b8079bfa3ae7f2#ts=1023?s=eyJ1IjoiNWY"
  );
  assertEqual(r1.episodeId, "69b4d2f9f8b8079bfa3ae7f2", "提取 episodeId");
  assertEqual(r1.timestampSeconds, 1023, "提取 timestampSeconds=1023");

  // 不带时间戳
  const r2 = parseEpisodeUrl(
    "https://www.xiaoyuzhoufm.com/episode/abc123"
  );
  assertEqual(r2.episodeId, "abc123", "不带时间戳时提取 episodeId");
  assertEqual(r2.timestampSeconds, null, "不带时间戳时 timestampSeconds 为 null");

  // ts=0 边界情况
  const r3 = parseEpisodeUrl(
    "https://www.xiaoyuzhoufm.com/episode/xyz#ts=0"
  );
  assertEqual(r3.timestampSeconds, 0, "ts=0 解析为 0（非 null）");

  // 非小宇宙链接抛错
  let threw = false;
  try {
    parseEpisodeUrl("https://weibo.com/foo");
  } catch {
    threw = true;
  }
  assert(threw, "非小宇宙链接抛出错误");
}

// ---------------------------------------------------------------------------
// Unit: parseSubtitleEntries
// ---------------------------------------------------------------------------

function testParseSubtitleEntries(): void {
  console.log("\n[parseSubtitleEntries]");

  // SRT format
  const srt = `1
00:00:05,000 --> 00:00:08,000
大家好，欢迎收听本期节目。

2
00:01:03,000 --> 00:01:10,500
今天我们来聊聊人工智能的未来。

3
00:02:30,000 --> 00:02:45,000
这是第三句话。
`;

  const entries = parseSubtitleEntries(srt);
  assertEqual(entries.length, 3, "解析出 3 条字幕");
  assertEqual(entries[0].startSeconds, 5, "第一条 startSeconds=5");
  assertEqual(entries[0].endSeconds, 8, "第一条 endSeconds=8");
  assertEqual(entries[0].text, "大家好，欢迎收听本期节目。", "第一条文本正确");
  assertEqual(entries[1].startSeconds, 63, "第二条 startSeconds=63（1分3秒）");
  assertEqual(entries[2].startSeconds, 150, "第三条 startSeconds=150（2分30秒）");

  // Empty input
  const empty = parseSubtitleEntries("");
  assertEqual(empty.length, 0, "空字符串解析为空数组");
}

function testFilterByTimeWindow(): void {
  console.log("\n[filterByTimeWindow]");

  const entries = [
    { startSeconds: 10, endSeconds: 15, text: "A" },
    { startSeconds: 60, endSeconds: 65, text: "B" },
    { startSeconds: 120, endSeconds: 130, text: "C" },
    { startSeconds: 200, endSeconds: 210, text: "D" },
  ];

  // Window [55s, 135s]: should include B (60-65) and C (120-130)
  const filtered = filterByTimeWindow(entries, 55, 135);
  assertEqual(filtered.length, 2, "窗口 [55s,135s] 含 2 条");
  assertEqual(filtered[0].text, "B", "第一条为 B");
  assertEqual(filtered[1].text, "C", "第二条为 C");

  // startSec=null, endSec=65: only A(10-15) and B(60-65)
  const fromStart = filterByTimeWindow(entries, null, 65);
  assertEqual(fromStart.length, 2, "endSec=65 含 A 和 B");
  assertEqual(fromStart[fromStart.length - 1].text, "B", "最后一条为 B");

  // startSec=120, endSec=null: C(120-130) and D(200-210)
  const toEnd = filterByTimeWindow(entries, 120, null);
  assertEqual(toEnd.length, 2, "startSec=120 含 C 和 D");
  assertEqual(toEnd[0].text, "C", "第一条为 C");

  // null window = all entries
  const all = filterByTimeWindow(entries, null, null);
  assertEqual(all.length, 4, "null 窗口返回全部");
}

function testFormatSubtitleSegment(): void {
  console.log("\n[formatSubtitleSegment]");

  const entries = [
    { startSeconds: 63, endSeconds: 70, text: "今天我们聊聊 AI。" },
    { startSeconds: 150, endSeconds: 160, text: "这是很重要的一点。" },
  ];

  const result = formatSubtitleSegment(entries);
  assert(result.includes("[01:03]"), "包含 [01:03] 时间戳");
  assert(result.includes("[02:30]"), "包含 [02:30] 时间戳");
  assert(result.includes("今天我们聊聊 AI。"), "包含第一条文本");
  assert(result.includes("这是很重要的一点。"), "包含第二条文本");
}

// ---------------------------------------------------------------------------
// E2E: Full handler pipeline
// ---------------------------------------------------------------------------

async function testE2E(): Promise<void> {
  console.log("\n[E2E] 运行小宇宙处理器...");

  const testUrl = "https://xyzfm.link/s/Qlkr7p";

  try {
    const { stdout } = await exec(
      "npx",
      ["tsx", "xiaoyuzhou.ts", testUrl, "--config", "../config.json"],
      { cwd: import.meta.dirname, timeout: 30_000 },
    );

    let result: Record<string, any>;
    try {
      result = JSON.parse(stdout);
    } catch {
      assert(false, "stdout 是合法 JSON");
      console.log("  Raw stdout:", stdout.slice(0, 300));
      return;
    }

    if (result.error) {
      console.log(`  ⚠ 处理器错误: ${result.error} (code: ${result.code})`);
      if (result.code === "NETWORK" || result.code === "AUTH") {
        console.log("  → 跳过 E2E 断言（网络/认证问题）");
        return;
      }
      assert(false, `处理器成功返回内容`);
      return;
    }

    assert(true, "stdout 是合法 JSON");
    assertEqual(result.platform, "xiaoyuzhou", "platform 为 xiaoyuzhou");
    assert(typeof result.episodeId === "string" && result.episodeId.length > 0, "episodeId 非空");
    assert(typeof result.title === "string" && result.title.length > 0, "title 非空");
    assert(typeof result.podcast === "string" && result.podcast.length > 0, "podcast 非空");
    assert(typeof result.audioUrl === "string" && result.audioUrl.startsWith("http"), "audioUrl 是 HTTP URL");
    assert(typeof result.durationSeconds === "number" && result.durationSeconds > 0, "durationSeconds > 0");
    assertEqual(result.timestampSeconds, 1023, "timestampSeconds=1023（17:03）");
    console.log(`  → Title: ${result.title}`);
    console.log(`  → Podcast: ${result.podcast}`);
    console.log(`  → Duration: ${result.durationSeconds}s`);
    console.log(`  → SubtitleUrl: ${result.subtitleUrl ?? "(none)"}`);
  } catch (e: any) {
    assert(false, `处理器正常执行（${e.message}）`);
  }
}

async function run(): Promise<void> {
  const runE2E = process.argv.includes("--e2e");

  console.log("=== Xiaoyuzhou Handler Tests ===");

  testParseEpisodeUrl();
  testParseSubtitleEntries();
  testFilterByTimeWindow();
  testFormatSubtitleSegment();

  if (runE2E) {
    await testE2E();
  } else {
    console.log("\n[E2E] Skipped (pass --e2e to run)");
  }

  console.log(`\n--- Results: ${passed} passed, ${failed} failed ---`);
  if (failed > 0) process.exit(1);
}

run();
