/**
 * 模块: 蓝火智能体关键词触发器（v6.5.0）
 *
 * 用户痛点：
 *   v6.4.x 的 harness 路径（拦工具、注 prompt 让 LLM 走 cc-media-task）治不住
 *   wecom 群里"@贾维斯 帮我 X"这种用户没说"蓝火"的 case。
 *   用户决断："你应该把 cc 封装一个智能体。让我用关键词触发这个智能体。让它去干活。"
 *
 * 设计：
 *   把 cc 整体封装成一个 HTTP 服务（cc-media-bridge POST /dispatch），关键词命中
 *   时本 hook 直接 POST 到桥，桥 spawn cc-media-task 干活，立即返 task_id。
 *   LLM 完全不参与决策——只看到 prependContext 里的 "task_id 是 X，照抄回复"。
 *
 *   触发关键词（只有用户明确指名"蓝火"才生效，不会误伤普通对话）：
 *     ^蓝火 X
 *     ^@蓝火 X
 *     ^蓝火,X / ^蓝火:X / ^蓝火，X / ^蓝火：X
 *   X 至少 3 字（避免匹配"蓝火?"这种短语）。
 *
 * 红线：
 *   - capability detection: ~/.openclaw-media-bridge 不存在则跳过
 *   - 零 child_process / 零 fs 写
 *   - HTTP 调用走 127.0.0.1:18790（桥服务端 loopback only，绝不暴露公网）
 *   - 触发后立即 return prependContext，不阻塞 LLM 太久（HTTP timeout 6s）
 */

import { existsSync } from "node:fs";
import { join } from "node:path";
import { request as httpRequest } from "node:http";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

const BRIDGE_PORT = Number(process.env.MCP_SERVER_PORT) || 18790;
const BRIDGE_BASE = `http://127.0.0.1:${BRIDGE_PORT}`;
const BRIDGE_STATE_DIR = ".openclaw-media-bridge";

// 关键词触发：仅在用户消息以"蓝火"或"@蓝火"开头时生效
//   例: "蓝火 帮我修登录bug"  ✓
//        "@蓝火 帮我做 PPT"     ✓
//        "蓝火,继续优化"        ✓
//        "蓝火：发给我那个文档" ✓
//        "我用蓝火做"           ✗ (不在开头)
//        "蓝火好用吗"           ✗ (没空格/标点 + 短)
const TRIGGER_RE =
  /^[\s　]*@?(?:蓝火|Lanhuo)[\s　:：,，、]+([^\s].{2,1500})$/is;

function bridgeInstalled(): boolean {
  const home = process.env.HOME || process.env.USERPROFILE;
  if (!home) return false;
  return existsSync(join(home, BRIDGE_STATE_DIR));
}

interface DispatchResp {
  ok?: boolean;
  task_id?: string | null;
  dashboard_url?: string | null;
  owner_id?: string | null;
  error?: string;
}

function postDispatch(
  desc: string,
  ownerId: string | undefined,
  timeoutMs = 6000,
): Promise<DispatchResp> {
  const body = JSON.stringify({
    desc,
    owner_id: ownerId || "",
    background: true,
  });
  return new Promise((resolve, reject) => {
    const req = httpRequest(
      `${BRIDGE_BASE}/dispatch`,
      {
        method: "POST",
        timeout: timeoutMs,
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(body).toString(),
        },
      },
      (res) => {
        let buf = "";
        res.on("data", (c: Buffer) => (buf += c.toString("utf-8")));
        res.on("end", () => {
          if ((res.statusCode || 500) >= 400) {
            return reject(new Error(`HTTP ${res.statusCode}: ${buf.slice(0, 200)}`));
          }
          try {
            resolve(JSON.parse(buf) as DispatchResp);
          } catch (e) {
            reject(e as Error);
          }
        });
      },
    );
    req.on("error", reject);
    req.on("timeout", () => req.destroy(new Error("dispatch timeout")));
    req.write(body);
    req.end();
  });
}

// 从 ctx / event 里捞 sender_id（wecom:xxx）——OpenClaw 把它放在 user message
// 前缀的 "Conversation info" JSON 块里，但 hook 拿到的是已经组装好的 prompt。
// 简化：扫 prompt 里的 `sender_id":"<xxx>"` 模式即可。
function extractOwner(prompt: string): string | undefined {
  const m = /"sender_id"\s*:\s*"([^"]+)"/.exec(prompt);
  if (!m) return undefined;
  // sender_id 是裸 userid，需要拼 channel 前缀
  const ch = /"channel"\s*:\s*"([^"]+)"/.exec(prompt);
  const channel = ch ? ch[1] : "wecom"; // 默认 wecom
  return `${channel}:${m[1]}`;
}

