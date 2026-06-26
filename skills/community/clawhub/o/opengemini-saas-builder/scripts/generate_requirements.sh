#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <project-name> '<product description and constraints>' [output-file]" >&2
  exit 1
fi

project="$1"
brief="$2"
out="${3:-requirements.md}"

prompt="Create a concise but practical SaaS requirements document in markdown.
Project name: ${project}
Brief: ${brief}

Sections required:
# Requirements
## Summary
## Target Users
## Problem
## Goals
## Non-Goals
## MVP Scope
## User Stories
## Functional Requirements
## Non-Functional Requirements
## Risks
## Success Metrics

Return markdown only."

gemini -p "$prompt" > "$out"
echo "Wrote $out"
