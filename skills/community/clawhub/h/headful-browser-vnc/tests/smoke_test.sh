#!/usr/bin/env bash
set -euo pipefail
echo "Running non-privileged smoke test for headful-browser-vnc"
# Dry-run start/stop
bash ../scripts/start_vnc.sh smoke_test :99 800x600 || true
sleep 1
bash ../scripts/start_chrome_debug.sh smoke_test --proxy=http://127.0.0.1:3128 9223 || true
sleep 2
echo "Attempting export (may fallback to wget)
"
bash ../scripts/export_page.sh smoke_test "https://ifconfig.co" 9223 || true
# cleanup
echo "Stopping"
bash ../scripts/stop_vnc.sh smoke_test :99 || true
echo "smoke test complete"
