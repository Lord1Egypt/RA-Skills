#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 环境自检
#
# ⚠️ 对外文案全在 lib/i18n/{en,zh}/doctor.sh，这里只留判据。
#    不带 --fix 时**一个字节都不写**，这条性质别在加检查项时破坏掉。
# ============================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
# ⚠️ i18n 必须排在下面那行 export LANG 之前 —— HKW_LANG=auto 是靠读系统 locale 定语言的，
#    先把 LANG 改成 en_US 再判断，auto 就永远只会得出英文。
hkw_i18n_init doctor "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/aliases.sh"

export LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8   # 防止 printf 多字节中文/· 乱码
set -u
BREW_PREFIX="$(brew --prefix 2>/dev/null || echo /opt/homebrew)"
DP_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
RUNTIME="$HOME/.config/hekouwang-terminal"
DOMAIN="com.googlecode.iterm2"
FAIL=0; WARN=0
FIX=0; QUIET=0; STATUS_ONLY=0; PARITY_ONLY=0
for a in "$@"; do
  case "$a" in
    --fix) FIX=1 ;;
    --quiet|-q) QUIET=1 ;;
    --status) STATUS_ONLY=1 ;;
    --parity) PARITY_ONLY=1 ;;
    -h|--help) blk_doctor_help; exit 0 ;;
  esac
done

g='\033[1;32m'; r='\033[1;31m'; y='\033[1;33m'; b='\033[1;34m'; d='\033[2m'; o='\033[0m'
FIXES=()   # 攒起来最后统一问，别打断体检的节奏
# --fix 分组：node / auto / optical / scene / reload / gui / theme / other
fix_group_of() {   # fix_group_of <cmd> <item文案>
  case "$1" in
    *node-mgr*|*install\ fnm*|*install\ nvm*|*install\ vfox*|*brew\ install\ fnm*|*brew\ install\ nvm*|*brew\ install\ vfox*|*brew\ install\ node*) printf '%s' node ;;
    *font.sh*) printf '%s' optical ;;
    *scene.sh*) printf '%s' scene ;;
    :manual:*) printf '%s' reload ;;
    *setup-gui*) printf '%s' gui ;;
    *theme.sh*) printf '%s' theme ;;
    *)
      case "$2" in
        *Node*|*fnm*|*nvm*|*vfox*) printf '%s' node ;;
        *光学*|*Optical*|*字体\ PostScript*|*font*) printf '%s' optical ;;
        *场景*|*Scene*) printf '%s' scene ;;
        *Ghostty*|*reload*|*重载*) printf '%s' reload ;;
        *GUI*|*Shift+Enter*|*Minimal*|*Cmd-click*|*CommandSelection*|*默认\ Profile*|*default\ profile*) printf '%s' gui ;;
        *Profile*|*主题*|*Triggers*|*语义*|*Smart\ Selection*) printf '%s' theme ;;
        *) printf '%s' other ;;
      esac
      ;;
  esac
}

ok()   { [ "$QUIET" = "1" ] || printf "  ${g}✓${o} %s\n" "$1"; }
bad()  { [ "$QUIET" = "1" ] || { printf "  ${r}✗${o} %s\n" "$1"; [ -n "${2:-}" ] && printf "      ${d}↳ %s${o}\n" "$2"; }; FAIL=$((FAIL+1)); [ -n "${3:-}" ] && FIXES+=("$1|$3"); }
warn() { [ "$QUIET" = "1" ] || { printf "  ${y}⚠${o} %s\n" "$1"; [ -n "${2:-}" ] && printf "      ${d}↳ %s${o}\n" "$2"; }; WARN=$((WARN+1)); [ -n "${3:-}" ] && FIXES+=("$1|$3"); }
sect() { [ "$QUIET" = "1" ] || printf "\n${b}%s${o}\n" "$1"; }
# 状态机仪表盘行：键对齐，值原样；不计入 fail/warn（明细检查仍在后面）
st()   { [ "$QUIET" = "1" ] || printf "  ${d}%-10s${o} %s\n" "$1" "$2"; }

print_parity() {
  local out rc status target detail
  printf "${b}%s${o}\n" "$(t M_DOC_PARITY_HEAD)"
  out="$(python3 "$SCRIPT_DIR/lib/parity.py" "$SCRIPT_DIR" 2>&1)"; rc=$?
  while IFS=$'\t' read -r status target detail; do
    [ -n "$status" ] || continue
    case "$status" in
      same) printf "  ${g}✓${o} %-18s ${d}%s${o}\n" "$target" "$detail" ;;
      manual) printf "  ${y}⚠${o} %-18s %s\n" "$target" "$(t M_DOC_PARITY_MANUAL "$detail")" ;;
      paid|not-installed) printf "  ${d}· %-18s %s${o}\n" "$target" "$(t M_DOC_PARITY_SKIP "$detail")" ;;
      missing|unsupported) printf "  ${y}⚠${o} %-18s %s\n" "$target" "$(t M_DOC_PARITY_MISSING "$detail")" ;;
      drift) printf "  ${r}✗${o} %-18s %s\n" "$target" "$(t M_DOC_PARITY_DRIFT "$detail")" ;;
      *) printf "  ${d}· %-18s %s${o}\n" "$target" "$detail" ;;
    esac
  done <<< "$out"
  printf "\n${d}%s${o}\n" "$(t M_DOC_PARITY_NOTE)"
  return "$rc"
}

if [ "$PARITY_ONLY" = "1" ]; then
  print_parity
  exit $?
fi

[ "$QUIET" = "1" ] || {
  printf "${b}%s${o}\n" "$(t M_DOC_HEAD)"
  printf "${d}brew prefix: %s   arch: %s   lang: %s${o}\n" "$BREW_PREFIX" "$(uname -m)" "$HKW_LANG"
}

