import { randomUUID } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

export const REPORT_CONST = {
  PLUGIN: "plugin",
} as const;

export type ReportPayload = Record<string, unknown>;

export interface IReporter {
  reportFunc(category: string, payload: ReportPayload): void;
}

// ── Singleton ──

let _reporter: IReporter | undefined;

export function initReporter(opts: {
  enabled: boolean;
  type: string;
  logger: { info: (msg: string) => void; debug?: (msg: string) => void };
  instanceId: string;
  pluginVersion: string;
}): void {
  if (_reporter) return;
  if (!opts.enabled) return;
  switch (opts.type) {
    case "local":
      _reporter = new LocalReporter(opts.logger, opts.instanceId, opts.pluginVersion);
      break;
    // TODO: add new reporter type
    default:
      opts.logger.debug?.(`[memory-tdai] Unknown reporter type "${opts.type}", disabled reporting`);
      break;
  }
}

export function setReporter(reporter: IReporter): void {
  _reporter = reporter;
}

/**
 * Reset the reporter singleton so that the next `initReporter` call takes effect.
 * Must be called at plugin re-registration (hot-reload) to pick up config changes.
 */
export function resetReporter(): void {
  _reporter = undefined;
}

export function report(event: string, data: ReportPayload): void {
  if (!_reporter) return;
  try {
    _reporter.reportFunc(REPORT_CONST.PLUGIN, { event, ...data });
  } catch { /* never block business logic */ }
}

// ── LocalReporter (default) ──

class LocalReporter implements IReporter {
  constructor(
    private readonly logger: { info: (msg: string) => void },
    private readonly instanceId: string,
    private readonly pluginVersion: string,
  ) {}

  reportFunc(category: string, payload: ReportPayload): void {
    try {
      this.logger.info(JSON.stringify({
        tag: "METRIC",
        category,
        plugin: "memory-tdai",
        instanceId: this.instanceId,
        pluginVersion: this.pluginVersion,
        ts: new Date().toISOString(),
        ...payload,
      }));
    } catch { /* swallow */ }
  }
}

// ── Instance ID (persisted per-install) ──

let _instanceIdCache: string | undefined;

export async function getOrCreateInstanceId(pluginDataDir: string): Promise<string> {
  if (_instanceIdCache) return _instanceIdCache;

  const idFile = path.join(pluginDataDir, ".metadata", "instance_id");
  try {
    const existing = (await fs.readFile(idFile, "utf-8")).trim();
    if (existing) {
      _instanceIdCache = existing;
      return existing;
    }
  } catch { /* file doesn't exist */ }

  const newId = randomUUID();
  await fs.mkdir(path.dirname(idFile), { recursive: true });
  await fs.writeFile(idFile, newId, "utf-8");
  _instanceIdCache = newId;
  return newId;
}
