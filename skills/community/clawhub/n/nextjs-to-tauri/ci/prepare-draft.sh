#!/usr/bin/env bash
set -euo pipefail
[[ "$TAG" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]] || { echo "::error::Expected vX.Y.Z or vX.Y.Z-prerelease tag"; exit 1; }
matches=$(gh api --paginate --slurp "repos/$REPO/releases?per_page=100" |
  jq -c --arg tag "$TAG" '[.[][] | select(.tag_name == $tag)]')
if [[ "$matches" == '[]' ]]; then
  pre=(); [[ "$TAG" == *-* ]] && pre=(--prerelease)
  gh release create "$TAG" -R "$REPO" --draft --verify-tag --title "$TAG" --generate-notes --notes "See CHANGELOG.md for details." "${pre[@]}"
else
  jq -e 'length == 1 and .[0].draft' <<< "$matches" >/dev/null
fi
id=$(gh release view "$TAG" -R "$REPO" --json databaseId --jq .databaseId)
echo "id=$id" >> "$GITHUB_OUTPUT"
echo "commit=$(git rev-parse HEAD)" >> "$GITHUB_OUTPUT"
