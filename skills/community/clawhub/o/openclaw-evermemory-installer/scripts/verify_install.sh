#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Gateway health"
openclaw gateway status

echo "[INFO] Plugin detail"
openclaw plugins info evermemory

echo "[INFO] Memory slot binding"
openclaw config get plugins.slots.memory || true

echo "[INFO] Skills readiness"
openclaw skills check || true

echo "[PASS] Verification completed."
