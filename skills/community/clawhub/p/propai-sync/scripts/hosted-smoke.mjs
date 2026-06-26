#!/usr/bin/env node

import { spawn } from "node:child_process";
import { createWriteStream } from "node:fs";
import { mkdir, mkdtemp } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..", "..", "..");
const port = Number.parseInt(process.env.PROPAI_SYNC_SMOKE_PORT ?? "18991", 10);

if (!Number.isFinite(port) || port <= 0) {
  console.error("Invalid PROPAI_SYNC_SMOKE_PORT");
  process.exit(1);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function onceExit(child) {
  return new Promise((resolve) => {
    child.once("exit", (code, signal) => resolve({ code, signal }));
  });
}

async function fetchJsonOrThrow(url, init = {}, expectedStatus) {
  const res = await fetch(url, init);
  const text = await res.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text };
  }
  if (!res.ok || (expectedStatus !== undefined && res.status !== expectedStatus)) {
    throw new Error(`${url} failed (${res.status}): ${text}`);
  }
  return body;
}

async function waitForHealth(baseUrl, timeoutMs = 20000) {
  const deadline = Date.now() + timeoutMs;
  let lastError = new Error("health check did not respond");
  while (Date.now() < deadline) {
    try {
      return await fetchJsonOrThrow(`${baseUrl}/api/health`, { method: "GET" }, 200);
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));
      await sleep(500);
    }
  }
  throw lastError;
}

async function stopProcess(child) {
  if (child.exitCode !== null) {
    return;
  }
  child.kill("SIGTERM");
  await Promise.race([onceExit(child), sleep(2000)]);
  if (child.exitCode === null) {
    child.kill("SIGKILL");
    await onceExit(child);
  }
}

async function main() {
  const logsRoot = path.join(repoRoot, ".tmp-job-logs");
  await mkdir(logsRoot, { recursive: true });
  const runDir = await mkdtemp(path.join(logsRoot, "propai-sync-hosted-smoke-"));
  const stateDir = path.join(runDir, "state");
  await mkdir(stateDir, { recursive: true });

  const stdoutPath = path.join(runDir, "gateway.stdout.log");
  const stderrPath = path.join(runDir, "gateway.stderr.log");
  const stdoutStream = createWriteStream(stdoutPath, { flags: "a" });
  const stderrStream = createWriteStream(stderrPath, { flags: "a" });

  const cfgPath = path.join(stateDir, "propaiclaw.json");
  const env = {
    ...process.env,
    PROPAICLAW_MODE: "1",
    PROPAICLAW_HOME: stateDir,
    PROPAICLAW_STATE_DIR: stateDir,
    PROPAICLAW_CONFIG_PATH: cfgPath,
    PROPAI_HOSTED_ALLOW_INSECURE_BOOTSTRAP: "1",
  };

  const gateway = spawn(
    process.execPath,
    [
      "dist/index.js",
      "gateway",
      "--allow-unconfigured",
      "--bind",
      "loopback",
      "--port",
      String(port),
      "--token",
      "smoke-token",
    ],
    { cwd: repoRoot, env, stdio: ["ignore", "pipe", "pipe"] },
  );

  gateway.stdout.pipe(stdoutStream);
  gateway.stderr.pipe(stderrStream);

  const baseUrl = `http://127.0.0.1:${port}`;

  try {
    const health = await waitForHealth(baseUrl);
    const bootstrap = await fetchJsonOrThrow(
      `${baseUrl}/api/auth/bootstrap`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ userId: "smoke-tenant", label: "smoke" }),
      },
      201,
    );

    const apiKey = typeof bootstrap.apiKey === "string" ? bootstrap.apiKey : "";
    if (!apiKey) {
      throw new Error("bootstrap did not return apiKey");
    }

    const me = await fetchJsonOrThrow(
      `${baseUrl}/api/users/me`,
      {
        method: "GET",
        headers: { "x-api-key": apiKey },
      },
      200,
    );

    console.log(
      JSON.stringify(
        {
          health_ok: Boolean(health?.ok),
          bootstrap_user: bootstrap.userId ?? null,
          api_key_prefix: apiKey.slice(0, 9),
          me_user: me.userId ?? null,
          me_api_keys: Array.isArray(me.apiKeys) ? me.apiKeys.length : null,
          run_dir: path.relative(repoRoot, runDir),
        },
        null,
        2,
      ),
    );
  } finally {
    await stopProcess(gateway);
    stdoutStream.end();
    stderrStream.end();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
