#!/bin/bash
set -eo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

echo "## Session Context"
echo ""
echo "### Date"
echo "$(date +%Y-%m-%d) ($(date +%A))"
echo ""

echo "### Recent Changes (last 48h)"
git log --oneline --since="48 hours ago" --no-merges 2>/dev/null | head -15 || echo "(no git history)"
echo ""

echo "### Active Packages"
ls -d packages/*/ 2>/dev/null | sed 's|packages/||;s|/$||' | head -15 || echo "(none)"
echo ""

echo "### Active Apps"
ls -d apps/*/ 2>/dev/null | sed 's|apps/||;s|/$||' | head -10 || echo "(none)"
echo ""

echo "### Brain Notes"
ls brain/*.md 2>/dev/null | sed 's|brain/||' || echo "(brain/ not found)"
echo ""

echo "### Open Tasks (memory index)"
head -20 memory/MEMORY.md 2>/dev/null || echo "(no memory index)"
echo ""

# Resume Card: inyectar estado pre-compaction si existe
if [ -f .claude/session-resume-card.md ]; then
  echo "### Resume Card (estado pre-compaction)"
  cat .claude/session-resume-card.md
  echo ""
fi

exit 0
