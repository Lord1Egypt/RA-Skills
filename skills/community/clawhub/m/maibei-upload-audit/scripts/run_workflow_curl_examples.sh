#!/usr/bin/env bash
set -euo pipefail

# Fill these before running.
TOKEN="${TOKEN:-}"
USER_ID="${USER_ID:-}"

if [[ -z "$TOKEN" || -z "$USER_ID" ]]; then
  echo "Set TOKEN and USER_ID first." >&2
  exit 1
fi

# 1) Copy source sheet
curl 'https://play-be.omnimcp.ai/api/v1/workflow/run' \
  -H 'accept: text/event-stream' \
  -H "authorization: Bearer $TOKEN" \
  -H 'content-type: application/json' \
  -H 'origin: https://maibei.maybe.ai' \
  -H 'referer: https://maibei.maybe.ai/' \
  -H "user-id: $USER_ID" \
  --data-raw '{"artifact_id":"69ca226377efb8a1de743d34","interaction":true,"task":"","task_id":"copy-sheet-task-id","workflow_id":"69ca238877efb8a1de743e3b","variables":[{"name":"variable:scalar:source_excel_url","default_value":"https://www.maybe.ai/docs/spreadsheets/d/69c2400ea25ba20198828d73?gid=0"}],"metadata":{"case":"upload-audit-file","title":"上传文件并审核"}}'

# 2) Analyze uploaded files into copied sheet
# Replace SHEET_URL and uploaded file entries before running.
# curl 'https://play-be.omnimcp.ai/api/v1/workflow/run' ...

# 3) Audit sheet
# curl 'https://play-be.omnimcp.ai/api/v1/workflow/run' ...
