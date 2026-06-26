#!/usr/bin/env bash
# uninstall.sh — 卸载 multi-agent skill
#
# 用法：
#   bash uninstall.sh                  # 卸载所有 agent 中的 skill 注册
#   bash uninstall.sh --all            # 同上，并删除本地项目代码
#   bash uninstall.sh --agent codebuddy

set -euo pipefail

SKILL_NAME="multi-agent"
INSTALL_DIR="${HOME}/.skills/multi-agent"

# 兼容 bash 3.x（macOS 自带），不使用关联数组
AGENTS="codebuddy claude openclaw"
dir_codebuddy="${HOME}/.codebuddy/skills"
dir_claude="${HOME}/.claude/skills"
dir_openclaw="${HOME}/.openclaw/skills"

get_agent_dir() {
    case "$1" in
        codebuddy) echo "${dir_codebuddy}" ;;
        claude)    echo "${dir_claude}" ;;
        openclaw)  echo "${dir_openclaw}" ;;
    esac
}

TARGET_AGENT="all"
DELETE_PROJECT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent) TARGET_AGENT="${2:-all}"; shift 2 ;;
        --all)   DELETE_PROJECT=true; shift ;;
        *) shift ;;
    esac
done

removed=""
for agent in ${AGENTS}; do
    skill_dir="$(get_agent_dir "${agent}")/${SKILL_NAME}"
    case "${TARGET_AGENT}" in
        all|"${agent}")
            if [[ -d "${skill_dir}" ]]; then
                rm -rf "${skill_dir}"
                removed="${removed} ${agent}"
                echo "✓ 已从 ${agent} 移除: ${skill_dir}"
            fi
            ;;
    esac
done

if [[ "${DELETE_PROJECT}" == "true" && -d "${INSTALL_DIR}" ]]; then
    rm -rf "${INSTALL_DIR}"
    echo "✓ 已删除项目代码: ${INSTALL_DIR}"
fi

if [[ -z "${removed}" ]]; then
    echo "未找到已安装的 multi-agent skill"
else
    echo "✓ multi-agent skill 已卸载（${removed}）"
fi
