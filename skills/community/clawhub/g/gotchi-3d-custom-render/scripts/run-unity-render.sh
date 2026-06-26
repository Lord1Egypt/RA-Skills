#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_ROOT="${ROOT}/unity/GotchiCustomRenderer"
UNITY_BIN="${UNITY_BIN:-/Applications/Unity/Hub/Editor/2022.3.11f1/Unity.app/Contents/MacOS/Unity}"
INPUT_JSON="${1:-$ROOT/Requests/sample-request.json}"
TRACE_LOG="$ROOT/Renders/cli-trace.log"
PROJECT_TRACE_LOG="$PROJECT_ROOT/Renders/cli-trace.log"

if [ ! -f "$INPUT_JSON" ]; then
  echo "Input JSON not found: $INPUT_JSON" >&2
  exit 1
fi

if [ ! -x "$UNITY_BIN" ]; then
  echo "Unity binary not found or not executable: $UNITY_BIN" >&2
  echo "Set UNITY_BIN to a local Unity Editor binary before running this skill." >&2
  exit 1
fi

MANIFEST_JSON="$(jq -r '.output.manifest_json' "$INPUT_JSON")"

run_unity() {
  local pass="$1"
  echo "== Unity batch pass ${pass} =="
  local args=(
    -batchmode
    -quit
    -logFile -
    -projectPath "$PROJECT_ROOT"
    -executeMethod GotchiCustomRenderCLI.RenderFromJson
    --input "$INPUT_JSON"
  )
  if [ "$(uname -s)" != "Darwin" ]; then
    args=(-nographics "${args[@]}")
  fi
  "$UNITY_BIN" "${args[@]}"
}

mkdir -p "$ROOT/Renders"
mkdir -p "$PROJECT_ROOT/Renders"
rm -f "$MANIFEST_JSON" "$TRACE_LOG" "$PROJECT_TRACE_LOG"

run_unity 1 || true
if [ ! -f "$MANIFEST_JSON" ] || { [ -f "$PROJECT_TRACE_LOG" ] && grep -Eq 'wearableLocations=0|sdk_component_missing|holder_missing' "$PROJECT_TRACE_LOG"; }; then
  echo "== Running pass 2 after compile/import refresh =="
  run_unity 2
fi

if [ -f "$PROJECT_TRACE_LOG" ]; then
  cp "$PROJECT_TRACE_LOG" "$TRACE_LOG"
fi
