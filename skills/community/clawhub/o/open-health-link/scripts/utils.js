import { homedir } from "os";
import { dirname, join, resolve } from "path";
import { mkdir } from "fs/promises";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_ROOT_DIR = resolve(__dirname, "..");
const PREVIOUS_OPEN_HEALTH_LINK_DATA_DIR = join(homedir(), ".openclaw", "open-health-link");
const LEGACY_BREO_DATA_DIR = join(homedir(), ".openclaw", "breo-scalp5");

export const OPEN_HEALTH_LINK_DATA_DIR = join(
  SKILL_ROOT_DIR,
  ".open-health-link-data"
);
export const TOKEN_FILE = join(OPEN_HEALTH_LINK_DATA_DIR, "token.json");
export const TOKEN_FALLBACK_FILES = [
  join(PREVIOUS_OPEN_HEALTH_LINK_DATA_DIR, "token.json"),
  join(LEGACY_BREO_DATA_DIR, "token.json"),
];
export const CODE_EXPIRY_MS = 10 * 60 * 1000;

const BREO_AUTH_API_URL = "https://op.breo.cn/ai-oc-proxy";
const BREO_DATA_API_BASE_URL = "https://op.breo.cn/op/cla";
export const BREO_QR_BASE_URL =
  "https://breoplus.breo.cn/breoapp/appPage/scanLogin";

export function getAuthApiUrl() {
  return BREO_AUTH_API_URL;
}

export function getDataApiBaseUrl() {
  return BREO_DATA_API_BASE_URL;
}

export function getWorkspaceDir() {
  const raw = String(process.env.OPENCLAW_WORKSPACE || "").trim();
  return raw || resolve(process.cwd());
}

export async function ensureDataDir() {
  await mkdir(OPEN_HEALTH_LINK_DATA_DIR, { recursive: true });
}

export function jsonOutput(data) {
  process.stdout.write(JSON.stringify(data));
}

export function errorExit(message, code = 1) {
  process.stderr.write(JSON.stringify({ error: message }));
  process.exit(code);
}
