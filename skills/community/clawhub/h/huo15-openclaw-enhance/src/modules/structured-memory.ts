/**
 * 模块1: 结构化记忆系统（多 Agent 隔离版）
 *
 * 每个动态 Agent（如 WeCom 用户/群组）拥有独立的记忆空间。
 * 工具使用 OpenClawPluginToolFactory 模式，从 ctx.agentId 获取当前 Agent。
 * 钩子从 ctx.agentId 获取当前 Agent。
 */
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import type { OpenClawPluginToolContext } from "openclaw/plugin-sdk/core";
import { Type } from "@sinclair/typebox";
import {
  getDb,
  storeMemory,
  searchMemories,
  getRecentMemories,
  deleteMemory,
  getMemoryStats,
  purgeMemories,
} from "../utils/sqlite-store.js";
import { resolveOpenClawHome } from "../utils/resolve-home.js";
import { DEFAULT_AGENT_ID, type MemoryConfig, type MemoryCategory } from "../types.js";

const VALID_CATEGORIES: MemoryCategory[] = ["user", "project", "feedback", "reference", "decision"];

// v5.7.2: 跟 memory-integrator 的 TAG_BLACKLIST 保持一致 — store 时拒绝写入这些 tag
const RESERVED_TAGS = new Set([
  "auto-compact",
  "auto-checkpoint",
  "audit",
  "internal",
]);

function hasReservedTag(tags: string): string | null {
  if (!tags) return null;
  for (const t of tags.split(",")) {
    const trimmed = t.trim().toLowerCase();
    if (RESERVED_TAGS.has(trimmed)) return trimmed;
  }
  return null;
}

function resolveAgentId(ctx: OpenClawPluginToolContext): string {
  return (ctx?.agentId ?? DEFAULT_AGENT_ID).trim();
}

