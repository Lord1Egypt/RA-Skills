/**
 * 模块: 知识库语料（KB Corpus）
 *
 * 设计原则（非侵入 + 职责分离）：
 * - 把 huo15-openclaw-openai-knowledge-base 技能的**共享知识库** wiki 挂为
 *   龙虾原生 memory 的 corpus supplement（corpus="kb"）。
 * - 只读源：扫描 ~/.openclaw/kb/shared/wiki/*.md，不写入。
 * - 与 enhance-memory 解耦：
 *     L2 enhance-memory：结构化「规则/为什么」（短条目）
 *     L3 KB wiki：长文档「事实/资料」（整篇 MD）
 * - 不处理 agent-scope kb（那是 per-agent 私有，不跨 agent 共享，不入 corpus）。
 *
 * Public API 对接（openclaw 2026.4.11）：
 *   api.registerMemoryCorpusSupplement(supplement)     — 单参
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { homedir } from "node:os";

const PLUGIN_CORPUS_ID = "kb";
const DEFAULT_SHARED_KB = join(homedir(), ".openclaw", "kb", "shared");
const WIKI_SUBDIR = "wiki";

// ── 龙虾记忆 SDK 本地类型（与 openclaw memory-state.ts 对齐） ──
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

export interface KbCorpusConfig {
  enabled?: boolean;
  /** 共享 KB 根目录，默认 ~/.openclaw/kb/shared */
  sharedKbPath?: string;
  /** 相关性阈值（0-1），低于此分数不返回，默认 0.3（KB 门槛低于 memory） */
  threshold?: number;
  /** 单次 search 最多返回几条，默认 5 */
  maxResults?: number;
  debug?: boolean;
}

// ── 扫描 shared wiki 目录 ──
interface WikiEntry {
  absPath: string;
  relPath: string; // 相对 wiki/ 的路径，作为 id
  title: string;
  content: string;
  updatedAt: string;
}

function listMarkdown(dir: string): string[] {
  const out: string[] = [];
  let items: string[];
  try {
    items = readdirSync(dir);
  } catch {
    return out;
  }
  for (const item of items) {
    if (item.startsWith(".") || item.startsWith("_")) continue;
    const full = join(dir, item);
    let st;
    try {
      st = statSync(full);
    } catch {
      continue;
    }
    if (st.isDirectory()) {
      out.push(...listMarkdown(full));
    } else if (item.endsWith(".md")) {
      out.push(full);
    }
  }
  return out;
}

