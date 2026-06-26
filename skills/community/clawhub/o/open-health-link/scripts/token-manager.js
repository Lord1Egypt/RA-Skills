#!/usr/bin/env node

/**
 * Manages Open Health Link authorization tokens on the local filesystem.
 *
 * Usage:
 *   node token-manager.js check   — check if a valid token exists
 *   node token-manager.js save '<json>'  — persist a new token
 *   node token-manager.js get     — retrieve the current valid token
 *   node token-manager.js clear   — remove stored token
 */

import { readFile, writeFile, unlink } from "fs/promises";
import {
  TOKEN_FILE,
  TOKEN_FALLBACK_FILES,
  ensureDataDir,
  jsonOutput,
  errorExit,
} from "./utils.js";

async function tryReadToken(filePath) {
  try {
    const raw = await readFile(filePath, "utf-8");
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

async function loadToken() {
  const candidates = [TOKEN_FILE, ...TOKEN_FALLBACK_FILES];
  for (const filePath of candidates) {
    const token = await tryReadToken(filePath);
    if (token) {
      return token;
    }
  }
  return null;
}

function isTokenValid(token) {
  return !!(token && token.authToken);
}

async function cmdCheck() {
  const token = await loadToken();
  const valid = isTokenValid(token);
  jsonOutput({
    valid,
    uid: valid ? token.uid || null : null,
  });
}

function readStdin() {
  if (process.stdin.isTTY) {
    return Promise.resolve("");
  }

  return new Promise((resolve, reject) => {
    let buf = "";
    let settled = false;
    const finish = (value) => {
      if (settled) {
        return;
      }
      settled = true;
      resolve(value);
    };

    // In some non-interactive runtimes stdin may stay open forever.
    const timer = setTimeout(() => finish(buf.trim()), 1500);
    process.stdin.setEncoding("utf-8");
    process.stdin.on("data", (chunk) => (buf += chunk));
    process.stdin.on("end", () => {
      clearTimeout(timer);
      finish(buf.trim());
    });
    process.stdin.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

async function cmdSave(jsonStr) {
  if (!jsonStr) {
    jsonStr = await readStdin();
  }
  if (!jsonStr) {
    errorExit("Usage: node token-manager.js save '<json>' (or pipe JSON via stdin)");
  }

  let data;
  try {
    data = JSON.parse(jsonStr);
  } catch {
    errorExit("Invalid JSON provided to save command.");
  }

  if (!data.authToken) {
    errorExit("Token data must contain authToken.");
  }

  const tokenRecord = {
    authToken: data.authToken,
    uid: data.uid || null,
    authType: data.authType ?? null,
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
  jsonOutput({ saved: true });
}

async function cmdGet() {
  const token = await loadToken();
  if (!isTokenValid(token)) {
    jsonOutput({ valid: false, authToken: null });
    return;
  }
  jsonOutput({ valid: true, authToken: token.authToken });
}

async function cmdClear() {
  const files = [TOKEN_FILE, ...TOKEN_FALLBACK_FILES];
  for (const filePath of files) {
    try {
      await unlink(filePath);
    } catch {
      // file may not exist, that's fine
    }
  }
  jsonOutput({ cleared: true });
}

async function main() {
  const command = process.argv[2];

  switch (command) {
    case "check":
      await cmdCheck();
      break;
    case "save":
      await cmdSave(process.argv[3]);
      break;
    case "get":
      await cmdGet();
      break;
    case "clear":
      await cmdClear();
      break;
    default:
      errorExit(
        "Unknown command. Usage: node token-manager.js <check|save|get|clear>"
      );
  }
}

main();
