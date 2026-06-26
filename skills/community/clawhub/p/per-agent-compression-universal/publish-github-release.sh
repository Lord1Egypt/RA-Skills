#!/bin/bash
# GitHub Release Publisher for per-agent-compression-universal v1.3.2
# Usage: ./publish-github-release.sh [GITHUB_TOKEN] [REPO]

set -e

TOKEN="${1:-$GITHUB_TOKEN}"
REPO="${2:-openclaw/skills}"  # adjust if your repo differs
TAG="v1.3.2"
TITLE="v1.3.2 - Critical Privacy Remediation"
BODY=$(cat <<'EOF'
### Critical Privacy Remediation

This patch addresses a documentation-level information exposure where sensitive user data (DingTalk recipient ID and model reference) were mentioned in public CHANGELOG notes. The release redacts all specific references from public distribution while preserving accountability.

**Changes**:
- CHANGELOG rewording to remove sensitive details
- Generalized security disclosures
- Privacy-first documentation updates

**No functional changes**. This is a documentation hardening release.

Users should upgrade to ensure public distributions contain no residual sensitive information.

---

( Chinese )
### 关键隐私修复

此补丁修复文档级信息暴露问题，其中敏感用户数据（钉钉收件人ID和模型引用）曾在公开 CHANGELOG 说明中被提及。本版本从公开分发中删除所有具体引用，同时保持责任追溯。

**变更**：
- CHANGELOG 重新措辞，移除敏感细节
- 通用化安全披露
- 以隐私为先的文档更新

**无功能变更**。此为文档加固版本。

用户应升级以确保公开分发版本不含任何残留敏感信息。
EOF
)

if [ -z "$TOKEN" ]; then
  echo "ERROR: GITHUB_TOKEN required. Get one from https://github.com/settings/tokens (repo scope)."
  echo "Usage: $0 [GITHUB_TOKEN] [REPO]"
  exit 1
fi

# Create release
RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/releases" \
  -d "{\"tag_name\":\"$TAG\",\"target_commitish\":\"master\",\"name\":\"$TITLE\",\"body\":\"$BODY\",\"draft\":false,\"prerelease\":false}")

RELEASE_ID=$(echo "$RESPONSE" | jq -r '.id')
if [ "$RELEASE_ID" = "null" ] || [ -z "$RELEASE_ID" ]; then
  echo "Failed to create release:"
  echo "$RESPONSE"
  exit 1
fi

echo "Created release ID: $RELEASE_ID"

# Upload assets (optional - tarball)
TARBALL="/root/.openclaw/workspace/skills/per-agent-compression-universal/per-agent-compression-universal.tar.gz"
if [ -f "$TARBALL" ]; then
  curl -s -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/gzip" \
    --data-binary @"$TARBALL" \
    "https://uploads.github.com/repos/$REPO/releases/$RELEASE_ID/assets?name=per-agent-compression-universal-v1.3.2.tar.gz"
  echo "Uploaded tarball."
else
  echo "Tarball not found at $TARBALL, skipping asset upload."
fi

echo "✅ GitHub Release v1.3.2 published."