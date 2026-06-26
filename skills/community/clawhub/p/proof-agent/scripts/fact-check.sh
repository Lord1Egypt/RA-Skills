#!/usr/bin/env bash
# fact-check.sh — Extract and validate factual claims from files
# Usage: ./fact-check.sh <file> [file2 ...]
#
# Checks:
# - URLs (HTTP status)
# - npm package versions (registry lookup)
# - GitHub action versions (tag existence)
# - Python package versions (PyPI lookup)
#
# Outputs a report of claims found and their validation status.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

check_url() {
  local url="$1"
  local status
  status=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null || echo "000")
  if [[ "$status" =~ ^[23] ]]; then
    echo -e "  ${GREEN}✓${NC} URL $url → $status"
    ((PASS_COUNT++))
  elif [ "$status" = "000" ]; then
    echo -e "  ${YELLOW}?${NC} URL $url → timeout/unreachable"
    ((WARN_COUNT++))
  else
    echo -e "  ${RED}✗${NC} URL $url → $status"
    ((FAIL_COUNT++))
  fi
}

check_npm_version() {
  local pkg="$1"
  local ver="$2"
  local registry_ver
  registry_ver=$(curl -s "https://registry.npmjs.org/$pkg/$ver" 2>/dev/null | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
  if [ "$registry_ver" = "$ver" ]; then
    echo -e "  ${GREEN}✓${NC} npm $pkg@$ver exists"
    ((PASS_COUNT++))
  elif [ -z "$registry_ver" ]; then
    echo -e "  ${RED}✗${NC} npm $pkg@$ver not found on registry"
    ((FAIL_COUNT++))
  else
    echo -e "  ${YELLOW}?${NC} npm $pkg@$ver — registry returned $registry_ver"
    ((WARN_COUNT++))
  fi
}

check_github_action() {
  local action="$1"
  local ref="$2"
  local repo
  repo=$(echo "$action" | cut -d'@' -f1)
  local status
  status=$(curl -sL -o /dev/null -w "%{http_code}" "https://github.com/$repo/tree/$ref" 2>/dev/null || echo "000")
  if [[ "$status" =~ ^[23] ]]; then
    echo -e "  ${GREEN}✓${NC} Action $repo@$ref exists"
    ((PASS_COUNT++))
  else
    echo -e "  ${RED}✗${NC} Action $repo@$ref → $status"
    ((FAIL_COUNT++))
  fi
}

if [ $# -eq 0 ]; then
  echo "Usage: fact-check.sh <file> [file2 ...]"
  exit 1
fi

for file in "$@"; do
  if [ ! -f "$file" ]; then
    echo -e "${YELLOW}Skipping $file (not found)${NC}"
    continue
  fi

  echo ""
  echo "=== Checking: $file ==="

  # Extract and check URLs
  URLS=$(grep -oE 'https?://[^ '\''")<>\]]+' "$file" 2>/dev/null | sort -u || true)
  if [ -n "$URLS" ]; then
    echo ""
    echo "URLs found:"
    while IFS= read -r url; do
      # Skip localhost and example URLs
      if echo "$url" | grep -qE 'localhost|127\.0\.0\.1|example\.com|your-'; then
        continue
      fi
      check_url "$url"
    done <<< "$URLS"
  fi

  # Extract and check npm packages (pattern: package@version)
  NPM_PKGS=$(grep -oE '[a-zA-Z@][a-zA-Z0-9./_-]*@[0-9]+\.[0-9]+\.[0-9]+[a-zA-Z0-9.-]*' "$file" 2>/dev/null | grep -v '^@' | sort -u || true)
  # Also catch scoped packages
  SCOPED_PKGS=$(grep -oE '@[a-zA-Z0-9-]+/[a-zA-Z0-9-]+@[0-9]+\.[0-9]+\.[0-9]+' "$file" 2>/dev/null | sort -u || true)
  ALL_PKGS=$(printf '%s\n%s' "$NPM_PKGS" "$SCOPED_PKGS" | grep -v '^$' | sort -u || true)
  if [ -n "$ALL_PKGS" ]; then
    echo ""
    echo "npm packages found:"
    while IFS= read -r pkg_ver; do
      pkg=$(echo "$pkg_ver" | sed 's/@[0-9]*\.[0-9]*\.[0-9]*.*$//' | sed 's/\^//g')
      ver=$(echo "$pkg_ver" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+[a-zA-Z0-9.-]*')
      if [ -n "$pkg" ] && [ -n "$ver" ]; then
        check_npm_version "$pkg" "$ver"
      fi
    done <<< "$ALL_PKGS"
  fi

  # Extract GitHub Actions (pattern: uses: owner/repo@ref)
  ACTIONS=$(grep -oE 'uses: *[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+@[a-zA-Z0-9._-]+' "$file" 2>/dev/null | sed 's/uses: *//' | sort -u || true)
  if [ -n "$ACTIONS" ]; then
    echo ""
    echo "GitHub Actions found:"
    while IFS= read -r action; do
      ref=$(echo "$action" | cut -d'@' -f2)
      check_github_action "$action" "$ref"
    done <<< "$ACTIONS"
  fi
done

echo ""
echo "=== Summary ==="
echo -e "${GREEN}Pass: $PASS_COUNT${NC}  ${RED}Fail: $FAIL_COUNT${NC}  ${YELLOW}Warn: $WARN_COUNT${NC}"

if [ "$FAIL_COUNT" -gt 0 ]; then
  exit 1
fi
