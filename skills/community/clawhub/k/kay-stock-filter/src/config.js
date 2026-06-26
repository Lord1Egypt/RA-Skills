import { config as loadDotenv } from "dotenv";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
loadDotenv({ path: resolve(__dirname, "..", ".env") });

export const API_BASE_URL = (process.env.STOCK_API_BASE_URL || "").replace(/\/+$/, "");
export const API_KEY = process.env.STOCK_API_KEY || "";
export const API_TIMEOUT = Number(process.env.STOCK_API_TIMEOUT || "30") * 1000;
export const API_PREFIX = "/api/v1";

export function getApiUrl(path) {
  if (!API_BASE_URL) {
    throw new Error("未设置 STOCK_API_BASE_URL 环境变量");
  }
  return `${API_BASE_URL}${API_PREFIX}${path}`;
}

export function getAuthHeaders() {
  const headers = { "Content-Type": "application/json", Accept: "application/json" };
  if (API_KEY) headers["X-API-Key"] = API_KEY;
  return headers;
}
