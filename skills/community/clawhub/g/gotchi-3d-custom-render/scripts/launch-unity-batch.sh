#!/bin/bash
set -euo pipefail
INPUT_JSON="${1:-}"
UNITY_PROJECT="/home/ubuntu/.openclaw/workspace/skills/gotchi-3d-custom-render/unity/GotchiCustomRenderer"
UNITY_METHOD="GotchiCustomRenderCLI.RenderFromJson"
UNITY_BIN="${UNITY_BIN:-}"

if [ -z "$INPUT_JSON" ]; then
  echo '{"ok":false,"error":"missing input json"}'
  exit 1
fi

if [ ! -d "$UNITY_PROJECT" ]; then
  echo '{"ok":false,"error":"unity project not installed","code":"unity_project_missing"}'
  exit 2
fi

if [ -z "$UNITY_BIN" ]; then
  echo '{"ok":false,"error":"UNITY_BIN is not set","code":"unity_bin_missing"}'
  exit 3
fi

xvfb-run -a "$UNITY_BIN"   -batchmode -nographics -quit   -projectPath "$UNITY_PROJECT"   -executeMethod "$UNITY_METHOD"   --input "$INPUT_JSON"
