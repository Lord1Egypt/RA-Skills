#!/usr/bin/env bash
# Copy to .github/scripts/verify-draft.sh with the release workflow.
set -euo pipefail
gh release view "$TAG" -R "$REPO" --json isDraft --jq .isDraft | grep -qx true
gh release download "$TAG" -R "$REPO" --dir dist
gh api --paginate --slurp "repos/$REPO/releases/$DRAFT_ID/assets?per_page=100" > "$RUNNER_TEMP/draft-assets.json"
APP_VERSION="${TAG#v}" node .github/scripts/release-assets.mjs verify
current=$(gh api "repos/$REPO/commits/$TAG" --jq .sha)
[[ "$current" == "$SOURCE_COMMIT" ]] || { echo "::error::Tag moved after build"; exit 1; }