# ---- 0. 状态机仪表盘（一眼看钉住了什么）----
# 只读汇总；光学/场景/Node 的「缺件报警」仍在后面各节，避免这里既摘要又重复打 ✗。
print_state_dashboard() {
  sect "$(t M_DOC_S0)"
  # theme
  _th="$(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || true)")"
  _p3=""
  [ -f "$RUNTIME/p3" ] && _p3=" · P3"
  if [ -n "$_th" ]; then
    st "$(t M_DOC_ST_THEME)" "$(t M_DOC_ST_PINNED "$_th")$_p3"
  else
    st "$(t M_DOC_ST_THEME)" "$(t M_DOC_ST_NONE)"
  fi
  # node
  _nm="$(tr -d '[:space:]' < "$RUNTIME/node-manager" 2>/dev/null || true)"
  if [ -n "$_nm" ]; then
    st "$(t M_DOC_ST_NODE)" "$_nm"
  else
    st "$(t M_DOC_ST_NODE)" "$(t M_DOC_ST_NODE_UNSET)"
  fi
  # optical (paid)
  if [ -f "$SCRIPT_DIR/config/typography/_engine.py" ]; then
    _oj="$(python3 "$SCRIPT_DIR/config/typography/_engine.py" resolve 2>/dev/null || true)"
    if [ -n "$_oj" ]; then
      _oid="$(printf '%s' "$_oj" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))' 2>/dev/null || true)"
      _od="$(printf '%s' "$_oj" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("density",""))' 2>/dev/null || true)"
      _os="$(printf '%s' "$_oj" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("source",""))' 2>/dev/null || true)"
      st "$(t M_DOC_ST_OPTICAL)" "$(t M_DOC_ST_OPTICAL_VAL "$_oid" "$_od" "$_os")"
    else
      st "$(t M_DOC_ST_OPTICAL)" "$(t M_DOC_ST_UNREADABLE)"
    fi
  else
    st "$(t M_DOC_ST_OPTICAL)" "$(t M_DOC_ST_PAID_ONLY)"
  fi
  # scene (paid)
  if [ -f "$SCRIPT_DIR/config/scenes/_engine.py" ]; then
    _sj="$(python3 "$SCRIPT_DIR/config/scenes/_engine.py" resolve 2>/dev/null || true)"
    if [ -n "$_sj" ]; then
      _sid="$(printf '%s' "$_sj" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))' 2>/dev/null || true)"
      _ss="$(printf '%s' "$_sj" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("source",""))' 2>/dev/null || true)"
      st "$(t M_DOC_ST_SCENE)" "$(t M_DOC_ST_SCENE_VAL "$_sid" "$_ss")"
    else
      st "$(t M_DOC_ST_SCENE)" "$(t M_DOC_ST_UNREADABLE)"
    fi
  else
    st "$(t M_DOC_ST_SCENE)" "$(t M_DOC_ST_PAID_ONLY)"
  fi
  # semantic layer from active profile
  _active="$DP_DIR/hekouwang-active-theme.json"
  if [ -f "$_active" ]; then
    _sem="$(python3 - "$_active" <<'PY' 2>/dev/null || true
import json,sys
p=json.load(open(sys.argv[1]))["Profiles"][0]
ss=p.get("Smart Selection Rules") or []
ours=sum(1 for r in ss if "hekouwang" in (r.get("notes") or ""))
sh=(p.get("Semantic History") or {}).get("action","")
print(f"{len(ss)}|{ours}|{sh}")
PY
)"
    _nr="${_sem%%|*}"; _rest="${_sem#*|}"; _no="${_rest%%|*}"; _sha="${_rest#*|}"
    if [ -n "$_nr" ] && [ "$_nr" != "$_sem" ]; then
      st "$(t M_DOC_ST_SEMANTIC)" "$(t M_DOC_ST_SEMANTIC_VAL "$_nr" "$_no" "$_sha")"
    else
      st "$(t M_DOC_ST_SEMANTIC)" "$(t M_DOC_ST_SEMANTIC_MISS)"
    fi
  else
    st "$(t M_DOC_ST_SEMANTIC)" "$(t M_DOC_ST_NONE)"
  fi
  # 色板视觉地板（对比度 / 明暗分档 / 暗字槽）—— 只读，读生成后的主题 JSON
  if [ -f "$SCRIPT_DIR/config/themes/_audit.py" ]; then
    _vb="$(python3 "$SCRIPT_DIR/config/themes/_audit.py" --brief 2>/dev/null || true)"
    _va="${_vb%% *}"; _rest="${_vb#* }"; _vn="${_rest%% *}"
    if [ -n "$_va" ] && [ "$_va" != "$_vb" ] && [ "$_va" != "$_vn" ]; then
      if [ "${_vn:-0}" = "0" ]; then
        st "$(t M_DOC_ST_VISUAL)" "$(t M_DOC_ST_VISUAL_OK "$_va")"
      else
        st "$(t M_DOC_ST_VISUAL)" "$(t M_DOC_ST_VISUAL_BAD "$_va" "$_vn")"
      fi
    fi
  fi
  # Ghostty reload hint（配置已写 ≠ 运行中窗口已吃进去）
  if [ -d "/Applications/Ghostty.app" ] || command -v ghostty >/dev/null 2>&1; then
    _gcfg="$HOME/.config/ghostty/config"
    if [ -f "$_gcfg" ]; then
      _need_reload="$(python3 - "$_gcfg" <<'PY' 2>/dev/null || echo ''
import os, sys, subprocess, time
cfg = sys.argv[1]
try:
    mtime = os.path.getmtime(cfg)
except OSError:
    print("")
    raise SystemExit
out = subprocess.run(
    ["ps", "-axo", "lstart=,comm="], capture_output=True, text=True
).stdout.splitlines()
hits = []
for line in out:
    line = line.rstrip()
    # ps comm 最后一列：Ghostty（GUI）—— CLI 子命令通常不叫这个
    if not line.endswith("Ghostty"):
        continue
    stamp = line[: -len("Ghostty")].strip()
    for fmt in ("%a %b %d %H:%M:%S %Y", "%c"):
        try:
            hits.append(time.mktime(time.strptime(stamp, fmt)))
            break
        except ValueError:
            continue
