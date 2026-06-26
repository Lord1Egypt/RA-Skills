#!/bin/bash
# PR-002: Integration test for config pollution
export SDLC_TEST_MODE=true
export PYTHONPATH="$(dirname "$0")"

# Remove any existing config to start clean for the test
rm -rf test_env
mkdir -p test_env/config
cd test_env

python3 -c "import os, sys; sys.path.insert(0, os.path.join(os.getcwd(), '..', 'scripts')); from orchestrator import load_or_merge_config; load_or_merge_config('.')"

if [ ! -f "config/sdlc_config.json" ]; then
    echo "[PASS] test_1094_config_pollution passed successfully"
else
    echo "FAIL"
    exit 1
fi
cd ..
rm -rf test_env
