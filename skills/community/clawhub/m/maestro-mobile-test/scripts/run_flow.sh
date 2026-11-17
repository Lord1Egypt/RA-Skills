#!/usr/bin/env bash
# Maestro test runner
# Boots an emulator (if needed), sets up adb reverse for backend access,
# and runs a Maestro flow or suite.
#
# Usage:
#   bash skills/maestro-mobile-test/scripts/run_flow.sh <avd-name> <flow.yaml> [backend_port]
#
# Examples:
#   bash skills/maestro-mobile-test/scripts/run_flow.sh my-avd .maestro/navigation/tab-nav.yaml
#   bash skills/maestro-mobile-test/scripts/run_flow.sh my-avd .maestro/suites/regression.yaml 8888
#   bash skills/maestro-mobile-test/scripts/run_flow.sh my-avd .maestro/suites/smoke.yaml ""  # no backend

set -euo pipefail

AVD_NAME="${1:?Usage: run_flow.sh <avd-name> <flow.yaml> [backend_port]}"
FLOW_FILE="${2:?Usage: run_flow.sh <avd-name> <flow.yaml> [backend_port]}"
BACKEND_PORT="${3:-}"  # optional: port to adb reverse (e.g. 8888 for netlify dev)

# --- Load environment ---
if [ -f "$HOME/.maestro/activate.sh" ]; then
    # shellcheck disable=SC1091
    source "$HOME/.maestro/activate.sh"
else
    echo "❌ Maestro environment not set up. Run setup.sh first."
    exit 1
fi

echo "=== Maestro test run ==="
echo "AVD:      $AVD_NAME"
echo "Flow:     $FLOW_FILE"
echo "Backend:  ${BACKEND_PORT:-none}"
echo ""

# --- Check flow file exists (resolve to absolute path BEFORE any cd) ---
if [ ! -f "$FLOW_FILE" ]; then
    echo "❌ Flow file not found: $FLOW_FILE"
    exit 1
fi
FLOW_ABS="$(cd "$(dirname "$FLOW_FILE")" && pwd)/$(basename "$FLOW_FILE")"

# --- Boot emulator if not running ---
echo "--- Checking emulator ---"
RUNNING=$(adb devices 2>/dev/null | grep -c "emulator.*device$" || true)

# Detect emulator binary name (Windows uses .exe)
EMU_BIN="emulator"
if [ -f "$ANDROID_HOME/emulator/emulator.exe" ]; then
    EMU_BIN="emulator.exe"
fi

if [ "$RUNNING" -eq 0 ]; then
    echo "Booting emulator '$AVD_NAME' (headed)..."
    "$ANDROID_HOME/emulator/$EMU_BIN" -avd "$AVD_NAME" -no-snapshot-load &

    echo "Waiting for boot..."
    adb wait-for-device 2>/dev/null
    # Wait for full boot
    BOOT_OK=0
    for i in $(seq 1 60); do
        BOOTED=$(adb shell getprop sys.boot_completed 2>/dev/null | tr -d '\r')
        if [ "$BOOTED" = "1" ]; then
            echo "✅ Boot complete"
            BOOT_OK=1
            break
        fi
        sleep 2
    done
    if [ "$BOOT_OK" -eq 0 ]; then
        echo "❌ Emulator failed to boot within 120s. Aborting."
        exit 1
    fi
else
    echo "✅ Emulator already running"
fi

# --- Set up adb reverse for backend ---
if [ -n "$BACKEND_PORT" ]; then
    echo ""
    echo "--- Setting up adb reverse (port $BACKEND_PORT) ---"
    adb reverse "tcp:$BACKEND_PORT" "tcp:$BACKEND_PORT"
    echo "✅ Emulator localhost:$BACKEND_PORT → host localhost:$BACKEND_PORT"
fi

# --- Run the flow (don't let set -e swallow the exit code) ---
echo ""
echo "--- Running flow ---"
EXIT_CODE=0
maestro test "$FLOW_ABS" || EXIT_CODE=$?

echo ""
if [ "$EXIT_CODE" -eq 0 ]; then
    echo "✅ Flow passed: $FLOW_FILE"
else
    echo "❌ Flow failed: $FLOW_FILE"
    echo "   Debug artifacts: ~/.maestro/tests/"
fi

exit $EXIT_CODE
