#!/usr/bin/env bash
# multi-codegen CLI 入口
# 用法：multi-codegen "需求"  或  echo "需求" | multi-codegen
# 特点：自动管理 venv（首次运行自动建 + 装依赖）

set -euo pipefail

# 解析软链到真实路径（支持 ~/.local/bin/multi-codegen 软链调用）
# 用 python os.path.realpath 替代 readlink -f（readlink -f 在某些环境解析错）
SCRIPT_PATH="$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "${BASH_SOURCE[0]}")"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_PATH")")"
SCRIPT="${SKILL_DIR}/scripts/multi_codegen.py"
SCRIPT="${SKILL_DIR}/scripts/multi_codegen.py"
REQ="${SKILL_DIR}/requirements.txt"
VENV_DIR="${SKILL_DIR}/.venv"
VENV_PY="${VENV_DIR}/bin/python"

# 选择 Python 解释器
if [[ -x "$VENV_PY" ]]; then
  PY="$VENV_PY"
else
  # 没有 venv，用系统 Python
  PY="$(command -v python3)"
  if [[ -z "$PY" ]]; then
    echo "❌ 找不到 python3，请先安装 Python 3.10+" >&2
    exit 1
  fi
  
  # 首次运行：检查依赖，没有就提示安装
  if ! "$PY" -c "import langgraph, langchain_anthropic" 2>/dev/null; then
    echo "⚠️  检测到首次运行，需要安装依赖..." >&2
    # 检测 PEP 668（Debian/Ubuntu 系统 Python 保护）
    # 用 set +e +o pipefail 同时禁用错误退出和 pipefail
    # （因为 pip dry-run 遇到 PEP 668 会 exit 1，但 grep 找到需要退出 0）
    PEP668_FLAG=""
    set +e +o pipefail
    "$PY" -m pip install --dry-run -r "$REQ" 2>&1 | grep -q "externally-managed-environment"
    PEP668_DETECTED=$?
    set -e -o pipefail
    if [[ $PEP668_DETECTED -eq 0 ]]; then
      PEP668_FLAG="--break-system-packages"
      echo "   检测到 PEP 668 保护，自动加 --break-system-packages" >&2
    fi
    echo "   自动执行：$PY -m pip install $PEP668_FLAG -r $REQ" >&2
    "$PY" -m pip install $PEP668_FLAG --user -r "$REQ" 2>&1 | tail -5
    if ! "$PY" -c "import langgraph, langchain_anthropic" 2>/dev/null; then
      echo "❌ 依赖安装失败，请手动：$PY -m pip install $PEP668_FLAG -r $REQ" >&2
      exit 1
    fi
    echo "✅ 依赖装好" >&2
  fi
fi

# 凭证透传
if [[ -n "${EM_API_KEY:-}" ]]; then
  export EM_API_KEY
fi
if [[ -n "${MINIMAX_API_KEY:-}" ]]; then
  export MINIMAX_API_KEY
fi

exec "$PY" "$SCRIPT" "$@"
