#!/usr/bin/env bash
# =============================================================================
# NexusTrader MCP — 一键安装脚本
# =============================================================================
# 执行顺序（每步失败即退出）：
#
#   1. 打印本脚本将做/不做的事项
#   2. 检查 Python 3.x 可用性
#   3. 检查 nexustrader-mcp 服务是否已在运行（已运行则退出）
#   4. 检查 ~/NexusTrader-mcp 代码目录（不存在则提示 git clone 并退出）
#   5. 检查 / 安装 uv
#   6. 运行 nexustrader-mcp setup（生成 config.yaml）
#   7. 启动 nexustrader-mcp 服务器
#   8. 验证服务已上线（最长等 90s），成功则打印安装完成
#
# 用法:
#   bash openclaw/install.sh
#   bash openclaw/install.sh --uninstall   移除 OpenClaw Skill 相关注册
#   bash openclaw/install.sh --help
# =============================================================================

set -euo pipefail

# ── 颜色 ──────────────────────────────────────────────────────────────────────
_green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
_red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
_yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }
_blue()   { printf '\033[0;34m%s\033[0m\n' "$*"; }
_bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

# ── 路径（固定安装到 ~/NexusTrader-mcp） ────────────────────────────────────
PROJECT_DIR="${HOME}/NexusTrader-mcp"
OPENCLAW_DIR="${PROJECT_DIR}/openclaw"
CONFIG_PATH="${PROJECT_DIR}/config.yaml"
BRIDGE_PY="${OPENCLAW_DIR}/bridge.py"
SKILL_BRIDGE="${HOME}/.openclaw/skills/nexustrader/bridge.py"

MCP_HOST="127.0.0.1"
MCP_PORT="18765"

PYTHON_CMD=""   # 由 check_python 设置

# ── 解析参数 ──────────────────────────────────────────────────────────────────
COMMAND="install"
for arg in "$@"; do
    case "${arg}" in
        --uninstall|uninstall) COMMAND="uninstall" ;;
        --help|-h)             COMMAND="help"      ;;
    esac
done

# ── 帮助 ──────────────────────────────────────────────────────────────────────
cmd_help() {
    cat <<EOF
NexusTrader MCP — 一键安装脚本

用法:
  bash openclaw/install.sh             完整安装（检查 → setup → 启动 → 验证）
  bash openclaw/install.sh --uninstall 卸载 OpenClaw Skill 注册信息
  bash openclaw/install.sh --help      显示帮助

说明:
  项目目录固定为 ~/NexusTrader-mcp。
  如未克隆，脚本会给出 git clone 命令后退出。
  setup 步骤需要交互式填写配置，无法跳过。
EOF
}

# ── 步骤 1：告知用户 ──────────────────────────────────────────────────────────
print_plan() {
    _bold "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    _bold " NexusTrader MCP — 一键安装"
    _bold "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "本脚本将依次完成以下工作："
    echo "  [2] 检查 Python 3.x 可用性"
    echo "  [3] 检查 MCP 服务是否已在运行（已运行则退出）"
    echo "  [4] 检查代码目录 ~/NexusTrader-mcp 是否存在"
    echo "  [5] 检查 uv 包管理器（如未安装则提示手动安装后退出）"
    echo "  [6] 运行 nexustrader-mcp setup（初始化 config.yaml）"
    echo "  [7] 启动 nexustrader-mcp 服务器"
    echo "  [8] 验证服务已成功上线"
    echo ""
    echo "本脚本不会做以下事情："
    echo "  ✘ 不修改系统 Python 环境或全局包"
    echo "  ✘ 不自动填写 API 密钥（需手动编辑 .keys/.secrets.toml）"
    echo "  ✘ 不自动克隆代码（目录不存在时给出命令后退出）"
    echo ""
}

# ── 步骤 2：检查 Python 3 ─────────────────────────────────────────────────────
check_python() {
    _blue "[2/8] 检查 Python 版本..."

    for cmd in python python3; do
        if command -v "${cmd}" &>/dev/null; then
            ver=$("${cmd}" --version 2>&1 || true)
            if [[ "${ver}" =~ Python\ 3\. ]]; then
                PYTHON_CMD="${cmd}"
                _green "  ✓ ${ver}  (命令: ${cmd})"
                return 0
            fi
        fi
    done

    _red "  ✗ 未找到 Python 3.x（尝试了 python / python3）"
    _red "  请先安装 Python 3.11+：https://www.python.org/downloads/"
    exit 1
}

