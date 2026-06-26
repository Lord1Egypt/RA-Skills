#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";

export const defaultEnvPath = "/Users/dellymac/.openclaw/secrets/notion.env";

export async function loadLocalEnv(file = defaultEnvPath) {
  try {
    const raw = await fs.readFile(file, "utf8");
    for (const line of raw.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) {
        continue;
      }
      const equalsIndex = trimmed.indexOf("=");
      if (equalsIndex === -1) {
        continue;
      }
      const key = trimmed.slice(0, equalsIndex).trim();
      let value = trimmed.slice(equalsIndex + 1).trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      if (key && !process.env[key]) {
        process.env[key] = value;
      }
    }
    return { ok: true, path: file };
  } catch (error) {
    if (error.code === "ENOENT") {
      return { ok: false, path: file, missing: true };
    }
    throw error;
  }
}

export async function writeEnvFile(values, file = defaultEnvPath) {
  const current = await readEnvFile(file);
  const merged = { ...current, ...values };
  const lines = [
    "# OpenClaw local runtime env",
    ...Object.entries(merged).map(([key, value]) => `${key}=${value ?? ""}`),
    "",
  ];
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, lines.join("\n"), { mode: 0o600 });
  await fs.chmod(file, 0o600);
  return { ok: true, path: file, values: merged };
}

export async function readEnvFile(file = defaultEnvPath) {
  try {
    const raw = await fs.readFile(file, "utf8");
    const values = {};
    for (const line of raw.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) {
        continue;
      }
      const equalsIndex = trimmed.indexOf("=");
      if (equalsIndex === -1) {
        continue;
      }
      const key = trimmed.slice(0, equalsIndex).trim();
      let value = trimmed.slice(equalsIndex + 1).trim();
      if (
        (value.startsWith('"') && value.endsWith('"')) ||
        (value.startsWith("'") && value.endsWith("'"))
      ) {
        value = value.slice(1, -1);
      }
      values[key] = value;
    }
    return values;
  } catch (error) {
    if (error.code === "ENOENT") {
      return {};
    }
    throw error;
  }
}
