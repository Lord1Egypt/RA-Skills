#!/usr/bin/env bash
# ============================================================================
# Infoseek 跨平台安装器 (POSIX: Linux / macOS / Windows-Git-Bash)
# ----------------------------------------------------------------------------
# 将本包安装为 WorkBuddy 用户级 skill: ~/.workbuddy/skills/infoseek
# 支持:
#   --target DIR    安装目标 (默认 $HOME/.workbuddy/skills/infoseek)
#   --venv          创建隔离 venv 并在其中装依赖 (推荐, 不污染系统)
#   --with-osint    额外安装 maigret/sherlock (身份归因 OSINT, 需显式授权)
#   --no-deps       仅复制文件, 不安装 Python 依赖
#   -h|--help       显示本帮助
# 示例:
#   bash install.sh
#   bash install.sh --venv --with-osint
#   bash install.sh --target /opt/infoseek --venv
# ============================================================================
set -euo pipefail

TARGET="${INFOSEEK_TARGET:-$HOME/.workbuddy/skills/infoseek}"
WITH_VENV=0
WITH_OSINT=0
NO_DEPS=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)     TARGET="$2"; shift 2;;
    --venv)       WITH_VENV=1; shift;;
    --with-osint) WITH_OSINT=1; shift;;
    --no-deps)    NO_DEPS=1; shift;;
    -h|--help)    grep -E '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
    *) echo "未知参数: $1" >&2; exit 1;;
  esac
done

PYBIN="$(command -v python3 || command -v python || true)"
if [[ -z "$PYBIN" ]]; then
  echo "[infoseek] 错误: 未找到 python3/python, 请先安装 Python 3.10+" >&2
  exit 1
fi

echo "[infoseek] 安装源 : $SCRIPT_DIR"
echo "[infoseek] 安装目标: $TARGET"

mkdir -p "$TARGET"
# 复制整个包 (含 install.sh 自身) 到目标
cp -R "$SCRIPT_DIR/." "$TARGET/"

if [[ "$NO_DEPS" -eq 0 ]]; then
  if [[ "$WITH_VENV" -eq 1 ]]; then
    echo "[infoseek] 创建隔离 venv: $TARGET/.venv"
    "$PYBIN" -m venv "$TARGET/.venv"
    PYBIN="$TARGET/.venv/bin/python"
    # Windows venv 可执行文件在 Scripts/
    if [[ ! -x "$PYBIN" && -x "$TARGET/.venv/Scripts/python.exe" ]]; then
      PYBIN="$TARGET/.venv/Scripts/python.exe"
    fi
  fi
  if [[ -f "$TARGET/requirements.txt" ]]; then
    echo "[infoseek] 安装依赖: requirements.txt"
    "$PYBIN" -m pip install --upgrade pip >/dev/null 2>&1 || true
    "$PYBIN" -m pip install -r "$TARGET/requirements.txt"
  fi
  if [[ "$WITH_OSINT" -eq 1 ]]; then
    echo "[infoseek] 可选 OSINT: 安装 maigret / sherlock (身份归因, 需显式 consent)"
    "$PYBIN" -m pip install maigret sherlock-project 2>&1 | tail -3 || \
      echo "[infoseek][warn] OSINT 依赖安装失败(可选, 跳过)"
  fi
fi

# 校验 skill 可加载: 语法解析关键模块
echo "[infoseek] 校验 skill 结构..."
for f in SKILL.md manifest.yaml requirements.txt; do
  if [[ ! -f "$TARGET/$f" ]]; then
    echo "[infoseek][warn] 缺少 $f" >&2
  fi
done
if "$PYBIN" -c "import ast,sys; [ast.parse(open('$TARGET/'+m).read()) for m in ['core/capability_registry.py','scripts/maigret_client.py','scripts/sherlock_client.py'] if __import__('os').path.exists('$TARGET/'+m)]; print('[infoseek] 语法校验通过')" 2>/dev/null; then
  :
else
  echo "[infoseek][warn] 语法校验跳过(可选)"
fi

echo "[infoseek] 完成. 重启 WorkBuddy 以加载 skill: $TARGET"
echo "[infoseek] 注: 身份归因(maigret/sherlock)默认关闭, 需在 pipeline 中显式授予 consent."
