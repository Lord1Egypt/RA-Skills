/**
 * 模块: 龙虾原生 Memory Surfacer (v5.7.10)
 *
 * 作用: 解决"第二天失忆"——新 session 启动时主动 surface L1 .md memory 文件锚点,
 *       让 Claude 不再依赖"主动想起去 Read 哪个文件"。MEMORY.md 索引会被龙虾自动注入,
 *       但 200 行外的子文件 / 跟当前 cwd 无字面匹配的子文件,默认不会激活。本模块按
 *       cwd / git remote 评分把相关文件锚点提前 surface 到 prompt。
 *
 * 非侵入式保证:
 * - 完全只读 ~/.claude/projects/-<cwd-key>/memory/*.md, 不写任何文件 / 数据库
 * - 不复制 MEMORY.md (已被龙虾自动注入索引), 不复制子文件正文 (只 surface 锚点)
 * - 通过 before_prompt_build prependContext 追加, 不覆盖龙虾原生 system prompt
 * - 单 (agentId, sessionKey) 仅注入一次, 避免污染 prompt cache
 *
 * 跟其他模块的边界:
 * - session-recap: idle > 75min 时注入 chapter/todo/decision 摘要 (本模块互补,开局即注入文件锚点)
 * - memory-integrator: 把 enhance SQLite 喂给 L1 corpus 搜索 (本模块只动 .md 文件,不动 SQLite)
 * - kb-corpus: 把 ~/.openclaw/kb/shared/wiki/*.md 挂给 corpus (本模块只动 ~/.claude/projects 下的 .md)
 *
 * 红线:
 * - 不引入 child_process (企业扫描器会拦截; 用 .git/config 文件读取代替 git remote)
 * - 不发起任何网络请求
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { DEFAULT_AGENT_ID } from "../types.js";

export interface NativeMemorySurfacerConfig {
  enabled?: boolean;
  /** 显式指定 memory 目录;不指定则按 cwd 推断 (fallback 到 home memory) */
  memoryDir?: string;
  /** 单次注入最多展示的文件数,默认 12（v6.1.9 起从 5 → 12，让更多 .md 进 surface） */
  maxFiles?: number;
  /** 单文件 description 截断长度,默认 80 */
  descriptionMaxChars?: number;
  /** 评分阈值 (0-1),低于此分数的文件不进入 surface,默认 0.05（v6.1.9 起从 0.15 → 0.05，REFERENCE/USER 类也能 surface） */
  threshold?: number;
  /** v6.1.9: cwd 匹配额外加权（默认 0.2，让项目目录相关 .md 优先） */
  cwdRelevanceBoost?: number;
  /** v6.1.9: 近 7 天文件额外加权（默认 0.1，让最近编辑的 .md 优先） */
  ageRecencyBoost?: number;
  debug?: boolean;
}

interface MemoryFileMeta {
  path: string;
  basename: string;
  name?: string;
  description?: string;
  type?: string;
  mtimeMs: number;
}

const SCAN_CACHE_TTL_MS = 10 * 60_000;
const MAX_DEDUP_ENTRIES = 500;
const memoryScanCache = new Map<
  string,
  { entries: MemoryFileMeta[]; scannedAt: number; sigSum: number }
>();

function pickAgentId(ctx: { agentId?: string } | undefined): string {
  return (ctx?.agentId ?? DEFAULT_AGENT_ID).trim() || DEFAULT_AGENT_ID;
}

function pickSessionId(ctx: { sessionKey?: string; sessionId?: string } | undefined): string {
  return ((ctx?.sessionKey ?? ctx?.sessionId ?? "") + "").trim();
}

