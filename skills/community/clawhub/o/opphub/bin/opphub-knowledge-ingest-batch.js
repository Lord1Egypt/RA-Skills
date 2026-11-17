#!/usr/bin/env node
// bin/opphub-knowledge-ingest-batch.js · v4.0.0
// status: implemented (v4 P1-3 mkdtemp + cleanup, 避免并发竞态)
//
//
// v3.3.0 改动: 不再循环调 knowledge-add (v3.2 旧姿势)
//   改成: 调 opphub-knowledge-submit (v3.3 新姿势, idempotent + 冲突检测)
//   ingest-batch 退化成纯"编排入口" (one-shot submit a batch, 不做实际提交)
//
// v4.0.0 P1-3 改动: 临时文件改 mkdtemp 每次独立目录
//   旧实现固定 /tmp/opphub-ingest-batch-cards.json, 并发 ingest 互相覆盖
//   A 进程写 → B 进程覆盖 → A 的 submit 拿到 B 的 cards → 入库错乱
//   修: mkdtemp 每次独立目录, 完成后 cleanup
//
// 返 { ok, mode, total, submitted, deduplicated, conflicts, summary, nextStep }
//
// 用法: bot 调 (阶段 5 批量入库)
//   opphub knowledge-ingest-batch --cards cards.json --json
//   opphub knowledge-ingest-batch --cards cards.json --dry-run --json
//   opphub knowledge-ingest-batch --cards cards.json --force-override-conflict --json
//
// 输入 cards.json 格式 (knowledge-card 的输出):
//   { "cards": [{ "type": "ability", "dimension": "达人营销", "emoji": "✅", "text": "..." }, ...] }
//
//   - 不做去重 (submit bin + server 端做)
//   - 不做冲突判断 (server 端做)
//   - 不做版本管理 (server 端做)
//   - 不调 LLM (skill turn 的活)

