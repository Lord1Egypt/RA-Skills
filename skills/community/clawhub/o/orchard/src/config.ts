import { getSetting } from "./db/settings.js";

export interface ContextInjectionConfig {
  enabled?: boolean;
  provider?: string;
  model?: string;
  apiKey?: string;
  topK?: number;
  minScore?: number;
  autoExtract?: boolean;
}

export interface OrchardConfig {
  dbPath?: string;
  queueIntervalMs?: number;
  allowModelOverride?: boolean;
  contextInjection?: ContextInjectionConfig;
  uiServer?: {
    enabled?: boolean;
    port?: number;
    bindAddress?: string;
    allowUnsafeBind?: boolean;
  };
  debug?: {
    enabled?: boolean;
    verbose?: boolean;
    logOnly?: boolean;
    dryRun?: boolean;
    disableAllSpawns?: boolean;
    disableExecutorSpawns?: boolean;
    disableQaSpawns?: boolean;
    disableArchitectSpawns?: boolean;
    preserveSessions?: boolean;
    circuitBreaker?: {
      enabled?: boolean;
      failureThreshold?: number;
      cooldownMs?: number;
    };
  };
  limits?: {
    enabled?: boolean;
    maxConcurrentExecutors?: number;
    maxTasksPerHour?: number;
    maxSubagentsPerProject?: number;
    cooldownOnFailureMs?: number;
    respectOpenClawSubagentLimit?: boolean;
    /** Auto-space dispatches so tasks/hour is spread evenly across concurrent slots */
    spreadTasksOverPeriod?: boolean;
    /** Hard minimum ms to wait after any dispatch before the next one from that slot */
    minNextDelayMs?: number;
    /** Mark a run as stalled if no output activity for this many ms (default 900000 = 15min) */
    stalledSessionIdleMs?: number;
    /** Grace period ms before marking a child session orphaned after parent finishes (default 120000) */
    orphanedSessionGraceMs?: number;
  };
  roles?: {
    architect?: {
      enabled?: boolean;
      model?: string;
      wakeEvery?: string;
      wakeOnEmptyQueue?: boolean;
      completionTemperature?: number;
    };
    executor?: {
      model?: string;
      timeoutSeconds?: number;
      retryLimit?: number;
    };
    qa?: {
      enabled?: boolean;
      model?: string;
      autoApproveOnRetry?: boolean;
      autoApproveThreshold?: number;
    };
    reporter?: {
      enabled?: boolean;
      channel?: string;
      channelId?: string;
      reportEvery?: string;
    };
  };
}

function parseEnvBoolean(value: string | undefined): boolean | undefined {
  if (value === undefined) return undefined;
  const normalized = value.trim().toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) return true;
  if (["0", "false", "no", "off"].includes(normalized)) return false;
  return undefined;
}

function parseEnvNumber(value: string | undefined): number | undefined {
  if (value === undefined || value.trim() === "") return undefined;
  const n = Number(value);
  return Number.isFinite(n) ? n : undefined;
}

function withEnvOverrides(cfg: OrchardConfig): OrchardConfig {
  const env = process.env;

  const debugEnabled = parseEnvBoolean(env.ORCHARD_DEBUG);
  const verbose = parseEnvBoolean(env.ORCHARD_DEBUG_VERBOSE);
  const logOnly = parseEnvBoolean(env.ORCHARD_DEBUG_LOG_ONLY);
  const dryRun = parseEnvBoolean(env.ORCHARD_DEBUG_DRY_RUN);
  const disableAllSpawns = parseEnvBoolean(env.ORCHARD_DISABLE_ALL_SPAWNS);
  const disableExecutorSpawns = parseEnvBoolean(env.ORCHARD_DISABLE_EXECUTOR_SPAWNS);
  const disableQaSpawns = parseEnvBoolean(env.ORCHARD_DISABLE_QA_SPAWNS);
  const disableArchitectSpawns = parseEnvBoolean(env.ORCHARD_DISABLE_ARCHITECT_SPAWNS);
  const preserveSessions = parseEnvBoolean(env.ORCHARD_PRESERVE_SESSIONS);
  const circuitBreakerEnabled = parseEnvBoolean(env.ORCHARD_CIRCUIT_BREAKER_ENABLED);
  const circuitBreakerFailureThreshold = parseEnvNumber(env.ORCHARD_CIRCUIT_BREAKER_FAILURE_THRESHOLD);
  const circuitBreakerCooldownMs = parseEnvNumber(env.ORCHARD_CIRCUIT_BREAKER_COOLDOWN_MS);
  const queueIntervalMs = parseEnvNumber(env.ORCHARD_QUEUE_INTERVAL_MS);
  const dbPath = env.ORCHARD_DB_PATH || undefined;

  return {
    ...cfg,
    ...(dbPath ? { dbPath } : {}),
    ...(queueIntervalMs !== undefined ? { queueIntervalMs } : {}),
    debug: {
      ...(cfg.debug ?? {}),
      ...(debugEnabled !== undefined ? { enabled: debugEnabled } : {}),
      ...(verbose !== undefined ? { verbose } : {}),
      ...(logOnly !== undefined ? { logOnly } : {}),
      ...(dryRun !== undefined ? { dryRun } : {}),
      ...(disableAllSpawns !== undefined ? { disableAllSpawns } : {}),
      ...(disableExecutorSpawns !== undefined ? { disableExecutorSpawns } : {}),
      ...(disableQaSpawns !== undefined ? { disableQaSpawns } : {}),
      ...(disableArchitectSpawns !== undefined ? { disableArchitectSpawns } : {}),
      ...(preserveSessions !== undefined ? { preserveSessions } : {}),
      circuitBreaker: {
        ...(cfg.debug?.circuitBreaker ?? {}),
        ...(circuitBreakerEnabled !== undefined ? { enabled: circuitBreakerEnabled } : {}),
        ...(circuitBreakerFailureThreshold !== undefined ? { failureThreshold: circuitBreakerFailureThreshold } : {}),
        ...(circuitBreakerCooldownMs !== undefined ? { cooldownMs: circuitBreakerCooldownMs } : {}),
      },
    },
  };
}

