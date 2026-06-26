#!/usr/bin/env bash
# 将用户提供的 api_key 写入当前技能工作区配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

new_api_key="$1"
if [[ -z "$new_api_key" ]] || [[ "$new_api_key" != hd_sk_* ]]; then
    echo "用法: $0 <hd_sk_开头的api_key>" >&2
    exit 1
fi

load_config || exit 1
env_name="${HUNDUN_ENV:-prod}"

mkdir -p "$(dirname "$CONFIG_FILE")"
{
    echo "# 混沌 Skill 配置"
    echo "api_key=$new_api_key"
    echo "base_url=$base_url"
    echo "env=$env_name"
} > "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE" 2>/dev/null || true

echo "已配置到当前工作区 ./.clawhub/.hdxy_config，后续可直接使用（env=$env_name）"
