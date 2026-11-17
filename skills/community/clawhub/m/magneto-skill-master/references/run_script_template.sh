#!/usr/bin/env bash
# run_script.sh 模板 —— 复制到目标技能根目录后使用
# 作用：用 WorkBuddy 受管虚拟环境的 python 执行 scripts/ 下的脚本，
#       避免污染系统 Python，也无需在技能目录内创建 .venv。
# 用法（在技能目录内）： bash run_script.sh <脚本名> <参数...>
# 路径可移植：从 $HOME 推导 venv 位置，并用 cygpath 转原生 Windows 路径。

set -euo pipefail

# 受管 venv 的 python（从 $HOME 推导；跨用户/跨机可用）
VENV_PY_POSIX="$HOME/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
if command -v cygpath >/dev/null 2>&1; then
  VENV_PY="$(cygpath -w -a "$VENV_PY_POSIX")"
else
  VENV_PY="$VENV_PY_POSIX"
fi

# 本脚本所在目录下的 scripts/（转为原生 Windows 路径，避免 MSYS 转换歧义）
SCRIPT_DIR_POSIX="$(cd "$(dirname "$0")" && pwd)/scripts"
if command -v cygpath >/dev/null 2>&1; then
  SCRIPT_DIR="$(cygpath -w -a "$SCRIPT_DIR_POSIX")"
else
  SCRIPT_DIR="$SCRIPT_DIR_POSIX"
fi
# 统一用反斜杠，Windows python 解析更稳
SCRIPT_DIR="${SCRIPT_DIR//\//\\}"

if [ "$#" -lt 1 ]; then
  echo "用法: bash run_script.sh <脚本名> <参数...>" >&2
  exit 1
fi

SCRIPT_NAME="$1"
shift

# 若未带 .py 后缀则补上
case "$SCRIPT_NAME" in
  *.py) ;;
  *) SCRIPT_NAME="$SCRIPT_NAME.py" ;;
esac

TARGET="${SCRIPT_DIR}\\${SCRIPT_NAME}"
if [ ! -f "$TARGET" ]; then
  echo "找不到脚本: $TARGET" >&2
  exit 1
fi

exec "$VENV_PY" "$TARGET" "$@"
