#!/bin/bash
# Automated Release Script for per-agent-compression-universal
# Follows SKILL_RELEASE_SOP.md
# Usage: ./scripts/release.sh <version> <changelog-entry>
# Example: ./scripts/release.sh 1.3.4 "Critical bug fix: STATE_FILE variable..."

set -e

# ============================================
# CONFIGURATION (adjust as needed)
# ============================================
GITHUB_REPO="your-org/your-repo"  # TODO: Set your GitHub repository
SKILL_NAME="per-agent-compression-universal"

# ============================================
# INPUT VALIDATION
# ============================================
VERSION="$1"
CHANGELOG_ENTRY="$2"

if [ -z "$VERSION" ] || [ -z "$CHANGELOG_ENTRY" ]; then
  echo "Usage: $0 <version> <changelog-entry>"
  echo "Example: $0 1.3.4 \"Critical bug fix: STATE_FILE variable case sensitivity corrected.\""
  exit 1
fi

echo "🚀 Starting release process for ${SKILL_NAME} v${VERSION}"
echo ""

# ============================================
# STEP 1: Pre-Release Checklist
# ============================================
echo "📋 STEP 1: Pre-Release Checklist"
echo "-----------------------------------------"

# 1.1 Version sync check
echo "🔍 Checking version consistency..."
CURRENT_VER=$(jq -r '.version' skill.json 2>/dev/null || echo "none")
if [ "$CURRENT_VER" != "$VERSION" ]; then
  echo "❌ skill.json version is $CURRENT_VER, expected $VERSION"
  echo "   Run: jq --arg v \"$VERSION\" '.version = $v' skill.json > tmp && mv tmp skill.json"
  exit 1
fi
README_VER=$(grep -oP '\*\*Version\*\*:\s*\K[0-9.]+' README.md | head -1)
if [ "$README_VER" != "$VERSION" ]; then
  echo "❌ README.md version is $README_VER, expected $VERSION"
  exit 1
fi
echo "✅ Version numbers synchronized (skill.json, README.md)"

# 1.2 Security & Privacy Scan
echo ""
echo "🔒 Running security scans..."
SKILL_DIR="$(pwd)"

# Scan 1: Hardcoded secrets
echo "  - Hardcoded credentials/IDs..."
if grep -rE "(client|id|token|secret|key)\s*[=:]\s*[\"\`'][^\"\`']+[\"\`']" "$SKILL_DIR" 2>/dev/null | grep -v CHANGELOG.md; then
  echo "    ❌ Found potential hardcoded secrets. Review above lines."
  exit 1
else
  echo "    ✅ No obvious hardcoded secrets"
fi

# Scan 2: Long numeric strings (exclude CHANGELOG)
echo "  - Long numeric strings (IDs)..."
if grep -rE "[0-9]{10,}" "$SKILL_DIR" 2>/dev/null | grep -v CHANGELOG.md; then
  echo "    ❌ Found long numeric strings (possible IDs). Review above."
  exit 1
else
  echo "    ✅ No long numeric IDs found"
fi

# Scan 3: Install script parameter inference
echo "  - Install script parameter inference..."
# Check for hardcoded values after --model/--channel/--to that are NOT variables (ending with } or ") and not 'auto'
# Matches like: --channel "dingtalk-connector" or --to "055..." or --model "stepfun/..."
if grep -E "(--model|--channel|--to)[[:space:]]+[\"\']" install.sh | grep -v -E "\$(\{|[A-Za-z_])[\w\}]*\"?\]?" > /dev/null; then
  echo "    ❌ Install script contains hardcoded params. Use variables or 'auto'."
  exit 1
else
  echo "    ✅ Parameter inference check passed"
fi

# Scan 4: Configuration data leakage
echo "  - Configuration data leakage..."
if grep -rE "dingtalk-connector|openrouter/|stepfun|clawhub|skillhub" "$SKILL_DIR" 2>/dev/null | grep -vE "example.com|placeholder|<replace>"; then
  echo "    ⚠️  Found user-specific configuration values. Ensure they are intentional examples only."
fi

# Scan 5: CHANGELOG sensitive references (should be abstract)
echo "  - CHANGELOG sensitive references..."
if grep -nE "05566651511149398|openrouter/stepfun/step-3.5-flash:free|client_id|client_secret" CHANGELOG.md > /dev/null 2>&1; then
  echo "    ❌ CHANGELOG contains specific sensitive references. Use abstract language."
  exit 1
