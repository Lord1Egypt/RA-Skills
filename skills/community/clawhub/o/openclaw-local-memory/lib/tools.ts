/**
 * Local Memory Tools
 * 
 * Provides tools for:
 * - Search: Find relevant memories
 * - Store: Save a specific memory
 * - List: View all memories
 * - Forget: Delete a memory
 * - Wipe: Delete all memories
 * - Profile: View user profile built from memory
 * - Stats: View memory statistics
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/plugin-runtime.js";
import type { LocalMemoryStore } from "./store.js";

interface LocalMemoryConfig {
  autoRecall?: boolean;
  autoCapture?: boolean;
  maxRecallResults?: number;
  similarityThreshold?: number;
  debug?: boolean;
  captureInterval?: number;
  captureSignificantOnly?: boolean;
  pruneAfterCapture?: boolean;
  maxMemories?: number;
  pruneOlderThanDays?: number;
}

type LogFn = (level: "info" | "warn" | "debug", msg: string, data?: Record<string, unknown>) => void;

// ─── Helper: Format Memory Line ───────────────────────────────────────────────

function formatMemoryLine(r: { content: string; similarity: number; importance: number; metadata: Record<string, unknown> }): string {
  const cat = r.metadata?.category ?? "other";
  const sim = Math.round(r.similarity * 100);
  const imp = Math.round(r.importance * 100);
  const age = formatAge(r.metadata?.createdAt as string ?? new Date().toISOString());
  const content = r.content.length > 400 ? r.content.slice(0, 400) + "..." : r.content;
  return `[${cat}·R:${sim}%·I:${imp}%·${age}]\n${content}`;
}

function formatAge(isoTimestamp: string): string {
  try {
    const dt = new Date(isoTimestamp);
    const now = new Date();
    const days = (now.getTime() - dt.getTime()) / (24 * 60 * 60 * 1000);
    if (days < 1) return "today";
    if (days < 7) return `${Math.floor(days)}d`;
    if (days < 30) return `${Math.floor(days / 7)}w`;
    return `${Math.floor(days / 30)}mo`;
  } catch {
    return "unknown";
  }
}

// ─── Search Tool ─────────────────────────────────────────────────────────────

export function registerSearchTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_search",
    description: "Search through long-term memories using semantic vector search. Returns memories ranked by relevance, importance, and recency.",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "What to search for (natural language)" },
        limit: { type: "number", description: "Max results (default 10)" },
        threshold: { type: "number", description: "Min relevance score 0-1 (default 0.3)" },
      },
      required: ["query"],
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? cfg.maxRecallResults ?? 10;
        const threshold = params.threshold ?? cfg.similarityThreshold ?? 0.3;
        const results = await store.search(params.query, limit, threshold);

        if (results.length === 0) {
          return { content: [{ type: "text", text: "No memories found matching that query." }] };
        }

        const lines = results.map(formatMemoryLine);

        return {
          content: [{
            type: "text",
            text: `Found ${results.length} relevant memories:\n\n${lines.join("\n\n---\n\n")}`,
          }],
        };
      } catch (err) {
        log("warn", "search tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Search failed: ${String(err)}` }] };
      }
    },
  });
}

// ─── Store Tool ────────────────────────────────────────────────────────────────

export function registerStoreTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_store",
    description: "Store a piece of information in long-term memory with automatic significance detection and categorization.",
    parameters: {
      type: "object",
      properties: {
        content: { type: "string", description: "What to remember" },
        category: {
          type: "string",
          description: "Category: preference, fact, decision, entity, skill, context, or other (auto-detected if omitted)",
        },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Optional tags for this memory",
        },
      },
      required: ["content"],
    },
    async execute(_id, params) {
      try {
        const validCategories = ["preference", "fact", "decision", "entity", "skill", "context", "other"];
        const category = params.category && validCategories.includes(params.category)
          ? params.category as any
          : undefined;

        const id = await store.add(params.content, {
          category,
          tags: params.tags,
          source: "user",
        });

        log("info", "memory stored via tool", { id });
        return {
          content: [{
            type: "text",
            text: `Stored in memory (id: ${id.slice(0, 8)})${category ? ` [${category}]` : ""}`,
          }],
        };
      } catch (err) {
        log("warn", "store tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to store: ${String(err)}` }] };
      }
    },
  });
}

// ─── List Tool ───────────────────────────────────────────────────────────────

export function registerListTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_list",
    description: "List all memories, optionally filtered by category. Shows most recently accessed first.",
    parameters: {
      type: "object",
      properties: {
        category: {
          type: "string",
          description: "Filter by category: preference, fact, decision, entity, skill, other",
        },
        limit: { type: "number", description: "Max results (default 20)" },
        sort: {
          type: "string",
          description: "Sort by: recent, importance, frequent (default: recent)",
        },
      },
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? 20;
        let memories;

        if (params.category) {
          memories = await store.getByCategory(params.category as any);
        } else if (params.sort === "importance") {
          memories = await store.listAll(limit * 2);
          memories.sort((a, b) => b.importance - a.importance);
          memories = memories.slice(0, limit);
        } else if (params.sort === "frequent") {
          memories = await store.getFrequent(limit);
        } else {
          memories = await store.listAll(limit);
        }

        if (memories.length === 0) {
          return { content: [{ type: "text", text: "No memories found." }] };
        }

        const lines = memories.map((m) => {
          const cat = m.metadata.category;
          const age = formatAge(m.metadata.createdAt);
          const imp = Math.round(m.importance * 100);
          const content = m.content.length > 200 ? m.content.slice(0, 200) + "..." : m.content;
          return `[${cat}·${imp}%·${age}]\n${content}`;
        });

        return {
          content: [{
            type: "text",
            text: `${memories.length} memories:\n\n${lines.join("\n\n---\n\n")}`,
          }],
        };
      } catch (err) {
        log("warn", "list tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to list: ${String(err)}` }] };
      }
    },
  });
}

// ─── Forget Tool ─────────────────────────────────────────────────────────────

export function registerForgetTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  cfg: LocalMemoryConfig,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_forget",
    description: "Delete the most relevant memory matching a query. Use to remove outdated or incorrect memories.",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "Query to find memory to delete" },
        limit: { type: "number", description: "Number of memories to delete (default 1)" },
      },
      required: ["query"],
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? 1;
        const result = await store.forgetByQuery(params.query, limit);
        
        if (result.success) {
          log("info", "memory forgotten via tool", { query: params.query });
        }
        
        return { content: [{ type: "text", text: result.message }] };
      } catch (err) {
        log("warn", "forget tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to forget: ${String(err)}` }] };
      }
    },
  });
}

// ─── Wipe Tool ─────────────────────────────────────────────────────────────

export function registerWipeTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_wipe",
    description: "Delete ALL memories. This is irreversible! Requires confirmation.",
    parameters: {
      type: "object",
      properties: {
        confirm: { type: "boolean", description: "Must be true to confirm wipe" },
      },
      required: ["confirm"],
    },
    async execute(_id, params) {
      try {
        if (!params.confirm) {
          return { content: [{ type: "text", text: "Wipe cancelled. Set confirm=true to proceed." }] };
        }
        
        const result = await store.wipeAll();
        log("info", "all memories wiped", { count: result.deletedCount });
        
        return {
          content: [{
            type: "text",
            text: `Wiped ${result.deletedCount} memories. This cannot be undone.`,
          }],
        };
      } catch (err) {
        log("warn", "wipe tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to wipe: ${String(err)}` }] };
      }
    },
  });
}

// ─── Profile Tool ───────────────────────────────────────────────────────────

export function registerProfileTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_profile",
    description: "View the user profile built from memory - entities, preferences, facts, and recent context.",
    parameters: {
      type: "object",
      properties: {},
    },
    async execute(_id, _params) {
      try {
        const profile = await store.buildProfile();

        const sections: string[] = [];

        if (profile.entities.length > 0) {
          sections.push(`## 👤 Known Entities\n${profile.entities.map(e => `- ${e}`).join("\n")}`);
        }

        if (profile.preferences.length > 0) {
          sections.push(`## ❤️ Preferences\n${profile.preferences.map(p => `- ${p}`).join("\n")}`);
        }

        if (profile.static.length > 0) {
          sections.push(`## 📝 Key Facts\n${profile.static.map(f => `- ${f}`).join("\n")}`);
        }

        if (profile.dynamic.length > 0) {
          sections.push(`## 🔄 Recent Context\n${profile.dynamic.map(d => `- ${d}`).join("\n")}`);
        }

        if (sections.length === 0) {
          return { content: [{ type: "text", text: "No profile data yet. Memory is being built over time." }] };
        }

        return {
          content: [{
            type: "text",
            text: `# 🧠 Memory Profile\n\n${sections.join("\n\n")}`,
          }],
        };
      } catch (err) {
        log("warn", "profile tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to get profile: ${String(err)}` }] };
      }
    },
  });
}

// ─── Stats Tool ─────────────────────────────────────────────────────────────

export function registerStatsTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_stats",
    description: "View memory statistics - total count, category breakdown, cleanup status.",
    parameters: {
      type: "object",
      properties: {},
    },
    async execute(_id, _params) {
      try {
        const stats = await store.getStats();
        const count = await store.count();

        const categories = Object.entries(stats.categoryBreakdown)
          .map(([cat, count]) => `${cat}: ${count}`)
          .join(", ");

        return {
          content: [{
            type: "text",
            text: `# 📊 Memory Statistics

- **Total Memories:** ${count}
- **Chunks:** ${stats.totalChunks}
- **Avg Importance:** ${Math.round(stats.avgImportance * 100)}%
- **Categories:** ${categories || "none"}
- **Last Cleanup:** ${stats.lastCleanup ? formatAge(stats.lastCleanup) : "never"}`,
          }],
        };
      } catch (err) {
        log("warn", "stats tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed to get stats: ${String(err)}` }] };
      }
    },
  });
}

// ─── Recent Tool ────────────────────────────────────────────────────────────

export function registerRecentTool(
  api: OpenClawPluginApi,
  store: LocalMemoryStore,
  log: LogFn,
) {
  api.registerTool({
    name: "local_memory_recent",
    description: "Get recently accessed memories.",
    parameters: {
      type: "object",
      properties: {
        limit: { type: "number", description: "Max results (default 5)" },
      },
    },
    async execute(_id, params) {
      try {
        const limit = params.limit ?? 5;
        const memories = await store.getRecent(limit);

        if (memories.length === 0) {
          return { content: [{ type: "text", text: "No recent memories." }] };
        }

        const lines = memories.map((m) => {
          const cat = m.metadata.category;
          const age = formatAge(m.metadata.createdAt);
          const content = m.content.length > 200 ? m.content.slice(0, 200) + "..." : m.content;
          return `[${cat}·${age}]\n${content}`;
        });

        return {
          content: [{
            type: "text",
            text: `## 🕐 Recent Memories\n\n${lines.join("\n\n---\n\n")}`,
          }],
        };
      } catch (err) {
        log("warn", "recent tool failed", { error: String(err) });
        return { content: [{ type: "text", text: `Failed: ${String(err)}` }] };
      }
    },
  });
}