if not hits:
    print("no-process")
elif max(hits) < mtime:
    print("reload")
else:
    print("ok")
PY
)"
      case "$_need_reload" in
        reload) st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_GHOSTTY)" ;;
        no-process) st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_NOPROC)" ;;
        ok) st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_OK)" ;;
        *) st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_SKIP)" ;;
      esac
    else
      st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_NOCFG)"
    fi
  else
    st "$(t M_DOC_ST_RELOAD)" "$(t M_DOC_ST_RELOAD_NOAPP)"
  fi
}

print_state_dashboard
if [ "$STATUS_ONLY" = "1" ]; then
  exit 0
fi


# ---- 1. 基础工具链 ----
sect "$(t M_DOC_S1)"
MISSING_PKGS=""
for tool in brew starship eza bat fzf fd zoxide rg atuin tmux delta; do
  if command -v "$tool" >/dev/null 2>&1; then ok "$tool"; else
    pkg="$tool"; [ "$tool" = "rg" ] && pkg="ripgrep"; [ "$tool" = "delta" ] && pkg="git-delta"
    MISSING_PKGS="$MISSING_PKGS $pkg"
    bad "$(t M_DOC_TOOL_MISSING "$tool")" "brew install $pkg" "brew install $pkg"
  fi
done
# Node 管理器按用户选择检查（不再硬要求 fnm）
_NODE_CUR=""
[ -f "$HOME/.config/hekouwang-terminal/node-manager" ] \
  && _NODE_CUR="$(tr -d '[:space:]' < "$HOME/.config/hekouwang-terminal/node-manager")"
case "$_NODE_CUR" in
  fnm)
    if command -v fnm >/dev/null 2>&1; then ok "$(t M_DOC_NODE_ACTIVE fnm)"
    else bad "$(t M_DOC_NODE_MISSING fnm)" "brew install fnm" "brew install fnm"; fi ;;
  nvm)
    if [ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ] \
       || [ -s "${HOMEBREW_PREFIX:-/opt/homebrew}/opt/nvm/nvm.sh" ] \
       || [ -s /usr/local/opt/nvm/nvm.sh ]; then
      ok "$(t M_DOC_NODE_ACTIVE nvm)"
    else
      bad "$(t M_DOC_NODE_MISSING nvm)" "brew install nvm" "brew install nvm"
    fi ;;
  brew)
    if command -v node >/dev/null 2>&1; then ok "$(t M_DOC_NODE_ACTIVE brew)"
    else bad "$(t M_DOC_NODE_MISSING brew)" "brew install node" "brew install node"; fi ;;
  vfox)
    if command -v vfox >/dev/null 2>&1; then ok "$(t M_DOC_NODE_ACTIVE vfox)"
    else bad "$(t M_DOC_NODE_MISSING vfox)" "brew install vfox" "brew install vfox"; fi ;;
  *)
    # 未选过：老用户可能仍在 .zshrc 内联 fnm，不算缺件
    ;;
esac

# ---- 2. 字体 ----
sect "$(t M_DOC_S2)"
FONTS="$HOME/Library/Fonts"
# 主字体：Maple Mono NF CN（OFL，免费可商用），自带 Nerd 图标 + 中文等宽
if [ -f "$FONTS/MapleMono-NF-CN-Regular.ttf" ] || \
   brew list --cask font-maple-mono-nf-cn >/dev/null 2>&1; then
  ok "$(t M_DOC_FONT_MAIN_OK)"
else
  bad "$(t M_DOC_FONT_MAIN_BAD)" \
      "brew install --cask font-maple-mono-nf-cn" \
      "brew install --cask font-maple-mono-nf-cn"
fi
if find "$FONTS" -maxdepth 1 -name 'SymbolsNerdFontMono*.ttf' 2>/dev/null | grep -q .; then
  ok "$(t M_DOC_FONT_SYM_OK)"
else
  warn "$(t M_DOC_FONT_SYM_WARN)" \
       "brew install --cask font-symbols-only-nerd-font" \
       "brew install --cask font-symbols-only-nerd-font"
fi
# 字体优先级表：本机实际会用到哪一套
if [ ! -f "$SCRIPT_DIR/config/font.conf" ]; then
  [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_FONT_OSS_NOTE)"
elif true; then
  PICKED=""
  while IFS='|' read -r fps ffam fstyle fnf fnote ffile; do
    # 跳过注释、空行，以及 APPLE_TERMINAL_FONT=xxx 这类**没有竖线**的设置行
    case "$fps" in *'|'*) : ;; esac
    [ -z "${ffam:-}" ] && [ -z "${fstyle:-}" ] && [ -z "${fnf:-}" ] && continue
    fps="$(printf '%s' "$fps" | tr -d '[:space:]')"
    case "$fps" in ''|'#'*) continue ;; esac
    ffam="$(printf '%s' "$ffam" | sed 's/^ *//;s/ *$//')"
    HIT=""
    for fdir in "$HOME/Library/Fonts" "/Library/Fonts" "/System/Library/Fonts"; do
      for fe in otf ttf ttc; do [ -f "$fdir/$fps.$fe" ] && HIT=1 && break 2; done
      [ -n "${ffile:-}" ] && [ -f "$fdir/$ffile" ] && { HIT=1; break; }
    done
    if [ -n "$HIT" ] && [ -z "$PICKED" ]; then
      PICKED="$ffam"; ok "$(t M_DOC_FONT_PICKED "$ffam" "$fps")"
    elif [ -n "$HIT" ]; then
      [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_FONT_ALSO "$ffam")"
    else
      [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" \
        "$(t M_DOC_FONT_ABSENT "$ffam" "$(printf '%s' "$fnote" | sed 's/^ *//')")"
    fi
  done < "$SCRIPT_DIR/config/font.conf"
  [ -z "$PICKED" ] && warn "$(t M_DOC_FONT_NONE)" "$(t M_DOC_FONT_NONE_FIX)"
fi
# 终端光学校准引擎：光学档是否在、当前钉的是哪一档
if [ -f "$SCRIPT_DIR/config/typography/_engine.py" ]; then
  OPT_JSON="$(python3 "$SCRIPT_DIR/config/typography/_engine.py" resolve 2>/dev/null || true)"
  if [ -n "$OPT_JSON" ]; then
    OPT_ID="$(printf '%s' "$OPT_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))' 2>/dev/null || true)"
    OPT_D="$(printf '%s' "$OPT_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("density",""))' 2>/dev/null || true)"
    OPT_SRC="$(printf '%s' "$OPT_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("source",""))' 2>/dev/null || true)"
    ok "$(t M_DOC_OPTICAL_OK "$OPT_ID" "$OPT_D" "$OPT_SRC")"
  else
    warn "$(t M_DOC_OPTICAL_WARN)" "$(t M_DOC_OPTICAL_FIX)"
  fi
