#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:3001}"

echo "1) challenge"
curl -sS -X POST "${BASE_URL}/api/v1/auth/permit/challenge" -H "Content-Type: application/json"

echo "2) solve and register"
echo "Use scripts/solve_pow.py and scripts/strict_register.py for deterministic flow."
