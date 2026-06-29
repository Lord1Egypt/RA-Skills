#!/usr/bin/env bash
# install_and_verify.sh — 大模型 Token 成本节约工具 一键安装验证脚本
# 用法：curl -sSL https://raw.githubusercontent.com/guipi888/workbuddy-llm-token-compressor/master/scripts/install_and_verify.sh | bash
# 或本地执行：bash scripts/install_and_verify.sh

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✅ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $*${NC}"; }
err()  { echo -e "${RED}❌ $*${NC}"; }

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  大模型 Token 成本节约工具 — 安装 & 验证脚本 v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── 1. 检测 Python 版本 ────────────────────────────────────────────
echo "🔍 检测 Python 版本..."
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo $PY_VER | cut -d. -f1)
    PY_MINOR=$(echo $PY_VER | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
        ok "Python $PY_VER（满足 3.10+ 要求）"
    else
        err "Python $PY_VER 版本过低，headroom 需要 Python 3.10+"
        echo "   请升级 Python 后重试：https://www.python.org/downloads/"
        exit 1
    fi
else
    err "未找到 python3，请先安装 Python 3.10+"
    exit 1
fi

# ── 2. 安装 headroom-ai ───────────────────────────────────────────
echo ""
echo "📦 安装 headroom-ai[all]..."
if python3 -c "import headroom" &>/dev/null 2>&1; then
    INSTALLED_VER=$(python3 -c "import importlib.metadata; print(importlib.metadata.version('headroom-ai'))" 2>/dev/null || echo "已安装")
    ok "headroom-ai 已安装（$INSTALLED_VER），跳过"
else
    echo "   首次安装需要下载 Rust 编译的核心组件，可能需要 2-5 分钟..."
    # 企业 SSL 环境：如设置了 CA 证书则传递
    PIP_CERT_OPTS=""
    if [ -n "$REQUESTS_CA_BUNDLE" ]; then
        PIP_CERT_OPTS="--cert $REQUESTS_CA_BUNDLE"
    fi
    if python3 -m pip install $PIP_CERT_OPTS "headroom-ai[all]" -q; then
        ok "headroom-ai 安装成功"
    else
        warn "完整安装失败，尝试仅安装核心功能..."
        python3 -m pip install $PIP_CERT_OPTS "headroom-ai" -q && ok "headroom-ai 核心版安装成功"
    fi
fi

# ── 3. 检测 headroom 命令 ─────────────────────────────────────────
echo ""
echo "🔍 验证 headroom CLI..."
if command -v headroom &>/dev/null; then
    HEADROOM_VER=$(headroom --version 2>/dev/null || echo "")
    ok "headroom CLI 可用${HEADROOM_VER:+（$HEADROOM_VER）}"
else
    # 尝试通过 python3 -m 调用
    if python3 -m headroom --version &>/dev/null 2>&1; then
        ok "headroom 可通过 python3 -m headroom 调用"
        HEADROOM_CMD="python3 -m headroom"
    else
        err "headroom CLI 未找到，请确认 pip 安装路径是否在 PATH 中"
        echo "   尝试：export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

# ── 4. 运行 doctor 检测 ───────────────────────────────────────────
echo ""
echo "🩺 运行 headroom doctor（检测可用后端）..."
DOCTOR_CMD="headroom"
if ! command -v headroom &>/dev/null; then
    DOCTOR_CMD="python3 -m headroom"
fi

if $DOCTOR_CMD audit-reads --codex 2>/dev/null || $DOCTOR_CMD perf 2>/dev/null; then
    ok "doctor 运行成功"
else
    warn "doctor 输出为空（可能是首次运行，尚无历史数据）"
fi

# ── 5. 展示快速接入命令 ───────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 安装验证完成！快速开始："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  # 包装 Claude Code（推荐）"
echo "  headroom wrap claude"
echo ""
echo "  # 代理模式（零代码改动，适合任意 SDK）"
echo "  headroom proxy --port 8787"
echo "  export ANTHROPIC_BASE_URL=http://localhost:8787"
echo ""
echo "  # 查看压缩节省量"
echo "  headroom perf"
echo ""