/** Claude Code 标准 cwd → memory dir key 转换:`/` → `-`, `.` → `-` */
function cwdToProjectKey(cwd: string): string {
  return cwd.replace(/\//g, "-").replace(/\./g, "-");
}

function resolveMemoryDir(explicit: string | undefined): string | undefined {
  const tryDir = (d: string): string | undefined => {
    try {
      return statSync(d).isDirectory() ? d : undefined;
    } catch {
      return undefined;
    }
  };
  if (explicit) return tryDir(explicit);
  const candidates = [
    join(homedir(), ".claude", "projects", cwdToProjectKey(process.cwd()), "memory"),
    join(homedir(), ".claude", "projects", cwdToProjectKey(homedir()), "memory"),
  ];
  for (const c of candidates) {
    const found = tryDir(c);
    if (found) return found;
  }
  return undefined;
}

function parseFrontmatter(text: string): Pick<MemoryFileMeta, "name" | "description" | "type"> {
  const lines = text.split("\n");
  if (lines[0]?.trim() !== "---") return {};
  const out: Record<string, string> = {};
  for (let i = 1; i < lines.length && i < 40; i++) {
    if (lines[i].trim() === "---") break;
    const m = lines[i].match(/^([A-Za-z_][\w-]*):\s*(.+)$/);
    if (m) out[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
  }
  return { name: out.name, description: out.description, type: out.type };
}

function scanMemoryDir(dir: string): MemoryFileMeta[] {
  let files: string[];
  try {
    files = readdirSync(dir).filter((f) => f.endsWith(".md") && f !== "MEMORY.md");
  } catch {
    return [];
  }

  let sigSum = 0;
  const stats: Array<{ file: string; mtimeMs: number }> = [];
  for (const f of files) {
    try {
      const s = statSync(join(dir, f));
      stats.push({ file: f, mtimeMs: s.mtimeMs });
      sigSum += s.mtimeMs;
    } catch {
      // 单文件 stat 失败,跳过
    }
  }

  const cached = memoryScanCache.get(dir);
  if (cached && cached.sigSum === sigSum && Date.now() - cached.scannedAt < SCAN_CACHE_TTL_MS) {
    return cached.entries;
  }

  const entries: MemoryFileMeta[] = [];
  for (const { file, mtimeMs } of stats) {
    try {
      const path = join(dir, file);
      const text = readFileSync(path, "utf8").slice(0, 2048);
      const fm = parseFrontmatter(text);
      entries.push({ path, basename: file, mtimeMs, ...fm });
    } catch {
      // 单文件读失败,跳过
    }
  }

  memoryScanCache.set(dir, { entries, scannedAt: Date.now(), sigSum });
  return entries;
}

function tokenize(s: string): string[] {
  return s
    .toLowerCase()
    .split(/[\s\W_]+/)
    .filter((t) => t.length > 2);
}

/** 从 .git/config 读 remote url (避免 child_process,符合企业扫描器红线) */
function readGitRemoteText(startCwd: string): string {
  let dir = startCwd;
  for (let i = 0; i < 8; i++) {
    try {
      const cfg = readFileSync(join(dir, ".git", "config"), "utf8");
      const urls = cfg.match(/^\s*url\s*=\s*(.+)$/gm) ?? [];
      return urls.join(" ");
    } catch {
      // 继续往上找
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  return "";
}

const TYPE_WEIGHT: Record<string, number> = {
  project: 0.3,
  feedback: 0.25,
  decision: 0.2,
  user: 0.15,
  reference: 0.1,
};

function scoreFile(
  meta: MemoryFileMeta,
  cwdTokens: Set<string>,
  remoteTokens: Set<string>,
  cwdRelevanceBoost: number = 0.2,
  ageRecencyBoost: number = 0.1,
): number {
  const haystack = [meta.name, meta.description, meta.basename]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
  if (!haystack) return 0;
  const fileTokens = tokenize(haystack);
  if (fileTokens.length === 0) return 0;

  let cwdHits = 0;
  let remoteHits = 0;
  for (const t of fileTokens) {
    if (cwdTokens.has(t)) cwdHits++;
    if (remoteTokens.has(t)) remoteHits++;
  }

  let score = 0;
  const denom = Math.min(fileTokens.length, 8);
  // v6.1.9: cwdRelevanceBoost 从 hardcoded 0.45 提到可配置（默认 0.2 + 0.45 = 0.65 总加权）
  if (cwdTokens.size > 0) score += (cwdHits / denom) * (0.45 + cwdRelevanceBoost);
  if (remoteTokens.size > 0) score += (remoteHits / denom) * 0.35;

  score += TYPE_WEIGHT[meta.type ?? ""] ?? 0.05;

  // v6.1.9: ageRecencyBoost 从 hardcoded 0.1 提到可配置（默认 0.1，近 7 天加倍 → 0.2）
  const ageDays = (Date.now() - meta.mtimeMs) / 86_400_000;
  if (ageDays <= 7) score += ageRecencyBoost * 2; // 近 7 天 2x 加权
  else if (ageDays <= 30) score += ageRecencyBoost * 0.5; // 近 30 天 0.5x

  return Math.min(1, score);
}

function buildSurfaceText(
  picked: Array<{ meta: MemoryFileMeta; score: number }>,
  descriptionMaxChars: number,
): string {
  const lines: string[] = [];
  lines.push(
    "【相关历史 memory 锚点】系统已主动调出可能相关的 L1 memory 文件;按需 Read 查看详情(本 surface 每 session 仅注入一次):",
  );
  for (const { meta } of picked) {
    const tag = meta.type ? `[${meta.type.toUpperCase()}]` : "";
    const desc = (meta.description ?? "").slice(0, descriptionMaxChars);
    const title = meta.name ?? meta.basename.replace(/\.md$/, "");
    lines.push(`  · ${tag} ${title}${desc ? ` — ${desc}` : ""}\n    Read: ${meta.path}`);
  }
  lines.push(
    "(由 enhance native-memory-surfacer 生成;关闭: config.nativeMemorySurfacer.enabled = false)",
  );
  return lines.join("\n");
}

export function registerNativeMemorySurfacer(
  api: OpenClawPluginApi,
  config?: NativeMemorySurfacerConfig,
) {
  if (config?.enabled === false) return;

  const memoryDir = resolveMemoryDir(config?.memoryDir);
  if (!memoryDir) {
    api.logger.info(
      "[enhance-surfacer] 未找到 ~/.claude/projects/-<cwd>/memory 目录,模块跳过(set config.nativeMemorySurfacer.memoryDir 显式指定)",
    );
    return;
  }

  // v6.1.9: 默认值松绑——从「5 文件 / 0.15 阈值」改成「12 文件 / 0.05 阈值」。
  // 触发：用户报"第二天失忆"。诊断：用户有 37 个 .md 但 REFERENCE(0.1)/USER(0.15) 类
  // 权重突破不了 0.15 阈值 → 72% 文件不被 surface → LLM 上下文残缺。
  // 新默认让 ≥10 个 .md 进 surface，覆盖 user 偏好/project 进度/reference 文档全部类型。
  const maxFiles = config?.maxFiles ?? 12;
  const descriptionMaxChars = config?.descriptionMaxChars ?? 80;
  const threshold = config?.threshold ?? 0.05;
  const cwdRelevanceBoost = config?.cwdRelevanceBoost ?? 0.2;
  const ageRecencyBoost = config?.ageRecencyBoost ?? 0.1;
  const debug = config?.debug === true;

  const surfacedSessions = new Map<string, number>();

  api.on("before_prompt_build", (_event, ctx) => {
    const agentId = pickAgentId(ctx);
    const sessionId = pickSessionId(ctx);
    const key = `${agentId}::${sessionId}`;
    if (surfacedSessions.has(key)) return;

    const entries = scanMemoryDir(memoryDir);
    if (entries.length === 0) {
      surfacedSessions.set(key, Date.now());
      return;
    }

    const cwd = process.cwd();
    const cwdTokens = new Set(tokenize(cwd));
    const remoteTokens = new Set(tokenize(readGitRemoteText(cwd)));

    const scored = entries
      .map((meta) => ({ meta, score: scoreFile(meta, cwdTokens, remoteTokens, cwdRelevanceBoost, ageRecencyBoost) }))
      .filter(({ score }) => score >= threshold)
      .sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        return b.meta.mtimeMs - a.meta.mtimeMs;
      })
      .slice(0, maxFiles);

    if (scored.length === 0) {
      surfacedSessions.set(key, Date.now());
      return;
    }

    // LRU eviction
    if (surfacedSessions.size >= MAX_DEDUP_ENTRIES) {
      const oldest = surfacedSessions.keys().next().value;
      if (oldest !== undefined) surfacedSessions.delete(oldest);
    }
    surfacedSessions.set(key, Date.now());

    const text = buildSurfaceText(scored, descriptionMaxChars);
    if (debug) {
      api.logger.info(
        `[enhance-surfacer] surface ${scored.length}/${entries.length} 条 (agent=${agentId}, session=${sessionId.slice(0, 12)}) dir=${memoryDir}`,
      );
    }
    return { prependContext: text };
  });

  api.logger.info(
    `[enhance] 原生记忆 surface 模块已加载 (dir=${memoryDir}, maxFiles=${maxFiles}, threshold=${threshold}, cwdBoost=${cwdRelevanceBoost}, ageBoost=${ageRecencyBoost})`,
  );
}