elif [ -f "$SCRIPT_DIR/config/font.conf" ]; then
  [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_OPTICAL_MISSING)"
fi
# 场景美学引擎：当前钉的场景
if [ -f "$SCRIPT_DIR/config/scenes/_engine.py" ]; then
  SCN_JSON="$(python3 "$SCRIPT_DIR/config/scenes/_engine.py" resolve 2>/dev/null || true)"
  if [ -n "$SCN_JSON" ]; then
    SCN_ID="$(printf '%s' "$SCN_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))' 2>/dev/null || true)"
    SCN_SRC="$(printf '%s' "$SCN_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("source",""))' 2>/dev/null || true)"
    SCN_PRIV="$(printf '%s' "$SCN_JSON" | python3 -c 'import sys,json;d=json.load(sys.stdin);print("privacy" if d.get("privacy") else "—")' 2>/dev/null || true)"
    ok "$(t M_DOC_SCENE_OK "$SCN_ID" "$SCN_SRC" "$SCN_PRIV")"
  else
    warn "$(t M_DOC_SCENE_WARN)" "$(t M_DOC_SCENE_FIX)"
  fi
elif [ -f "$SCRIPT_DIR/config/font.conf" ]; then
  [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_SCENE_MISSING)"
fi
# ⚠️ 装了 ≠ 上屏。Profile 里写的 PostScript 名如果和字体文件对不上，
#    iTerm2 会静默回退到系统字体 —— 所以这里比对 Profile 写的名字和实际字体。
ACTIVE="$DP_DIR/hekouwang-active-theme.json"
if [ -f "$ACTIVE" ]; then
  PS_NAME="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['Profiles'][0]['Normal Font'].rsplit(' ',1)[0])" "$ACTIVE" 2>/dev/null)"
  if [ -n "$PS_NAME" ]; then
    if [ -f "$FONTS/$PS_NAME.ttf" ] || [ -f "$FONTS/$PS_NAME.otf" ] \
       || [ -f "/Library/Fonts/$PS_NAME.ttf" ] || [ -f "/Library/Fonts/$PS_NAME.otf" ]; then
      ok "$(t M_DOC_FONT_PS_OK "$PS_NAME")"
    else
      warn "$(t M_DOC_FONT_PS_WARN "$PS_NAME")" "$(t M_DOC_FONT_PS_FIX)"
    fi
  fi
fi

# ---- 3. Dynamic Profile ----
sect "$(t M_DOC_S3)"
GUID=""
if [ -f "$ACTIVE" ]; then
  ok "$(t M_DOC_DP_OK)"
elif [ -f "$DP_DIR/catppuccin-mocha.json" ]; then
  ACTIVE="$DP_DIR/catppuccin-mocha.json"
  warn "$(t M_DOC_DP_OLD)" "$(t M_DOC_DP_OLD_FIX)" \
       "$SCRIPT_DIR/scripts/theme.sh ember"
else
  ACTIVE=""
  bad "$(t M_DOC_DP_NONE)" "$(t M_DOC_DP_NONE_FIX)" \
      "$SCRIPT_DIR/scripts/theme.sh ember"
fi
if [ -n "$ACTIVE" ]; then
  GUID="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['Profiles'][0]['Guid'])" "$ACTIVE" 2>/dev/null)"
  NAME="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['Profiles'][0]['Name'])" "$ACTIVE" 2>/dev/null)"
  if [ -n "$GUID" ]; then ok "$(t M_DOC_DP_VALID "$NAME" "$GUID")"
  else bad "$(t M_DOC_DP_PARSE)" "$(t M_DOC_DP_PARSE_FIX "$ACTIVE")"; fi
  # Guid 唯一性：DynamicProfiles 里不能有第二个文件用同一 Guid（iTerm2 会整个拒载）
  if [ -n "$GUID" ]; then
    DUP="$(grep -l "$GUID" "$DP_DIR"/*.json 2>/dev/null | wc -l | tr -d ' ')"
    [ "$DUP" -gt 1 ] && bad "$(t M_DOC_DP_DUP "$DUP")" "$(t M_DOC_DP_DUP_FIX)"
  fi
  NTRIG="$(python3 -c "import json,sys;print(len(json.load(open(sys.argv[1]))['Profiles'][0].get('Triggers',[])))" "$ACTIVE" 2>/dev/null)"
  if [ -n "$NTRIG" ] && [ "$NTRIG" -ge 4 ]; then
    ok "$(t M_DOC_TRIG_OK "$NTRIG")"
  else
    warn "$(t M_DOC_TRIG_WARN)" "$(t M_DOC_TRIG_FIX)"
  fi
  # 语义交互层 v1：Smart Selection 产品规则 + Semantic History
  _SEM_META="$(python3 - "$ACTIVE" <<'PY' 2>/dev/null || true
