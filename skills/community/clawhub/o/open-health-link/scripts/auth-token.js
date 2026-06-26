import { readFile } from "fs/promises";
import { TOKEN_FILE, TOKEN_FALLBACK_FILES } from "./utils.js";

async function tryReadToken(filePath) {
  try {
    const raw = await readFile(filePath, "utf-8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export async function loadStoredAuthToken() {
  const candidates = [TOKEN_FILE, ...TOKEN_FALLBACK_FILES];
  for (const filePath of candidates) {
    const token = await tryReadToken(filePath);
    const tokenValue = typeof token?.authToken === "string" ? token.authToken.trim() : "";
    if (tokenValue) {
      return tokenValue;
    }
  }
  return null;
}
