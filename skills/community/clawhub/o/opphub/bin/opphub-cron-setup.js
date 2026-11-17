#!/usr/bin/env node
// opphub-cron-setup.js · v4.0
// status: deprecated (v4 cron v3 起改 trigger plugin 写, peer 由 plugin 维护)
//
// 用途: 自动建 opphub-skill-daily-check cron 任务 (架构 B isolated + announce last)
//       幂等: 重复跑不会重复建, 自动覆盖原 config
//
// - 任务名固定 'opphub-skill-daily-check' (升级不变化)
// - 调度: cron "0 9 * * *" @ Asia/Shanghai (可配 OPPHUB_CRON_EXPR / OPPHUB_CRON_TZ)
// - argv: [node, bin/opphub-check-update.js]
//
// 1. 调 'openclaw cron list --json' 查 opphub-skill-daily-check 在不在
// 2. 在 → 返 'already_installed', 顺便报 last_run / next_run / enabled
// 3. 不在 → 调 'openclaw cron add' 建 (带 --force 防止重名)
// 4. 返 'created' + 新 cron id

import { exec, execFile, spawn } from "node:child_process";
import { promisify } from "node:util";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { existsSync, readFileSync } from "node:fs";
import http from "node:http";
import https from "node:https";
const execp = promisify(exec);

const CRON_NAME = "opphub-skill-daily-check";
const DEFAULT_EXPR = process.env.OPPHUB_CRON_EXPR || "0 9 * * *";
const DEFAULT_TZ = process.env.OPPHUB_CRON_TZ || "Asia/Shanghai";
// 与 skill/bin/opphub 在同目录, 引用绝对路径
const __dirname = dirname(fileURLToPath(import.meta.url));
const CHECK_UPDATE_BIN = join(__dirname, "opphub-check-update.js");