import { readFileSync, existsSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { homedir, tmpdir } from "node:os";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SUBMIT_BIN = join(__dirname, "opphub-knowledge-submit.js");
const ADD_BIN = join(__dirname, "opphub-knowledge-add.js"); // 保留备查 (v3.1 老接口)

function parseArgs(argv) {
  const args = { _: [], forceOverrideConflict: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--cards") args.cards = argv[++i];
    else if (a === "--cards-out") args.cardsOut = argv[++i];
    else if (a === "--dry-run") args.dryRun = true;
    else if (a === "--force-override-conflict") args.forceOverrideConflict = true;
    else if (a === "--keep-tmp") args.keepTmp = true;  // v4 调试用, 默认 cleanup
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const wantJson = args.json;

  if (!args.cards) {
    const result = {
      ok: false,
      error: "missing_cards",
      message: "需要 --cards cards.json (knowledge-card 的输出) 或 --cards - (从 stdin 读, SKILL.md 阶段 5 例子姿势)",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  // A6 修: --cards - 走 stdin (SKILL.md 阶段 5 例子 `bin/opphub-knowledge-ingest-batch < cards.json`
  //                            v3.3 之前 bin 拒收 stdin, 现在接上)
  let cardsData;
  const t0 = Date.now();
  if (args.cards === "-") {
    try {
      const stdinText = readFileSync(0, "utf8");
      cardsData = JSON.parse(stdinText);
    } catch (e) {
      const result = {
        ok: false,
        error: "stdin_invalid_json",
        message: e?.message ?? String(e),
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
  } else {
    if (!existsSync(args.cards)) {
      const result = {
        ok: false,
        error: "cards_not_found",
        message: `cards 文件不存在: ${args.cards}`,
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
    try {
      cardsData = JSON.parse(readFileSync(args.cards, "utf8"));
    } catch (e) {
      const result = {
        ok: false,
        error: "invalid_cards_json",
        message: e?.message ?? String(e),
      };
      if (wantJson) console.log(JSON.stringify(result, null, 2));
      process.exit(1);
    }
  }

  const cards = cardsData.cards || cardsData; // 兼容直接传数组
  if (!Array.isArray(cards) || cards.length === 0) {
    const result = {
      ok: false,
      error: "no_cards",
      message: "cards 为空",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    process.exit(1);
  }

  if (args.dryRun) {
    const result = {
      ok: true,
      mode: "dry-run",
      cardCount: cards.length,
      preview: cards.slice(0, 3).map((c) => ({
        type: c.type,
        dimension: c.dimension,
        textLen: c.text?.length ?? 0,
      })),
      durationMs: Date.now() - t0,
      nextStep: "opphub knowledge-ingest-batch (去掉 --dry-run 调 submit)",
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.log(`[dry-run] 将调 submit 入库 ${cards.length} 条卡片`);
    return;
  }

  // v4.0.0 P1-3: 改 mkdtemp 每次独立目录 + cleanup
  // 旧实现固定 /tmp/opphub-ingest-batch-cards.json, 并发 ingest 互相覆盖
  // 修: 每次 mkdtempSync 创建独立目录, submit 完 rmSync 清理
  const tmpDir = args.cardsOut
    ? dirname(args.cardsOut)
    : mkdtempSync(join(tmpdir(), "opphub-ingest-batch-"));
  const tmpCards = args.cardsOut || join(tmpDir, "cards.json");
  writeFileSync(tmpCards, JSON.stringify(cardsData, null, 2));

  const submitArgs = [
    SUBMIT_BIN,
    "--cards", tmpCards,
    "--json",
  ];
  if (args.forceOverrideConflict) {
    submitArgs.push("--force-override-conflict");
  }

  let res;
  try {
    // spawnSync node <submit-script> (ClawHub audit flagged dangerous_exec)
    // 安全设计: 仅 spawn("node", argv), stdio pipe, timeout 120s, env 透传 (MOCK_TOKEN 等)
    // 业务必需: idempotent batch 编排入口, 调 submit 子 bin 处理每张卡
    res = spawnSync("node", submitArgs, {
      encoding: "utf8",
      timeout: 120_000,
      env: { ...process.env },  // 透传 env 让 submit 拿到 OPPHUB_API_BASE + MOCK_TOKEN (E2E mock / 真 server 都要)
    });
  } finally {
    // v4.0.0 P1-3: cleanup 临时目录
    //   不论 submit 成功失败, 都清, 避免残留公司能力信息
    //   --keep-tmp 跳过 cleanup (调试用)
    if (!args.keepTmp && !args.cardsOut) {
      try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
    }
  }

  if (res.error) {
    const result = {
      ok: false,
      mode: "submit-error",
      error: "submit_spawn_failed",
      message: res.error.message,
      durationMs: Date.now() - t0,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error("submit spawn 失败:", res.error.message);
    process.exit(1);
  }
  if (res.status !== 0) {
    const result = {
      ok: false,
      mode: "submit-failed",
      error: "submit_exit_failed",
      message: res.stderr || res.stdout,
      durationMs: Date.now() - t0,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error("submit exit 非 0:", res.stderr || res.stdout);
    process.exit(res.status || 1);
  }

  // submit 返了 JSON, 直接透传 + 加 wrapper 字段
  let submitResult;
  try {
    submitResult = JSON.parse(res.stdout);
  } catch (e) {
    const result = {
      ok: false,
      mode: "submit-invalid-json",
      error: "invalid_submit_response",
      message: e?.message ?? String(e),
      rawStdout: res.stdout,
      durationMs: Date.now() - t0,
    };
    if (wantJson) console.log(JSON.stringify(result, null, 2));
    else console.error("submit 返的 JSON 解析失败:", e?.message);
    process.exit(1);
  }

  const result = {
    ok: submitResult.ok ?? true,
    mode: "ingest-via-submit",
    total: cards.length,
    summary: submitResult.summary,
    submitted: submitResult.submitted,
    deduplicated: submitResult.deduplicated,
    conflicts: submitResult.conflicts,
    userId: submitResult.userId,
    nextStep: submitResult.nextStep,
    durationMs: Date.now() - t0,
  };

  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    if (result.summary.submitted > 0) {
      console.log(`✅ 新提交 ${result.summary.submitted} 条`);
    }
    if (result.summary.deduplicated > 0) {
      console.log(`🔁 幂等命中 ${result.summary.deduplicated} 条 (已存在, 跳过)`);
    }
    if (result.summary.conflicts > 0) {
      for (const c of result.conflicts) {
        const cf = c.conflictReport?.conflictFields?.join(", ") || c.conflictReport?.message || "?";
        console.log(`  card ${c.cardIndex} [${c.type}/${c.dimension}]: ${cf}`);
      }
    }
  }
}

main().catch((e) => {
  console.error("opphub-knowledge-ingest-batch fatal:", e?.message ?? e);
  process.exit(1);
});
