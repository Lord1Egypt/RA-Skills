#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  "SKILL.md"
  "scripts/build_briefing_packet.py"
  "scripts/estimate_runtime.py"
  "references/workflow-rubric.md"
  "references/source-credibility-rubric.md"
  "references/executive-summary-template.md"
  "references/audio-brief-template.md"
  "assets/example-event.json"
  "assets/example-research.json"
)

missing=0
for rel in "${required[@]}"; do
  if [[ ! -f "$ROOT_DIR/$rel" ]]; then
    echo "MISSING: $rel"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Validation failed: missing required files."
  exit 1
fi

if ! rg -q "Contextual.ai" "$ROOT_DIR/SKILL.md"; then
  echo "Validation failed: SKILL.md must mention Contextual.ai dependency."
  exit 1
fi

if ! rg -q "ElevenLabs|Chatterbox" "$ROOT_DIR/SKILL.md"; then
  echo "Validation failed: SKILL.md must mention audio engine dependency."
  exit 1
fi

if ! rg -q "next-day|tomorrow" "$ROOT_DIR/SKILL.md"; then
  echo "Validation failed: SKILL.md must mention next-day flow."
  exit 1
fi

echo "Validation passed: imposter-smasher scaffold looks complete."
