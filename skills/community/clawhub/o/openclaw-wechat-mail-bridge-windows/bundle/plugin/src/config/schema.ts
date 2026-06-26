import path from "node:path";
import { z } from "zod";

function parseCsv(input: string | undefined, fallback: string[]): string[] {
  if (!input || input.trim().length === 0) {
    return fallback;
  }

  return input
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function parseBoolean(input: string | undefined, fallback: boolean): boolean {
  if (input === undefined) {
    return fallback;
  }

  const normalized = input.trim().toLowerCase();
  return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on";
}

function parseNumber(input: string | undefined, fallback: number): number {
  if (input === undefined || input.trim().length === 0) {
    return fallback;
  }

  const value = Number(input);
  if (Number.isNaN(value)) {
    return fallback;
  }
  return value;
}

const envSchema = z
  .object({
    HOST: z.string().optional(),
    PORT: z.string().optional(),

    BRIDGE_SHARED_SECRET: z.string().optional(),
    AUTH_WINDOW_SEC: z.string().optional(),
    SQLITE_PATH: z.string().optional(),
    SWEEP_INTERVAL_SEC: z.string().optional(),
    STALE_CLAIM_SEC: z.string().optional(),
    DEDUPE_RETENTION_HOURS: z.string().optional(),
    JOB_RETENTION_HOURS: z.string().optional(),
    SIDECAR_STALE_SEC: z.string().optional(),

    ALLOW_GROUPS: z.string().optional(),
    TRIGGER_PREFIXES: z.string().optional(),
    PASSIVE_SINGLE_EMAIL_MODE: z.string().optional(),
    DEFAULT_WAIT_TIMEOUT_SEC: z.string().optional(),

    MAIL_BACKEND: z.enum(["mock", "bhmailer-http"]).optional(),
    MAIL_QUERY_MODE: z.enum(["direct-api", "push-webhook"]).optional(),
    MAIL_PREFER_PUSH_WEBHOOK: z.string().optional(),
    BHMAILER_API_BASE: z.string().optional(),
    BHMAILER_UID: z.string().optional(),
    BHMAILER_SIGN: z.string().optional(),
    BHMAILER_WEBHOOK_SECRET: z.string().optional(),
    BHMAILER_DEFAULT_TIMEOUT_SEC: z.string().optional(),
    BHMAILER_EXTRACTION_PROFILE: z.string().optional(),

    REPLY_MAX_BODY_PREVIEW_CHARS: z.string().optional(),
    REPLY_INCLUDE_SUBJECT: z.string().optional(),
    REPLY_INCLUDE_FROM: z.string().optional(),
    REPLY_INCLUDE_RECEIVED_AT: z.string().optional(),

    PRIVACY_REDACT_EMAILS_IN_LOGS: z.string().optional(),
    PRIVACY_STORE_RAW_WECHAT_TEXT: z.string().optional(),
    PRIVACY_STORE_RAW_MAIL_BODY: z.string().optional()
  })
  .passthrough();

export interface BridgeConfig {
  server: {
    host: string;
    port: number;
  };
  bridge: {
    sharedSecret: string;
    authWindowSec: number;
    sqlitePath: string;
    sweepIntervalSec: number;
    staleClaimSec: number;
    dedupeRetentionHours: number;
    jobRetentionHours: number;
    sidecarStaleSec: number;
  };
  wechat: {
    allowGroups: string[];
    triggerPrefixes: string[];
    passiveSingleEmailMode: boolean;
    defaultWaitTimeoutSec: number;
  };
  mail: {
    backend: "mock" | "bhmailer-http";
    queryMode: "direct-api" | "push-webhook";
    preferPushWebhook: boolean;
    bhmailerApiBase: string;
    uid: string;
    sign: string;
    webhookSecret?: string;
    defaultTimeoutSec: number;
    extractionProfile: string;
  };
  reply: {
    maxBodyPreviewChars: number;
    includeSubject: boolean;
    includeFrom: boolean;
    includeReceivedAt: boolean;
  };
  privacy: {
    redactEmailsInLogs: boolean;
    storeRawWechatText: boolean;
    storeRawMailBody: boolean;
  };
}

export function loadConfig(inputEnv: NodeJS.ProcessEnv = process.env): BridgeConfig {
  const env = envSchema.parse(inputEnv);

  return {
    server: {
      host: env.HOST ?? "0.0.0.0",
      port: Math.max(1, parseNumber(env.PORT, 8787))
    },
    bridge: {
      sharedSecret: env.BRIDGE_SHARED_SECRET ?? "dev-bridge-secret",
      authWindowSec: Math.max(0, parseNumber(env.AUTH_WINDOW_SEC, 300)),
      sqlitePath: env.SQLITE_PATH ?? path.resolve(process.cwd(), "state", "wechat-mail-bridge.db"),
      sweepIntervalSec: Math.max(2, parseNumber(env.SWEEP_INTERVAL_SEC, 5)),
      staleClaimSec: Math.max(10, parseNumber(env.STALE_CLAIM_SEC, 120)),
      dedupeRetentionHours: Math.max(1, parseNumber(env.DEDUPE_RETENTION_HOURS, 72)),
      jobRetentionHours: Math.max(1, parseNumber(env.JOB_RETENTION_HOURS, 24 * 7)),
      sidecarStaleSec: Math.max(5, parseNumber(env.SIDECAR_STALE_SEC, 60))
    },
    wechat: {
      allowGroups: parseCsv(env.ALLOW_GROUPS, []),
      triggerPrefixes: parseCsv(env.TRIGGER_PREFIXES, [
        "/mail",
        "查邮箱",
        "/watch",
        "/mail-watch",
        "监控"
      ]),
      passiveSingleEmailMode: parseBoolean(env.PASSIVE_SINGLE_EMAIL_MODE, false),
      defaultWaitTimeoutSec: Math.min(3600, Math.max(5, parseNumber(env.DEFAULT_WAIT_TIMEOUT_SEC, 120)))
    },
    mail: {
      backend: env.MAIL_BACKEND ?? "mock",
      queryMode: env.MAIL_QUERY_MODE ?? "direct-api",
      preferPushWebhook: parseBoolean(env.MAIL_PREFER_PUSH_WEBHOOK, true),
      bhmailerApiBase: env.BHMAILER_API_BASE ?? "",
      uid: env.BHMAILER_UID ?? "",
      sign: env.BHMAILER_SIGN ?? "",
      webhookSecret: env.BHMAILER_WEBHOOK_SECRET,
      defaultTimeoutSec: Math.max(1, parseNumber(env.BHMAILER_DEFAULT_TIMEOUT_SEC, 20)),
      extractionProfile: env.BHMAILER_EXTRACTION_PROFILE ?? "default"
    },
    reply: {
      maxBodyPreviewChars: Math.max(100, parseNumber(env.REPLY_MAX_BODY_PREVIEW_CHARS, 400)),
      includeSubject: parseBoolean(env.REPLY_INCLUDE_SUBJECT, true),
      includeFrom: parseBoolean(env.REPLY_INCLUDE_FROM, true),
      includeReceivedAt: parseBoolean(env.REPLY_INCLUDE_RECEIVED_AT, true)
    },
    privacy: {
      redactEmailsInLogs: parseBoolean(env.PRIVACY_REDACT_EMAILS_IN_LOGS, true),
      storeRawWechatText: parseBoolean(env.PRIVACY_STORE_RAW_WECHAT_TEXT, true),
      storeRawMailBody: parseBoolean(env.PRIVACY_STORE_RAW_MAIL_BODY, false)
    }
  };
}
