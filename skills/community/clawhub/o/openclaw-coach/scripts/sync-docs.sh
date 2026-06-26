#!/bin/bash
# OpenClaw 文档同步脚本 - 从 GitHub 获取
# 每天凌晨 3:21 执行

OBSIDIAN_PATH="$HOME/Obsidian/Docs/OpenClaw"
GITHUB_RAW="https://raw.githubusercontent.com/openclaw/openclaw/main/docs"

echo "🔄 开始同步 OpenClaw 官方文档..."

mkdir -p "$OBSIDIAN_PATH/docs"

# 文档文件列表（从 GitHub docs 目录）
DOCS=(
    "cli/acp.md"
    "cli/agent.md"
    "cli/agents.md"
    "cli/approvals.md"
    "cli/browser.md"
    "cli/channels.md"
    "cli/config.md"
    "cli/configure.md"
    "cli/cron.md"
    "cli/daemon.md"
    "cli/dashboard.md"
    "cli/devices.md"
    "cli/gateway.md"
    "cli/health.md"
    "cli/hooks.md"
    "cli/logs.md"
    "cli/memory.md"
    "cli/message.md"
    "cli/models.md"
    "cli/node.md"
    "cli/nodes.md"
    "cli/plugins.md"
    "cli/secrets.md"
    "cli/security.md"
    "cli/sessions.md"
    "cli/setup.md"
    "cli/skills.md"
    "cli/status.md"
    "cli/system.md"
    "cli/tui.md"
    "cli/update.md"
)

SYNCED=0
for doc in "${DOCS[@]}"; do
    filename=$(basename "$doc" .md)
    echo "📄 下载: $filename"
    
    content=$(curl -s "${GITHUB_RAW}/${doc}" 2>/dev/null)
    
    if [[ -n "$content" && "$content" != *"404"* ]]; then
        echo "# $filename

> 来源: https://github.com/openclaw/openclaw/blob/main/docs/$doc

$content" > "$OBSIDIAN_PATH/docs/${filename}.md"
        ((SYNCED++))
    else
        echo "  ⚠️ 未找到: $doc"
    fi
done

# 获取版本信息
VERSION=$(curl -s "https://api.github.com/repos/openclaw/openclaw/releases/latest" 2>/dev/null | grep -oE '"tag_name": "[^"]+"' | cut -d'"' -f4)
if [[ -n "$VERSION" ]]; then
    echo "$VERSION" > "$OBSIDIAN_PATH/latest-version.txt"
fi

echo "✅ 同步完成！已同步 $SYNCED 个文档，版本: $VERSION"
