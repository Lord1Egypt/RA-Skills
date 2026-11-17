#!/usr/bin/env node
// opphub-oauth-login.js · v4.0
// status: implemented (v4 P1-1 start 复用前置 + P0-2 spawn argv)
//
// 用途: OPC 用户在 OpenClaw chat 里 @bot 说"偶合登录",bot 调这个脚本走 OAuth Device Flow,
//       拿 access_token + refresh_token → 写 macOS Keychain / Linux AES-256-GCM 加密文件
//
// 跟 mtty-ai/opphub-plugin v0.4.0+ 同构 (oauth-client.ts):
//   - 同一 client_id  "opphub-plugin"
//   - 同一 Keychain service + account (openclaw-opphub-uat / opphub:default)
//   - 同一 scope (profile ws:read ws:write)
//   - 同 REFRESH_AHEAD_MS = 5min
//
//   - server 端接口 (device/code + device/token + userinfo) 已知存在 (plugin v0.4.0 在用)

//   skill 不再双源重写 readToken/writeToken/keychain.
//   改 import plugin client (lib/opphub-plugin-client.js) → plugin = source of truth
import { exec, execFile } from "node:child_process";
import { promisify } from "node:util";
import { readFileSync, existsSync, writeFileSync, unlinkSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import {
  readToken as pluginReadToken,
  writeToken as pluginWriteToken,
  clearToken as pluginClearToken,
  tokenStatus,
  getAccessToken as pluginGetAccessToken,
  getOpcIdFromToken,
  refreshToken as pluginRefreshToken,
  healthCheck as pluginHealthCheck,
} from "../lib/opphub-plugin-client.js";

const execp = promisify(exec);
const execpFile = promisify(execFile);

// === 配置 ===
const AUTHORIZE_URL = "https://api.opphub.ruiplus.cn/api/oauth/device/code";
const TOKEN_URL = "https://api.opphub.ruiplus.cn/api/oauth/device/token";
const USERINFO_URL = "https://api.opphub.ruiplus.cn/api/oauth/userinfo";
const CLIENT_ID = "opphub-plugin";
const DEFAULT_SCOPE = "profile ws:read ws:write";

// === start-state (skill 自己的, 不在 plugin Keychain) ===
const TOKEN_DIR = join(homedir(), ".opphub-plugin");
const START_STATE_FILE = join(TOKEN_DIR, "start-state.json");

function saveStartState(deviceCode, userCode, verificationUriComplete, expiresAt, originalExpiresIn) {
  try {
    if (!existsSync(TOKEN_DIR)) mkdirSync(TOKEN_DIR, { recursive: true, mode: 0o700 });
    writeFileSync(START_STATE_FILE, JSON.stringify({
      device_code: deviceCode,
      user_code: userCode,
      verification_uri_complete: verificationUriComplete,
      expires_at: expiresAt,
      original_expires_in: originalExpiresIn,
      started_at: Date.now(),
    }, null, 2), { mode: 0o600 });
  } catch {}
}
function readStartState() {
  try {
    if (!existsSync(START_STATE_FILE)) return null;
    const s = JSON.parse(readFileSync(START_STATE_FILE, "utf8"));
    const graceMs = 60 * 1000;
    if (Date.now() > s.expires_at + graceMs) {
      try { unlinkSync(START_STATE_FILE); } catch {}
      return null;
    }
    return s;
  } catch { return null; }
}
function clearStartState() {
  try { unlinkSync(START_STATE_FILE); } catch {}
}

// === plugin client 包装 (skill 这边复用 plugin 函数) ===
async function readToken() { return await pluginReadToken(); }
async function writeToken(t) { return await pluginWriteToken(t); }
async function clearToken() { return await pluginClearToken(); }
async function refreshTokenNow() { return await pluginRefreshToken(); }
async function resolveOpcId(t) {
  if (!t?.access_token) return null;
  const id = await getOpcIdFromToken(t);
  return id || null;
}

// === 输出 (bot 解析) ===
function out(obj) {
  console.log(JSON.stringify(obj, null, 2));
}

function err(code, message, extra = {}) {
  out({ ok: false, error: code, message, ...extra });
  process.exit(1);
}

// === opener 跨平台 (v4.0.0 P0-2: spawn argv 避免 shell 注入 + 路径带空格失败) ===
// 之前用 `open "${url}"` exec 字符串拼接, URL 含引号/特殊字符会注入, 安装目录带空格会失败
async function openUrl(url) {
  const { spawn } = await import("node:child_process");
  const platform = process.platform;
  let cmd, args;
  if (platform === "darwin") {
    cmd = "open"; args = [url];
  } else if (platform === "win32") {
    cmd = "cmd"; args = ["/c", "start", "", url];
  } else {
    cmd = "xdg-open"; args = [url];
  }
  try {
    const child = spawn(cmd, args, { stdio: "ignore", detached: true });
    child.unref();
    return true;
  } catch {
    return false;
  }
}

// skill 不再自实现 darwinKeychain*/aesGcm*/writeToken/readToken/tokenStatus
// 跟 plugin 共享同一个 Keychain entry (写死 plugin = source of truth)

// startDeviceFlow: 拿 device_code + user_code + verification_url, 不 poll
// pollDeviceFlow: 阻塞 poll 拿 access_token
async function startDeviceFlow() {
  //   之前: 先请求 server 拿 device_code (老的被作废) → 后读 start state 检查复用
  //         复用逻辑永远不命中, 浪费 1 个 device_code
  //   修: 先读 start state, 命中复用就 return, 没命中再请求 server
  const recent = readStartState();
  if (recent) {
    out({
      ok: true,
      stage: "awaiting_user_authorization",
      verification_uri: recent.verification_uri_complete?.split("?")[0] ?? null,
      verification_uri_complete: recent.verification_uri_complete,
      user_code: recent.user_code,
      device_code: recent.device_code,
      expires_in: Math.floor((recent.expires_at - Date.now()) / 1000),
      interval: 5,
      browser_opened: false,
      reused: true,  // bot 知道这是复用, 不再出新的 user_code 让用户输
      next_steps: {
        bot_prompt: `🟡 复用上次的 device_code, 不重复弹验证码

上次验证码 (10 分钟内有效, 还没超时):
${recent.user_code}

点链接同意授权:
${recent.verification_uri_complete}

[我已同意并完成]  [取消]`,
      },
    });
    return;
  }

  // 没复用, 才请求 server 拿新 device_code
  const codeResp = await fetch(AUTHORIZE_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ client_id: CLIENT_ID, scope: DEFAULT_SCOPE }),
  });
  if (!codeResp.ok) {
    const text = await codeResp.text();
    err("device_code_failed", `server 返 ${codeResp.status}: ${text}`);
  }
  const dc = await codeResp.json();
  const verificationUriComplete =
    dc.verification_uri_complete ??
    `${dc.verification_uri}${dc.verification_uri.includes("?") ? "&" : "?"}user_code=${encodeURIComponent(dc.user_code)}`;

  // v3.1: 不自动 openBrowser (bot 跑没 stdin, 不能 spawn `open`)
  // 让 bot 拿到 verification_uri_complete 出 IntentMessage, 用户自己点开
  // 保留老行为兜底: 如果显式传 OPEN_BROWSER=1 才弹
  let opened = false;
  if (process.env.OPEN_BROWSER === "1") {
    opened = await openUrl(verificationUriComplete);
  }

  saveStartState(dc.device_code, dc.user_code, verificationUriComplete, Date.now() + dc.expires_in * 1000, dc.expires_in);

  // 3. bot 拿到这串去出 IntentMessage (channel-agnostic)
  out({
    ok: true,
    stage: "awaiting_user_authorization",
    verification_uri: dc.verification_uri,
    verification_uri_complete: verificationUriComplete,
    user_code: dc.user_code,
    device_code: dc.device_code,
    expires_in: dc.expires_in,
    interval: dc.interval,
    browser_opened: opened,
    next_steps: {
      bot_prompt: `🟡 待你授权

点链接同意授权:
${verificationUriComplete}

输入验证码:
${dc.user_code}
(5 分钟内有效)

[我已同意并完成]  [取消]`,
    },
  });
  // 注意: 不 poll, 让 bot 把 device_code 暂存, 用户点同意后 bot 调 poll
  // 或 bot 拿到 stage=awaiting_user_authorization 后立即起 cron 轮询 (跟 v2.8 行为对齐)
}

