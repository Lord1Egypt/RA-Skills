#!/usr/bin/env bash
# run_tests.sh — run the memory-health-check test suite
set -euo pipefail
cd "$(dirname "$0")/.."
pytest tests/ -v --tb=short
