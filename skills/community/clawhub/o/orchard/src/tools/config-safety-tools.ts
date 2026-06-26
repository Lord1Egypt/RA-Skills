import { Type } from "@sinclair/typebox";
import type Database from "better-sqlite3";

type ToolResult = { content: Array<{ type: "text"; text: string }> };

function ok(data: unknown): ToolResult { return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] }; }
function err(msg: string): ToolResult { return { content: [{ type: "text", text: `Error: ${msg}` }] }; }

export function registerConfigSafetyTools(
  api: any,
  getDb: () => Database.Database
): void {
  api.registerTool({
    name: "orchard_config_safety_inject",
    description: "Get config-change safety injection text. Call before making any config change.",
    parameters: Type.Object({
      profile_id: Type.String({ description: "Profile ID, use default", default: "default" }),
    }),
    async handler({ profile_id }: { profile_id: string }): Promise<ToolResult> {
      try {
        const db = getDb();
        const pid = profile_id || "default";
        const row = db.prepare("SELECT * FROM config_safety_profiles WHERE id = ?").get(pid) as any;

        if (!row) {
          return err(`Profile '${pid}' not found`);
        }

        let customRules: string[] = [];
        try {
          customRules = JSON.parse(row.custom_rules || "[]");
        } catch {
          customRules = [];
        }

        const lines: string[] = [];

        lines.push("## ⛔ Config Change Safety Protocol — MANDATORY");
        lines.push("");
        lines.push("Before making ANY OpenClaw config change:");
        lines.push("");
        lines.push("1. **Read the docs first** — fetch `https://docs.openclaw.ai/llms.txt` or the relevant doc page");
        lines.push("2. **Leave a note** in `~/.openclaw/watchdog-notes.md` describing what you are about to change");
        lines.push("3. **Make the change**, then verify it works");
        lines.push("4. **If it breaks** — the watchdog will auto-restore from backup within 60s");
        lines.push("");
        lines.push("### Watchdog Rules");
        lines.push("- Watchdog runs every 60s and monitors gateway health");
        lines.push("- Bad config → 3 consecutive failures → auto-restore from `~/.backup/openclaw-configs/`");
        lines.push("- Never delete `~/.backup/openclaw-configs/` — it's the restore source");
        lines.push("- After a config restore, check `~/.openclaw/watchdog-notes.md` for the rollback reason");
        lines.push("- To trigger a safe restart: `POST /wdog/safe-restart` or use the OrchardOS Watchdog panel");
        lines.push("- To take a manual snapshot: `POST /wdog/snapshot`");
        lines.push("");

        if (customRules.length > 0) {
          lines.push("### Custom Rules");
          for (const rule of customRules) {
            lines.push(`- ${rule}`);
          }
          lines.push("");
        }

        lines.push(`Profile: ${row.name || pid} | Watchdog active: ${row.watchdog_active ? "yes" : "no"}`);

        return ok({ injection: lines.join("\n"), profile_id: pid });
      } catch (e: any) {
        return err(e.message || String(e));
      }
    },
  });
}
