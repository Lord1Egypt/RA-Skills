/**
 * 模块: 蓝火 / cc-media-bridge 预查询 — 真 harness 反幻觉（v6.x）
 *
 * 痛点：用户在 wecom 群问"蓝火任务"，LLM hallucinate ——不调任何工具，
 * 拿训练数据里的 plausible task list（cc-YYYYMMDD-XXX 假 ID + 假摘要）回。
 * 哪怕 SKILL 写"必调工具" + cc_task_list 已 deprecated + 响应级 redirect，
 * LLM 仍偶发跳过工具直接编。
 *
 * harness 思想：**不依赖 LLM 自觉**，在 user message 进入 LLM context 前
 * 检测到"蓝火 + 任务/列表/历史"模式时**强行预填**真实数据进 prependContext。
 * LLM 看到 system prompt 已有 trusted 数据 → 没有"决定要不要调工具"的余地 →
 * 只能 copy 真数据回答 → hallucination 不可能发生。
 *
 * 实现：
 *   - before_prompt_build hook（同 session-recap）拿 event.prompt 做模式检测
 *   - 检测命中 → 用缓存的 cc-media-bridge `/cc-sessions` 数据预渲染 markdown
 *   - 缓存 30s 后台刷新（避免每条消息都打 HTTP）
 *   - 拒绝命中模式但 cache stale (>2.5min) 的情况——不喂 LLM 旧数据，让它走兜底（调工具或拒答）
 *
 * 红线：
 *   - capability detection: ~/.openclaw-media-bridge 不存在则跳过整个模块
 *   - 零 child_process / 零 fs 写
 *   - 零 cc-media-bridge 代码 import（HTTP 调用，不强 require）
 *   - dashboard_password 用 huo15.com 默认值（如用户改了，hook 拿不到，cache 留空）
 */

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { request as httpRequest } from "node:http";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

const BRIDGE_PORT = Number(process.env.MCP_SERVER_PORT) || 18790;
const BRIDGE_BASE = `http://127.0.0.1:${BRIDGE_PORT}`;
const BRIDGE_STATE_DIR = ".openclaw-media-bridge";
const CACHE_TTL_MS = 30_000;
const CACHE_STALE_MS = 150_000; // > 2.5min stale 不再喂

let _cache: { rendered: string; sessionsCount: number; ts: number } | null = null;
let _password: string | null = null;

function bridgeInstalled(): boolean {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) return false;
  return existsSync(join(home, BRIDGE_STATE_DIR));
}

function readBridgePassword(): string {
  if (_password !== null) return _password;
  const home = process.env.HOME || process.env.USERPROFILE;
  if (home) {
    try {
      const cfgPath = join(home, BRIDGE_STATE_DIR, "config.json");
      if (existsSync(cfgPath)) {
        const cfg = JSON.parse(readFileSync(cfgPath, "utf-8")) as {
          dashboard_password?: string;
        };
        _password = (cfg.dashboard_password || "").trim() || "huo15.com";
        return _password;
      }
    } catch {
      // ignore
    }
  }
  _password = "huo15.com";
  return _password;
}

function fetchSessions(): Promise<{ sessions?: any[] }> {
  return new Promise((resolve, reject) => {
    const pwd = readBridgePassword();
    const url = `${BRIDGE_BASE}/cc-sessions?limit=20&pwd=${encodeURIComponent(pwd)}`;
    const req = httpRequest(url, { method: "GET", timeout: 3000 }, (res) => {
      let body = "";
      res.on("data", (c: Buffer) => (body += c.toString("utf-8")));
      res.on("end", () => {
        if ((res.statusCode || 500) >= 400) {
          return reject(new Error(`HTTP ${res.statusCode}`));
        }
        try {
          resolve(JSON.parse(body) as { sessions?: any[] });
        } catch (e) {
          reject(e as Error);
        }
      });
    });
    req.on("error", reject);
    req.on("timeout", () => req.destroy(new Error("timeout")));
    req.end();
  });
}