import json,sys
p=json.load(open(sys.argv[1]))["Profiles"][0]
ss=p.get("Smart Selection Rules") or []
ours=[r.get("notes","") for r in ss if "hekouwang" in (r.get("notes") or "")]
sh=(p.get("Semantic History") or {}).get("action","")
print(f"{len(ours)}|{sh}|{'|'.join(ours)}")
PY
)"
  _SEM_N="${_SEM_META%%|*}"
  _SEM_REST="${_SEM_META#*|}"
  _SEM_SH="${_SEM_REST%%|*}"
  if [ -n "$_SEM_N" ] && [ "$_SEM_N" -ge 3 ] 2>/dev/null; then
    ok "$(t M_DOC_SEM_OK "$_SEM_N" "${_SEM_SH:-?}")"
  else
    warn "$(t M_DOC_SEM_WARN)" "$(t M_DOC_SEM_FIX)" \
         "$SCRIPT_DIR/scripts/theme.sh $(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || echo ember)")"
  fi
fi
DEF="$(defaults read "$DOMAIN" 'Default Bookmark Guid' 2>/dev/null || echo '')"
if [ -n "$GUID" ] && [ "$DEF" = "$GUID" ]; then ok "$(t M_DOC_DEFAULT_OK)"
else warn "$(t M_DOC_DEFAULT_WARN)" "$(t M_DOC_DEFAULT_FIX)" "$SCRIPT_DIR/scripts/setup-gui.sh"; fi

# ---- 4. GUI 关键设置 ----
sect "$(t M_DOC_S4)"
THEME="$(defaults read "$DOMAIN" TabStyleWithAutomaticOption 2>/dev/null || echo '')"
[ "$THEME" = "5" ] && ok "$(t M_DOC_MINIMAL_OK)" \
  || warn "$(t M_DOC_MINIMAL_WARN "${THEME:-$(t M_DOC_VALUE_DEFAULT)}")" "$(t M_DOC_RUN_SETUPGUI)" "$SCRIPT_DIR/scripts/setup-gui.sh"
if defaults read "$DOMAIN" GlobalKeyMap 2>/dev/null | grep -q '0xd-0x20000'; then
  ok "$(t M_DOC_SHIFTENTER_OK)"
else
  warn "$(t M_DOC_SHIFTENTER_WARN)" "$(t M_DOC_RUN_SETUPGUI)" "$SCRIPT_DIR/scripts/setup-gui.sh"
fi
# Cmd-click → Semantic History / URL（键名 CommandSelection，出厂默认 YES）
_CMDCLICK="$(defaults read "$DOMAIN" CommandSelection 2>/dev/null || echo '')"
case "$_CMDCLICK" in
  1|YES|Yes|yes|true|TRUE) ok "$(t M_DOC_CMDCLICK_OK)" ;;
  0|NO|No|no|false|FALSE)
    warn "$(t M_DOC_CMDCLICK_OFF)" "$(t M_DOC_CMDCLICK_FIX)" \
         "defaults write $DOMAIN CommandSelection -bool true" ;;
  *)
    # 键不存在 = 走 iTerm2 出厂默认 YES，不算故障
    ok "$(t M_DOC_CMDCLICK_DEFAULT)" ;;
esac
# 常用操作三项：复制即选 / 三击选整行（含折行）/ 标签页新输出指示
_COPY="$(defaults read "$DOMAIN" CopySelection 2>/dev/null || echo 0)"
_TRIPLE="$(defaults read "$DOMAIN" TripleClickSelectsFullWrappedLines 2>/dev/null || echo 0)"
_NEWOUT="$(defaults read "$DOMAIN" ShowNewOutputIndicator 2>/dev/null || echo 0)"
_COMMON_OFF=""
[ "$_COPY" = "1" ] || _COMMON_OFF="$_COMMON_OFF CopySelection"
[ "$_TRIPLE" = "1" ] || _COMMON_OFF="$_COMMON_OFF TripleClick"
[ "$_NEWOUT" = "1" ] || _COMMON_OFF="$_COMMON_OFF NewOutput"
if [ -z "$_COMMON_OFF" ]; then
  ok "$(t M_DOC_COMMON_OK)"
else
  warn "$(t M_DOC_COMMON_WARN "$_COMMON_OFF")" "$(t M_DOC_COMMON_FIX)" "$SCRIPT_DIR/scripts/setup-gui.sh"
fi
# AI CLI 主题检查需要用户用 --config 显式指定设置文件；doctor 不探测、不猜路径。

# ---- 5. 生态配色是否真的一致 ----
# 开源版只同步 iTerm2，多终端与生态是付费包能力 —— 缺了不是故障，别报警。
HAS_PRO=0
[ -f "$SCRIPT_DIR/config/themes/generators/pro.py" ] && HAS_PRO=1
# 1.x 版最典型的穿帮：终端切了 ember 暖橙黑，bat 还是 Catppuccin 紫蓝。
sect "$(t M_DOC_S5)"
if [ -f "$RUNTIME/current/colors.sh" ]; then
  # shellcheck disable=SC1091
  ECO_THEME="$(grep -m1 '^export HEKOUWANG_THEME=' "$RUNTIME/current/colors.sh" | cut -d'"' -f2)"
  ok "$(t M_DOC_ECO_OK "$ECO_THEME")"
  if [ -n "$GUID" ] && [ -n "${NAME:-}" ]; then
    ITERM_THEME="$(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || echo '')")"
    if [ -n "$ITERM_THEME" ] && [ "$ITERM_THEME" != "$ECO_THEME" ]; then
      warn "$(t M_DOC_ECO_MISMATCH "$ITERM_THEME" "$ECO_THEME")" \
           "$(t M_DOC_ECO_MISMATCH_FIX "$ITERM_THEME")" "$SCRIPT_DIR/scripts/theme.sh $ITERM_THEME"
    fi
  fi
  # bat 主题装没装
  # ⚠️ 必须查**当前这套**在不在，不能只查有没有 hekouwang-* ——
  #    装了付费包之后，缓存里躺着 3 套社区主题、当前用的品牌主题却没有，
  #    宽松的检查会一路绿灯，而 bat 正在静默回退默认主题（实测踩过）。
  if command -v bat >/dev/null 2>&1; then
    if bat --list-themes 2>/dev/null | grep -qx "hekouwang-$ECO_THEME"; then
      ok "$(t M_DOC_BAT_OK "$ECO_THEME")"
    elif bat --list-themes 2>/dev/null | grep -q "^hekouwang-"; then
      warn "$(t M_DOC_BAT_OTHER)" \
           "$(t M_DOC_BAT_OTHER_FIX "$ECO_THEME")" "$SCRIPT_DIR/scripts/theme.sh $ECO_THEME"
    else
      warn "$(t M_DOC_BAT_NONE)" \
           "$(t M_DOC_BAT_NONE_FIX)" "$SCRIPT_DIR/scripts/theme.sh $ECO_THEME"
    fi
  fi
  # git 有没有把 delta 配置挂上
  if git config --get-all include.path 2>/dev/null | grep -q hekouwang-terminal; then
    ok "$(t M_DOC_GIT_OK)"
  else
    warn "$(t M_DOC_GIT_WARN)" \
         "git config --global --add include.path ~/.config/hekouwang-terminal/current/delta.gitconfig" \
         "git config --global --add include.path $RUNTIME/current/delta.gitconfig"
  fi
  # macOS 自带终端
  # ⚠️ 别用 `defaults read` 的输出做字符串匹配：它对非 ASCII 的转义时灵时不灵
  #    （实测同一个值，有时原样输出中文，有时吐成 会勇… 和 \267），
  #    拿去和中文前缀比对会假性不匹配。走 plist 拿真值才稳。
  APPLE_DEF="$(python3 - <<'PY' 2>/dev/null || echo ''
