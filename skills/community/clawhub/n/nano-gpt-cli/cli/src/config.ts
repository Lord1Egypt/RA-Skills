import { mkdir, readFile, writeFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

import {
  APP_NAME,
  DEFAULT_BASE_URL,
  DEFAULT_IMAGE_MODEL,
  DEFAULT_TEXT_MODEL,
  DEFAULT_VIDEO_MODEL,
} from "./constants.js";
import type { AppConfig, OutputFormat, ResolvedSettings } from "./types.js";

export type ConfigKey =
  | "api-key"
  | "default-model"
  | "default-image-model"
  | "default-video-model"
  | "output-format"
  | "base-url";

const VALID_OUTPUT_FORMATS = new Set<OutputFormat>(["text", "json"]);

export function getConfigDir(): string {
  if (process.env.XDG_CONFIG_HOME) {
    return join(process.env.XDG_CONFIG_HOME, APP_NAME);
  }

  if (process.platform === "darwin") {
    return join(homedir(), "Library", "Application Support", APP_NAME);
  }

  if (process.platform === "win32") {
    return join(process.env.APPDATA ?? join(homedir(), "AppData", "Roaming"), APP_NAME);
  }

  return join(homedir(), ".config", APP_NAME);
}

export function getConfigPath(): string {
  return join(getConfigDir(), "config.json");
}

export async function readConfig(configPath = getConfigPath()): Promise<AppConfig> {
  try {
    const raw = await readFile(configPath, "utf8");
    const parsed = JSON.parse(raw) as AppConfig;
    return sanitizeConfig(parsed);
  } catch (error) {
    const err = error as NodeJS.ErrnoException;
    if (err.code === "ENOENT") {
      return {};
    }
    throw error;
  }
}

export function mergeConfig(
  fileConfig: AppConfig,
  env: NodeJS.ProcessEnv,
  overrides: AppConfig = {},
): ResolvedSettings {
  return {
    apiKey: overrides.apiKey ?? env.NANO_GPT_API_KEY ?? fileConfig.apiKey,
    defaultModel:
      overrides.defaultModel ??
      env.NANO_GPT_MODEL ??
      fileConfig.defaultModel ??
      DEFAULT_TEXT_MODEL,
    defaultImageModel:
      overrides.defaultImageModel ??
      env.NANO_GPT_IMAGE_MODEL ??
      fileConfig.defaultImageModel ??
      DEFAULT_IMAGE_MODEL,
    defaultVideoModel:
      overrides.defaultVideoModel ??
      env.NANO_GPT_VIDEO_MODEL ??
      fileConfig.defaultVideoModel ??
      DEFAULT_VIDEO_MODEL,
    outputFormat: normalizeOutputFormat(
      overrides.outputFormat ??
        (env.NANO_GPT_OUTPUT_FORMAT as OutputFormat | undefined) ??
        fileConfig.outputFormat ??
        "text",
    ),
    baseUrl: normalizeBaseUrl(
      overrides.baseUrl ?? env.NANO_GPT_BASE_URL ?? fileConfig.baseUrl ?? DEFAULT_BASE_URL,
    ),
  };
}

export async function resolveSettings(overrides: AppConfig = {}): Promise<ResolvedSettings> {
  const fileConfig = await readConfig();
  return mergeConfig(fileConfig, process.env, overrides);
}

export async function setConfigValue(key: ConfigKey, value: string): Promise<void> {
  const configPath = getConfigPath();
  const current = await readConfig(configPath);
  const next = { ...current, ...mapConfigValue(key, value) };

  await mkdir(dirname(configPath), { recursive: true });
  await writeFile(configPath, `${JSON.stringify(next, null, 2)}\n`, "utf8");
}

export function getConfigValue(config: AppConfig, key: ConfigKey): string | undefined {
  const mapped = mapConfigKey(key);
  const value = config[mapped];
  return typeof value === "string" ? value : undefined;
}

export function redactConfig(config: AppConfig): AppConfig {
  return {
    ...config,
    apiKey: config.apiKey ? redactSecret(config.apiKey) : undefined,
  };
}

function sanitizeConfig(config: AppConfig): AppConfig {
  return {
    apiKey: trimOrUndefined(config.apiKey),
    defaultModel: trimOrUndefined(config.defaultModel),
    defaultImageModel: trimOrUndefined(config.defaultImageModel),
    defaultVideoModel: trimOrUndefined(config.defaultVideoModel),
    outputFormat: config.outputFormat ? normalizeOutputFormat(config.outputFormat) : undefined,
    baseUrl: config.baseUrl ? normalizeBaseUrl(config.baseUrl) : undefined,
  };
}

function mapConfigValue(key: ConfigKey, value: string): AppConfig {
  switch (key) {
    case "api-key":
      return { apiKey: value.trim() };
    case "default-model":
      return { defaultModel: value.trim() };
    case "default-image-model":
      return { defaultImageModel: value.trim() };
    case "default-video-model":
      return { defaultVideoModel: value.trim() };
    case "output-format":
      return { outputFormat: normalizeOutputFormat(value as OutputFormat) };
    case "base-url":
      return { baseUrl: normalizeBaseUrl(value) };
  }
}

function mapConfigKey(key: ConfigKey): keyof AppConfig {
  switch (key) {
    case "api-key":
      return "apiKey";
    case "default-model":
      return "defaultModel";
    case "default-image-model":
      return "defaultImageModel";
    case "default-video-model":
      return "defaultVideoModel";
    case "output-format":
      return "outputFormat";
    case "base-url":
      return "baseUrl";
  }
}

function trimOrUndefined(value?: string): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

function normalizeOutputFormat(value?: OutputFormat): OutputFormat {
  if (!value) {
    return "text";
  }

  if (!VALID_OUTPUT_FORMATS.has(value)) {
    throw new Error(`Invalid output format: ${value}`);
  }

  return value;
}

function normalizeBaseUrl(value: string): string {
  return value.endsWith("/") ? value.slice(0, -1) : value;
}

function redactSecret(secret: string): string {
  if (secret.length <= 8) {
    return "*".repeat(secret.length);
  }

  return `${secret.slice(0, 4)}...${secret.slice(-4)}`;
}
