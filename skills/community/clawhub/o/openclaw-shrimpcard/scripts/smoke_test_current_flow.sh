#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export SHRIMPCARD_ALLOW_FIXTURES=1

EVIDENCE_SAMPLE="$ROOT_DIR/examples/hermes-agent.public-evidence.json"
SUBMISSION_SAMPLE="$ROOT_DIR/examples/hermes-agent.public-submission.json"

python3 "$ROOT_DIR/scripts/build_memory_search_prompt.py" \
  "$EVIDENCE_SAMPLE" \
  --lang zh \
  --out "$TMP_DIR/memory-search-prompt.txt"

python3 "$ROOT_DIR/scripts/build_agent_workflow_prompt.py" \
  "$EVIDENCE_SAMPLE" \
  --lang en \
  --out "$TMP_DIR/agent-workflow-prompt.txt"

python3 "$ROOT_DIR/scripts/build_submission_prompt.py" \
  "$EVIDENCE_SAMPLE" \
  --lang zh \
  --out "$TMP_DIR/submission-prompt.txt"

python3 "$ROOT_DIR/scripts/validate_self_intro_submission.py" \
  "$SUBMISSION_SAMPLE"

python3 "$ROOT_DIR/scripts/submission_to_share_card.py" \
  "$SUBMISSION_SAMPLE" \
  --out "$TMP_DIR/share-card.json"

python3 "$ROOT_DIR/scripts/build_image_task_prompt.py" \
  "$SUBMISSION_SAMPLE" \
  --out "$TMP_DIR/image-task.txt"

if python3 "$ROOT_DIR/scripts/render_card_html.py" \
  "$TMP_DIR/share-card.json" \
  --out "$TMP_DIR/should-not-render.html" >/dev/null 2>&1; then
  echo "[FAIL] render_card_html.py should reject share cards without a final image"
  exit 1
fi

python3 "$ROOT_DIR/scripts/attach_generated_image.py" \
  "$TMP_DIR/share-card.json" \
  --image-file "$ROOT_DIR/assets/hermes-agent.png"

python3 "$ROOT_DIR/scripts/validate_final_bundle.py" \
  "$TMP_DIR/share-card.json"

python3 "$ROOT_DIR/scripts/render_card_html.py" \
  "$TMP_DIR/share-card.json" \
  --lang zh \
  --out "$TMP_DIR/selfie-card.zh.html"

python3 "$ROOT_DIR/scripts/render_card_html.py" \
  "$TMP_DIR/share-card.json" \
  --lang en \
  --out "$TMP_DIR/selfie-card.en.html"

python3 "$ROOT_DIR/scripts/validate_rendered_html.py" \
  "$TMP_DIR/selfie-card.zh.html"

python3 "$ROOT_DIR/scripts/validate_rendered_html.py" \
  "$TMP_DIR/selfie-card.en.html"

test -f "$TMP_DIR/memory-search-prompt.txt"
test -f "$TMP_DIR/agent-workflow-prompt.txt"
test -f "$TMP_DIR/submission-prompt.txt"
test -f "$TMP_DIR/share-card.json"
test -f "$TMP_DIR/image-task.txt"
test -f "$TMP_DIR/selfie-card.zh.html"
test -f "$TMP_DIR/selfie-card.en.html"
rg -q '<html lang="zh-CN">' "$TMP_DIR/selfie-card.zh.html"
rg -q '<html lang="en">' "$TMP_DIR/selfie-card.en.html"
rg -q "recognizable character" "$TMP_DIR/image-task.txt"
! rg -q 'id="photoId"' "$TMP_DIR/selfie-card.zh.html"
! rg -q 'id="photoId"' "$TMP_DIR/selfie-card.en.html"
! rg -q 'id="langZh"' "$TMP_DIR/selfie-card.zh.html"
! rg -q 'id="langEn"' "$TMP_DIR/selfie-card.zh.html"
! rg -q 'id="exportCardBtn"' "$TMP_DIR/selfie-card.zh.html"
! rg -q 'html2canvas.min.js' "$TMP_DIR/selfie-card.zh.html"

echo "[OK] Current flow smoke test passed"
