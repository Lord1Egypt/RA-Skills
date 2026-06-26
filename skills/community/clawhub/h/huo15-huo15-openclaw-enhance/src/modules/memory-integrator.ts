/**
 * 模块: 记忆整合（Memory Integrator）
 *
 * 设计原则（非侵入）：
 * - 不复制龙虾的原生记忆，仅通过 registerMemoryCorpusSupplement 把 enhance 的 SQLite
 *   分类记忆喂给龙虾的记忆引擎。
 * - 搜索评分在 corpus.search() 内部完成（合并原 context-pruner 逻辑），
 *   不再通过 before_prompt_build 绕过龙虾的原生注入路径。
 * - 龙虾构建 system prompt 时会自己决定是否、如何注入 corpus 结果 —— 我们只做数据源。
 *
 * Public API 对接（openclaw 2026.4.11）：
 *   api.registerMemoryCorpusSupplement(supplement)     — 单参，龙虾内部挂 pluginId
 *   api.registerMemoryPromptSupplement(builder)        — 可选，只追加提示词段
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { getDb, searchMemories } from "../utils/sqlite-store.js";
import { DEFAULT_AGENT_ID } from "../types.js";
import type { MemoryEntry } from "../types.js";

const PLUGIN_CORPUS_ID = "enhance";

// ── 龙虾记忆 SDK 本地类型（与 openclaw memory-state.ts 完全对齐） ──
interface MemoryCorpusSearchResult {
  corpus: string;
  path: string;
  title?: string;
  kind?: string;
  score: number;
  snippet: string;
  id?: string;
  startLine?: number;
  endLine?: number;
  citation?: string;
  source?: string;
  provenanceLabel?: string;
  sourceType?: string;
  sourcePath?: string;
  updatedAt?: string;
}

interface MemoryCorpusGetResult {
  corpus: string;
  path: string;
  title?: string;
  kind?: string;
  content: string;
  fromLine: number;
  lineCount: number;
  id?: string;
  provenanceLabel?: string;
  sourceType?: string;
  sourcePath?: string;
  updatedAt?: string;
}

interface MemoryCorpusSupplement {
  search(params: {
    query: string;
    maxResults?: number;
    agentSessionKey?: string;
  }): Promise<MemoryCorpusSearchResult[]>;
  get(params: {
    lookup: string;
    fromLine?: number;
    lineCount?: number;
    agentSessionKey?: string;
  }): Promise<MemoryCorpusGetResult | null>;
}

// ── 集成器配置（合并自原 ContextPrunerConfig） ──
export interface MemoryIntegratorOptions {
  /** 相关性阈值（0-1），低于此分数的记忆不会返回给龙虾，默认 0.5 */
  threshold?: number;
  /** 单次 search 最多返回几条，默认 5 */
  maxEntries?: number;
  /** 调试日志 */
  debug?: boolean;
}

// ── v5.7.2 防御性 tag 黑名单 ──
// 任何带有这些 tag 的记忆条目在 corpus.search 中直接 score=0（永不召回）。
// 防止类似 v5.7.1 修复的 [auto-compact] noise 再次混进 prompt。
// 即便未来 enhance 又冒出"高频 hook 自动写入"，这层兜底也能消除其影响。
const TAG_BLACKLIST = new Set([
  "auto-compact",
  "auto-checkpoint",
  "audit",
  "internal",
]);

function isBlacklisted(tags: string): boolean {
  if (!tags) return false;
  // tags 是逗号分隔字符串
  return tags
    .split(",")
    .map((t) => t.trim().toLowerCase())
    .some((t) => TAG_BLACKLIST.has(t));
}

// ── 相关性评分（沿用原 context-pruner 权重模型） ──
const STOP_WORDS = new Set([
  "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
  "have", "has", "had", "do", "does", "did", "will", "would", "could",
  "should", "may", "might", "must", "can", "to", "of", "in", "for",
  "on", "with", "at", "by", "from", "as", "into", "through", "during",
  "before", "after", "above", "below", "between", "under", "again",
  "further", "then", "once", "here", "there", "when", "where", "why",
  "how", "all", "each", "few", "more", "most", "other", "some", "such",
  "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
  "just", "but", "and", "or", "if", "because", "until", "while",
  "about", "against", "this", "that", "these", "those", "am", "it", "its",
]);