function loadWikiEntry(wikiRoot: string, absPath: string): WikiEntry | null {
  let content: string;
  let mtime: Date;
  try {
    content = readFileSync(absPath, "utf8");
    mtime = statSync(absPath).mtime;
  } catch {
    return null;
  }
  const titleMatch = content.match(/^#\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim() : absPath.split("/").pop() ?? absPath;
  return {
    absPath,
    relPath: relative(wikiRoot, absPath),
    title,
    content,
    updatedAt: mtime.toISOString(),
  };
}

// ── 相关性评分（KB 专用：title 权重最高，子串匹配 + token 匹配） ──
function scoreEntry(entry: WikiEntry, query: string): number {
  const q = query.toLowerCase();
  const titleLower = entry.title.toLowerCase();
  const contentLower = entry.content.toLowerCase();

  if (!q) return 0;

  let score = 0;
  // title 完整匹配强信号
  if (titleLower.includes(q)) score += 0.6;
  // token 匹配
  const tokens = q.split(/[\s\W]+/).filter((t) => t.length >= 2);
  if (tokens.length > 0) {
    const titleHits = tokens.filter((t) => titleLower.includes(t)).length;
    const contentHits = tokens.filter((t) => contentLower.includes(t)).length;
    score += 0.25 * (titleHits / tokens.length);
    score += 0.2 * (contentHits / tokens.length);
  }
  // content 子串命中额外加分（长文档不应被 token 稀释）
  if (contentLower.includes(q)) score += 0.15;
  return Math.min(1, score);
}

function buildSnippet(content: string, query: string, width = 300): string {
  const q = query.toLowerCase();
  const lower = content.toLowerCase();
  const idx = lower.indexOf(q);
  if (idx < 0) return content.slice(0, width).trim();
  const start = Math.max(0, idx - Math.floor(width / 3));
  const end = Math.min(content.length, start + width);
  const prefix = start > 0 ? "…" : "";
  const suffix = end < content.length ? "…" : "";
  return prefix + content.slice(start, end).trim() + suffix;
}

function findEntryByLookup(wikiRoot: string, lookup: string): string | null {
  const normalized = lookup.replace(/^kb:\/\//, "").replace(/^\//, "");
  const candidates = [
    resolve(wikiRoot, normalized),
    resolve(wikiRoot, normalized.endsWith(".md") ? normalized : `${normalized}.md`),
  ];
  for (const c of candidates) {
    try {
      if (!c.startsWith(resolve(wikiRoot))) continue; // 防止越界
      if (statSync(c).isFile()) return c;
    } catch {
      // ignore
    }
  }
  // 兜底：扫描匹配相对路径
  for (const abs of listMarkdown(wikiRoot)) {
    if (relative(wikiRoot, abs) === normalized) return abs;
    if (relative(wikiRoot, abs) === `${normalized}.md`) return abs;
  }
  return null;
}

// ── 构建 MemoryCorpusSupplement ──
function buildKbCorpus(
  api: OpenClawPluginApi,
  config: Required<Pick<KbCorpusConfig, "sharedKbPath" | "threshold" | "maxResults" | "debug">>,
): MemoryCorpusSupplement {
  const wikiRoot = join(config.sharedKbPath, WIKI_SUBDIR);

  return {
    async search({ query, maxResults }) {
      const cleanQuery = (query ?? "").trim();
      if (!cleanQuery) return [];

      const files = listMarkdown(wikiRoot);
      if (files.length === 0) return [];

      const limit = maxResults ?? config.maxResults;
      const scored: Array<{ entry: WikiEntry; score: number }> = [];
      for (const f of files) {
        const entry = loadWikiEntry(wikiRoot, f);
        if (!entry) continue;
        const score = scoreEntry(entry, cleanQuery);
        if (score >= config.threshold) {
          scored.push({ entry, score });
        }
      }

      scored.sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        return b.entry.updatedAt.localeCompare(a.entry.updatedAt);
      });

      if (config.debug) {
        api.logger.info(
          `[enhance] kb corpus.search query="${cleanQuery.slice(0, 60)}" → ${scored.length}/${files.length} 条`,
        );
      }

      return scored.slice(0, limit).map(({ entry, score }) => ({
        corpus: PLUGIN_CORPUS_ID,
        path: `kb://${entry.relPath}`,
        title: entry.title,
        kind: "wiki",
        score,
        snippet: buildSnippet(entry.content, cleanQuery),
        id: entry.relPath,
        citation: `@kb:${entry.relPath}`,
        provenanceLabel: "shared-kb",
        sourceType: "wiki_markdown",
        sourcePath: entry.absPath,
        updatedAt: entry.updatedAt,
      }));
    },

    async get({ lookup, fromLine = 1, lineCount = 200 }) {
      const abs = findEntryByLookup(wikiRoot, lookup);
      if (!abs) return null;
      const entry = loadWikiEntry(wikiRoot, abs);
      if (!entry) return null;

      const lines = entry.content.split("\n");
      const startLine = Math.max(1, Math.min(fromLine, lines.length));
      const endLine = Math.min(startLine + lineCount - 1, lines.length);
      const selected = lines.slice(startLine - 1, endLine);

      return {
        corpus: PLUGIN_CORPUS_ID,
        path: `kb://${entry.relPath}`,
        title: entry.title,
        kind: "wiki",
        content: selected.join("\n"),
        fromLine: startLine,
        lineCount: selected.length,
        id: entry.relPath,
        provenanceLabel: "shared-kb",
        sourceType: "wiki_markdown",
        sourcePath: entry.absPath,
        updatedAt: entry.updatedAt,
      };
    },
  };
}

// ── 主注册入口 ──
export function registerKbCorpus(api: OpenClawPluginApi, options: KbCorpusConfig = {}) {
  if (options.enabled === false) {
    api.logger.info("[enhance] kb corpus 已禁用（config.kbCorpus.enabled=false）");
    return;
  }

  const resolved = {
    sharedKbPath: options.sharedKbPath ?? DEFAULT_SHARED_KB,
    threshold: options.threshold ?? 0.3,
    maxResults: options.maxResults ?? 5,
    debug: options.debug ?? false,
  };

  if (typeof api.registerMemoryCorpusSupplement !== "function") {
    api.logger.warn(
      "[enhance] 当前 openclaw 版本未提供 registerMemoryCorpusSupplement；kb corpus 跳过",
    );
    return;
  }

  const corpus = buildKbCorpus(api, resolved);
  try {
    api.registerMemoryCorpusSupplement(corpus);
    api.logger.info(
      `[enhance] kb corpus 已注册（共享知识库 → memory_search；path=${resolved.sharedKbPath}）`,
    );
  } catch (err) {
    api.logger.error(`[enhance] kb corpus 注册失败: ${err}`);
  }

  // 在 memory system prompt 加一行说明
  if (typeof api.registerMemoryPromptSupplement === "function") {
    try {
      api.registerMemoryPromptSupplement(() => [
        "- `corpus=\"kb\"` 来自 huo15-openclaw-openai-knowledge-base 技能的**共享知识库**（长文档/外部资料）；当需要事实性资料而非行为规则时优先。",
      ]);
    } catch (err) {
      api.logger.warn(`[enhance] kb prompt supplement 注册失败: ${err}`);
    }
  }
}
