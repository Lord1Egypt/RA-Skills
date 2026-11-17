#!/usr/bin/env bash
set -euo pipefail
gh api --paginate --slurp "repos/$REPO/releases/$DRAFT_ID/assets?per_page=100" > "$RUNNER_TEMP/draft-assets.json"
gh release download "$TAG" -R "$REPO" -p latest.json -O "$RUNNER_TEMP/build-feed.json" --clobber
node .github/scripts/release-assets.mjs record
