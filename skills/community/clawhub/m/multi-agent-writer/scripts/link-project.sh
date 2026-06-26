#!/usr/bin/env bash
# link-project.sh — 开发模式：符号链接本地 multi-agent 项目（无需 clone）
#
# 用法：
#   bash scripts/link-project.sh /path/to/local/multi-agent
#
# 适用场景：本地同时开发 multi-agent 项目和 skills 项目时，
# 使 skill 直接指向本地项目，修改立即生效，无需重新 clone。

set -euo pipefail

INSTALL_DIR="${HOME}/.skills/multi-agent"

if [[ $# -lt 1 ]]; then
    echo "用法: bash scripts/link-project.sh <本地 multi-agent 项目路径>" >&2
    exit 1
fi

SOURCE_DIR="$(cd "$1" && pwd)"

if [[ ! -f "${SOURCE_DIR}/main.py" ]]; then
    echo "错误: '${SOURCE_DIR}' 不像是有效的 multi-agent 项目（缺少 main.py）" >&2
    exit 1
fi

# 如已存在则先删除
[[ -e "${INSTALL_DIR}" ]] && rm -rf "${INSTALL_DIR}"

mkdir -p "$(dirname "${INSTALL_DIR}")"
ln -s "${SOURCE_DIR}" "${INSTALL_DIR}"

echo "✓ 已创建符号链接: ${INSTALL_DIR} → ${SOURCE_DIR}"
echo "  现在运行 bash install.sh 以注册 skill 到各 agent"