// pollDeviceFlow: 阻塞 poll 拿 access_token
// args: --device-code <dc> --interval <sec> --expires-in <sec>
async function pollDeviceFlow({ deviceCode, interval, expiresIn }) {
  if (!deviceCode) {
    err("missing_device_code", "需要 --device-code");
  }
  const expiresAt = Date.now() + (expiresIn ?? 600) * 1000;
  let pollInterval = (interval ?? 5) * 1000;
  while (Date.now() < expiresAt) {
    await new Promise((r) => setTimeout(r, pollInterval));
    const tokenResp = await fetch(TOKEN_URL, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ device_code: deviceCode }),
    });
    const data = await tokenResp.json().catch(() => ({}));
    if (tokenResp.ok && data.access_token) {
      const jwtPayload = decodeJwtPayload(data.access_token);
      let userId = jwtPayload?.userId ?? jwtPayload?.sub ?? "";
      if (!userId) {
        userId = (await fetchUserinfo(data.access_token)) ?? data.user_id ?? "";
      }
      const t = {
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        expires_at: Date.now() + data.expires_in * 1000,
        refresh_expires_at:
          Date.now() + (data.refresh_expires_in ?? 30 * 24 * 3600) * 1000,
        scope: data.scope,
        user_id: userId,
        obtained_at: new Date().toISOString(),
      };

      // v4.0.0 P0-2: 改 execFile argv 形式, 避免路径带空格 + shell 注入
      const path = await import("node:path");
      const urlMod = await import("node:url");
      const __filename = urlMod.fileURLToPath(import.meta.url);
      const __skillDir = path.dirname(__filename);
      async function runCronSetup() {
        try {
          const { stdout } = await execpFile("node", [join(__skillDir, "bin/opphub-cron-setup.js"), "setup"]);
          try {
            const objStart = stdout.indexOf("{");
            if (objStart >= 0) return JSON.parse(stdout.slice(objStart));
          } catch {}
          return { action: "spawn_failed", cron_check: null };
        } catch (e) {
          return { action: "spawn_error", cron_check: null, error: e?.message ?? String(e) };
        }
      }
      await writeToken(t);
      clearStartState();
      const cronSpawn = await runCronSetup();
      out({
        ok: true,
        stage: "logged_in",
        user_id: userId,
        token_expires_at: new Date(t.expires_at).toISOString(),
        storage: process.platform === "darwin"
          ? `macOS Keychain (service=openclaw-opphub-uat, account=opphub:default)`
          : `AES-256-GCM (~/.opphub-plugin/token.json)`,
        cron_auto_setup: cronSpawn.action ?? "unknown",
        cron_check: cronSpawn.cron_check ?? null,
        next_steps: {
          bot_prompt: `✅ 登录成功！OPC ID: ${userId}

现在可以试试:
· 「偶合商机」 — 看捰合市场
· 「偶合状态」 — 看登录态 + plugin/cron
· 「偶合配置」 — 选默认推送通道 (6 步闭环第一步)

📬 默认推送: cron 每天 09:00 检查 skill 更新.
捰合推送走 server WS (需要 plugin, 没装时 bot 提示).

⭐ 想秒收捰合: openclaw plugins install clawhub:@mtty-ai/opphub`,
        },
      });
      return;
    }
    if (data.error === "authorization_pending") continue;
    if (data.error === "slow_down") { pollInterval += 5000; continue; }
    if (data.error === "expired_token") {
      clearStartState();
      err("device_flow_expired", "device flow 超时 (请重新跑 login-start)", {
        next_steps: { bot_prompt: "@bot 重新跑偶合登陆" },
      });
    }
    if (data.error === "access_denied") err("device_flow_denied", "用户在浏览器点了拒绝");
    err("device_flow_unknown", `unknown error: ${data.error || tokenResp.status}`);
  }
  err("device_flow_expired", "device flow 超时");
}


