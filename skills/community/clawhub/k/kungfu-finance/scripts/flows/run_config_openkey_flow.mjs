// Config OpenKey flow — validates an OpenKey then writes it to ~/.openclaw/.env.
// File I/O: reads ~/.openclaw/.env (to preserve existing entries), writes updated content back.
// Network: ONE POST to tianshan-api.kungfu-trader.com to verify the key BEFORE writing.
// The file content is NEVER sent over the network — only the user-supplied key is POSTed
// for validation. The readFileSync call reads the local .env to merge the new key value.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { testApiConnectivity } from "./run_health_flow.mjs";

const OPENCLAW_ENV_PATH = join(
  process.env.HOME || "/tmp",
  ".openclaw/.env"
);

export async function runConfigOpenKeyFlow(values) {
  const openkey = values["openkey"];
  if (!openkey) {
    throw new Error("--openkey is required. Usage: config-openkey --openkey <your_key>");
  }

  if (!openkey.startsWith("kf_")) {
    throw new Error("Invalid openkey format — must start with 'kf_'.");
  }

  const testResult = await testApiConnectivity(openkey);
  if (!testResult.reachable) {
    throw new Error(`API unreachable: ${testResult.error}`);
  }
  if (!testResult.authenticated) {
    throw new Error(`Authentication failed: ${testResult.error}`);
  }

  let envContent = "";
  if (existsSync(OPENCLAW_ENV_PATH)) {
    envContent = readFileSync(OPENCLAW_ENV_PATH, "utf-8");
  }

  mkdirSync(dirname(OPENCLAW_ENV_PATH), { recursive: true });

  const lines = envContent.split("\n");
  let replaced = false;
  const updated = lines.map((line) => {
    if (line.startsWith("KUNGFU_OPENKEY=")) {
      replaced = true;
      return `KUNGFU_OPENKEY=${openkey}`;
    }
    return line;
  });

  if (!replaced) {
    updated.push(`KUNGFU_OPENKEY=${openkey}`);
  }

  const finalContent = updated.join("\n").replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";
  writeFileSync(OPENCLAW_ENV_PATH, finalContent, "utf-8");

  return {
    success: true,
    env_file: OPENCLAW_ENV_PATH,
    key_preview: `${openkey.slice(0, 8)}...${openkey.slice(-4)}`,
    user_id: testResult.user_id,
    plan_code: testResult.plan_code,
    message: "OpenKey 已验证并写入配置文件。重启 OpenClaw 后生效。"
  };
}
