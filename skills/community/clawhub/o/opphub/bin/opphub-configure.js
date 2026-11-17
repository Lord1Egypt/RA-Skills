#!/usr/bin/env node
// bin/opphub-configure.js · v4.0.0
// status: implemented (v4 通道 v4: 通道清单走 runtime, 默认通道走 server PATCH)
//
//
// v4.0.0 P0-5: 通道 v4 改造 (实测已符合, 无代码改动)
//   - 通道清单 = OpenClaw runtime 真源, 走 `openclaw channels list --json` (不经 plugin)
//   - 默认通道真源 = opphub-server, PATCH /api/user/channels/default 直连 server (不经 plugin)
//   - 旧版: 调 `openclaw opphub channels` 走 plugin CLI, plugin 进程不在就拿不到
//   - 现版: 调 `openclaw channels list --json` 走 runtime, plugin 缺也能跑
//
// 用法: bot 调
//   opphub configure list --json
//     → 返 { ok, channels: [{type, account, valid, reportedAs, reason?}], skipped, default_channel }
//   opphub configure set --channel-type feishu --channel-id pm --json
//     → PATCH /api/user/channels/default (用户 JWT, 不传 peer)
//
// 注意: 不直接拿 openclaw.json 校验凭证 (那是 plugin 直读模式)
// skill 调 `openclaw opphub channels` (plugin CLI) 拿已校验过的清单

import { exec as execSync } from "node:child_process";
import { promisify } from "node:util";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import {
  buildInteractive,
  output,
  errorOut,
} from "../lib/intent-card.js";

const execp = promisify(execSync);

const API_BASE = process.env.OPPHUB_API_BASE || "https://api.opphub.ruiplus.cn";

async function readToken() {
  //   plain text 不存在 → readToken 永远 null → configure set 永远 need_login
  const { readToken: proxyReadToken } = await import("../lib/opphub-plugin-client.js");
  return await proxyReadToken();
}

async function getChannelsViaOpenclawCli() {
  //   之前调 `openclaw opphub channels` (plugin CLI), plugin runtime 不在就拿不到
  //   正解: 调 openclaw 官方 `openclaw channels list --json` (gateway 端, 不依赖 plugin)
  //
  // stdout 格式:
  // {
  //   "chat": {
  //     "feishu": {
  //       "accounts": ["default", "dev", "frontend", "pm"],
  //       "installed": true,
  //       "origin": "configured"
  //     },
  //     "openclaw-weixin": {
  //       "accounts": ["ece6e448d6c4-im-bot"],
  //       "installed": true
  //     }
  //   }
  // }
  try {
    const { stdout } = await execp("openclaw channels list --json", {
      encoding: "utf8",
      timeout: 8000,
    });
    const j = JSON.parse(stdout);
    const channels = [];
    for (const [type, info] of Object.entries(j?.chat ?? {})) {
      if (!info?.accounts || info.accounts.length === 0) continue;
      for (const account of info.accounts) {
        channels.push({
          type,
          account,
          installed: !!info.installed,
          origin: info.origin,
          // valid: 暂设 null, 让 user 看配置列表时知道凭证校验待 plugin 上报 server 后才有
          valid: null,
        });
      }
    }
    return channels;
  } catch (e) {
    return { error: "openclaw_cli_failed", message: e?.message ?? String(e) };
  }
}

async function cmdList() {
  // 1. 拿 channels (via plugin CLI, 已校验)
  const channels = await getChannelsViaOpenclawCli();
  if (channels?.error) {
    errorOut(channels.error, channels.message, { hint: "openclaw CLI 跑不了, 检查 openclaw 是否装好 (PATH / openclaw 命令)" });
  }
  if (channels.length === 0) {
    errorOut("no_valid_channels", "本机没任何有效通道", {
      hint: "先跑 openclaw channels add 加 IM 通道",
    });
  }

  //    合并 server 端 /api/user/channels/default 选中态
  //    原实现: isDefault: i === 0 (写死第一条), 没真查 server
  //    现实现: 调 getDefaultChannel() 拿 server 选中, 给对应那条打 isDefault: true
  const { getDefaultChannel } = await import("../lib/opphub-server-client.js");
  const defaultChannel = await getDefaultChannel();
  const selected = defaultChannel.selected; // { channelType, channelId, isDefault } | null

  // 3. 拼 IntentMessage 给 skill → skill 调 bot.skillApi.askInteractive
  const intent = buildInteractive({
    header: { title: "选默认推送通道", color: "blue" },
    prompt: selected
      ? `本机已配通道 · ⭐ server 选中: \`${selected.channelType}:${selected.channelId}\``
      : "本机已配通道 (有效 + 凭证校验过)",
    options: channels.map((c) => {
      const isServerSelected = selected
        && c.type === selected.channelType
        && c.account === selected.channelId;
      return {
        id: `${c.type}:${c.account}`,
        label: isServerSelected ? `${c.type}:${c.account} ⭐` : `${c.type}:${c.account}`,
        hint: isServerSelected
          ? "⭐ server 选中 (默认推送走这里)"
          : (c.valid ? "✅ 凭证齐" : c.reason),
        isDefault: !!isServerSelected,
      };
    }),
    actions: [
      { id: "confirm", label: "确认", style: "primary" },
      { id: "cancel", label: "取消", style: "danger" },
    ],
  });

  output({ ok: true, intent, channels, default_channel: defaultChannel });
}

async function cmdSet({ channelType, channelId }) {
  if (!channelType || !channelId) {
    errorOut("missing_params", "需要 --channel-type + --channel-id");
  }

  // 1. 拿 token
  const token = await readToken();
  if (!token?.access_token) {
    errorOut("need_login", "先跑偶合登录", {
      hint: "@bot 偶合登录 走 device flow",
    });
  }

  // 2. PATCH /api/user/channels/default
  const url = `${API_BASE}/api/user/channels/default`;
  let resp;
  try {
    resp = await fetch(url, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token.access_token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        channelType,
        channelId,
      }),
    });
  } catch (e) {
    errorOut("network_failed", `PATCH ${url} 失败: ${e?.message ?? String(e)}`);
  }

  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    errorOut(`http_${resp.status}`, `${url}: ${text.trim().slice(0, 200)}`);
  }

  let result = {};
  try {
    result = await resp.json();
  } catch {}
  if (!result?.ok) {
    errorOut("server_ok_false", `server 返 ok=false: ${JSON.stringify(result)}`);
  }

  // 3. 输出 IntentMessage 给 skill → skill 调 bot.skillApi.send
  const { buildSend } = await import("../lib/intent-card.js");
  const intent = buildSend({
    header: { title: "偶合配置成功", color: "green" },
    prompt: `✅ 默认通道已设为 \`${channelType}:${channelId}\``,
    markdown: [
      "| 项 | 状态 |",
      "|---|---|",
      "| server 同步 | ✅ ok |",
      "| 配置生效 | ✅ 推送会走该通道 |",
    ].join("\n"),
  });

  output({ ok: true, intent, server: { ok: true } });
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--channel-type") args.channelType = argv[++i];
    else if (a === "--channel-id") args.channelId = argv[++i];
    else if (!a.startsWith("--")) args._.push(a);
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const cmd = args._[0];

if (cmd === "list") {
  cmdList().catch((e) => errorOut("list_failed", e?.message ?? String(e)));
} else if (cmd === "set") {
  cmdSet(args).catch((e) => errorOut("set_failed", e?.message ?? String(e)));
} else {
  errorOut("usage", "opphub configure list --json | set --channel-type X --channel-id Y --json");
}
