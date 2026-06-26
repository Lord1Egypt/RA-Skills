#!/bin/bash
set -euo pipefail

# ==============================================================================
# LLM Stream Guard -- Deterministic Deployment Script
# ==============================================================================
# Deploys the two-layer defense into an Openclaw installation.
#
# Layer 1: Stream Entropy Breaker (Node.js) -- patches global.fetch
# Layer 2: Host Resource Watchdog (Python)  -- daemon process
#
# This script is idempotent: safe to run multiple times.
# ==============================================================================

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${OPENCLAW_APP_DIR:-/app}"
DIST_DIR="${TARGET_DIR}/dist/llm_stream_guard"
TARGET_FILE="${TARGET_DIR}/openclaw.mjs"
MARKER="__streamEntropyBreakerInstalled"

# ---- Step 1: Preflight checks ----

echo "[LLM Stream Guard] Preflight checks..."

if [[ ! -f "${TARGET_FILE}" ]]; then
  echo "ERROR: ${TARGET_FILE} not found. Set OPENCLAW_APP_DIR to your Openclaw root."
  exit 1
fi

if ! command -v python3 &>/dev/null; then
  echo "ERROR: python3 is required but not found in PATH."
  exit 1
fi

# ---- Step 2: Ensure psutil is installed ----

echo "[LLM Stream Guard] Checking Python dependencies..."

if ! python3 -c "import psutil" &>/dev/null; then
  echo "[LLM Stream Guard] Installing psutil..."
  if command -v apt-get &>/dev/null; then
    apt-get update -qq && apt-get install -y -qq python3-psutil
  else
    python3 -m pip install psutil
  fi
  if ! python3 -c "import psutil" &>/dev/null; then
    echo "ERROR: Failed to install psutil. Aborting."
    exit 1
  fi
  echo "[LLM Stream Guard] psutil installed."
else
  echo "[LLM Stream Guard] psutil OK."
fi

# ---- Step 3: Copy runtime files ----

echo "[LLM Stream Guard] Deploying files to ${DIST_DIR}/"
mkdir -p "${DIST_DIR}"
cp "${BASE_DIR}/src/stream-entropy-breaker.cjs" "${DIST_DIR}/"
cp "${BASE_DIR}/src/entropy-engine.cjs"         "${DIST_DIR}/"
cp "${BASE_DIR}/host-resource-watchdog.py"      "${DIST_DIR}/"
chmod +x "${DIST_DIR}/host-resource-watchdog.py"
echo "[LLM Stream Guard] Files deployed."

# ---- Step 4: Inject into openclaw.mjs (idempotent) ----

if grep -q "${MARKER}" "${TARGET_FILE}"; then
  echo "[LLM Stream Guard] Already injected into ${TARGET_FILE}. Skipping."
else
  BACKUP_FILE="${TARGET_FILE}.bak.$(date +%Y%m%d_%H%M%S)"
  cp "${TARGET_FILE}" "${BACKUP_FILE}"
  echo "[LLM Stream Guard] Backup created: ${BACKUP_FILE}"

  cat >> "${TARGET_FILE}" << 'INJECT'

// [LLM_STREAM_GUARD_START] -- Injected by deploy.sh. Do not edit manually.
// Layer 2: Pull up Host Resource Watchdog daemon
try {
  const { execSync } = module.createRequire(import.meta.url)("child_process");
  try {
    execSync('pgrep -f "[h]ost-resource-watchdog.py"');
  } catch (err) {
    const distDir = new URL("dist/llm_stream_guard/", import.meta.url).pathname;
    const logDir = (process.env.HOME || "/root") + "/.openclaw/workspace/memory/core";
    execSync(`mkdir -p "${logDir}"`);
    execSync(`nohup python3 "${distDir}host-resource-watchdog.py" > "${logDir}/host_watchdog.log" 2>&1 &`);
    console.log("[Host Resource Watchdog] Started.");
  }
} catch (e) {
  console.error("[Host Resource Watchdog] Failed to start:", e.message);
}

// Layer 1: Activate Stream Entropy Breaker (patches global.fetch)
try {
  const { createRequire } = await import("node:module");
  const require = createRequire(import.meta.url);
  const breaker = require("./dist/llm_stream_guard/stream-entropy-breaker.cjs");
  if (breaker && breaker.install) {
    breaker.install();
  }
} catch (e) {
  console.error("[Stream Entropy Breaker] Failed to activate:", e);
}
// [LLM_STREAM_GUARD_END]
INJECT

  echo "[LLM Stream Guard] Injected into ${TARGET_FILE}."
fi

echo "[LLM Stream Guard] Deployment complete. Restart the gateway to activate."
