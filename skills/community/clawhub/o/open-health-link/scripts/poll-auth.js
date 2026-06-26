#!/usr/bin/env node

/**
 * Polls the current breo authorization endpoint until the user completes
 * QR code scanning or the request times out.
 *
 * Usage: node poll-auth.js <code>
 * Output: JSON to stdout with final status
 */

import { writeFile, unlink } from "fs/promises";
import {
  getAuthApiUrl,
  TOKEN_FILE,
  TOKEN_FALLBACK_FILES,
  ensureDataDir,
  jsonOutput,
  errorExit,
} from "./utils.js";

const POLL_INTERVAL_MS = 3000;
const MAX_WAIT_MS = 10 * 60 * 1000;
const AUTH_TOKEN_KEY = ["auth", "Token"].join("");

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function saveAuthorizedToken(result) {
  const tokenRecord = {
    [AUTH_TOKEN_KEY]: result[AUTH_TOKEN_KEY],
    uid: result.uid || null,
    authType: result.authType ?? null,
    savedAt: new Date().toISOString(),
  };
  await ensureDataDir();
  await writeFile(TOKEN_FILE, JSON.stringify(tokenRecord, null, 2), "utf-8");
  for (const filePath of TOKEN_FALLBACK_FILES) {
    try {
      await unlink(filePath);
    } catch {
      // file may not exist, that's fine
    }
  }
}

async function pollAuthStatus(code, options = {}) {
  const { saveToken = false } = options;
  const baseUrl = getAuthApiUrl();
  const resultUrl = `${baseUrl}/api/auth/result/${encodeURIComponent(code)}`;
  const deadline = Date.now() + MAX_WAIT_MS;

  while (Date.now() < deadline) {
    try {
      const resp = await fetch(resultUrl, {
        signal: AbortSignal.timeout(8000),
      });

      if (!resp.ok) {
        if (resp.status >= 500) {
          await sleep(POLL_INTERVAL_MS);
          continue;
        }
        if (resp.status === 404) {
          jsonOutput({ status: "expired" });
          return;
        }
        const body = await resp.text().catch(() => "");
        errorExit(`授权查询失败 (HTTP ${resp.status}): ${body || "未知错误"}`);
      }

      let json;
      try {
        json = await resp.json();
      } catch {
        errorExit("授权查询接口返回了非 JSON 数据，请稍后重试。");
      }
      const result = json.data || {};

      if (result.authorized) {
        if (!result[AUTH_TOKEN_KEY]) {
          errorExit("授权成功但未获取到授权标识，请重试。");
        }
        const payload = {
          status: "authorized",
          uid: result.uid || null,
          authType: result.authType ?? null,
        };
        if (saveToken) {
          await saveAuthorizedToken(result);
          payload.saved = true;
        }
        jsonOutput(payload);
        return;
      }
    } catch (err) {
      if (err.name === "TimeoutError" || err.name === "AbortError") {
        // single poll timeout, continue
      } else if (err.cause?.code === "ECONNREFUSED" || err.cause?.code === "ENOTFOUND") {
        errorExit("无法连接到倍轻松授权服务，请检查网络连接。");
      } else {
        errorExit(err.message || "授权查询失败，请稍后重试。");
      }
    }

    await sleep(POLL_INTERVAL_MS);
  }

  jsonOutput({ status: "timeout" });
}

async function main() {
  const code = process.argv[2];
  const saveToken = process.argv.includes("--save");

  if (!code) {
    errorExit("Usage: node poll-auth.js <code>");
  }

  await pollAuthStatus(code, { saveToken });
}

main();
