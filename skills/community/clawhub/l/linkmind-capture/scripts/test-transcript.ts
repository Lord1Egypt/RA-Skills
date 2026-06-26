/**
 * extract-transcript tests
 * Usage: npx tsx test-transcript.ts [--e2e]
 */

import {
  formatSrtTime,
  parseLfasrResult,
  checkDependency,
} from "./extract-transcript.js";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";

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
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    label += ` (got ${JSON.stringify(actual)}, expected ${JSON.stringify(expected)})`;
  }
  assert(ok, label);
}

// ---------------------------------------------------------------------------
// Unit: formatSrtTime
// ---------------------------------------------------------------------------

function testFormatSrtTime(): void {
  console.log("\n[formatSrtTime]");
  assertEqual(formatSrtTime(0),        "00:00:00,000", "0ms → 00:00:00,000");
  assertEqual(formatSrtTime(1000),     "00:00:01,000", "1000ms → 00:00:01,000");
  assertEqual(formatSrtTime(61500),    "00:01:01,500", "61500ms → 00:01:01,500");
  assertEqual(formatSrtTime(3661250),  "01:01:01,250", "3661250ms → 01:01:01,250");
  assertEqual(formatSrtTime(5320),     "00:00:05,320", "5320ms → 00:00:05,320");
}

// ---------------------------------------------------------------------------
// Unit: parseLfasrResult
// ---------------------------------------------------------------------------

function testParseLfasrResult(): void {
  console.log("\n[parseLfasrResult]");

  // iFlytek LFASR v2 orderResult: lattice[].json_1best → { st: { rt: [{ ws: [...] }] } }
  // Each ws: { wb, we (10ms units), cw: [{ w: text }] }
  const orderResult = JSON.stringify({
    lattice: [
      {
        json_1best: JSON.stringify({
          st: { rt: [{ ws: [
            { wb: 0,   we: 200,  cw: [{ w: "今天" }] },
            { wb: 200, we: 532,  cw: [{ w: "我们来聊" }] },
          ] }] },
        }),
      },
      {
        json_1best: JSON.stringify({
          st: { rt: [{ ws: [
            { wb: 600,  we: 800,  cw: [{ w: "这个话题" }] },
            { wb: 800,  we: 1084, cw: [{ w: "很有意思" }] },
          ] }] },
        }),
      },
    ],
  });

  const result = parseLfasrResult(orderResult);

  assert(result.srt.includes("00:00:00,000 --> 00:00:05,320"), "第一句时间戳正确");
  assert(result.srt.includes("今天我们来聊"), "第一句文本正确");
  assert(result.srt.includes("00:00:06,000 --> 00:00:10,840"), "第二句时间戳正确");
  assert(result.srt.includes("这个话题很有意思"), "第二句文本正确");
  assert(result.srt.startsWith("1\n"), "SRT 从序号 1 开始");
  assert(result.fullText.includes("今天我们来聊"), "fullText 包含第一句");
  assert(result.fullText.includes("这个话题很有意思"), "fullText 包含第二句");

  // Empty lattice
  const emptyResult = parseLfasrResult(JSON.stringify({ lattice: [] }));
  assertEqual(emptyResult.srt, "", "空 lattice → 空 SRT");
  assertEqual(emptyResult.fullText, "", "空 lattice → 空 fullText");
}

// ---------------------------------------------------------------------------
// Unit: checkDependency
// ---------------------------------------------------------------------------

function testCheckDependency(): void {
  console.log("\n[checkDependency]");

  // Real command should not throw
  let threw = false;
  try {
    checkDependency("node");
  } catch {
    threw = true;
  }
  assert(!threw, "node 存在 → 不抛错");

  // Nonexistent command should throw with depCode="DEPENDENCY"
  threw = false;
  let errorCode: string | undefined;
  try {
    checkDependency("__linkmind_nonexistent_tool__");
  } catch (e) {
    threw = true;
    errorCode = (e as any).depCode;
  }
  assert(threw, "不存在的命令 → 抛错");
  assertEqual(errorCode, "DEPENDENCY", "错误码为 DEPENDENCY");
}

