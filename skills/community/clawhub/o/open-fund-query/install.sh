#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="open-fund-query"
SKILLS_DIR="${OPENCLAW_SKILLS_DIR:-${HOME}/.openclaw/workspace/skills}"
API_KEY="${ETF_API_KEY:-}"
API_KEY_PROVIDED=0
DO_INSTALL=1
VERIFY_API=1

usage() {
  cat <<'EOF'
Install and initialize the OEF fund query skill (open-fund-query).

Usage:
  ./install.sh --api-key KEY
  ./install.sh

Options:
  --skills-dir DIR        Target install directory. Default: ~/.openclaw/workspace/skills
  --api-key KEY           API key. If omitted, the script prompts for it.
  --no-install            Only update the API key in already-installed files.
  --skip-api-verify       Skip the final network smoke test.
  -h, --help              Show this help.
EOF
}

stage() { printf '\n==> 阶段 %s：%s\n' "$1" "$2"; }

fail() {
  local reason="$1" fix="$2" code="${3:-1}"
  printf '\n安装中止：%s\n' "$reason" >&2
  printf '修复建议：%s\n' "$fix" >&2
  exit "$code"
}

mask_key() {
  local key="$1"
  local len=${#key}
  if (( len <= 8 )); then printf '***'; else printf '%s***%s' "${key:0:4}" "${key: -4}"; fi
}

require_file() { [[ -f "$1" ]] || fail "缺少文件：$1" "$2"; }
require_dir()  { [[ -d "$1" ]] || fail "缺少目录：$1" "$2"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skills-dir) SKILLS_DIR="${2-}"; if [[ $# -ge 2 ]]; then shift 2; else shift; fi ;;
    --api-key)    API_KEY="${2-}"; API_KEY_PROVIDED=1; if [[ $# -ge 2 ]]; then shift 2; else shift; fi ;;
    --no-install) DO_INSTALL=0; shift ;;
    --skip-api-verify) VERIFY_API=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; fail "未知参数：$1" "运行 ./install.sh --help 查看支持的参数。" 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

stage 1 "环境检测"
command -v python3 >/dev/null 2>&1 || fail "未找到 python3。" "请先安装 Python 3.8 或更高版本。"
python3 - <<'PY' || fail "Python 版本过低。" "请升级到 Python 3.8 或更高版本。"
import sys; raise SystemExit(0 if sys.version_info >= (3, 8) else 1)
PY
if [[ "$DO_INSTALL" -eq 1 ]]; then
  mkdir -p "$SKILLS_DIR" || fail "无法创建安装目录：$SKILLS_DIR" "使用 --skills-dir 指定一个可写目录。"
  [[ -w "$SKILLS_DIR" ]] || fail "安装目录不可写：$SKILLS_DIR" "修复目录权限或使用 --skills-dir。"
fi
printf 'Python: %s\n' "$(python3 --version 2>&1)"
printf '安装目录: %s\n' "$SKILLS_DIR"

stage 2 "安装包完整性检查"
require_dir  "${SCRIPT_DIR}" "请重新解压安装包，确保 ${SKILL_NAME} 目录存在。"
require_file "${SCRIPT_DIR}/SKILL.md" "请重新下载安装包，确保文件完整。"
require_file "${SCRIPT_DIR}/config.py" "请重新下载安装包，确保配置文件完整。"
require_file "${SCRIPT_DIR}/references/catalog-oef.md" "请重新解压安装包，确保 OEF 参考文件完整。"
printf '安装包检查通过：%s\n' "$SKILL_NAME"

stage 3 "初始化 API Key"
if [[ -z "$API_KEY" && "$API_KEY_PROVIDED" -eq 0 ]]; then
  read -r -s -p "请输入 API Key: " API_KEY; printf '\n'
fi
[[ -n "$API_KEY" ]] || fail "API Key 为空。" "使用 --api-key YOUR_KEY 重新运行。" 2
printf 'API Key 读取成功：%s\n' "$(mask_key "$API_KEY")"

stage 4 "安装功能"
if [[ "$DO_INSTALL" -eq 1 ]]; then
  rm -rf "${SKILLS_DIR:?}/${SKILL_NAME}"
  cp -R "${SCRIPT_DIR}" "${SKILLS_DIR}/${SKILL_NAME}" || fail "复制 ${SKILL_NAME} 失败。" "检查 ${SKILLS_DIR} 权限。"
  find "${SKILLS_DIR}/${SKILL_NAME}" \( -name '.DS_Store' -o -name '__pycache__' \) -prune -exec rm -rf {} +
  require_file "${SKILLS_DIR}/${SKILL_NAME}/SKILL.md" "复制后文件不完整，请重新安装。"
  require_file "${SKILLS_DIR}/${SKILL_NAME}/config.py" "复制后文件不完整，请重新安装。"
  printf '已安装功能：%s\n' "$SKILL_NAME"
fi

PROFILE_WRITTEN=0
SHELL_PROFILE=""
case "${SHELL:-}" in
  */zsh)  SHELL_PROFILE="${ZDOTDIR:-$HOME}/.zshrc" ;;
  */bash) SHELL_PROFILE="$HOME/.bash_profile" ;;
