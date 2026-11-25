#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — AI CLI 主题/差异渲染检查
#
#   ./scripts/setup-cli.sh --config <设置文件>                    # 看该 CLI 当前主题
#   ./scripts/setup-cli.sh --config <设置文件> --check            # 0=OK 1=ANSI 2=没有配置
#   ./scripts/setup-cli.sh --config <设置文件> --dry-run --apply
#   ./scripts/setup-cli.sh --config <设置文件> --apply            # 把 ANSI 主题改成 theme = dark（带备份）
#
# ⛔ 不自动探测任何 CLI 的配置目录：调用方必须用 --config 显式传入设置文件路径。
# 为什么需要它：AI CLI 的 dark-ansi / light-ansi 主题会把
# diffAddedWord / diffRemovedWord 映射到 ansi:greenBright / ansi:redBright。
# 终端亮绿/亮红是给前景用的高亮槽，一旦被拿来当差异背景，正文和橙字会掉到
# 1.0–1.7:1（实测 voltage）。这不是终端色板能同时满足的两个角色，正确修法是
# 让 CLI 用非 ANSI 的 dark 主题，它自带深绿/深红差异底。
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init setup-cli "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/aliases.sh"

MODE="show"
DRY=0
TARGETS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --config)
      if [ $# -lt 2 ]; then
        printf '%s\n' "$(t M_CLI_USAGE)"; exit 1
      fi
      _cfg="$2"; shift 2
      if [ ! -f "$_cfg" ]; then
        printf '%s\n' "$(t M_CLI_NO_FILE "$_cfg")"; exit 1
      fi
      _label="$(basename "$(dirname "$_cfg")")"
      _label="${_label#.}"
      TARGETS[${#TARGETS[@]}]="$_label|$_cfg"
      ;;
    --check)   MODE="check"; shift ;;
    --apply)   MODE="apply"; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) printf '%s\n' "$(t M_CLI_USAGE)"; exit 0 ;;
    *)         printf '%s\n' "$(t M_CLI_USAGE)"; exit 1 ;;
  esac
done

c='\033[1;35m'; d='\033[2m'; o='\033[0m'
say()  { printf "\n${c}▶ %s${o}\n" "$(t "$@")"; }
info() { printf "${d}%s${o}\n" "$(t "$@")"; }
ok()   { printf "\033[1;32m%s\033[0m\n" "$(t "$@")"; }
warn() { printf "\033[1;33m%s\033[0m\n" "$(t "$@")"; }

if [ ${#TARGETS[@]} -eq 0 ]; then
  [ "$MODE" = "check" ] && exit 2
  printf '%s\n' "$(t M_CLI_NO_CONFIG)"
  exit 1
fi

# 目标主题跟当前 会勇禾口王·终端工作台 主题的明暗走：暗底终端配 dark，亮底配 light。
# 写死 dark 会让 parchment / v3 用户得到一个暗色 CLI，反而更割裂。
WANT="dark"
WANT_LABEL="Dark"
_pin="$HOME/.config/hekouwang-terminal/theme"
if [ -f "$_pin" ]; then
  _theme="$(hkw_resolve_theme "$(cat "$_pin" 2>/dev/null || true)")"
  _json="$SCRIPT_DIR/config/themes/$_theme.json"
  if [ -f "$_json" ]; then
    _light="$(python3 - "$_json" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    p = json.load(f)["Profiles"][0]
c = p["Background Color"]
def lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
r, g, b = (lin(c[k]) for k in ("Red Component", "Green Component", "Blue Component"))
print(1 if 0.2126 * r + 0.7152 * g + 0.0722 * b > 0.5 else 0)
PY
)"
    [ "$_light" = "1" ] && WANT="light"
  fi
fi
[ "$WANT" = "light" ] && WANT_LABEL="Light"

read_theme() {
  python3 - "$1" <<'PY'
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
except (OSError, ValueError):
    raise SystemExit(0)
if isinstance(data, dict) and isinstance(data.get("theme"), str):
    print(data["theme"])
PY
}

is_ansi() {
  case "${1:-}" in dark-ansi|light-ansi) return 0 ;; *) return 1 ;; esac
}

ANSI_COUNT=0
for entry in "${TARGETS[@]}"; do
  name="${entry%%|*}"
  path="${entry#*|}"
  theme="$(read_theme "$path")"
  if is_ansi "$theme"; then
    ANSI_COUNT=$((ANSI_COUNT + 1))
  fi
  if [ "$MODE" = "check" ]; then
    continue
  fi
  say M_CLI_CURRENT "$name" "${theme:-?}"
  if is_ansi "$theme"; then
    warn M_CLI_ANSI_WARN "$name" "$theme"
    info M_CLI_ANSI_FIX "$path" "$WANT" "$path"
  elif [ -z "$theme" ]; then
    info M_CLI_UNKNOWN "$name"
    info M_CLI_HINT "$WANT_LABEL"
  else
    ok M_CLI_OK "$name"
  fi
done

if [ "$MODE" = "check" ]; then
  [ "$ANSI_COUNT" -gt 0 ] && exit 1
  exit 0
fi

if [ "$MODE" = "apply" ]; then
  APPLIED=0
  for entry in "${TARGETS[@]}"; do
    name="${entry%%|*}"
    path="${entry#*|}"
    theme="$(read_theme "$path")"
    if ! is_ansi "$theme"; then
      continue
    fi
    if [ "$DRY" = "1" ]; then
      info M_CLI_APPLY_DRY "$WANT" "$path"
      APPLIED=$((APPLIED + 1))
      continue
    fi
    python3 - "$path" "$WANT" <<'PY'
import json, os, shutil, sys, time
path, want = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
if not isinstance(data, dict):
    raise SystemExit(2)
shutil.copy2(path, path + ".bak-" + time.strftime("%Y%m%d-%H%M%S"))
data["theme"] = want
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write("\n")
PY
    if [ $? -eq 0 ]; then
      ok M_CLI_APPLY_OK "$WANT" "$path"
      APPLIED=$((APPLIED + 1))
    else
      warn M_CLI_APPLY_FAIL "$path"
    fi
  done
  if [ "$APPLIED" -eq 0 ]; then
    info M_CLI_OK "$(printf '%s' "${TARGETS[0]%%|*}")"
  fi
fi