import plistlib, subprocess
o = subprocess.run(['defaults', 'export', 'com.apple.Terminal', '-'], capture_output=True)
print(plistlib.loads(o.stdout).get('Default Window Settings', '') if o.stdout else '')
PY
)"
  # ⚠️ 自带终端的 Profile 名跟语言走（英文 "hekouwang · Ember" / 中文「会勇禾口王 · 暖烬」），
  #    所以「是不是我们写的」必须两个前缀都认，不能只认中文那个 —— 只认一个的话，
  #    换到另一种语言重装后，这里会报「自带终端还是原样」，而它其实已经同步好了。
  APPLE_OURS=0
  case "$APPLE_DEF" in
    会勇禾口王*|hekouwang*|Hekouwang*) APPLE_OURS=1 ;;
  esac
  if [ -z "$APPLE_DEF" ]; then
    [ "$QUIET" = "1" ] || printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_APPLE_NONE)"
  elif [ "$APPLE_OURS" = "1" ]; then
    ok "$(t M_DOC_APPLE_OK "$APPLE_DEF")"
    # ⚠️ 它只有一个字体字段，没有 iTerm2 那层 Symbols Nerd Font 兜底。
    #    配了不含图标的字体，ls 的文件夹图标会全变 ? 豆腐块，而且不报错。
    APPLE_FONT="$(python3 - <<'PY' 2>/dev/null || echo ''
import plistlib, subprocess
o = subprocess.run(['defaults', 'export', 'com.apple.Terminal', '-'], capture_output=True)
pl = plistlib.loads(o.stdout) if o.stdout else {}
p = pl.get('Window Settings', {}).get(pl.get('Default Window Settings', ''), {})
f = p.get('Font')
print(plistlib.loads(f)['$objects'][2] if f else '')
PY
)"
    FONT_POLICY="$(grep -m1 '^APPLE_TERMINAL_FONT=' "$SCRIPT_DIR/config/font.conf" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')"
    # 没有 font.conf（开源版）就读不到策略，无从判断这字体是不是刻意选的 —— 不猜、不报。
    if [ ! -f "$SCRIPT_DIR/config/font.conf" ]; then
      APPLE_FONT=""
    fi
    if [ -n "$APPLE_FONT" ]; then
      if grep -q "^${APPLE_FONT}|.*|nf|" "$SCRIPT_DIR/config/font.conf" 2>/dev/null; then
        ok "$(t M_DOC_APPLE_FONT_NF "$APPLE_FONT")"
      elif [ "${FONT_POLICY:-icons}" = "match" ]; then
        # match 策略下这是**故意的**：字体跟主字体统一，代价是没图标，
        # 而 .zshrc 已经据此在自带终端里关掉了 eza 的 --icons，不会出现 ? 方块。
        SOLO_NF_FLAG="$(grep -m1 '^export HEKOUWANG_SOLO_NF=' "$RUNTIME/current/colors.sh" 2>/dev/null | cut -d= -f2)"
        if [ "${SOLO_NF_FLAG:-1}" = "0" ]; then
          ok "$(t M_DOC_APPLE_FONT_MATCH "$APPLE_FONT")"
        else
          warn "$(t M_DOC_APPLE_FONT_MARK_WARN)" \
               "$(t M_DOC_APPLE_FONT_MARK_FIX "$ECO_THEME")" "$SCRIPT_DIR/scripts/theme.sh $ECO_THEME"
        fi
      else
        warn "$(t M_DOC_APPLE_FONT_NOICON "$APPLE_FONT")" \
             "$(t M_DOC_APPLE_FONT_NOICON_FIX "$ECO_THEME")" \
             "$SCRIPT_DIR/scripts/theme.sh $ECO_THEME"
      fi
    fi
  else
    warn "$(t M_DOC_APPLE_UNSYNCED "$APPLE_DEF")" \
         "$(t M_DOC_APPLE_UNSYNCED_FIX "$ECO_THEME")" \
         "$SCRIPT_DIR/scripts/theme.sh $ECO_THEME"
  fi
  # tmux
  if [ -f "$HOME/.tmux.conf" ] && grep -q hekouwang-terminal "$HOME/.tmux.conf" 2>/dev/null; then
    ok "$(t M_DOC_TMUX_OK)"
  else
    warn "$(t M_DOC_TMUX_WARN)" \
         "echo 'source-file ~/.config/hekouwang-terminal/current/tmux.conf' >> ~/.tmux.conf"
  fi
  # Ghostty：进程是否吃到最新 config（与状态机仪表盘同源判据，这里升级成 warn）
  if { [ -d "/Applications/Ghostty.app" ] || command -v ghostty >/dev/null 2>&1; } \
     && [ -f "$HOME/.config/ghostty/config" ]; then
    _gr="$(python3 - "$HOME/.config/ghostty/config" <<'PY' 2>/dev/null || echo ''
