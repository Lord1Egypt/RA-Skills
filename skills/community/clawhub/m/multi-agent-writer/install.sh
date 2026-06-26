#!/usr/bin/env bash
# install.sh — 安装 multi-agent skill
#
# 用法：
#   bash install.sh                    # 自动检测已安装的 agent
#   bash install.sh --agent all        # 安装到所有 agent
#   bash install.sh --agent codebuddy
#   bash install.sh --agent claude
#   bash install.sh --agent openclaw
#
# 卸载：
#   bash uninstall.sh

set -euo pipefail

SKILL_NAME="multi-agent"
REPO_URL="https://github.com/gonelake/multi-agent.git"
INSTALL_DIR="${HOME}/.skills/multi-agent"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── 1. 确保项目代码已就绪 ──────────────────────────────────
if [[ -d "${INSTALL_DIR}/.git" ]]; then
    echo "→ 更新项目代码..."
    git -C "${INSTALL_DIR}" pull --quiet
    echo "✓ 代码已更新: ${INSTALL_DIR}"
else
    echo "→ 正在 clone 项目代码..."
    git clone --quiet "${REPO_URL}" "${INSTALL_DIR}"
    echo "✓ 项目代码已下载: ${INSTALL_DIR}"
fi

# ── 2. 安装 Python 依赖 ────────────────────────────────────
if [[ -f "${INSTALL_DIR}/requirements.txt" ]]; then
    echo "→ 安装 Python 依赖..."
    pip install --quiet -r "${INSTALL_DIR}/requirements.txt"
    echo "✓ Python 依赖已安装"
fi

# ── 3. 生成包含真实路径的 SKILL.md ────────────────────────
RESOLVED_SKILL="$(mktemp)"
sed "s|<INSTALL_DIR>|${INSTALL_DIR}|g" "${SCRIPT_DIR}/SKILL.md" > "${RESOLVED_SKILL}"

# ── 4. 解析 --agent 参数 ──────────────────────────────────
TARGET_AGENT="auto"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent) TARGET_AGENT="${2:-auto}"; shift 2 ;;
        *) shift ;;
    esac
done

# ── 5. 注册到各 AI agent ───────────────────────────────────
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

install_to_agent() {
    local agent="$1"
    local base_dir
    base_dir="$(get_agent_dir "${agent}")"
    local dest_dir="${base_dir}/${SKILL_NAME}"
    mkdir -p "${dest_dir}"
    cp "${RESOLVED_SKILL}" "${dest_dir}/SKILL.md"
    echo "✓ 已注册到 ${agent}: ${dest_dir}"
}

agent_exists() {
    local base_dir
    base_dir="$(get_agent_dir "$1")"
    [[ -d "${base_dir}" ]] || [[ -d "$(dirname "${base_dir}")" ]]
}

installed=""

for agent in ${AGENTS}; do
    case "${TARGET_AGENT}" in
        auto)
            if agent_exists "${agent}"; then
                install_to_agent "${agent}"
                installed="${installed} ${agent}"
            fi
            ;;
        all|"${agent}")
            install_to_agent "${agent}"
            installed="${installed} ${agent}"
            ;;
    esac
done

rm -f "${RESOLVED_SKILL}"

if [[ -z "${installed}" ]]; then
    echo "⚠ 未检测到已安装的 agent，请手动指定：" >&2
    echo "  bash install.sh --agent [codebuddy|claude|openclaw|all]" >&2
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ multi-agent skill 安装完成"
echo "  已注册到:${installed}"
echo "  项目路径: ${INSTALL_DIR}"
echo ""
echo "快速体验（demo 模式，无需 API Key）："
echo "  cd ${INSTALL_DIR} && python main.py --demo"
echo ""
echo "生产模式（需配置 API Key）："
echo "  # 在 ${INSTALL_DIR}/ 创建 .env 文件，填入以下内容："
echo "  # LLM_API_KEY=your-api-key"
echo "  # LLM_BASE_URL=https://api.moonshot.cn/v1  # 可选"
echo "  # LLM_MODEL=moonshot-v1-8k                 # 可选"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