# ── 辅助：检测服务状态（返回 "online" 或 "offline"）──────────────────────────
_get_service_status() {
    local bridge=""
    if [[ -f "${BRIDGE_PY}" ]]; then
        bridge="${BRIDGE_PY}"
    elif [[ -f "${SKILL_BRIDGE}" ]]; then
        bridge="${SKILL_BRIDGE}"
    fi

    if [[ -n "${bridge}" ]]; then
        "${PYTHON_CMD}" "${bridge}" status 2>/dev/null \
            | "${PYTHON_CMD}" -c "import sys,json; print(json.load(sys.stdin).get('status','offline'))" 2>/dev/null \
            || echo "offline"
    else
        # 兜底：直接 TCP 探测
        "${PYTHON_CMD}" - <<PYEOF 2>/dev/null || echo "offline"
import socket
try:
    s = socket.create_connection(("${MCP_HOST}", ${MCP_PORT}), timeout=2)
    s.close()
    print("online")
except Exception:
    print("offline")
PYEOF
    fi
}

# ── 步骤 3：检查服务是否已运行 ────────────────────────────────────────────────
check_service_running() {
    _blue "[3/8] 检查 nexustrader-mcp 服务状态..."

    local status
    status=$(_get_service_status)

    if [[ "${status}" == "online" ]]; then
        _green "  ✓ 服务已在运行（http://${MCP_HOST}:${MCP_PORT}/sse）"
        _yellow "  无需重新安装。如需重启，请运行："
        echo "    cd ${PROJECT_DIR} && uv run nexustrader-mcp stop && uv run nexustrader-mcp start"
        exit 0
    fi

    _yellow "  服务未运行，继续安装流程..."
}

# ── 步骤 4：检查代码目录 ──────────────────────────────────────────────────────
check_dirs() {
    _blue "[4/8] 检查代码目录..."

    if [[ ! -d "${PROJECT_DIR}" ]] || [[ ! -d "${OPENCLAW_DIR}" ]]; then
        _yellow "  代码目录不存在，请先克隆项目到本地："
        echo ""
        _bold "    git clone https://github.com/Quantweb3-com/NexusTrader-mcp.git ~/NexusTrader-mcp"
        echo ""
        echo "  克隆完成后重新运行："
        echo "    bash ~/NexusTrader-mcp/openclaw/install.sh"
        exit 1
    fi

    _green "  ✓ 代码目录存在: ${PROJECT_DIR}"
}

# ── 步骤 5：检查 uv（不自动下载，要求用户手动安装）────────────────────────────
check_uv() {
    _blue "[5/8] 检查 uv..."
    export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${PATH}"

    if command -v uv &>/dev/null; then
        _green "  ✓ uv 已安装: $(uv --version)"
        return 0
    fi

    _red "  ✗ 未找到 uv"
    echo ""
    echo "  请先手动安装 uv，然后重新运行本脚本："
    echo ""
    _bold "    # macOS / Linux："
    echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    _bold "    # 或通过包管理器："
    echo "    brew install uv          # macOS Homebrew"
    echo "    pip install uv           # pip"
    echo ""
    echo "  详细安装说明：https://docs.astral.sh/uv/getting-started/installation/"
    echo "  建议安装前先查看脚本内容：curl -fsSL https://astral.sh/uv/install.sh | less"
    echo ""
    exit 1
}