import os, sys, subprocess, time
cfg = sys.argv[1]
try:
    mtime = os.path.getmtime(cfg)
except OSError:
    print(""); raise SystemExit
hits = []
for line in subprocess.run(["ps","-axo","lstart=,comm="], capture_output=True, text=True).stdout.splitlines():
    line = line.rstrip()
    if not line.endswith("Ghostty"):
        continue
    stamp = line[: -len("Ghostty")].strip()
    try:
        hits.append(time.mktime(time.strptime(stamp, "%a %b %d %H:%M:%S %Y")))
    except ValueError:
        pass
if not hits:
    print("no-process")
elif max(hits) < mtime:
    print("reload")
else:
    print("ok")
PY
)"
    case "$_gr" in
      reload) warn "$(t M_DOC_GHOSTTY_RELOAD)" "$(t M_DOC_GHOSTTY_RELOAD_FIX)" ":manual:" ;;
      ok) ok "$(t M_DOC_GHOSTTY_OK)" ;;
    esac
  fi
elif [ "$HAS_PRO" = "0" ]; then
  [ "$QUIET" = "1" ] || {
    printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_OSS_ONLY1)"
    printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_OSS_ONLY2)"
    printf "  ${d}·${o} ${d}%s${o}\n" "$(t M_DOC_OSS_ONLY3)"
  }
else
  warn "$(t M_DOC_ECO_MISSING)" \
       "$(t M_DOC_ECO_MISSING_FIX)" "$SCRIPT_DIR/scripts/theme.sh ember"
fi

# ---- 6. ~/.zshrc 加载顺序 ----
sect "$(t M_DOC_S6)"
ZRC="$HOME/.zshrc"
if [ -f "$ZRC" ]; then
  ln_syntax="$(grep -n 'zsh-syntax-highlighting.zsh' "$ZRC" | tail -1 | cut -d: -f1)"
  ln_iterm="$(grep -n 'iterm2_shell_integration' "$ZRC" | tail -1 | cut -d: -f1)"
  ln_starship="$(grep -n 'starship init' "$ZRC" | tail -1 | cut -d: -f1)"
  [ -n "$ln_starship" ] && ok "$(t M_DOC_STARSHIP_OK)" \
    || warn "$(t M_DOC_STARSHIP_WARN)" "$(t M_DOC_STARSHIP_FIX)"
  if [ -n "$ln_syntax" ] && [ -n "$ln_starship" ] && [ "$ln_syntax" -gt "$ln_starship" ]; then
    ok "$(t M_DOC_SYNTAX_OK)"
  elif [ -n "$ln_syntax" ]; then
    warn "$(t M_DOC_SYNTAX_WARN)" "$(t M_DOC_SYNTAX_FIX)"
  fi
  if [ -n "$ln_iterm" ] && [ -n "$ln_syntax" ] && [ "$ln_iterm" -lt "$ln_syntax" ]; then
    warn "$(t M_DOC_ITERM_ORDER_WARN)" "$(t M_DOC_ITERM_ORDER_FIX)"
  fi
  if grep -q 'hekouwang-terminal/current/colors.sh' "$ZRC"; then
    ok "$(t M_DOC_COLORS_OK)"
  else
    warn "$(t M_DOC_COLORS_WARN)" "$(t M_DOC_COLORS_FIX)"
  fi
  nodemgrs=0
  # 扫 .zshrc / .zshrc.local / runtime node.sh —— 多套同时出现才算冲突
  _node_scan="$ZRC"
  [ -f "$HOME/.zshrc.local" ] && _node_scan="$_node_scan $HOME/.zshrc.local"
  [ -f "$HOME/.config/hekouwang-terminal/node.sh" ] \
    && _node_scan="$_node_scan $HOME/.config/hekouwang-terminal/node.sh"
  # shellcheck disable=SC2086
  grep -qE 'fnm[[:space:]]+env|fnm env' $_node_scan 2>/dev/null && nodemgrs=$((nodemgrs+1))
  # shellcheck disable=SC2086
  grep -qE 'NVM_DIR|nvm\.sh' $_node_scan 2>/dev/null && nodemgrs=$((nodemgrs+1))
  # shellcheck disable=SC2086
  grep -qE 'vfox[[:space:]]+activate|vfox activate' $_node_scan 2>/dev/null && nodemgrs=$((nodemgrs+1))
  # brew node：只认明确的 opt/node 路径，避免误伤无关 PATH 行
  # shellcheck disable=SC2086
  grep -qE 'opt/node(/bin)?|brew --prefix node' $_node_scan 2>/dev/null && nodemgrs=$((nodemgrs+1))
  if [ "$nodemgrs" -gt 1 ]; then
    warn "$(t M_DOC_NODE_WARN)" "$(t M_DOC_NODE_FIX)"
  else ok "$(t M_DOC_NODE_OK)"; fi
else
  bad "$(t M_DOC_ZSHRC_MISSING)" "$(t M_DOC_ZSHRC_MISSING_FIX)"
fi

# ---- 7. 启动耗时 ----
# 「终端一开要等两秒」是最常见也最烦人的问题，但光看配置看不出来是谁慢。
# 跑 7 次取中位数（第一次有磁盘缓存影响，别只跑一次就下结论）。
sect "$(t M_DOC_S7)"
if command -v zsh >/dev/null 2>&1; then
  MS="$(python3 - <<'PY'
import subprocess, time, statistics, os
t = []
for _ in range(7):
    s = time.perf_counter()
    subprocess.run(['zsh', '-i', '-c', 'exit'], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, env={**os.environ, 'ZDOTDIR': os.path.expanduser('~')})
    t.append((time.perf_counter() - s) * 1000)
