#!/usr/bin/env bash
# 发布 <namespace>/myapp-creator 到 ClawHub（slug = ClawHub 账号/组织 + skill 名）
#
# 前置：安装官方 ClawHub CLI 并完成登录（与 openclaw 自带的 skills 子命令不同）
#   npm i -g clawhub && clawhub login
# 用法：./publish.sh [--dry-run]
#
# 说明：新版 openclaw 的 `skills` 子命令不接受 `publish <path>`，会出现
#   "too many arguments for 'skills'"，请一律用本脚本调用的 `clawhub skill publish`。

set -euo pipefail

cd "$(dirname "$0")"

VERSION=$(cat version.txt | tr -d '[:space:]')

# 校验 clawhub.yaml 中的 version 与 version.txt 一致
if command -v yq >/dev/null 2>&1; then
  YAML_VERSION=$(yq -r '.version' clawhub.yaml)
  if [ "$VERSION" != "$YAML_VERSION" ]; then
    echo "error: version mismatch: version.txt=$VERSION clawhub.yaml=$YAML_VERSION" >&2
    exit 2
  fi
else
  echo "warn: yq not installed, skipping clawhub.yaml version check" >&2
fi

echo "preparing to publish skill@${VERSION} (see clawhub.yaml / ClawHub slug)"

# 给 scripts 加可执行位（ClawHub 不保证保留 +x，但便于本地测试）
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x publish.sh 2>/dev/null || true

if [ "${1:-}" = "--dry-run" ]; then
  echo "dry-run: 将发布以下文件："
  ls -la SKILL.md openai.yaml clawhub.yaml metadata.json LICENSE README.md version.txt
  ls -la scripts/
  exit 0
fi

# ClawHub 官方 CLI：https://docs.openclaw.ai/clawhub/cli
# 技能发布：`clawhub skill publish <path> --version <semver>`（也可用 legacy `clawhub publish`）
if command -v clawhub >/dev/null 2>&1; then
  echo "publishing via clawhub skill publish"
  clawhub skill publish . --version "$VERSION"
elif command -v npx >/dev/null 2>&1; then
  echo "publishing via npx clawhub@latest skill publish"
  npx --yes clawhub@latest skill publish . --version "$VERSION"
else
  echo "error: clawhub CLI not found. Install with: npm i -g clawhub" >&2
  echo "then: clawhub login && ./publish.sh" >&2
  echo "hint: 'openclaw skills publish' is no longer supported; use clawhub." >&2
  exit 127
fi

cat <<EOF

[OK] published skill@${VERSION} — 用户机器上安装请用裸 slug：clawhub install myapp-creator --version ${VERSION}

下一步：
  1) 同步更新 fe-service 配置中 MYAPP_SKILL_REQUIRED_VERSION 为 ${VERSION}
     conf/x-config/config.development.json
     conf/x-config/config.production.json
  2) 部署 fe-service
  3) 已有用户首次进 "我的应用" 页时，会被检测为 needs_update，install_prompt 会执行（示例）：
       clawhub install myapp-creator --version ${VERSION}
EOF