# ── 步骤 6：运行 setup ────────────────────────────────────────────────────────
run_setup() {
    _blue "[6/8] 初始化配置（nexustrader-mcp setup）..."

    if [[ -f "${CONFIG_PATH}" ]]; then
        _green "  ✓ config.yaml 已存在，跳过 setup"
        return 0
    fi

    echo ""
    _yellow "  config.yaml 不存在，需要运行初始化向导。"
    echo "  向导会询问：交易所、账户类型、预订阅交易对，以及 AI 客户端配置。"
    echo "  API 密钥请事后手动填入 ${PROJECT_DIR}/.keys/.secrets.toml"
    echo ""

    cd "${PROJECT_DIR}"
    if ! uv run nexustrader-mcp setup; then
        _red "  ✗ setup 执行失败，请查看上方错误信息并重新运行"
        exit 1
    fi

    if [[ -f "${CONFIG_PATH}" ]]; then
        _green "  ✓ setup 完成，config.yaml 已生成"
    else
        _red "  ✗ setup 未生成 config.yaml，请检查错误并重新运行"
        exit 1
    fi
}

# ── 步骤 7：启动服务器 ────────────────────────────────────────────────────────
start_server() {
    _blue "[7/8] 启动 nexustrader-mcp 服务器..."
    echo "  (初始化可能需要 30–60 秒，请稍候...)"

    cd "${PROJECT_DIR}"
    if ! uv run nexustrader-mcp start; then
        _red "  ✗ 服务器启动命令执行失败"
        exit 1
    fi
}

# ── 步骤 8：验证服务已上线 ────────────────────────────────────────────────────
verify_service() {
    _blue "[8/8] 验证服务状态（最长等待 90s）..."

    local waited=0
    while [[ ${waited} -lt 90 ]]; do
        sleep 3
        waited=$((waited + 3))

        local status
        status=$(_get_service_status)

        if [[ "${status}" == "online" ]]; then
            echo ""
            _bold "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            _bold " ✅ 安装成功！NexusTrader MCP 服务已就绪"
            _bold "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
            echo "  SSE URL : http://${MCP_HOST}:${MCP_PORT}/sse"
            echo "  项目目录: ${PROJECT_DIR}"
            echo "  API 密钥: ${PROJECT_DIR}/.keys/.secrets.toml"
            echo ""
            echo "常用命令:"
            echo "  cd ${PROJECT_DIR}"
            echo "  uv run nexustrader-mcp status   # 查看状态"
            echo "  uv run nexustrader-mcp logs     # 查看日志"
            echo "  uv run nexustrader-mcp stop     # 停止服务"
            echo ""
            return 0
        fi

        printf "  等待服务上线... %ds / 90s\r" "${waited}"
    done

    echo ""
    _red "  ✗ 服务未能在 90s 内上线，安装失败"
    _yellow "  请查看日志排查原因："
    echo "    cd ${PROJECT_DIR} && uv run nexustrader-mcp logs"
    exit 1
}

# ── 更新本地 skill registry（index.json）────────────────────────────────────
# 把 SKILL.md 中声明的 metadata 写入 ~/.openclaw/skills/index.json，
# 确保 registry 与实际 SKILL.md 一致（避免审查工具报告元数据不一致）。
update_skill_registry() {
    local INDEX="${HOME}/.openclaw/skills/index.json"
    local SKILL_DIR="${HOME}/.openclaw/skills/nexustrader"

    # 只有在 OpenClaw skill 已安装时才执行（未安装则跳过）
    if [[ ! -f "${INDEX}" ]]; then
        return 0
    fi

    "${PYTHON_CMD}" - <<PYEOF
import json, pathlib, datetime

index_path = pathlib.Path("${INDEX}")
data = json.loads(index_path.read_text())

entry = next((s for s in data.get("skills", []) if s.get("id") == "nexustrader"), None)
if entry is None:
    print("  ℹ skills/index.json 中无 nexustrader 条目，跳过 registry 更新")
else:
    entry["metadata"] = {
        "requires": {
            "bins": ["python3", "uv"],
            "python_packages": ["fastmcp"]
        },
        "credentials": [
            {
                "name": "NEXUSTRADER_API_KEYS",
                "description": "Exchange API keys stored in NexusTrader-mcp project at .keys/.secrets.toml",
                "scope": "local_file"
            }
        ],
        "env": [
            "NEXUSTRADER_MCP_URL",
            "NEXUSTRADER_PROJECT_DIR",
            "NEXUSTRADER_NO_AUTOSTART"
        ],
        "network": [
            "127.0.0.1:18765 (local MCP server via SSE)"
        ],
        "side_effects": [
            "May auto-start nexustrader-mcp background daemon (set NEXUSTRADER_NO_AUTOSTART=1 to disable)",
            "Reads .env and .keys/.secrets.toml from NexusTrader-mcp project directory",
            "Can execute real trades via create_order/cancel_order/modify_order (requires explicit user confirmation)"
        ]
    }
    index_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("  ✓ skills/index.json metadata 已更新（credentials、requires、side_effects）")
PYEOF
}