function renderResponseTemplate(taskId: string, dashboardUrl: string, desc: string): string {
  // 用户没说"@贾维斯"也会触发蓝火 —— 让 LLM 直接 echo 这段，不要任何额外动作
  const shortDesc = desc.length > 60 ? desc.slice(0, 60) + "…" : desc;
  return [
    `## 🦞 [蓝火智能体已派活 — 不是 LLM 编造，本 plugin 已直接调 cc-media-bridge POST /dispatch 派出]`,
    ``,
    `用户输入「蓝火 …」关键词触发蓝火智能体，已**直接派给 cc-media-task**（不是 ACP 子 agent / 不是你 jarvis 自己干）。`,
    ``,
    `**你的唯一动作**：原文复制以下 markdown 给用户作为回复（不要 spawn 任何工具，不要解释，不要思考补充）：`,
    ``,
    "```",
    `🦞 蓝火接活了`,
    ``,
    `📋 任务：${shortDesc}`,
    `🎯 task_id：\`${taskId}\``,
    `🔗 进度：${dashboardUrl}`,
    ``,
    `蓝火会在 dashboard 实时回写每一步工具调用 / 思考过程 / 结果。`,
    "```",
    ``,
    `**禁止动作**（hook 已运行了真正派活动作，你 jarvis 不要再 spawn）：`,
    `- ❌ 调用 sessions_spawn / Task / spawn_task / mcp__ccd_session__spawn_task`,
    `- ❌ Bash claude -p / claude --resume / 直接 exec claude`,
    `- ❌ 自己 Write/Edit/Bash 把这个任务做了——任务已经派给蓝火，等结果就行`,
  ].join("\n");
}

function renderErrorTemplate(error: string, desc: string): string {
  const shortDesc = desc.length > 50 ? desc.slice(0, 50) + "…" : desc;
  return [
    `## ⚠️ [蓝火智能体派活失败 — 本 plugin 已尝试 HTTP POST /dispatch 但出错]`,
    ``,
    `用户输入「蓝火 ${shortDesc}」关键词，但 enhance plugin 直连 cc-media-bridge 派活时报错：`,
    ``,
    "```",
    error,
    "```",
    ``,
    `**你的回复**：原文给用户：`,
    `> 🦞⚠️ 蓝火接活失败：${error.slice(0, 80)}`,
    `> `,
    `> 你可以稍后重试，或直接在终端跑：\`cc-media-task --desc "${shortDesc}"\``,
  ].join("\n");
}

export function registerCcBridgeKeywordDispatch(api: OpenClawPluginApi) {
  if (!bridgeInstalled()) {
    api.logger.info(
      "[enhance-cc-keyword-dispatch] cc-media-bridge 未装（~/.openclaw-media-bridge 不存在），跳过关键词触发器",
    );
    return;
  }

  api.on("before_prompt_build", async (event: any, ctx: any) => {
    const userMessage: string = (event as any)?.prompt ?? "";
    if (!userMessage || userMessage.length < 5 || userMessage.length > 4000) return {};

    const m = TRIGGER_RE.exec(userMessage);
    if (!m) return {};
    const desc = m[1].trim();
    if (desc.length < 3) return {}; // 防"蓝火 ？"这种空指令

    const owner = extractOwner(userMessage);
    const sessionKey: string =
      ctx?.sessionKey ?? ctx?.sessionId ?? ctx?.agentId ?? "?";

    api.logger.info?.(
      `[enhance-cc-keyword-dispatch] 关键词命中 (session=${sessionKey.slice(-12)}) desc="${desc.slice(0, 60)}..." owner=${owner || "(none)"}`,
    );

    try {
      const resp = await postDispatch(desc, owner);
      if (!resp.ok || !resp.task_id) {
        api.logger.warn?.(
          `[enhance-cc-keyword-dispatch] dispatch 返回但无 task_id: ${JSON.stringify(resp).slice(0, 200)}`,
        );
        return {
          prependContext: renderErrorTemplate(
            resp.error || "桥服务返回无 task_id",
            desc,
          ),
        };
      }
      api.logger.info?.(
        `[enhance-cc-keyword-dispatch] ✓ 派活成功 task_id=${resp.task_id} (session=${sessionKey.slice(-12)})`,
      );
      return {
        prependContext: renderResponseTemplate(
          resp.task_id,
          resp.dashboard_url || `https://keepermac.huo15.com/lanhuo?task=${resp.task_id}`,
          desc,
        ),
      };
    } catch (e) {
      const err = e instanceof Error ? e.message : String(e);
      api.logger.error?.(
        `[enhance-cc-keyword-dispatch] HTTP dispatch failed: ${err}`,
      );
      return {
        prependContext: renderErrorTemplate(err, desc),
      };
    }
  });

  api.logger.info(
    `[enhance-cc-keyword-dispatch] 蓝火智能体关键词触发器已注册 (规则：消息以 ^蓝火 / ^@蓝火 开头 → 直接 POST ${BRIDGE_BASE}/dispatch 派活，跳过 LLM 决策)`,
  );
}
