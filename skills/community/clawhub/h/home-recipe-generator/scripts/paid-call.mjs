#!/usr/bin/env node
// -*- coding: utf-8 -*-
/**
 * 家常菜谱生成 — 付费调用脚本（AI 按量付费 / A2M）
 *
 * 三阶段，与支付宝 402 协议一一对应：
 *   probe     请求资源接口，未付款时拿到 HTTP 402 + Payment-Needed 账单并落盘
 *   pay       把账单和原始请求交给官方买家 CLI，展示支付入口等用户付款
 *   complete  付款后按原订单查询并取回资源，不重新下单
 *
 * 本脚本不接触任何密钥，也不自行实现签名或付款，只做编排。
 *
 * 依赖（买家侧，安装一次即可）：
 *   npx -y @alipay/agent-payment@latest install
 */
import { execFile } from "node:child_process";
import { mkdir, readFile, writeFile, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

// ===== 本技能固定配置 =====
const SLUG = "home-recipe-generator";
const RESOURCE_URL = "https://skillpay-aipay.app.workbuddy.host/skills/" + SLUG;
const PRICE = "0.10"; // 元/次；与支付宝服务登记价、SkillHub 展示价三处一致
const STATE_VERSION = 1;
// =========================

const TIMEOUT_MS = 60_000;

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) {
        out[key] = true;
      } else {
        out[key] = next;
        i += 1;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

function die(msg) {
  console.error("❌ " + msg);
  process.exit(1);
}

function statePaths(stateDir) {
  return {
    dir: stateDir,
    challenge: path.join(stateDir, "payment-needed.txt"),
    state: path.join(stateDir, "state.json"),
  };
}

async function loadState(stateDir) {
  const p = statePaths(stateDir);
  if (!existsSync(p.state)) die("未找到会话状态，请先执行 probe");
  const raw = await readFile(p.state, "utf8");
  const st = JSON.parse(raw);
  if (st.version !== STATE_VERSION) die("状态文件版本不匹配，请重新执行 probe");
  return st;
}

/** probe：请求资源接口，预期 402，保存账单与原始请求。 */
async function probe(args) {
  const input = args.input ?? args._?.[0] ?? "";
  if (!input) die("缺少 --input（需要处理的原始内容）");
  const stateDir = args["state-dir"] || path.join(".state", SLUG);
  const p = statePaths(stateDir);
  await mkdir(stateDir, { recursive: true });

  const body = JSON.stringify({ input });
  const curlArgs = [
    "-sS",
    "-D", p.challenge + ".headers",
    "-o", p.challenge + ".body",
    "-w", "HTTP_STATUS:%{http_code}",
    "-X", "POST",
    "-H", "Content-Type: application/json",
    "--data-binary", body,
    "--connect-timeout", "10",
    "--max-time", "30",
    RESOURCE_URL,
  ];

  let stdout = "";
  try {
    ({ stdout } = await execFileAsync("curl", curlArgs, { timeout: TIMEOUT_MS }));
  } catch (err) {
    die("请求资源接口失败：" + (err.message || err));
  }

  const status = Number(String(stdout).match(/HTTP_STATUS:(\d+)/)?.[1] ?? 0);
  const headers = await readFile(p.challenge + ".headers", "utf8");

  if (status === 200) {
    // 已付款或免费直达：直接输出结果
    const bodyText = await readFile(p.challenge + ".body", "utf8");
    console.log("✅ 直接取得资源（HTTP 200）：");
    console.log(bodyText);
    return;
  }
  if (status !== 402) {
    const bodyText = await readFile(p.challenge + ".body", "utf8").catch(() => "");
    die(`资源接口返回 HTTP ${status}，预期 402。响应：${String(bodyText).slice(0, 300)}`);
  }

  const m = headers.match(/payment-needed:\s*([^\r\n]+)/i);
  if (!m) die("HTTP 402 响应缺少 Payment-Needed 响应头");
  const paymentNeeded = m[1].trim();
  await writeFile(p.challenge, paymentNeeded, { encoding: "utf8", mode: 0o600 });

  const sessionId = `${SLUG}-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  const state = {
    version: STATE_VERSION,
    slug: SLUG,
    sessionId,
    resourceUrl: RESOURCE_URL,
    method: "POST",
    data: body,
    headers: ["Content-Type: application/json"],
    price: PRICE,
    createdAt: new Date().toISOString(),
  };
  await writeFile(p.state, JSON.stringify(state, null, 2), { encoding: "utf8", mode: 0o600 });

  // 账单摘要（不含签名等敏感内容）
  let amount = "";
  let goods = "";
  try {
    const bill = JSON.parse(Buffer.from(paymentNeeded, "base64url").toString("utf8"));
    amount = bill?.protocol?.amount ?? "";
    goods = bill?.method?.goods_name ?? "";
  } catch {
    /* 解不出就只展示状态码 */
  }

  console.log("💰 收到付款账单（HTTP 402）");
  console.log(`   技能：${goods || SLUG}`);
  console.log(`   金额：¥${amount || PRICE} / 次`);
  console.log(`   会话：${sessionId}`);
  console.log(`   状态目录：${stateDir}`);
  console.log("");
  console.log("下一步：node scripts/paid-call.mjs pay --state-dir " + stateDir);
}

/** pay：把账单和原始请求交给官方买家 CLI，等用户付款。 */
async function pay(args) {
  const stateDir = args["state-dir"] || path.join(".state", SLUG);
  const st = await loadState(stateDir);
  const p = statePaths(stateDir);

  const cliArgs = [
    "402-buyer-pay",
    "--session-id", st.sessionId,
    "--file", p.challenge,
    "--resource-url", st.resourceUrl,
    "--method", st.method,
    "--data", st.data,
    ...st.headers.flatMap((h) => ["--header", h]),
    "--intent-summary", `种草图文笔记创作 付费调用，¥${st.price}/次`,
  ];
  if (args.json) cliArgs.push("--json");

  console.log("→ alipay-bot " + cliArgs.join(" "));
  try {
    const { stdout, stderr } = await execFileAsync("alipay-bot", cliArgs, {
      timeout: 5 * 60_000,
      maxBuffer: 8 * 1024 * 1024,
    });
    if (stdout) process.stdout.write(stdout);
    if (stderr) process.stderr.write(stderr);
  } catch (err) {
    die("支付命令执行失败：" + (err.message || err) + "\n请先安装买家侧依赖：npx -y @alipay/agent-payment@latest install");
  }
  console.log("");
  console.log("付款完成后执行：node scripts/paid-call.mjs complete --state-dir " + stateDir + " --out-shake-no <订单号>");
}

/** complete：按原订单查询并取回资源，不重新下单。 */
async function complete(args) {
  const stateDir = args["state-dir"] || path.join(".state", SLUG);
  const st = await loadState(stateDir);
  const outShakeNo = args["out-shake-no"] || args.trade || "";
  if (!outShakeNo) die("缺少 --out-shake-no（付款后得到的订单号）");

  const cliArgs = [
    "402-query-payment-status",
    "--out-shake-no", outShakeNo,
    "--resource-url", st.resourceUrl,
    "--method", st.method,
    "--data", st.data,
    ...st.headers.flatMap((h) => ["--header", h]),
  ];

  console.log("→ alipay-bot " + cliArgs.join(" "));
  try {
    const { stdout, stderr } = await execFileAsync("alipay-bot", cliArgs, {
      timeout: 5 * 60_000,
      maxBuffer: 8 * 1024 * 1024,
    });
    if (stdout) process.stdout.write(stdout);
    if (stderr) process.stderr.write(stderr);
  } catch (err) {
    die("查询/取资源失败：" + (err.message || err));
  }
}

/** reset：清理本地会话状态。 */
async function reset(args) {
  const stateDir = args["state-dir"] || path.join(".state", SLUG);
  await rm(stateDir, { recursive: true, force: true });
  console.log("已清理：" + stateDir);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args._[0] || "probe";
  switch (cmd) {
    case "probe":
      return probe(args);
    case "pay":
      return pay(args);
    case "complete":
      return complete(args);
    case "reset":
      return reset(args);
    case "info":
      console.log(JSON.stringify({ slug: SLUG, resourceUrl: RESOURCE_URL, price: PRICE }, null, 2));
      return;
    default:
      die("未知子命令：" + cmd + "（可用：probe | pay | complete | reset | info）");
  }
}

main().catch((err) => {
  console.error("❌ " + (err?.message || err));
  process.exit(1);
});