export function registerStructuredMemory(api: OpenClawPluginApi, config?: MemoryConfig) {
  const openclawDir = resolveOpenClawHome(api);
  const db = getDb();
  const maxCtx = config?.maxContextEntries ?? 5;

  // ── Tool Factory: enhance_memory_store ──
  api.registerTool( (
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_memory_store",
      description: "存储结构化记忆（按 Agent 隔离）；规则/决策短条目，长文档走 kb-ingest",
      parameters: Type.Object({
        category: Type.Union(VALID_CATEGORIES.map((c) => Type.Literal(c)), {
          description: "user|project|feedback|reference|decision",
        }),
        content: Type.String({ description: "记忆主体内容" }),
        why: Type.Optional(
          Type.String({ description: "为什么值得记住（背景/约束）" }),
        ),
        howToApply: Type.Optional(
          Type.String({ description: "何时/如何套用" }),
        ),
        tags: Type.Optional(Type.String({ description: "逗号分隔标签" })),
        importance: Type.Optional(
          Type.Number({ description: "1-10，默认 5", minimum: 1, maximum: 10 }),
        ),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = resolveAgentId(ctx);
        const tagsRaw = (params.tags as string) ?? "";
        const reserved = hasReservedTag(tagsRaw);
        if (reserved) {
          return {
            content: [
              {
                type: "text" as const,
                text: `❌ 拒绝存储：tag "${reserved}" 是 enhance 保留的系统类标签（${[...RESERVED_TAGS].join(" / ")}），不允许在用户决策记忆中使用。请改用业务相关 tag。`,
              },
            ],
          };
        }
        const entry = storeMemory(
          db,
          agentId,
          params.category as MemoryCategory,
          params.content as string,
          tagsRaw,
          (params.importance as number) ?? 5,
          "",
          {
            why: params.why as string | undefined,
            howToApply: params.howToApply as string | undefined,
          },
        );
        return {
          content: [
            {
              type: "text" as const,
              text: `已存储记忆 #${entry.id} [${entry.category}] (agent: ${agentId}): ${(params.content as string).slice(0, 80)}...`,
            },
          ],
        };
      },
    }) as any),
    { name: "enhance_memory_store" },
  );

  // ── Tool Factory: enhance_memory_search ──
  api.registerTool( (
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_memory_search",
      description: "搜索当前 Agent 的结构化记忆，可按分类/关键词筛选",
      parameters: Type.Object({
        category: Type.Optional(
          Type.Union(VALID_CATEGORIES.map((c) => Type.Literal(c)), {
            description: "分类筛选",
          }),
        ),
        keyword: Type.Optional(Type.String({ description: "关键词" })),
        limit: Type.Optional(Type.Number({ description: "默认 10", default: 10 })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = resolveAgentId(ctx);
        const entries = searchMemories(db, agentId, {
          category: params.category as MemoryCategory | undefined,
          keyword: params.keyword as string | undefined,
          limit: (params.limit as number) ?? 10,
        });
        if (entries.length === 0) {
          return { content: [{ type: "text" as const, text: `未找到匹配的记忆 (agent: ${agentId})。` }] };
        }
        const lines = entries.map((e) => {
          const body = [
            `#${e.id} [${e.category}] (重要性:${e.importance}) ${e.created_at}`,
            `  内容: ${e.content}`,
          ];
          if (e.why && e.why.trim()) body.push(`  原因(Why): ${e.why.trim()}`);
          if (e.how_to_apply && e.how_to_apply.trim()) body.push(`  套用(How): ${e.how_to_apply.trim()}`);
          body.push(`  标签: ${e.tags || "无"}`);
          return body.join("\n");
        });
        return {
          content: [{ type: "text" as const, text: `找到 ${entries.length} 条记忆 (agent: ${agentId})：\n\n${lines.join("\n\n")}` }],
        };
      },
    }) as any),
    { name: "enhance_memory_search" },
  );

  // ── Tool Factory: enhance_memory_review ──
  api.registerTool( (
    (ctx: OpenClawPluginToolContext) => ({
      name: "enhance_memory_review",
      description: "查看 Agent 记忆统计/最近条目，或删除指定记忆",
      parameters: Type.Object({
        action: Type.Union([Type.Literal("stats"), Type.Literal("recent"), Type.Literal("delete")], {
          description: "stats|recent|delete",
        }),
        id: Type.Optional(Type.Number({ description: "delete 必填的记忆 ID" })),
        limit: Type.Optional(Type.Number({ description: "recent 条数，默认 10" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = resolveAgentId(ctx);
        const action = params.action as string;

        if (action === "stats") {
          const stats = getMemoryStats(db, agentId);
          const lines = Object.entries(stats).map(([k, v]) => `${k}: ${v}`);
          return { content: [{ type: "text" as const, text: `记忆统计 (agent: ${agentId})：\n${lines.join("\n")}` }] };
        }
        if (action === "delete") {
          const memId = params.id as number | undefined;
          if (!memId) {
            return { content: [{ type: "text" as const, text: "删除操作需要提供记忆 ID。" }] };
          }
          const ok = deleteMemory(db, agentId, memId);
          return {
            content: [{ type: "text" as const, text: ok ? `已删除记忆 #${memId}` : `未找到记忆 #${memId}（或不属于当前 Agent）` }],
          };
        }
        // recent
        const entries = getRecentMemories(db, agentId, (params.limit as number) ?? 10);
        if (entries.length === 0) {
          return { content: [{ type: "text" as const, text: `暂无记忆 (agent: ${agentId})。` }] };
        }
        const lines = entries.map((e) => {
          const extras: string[] = [];
          if (e.why && e.why.trim()) extras.push(`why="${e.why.trim().slice(0, 60)}"`);
          if (e.how_to_apply && e.how_to_apply.trim()) extras.push(`how="${e.how_to_apply.trim().slice(0, 60)}"`);
          const suffix = extras.length > 0 ? ` · ${extras.join(" · ")}` : "";
          return `#${e.id} [${e.category}] ${e.created_at}: ${e.content.slice(0, 100)}${suffix}`;
        });
        return {
          content: [{ type: "text" as const, text: `最近 ${entries.length} 条记忆 (agent: ${agentId})：\n${lines.join("\n")}` }],
        };
      },
    }) as any),
    { name: "enhance_memory_review" },
  );

  // ── 注意：不在 before_prompt_build 中注入记忆内容 ──
  // openclaw 内置 memory-core / memory-lancedb 已通过 registerMemoryCapability
  // 和 before_agent_start hook 注入记忆上下文。本插件不重复注入，
  // 仅通过上面注册的 enhance_memory_* 工具提供结构化分类记忆的补充能力。

  // ── Tool: enhance_memory_purge —— 按 tag/category 批量清理 ──
  // 给 v5.7.1 hot-fix 使用：清掉之前 before_compaction hook 误存的 [auto-compact] 噪音
  api.registerTool(
    ((ctx: OpenClawPluginToolContext) => ({
      name: "enhance_memory_purge",
      description: "按 tag 或 category 批量清理当前 Agent 的记忆（dry_run 默认 true，预览不删除）",
      parameters: Type.Object({
        tag: Type.Optional(Type.String({ description: "tag 子串匹配（LIKE %tag%）" })),
        category: Type.Optional(
          Type.Union(VALID_CATEGORIES.map((c) => Type.Literal(c)), {
            description: "限定 category",
          }),
        ),
        contentLike: Type.Optional(
          Type.String({ description: "content LIKE %?% 子串匹配" }),
        ),
        dry_run: Type.Optional(Type.Boolean({ description: "默认 true，仅预览匹配条数" })),
      }),
      async execute(_id: string, params: Record<string, unknown>) {
        const agentId = resolveAgentId(ctx);
        const tag = params.tag as string | undefined;
        const category = params.category as MemoryCategory | undefined;
        const contentLike = params.contentLike as string | undefined;
        const dryRun = params.dry_run !== false; // 默认 true 安全
        if (!tag && !category && !contentLike) {
          return {
            content: [
              { type: "text", text: "❌ 必须至少传一个过滤条件：tag / category / contentLike" },
            ],
          };
        }
        const result = purgeMemories(db, agentId, { tag, category, contentLike, dryRun });
        const verb = dryRun ? "将匹配（未删除）" : "已删除";
        return {
          content: [
            {
              type: "text",
              text: `${verb} ${result.matched} 条记忆（agent=${agentId}${tag ? `, tag~"${tag}"` : ""}${
                category ? `, category=${category}` : ""
              }${contentLike ? `, content~"${contentLike}"` : ""}）${
                dryRun ? "\n— dry_run=true，加 dry_run=false 真实删除" : ""
              }`,
            },
          ],
        };
      },
    })) as any,
    { name: "enhance_memory_purge" },
  );

  api.logger.info("[enhance] 结构化记忆模块已加载（多 Agent 隔离，不干涉 openclaw 内置记忆）");
}
