/**
 * 模块: enhance_transcript_search — 全文搜索历史会话 JSONL
 *
 * 来源 / 设计参考:
 *   /Applications/Claude.app/Contents/Resources/app.asar 里的
 *   .vite/build/transcript-search-worker/transcriptSearchWorker.js
 *
 * 那是 Claude Desktop 的官方实现，做法极简：
 *   - 不建二级索引，直接流式读 JSONL
 *   - 行级 JSON.parse，filter 出 message 类型
 *   - extractText 兼容 string / [{type:"text", text}] 数组
 *   - indexOf 子串匹配 + ±80 字符 snippet
 *
 * 我们把这套搬到 openclaw 的 session 目录上 (~/.openclaw/agents/<agentId>/sessions/*.jsonl)：
 *   - 完全只读 — 不动龙虾任何东西
 *   - 不建表 — 不与 enhance 的 SQLite 库重叠
 *   - 不建 FTS — 用户每次搜临时扫，简单可靠（Claude Desktop 都没用 FTS）
 *
 * 性能：单 session 通常 < 1 MB，几十个 session 全扫一次 < 100ms（SSD），完全可接受。
 */

import { promises as fs } from "node:fs";
import { createReadStream } from "node:fs";
import { createInterface } from "node:readline";
import { join } from "node:path";
import { Type } from "@sinclair/typebox";

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { DEFAULT_AGENT_ID } from "../types.js";

const SNIPPET_RADIUS = 80;
const DEFAULT_LIMIT = 10;
const HARD_LIMIT_FILES = 50; // 即使没 hit 满 limit，最多扫这么多文件

interface SearchHit {
  sessionId: string;
  fileName: string;
  role: string;
  snippet: string;
  matchedAt: string;
  lastModifiedMs: number;
}

interface SessionFile {
  sessionId: string;
  filePath: string;
  fileName: string;
  lastModifiedMs: number;
  isReset: boolean;
}

function pickAgentId(ctx: unknown): string {
  return (((ctx as any)?.agentId as string | undefined) ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID;
}

/**
 * 列出某个 agent 下所有可读的 session jsonl 文件，按 mtime 倒序。
 * - 默认跳过 .reset. / .deleted. / .checkpoint. / .trajectory.（这些是历史快照）
 * - includeReset=true 时把 .reset. 也算进来（用户可能想搜被压缩前的内容）
 */
async function listSessionFiles(
  openclawHome: string,
  agentId: string,
  includeReset: boolean,
): Promise<SessionFile[]> {
  const sessionsDir = join(openclawHome, "agents", agentId, "sessions");
  let entries: string[];
  try {
    entries = await fs.readdir(sessionsDir);
  } catch {
    return [];
  }

  const out: SessionFile[] = [];
  for (const fname of entries) {
    if (!fname.endsWith(".jsonl")) continue;

    const isDeleted = fname.includes(".deleted.");
    const isReset = fname.includes(".reset.");
    const isCheckpoint = fname.includes(".checkpoint.");
    const isTrajectory = fname.includes(".trajectory.");

    if (isDeleted || isCheckpoint || isTrajectory) continue;
    if (isReset && !includeReset) continue;

    // 提取 sessionId（取第一段 UUID 形式）
    const sessionId = fname.split(".")[0];

    const filePath = join(sessionsDir, fname);
    let lastModifiedMs = 0;
    try {
      const stat = await fs.stat(filePath);
      lastModifiedMs = stat.mtimeMs;
    } catch {
      continue;
    }

    out.push({ sessionId, filePath, fileName: fname, lastModifiedMs, isReset });
  }

  out.sort((a, b) => b.lastModifiedMs - a.lastModifiedMs);
  return out;
}

/**
 * 从 message.content 提取纯文本。
 * 兼容三种形态：
 *   - string                              （早期版本）
 *   - [{type:"text", text:"…"}, …]        （Anthropic block 标准）
 *   - {type:"text", text:"…"}             （单 block，不规范但偶见）
 */
function extractText(content: unknown): string {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    let out = "";
    for (const block of content) {
      if (block && typeof block === "object") {
        const b = block as { type?: unknown; text?: unknown };
        if (b.type === "text" && typeof b.text === "string") out += b.text + " ";
      }
    }
    return out;
  }
  if (content && typeof content === "object") {
    const b = content as { type?: unknown; text?: unknown };
    if (b.type === "text" && typeof b.text === "string") return b.text;
  }
  return "";
}

function makeSnippet(text: string, idx: number, qLen: number): string {
  const start = Math.max(0, idx - SNIPPET_RADIUS);
  const end = Math.min(text.length, idx + qLen + SNIPPET_RADIUS);
  const slice = text.slice(start, end).trim();
  return (start > 0 ? "…" : "") + slice + (end < text.length ? "…" : "");
}

/**
 * 流式扫单个文件，找到第一条匹配就返回。
 * 与 Claude Desktop 的实现策略一致：每个 session 只贡献一个 hit（first match），
 * 这样 limit=10 就是"找到 10 个不同 session"，比"全文返回所有匹配"更可读。
 */