function out(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

function err(code, message, extra = {}) {
  out({ ok: false, error: code, message, ...extra });
  process.exit(1);
}
// execP: 业务必需的子进程调用 (ClawHub security audit flagged suspicious.dangerous_exec)
// 安全设计: 仅 argv 形式 spawn (不拼 shell 字符串), stdio 隔离, 不传用户输入到 shell
// 用途: openclaw cron / openclaw channels / macOS security 命令
function execP(cmd, args = [], opts = {}) {
  return new Promise((resolve, reject) => {
    const sp = spawn(cmd, args, { ...opts, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "", stderr = "";
    sp.stdout.on("data", d => (stdout += d.toString()));
    sp.stderr.on("data", d => (stderr += d.toString()));
    sp.on("error", reject);
    sp.on("close", code => {
      if (code === 0) resolve({ stdout, stderr });
      else reject(Object.assign(new Error(`${cmd} exit ${code}`), { code, stdout, stderr }));
    });
  });
}

async function cronListJson() {
  try {
    const { stdout } = await execP("openclaw", ["cron", "list", "--json"]);
    const objStart = stdout.indexOf("{");
    if (objStart < 0) return [];
    const obj = JSON.parse(stdout.slice(objStart));
    return Array.isArray(obj?.jobs) ? obj.jobs : (Array.isArray(obj) ? obj : []);
  } catch (e) {
    return [];
  }
}

async function cronExists() {
  const all = await cronListJson();
  return all.find((j) => j.name === CRON_NAME) ?? null;
}


// 从 credentials 读, 没读到返 null 让上层处理 (不硬编码 user ID, 公开包不能含内部 ID)
async function resolveDefaultUserOpenId() {
  const candidates = [
    join(process.env.HOME || "", ".openclaw/credentials/feishu-dev-allowFrom.json"),
    join(process.env.HOME || "", ".openclaw/credentials/feishu-dev-allowfrom.json"),
  ];
  for (const f of candidates) {
    if (existsSync(f)) {
      try {
        const arr = JSON.parse(readFileSync(f, "utf8"));
        if (Array.isArray(arr) && arr.length) return arr[0];
        if (arr?.open_id) return arr.open_id;
      } catch {}
    }
  }
  return null;
}


// 设计: skill 不再硬编码 channel, server 告诉 skill "我是谁 + 默认推哪"
async function fetchDefaultChannel(accessToken) {
  try {

    const url = new URL("https://api.opphub.ruiplus.cn/api/user/me");
    return await new Promise((resolve) => {
      const mod = url.protocol === "https:" ? https : http;
      const req = mod.request(url, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${accessToken}`,
          "Accept": "application/json",
        },
        timeout: 5000,
      }, (res) => {
        let body = "";
        res.on("data", (d) => (body += d));
        res.on("end", () => {
          if (res.statusCode === 404) {
            resolve({ source: "fallback_404", reason: "/api/user/me 404 (server 团队待实现)" });
            return;
          }
          if (res.statusCode !== 200) {
            resolve({ source: "fallback_error", reason: `HTTP ${res.statusCode}` });
            return;
          }
          try {
            const j = JSON.parse(body);
            // 期望: { ok: true, userId, channels: [{channelType, accountId, recipientId, isDefault}], defaultChannel: {...} }
            const def = j.defaultChannel ?? j.channels?.find((ch) => ch.isDefault) ?? null;
            if (!def) {
              resolve({ source: "fallback_no_default", reason: "server 返了但没 defaultChannel", data: j });
              return;
            }
            resolve({
              source: "server",
              channelType: def.channelType ?? def.type,
              accountId: def.accountId ?? def.account,
              recipientId: def.recipientId ?? def.to,
            });
          } catch (e) {
            resolve({ source: "fallback_parse_error", reason: e.message });
          }
        });
      });
      req.on("error", (e) => resolve({ source: "fallback_net_error", reason: e.message }));
      req.on("timeout", () => { req.destroy(); resolve({ source: "fallback_timeout" }); });
      req.end();
    });
  } catch (e) {
    return { source: "fallback_exception", reason: e.message ?? String(e) };
  }
}

async function darwinKeychainGet(account) {
  return new Promise((resolve) => {
    const sp = spawn("security", ["find-generic-password", "-s", "openclaw-opphub-uat", "-a", account, "-w"], { stdio: ["ignore", "pipe", "pipe"] });
    let out = "";
    sp.stdout.on("data", (d) => (out += d.toString()));
    sp.on("close", () => {
      const t = out.trim();
      if (!t) return resolve(null);
      try {
        // 与 plugin 同构: base64 decode (keychain -w 返 raw bytes 时会被 hex)
        return resolve(Buffer.from(t, "base64").toString("utf8"));
      } catch {
        return resolve(t);
      }
    });
    sp.on("error", () => resolve(null));
  });
}

async function cronAdd() {
  let delivery = { source: "alpha5_fallback" };
  try {
    const raw = await darwinKeychainGet("opphub:default");
    if (raw) {
      const token = JSON.parse(raw);
      const fromServer = await fetchDefaultChannel(token.access_token);
      if (fromServer.source === "server") {
        delivery = fromServer;
      } else {
        delivery.source = fromServer.source;
        delivery.reason = fromServer.reason;
      }
    } else {
      delivery.reason = "no token in keychain";
    }
  } catch (e) {
    delivery.reason = e.message ?? String(e);
  }

  if (delivery.source !== "server") {
    delivery.channelType = "feishu";
    delivery.accountId = "dev";
    delivery.recipientId = await resolveDefaultUserOpenId();
  }

  const argv = ["node", CHECK_UPDATE_BIN];
  const args = [
    "cron", "add",
    "--cron", DEFAULT_EXPR,
    "--tz", DEFAULT_TZ,
    "--name", CRON_NAME,
    "--description", "opphub skill daily check · check update, not 撮合",
    "--session", "isolated",
    `--channel=${delivery.channelType}`,
    `--account=${delivery.accountId}`,
    `--to=${delivery.recipientId}`,
    "--announce", "--best-effort-deliver",
    "--command-argv", JSON.stringify(argv),
  ];
  // args[0]='cron', args[1]='add', execP("openclaw", [...]) 跳过这两个
  const { stdout, stderr } = await execP("openclaw", ["cron", "add", ...args.slice(2)]);
  return { stdout, stderr, delivery };
}

// 查 cron 状态 (含 enabled / last / next)
function shapeCron(j) {
  if (!j) return null;
  return {
    id: j.id ?? j.ID ?? null,
    name: j.name ?? null,
    enabled: j.enabled ?? true,
    schedule: j.schedule ?? j.expr ?? null,
    tz: j.tz ?? null,
    last_run_at: j.lastRunAt ?? j.last_run_at ?? null,
    next_run_at: j.nextRunAt ?? j.next_run_at ?? null,
    last_status: j.lastStatus ?? j.last_status ?? null,
    delivery: j.delivery ?? null,
    session_target: j.sessionTarget ?? j.session_target ?? null,
  };
}

async function main() {
  const cmd = process.argv[2] || "setup";

  if (cmd === "status") {
    const existing = await cronExists();
    if (!existing) {
      out({ ok: true, installed: false, hint: "cron 未建, 跑 'opphub cron-setup' 自动建" });
      return;
    }
    out({
      ok: true,
      installed: true,
      cron: shapeCron(existing),
      hint: "cron 已建, 每天跑一次. token/插件 检查走 status 的其他字段",
    });
    return;
  }

  if (cmd === "setup") {
    const existing = await cronExists();
    if (existing) {
      const d = existing?.delivery ?? {};
      const fromServerOrFallback = d.accountId && d.to ? {
        source: "server_or_fallback",
        channelType: d.channel,
        accountId: d.accountId,
        recipientId: d.to,
      } : { source: "unknown" };
      out({
        ok: true,
        action: "already_installed",
        cron: shapeCron(existing),
        delivery: fromServerOrFallback,
        hint: "幂等: 重复跑不会重复建 (delivery 配置从现有 cron 读)",
      });
      return;
    }
    try {
      const cronAddResult = await cronAdd();
      const { stdout, stderr } = cronAddResult;
      // 验证再建一次 (避免 --name 不接受重名 也 看不到错误)
      const after = await cronExists();
      if (!after) {
        err("cron_add_failed", "cron add 命令返了但查不到. 命令输出:" + (stdout || stderr).slice(0, 500));
      }
      out({
        ok: true,
        action: "created",
        cron: shapeCron(after),
        schedule_human: `${DEFAULT_EXPR} @ ${DEFAULT_TZ}`,
        argv: ["node", CHECK_UPDATE_BIN],
        delivery_source: cronAddResult.delivery.source,
        delivery: cronAddResult.delivery,
        hint: cronAddResult.delivery.source === "server"
          ? "cron 每天 09:00 跑 check-update, 推送到 server 给的 defaultChannel"
          : "cron 每天 09:00 跑 check-update, fallback 到本地 defaultChannel",
      });
      return;
    } catch (e) {
      err("cron_add_error", e.message ?? String(e), { stderr: e.stderr ?? null });
    }
    return;
  }

  err("unknown_command", `unknown subcommand: ${cmd} (可用: setup / status)`);
}

main().catch((e) => err("internal_error", e.message ?? String(e)));