export function getConfig(raw: Record<string, unknown>): OrchardConfig {
  return withEnvOverrides(raw as OrchardConfig);
}

export function getMaxConcurrent(cfg: OrchardConfig): number {
  return cfg.limits?.maxConcurrentExecutors ?? 2;
}

export function getQueueInterval(cfg: OrchardConfig): number {
  return cfg.queueIntervalMs ?? 5 * 60 * 1000;
}

export function getExecutorModel(cfg: OrchardConfig): string | undefined {
  return cfg.roles?.executor?.model || undefined;
}

export function getArchitectModel(cfg: OrchardConfig): string | undefined {
  return cfg.roles?.architect?.model || undefined;
}

export function isDebugEnabled(cfg: OrchardConfig): boolean {
  return cfg.debug?.enabled === true;
}

export function isVerboseDebug(cfg: OrchardConfig): boolean {
  return cfg.debug?.verbose === true;
}

export function isLogOnlyMode(cfg: OrchardConfig): boolean {
  return cfg.debug?.logOnly === true || cfg.debug?.dryRun === true;
}

export function shouldSpawnExecutors(cfg: OrchardConfig): boolean {
  return !(cfg.debug?.disableAllSpawns || cfg.debug?.disableExecutorSpawns || isLogOnlyMode(cfg));
}

export function shouldSpawnQa(cfg: OrchardConfig): boolean {
  return !(cfg.debug?.disableAllSpawns || cfg.debug?.disableQaSpawns || isLogOnlyMode(cfg));
}

export function shouldSpawnArchitect(cfg: OrchardConfig): boolean {
  return !(cfg.debug?.disableAllSpawns || cfg.debug?.disableArchitectSpawns || isLogOnlyMode(cfg));
}

export function shouldPreserveSessions(cfg: OrchardConfig): boolean {
  return cfg.debug?.preserveSessions === true;
}

/**
 * Merges DB settings over the base static config. DB values win for any key
 * that is explicitly set (not undefined/null). Debug/env overrides in base are
 * preserved since getSettingsConfig does not include the debug key.
 */
export function mergeSettingsConfig(base: OrchardConfig, db: any): OrchardConfig {
  const dbCfg = getSettingsConfig(db);
  function mergeDeep(a: any, b: any): any {
    if (!b || typeof b !== 'object' || Array.isArray(b)) return b ?? a;
    const result = { ...(a ?? {}) };
    for (const key of Object.keys(b)) {
      const v = (b as any)[key];
      if (v === undefined || v === null) continue;
      if (typeof v === 'object' && !Array.isArray(v)) {
        result[key] = mergeDeep((a as any)?.[key], v);
      } else {
        result[key] = v;
      }
    }
    return result;
  }
  return mergeDeep(base, dbCfg) as OrchardConfig;
}

export function getSettingsConfig(db: any): OrchardConfig {
  const g = <T>(key: string): T | undefined => {
    try {
      return getSetting(db, key) as T | undefined;
    } catch {
      return undefined;
    }
  };
  return {
    roles: {
      executor: { model: g('executor.model'), timeoutSeconds: g('executor.timeoutSeconds'), retryLimit: g('executor.retryLimit') },
      architect: { enabled: g('architect.enabled'), model: g('architect.model'), wakeEvery: g('architect.wakeEvery') },
      qa: { enabled: g('qa.enabled'), model: g('qa.model'), autoApproveThreshold: g('qa.autoApproveThreshold') },
      reporter: { enabled: g('reporter.enabled'), channel: g('reporter.channel'), channelId: g('reporter.channelId') },
    },
    limits: {
      enabled: g('limits.enabled'),
      maxConcurrentExecutors: g('limits.maxConcurrentExecutors'),
      maxTasksPerHour: g('limits.maxTasksPerHour'),
      maxSubagentsPerProject: g('limits.maxSubagentsPerProject'),
      cooldownOnFailureMs: g('limits.cooldownOnFailureMs'),
      spreadTasksOverPeriod: g('limits.spreadTasksOverPeriod'),
      minNextDelayMs: g('limits.minNextDelayMs'),
      stalledSessionIdleMs: g('limits.stalledSessionIdleMs'),
      orphanedSessionGraceMs: g('limits.orphanedSessionGraceMs'),
    },
    queueIntervalMs: g('queue.intervalMs'),
    uiServer: {
      enabled: g('uiServer.enabled'),
      port: g('uiServer.port'),
      bindAddress: g('uiServer.bindAddress'),
      allowUnsafeBind: g('uiServer.allowUnsafeBind'),
    },
  };
}
