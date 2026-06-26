#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <project-name> '<requirements summary or brief>' [output-file]" >&2
  exit 1
fi

project="$1"
brief="$2"
out="${3:-architecture.md}"

prompt="Create a practical architecture document in markdown for this SaaS project.
Project name: ${project}
Brief: ${brief}

Sections required:
# Architecture
## System Overview
## Stack Choices
## Frontend
## Backend
## Data Model
## Authentication
## External Integrations
## Deployment Shape
## Scaling Notes
## Open Questions

Include a Mermaid diagram under System Overview.
Return markdown only."

gemini -p "$prompt" > "$out"
echo "Wrote $out"
