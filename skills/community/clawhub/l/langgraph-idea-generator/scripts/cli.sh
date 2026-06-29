#!/usr/bin/env bash
# idea-gen CLI 入口
# 用法：idea-gen "需求"  或  echo "需求" | idea-gen
# 特点：自动用 skill 自带 venv

set -euo pipefail

# 解析软链到真实路径（支持 ~/.local/bin/idea-gen 软链调用）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "${BASH_SOURCE[0]}")"
SKILL_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
VENV_PY="${SKILL_DIR}/.venv/bin/python"
SCRIPT="${SKILL_DIR}/scripts/idea_gen.py"

# 检查 venv
if [[ ! -x "$VENV_PY" ]]; then
  echo "❌ venv 不存在：$VENV_PY" >&2
  echo "   修复：cd $SKILL_DIR && python3 -m venv .venv && .venv/bin/pip install langgraph langchain-anthropic" >&2
  exit 1
fi

# 检查脚本
if [[ ! -f "$SCRIPT" ]]; then
  echo "❌ 脚本不存在：$SCRIPT" >&2
  exit 1
fi

# 凭证透传（如果父 shell 有）
if [[ -n "${EM_API_KEY:-}" ]]; then
  export EM_API_KEY
fi
if [[ -n "${MINIMAX_API_KEY:-}" ]]; then
  export MINIMAX_API_KEY
fi

# 调用
exec "$VENV_PY" "$SCRIPT" "$@"
