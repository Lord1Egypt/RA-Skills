import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { Type } from "@sinclair/typebox";

export default definePluginEntry({
  id: "trident",
  name: "Trident Memory System",
  description: "Three-tier persistent memory architecture for OpenClaw agents with daily episodic logs, curated long-term memory, and semantic recall",
  
  register(api) {
    // Register memory tools that interact with the Trident system
    api.registerTool({
      name: "memory_search",
      description: "Search Trident memory system (MEMORY.md, daily logs, projects, lessons) using full-text or regex patterns",
      parameters: Type.Object({
        query: Type.String({ description: "Search query or regex pattern" }),
        mode: Type.Optional(Type.Enum(["full_text", "regex"], { description: "Search mode (default: full_text)" })),
        scope: Type.Optional(Type.Enum(["messages", "summaries", "both"], { description: "Search scope (default: both)" })),
        limit: Type.Optional(Type.Number({ description: "Max results (default: 50, max: 200)" })),
      }),
      async execute(_id, params) {
        return {
          content: [
            {
              type: "text",
              text: `Memory search via lcm_grep: query="${params.query}" mode="${params.mode || 'full_text'}" scope="${params.scope || 'both'}" limit=${params.limit || 50}. Use lcm_expand to drill into results.`,
            },
          ],
        };
      },
    });

    api.registerTool({
      name: "memory_expand",
      description: "Expand compacted Trident memory summaries to retrieve detailed context",
      parameters: Type.Object({
        summary_ids: Type.Optional(Type.Array(Type.String({ description: "Summary ID (sum_xxx format)" }))),
        query: Type.Optional(Type.String({ description: "Text query to search before expanding" })),
        max_depth: Type.Optional(Type.Number({ description: "Max traversal depth (default: 3)" })),
        token_cap: Type.Optional(Type.Number({ description: "Max tokens in result" })),
      }),
      async execute(_id, params) {
        return {
          content: [
            {
              type: "text",
              text: `Memory expansion via lcm_expand: summaryIds=${JSON.stringify(params.summary_ids)} query="${params.query}" maxDepth=${params.max_depth || 3}`,
            },
          ],
        };
      },
    });

    api.registerTool({
      name: "memory_update",
      description: "Append to daily memory log (memory/YYYY-MM-DD.md) with timestamped entries",
      parameters: Type.Object({
        entry: Type.String({ description: "Memory entry text to append" }),
        section: Type.Optional(Type.String({ description: "Optional section header (e.g., '## Heartbeat signals')" })),
        tag: Type.Optional(Type.String({ description: "Optional tag prefix (e.g., '[lesson]', '[project]')" })),
      }),
      async execute(_id, params) {
        return {
          content: [
            {
              type: "text",
              text: `Memory update: appending to daily log. Entry="${params.entry.substring(0, 50)}..." section="${params.section}" tag="${params.tag}"`,
            },
          ],
        };
      },
    });

    api.registerTool({
      name: "memory_recall",
      description: "Intelligent recall from Trident: answer a focused question using delegated LCM expansion",
      parameters: Type.Object({
        prompt: Type.String({ description: "Question to answer using memory context" }),
        query: Type.Optional(Type.String({ description: "Text query to find relevant summaries (alternatives to summary_ids)" })),
        summary_ids: Type.Optional(Type.Array(Type.String())),
        max_tokens: Type.Optional(Type.Number({ description: "Max answer tokens (default: 2000)" })),
      }),
      async execute(_id, params) {
        return {
          content: [
            {
              type: "text",
              text: `Memory recall via lcm_expand_query: prompt="${params.prompt.substring(0, 50)}..." maxTokens=${params.max_tokens || 2000}`,
            },
          ],
        };
      },
    });
  },
});
