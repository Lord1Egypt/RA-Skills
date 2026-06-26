import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface AsrConfig {
  provider?: "iflytek" | "openai";
  iflytek?: {
    app_id?: string;
    secret_key?: string;
  };
  openai?: {
    api_key?: string;
    base_url?: string;
    model?: string;
  };
}

export interface LinkMindConfig {
  obsidian_vault: string;
  cookies?: {
    weibo?: string;
    xiaohongshu?: string;
    wechat?: string;
    xiaoyuzhou?: string; // x-jike-access-token，用于字幕 API
  };
  asr?: AsrConfig;
}

// ---------------------------------------------------------------------------
// .env loader (minimal, no external dependency)
// ---------------------------------------------------------------------------

function loadEnvFile(path: string): void {
  if (!existsSync(path)) return;
  const content = readFileSync(path, "utf-8");
  for (const line of content.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let value = trimmed.slice(eqIdx + 1).trim();
    // Strip surrounding quotes
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

/**
 * Load .env files. Priority (highest first):
 *   1. process.env (already set)
 *   2. skills/linkmind/.env  (project-level)
 *   3. ~/.linkmind/.env      (user-level)
 */
function loadEnvFiles(configPath?: string): void {
  const home = process.env.HOME ?? process.env.USERPROFILE ?? "";
  if (home) {
    loadEnvFile(resolve(home, ".linkmind", ".env"));
  }
  if (configPath) {
    loadEnvFile(resolve(dirname(configPath), ".env"));
  }
}

// ---------------------------------------------------------------------------
// Env → config overlay
// ---------------------------------------------------------------------------

function envString(key: string): string | undefined {
  const v = process.env[key];
  return v && v.trim() ? v.trim() : undefined;
}

function applyEnvOverrides(config: LinkMindConfig): LinkMindConfig {
  config.obsidian_vault =
    envString("LINKMIND_OBSIDIAN_VAULT") ?? config.obsidian_vault;

  config.cookies ??= {};
  config.cookies.weibo =
    envString("LINKMIND_WEIBO_COOKIE") ?? config.cookies.weibo;
  config.cookies.xiaohongshu =
    envString("LINKMIND_XHS_COOKIE") ?? config.cookies.xiaohongshu;
  config.cookies.wechat =
    envString("LINKMIND_WXMP_COOKIE") ?? config.cookies.wechat;
  config.cookies.xiaoyuzhou =
    envString("LINKMIND_XIAOYUZHOU_TOKEN") ?? config.cookies.xiaoyuzhou;

  config.asr ??= {};
  config.asr.iflytek ??= {};
  config.asr.iflytek.app_id =
    envString("LINKMIND_IFLYTEK_APP_ID") ?? config.asr.iflytek.app_id;
  config.asr.iflytek.secret_key =
    envString("LINKMIND_IFLYTEK_SECRET_KEY") ?? config.asr.iflytek.secret_key;

  config.asr.openai ??= {};
  config.asr.openai.api_key =
    envString("LINKMIND_OPENAI_API_KEY") ?? config.asr.openai.api_key;
  config.asr.openai.base_url =
    envString("LINKMIND_OPENAI_BASE_URL") ?? config.asr.openai.base_url;
  config.asr.openai.model =
    envString("LINKMIND_OPENAI_MODEL") ?? config.asr.openai.model;

  return config;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

export function loadConfig(configPath: string): LinkMindConfig {
  loadEnvFiles(configPath);

  const abs = resolve(configPath);
  const raw = readFileSync(abs, "utf-8");
  const parsed = JSON.parse(raw) as LinkMindConfig;

  const config = applyEnvOverrides(parsed);

  if (!config.obsidian_vault) {
    throw new Error(
      "config.json 缺少 obsidian_vault 字段，请配置你的 Obsidian 知识库路径",
    );
  }

  return config;
}

/**
 * Parse a `--config <path>` argument from argv. Returns the config path or
 * undefined if not provided.
 */
export function parseConfigArg(argv: string[]): string | undefined {
  const idx = argv.indexOf("--config");
  if (idx !== -1 && idx + 1 < argv.length) {
    return argv[idx + 1];
  }
  return undefined;
}
