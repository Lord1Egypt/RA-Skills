#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "${ROOT_DIR}/scripts/common.sh"

PYTHON_BIN="$(python3_bin || true)"

if [[ -z "${PYTHON_BIN}" ]]; then
  log "未找到 python3，无法安装本地搜索服务。"
  exit 1
fi

mkdir -p "${LOCAL_SEARCH_ROOT}"

log "安装目录: ${LOCAL_SEARCH_ROOT}"
log "下载 SearXNG 源码（GitHub 较慢时会自动续传）"
curl -L -C - --retry 5 --retry-all-errors --retry-delay 2 \
  https://codeload.github.com/searxng/searxng/tar.gz/refs/heads/master \
  -o "${LOCAL_SEARCH_ARCHIVE}"

rm -rf "${LOCAL_SEARCH_SRC_PARENT}"
mkdir -p "${LOCAL_SEARCH_SRC_PARENT}"
tar -xzf "${LOCAL_SEARCH_ARCHIVE}" -C "${LOCAL_SEARCH_SRC_PARENT}"

SRC_DIR="$(find "${LOCAL_SEARCH_SRC_PARENT}" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "${SRC_DIR}" ]]; then
  log "源码解压失败，未找到 SearXNG 目录。"
  exit 1
fi

log "创建 Python 虚拟环境"
"${PYTHON_BIN}" -m venv "${LOCAL_SEARCH_VENV_DIR}"

log "安装依赖"
"${LOCAL_SEARCH_VENV_DIR}/bin/python" -m pip install -U pip setuptools wheel
"${LOCAL_SEARCH_VENV_DIR}/bin/pip" install -U pyyaml msgspec typing_extensions
"${LOCAL_SEARCH_VENV_DIR}/bin/pip" install waitress
"${LOCAL_SEARCH_VENV_DIR}/bin/pip" install --use-pep517 --no-build-isolation -e "${SRC_DIR}"

if [[ ! -f "${LOCAL_SEARCH_SETTINGS_FILE}" ]]; then
  LOCAL_SECRET="$(generate_local_search_secret)"
  cat > "${LOCAL_SEARCH_SETTINGS_FILE}" <<EOF
use_default_settings: true

general:
  debug: false
  instance_name: "Local SearXNG"

search:
  safe_search: 1
  autocomplete: "duckduckgo"
  formats:
    - html
    - json

server:
  base_url: ${LOCAL_SEARCH_URL}/
  port: ${LOCAL_SEARCH_PORT}
  bind_address: "${LOCAL_SEARCH_HOST}"
  secret_key: "${LOCAL_SECRET}"
  limiter: false
  image_proxy: false

engines:
  - name: bing
    disabled: false
  - name: duckduckgo
    disabled: false
  - name: google
    disabled: false
EOF
  log "已生成配置: ${LOCAL_SEARCH_SETTINGS_FILE}"
else
  log "保留现有配置: ${LOCAL_SEARCH_SETTINGS_FILE}"
fi

# ─── 安装 Scrapling（browse_page.py 满血运行所需）──────────────────────────────
log "安装 Scrapling（反爬抓取引擎，browse_page.py 核心依赖）"
if "${PYTHON_BIN}" -c "import scrapling" 2>/dev/null; then
  log "Scrapling 已安装，跳过"
else
  "${PYTHON_BIN}" -m pip install -q "scrapling[all]" \
    && log "Scrapling 安装成功" \
    || { log "[警告] Scrapling 安装失败，browse_page.py 将降级为 stdlib urllib 模式"; }
fi

# 安装 Playwright 浏览器（Scrapling DynamicFetcher / StealthyFetcher 所需）
if "${PYTHON_BIN}" -c "from scrapling.fetchers import StealthyFetcher" 2>/dev/null; then
  log "安装 Playwright 浏览器（首次约 100MB，仅需一次）"
  "${PYTHON_BIN}" -m playwright install chromium --with-deps 2>&1 | tail -3 \
    && log "Playwright Chromium 安装成功" \
    || log "[警告] Playwright 安装失败，StealthyFetcher/DynamicFetcher 不可用，将使用 Fetcher 模式"
fi

# 验证 Scrapling 三级 fetcher 可用性
log "验证 Scrapling fetcher 可用性..."
"${PYTHON_BIN}" - <<'PYEOF'
import sys
results = []
for name, mod in [
    ("Fetcher",        "scrapling.fetchers.Fetcher"),
    ("StealthyFetcher","scrapling.fetchers.StealthyFetcher"),
    ("DynamicFetcher", "scrapling.fetchers.DynamicFetcher"),
]:
    try:
        parts = mod.rsplit(".", 1)
        m = __import__(parts[0], fromlist=[parts[1]])
        getattr(m, parts[1])
        results.append(f"  [OK]  {name}")
    except Exception as e:
        results.append(f"  [--]  {name} (不可用: {e})")
print("\n".join(results))
PYEOF

if [[ -x "${ROOT_DIR}/sync_openclaw_workspace.sh" ]]; then
  log "同步 OpenClaw workspace 配置"
  "${ROOT_DIR}/sync_openclaw_workspace.sh"
fi

log "安装完成。下一步执行 ./start_local_search.sh"