print(int(statistics.median(t)))
PY
)"
  if [ -z "$MS" ]; then
    warn "$(t M_DOC_START_FAIL)" "$(t M_DOC_START_FAIL_FIX)"
  elif [ "$MS" -lt 300 ]; then
    ok "$(t M_DOC_START_FAST "$MS")"
  elif [ "$MS" -lt 600 ]; then
    warn "$(t M_DOC_START_SLOW "$MS")" "$(t M_DOC_START_SLOW_FIX)"
  else
    bad "$(t M_DOC_START_BAD "$MS")" "$(t M_DOC_START_BAD_FIX)"
  fi
  # --profile：用 zprof 把耗时前几名点名，别只说「慢」
  if [ "${1:-}" = "--profile" ] || printf '%s\n' "$@" | grep -q -- '--profile'; then
    sect "$(t M_DOC_S7B)"
    PROF_DIR="$(mktemp -d)"
    cat > "$PROF_DIR/.zshrc" <<PROFRC
zmodload zsh/zprof
source "$HOME/.zshrc"
zprof
PROFRC
    ZDOTDIR="$PROF_DIR" zsh -i -c exit 2>/dev/null \
      | grep -E '^\s*[0-9]+\)' | head -8 | sed 's/^/  /'
    rm -rf "$PROF_DIR"
    printf "  ${d}%s${o}\n" "$(t M_DOC_PROF_LEGEND)"
  fi
fi

# ---- 8. Shell 集成 ----
sect "$(t M_DOC_S8)"
# 官方脚本，执行前可先审阅：先下载到 /tmp 并显示路径，确认后再执行。
[ -f "$HOME/.iterm2_shell_integration.zsh" ] && ok "$(t M_DOC_SI_OK)" \
  || warn "$(t M_DOC_SI_WARN)" \
          "curl -L -o /tmp/iterm2-shell-integration.sh https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh && echo 已保存到：/tmp/iterm2-shell-integration.sh（官方脚本，已下载未执行；审阅后自行运行 bash /tmp/iterm2-shell-integration.sh）"

# ---- 汇总 ----
if [ "$QUIET" = "1" ]; then
  printf "doctor: fail=%d warn=%d\n" "$FAIL" "$WARN"
  [ "$FAIL" -eq 0 ] && exit 0 || exit 1
fi
printf "\n${b}%s${o}\n" "$(t M_DOC_RESULT)"
if [ "$FAIL" -eq 0 ] && [ "$WARN" -eq 0 ]; then
  printf "${g}%s${o}\n" "$(t M_DOC_ALL_PASS)"
elif [ "$FAIL" -eq 0 ]; then
  printf "${y}%s${o}\n" "$(t M_DOC_WARN_ONLY "$WARN")"
else
  printf "${r}%s${o}  ${y}%s${o}\n" "$(t M_DOC_FAIL_N "$FAIL")" "$(t M_DOC_WARN_N "$WARN")"
fi

# ---- 付费档在哪儿（开源版才打）----
# 体检跑完是用户主动来确认「我这套是好的」的时刻，顺带告诉他还有一档能力在哪儿。
# ⚠️ HKW_NO_PROMO：install.sh 里会调一次 doctor，紧接着自己的收尾也打同一句 ——
#    十行之内出现两次广告，人只会学会无视它。装机路径上让 install.sh 那句说，
#    这里闭嘴。⛔ 别把这条去掉图省事。
if [ -z "${HKW_NO_PROMO:-}" ] && [ ! -f "$SCRIPT_DIR/config/themes/_apply_pro.sh" ] \
   && [ -n "${HKW_URL_BUY:-}" ]; then
  printf "${d}%s${o}\n" "$(t M_DOC_PAID_HINT "$HKW_URL_BUY")"
fi

# ---- --fix：按组问，每项先说清楚要跑什么 ----
if [ "$FIX" = "1" ] && [ "${#FIXES[@]}" -gt 0 ]; then
  printf "\n${b}%s${o}\n" "$(t M_DOC_FIX_HEAD)"
  printf "${d}%s${o}\n" "$(t M_DOC_FIX_GROUP_HINT)"
  _fix_order="node auto optical scene reload gui theme other"
  for _g in $_fix_order; do
    _group_has=0
    for entry in "${FIXES[@]}"; do
      item="${entry%%|*}"; cmd="${entry#*|}"
      [ "$(fix_group_of "$cmd" "$item")" = "$_g" ] || continue
      if [ "$_group_has" = "0" ]; then
        printf "\n${b}── %s ──${o}\n" "$(t "M_DOC_FIX_G_$_g")"
        _group_has=1
      fi
      printf "\n  ${y}%s${o} %s\n" "$(t M_DOC_FIX_ITEM)" "$item"
      if [[ "$cmd" == :manual:* ]]; then
        printf "  ${d}%s${o}\n" "$(t M_DOC_FIX_MANUAL)"
      else
        printf "  ${d}%s${o}\n" "$(t M_DOC_FIX_CMD "$cmd")"
      fi
      printf "  ${y}?${o} %s%s" "$(t M_DOC_FIX_ASK)" "$(t M_YES_NO)"
      read -r a </dev/tty || a=""
      if [[ "$a" =~ ^[Yy] ]]; then
        if [[ "$cmd" == :manual:* ]]; then
          printf "  ${g}%s${o}\n" "$(t M_DOC_FIX_MANUAL_OK)"
        else
          # shellcheck disable=SC2086
          eval "$cmd" && printf "  ${g}%s${o}\n" "$(t M_DONE_EXEC)" || printf "  ${r}%s${o}\n" "$(t M_FAILED_EXEC)"
        fi
      else
        printf "  ${d}%s${o}\n" "$(t M_SKIPPED)"
      fi
    done
  done
  printf "\n${d}%s${o}\n" "$(t M_DOC_FIX_RECHECK)"
elif [ "$FIX" = "0" ] && [ "${#FIXES[@]}" -gt 0 ]; then
  printf "${d}%s${o}\n" "$(t M_DOC_FIX_HINT "${#FIXES[@]}")"
fi

[ "$FAIL" -eq 0 ] && exit 0 || exit 1