function scoreRelevance(memory: MemoryEntry, query: string): number {
  // v5.7.2: tag 黑名单兜底——audit / auto-compact 等系统类记忆永不召回
  if (isBlacklisted(memory.tags)) return 0;

  const queryLower = query.toLowerCase();
  const contentLower = memory.content.toLowerCase();
  const tagsLower = memory.tags.toLowerCase();

  const queryTokens = queryLower
    .split(/[\s\W]+/)
    .filter((t) => t.length > 1)
    .filter((t) => !STOP_WORDS.has(t));

  let keywordScore = 0;
  if (queryTokens.length > 0) {
    const matched = queryTokens.filter(
      (t) => contentLower.includes(t) || tagsLower.includes(t),
    );
    keywordScore = matched.length / queryTokens.length;
  } else if (queryLower.length > 2) {
    keywordScore =
      contentLower.includes(queryLower) || tagsLower.includes(queryLower) ? 0.5 : 0;
  }

  const categoryWeight: Record<string, number> = {
    project: 0.3,
    decision: 0.25,
    user: 0.2,
    feedback: 0.15,
    reference: 0.1,
  };
  const catScore = categoryWeight[memory.category] ?? 0.1;
  const importanceScore = ((memory.importance ?? 5) / 10) * 0.1;

  let freshnessScore = 0.1;
  try {
    const ageDays = (Date.now() - new Date(memory.created_at).getTime()) / 86_400_000;
    if (ageDays <= 7) freshnessScore = 0.1;
    else if (ageDays <= 30) freshnessScore = 0.1 * (1 - (ageDays - 7) / 23);
    else freshnessScore = 0;
  } catch {
    freshnessScore = 0.05;
  }

  return Math.min(1, Math.max(0, keywordScore * 0.5 + catScore + importanceScore + freshnessScore));
}

// ── agentId / lookup 辅助 ──
function extractAgentId(sessionKey: string | undefined): string {
  if (!sessionKey) return DEFAULT_AGENT_ID;
  if (sessionKey.startsWith("agent:")) return sessionKey.slice(6) || DEFAULT_AGENT_ID;
  return sessionKey;
}

function extractIdFromLookup(lookup: string): number | null {
  if (/^\d+$/.test(lookup)) return parseInt(lookup, 10);
  const match = lookup.match(/(\d+)(?:\/[^/]*)?$/);
  return match ? parseInt(match[1], 10) : null;
}

// ── SQLite 访问 ──
interface EnhanceMemoryRow {
  id: number;
  category: string;
  content: string;
  tags: string;
  importance: number;
  agent_id: string;
  created_at: string;
  why?: string | null;
  how_to_apply?: string | null;
}

function getMemoryById(db: any, agentId: string, id: number): EnhanceMemoryRow | null {
  try {
    return db
      .prepare(
        "SELECT id, category, content, tags, importance, agent_id, created_at, why, how_to_apply FROM memories WHERE id = ? AND agent_id = ?",
      )
      .get(id, agentId) as EnhanceMemoryRow | null;
  } catch {
    return null;
  }
}

function listRecentMemories(db: any, agentId: string, limit: number): EnhanceMemoryRow[] {
  try {
    return db
      .prepare(
        "SELECT id, category, content, tags, importance, agent_id, created_at, why, how_to_apply FROM memories WHERE agent_id = ? ORDER BY created_at DESC LIMIT ?",
      )
      .all(agentId, limit) as EnhanceMemoryRow[];
  } catch {
    return [];
  }
}