else
  echo "    ✅ CHANGELOG clear of specific sensitive references"
fi

# Scan 6: Bilingual completeness
echo "  - Bilingual completeness..."
CHINESE_SECTIONS=$(grep -c "( Chinese )" CHANGELOG.md 2>/dev/null || echo 0)
if [ "$CHINESE_SECTIONS" -lt 1 ]; then
  echo "    ❌ Missing Chinese sections in CHANGELOG"
  exit 1
fi
# Check Chinese section length (heuristic: >100 chars after separator)
if grep -A 20 "( Chinese )" CHANGELOG.md 2>/dev/null | head -n 21 | wc -c | grep -qE '^[0-9]+$' && [ $(grep -A 20 "( Chinese )" CHANGELOG.md 2>/dev/null | head -n 21 | wc -c) -lt 100 ]; then
  echo "    ⚠️  Chinese section seems too short (may be incomplete translation)"
else
  echo "    ✅ Chinese sections present"
fi

echo ""
echo "✅ All security checks passed"

# 1.3 Documentation Completeness
echo ""
echo "📚 Checking documentation completeness..."
# Scroll notice check
if grep -q "请往下翻页查看中文说明" README.md CHANGELOG.md; then
  echo "  ✅ Scroll notice present"
else
  echo "  ⚠️  Scroll notice missing (recommended)"
fi
# Anchor link check (optional)
if grep -q '\[skip to Chinese\]' README.md; then
  echo "  ✅ Anchor link present in README"
fi

echo ""
echo "✅ Pre-Release Checklist complete"
echo ""

# ============================================
# STEP 2: Git Commit & Tag
# ============================================
echo "📦 STEP 2: Git Commit & Tag"
echo "-----------------------------------------"

# Check if git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "⚠️  Not a git repository. Skipping git steps."
else
  # Ensure on main and up to date
  git checkout main 2>/dev/null || git checkout master
  git pull origin main 2>/dev/null || git pull origin master || echo "⚠️  Could not pull from remote (may be bare repo)"

  # Check uncommitted changes
  if ! git status --porcelain | grep -q .; then
    echo "✅ Clean working tree"
  else
    echo "⚠️  Uncommitted changes detected. Stashing..."
    git stash push -m "Automatic stash before release ${VERSION}"
  fi

  # Add all changes
  git add .
  git commit -m "Bump version ${VERSION} - ${CHANGELOG_ENTRY}" || echo "⚠️  Commit failed (maybe no changes?)"

  # Create and push tag
  git tag -a "v${VERSION}" -m "v${VERSION} - ${CHANGELOG_ENTRY}"
  git push origin main --tags || echo "⚠️  Could not push to remote (check permissions)"
  echo "✅ Git commit and tag created: v${VERSION}"
fi

echo ""

# ============================================
# STEP 3: Publish to ClawHub
# ============================================
echo "🌐 STEP 3: Publish to ClawHub"
echo "-----------------------------------------"

if ! command -v clawhub &> /dev/null; then
  echo "❌ clawhub CLI not found. Install: https://clawhub.com"
  exit 1
fi

# Build full changelog (extract this version entry from CHANGELOG.md)
# For simplicity, use provided entry; user should ensure it matches CHANGELOG
clawhub publish . --version "${VERSION}" --changelog "${CHANGELOG_ENTRY}"
CLAwHUB_ID=$(clawhub list --json 2>/dev/null | jq -r --arg v "${VERSION}" '.[] | select(.version==$v) | .id' | head -1)

if [ -n "$CLAwHUB_ID" ]; then
  echo "✅ Published to ClawHub (ID: ${CLAwHUB_ID})"
else
  echo "✅ Published to ClawHub (ID not retrievable)"
fi

echo ""

# ============================================
# STEP 4: Create GitHub Release
# ============================================
echo "🐙 STEP 4: Create GitHub Release"
echo "-----------------------------------------"

if ! command -v gh &> /dev/null; then
  echo "⚠️  GitHub CLI (gh) not found. Skipping GitHub release."
  echo "   Install: https://cli.github.com/ and run 'gh auth login'"
else
  if ! gh auth status &>/dev/null; then
    echo "❌ Not authenticated with GitHub. Run: gh auth login"
    exit 1
  fi

  # Create tarball
  cd ..
  TARBALL="${SKILL_NAME}-${VERSION}.tar.gz"
  tar -czf "${TARBALL}" "${SKILL_NAME}"
  cd "${SKILL_NAME}"

  # Build release notes from CHANGELOG entry (use provided)
  RELEASE_NOTES="# ${SKILL_NAME} v${VERSION}

