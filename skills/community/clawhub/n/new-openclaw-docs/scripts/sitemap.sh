#!/bin/bash
# Sitemap generator - shows all docs by category

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

echo "📚 OpenClaw Documentation Sitemap"
echo "================================="
echo ""

# Categories structure based on docs.clawd.bot
CATEGORIES=(
  "start:Getting Started"
  "gateway:Gateway & Operations"
  "providers:Providers"
  "concepts:Core Concepts"
  "tools:Tools"
  "automation:Automation"
  "cli:CLI"
  "platforms:Platforms"
  "nodes:Nodes"
  "web:Web"
  "install:Install"
  "reference:Reference"
)

for entry in "${CATEGORIES[@]}"; do
  IFS=':' read -r cat label <<< "$entry"
  # Count cached docs in this category
  count=$(ls "$OPENCLAW_DOCS_CACHE_DIR"/${cat}_*.md 2>/dev/null | wc -l)
  if [[ $count -gt 0 ]]; then
    printf "  📁 %-20s %s  (%d docs cached)\n" "/$cat/" "$label" "$count"
  else
    printf "  📁 %-20s %s\n" "/$cat/" "$label"
  fi
done

echo ""
echo "Tip: Use 'fetch-doc.sh <path>' to download or cache a specific doc"
echo "     Use 'search.sh <keyword>' to search cached docs"