/** 组合成供龙虾 memory 引擎读取的多段式正文：Content + Why + How-to-apply。 */
function formatMemoryBody(memory: Pick<MemoryEntry, "content" | "why" | "how_to_apply">): string {
  const parts: string[] = [memory.content];
  if (memory.why && memory.why.trim()) {
    parts.push(`\n**Why:** ${memory.why.trim()}`);
  }
  if (memory.how_to_apply && memory.how_to_apply.trim()) {
    parts.push(`**How to apply:** ${memory.how_to_apply.trim()}`);
  }
  return parts.join("\n");
}

// ── 构建 MemoryCorpusSupplement ──
function buildEnhanceCorpus(
  api: OpenClawPluginApi,
  options: MemoryIntegratorOptions,
): MemoryCorpusSupplement {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();
  const threshold = options.threshold ?? 0.5;
  const defaultMax = options.maxEntries ?? 5;
  const debug = options.debug ?? false;

  return {
    async search({ query, maxResults, agentSessionKey }) {
      const cleanQuery = (query ?? "").trim();
      if (!cleanQuery) return [];

      const agentId = extractAgentId(agentSessionKey);
      const all = searchMemories(db, agentId, { limit: 100 });
      if (all.length === 0) return [];

      const limit = maxResults ?? defaultMax;
      // Deterministic tie-break so prompt cache prefix stays stable across turns.
      // Order: score DESC → importance DESC → updated_at DESC → id DESC.
      const scored = all
        .map((m) => ({ memory: m, score: scoreRelevance(m, cleanQuery) }))
        .filter(({ score }) => score >= threshold)
        .sort((a, b) => {
          if (b.score !== a.score) return b.score - a.score;
          const ai = a.memory.importance ?? 5;
          const bi = b.memory.importance ?? 5;
          if (bi !== ai) return bi - ai;
          const at = new Date(a.memory.updated_at || a.memory.created_at).getTime();
          const bt = new Date(b.memory.updated_at || b.memory.created_at).getTime();
          if (bt !== at) return bt - at;
          return b.memory.id - a.memory.id;
        })
        .slice(0, limit);

      if (debug) {
        api.logger.info(
          `[enhance] corpus.search query="${cleanQuery.slice(0, 60)}" → ${scored.length}/${all.length} 条 (agent: ${agentId})`,
        );
      }

      return scored.map(({ memory, score }) => ({
        corpus: PLUGIN_CORPUS_ID,
        path: `memory://enhance/${memory.category}/${memory.id}`,
        title: `[${memory.category.toUpperCase()}] ${memory.content.slice(0, 60)}`,
        kind: memory.category,
        score,
        snippet: formatMemoryBody(memory).slice(0, 400),
        id: String(memory.id),
        citation: `@enhance:${memory.id}`,
        provenanceLabel: "enhance-memory",
        sourceType: "structured_memory",
        sourcePath: `enhance://memory/${memory.category}/${memory.id}`,
        updatedAt: memory.created_at,
      }));
    },

    async get({ lookup, fromLine = 1, lineCount = 100, agentSessionKey }) {
      const id = extractIdFromLookup(lookup);
      if (!id) return null;

      const agentId = extractAgentId(agentSessionKey);
      const row = getMemoryById(db, agentId, id);
      if (!row) return null;

      const fullBody = formatMemoryBody({
        content: row.content,
        why: row.why ?? undefined,
        how_to_apply: row.how_to_apply ?? undefined,
      });
      const lines = fullBody.split("\n");
      const startLine = Math.max(1, Math.min(fromLine, lines.length));
      const endLine = Math.min(startLine + lineCount - 1, lines.length);
      const selected = lines.slice(startLine - 1, endLine);

      return {
        corpus: PLUGIN_CORPUS_ID,
        path: `memory://enhance/${row.category}/${row.id}`,
        title: `[${row.category.toUpperCase()}] ${row.content.slice(0, 60)}`,
        kind: row.category,
        content: selected.join("\n"),
        fromLine: startLine,
        lineCount: selected.length,
        id: String(row.id),
        provenanceLabel: "enhance-memory",
        sourceType: "structured_memory",
        sourcePath: `enhance://memory/${row.category}/${row.id}`,
        updatedAt: row.created_at,
      };
    },
  };
}

