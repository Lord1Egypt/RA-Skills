#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <project-name> '<stack and working rules context>' [output-file]" >&2
  exit 1
fi

project="$1"
brief="$2"
out="${3:-Rules.md}"

prompt="Create a strict project Rules.md in markdown for this project.
Project name: ${project}
Context: ${brief}

Sections required:
# Rules
## Engineering Rules
## Package Manager
## File and Folder Rules
## Environment Variable Rules
## Testing Rules
## Migration Rules
## Git and PR Rules
## Deployment Rules
## Safety Rules

Return markdown only."

gemini -p "$prompt" > "$out"
echo "Wrote $out"