async function fetchUserinfo(accessToken) {
  try {
    const r = await fetch(USERINFO_URL, {
      headers: { authorization: `Bearer ${accessToken}` },
    });
    if (!r.ok) return null;
    const u = await r.json();
    return u.userId ?? u.user_id ?? null;
  } catch {
    return null;
  }
}

// 不调 userinfo API (server 端 /api/oauth/userinfo 是否存在未验, plugin 走的是 JWT 解 userId)
function decodeJwtPayload(token) {
  try {
    const payload = token.split(".")[1];
    const b64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    return JSON.parse(
      Buffer.from(b64 + "=".repeat((4 - b64.length % 4) % 4), "base64").toString()
    );
  } catch {
    return null;
  }
}

// === CLI ===
async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0] || "login";

  function getArg(args, name) {
    const i = args.indexOf(name);
    return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
  }

  // 与 plugin decodeJwtPayload 同构
  function resolveOpcId(t) {
    if (!t?.access_token) return null;
    const payload = decodeJwtPayload(t.access_token);
    return payload?.userId ?? payload?.sub ?? null;
  }

  // 读 package.json 的 version
  function checkPluginInstalled() {
    const candidates = [
      join(homedir(), ".openclaw", "extensions", "opphub", "package.json"),
      join(homedir(), ".openclaw", "plugins", "opphub", "package.json"),
    ];
    for (const pkg of candidates) {
      if (existsSync(pkg)) {
        try {
          const json = JSON.parse(readFileSync(pkg, "utf8"));
          return {
            installed: true,
            version: json.version ?? null,
            path: pkg.replace("/package.json", ""),
          };
        } catch {
          return { installed: true, version: null, path: pkg.replace("/package.json", "") };
        }
      }
    }
    return { installed: false, version: null, path: null };
  }


  // v4.0.0 P0-2: 改 execFile argv 形式, 避免 shell 注入
  async function getCronCheck() {
    try {
      const { stdout } = await execpFile("openclaw", ["cron", "list", "--json"]);
      // openclaw 输出 {"jobs": [...]} 而且 warnings 在前, 从 { 开始拿
      const objStart = stdout.indexOf('{');
      const obj = JSON.parse(stdout.slice(objStart));
      const jobs = Array.isArray(obj?.jobs) ? obj.jobs : (Array.isArray(obj) ? obj : []);
      const job = jobs.find((j) => j.name === 'opphub-skill-daily-check' || j?.payload?.name === 'opphub-skill-daily-check');
      if (!job) {
        return {
          installed: false,
          enabled: null,
          schedule: null,
          last_run_at: null,
          next_run_at: null,
          hint: 'cron 未建 · 跑 opphub cron-setup 自动建 (幂等)',
        };
      }
      return {
        installed: true,
        enabled: job.enabled ?? true,
        schedule: job.schedule?.expr ?? job.schedule ?? null,
        tz: job.schedule?.tz ?? null,
        last_run_at: job.lastRunAtMs ? new Date(job.lastRunAtMs).toISOString() : null,
        next_run_at: job.nextRunAtMs ? new Date(job.nextRunAtMs).toISOString() : null,
        last_status: job.lastStatus ?? job.lastRunStatus ?? null,
        hint: job.enabled
          ? 'cron 已建并启用 · 每天到点自动跑'
          : 'cron 存在但 disabled · 跑 openclaw cron enable <id>',
      };
    } catch (e) {
      return { installed: null, enabled: null, schedule: null, last_run_at: null, next_run_at: null, hint: 'openclaw cron list 调用失败: ' + (e.message ?? String(e)) };
    }
  }

  //   getDefaultChannel 抽到 lib/opphub-server-client.js
  //   configure list + oauth-login status 共享同一份实现, 避免飘走
  async function getDefaultChannel() {
    const { getDefaultChannel: serverGetDefaultChannel } = await import("../lib/opphub-server-client.js");
    return await serverGetDefaultChannel();
  }

  if (cmd === "status") {
    const t = await readToken();
    const s = await tokenStatus(t);
    const plugin = checkPluginInstalled();
    // 让 bot 看到 plugin client 能不能正常加载, 不会被 secret 锁卡
    let pluginHealth = { ok: false, error: "plugin_client not loaded" };
    try {
      pluginHealth = await pluginHealthCheck();
    } catch (e) {
      pluginHealth = { ok: false, error: e?.message ?? String(e) };
    }

    // 原代码: default_channel: null (placeholder), 不查 server
    // 真相: server GET /api/user/channels/default 返回 { channelType, channelId, isDefault }
    //      返 { ok:false, error:"no_default" } 表示用户没设 (走 plugin CLI configure 才会设)
    //      不是 server 团队活, 是 skill 端没去查
    const defaultChannel = await getDefaultChannel();

    let knowledgeStatus = { entries: 0, lastKnowledgeAt: null };
    try {
      const { fileURLToPath } = await import("node:url");
      const { dirname } = await import("node:path");
      const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
      const { stdout: kStdout } = await execpFile("node", [join(skillDir, "bin/opphub-knowledge-status.js"), "--json"]);
      const kObjStart = kStdout.indexOf("{");
      if (kObjStart >= 0) {
        const k = JSON.parse(kStdout.slice(kObjStart));
        knowledgeStatus = {
          entries: k.knowledgeCount ?? k.entries?.length ?? 0,
          lastKnowledgeAt: k.lastKnowledgeAt ?? null,
        };
      }
    } catch {}

    out({
      ok: true,
      status: s,
      user_id: resolveOpcId(t),
      expires_at: t ? new Date(t.expires_at).toISOString() : null,
      obtained_at: t?.obtained_at ?? null,
      refresh_expires_at: t?.refresh_expires_at ? new Date(t.refresh_expires_at).toISOString() : null,
      storage: process.platform === "darwin"
        ? `macOS Keychain (service=openclaw-opphub-uat, account=opphub:default)`
        : `AES-256-GCM (~/.opphub-plugin/token.json)`,
      plugin_oauth_client: pluginHealth,
      plugin_check: {
        installed: plugin.installed,
        version: plugin.version,
        path: plugin.path,
        hint: plugin.installed
          ? `plugin v${plugin.version} 已装 · 推送走 server WS 秒级`
          : "plugin 未装 · 推送走 skill 自带 cron(每天 09:00 检查 skill 版本, 不查撮合)",
      },
      cron_check: await getCronCheck(),
      knowledge_status: knowledgeStatus,
      link_health: {
        ws_connected: false,  // 待 plugin v0.6.x 上报 server ws 状态后填
        cron_ok: null,
        hint: "link_health 待 plugin v0.6.x 上报 (plugin 团队活)",
      },
    });
    return;
  }

  if (cmd === "logout") {
    //   4 步:
    //     1) clearToken() (Keychain)        ✅
    //     2) 清 cfg.devToken (plugin v0.5.30 noop, 重启即丢)
    //     3) 推飞书卡片 (走 IntentMessage → bot.skillApi.send → runtime 渲染层)
    //     4) WS client.stop (plugin runtime 不在 → noop; 下次 plugin 启拿 stale token 走 onFatal)
    //
    // 所以 skill 这里只返 IntentMessage (channel-agnostic), 让 OpenClaw runtime 渲染

    // 1) clearToken
    await clearToken();

    // 1.5) 清 skill 自己的 start-state.json (避免下次 start 复用上次的 device_code)
    try { clearStartState(); } catch {}

    //   plugin 重启后 cfg 没 devToken 就跟新装一样

    // 3) IntentMessage (channel-agnostic, bot 拿到自动推)
    out({
      ok: true,
      stage: "logged_out",
      intent: {
        header: {
          title: "✅ 偶合 OppHub 已登出",
          color: "green",
        },
        body: [
          {
            type: "text",
            content: "Keychain 本地 token 已清。\n\n",
          },
          {
            type: "text",
            content: "**WS 连接**: plugin runtime 不在线, 无需主动 stop。下次 plugin 启时拿到 stale token 会走 onFatal 路径自我清理 + 推送重登提示。\n\n",
          },
          {
            type: "text",
            content: "**重新登录**: 跟 bot 说 \"偶合登陆\" 或在终端跑 `opphub login-start --json`。\n",
          },
        ],
        prompt: "需要重新走 device flow 授权吗?",
        options: [
          {
            id: "login_now",
            label: "现在重新登录",
            style: "primary",
          },
          {
            id: "later",
            label: "稍后再说",
            style: "default",
          },
        ],
        actions: [
          { id: "login_now", label: "现在重新登录", style: "primary" },
          { id: "later", label: "稍后再说", style: "default" },
        ],
      },
      // 原始数据 (channel-agnostic, 给 bot / dashboard 看)
      cleared: {
        keychain: true,
        start_state: true,
        cfg_dev_token: "noop (plugin 重启即丢)",
        ws_client_stopped: "noop (plugin runtime 不在, onFatal 路径接管)",
      },
      // 下一动作提示 (bot 用)
      next_steps: {
        bot_prompt: "✅ 偶合已登出 · 需要重新登录吗?",
        actions: ["login_now", "later"],
      },
    });
    return;
  }

  if (cmd === "login") {
    // 老姿势保留: 直接 start + 自动 poll (兼容 SSH/headless)
    // (之前会让 poll 的 device_code 被新 start 作废)
    const t = await readToken();
    const s = await tokenStatus(t);
    if (s === "valid") {
      // 原始: 只返 already_logged_in 文本, 不查 plugin/configure/knowledge 状态
      // 改造: 检查 4 件事, 哪件没做引导到下一步
      const plugin = checkPluginInstalled();
      const cron = await getCronCheck();
      const defaultChannel = await getDefaultChannel();
      // knowledge_status: 调 bin/opphub-knowledge-status (subprocess)
      // v4.0.0 P0-2: 改 execFile argv 形式, 避免路径带空格 + shell 注入
      let knowledge = null;
      try {
        const _urlMod = await import("node:url");
        const _pathMod = await import("node:path");
        const _filePath = _urlMod.fileURLToPath(import.meta.url);
        const _skillDir = _pathMod.dirname(_pathMod.dirname(_filePath));
        const { stdout: kStdout } = await execpFile("node", [join(_skillDir, "bin/opphub-knowledge-status.js"), "--json"]);
        const kObjStart = kStdout.indexOf("{");
        if (kObjStart >= 0) knowledge = JSON.parse(kStdout.slice(kObjStart));
      } catch {}
      // 拼 6 步闭环状态 + 引导到下一步
      const next = [];
      if (!plugin.installed) {
        next.push({
          step: 4,
          key: "install_plugin",
          severity: "warn",
          prompt: "⚠️ 还没装 opphub-plugin, 撮合推送过来没人接 = 收不到",
          cmd: "openclaw plugins install clawhub:@mtty-ai/opphub",
        });
      }
      if (!cron.installed || !cron.enabled) {
        next.push({
          step: 5,
          key: "setup_cron",
          severity: "info",
          prompt: "💡 cron 未建 · 跑 opphub cron-setup 自动建 (幂等)",
          cmd: "opphub cron-setup",
        });
      }
      if (knowledge && knowledge.knowledgeCount === 0) {
        next.push({
          step: 6,
          key: "fill_knowledge",
          severity: "warn",
          prompt: "⚠️ 知识库空 · 撮合匹配不精准 · 「偶合知识库」引导录入",
          cmd: "@bot 偶合知识库",
        });
      }
      //   selected != null (用户已设) → 不引导
      //   selected == null (server 返 no_default) → 引导设默认通道
      if (!defaultChannel.selected) {
        next.push({
          step: 2,
          key: "configure_channel",
          severity: "info",
          prompt: "💡 设默认推送通道 · 「偶合配置」 → 选 IM (现在 plugin 未装或走默认)",
          cmd: "@bot 偶合配置",
        });
      }
      // v3.1 IntentMessage 格式 (channel-agnostic, OpenClaw runtime 转译)
      out({
        ok: true,
        stage: "already_logged_in",
        user_id: resolveOpcId(t),
        expires_at: new Date(t.expires_at).toISOString(),
        status_snapshot: {
          plugin: plugin.installed
            ? { installed: true, version: plugin.version, hint: "✅ plugin v" + plugin.version + " 已装, 推送链路通" }
            : { installed: false, hint: "⚠️ plugin 未装" },
          cron: cron,
          knowledge: knowledge
            ? { entries: knowledge.knowledgeCount ?? 0, hint: knowledge.hint }
            : { entries: null, hint: "knowledge_status 未拉取" },
        },
        next_steps: {
          bot_prompt: next.length > 0
            ? `✅ 已登录 OPC ${resolveOpcId(t)}。\n\n` + next.map(n => `${n.prompt}\n  ${n.cmd}`).join("\n\n")
            : `✅ 已登录 OPC ${resolveOpcId(t)}, 闭环全过 (插件装好 + cron 建好 + 知识库有内容)。`,
          actions: next.map(n => ({
            id: n.key,
            label: n.prompt.split("·")[0].trim(),
            style: n.severity === "warn" ? "primary" : "default",
            payload: { cmd: n.cmd },
          })),
        },
        message: next.length === 0
          ? "已登录, 闭环全过"
          : `已登录, ${next.length} 步未做`,
      });
      return;
    }
    // needs_refresh / missing / expired: 走老 start + 自动 poll (一键)
    await startDeviceFlow();
    return;
  }

  if (cmd === "start") {
    await startDeviceFlow();
    return;
  }

  if (cmd === "poll") {
    // 解析 --device-code / --interval / --expires-in
    const args = process.argv.slice(3);
    const deviceCode = getArg(args, "--device-code");
    const interval = parseInt(getArg(args, "--interval") ?? "5", 10);
    const expiresIn = parseInt(getArg(args, "--expires-in") ?? "600", 10);
    await pollDeviceFlow({ deviceCode, interval, expiresIn });
    return;
  }

  //   bot 调用 oauth-login --json, argv[2]=--json 不是子命令名, 报 unknown_command
  //   修法: 把 --json 这种 flag 拿掉, 重派发到默认 login
  if (cmd && cmd.startsWith("--")) {
    const realCmd = "login";  // 默认走 login (老姿势: start + 自动 poll)
    const rest = [cmd, ...process.argv.slice(3)];
    // 重新分发给 login
    process.argv = [process.argv[0], process.argv[1], realCmd, ...rest];
    return main();
  }

  err("unknown_command", `unknown subcommand: ${cmd} (可用: login / start / poll / status / logout)`);
}

main().catch((e) => err("internal_error", e.message ?? String(e)));
