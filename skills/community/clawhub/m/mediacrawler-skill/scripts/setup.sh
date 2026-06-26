#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/NanmiCoder/MediaCrawler.git"
PROJECT_DIR="${PROJECT_PATH:-$HOME/MediaCrawler}"
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"
export UV_HTTP_TIMEOUT="${UV_HTTP_TIMEOUT:-120}"

log() {
  echo "[MediaCrawler Skill] $*"
}

fail() {
  echo "[MediaCrawler Skill] ERROR: $*" >&2
  exit 1
}

log "[1/6] 检查 git ..."
command -v git >/dev/null 2>&1 || fail "未检测到 git，请先安装 git。"

log "[2/6] 检查 uv ..."
if ! command -v uv >/dev/null 2>&1; then
  log "未检测到 uv，开始自动安装..."
  command -v curl >/dev/null 2>&1 || fail "安装 uv 需要 curl，请先安装 curl。"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 || fail "uv 安装完成，但当前 shell 仍无法找到 uv。"
fi

log "[3/6] 准备项目目录: $PROJECT_DIR"
if [ -d "$PROJECT_DIR" ]; then
  if [ -d "$PROJECT_DIR/.git" ]; then
    REMOTE_URL="$(git -C "$PROJECT_DIR" remote get-url origin 2>/dev/null || true)"
    echo "$REMOTE_URL" | grep -q "NanmiCoder/MediaCrawler" || fail "目录已存在，但不是目标仓库: $PROJECT_DIR"
    log "检测到已有 MediaCrawler 仓库，尝试更新..."
    git -C "$PROJECT_DIR" pull --ff-only || fail "git pull 失败，请检查本地改动或网络。"
  else
    fail "目录已存在但不是 git 仓库: $PROJECT_DIR"
  fi
else
  log "开始克隆项目..."
  git clone "$REPO_URL" "$PROJECT_DIR" || fail "git clone 失败，请检查网络或仓库地址。"
fi

cd "$PROJECT_DIR"

[ -f "pyproject.toml" ] || fail "未找到 pyproject.toml，项目结构异常。"
[ -f "main.py" ] || fail "未找到 main.py，项目结构异常。"

log "[4/6] 使用 uv 同步依赖 ..."
if ! uv sync; then
  log "首次 uv sync 失败，重试一次..."
  uv sync || fail "uv sync 执行失败。"
fi

log "[5/6] 安装 Playwright Chromium ..."
uv run playwright install chromium || fail "Playwright Chromium 安装失败。"

log "[6/6] 执行健康检查 ..."
uv run main.py --help >/dev/null || fail "健康检查失败：无法执行 'uv run main.py --help'。"

log "安装完成。"
log "项目目录: $PROJECT_DIR"
log "帮助命令: cd \"$PROJECT_DIR\" && uv run main.py --help"
log "默认结果目录: $PROJECT_DIR/data"
log "例如抖音 JSONL 结果通常位于: $PROJECT_DIR/data/douyin/jsonl"