// ---------------------------------------------------------------------------
// Unit: routeAsr config selection
// ---------------------------------------------------------------------------

function testRouteAsrConfig(): void {
  console.log("\n[routeAsr config selection]");

  // Helper: determine which provider would be selected for a given config
  function selectProvider(cfg: {
    iflytek?: { app_id?: string; api_key?: string; api_secret?: string };
    openai?: { api_key?: string };
  }): string {
    const hasIflytek =
      !!cfg.iflytek?.app_id &&
      !!cfg.iflytek?.api_key &&
      !!cfg.iflytek?.api_secret;
    const hasOpenai = !!cfg.openai?.api_key;
    if (hasIflytek) return "iflytek";
    if (hasOpenai) return "openai";
    return "none";
  }

  assertEqual(
    selectProvider({ iflytek: { app_id: "id", api_key: "key", api_secret: "sec" } }),
    "iflytek",
    "仅配置讯飞 → 选 iflytek",
  );
  assertEqual(
    selectProvider({ openai: { api_key: "sk-xxx" } }),
    "openai",
    "仅配置 OpenAI → 选 openai",
  );
  assertEqual(
    selectProvider({
      iflytek: { app_id: "id", api_key: "key", api_secret: "sec" },
      openai: { api_key: "sk-xxx" },
    }),
    "iflytek",
    "两者都配置 → 优先选 iflytek",
  );
  assertEqual(selectProvider({}), "none", "均未配置 → none");
  assertEqual(
    selectProvider({ iflytek: { app_id: "id" } }),
    "none",
    "讯飞配置不完整 → none",
  );
}

// ---------------------------------------------------------------------------
// Run all unit tests
// ---------------------------------------------------------------------------

const isE2E = process.argv.includes("--e2e");

testFormatSrtTime();
testParseLfasrResult();
testCheckDependency();
testRouteAsrConfig();

// E2E tests defined in Task 9

if (!isE2E) {
  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

// ---------------------------------------------------------------------------
// E2E tests (--e2e flag, requires real credentials + yt-dlp + ffmpeg)
// ---------------------------------------------------------------------------

async function runE2E(): Promise<void> {
  console.log("\n=== E2E Tests (requires ASR credentials) ===");

  const testVideoUrl = process.env.TEST_VIDEO_URL ??
    "https://weibo.com/2192828333/QyWziEdkQ"; // ElevenLabs fine-tune demo, verified working

  const tmpOutputDir = `/tmp/linkmind-e2e-${Date.now()}`;
  const configPath = process.env.TEST_CONFIG_PATH ??
    new URL("../config.json", import.meta.url).pathname;

  console.log(`  Testing URL: ${testVideoUrl}`);

  const result = spawnSync(
    "npx",
    [
      "tsx", "extract-transcript.ts",
      "--media-url", testVideoUrl,
      "--output-dir", tmpOutputDir,
      "--config", configPath,
      "--referer", "https://weibo.com",
    ],
    { encoding: "utf-8", timeout: 15 * 60 * 1000 },
  );

  let output: { srtPath?: string; fullText?: string; error?: string } = {};
  try {
    output = JSON.parse(result.stdout);
  } catch {
    console.log(`  ✗ 无法解析输出: ${result.stdout}`);
    process.exit(1);
  }

  assert(!output.error, `转写成功（无 error 字段）: ${output.error ?? ""}`);
  assert(!!output.srtPath, "输出包含 srtPath");
  assert(!!output.fullText && output.fullText.length > 0, "fullText 非空");

  const srtFile = `${tmpOutputDir}/transcript.srt`;
  assert(existsSync(srtFile), `SRT 文件已生成: ${srtFile}`);

  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

if (isE2E) {
  runE2E().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