async function scanFile(
  session: SessionFile,
  needle: string,
  caseSensitive: boolean,
): Promise<SearchHit | null> {
  const stream = createReadStream(session.filePath, { encoding: "utf8" });
  const rl = createInterface({ input: stream, crlfDelay: Infinity });
  try {
    for await (const line of rl) {
      if (!line) continue;
      let parsed: { type?: unknown; message?: { role?: unknown; content?: unknown }; timestamp?: unknown };
      try {
        parsed = JSON.parse(line);
      } catch {
        continue;
      }
      if (parsed.type !== "message") continue;
      const role = typeof parsed.message?.role === "string" ? parsed.message.role : "?";
      const text = extractText(parsed.message?.content);
      if (!text) continue;
      const normalized = text.replace(/\s+/g, " ");
      const haystack = caseSensitive ? normalized : normalized.toLowerCase();
      const idx = haystack.indexOf(needle);
      if (idx === -1) continue;

      const matchedAtRaw = parsed.timestamp;
      const matchedAt =
        typeof matchedAtRaw === "string"
          ? matchedAtRaw
          : typeof matchedAtRaw === "number"
            ? new Date(matchedAtRaw).toISOString()
            : new Date(session.lastModifiedMs).toISOString();

      return {
        sessionId: session.sessionId,
        fileName: session.fileName,
        role,
        snippet: makeSnippet(normalized, idx, needle.length),
        matchedAt,
        lastModifiedMs: session.lastModifiedMs,
      };
    }
  } finally {
    rl.close();
    stream.destroy();
  }
  return null;
}

export function registerTranscriptSearch(api: OpenClawPluginApi) {
  const openclawHome = resolveOpenClawHome(api);

  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_transcript_search",
      description: "搜索当前 Agent 历史会话 jsonl（流式扫，无索引）；找『我上次怎么做的』",
      parameters: Type.Object({
        query: Type.String({ description: "搜索词，不区分大小写" }),
        agentId: Type.Optional(Type.String({ description: "目标 agent，默认当前" })),
        limit: Type.Optional(Type.Number({ description: "最多返回 hit 数，默认 10", minimum: 1, maximum: 50 })),
        includeReset: Type.Optional(Type.Boolean({ description: "是否包含 .reset. 历史，默认 false" })),
        caseSensitive: Type.Optional(Type.Boolean({ description: "区分大小写，默认 false" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const rawQuery = String(params.query ?? "").trim();
        if (!rawQuery) {
          return { content: [{ type: "text" as const, text: "query 不能为空。" }] };
        }
        const agentId = (String(params.agentId ?? "").trim() || pickAgentId(ctx)) || DEFAULT_AGENT_ID;
        const limit = Math.min(Math.max(Number(params.limit ?? DEFAULT_LIMIT), 1), 50);
        const includeReset = Boolean(params.includeReset);
        const caseSensitive = Boolean(params.caseSensitive);

        const needle = caseSensitive
          ? rawQuery.replace(/\s+/g, " ")
          : rawQuery.replace(/\s+/g, " ").toLowerCase();

        const files = await listSessionFiles(openclawHome, agentId, includeReset);
        if (files.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text: `没找到 agent=${agentId} 的任何 session 文件（路径：${join(openclawHome, "agents", agentId, "sessions")}）。`,
              },
            ],
            structuredContent: { agentId, hits: [], filesScanned: 0 },
          };
        }

        const hits: SearchHit[] = [];
        let filesScanned = 0;
        for (const f of files.slice(0, HARD_LIMIT_FILES)) {
          filesScanned++;
          try {
            const hit = await scanFile(f, needle, caseSensitive);
            if (hit) hits.push(hit);
          } catch {
            // 单文件失败不影响整体
          }
          if (hits.length >= limit) break;
        }

        if (hits.length === 0) {
          return {
            content: [
              {
                type: "text" as const,
                text:
                  `agent=${agentId} 扫描了 ${filesScanned} 个 session，未找到匹配「${rawQuery}」的内容。\n` +
                  (includeReset
                    ? "已包含 .reset. 历史。"
                    : "提示：加 includeReset=true 可搜被压缩重置过的旧 session。"),
              },
            ],
            structuredContent: { agentId, hits: [], filesScanned },
          };
        }

        const lines: string[] = [
          `🔍 命中 ${hits.length} 条（扫了 ${filesScanned} 个 session，agent=${agentId}）`,
          "",
        ];
        for (const h of hits) {
          const ts = h.matchedAt.replace("T", " ").replace(/\.\d+Z$/, "Z");
          lines.push(`【${h.role}@${ts}】 session=${h.sessionId.slice(0, 8)}…`);
          lines.push(`  ${h.snippet}`);
          lines.push("");
        }

        return {
          content: [{ type: "text" as const, text: lines.join("\n").trim() }],
          structuredContent: { agentId, hits, filesScanned },
        };
      },
    })) as any,
    { name: "enhance_transcript_search" },
  );

  api.logger.info("[enhance] 历史会话搜索模块已加载（enhance_transcript_search）");
}
