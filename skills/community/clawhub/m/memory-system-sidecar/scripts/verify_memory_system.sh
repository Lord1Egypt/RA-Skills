#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

python3 -m unittest memory-system.tests.test_transcript_pipeline
python3 -m unittest memory-system.tests.test_retrieval_foundation
python3 -m unittest memory-system.tests.test_context_bridge
python3 -m unittest memory-system.tests.test_semantic_retrieval
python3 memory-system/eval/run_eval.py
