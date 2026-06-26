import { Type } from "@sinclair/typebox";
import type Database from "better-sqlite3";
import type { OrchardConfig } from "../config.js";
import { addKnowledge, searchKnowledge } from "../kb/knowledge.js";

type ToolResult = { content: Array<{ type: "text"; text: string }> };
function ok(data: unknown): ToolResult { return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] }; }
function err(msg: string): ToolResult { return { content: [{ type: "text", text: `Error: ${msg}` }] }; }

export function registerKbTools(api: any, getDb: () => Database.Database, getCfg: () => OrchardConfig): void {
  api.registerTool({
    name: "orchard_kb_add",
    description: "Manually add a knowledge chunk to an OrchardOS project's knowledge base",
    parameters: Type.Object({
      project_id: Type.String({ description: "Project ID" }),
      content: Type.String({ description: "Knowledge content to store" }),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(params.project_id);
      if (!project) return err(`Project ${params.project_id} not found`);
      await addKnowledge(db, getCfg(), params.project_id, params.content, "user");
      return ok({ stored: true, project_id: params.project_id });
    },
  });

  api.registerTool({
    name: "orchard_kb_search",
    description: "Search the knowledge base for a project by semantic similarity",
    parameters: Type.Object({
      project_id: Type.String({ description: "Project ID" }),
      query: Type.String({ description: "Search query" }),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const project = db.prepare(`SELECT id FROM projects WHERE id = ?`).get(params.project_id);
      if (!project) return err(`Project ${params.project_id} not found`);
      const hits = await searchKnowledge(db, getCfg(), params.project_id, params.query);
      return ok(hits.map((h) => ({ id: h.id, source: h.source, content: h.content, created_at: h.created_at })));
    },
  });
}