esac
if [[ -n "$SHELL_PROFILE" ]]; then
  {
    grep -v '^export ETF_API_KEY=' "$SHELL_PROFILE" 2>/dev/null > "${SHELL_PROFILE}.tmp" || true
    printf 'export ETF_API_KEY="%s"\n' "$API_KEY" >> "${SHELL_PROFILE}.tmp"
    mv "${SHELL_PROFILE}.tmp" "$SHELL_PROFILE"
  } && PROFILE_WRITTEN=1 || rm -f "${SHELL_PROFILE}.tmp"
  if [[ "$PROFILE_WRITTEN" -eq 1 ]]; then
    printf 'API Key 已写入环境变量：%s\n' "$SHELL_PROFILE"
    printf '请执行 source %s 或重启终端使配置生效。\n' "$SHELL_PROFILE"
  else
    printf '写入环境变量失败。\n'
  fi
fi

config_path="${SKILLS_DIR}/${SKILL_NAME}/config.py"
if [[ -f "$config_path" ]]; then
  python3 - "$config_path" "$API_KEY" <<'PY' || fail "写入本地配置失败。" "检查安装目录权限。"
import re, sys
from pathlib import Path
path = Path(sys.argv[1]); key = sys.argv[2]
text = path.read_text(encoding="utf-8")
text = re.sub(r'(_FALLBACK_KEY\s*=\s*")[^"]*(")', rf'\g<1>{key}\2', text)
path.write_text(text, encoding="utf-8")
PY
  printf 'API Key 已保存到本地配置中。\n'
fi

export ETF_API_KEY="$API_KEY"

stage 5 "能力校验"
config_path="${SKILLS_DIR}/${SKILL_NAME}/config.py"

require_file "$config_path" "确认安装目录中的 config.py 存在。"

BASE_URL="$(sed -nE 's/^BASE_URL[[:space:]]*=[[:space:]]*"([^"]+)".*/\1/p' "$config_path" | head -n 1)"
CALLER_TYPE="$(sed -nE 's/^CALLER_TYPE[[:space:]]*=[[:space:]]*"([^"]+)".*/\1/p' "$config_path" | head -n 1)"

if [[ -z "$CALLER_TYPE" ]]; then
  CALLER_TYPE="external"
fi

[[ "$BASE_URL" == https://* ]] || fail "本地配置校验失败：BASE_URL 无效。" "检查 config.py 中的 BASE_URL。"
[[ -n "$API_KEY" ]] || fail "本地配置校验失败：API_KEY 为空。" "请使用 --api-key YOUR_KEY 重新安装。"

printf '本地配置校验通过。\n'

if [[ "$VERIFY_API" -eq 1 ]]; then
  python3 - "$BASE_URL" "$API_KEY" "$CALLER_TYPE" <<'PY' || fail "接口连通性校验失败。" "确认网络、API Key 有效；离线环境可加 --skip-api-verify。"
import json
import ssl
import sys
import urllib.request

base_url, api_key, caller_type = sys.argv[1], sys.argv[2], sys.argv[3]

ctx = ssl.create_default_context()
req = urllib.request.Request(
    base_url + "/skill/v1/oef/detail",
    data=json.dumps({"fundCodes": ["006748"]}).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Caller-Type": caller_type,
    },
    method="POST",
)

with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
    body = json.loads(resp.read())

if body.get("success") is False:
    raise RuntimeError(body.get("message") or str(body)[:200])
PY
  printf '接口连通性校验通过。\n'
else
  printf '已跳过接口连通性校验。\n'
fi

stage 6 "完成"
printf '安装完成。\n'
printf '安装目录: %s\n' "$SKILLS_DIR"
printf '可用功能: %s\n' "$SKILL_NAME"