function renderSessions(sessions: any[]): string {
  const pinned = sessions.filter((s) => s.custom_title);
  const recents = sessions.filter((s) => !s.custom_title);
  const lines: string[] = [];
  lines.push("## 🔒 [蓝火预查询 trusted 数据 — 由 enhance plugin 自动 fetch，不是 LLM 编造]");
  lines.push("");
  lines.push(
    "用户问蓝火任务/会话/列表/历史 — **已自动调 cc-media-bridge `/cc-sessions` 拿真实 trusted 数据**：",
  );
  lines.push("");
  if (pinned.length > 0) {
    lines.push("### 📌 Pinned (custom_title 命名过的)");
    for (const s of pinned.slice(0, 10)) {
      const t = (s.custom_title || "").slice(0, 80);
      const ts = (s.mtime || "").slice(0, 10);
      const sid = (s.session_id || "").slice(0, 8);
      lines.push(`- ⭐ ${t} · ${ts} · \`${sid}\``);
    }
    lines.push("");
  }
  if (recents.length > 0) {
    lines.push("### 📋 Recents (按 mtime 倒序)");
    for (const s of recents.slice(0, 15)) {
      const title = ((s.task_summary || s.first_user || "(no preview)") + "")
        .slice(0, 80)
        .replace(/\n/g, " ");
      const owner = s.task_owner ? ` · via @${s.task_owner.replace("wecom:", "")}` : "";
      const ts = (s.mtime || "").slice(0, 10);
      const sid = (s.session_id || "").slice(0, 8);
      lines.push(`- 💬 ${title} · ${ts} · \`${sid}\`${owner}`);
    }
    lines.push("");
  }
  lines.push("🌐 https://keepermac.huo15.com/lanhuo");
  lines.push("");
  lines.push("---");
  lines.push("");
  lines.push("**渲染规则**（必遵守）：");
  lines.push("");
  lines.push("1. 直接用上面这段 markdown 回复用户（可加少量寒暄但**不要**重新查工具/重新组织数据）");
  lines.push("2. 上面**没有**出现的 session_id / 标题 / 时间，**禁止出现在回复里**——一旦出现就是 hallucination");
  lines.push("3. **禁止**编造 cc-YYYYMMDD-XXXXX 格式 task ID（那是 v2.16.1 之前已废弃格式）");
  lines.push("4. **禁止**拿 OpenClaw 平台 task / agent task 冒充蓝火任务（只有 ~/.claude/projects/ 的 jsonl 算）");
  return lines.join("\n");
}

async function refreshCache() {
  try {
    const data = await fetchSessions();
    const sessions = Array.isArray(data.sessions) ? data.sessions : [];
    _cache = {
      rendered: renderSessions(sessions),
      sessionsCount: sessions.length,
      ts: Date.now(),
    };
  } catch {
    // bridge unreachable, leave cache
  }
}

// 检测 user message 是否是"列任务/会话/历史"类查询
const QUERY_PATTERN =
  /(蓝火|虾任务|龙任务|cc[\s-]?task|claude code).{0,8}(任务|列表|历史|最近|会话|sessions?|tasks?|chat history)|我的(蓝火|虾任务|task|chat history)|list\s+my\s+(tasks?|sessions?|chat)|recent\s+(tasks?|sessions?|chat)/i;

// 排除 dispatch 动词（这些是"让蓝火做X"，不是查询）
const DISPATCH_VERB_PATTERN =
  /(做|帮|写|改|继续|优化|创建|生成|制作|分析|修复|debug|fix|implement|build|create|让.{1,5}做)/;

export function registerCcBridgePreFetch(api: OpenClawPluginApi) {
  if (!bridgeInstalled()) {
    api.logger.info(
      "[enhance-cc-pre-fetch] cc-media-bridge 未装（~/.openclaw-media-bridge 不存在），跳过 pre-fetch hook",
    );
    return;
  }

  // 启动时初始化 + 每 30s 后台刷新
  void refreshCache();
  const timer = setInterval(() => void refreshCache(), CACHE_TTL_MS);
  if (typeof timer.unref === "function") timer.unref();

  api.on("before_prompt_build", (event: any) => {
    const userMessage: string = (event as any)?.prompt ?? "";
    if (!userMessage || userMessage.length > 500) return {}; // 太长 likely 不是简单查询

    // 模式必须命中查询 + 不能含 dispatch 动词
    if (!QUERY_PATTERN.test(userMessage)) return {};
    if (DISPATCH_VERB_PATTERN.test(userMessage)) return {};

    // cache miss / stale → 不喂数据，让 LLM 走兜底（调工具或拒答）
    if (!_cache) return {};
    if (Date.now() - _cache.ts > CACHE_STALE_MS) return {};

    api.logger.info?.(
      `[enhance-cc-pre-fetch] 命中 query 模式 "${userMessage.slice(0, 40)}..."，注入 ${_cache.sessionsCount} 条 trusted 会话数据`,
    );

    return {
      prependContext: _cache.rendered,
    };
  });

  api.logger.info(
    "[enhance-cc-pre-fetch] before_prompt_build hook 已注册（蓝火+名词查询自动 fetch session list 注入 system prompt）",
  );
}
