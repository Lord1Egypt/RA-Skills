import { Type } from "@sinclair/typebox";
import { randomUUID } from "crypto";
import type Database from "better-sqlite3";
import type { OrchardConfig } from "../config.js";

type ToolResult = { content: Array<{ type: "text"; text: string }> };

function ok(data: unknown): ToolResult {
  return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
}

function err(msg: string): ToolResult {
  return { content: [{ type: "text", text: `Error: ${msg}` }] };
}

export function registerProjectTools(
  api: any,
  getDb: () => Database.Database
): void {
  api.registerTool({
    name: "orchard_project_create",
    description: "Create a new OrchardOS project with a name and goal",
    parameters: Type.Object({
      name: Type.String({ description: "Project name" }),
      goal: Type.String({ description: "High-level goal for the project" }),
      completion_temperature: Type.Optional(
        Type.Number({ description: "0=declare done early, 1=always generate more work", minimum: 0, maximum: 1 })
      ),
    }),
    execute: async (_id: string, params: any): Promise<ToolResult> => {
      const db = getDb();
      const id = randomUUID();
      const temp = params.completion_temperature ?? 0.7;
      db.prepare(`
        INSERT INTO projects (id, name, goal, completion_temperature)
        VALUES (?, ?, ?, ?)
      `).run(id, params.name, params.goal, temp);
      return ok({ id, name: params.name, goal: params.goal, completion_temperature: temp, status: "active" });
    },
  });

  api.registerTool({
    name: "orchard_project_list",
    description: "List all OrchardOS projects",
    parameters: Type.Object({}),
    execute: async (_id: string, _params: any): Promise<ToolResult> => {
      const db = getDb();
      const rows = db.prepare(`SELECT * FROM projects ORDER BY created_at DESC`).all();
      return ok(rows);
    },
  });
}
