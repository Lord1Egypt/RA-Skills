#!/usr/bin/env bash
# Ubuntu/Linux launcher: start llama-server in the skill root using a relative model path.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL="${MODEL:-models/Hy-MT2-7B-Q4_K_M.gguf}"
PORT="${PORT:-8001}"
API_KEY="${API_KEY:-llama2025}"
exec llama-server -m "${SKILL_DIR}/${MODEL}" -ngl -1 --host 127.0.0.1 --port "${PORT}" --api-key "${API_KEY}" -c 32768