// ── 主注册入口 ──
export function registerMemoryIntegrator(
  api: OpenClawPluginApi,
  options: MemoryIntegratorOptions = {},
) {
  const corpus = buildEnhanceCorpus(api, options);

  // 龙虾 2026.4.11 公共 API：单参签名。api-builder 会自动把 pluginId 挂上。
  if (typeof api.registerMemoryCorpusSupplement === "function") {
    try {
      api.registerMemoryCorpusSupplement(corpus);
      api.logger.info("[enhance] corpus supplement 已注册（enhance 分类记忆并入 openclaw memory 搜索）");
    } catch (err) {
      api.logger.error(`[enhance] corpus supplement 注册失败: ${err}`);
    }
  } else {
    api.logger.warn(
      "[enhance] 当前 openclaw 版本未提供 registerMemoryCorpusSupplement；记忆整合跳过（建议升级到 2026.4.11+）",
    );
  }

  // v6.2.0 ⭐ 强化 prompt supplement：引导 LLM **主动**调 enhance_memory_store
  //
  // 实测痛点：用户机器 5 月以来 memories 表仅 8 条记录（vs 146 章节）—— LLM 几乎没
  // 主动用过 store 工具，导致跨 session 长期"遗忘"。原 supplement 只是简单一行
  // "提供分类记忆"——LLM 知道有这工具但不知**何时该调**。本次升级按 v5.7.27 给
  // enhance_share_file 强约束的同款套路：列具体场景 + 给可执行的判据。
  //
  if (typeof api.registerMemoryPromptSupplement === "function") {
    try {
      api.registerMemoryPromptSupplement(({ availableTools }) => {
        if (!availableTools.has("enhance_memory_store") && !availableTools.has("enhance_memory_search")) {
          return [];
        }
        return [
          "## 长期记忆（主动 store）",
          "- `enhance_memory_store(category, content)` 把跨 session 还会用上的事实存为分类记忆。5 类：`decision`（决策）/`project`（进度）/`user`（偏好）/`feedback`（踩坑）/`reference`（参考）。",
          "- 判据：下次 reset / 第二天被问到要重新解释 → store；可重新计算的、纯 tool result → 不用。`enhance_memory_search` 召回，已并入龙虾 `memory` 搜索。",
        ];
      });
      api.logger.info("[enhance] memory prompt supplement v6.2.1 已注册（精简版 ~150 token，5 类 + 判据）");
    } catch (err) {
      api.logger.warn(`[enhance] prompt supplement 注册失败: ${err}`);
    }
  }

  // enhance_memory_export — 导出为 JSON，方便同步到 Obsidian / KB
  api.registerTool(((ctx: any) => ({
    name: "enhance_memory_export",
    description: "导出当前 Agent 全部 enhance 记忆为 JSON（可同步到 Obsidian/KB）",
    parameters: {},
    async execute(_id: string, _params: Record<string, unknown>): Promise<any> {
      const openclawDir = resolveOpenClawHome(api);
      const db = getDb();
      const agentId = ((ctx?.agentId as string | undefined) ?? DEFAULT_AGENT_ID).trim();

      const rows = listRecentMemories(db, agentId, 1000);
      const json = JSON.stringify(
        {
          source: "huo15-openclaw-enhance",
          version: "2.2.0",
          exported_at: new Date().toISOString(),
          agent_id: agentId,
          count: rows.length,
          memories: rows,
        },
        null,
        2,
      );

      return {
        content: [
          {
            type: "text" as const,
            text: `已导出 ${rows.length} 条记忆 (agent: ${agentId})：\n\n${json}`,
          },
        ],
      };
    },
  })) as any, { name: "enhance_memory_export" });

  api.logger.info("[enhance] 记忆整合模块已加载（corpus supplement + 相关性评分 + 导出工具）");
}