# ── 卸载 ──────────────────────────────────────────────────────────────────────
cmd_uninstall() {
    SKILL_DIR="${HOME}/.openclaw/skills/nexustrader"
    OPENCLAW_WORKSPACE="${HOME}/.openclaw/workspace"
    BOOT_MD="${OPENCLAW_WORKSPACE}/BOOT.md"
    TOOLS_MD="${OPENCLAW_WORKSPACE}/TOOLS.md"
    BOOT_MARKER="# NexusTrader Boot Check"
    TOOLS_MARKER="## NexusTrader"

    _blue "卸载 NexusTrader MCP Skill 注册信息..."

    if [[ -f "${BOOT_MD}" ]] && grep -qF "${BOOT_MARKER}" "${BOOT_MD}"; then
        "${PYTHON_CMD}" - <<PYEOF
import re, pathlib
p = pathlib.Path("${BOOT_MD}")
txt = p.read_text()
txt = re.sub(r'\n*# NexusTrader Boot Check\b.*?(?=\n# |\Z)', '', txt, flags=re.DOTALL)
p.write_text(txt.strip() + '\n' if txt.strip() else '')
PYEOF
        _green "  已从 BOOT.md 移除"
    fi

    if [[ -f "${TOOLS_MD}" ]] && grep -qF "${TOOLS_MARKER}" "${TOOLS_MD}"; then
        "${PYTHON_CMD}" - <<PYEOF
import re, pathlib
p = pathlib.Path("${TOOLS_MD}")
txt = p.read_text()
txt = re.sub(r'\n*## NexusTrader\b.*?(?=\n## |\Z)', '', txt, flags=re.DOTALL)
p.write_text(txt.strip() + '\n' if txt.strip() else '')
PYEOF
        _green "  已从 TOOLS.md 移除"
    fi

    INDEX="${HOME}/.openclaw/skills/index.json"
    if [[ -f "${INDEX}" ]]; then
        "${PYTHON_CMD}" - <<PYEOF
import json, pathlib
p = pathlib.Path("${INDEX}")
data = json.loads(p.read_text())
data["skills"] = [s for s in data.get("skills", []) if s.get("id") != "nexustrader"]
p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("  已从 skills/index.json 移除")
PYEOF
    fi

    APPROVALS_FILE="${HOME}/.openclaw/exec-approvals.json"
    if [[ -f "${APPROVALS_FILE}" ]]; then
        "${PYTHON_CMD}" - <<PYEOF
import json, pathlib
p = pathlib.Path("${APPROVALS_FILE}")
data = json.loads(p.read_text())
pattern = "~/.openclaw/skills/nexustrader/bridge.py"
main = data.get("agents", {}).get("main", {})
before = len(main.get("allowlist", []))
main["allowlist"] = [e for e in main.get("allowlist", []) if e.get("pattern") != pattern]
if len(main.get("allowlist", [])) < before:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("  已从 exec allowlist 移除")
PYEOF
    fi

    _green "卸载完成。"
    _yellow "Skill 文件保留在 ${SKILL_DIR}（如需删除: rm -rf ${SKILL_DIR}）"
    _yellow "config.yaml 和 API 密钥未删除（保留在 ${PROJECT_DIR}）"
}

# ── 入口 ──────────────────────────────────────────────────────────────────────
case "${COMMAND}" in
    help)
        cmd_help
        ;;
    uninstall)
        check_python
        cmd_uninstall
        ;;
    install)
        print_plan
        check_python
        check_service_running
        check_dirs
        check_uv
        run_setup
        start_server
        verify_service
        update_skill_registry
        ;;
    *)
        echo "用法: bash install.sh [--uninstall] [--help]"
        exit 1
        ;;
esac
