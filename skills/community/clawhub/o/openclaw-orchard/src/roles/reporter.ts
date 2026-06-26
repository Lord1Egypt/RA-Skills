import type Database from "better-sqlite3";
import type { OrchardConfig } from "../config.js";
import { isLogOnlyMode } from "../config.js";

function parseDuration(s: string): number {
  const m = s.match(/^(\d+)(h|m|s)$/);
  if (!m) return 60 * 60 * 1000;
  const n = parseInt(m[1], 10);
  if (m[2] === "h") return n * 60 * 60 * 1000;
  if (m[2] === "m") return n * 60 * 1000;
  return n * 1000;
}

let reporterInFlight = false;

async function sendReport(db: Database.Database, cfg: OrchardConfig, logger: any): Promise<void> {
  const reporterCfg = cfg.roles!.reporter!;
  const channelId = reporterCfg.channelId;

  const projects = db.prepare(`SELECT * FROM projects WHERE status = 'active'`).all() as any[];
  if (projects.length === 0) return;

  const today = new Date().toISOString().split("T")[0];

  const lines: string[] = ["📊 **OrchardOS Daily Report**\n"];
  for (const p of projects) {
    const done = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'done'`).get(p.id) as any).n;
    const running = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status IN ('running','assigned')`).get(p.id) as any).n;
    const ready = (db.prepare(`SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'ready'`).get(p.id) as any).n;
    const doneToday = (db.prepare(
      `SELECT COUNT(*) as n FROM tasks WHERE project_id = ? AND status = 'done' AND date(updated_at) = ?`
    ).get(p.id, today) as any).n;
    const next = db.prepare(
      `SELECT title FROM tasks WHERE project_id = ? AND status = 'ready' ORDER BY CASE priority WHEN 'critical' THEN 0 WHEN 'high' THEN 1 ELSE 2 END LIMIT 3`
    ).all(p.id) as any[];

    lines.push(`**${p.name}** — score: ${(p.completion_score * 100).toFixed(0)}%`);
    lines.push(`  ✅ Done today: ${doneToday} | 🔄 Running: ${running} | 📋 Ready: ${ready} | 🏁 Total done: ${done}`);
    if (next.length > 0) lines.push(`  ⏭️ Next: ${next.map((t) => t.title).join(", ")}`);
    lines.push("");
  }

  const content = lines.join("\n");

  logger.warn(`[orchard][safety] reporter send skipped for channel ${channelId || '(unset)'}; log-only/safety mode is active`);
  logger.info(content);
  return;
}

export function scheduleReporter(
  getDb: () => Database.Database,
  cfg: OrchardConfig,
  logger: any
): ReturnType<typeof setInterval> | null {
  const reporterCfg = cfg.roles?.reporter;
  if (!reporterCfg?.enabled || !reporterCfg?.reportEvery) return null;
  if (isLogOnlyMode(cfg)) {
    logger.warn(`[orchard] reporter scheduler disabled in log-only mode`);
    return null;
  }

  const interval = parseDuration(reporterCfg.reportEvery);
  logger.info(`[orchard] reporter scheduled every ${reporterCfg.reportEvery} (${interval}ms)`);

  return setInterval(async () => {
    if (reporterInFlight) {
      logger.warn(`[orchard] reporter already in flight, skipping overlapping run`);
      return;
    }
    reporterInFlight = true;
    try {
      await sendReport(getDb(), cfg, logger);
    } catch (err: any) {
      logger.error(`[orchard] reporter error: ${err?.message}`);
    } finally {
      reporterInFlight = false;
    }
  }, interval);
}