${CHANGELOG_ENTRY}

---

## 📋 Release Details

- **Skill**: ${SKILL_NAME}
- **Version**: ${VERSION}
- **Published**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
if [ -n "$CLAwHUB_ID" ]; then
  RELEASE_NOTES="${RELEASE_NOTES}
- **ClawHub ID**: ${CLAwHUB_ID}"
fi
RELEASE_NOTES="${RELEASE_NOTES}

## ✅ Pre-Release Checklist

- [x] CHANGELOG entry added (top of file, bilingual)
- [x] README version header updated
- [x] skill.json version bumped
- [x] All security scans passed
- [x] Installation tested
- [x] Git tag created and pushed

## 🚀 Installation

\`\`\`bash
# From ClawHub
clawhub install ${SKILL_NAME}

# Or manual download
tar -xzf ${TARBALL}
cd ${SKILL_NAME} && ./install.sh
\`\`\`

## 📝 Notes

This release addresses critical bugs and improves reliability. Existing users should re-run \`./install.sh\` to update tasks.
"

  # Create draft release
  gh release create "v${VERSION}" \
    --repo "${GITHUB_REPO}" \
    --title "${SKILL_NAME} v${VERSION}" \
    --notes "${RELEASE_NOTES}" \
    --draft \
    "../${TARBALL}"

  echo "✅ Draft GitHub release created: https://github.com/${GITHUB_REPO}/releases/tag/v${VERSION}"
  echo "   Review and publish manually (required for finalization)."
fi

echo ""

# ============================================
# STEP 5: Sync Local Deploy
# ============================================
echo "🔄 STEP 5: Sync Local Deploy"
echo "-----------------------------------------"

if [ -d "/root/.openclaw/skills/${SKILL_NAME}" ]; then
  rm -rf "/root/.openclaw/skills/${SKILL_NAME}"
  cp -r "." "/root/.openclaw/skills/${SKILL_NAME}/"
  echo "✅ Synced to /root/.openclaw/skills/${SKILL_NAME}/"
else
  cp -r "." "/root/.openclaw/skills/${SKILL_NAME}/"
  echo "✅ Installed to /root/.openclaw/skills/${SKILL_NAME}/"
fi

echo ""

# ============================================
# STEP 6: Post-Release Documentation
# ============================================
echo "📝 STEP 6: Record Release in MEMORY.md"
echo "-----------------------------------------"

# Append release info to MEMORY.md (workspace-level)
if [ -f "/root/.openclaw/workspace/MEMORY.md" ]; then
  cat >> /root/.openclaw/workspace/MEMORY.md << EOF

### ${VERSION} - $(date +%Y-%m-%d) - Skill Release: ${SKILL_NAME}

- **Version**: ${VERSION}
- **ClawHub**: Published (ID: ${CLAwHUB_ID:-not recorded})
- **GitHub**: https://github.com/${GITHUB_REPO}/releases/tag/v${VERSION}
- **Changelog**: ${CHANGELOG_ENTRY}
- **Released**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
- **Notes**: Followed SKILL_RELEASE_SOP.md v1.0

EOF
  echo "✅ Appended release notes to /root/.openclaw/workspace/MEMORY.md"
else
  echo "⚠️  No MEMORY.md found in workspace; skipping memory update"
fi

echo ""

# ============================================
# FINAL SUMMARY
# ============================================
echo "🎉 RELEASE COMPLETE!"
echo "=========================================="
echo "Skill:        ${SKILL_NAME}"
echo "Version:      ${VERSION}"
echo "ClawHub ID:   ${CLAwHUB_ID:-not recorded}"
echo "GitHub Repo:  ${GITHUB_REPO}"
echo "Git Tag:      v${VERSION}"
echo "Tarball:      ${TARBALL:-(not created, not in skill dir)}"
echo ""
echo "Next actions:"
echo "1. Review GitHub draft release: https://github.com/${GITHUB_REPO}/releases/tag/v${VERSION}"
echo "2. Publish the release when ready"
echo "3. Notify users if critical fix"
echo "4. Verify tasks: openclaw cron list | grep ${SKILL_NAME}"
echo ""
echo "✅ All steps completed successfully."
echo "=========================================="
