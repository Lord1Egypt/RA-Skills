#!/usr/bin/env bash
set -euo pipefail
printf '### Draft release v%s\n\n[Open the draft release](%s)\n\nThis release is a **draft**. The updater resolves `releases/latest`, which\nignores drafts — publish it or no client will ever be offered this version.\n' "$APP_VERSION" "$RELEASE_URL" >> "$GITHUB_STEP_SUMMARY"
