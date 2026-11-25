#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 一键换肤（终端 + 整条工具链）
#
# ⚠️ 对外文案（help / 画廊提示 / 换肤回执）全在 lib/i18n/{en,zh}/theme.sh，这里只留逻辑。
#
# 原理：所有 iTerm2 主题共享同一个 Guid，切主题只是把对应 JSON 拷成
# 「当前激活主题」文件；iTerm2 监听 DynamicProfiles 目录，保存即生效。
# 生态那半边是把 ecosystem/<主题>/ 拷进 ~/.config/hekouwang-terminal/current/，
# .zshrc 固定 source 那个固定路径，所以 .zshrc 一行都不用动。
# ============================================================
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init theme "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/transaction.sh"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/aliases.sh"
THEMES_DIR="$SCRIPT_DIR/config/themes"
ECO_DIR="$THEMES_DIR/ecosystem"
DP_DIR="$HOME/Library/Application Support/iTerm2/DynamicProfiles"
ACTIVE="$DP_DIR/hekouwang-active-theme.json"
GHOSTTY_CFG="$HOME/.config/ghostty/config"
GHOSTTY_THEMES="$HOME/.config/ghostty/themes"
WARP_THEMES="$HOME/.warp/themes"
RUNTIME="$HOME/.config/hekouwang-terminal"
CURRENT="$RUNTIME/current"

c_purple='\033[1;35m'; c_dim='\033[2m'; c_off='\033[0m'
c_ok='\033[32m'; c_bold='\033[1m'
say()  { printf "${c_purple}%s${c_off}\n" "$(t "$@")"; }
dim()  { printf "${c_dim}%s${c_off}\n" "$(t "$@")"; }

# ---- 换肤回执 -------------------------------------------------
# 为什么先攒后印：一次换肤要动 iTerm2 / Ghostty / Warp / 自带终端 / 工具链 / 字体
# 六件事，边做边打就是一堵没有层次的平墙（1.x 就是那样）。攒成分组回执再一次印出来。
#
# ⚠️ 行内**不做定宽对齐**（不用 printf %-Ns）：bash 的 printf 按字节数补齐，
#    「macOS 自带终端」这种中文标题一定会歪。要对齐的只有抬头那一行，
#    那行交给 _preview.py --banner 出（Python 那边按显示宽度算）。
#
# ⚠️ 颜色转义必须待在 printf 的**格式串**里，不能塞进 %s 的参数：
#    c_dim 存的是字面量 \033[2m，printf 只解释格式串里的转义，
#    从参数进来的会原样打印成一串 "\033[2m"（写第一版时就是这么翻的车）。
RECEIPT=()
r_sec()  { RECEIPT+=("" "$(printf "  ${c_dim}%s${c_off}" "$1")"); }
r_ok()   { RECEIPT+=("$(printf "    ${c_ok}✓${c_off} %s${c_dim}%s${c_off}" "$1" "${2:+   $2}")"); }
r_skip() { RECEIPT+=("$(printf "    ${c_dim}· %s%s${c_off}" "$1" "${2:+   $2}")"); }
r_note() { RECEIPT+=("$(printf "      ${c_dim}%s${c_off}" "$1")"); }
r_flush() {
  local l
  for l in "${RECEIPT[@]}"; do printf '%s\n' "$l"; done
  RECEIPT=()
}

# 画廊 / 预览 / 抬头都走同一个渲染器；它不在或跑挂了就退回纯文字，不让换肤失败
PREVIEW="$THEMES_DIR/_preview.py"
render() {   # render <模式> [参数…] → 成功返回 0
  [ -f "$PREVIEW" ] || return 1
  python3 "$PREVIEW" "$@" 2>/dev/null || return 1
}

theme_display() {
  python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['Profiles'][0]['Name'])" "$1" 2>/dev/null \
    || basename "$1" .json
}

# 这个 .json 是不是「一套主题」？
# ⛔ 目录里还躺着同后缀的**非主题**文件：names.json（显示名边表）、minimal.json（无配色骨架）。
#    直接按 *.json 枚举会把它们当主题列出来，甚至 `./scripts/theme.sh names` 真能切过去
#    （2026-07-23 加 names.json 后实测到，列表里凭空多出一套「names」）。
#    判据用「文件里有没有 Profiles 数组」，不用文件名黑名单 —— 以后再加边表不用回来改这儿。
is_theme_json() {
  [ -f "$1" ] && grep -q '"Profiles"' "$1"
}

is_light() {   # 主题是不是亮底：读生态文件里的标记，不猜
  [ -f "$ECO_DIR/$1/colors.sh" ] && grep -q 'HEKOUWANG_THEME_IS_LIGHT="1"' "$ECO_DIR/$1/colors.sh"
}

# ---- 字体：按 config/font.conf 的优先级探测本机实际装了哪套 ----
# 为什么要探测而不是写死：好看的等宽字体里有一批是商业字体（Operator Mono 等），
# 本套装**不分发任何字体文件**——你自己买过授权装在本机上，这里就自动用上；
# 没有的人自动落到免费字体。顺带还挡掉「字体名写错→静默回退系统字体」这个坑。
# 输出：PostScript名|family名|Ghostty的font-style
# $1 = "nf" 时只认自带 Nerd 图标的字体（给单字体终端用），留空则第一个装了的就行
# $2 = 可选，强制指定 PostScript 名（./scripts/theme.sh <主题> --font 或 ./scripts/font.sh apply）
resolve_font() {
  local need_nf="${1:-}" force_ps="${2:-}" conf="$SCRIPT_DIR/config/font.conf" ps fam style nf _note file_name d ext
  if [ -f "$conf" ]; then
    while IFS='|' read -r ps fam style nf _note file_name; do
      ps="${ps#"${ps%%[![:space:]]*}"}"; ps="${ps%"${ps##*[![:space:]]}"}"
      case "$ps" in ''|'#'*) continue ;; esac
      fam="${fam#"${fam%%[![:space:]]*}"}"; fam="${fam%"${fam##*[![:space:]]}"}"
      style="${style#"${style%%[![:space:]]*}"}"; style="${style%"${style##*[![:space:]]}"}"
      nf="$(printf '%s' "${nf:-}" | tr -d '[:space:]')"
      # 强制指定时：命中 PostScript 名就返回（仍要求文件真的在）
      if [ -n "$force_ps" ] && [ "$ps" != "$force_ps" ]; then
        continue
      fi
      # 要求自带图标时，跳过没标 nf 的
      [ "$need_nf" = "nf" ] && [ "$nf" != "nf" ] && continue
      for d in "$HOME/Library/Fonts" "/Library/Fonts" "/System/Library/Fonts"; do
        for ext in otf ttf ttc; do
          if [ -f "$d/$ps.$ext" ]; then
            printf '%s|%s|%s\n' "$ps" "$fam" "$style"; return 0
          fi
        done
        # A few web fonts use a human-readable file name rather than their
        # PostScript name. The optional sixth column preserves exact detection.
        if [ -n "${file_name:-}" ] && [ -f "$d/$file_name" ]; then
          printf '%s|%s|%s\n' "$ps" "$fam" "$style"; return 0
        fi
      done
      # 强制指定但文件不在：继续找，别静默成功
      if [ -n "$force_ps" ]; then
        continue
      fi
    done < "$conf"
  fi
  # font.conf 不在（开源版）或一套都没装：用推荐默认字体。
  # Maple Mono NF CN 是安全默认 —— SIL OFL 免费可商用、自带 Nerd 图标、中文等宽，
  # 单字体/双字体两种终端都能用。想按优先级自动认出自购的商业字体（Operator Mono 等），
  # 那张表在付费包里。
  if [ -n "$force_ps" ]; then
    # 强制名不在表里 / 没装上：仍按名写出去，family 退化成 PostScript 名（总比悄悄换字体好）
    printf '%s|%s|\n' "$force_ps" "$force_ps"
    return 0
  fi
  printf '%s|%s|\n' "MapleMono-NF-CN-Regular" "Maple Mono NF CN"
}

current_theme() {   # 当前激活的是哪套
  # ⛔ 别用 `cmp -s <仓库里的 json> <激活的 json>` —— apply() 会把本机探测到的字体
  #    写进激活的那份，两个文件从此永远不相等，「← 当前」永远不显示（1.x 就是这个哑 bug，
  #    而且 set -e 下这个函数返回 1 会把整个 list 干掉，表现是**一行都不打**）。
  #    真相源是 apply() 落的 $RUNTIME/theme；它不在时退回比对 Profile 的 Name 字段。
  local f n
  if [ -f "$RUNTIME/theme" ]; then
    n="$(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || true)")"
    [ -n "$n" ] && [ -f "$THEMES_DIR/$n.json" ] && { printf '%s\n' "$n"; return 0; }
  fi
  [ -f "$ACTIVE" ] || return 0
  n="$(theme_display "$ACTIVE")"
  for f in "$THEMES_DIR"/*.json; do
    is_theme_json "$f" || continue
    [ "$(theme_display "$f")" = "$n" ] && { basename "$f" .json; return 0; }
  done
  return 0
}

theme_names() {   # stdout：每行一个可 apply 的主题名
  local f
  for f in "$THEMES_DIR"/*.json; do
    is_theme_json "$f" || continue
    basename "$f" .json
  done
}

list() {
  local cur; cur="$(current_theme)"
  # 主路：带真彩色色条的画廊。卖配色的东西，列表里必须能看见颜色。
  if ! render --gallery ${cur:+--current "$cur"}; then
    # 退路：渲染器不在（或 python3 没了）时的纯文字列表，功能一条不少
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_LIST_TITLE)"
    for f in "$THEMES_DIR"/*.json; do
      is_theme_json "$f" || continue
      name="$(basename "$f" .json)"
      mark=""; [ "$name" = "$cur" ] && mark=" ${c_purple}$(t M_THEME_CURRENT)${c_off}"
      tone="$(t M_THEME_TONE_DARK)"; is_light "$name" && tone="$(t M_THEME_TONE_LIGHT)"
      # ⚠️ 显示名可能是中文（「会勇禾口王 · Ember 暖烬」），不能用 %-26s 补 —— 按字节补必歪
      printf "  ${c_dim}%-16s${c_off} %s${c_dim}%s${c_off}%b\n" \
        "$name" "$(hkw_pad "$(theme_display "$f")" 26)" "$tone" "$mark"
    done
    echo
  fi

  printf "  ${c_dim}%s${c_off}./scripts/theme.sh <name>${c_dim}%s${c_off}./scripts/theme.sh --preview <name>${c_dim}%s${c_off}./scripts/theme.sh --gallery\n" \
    "$(t M_THEME_HINT_SWITCH)" "$(t M_THEME_HINT_PREVIEW)" "$(t M_THEME_HINT_GALLERY)"
  if command -v fzf >/dev/null 2>&1; then
    printf "  ${c_dim}%s${c_off}./scripts/theme.sh --pick${c_dim}%s${c_off}\n" \
      "$(t M_THEME_HINT_PICK)" "$(t M_THEME_HINT_PICK_HOW)"
  fi
  printf "${c_off}\n"
}

# fzf 模糊选主题；右侧 ANSI 整块预览（直接调 _preview.py，不经 theme.sh 以免递归）
# 没有 fzf / 非 tty → 退回画廊 list，不报错。
pick() {
  local cur chosen preview_cmd
  cur="$(current_theme)"
  if ! command -v fzf >/dev/null 2>&1 || [ ! -t 0 ]; then
    [ -t 0 ] || dim M_THEME_PICK_NO_TTY
    command -v fzf >/dev/null 2>&1 || dim M_THEME_PICK_NO_FZF
    list
    return 0
  fi
  preview_cmd="python3 \"$PREVIEW\" --card {}"
  [ -f "$PREVIEW" ] || preview_cmd="echo '(preview renderer missing)'"
  # --ansi：预览里的真彩色别被 fzf 吃掉
  chosen="$(
    theme_names | fzf \
      --ansi \
      --prompt="$(t M_THEME_PICK_PROMPT) " \
      --header="$(t M_THEME_PICK_HEADER "${cur:-?}")" \
      --preview="$preview_cmd" \
      --preview-window='right,70%,border-left' \
      --height=90% \
      --bind='ctrl-/:toggle-preview' \
      ${cur:+--query="$cur"}
  )" || true
  if [ -z "${chosen:-}" ]; then
    dim M_THEME_PICK_ABORT
    return 0
  fi
  apply "$chosen"
}

# 整块「假终端」预览：提示符 / eza / git diff / 语法高亮 / 错误标色全在一张图里。
# 这是给付费仓截主题图的那把工具 —— 用真彩色画，跟当前终端用的是哪套主题无关。
preview() {
  local name="$1"
  if [ -z "$name" ]; then
    printf "${c_purple}%s${c_off}  ./scripts/theme.sh --preview ember\n\n" "$(t M_THEME_PREVIEW_WHICH)"; list; exit 1
  fi
  render --card "$name" || {
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_PREVIEW_FAIL)"
    dim M_THEME_PREVIEW_NEED "$name"
    exit 1
  }
}

gallery_all() {   # 七套连着渲染，一次截完整套图
  local f name
  for f in "$THEMES_DIR"/*.json; do
    is_theme_json "$f" || continue
    name="$(basename "$f" .json)"
    render --card "$name" || true
  done
}

# ---- 真正的切换动作 ----------------------------------------
# FORCE_FONT：可选，由 ./scripts/theme.sh <主题> --font <PostScript名> 或 ./scripts/font.sh apply 传入
FORCE_FONT="${FORCE_FONT:-}"

apply_impl() {
  local theme="$1" src="$THEMES_DIR/$1.json"
  # 非主题的 .json（names/minimal）当成「没有这套主题」，别真去 apply
  if ! is_theme_json "$src"; then
    printf "${c_purple}%s${c_off}\n\n" "$(t M_THEME_NO_SUCH "$theme")"; list; exit 1
  fi


  # 0. 先定字体。分两套：
  #    · 主字体      给 iTerm2 / Ghostty —— 它们有「主字体 + Symbols Nerd Font 兜底」两层，
  #                  所以可以用不含图标的商业字体（如 Operator Mono）
  #    · 单字体      给 macOS 自带终端 —— 它**只有一个字体字段**，没有兜底层，
  #                  必须选自带 Nerd 图标的那套，否则 ls 的图标全变 ? 豆腐块（实测踩过）
  local FONT_PS FONT_FAM FONT_STYLE SOLO_PS SOLO_FAM SOLO_NF FONT_POLICY THEME_FONT_OVERRIDE EXPLICIT_FONT
  local ECO_STATE="missing" ECO_TMUX="" WS_OK="" OPTICAL_NOTE="" SCENE_NOTE=""
  RECEIPT=()
  EXPLICIT_FONT="${FORCE_FONT:-}"
  # 终端光学校准引擎：若用户 ./scripts/font.sh apply 钉过字体，且本机装了，换肤时优先用它
  # （否则 font.conf 优先级会把 Operator 盖过刚钉住的 maple，光学档与字体错位）
  if [ -z "${FORCE_FONT:-}" ] && [ -f "$SCRIPT_DIR/config/typography/_engine.py" ] \
     && [ -f "$HOME/.config/hekouwang-terminal/typography" ]; then
    _pin_id="$(grep -m1 '^FONT_ID=' "$HOME/.config/hekouwang-terminal/typography" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')"
    if [ -n "$_pin_id" ]; then
      _pin_ps="$(python3 "$SCRIPT_DIR/config/typography/_engine.py" ps-for "$_pin_id" 2>/dev/null || true)"
      if [ -n "$_pin_ps" ]; then
        _hit=""
        for _d in "$HOME/Library/Fonts" "/Library/Fonts" "/System/Library/Fonts"; do
          for _e in otf ttf ttc; do
            [ -f "$_d/$_pin_ps.$_e" ] && _hit=1 && break 2
          done
        done
        [ -n "$_hit" ] && FORCE_FONT="$_pin_ps"
      fi
    fi
  fi
  # A theme may opt into a specific installed font. Explicit --font still wins;
  # the theme override intentionally takes precedence over a global pinned font.
  THEME_FONT_OVERRIDE="$(python3 - "$src" <<'PY'
import json, sys
try:
    print(json.load(open(sys.argv[1], encoding="utf-8"))["Profiles"][0].get("Hekouwang Font Override", ""))
except (OSError, ValueError, KeyError, IndexError):
    pass
PY
)"
  if [ -z "$EXPLICIT_FONT" ] && [ -n "$THEME_FONT_OVERRIDE" ]; then
    FORCE_FONT="$THEME_FONT_OVERRIDE"
  fi
  IFS='|' read -r FONT_PS FONT_FAM FONT_STYLE <<<"$(resolve_font "" "${FORCE_FONT:-}")"
  IFS='|' read -r SOLO_PS SOLO_FAM _ <<<"$(resolve_font nf)"
  SOLO_NF=1
  # 策略见 config/font.conf 的 APPLE_TERMINAL_FONT
  FONT_POLICY="$(grep -m1 '^APPLE_TERMINAL_FONT=' "$SCRIPT_DIR/config/font.conf" 2>/dev/null | cut -d= -f2 | tr -d '[:space:]')"
  if [ "${FONT_POLICY:-icons}" = "match" ]; then
    SOLO_PS="$FONT_PS"; SOLO_FAM="$FONT_FAM"
    # 主字体自己含不含图标？含就还是 1，不含就置 0（.zshrc 据此在自带终端里去掉 ls 图标）
    grep -q "^${FONT_PS}|.*|nf|" "$SCRIPT_DIR/config/font.conf" 2>/dev/null || SOLO_NF=0
  fi

  # 1. iTerm2 —— 换激活文件，Guid 不变，默认 Profile 绑定不断
  mkdir -p "$DP_DIR"
  rm -f "$DP_DIR/catppuccin-mocha.json"   # 清历史单文件，避免撞 Guid 被 iTerm2 拒载
  cp "$src" "$ACTIVE"
  # 把探测到的字体写进这份**部署出去的** Profile（仓库里那份保持默认，
  # 这样每台机器用各自装了的字体，仓库不用为谁改一次）
  python3 - "$ACTIVE" "$FONT_PS" "$THEMES_DIR/names.json" "$theme" <<'PY'
import json, os, sys
path, ps, names_path, theme = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
d = json.load(open(path, encoding='utf-8'))
prof = d['Profiles'][0]
size = prof.get('Normal Font', 'x 15').rsplit(' ', 1)[-1]
prof['Normal Font'] = f'{ps} {size}'
# Profile 显示名跟语言走：仓库里的产物一律烧英文名（公开仓要对英文用户成立），
# 中文名在**部署这一刻**注入。所以两种语言共用一套产物，不会有两份互相漂的 JSON。
try:
    entry = json.load(open(names_path, encoding='utf-8')).get(theme) or {}
    prof['Name'] = entry.get(os.environ.get('HKW_LANG', 'en')) or entry.get('en') or prof['Name']
except (OSError, ValueError):
    pass
json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
PY
  # ⭐ 免费版默认品牌水印：没有场景引擎时，部署 Profile 一律写 hekouwang。
  #    付费包有 scenes/_engine.py，水印改由场景 / scene.sh badge 管（日常默认可干净）。
  #    Alpha 提到 0.55：生成器默认 0.30 在深色底上几乎看不见。
  if [ ! -f "$SCRIPT_DIR/config/scenes/_engine.py" ]; then
    python3 - "$ACTIVE" <<'PY'
import json, sys
path = sys.argv[1]
d = json.load(open(path, encoding="utf-8"))
prof = d["Profiles"][0]
prof["Badge Text"] = "hekouwang"
bc = dict(prof.get("Badge Color") or {})
if bc:
    bc["Alpha Component"] = 0.55
    prof["Badge Color"] = bc
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
  fi
  # ⭐ 终端光学校准引擎：字号/行距/Thin Strokes 按光学档覆写（付费）
  #    仓库 JSON 仍保持生成器默认；只动部署出去的激活 Profile。
  if [ -f "$SCRIPT_DIR/config/typography/_engine.py" ]; then
    if python3 "$SCRIPT_DIR/config/typography/_engine.py" apply-iterm "$ACTIVE" --ps "$FONT_PS" >/dev/null; then
      OPTICAL_NOTE="$(python3 "$SCRIPT_DIR/config/typography/_engine.py" resolve --ps "$FONT_PS" 2>/dev/null \
        | python3 -c 'import sys,json;d=json.load(sys.stdin);print("%s@%s"% (d["id"],d["density"]))' 2>/dev/null || true)"
    fi
  fi
  # ⭐ 场景美学引擎：透明度/毛玻璃/窗尺寸/徽章/隐私（付费）
  #    若场景要求 optical_density=present，再叠一次光学档（不改钉住，只覆盖本次部署）。
  if [ -f "$SCRIPT_DIR/config/scenes/_engine.py" ]; then
    if python3 "$SCRIPT_DIR/config/scenes/_engine.py" apply-iterm "$ACTIVE" >/dev/null; then
      SCENE_NOTE="$(python3 "$SCRIPT_DIR/config/scenes/_engine.py" resolve 2>/dev/null \
        | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("id",""))' 2>/dev/null || true)"
      _scene_dens="$(python3 "$SCRIPT_DIR/config/scenes/_engine.py" resolve 2>/dev/null \
        | python3 -c 'import sys,json;d=json.load(sys.stdin);print(d.get("optical_density") or "")' 2>/dev/null || true)"
      if [ -n "$_scene_dens" ] && [ -f "$SCRIPT_DIR/config/typography/_engine.py" ]; then
        if python3 "$SCRIPT_DIR/config/typography/_engine.py" apply-iterm "$ACTIVE" --ps "$FONT_PS" --density "$_scene_dens" >/dev/null; then
          OPTICAL_NOTE="$(python3 "$SCRIPT_DIR/config/typography/_engine.py" resolve --ps "$FONT_PS" --density "$_scene_dens" 2>/dev/null \
            | python3 -c 'import sys,json;d=json.load(sys.stdin);print("%s@%s"% (d["id"],d["density"]))' 2>/dev/null || true)"
        fi
      fi
    fi
  fi
  # 记下「当前是哪套」。⚠️ 这一行必须在生态层的 if 之外 —— 它以前埋在
  # 「付费生态件在不在」那个分支里，开源版换完肤 current_theme() 就问不出答案了。
  mkdir -p "$RUNTIME"
  printf '%s\n' "$theme" > "$RUNTIME/theme"
  # P3 广色域：只改部署出去的 Profile，仓库 JSON 保持 sRGB；Ghostty 侧在 _apply_pro.sh 里选 -p3 主题
  P3_NOTE=""
  if [ "${HKW_P3:-0}" = "1" ] && [ -f "$THEMES_DIR/_p3.py" ]; then
    if python3 "$THEMES_DIR/_p3.py" "$ACTIVE" >/dev/null 2>&1; then
      printf '1\n' > "$RUNTIME/p3"
      P3_NOTE=" · P3"
    else
      rm -f "$RUNTIME/p3"
      export HKW_P3=0
    fi
  else
    rm -f "$RUNTIME/p3"
    export HKW_P3=0
  fi

  r_sec "$(t M_THEME_SEC_TERMINAL)"
  if [ -n "$OPTICAL_NOTE" ] && [ -n "$SCENE_NOTE" ]; then
    r_ok "iTerm2" "$(t M_THEME_ITERM_FONT "$FONT_FAM") · $OPTICAL_NOTE · scene=$SCENE_NOTE$P3_NOTE"
  elif [ -n "$OPTICAL_NOTE" ]; then
    r_ok "iTerm2" "$(t M_THEME_ITERM_FONT "$FONT_FAM") · $OPTICAL_NOTE$P3_NOTE"
  elif [ -n "$SCENE_NOTE" ]; then
    r_ok "iTerm2" "$(t M_THEME_ITERM_FONT "$FONT_FAM") · scene=$SCENE_NOTE$P3_NOTE"
  else
    r_ok "iTerm2" "$(t M_THEME_ITERM_FONT "$FONT_FAM")$P3_NOTE"
  fi
  r_note "$(t M_THEME_ITERM_NOTE)"

  # ---- 2–5：多终端 + 全生态 ----------------------------------
  # ⭐付费：Ghostty / Warp / macOS 自带终端 / bat / fzf / eza / git diff / tmux。
  # 用 source 不用子进程 —— 这段跟 apply() 共享十几个局部变量（字体、路径、回执数组）。
  if [ -f "$THEMES_DIR/_apply_pro.sh" ]; then
    . "$THEMES_DIR/_apply_pro.sh"
  else
    # 只报多终端这一段 —— 工具链那段回执下面本来就有（ECO_STATE 保持 missing 即可），
    # 两边都报会出现两个「工具链」标题。
    r_sec "$(t M_THEME_SEC_MULTI)"
    r_skip "$(t M_THEME_MULTI_ITEMS)" "$(t M_THEME_PAID_ONLY)"
  fi


  # ---- 出回执 ------------------------------------------------
  # 工具链一段在这里补（见上面「只记事实」那条注释）
  r_sec "$(t M_THEME_SEC_TOOLCHAIN)"
  if [ "$ECO_STATE" = "ok" ]; then
    r_ok "$(t M_THEME_ECO_ITEMS)" "$(t M_THEME_ECO_SAME)"
    r_note "$(t M_THEME_ECO_NOTE)"
    [ -n "$ECO_TMUX" ] && r_note "$(t M_THEME_ECO_TMUX)"
  else
    r_skip "$(t M_THEME_ECO_ITEMS)" "$(t M_THEME_ECO_DEFAULT)"
    r_note "$(t M_THEME_ECO_PAID_NOTE)"
  fi
  [ -n "$WS_OK" ] && r_ok "$(t M_THEME_WS_OK)" "$(t M_THEME_WS_REBUILT)"

  echo
  render --banner "$theme" || printf "  ${c_bold}%s${c_off}\n" "$(theme_display "$src")"
  r_flush
  echo
  printf "  ${c_dim}%s${c_off}./scripts/theme.sh --preview %s\n" "$(t M_THEME_SEE_IT)" "$theme"
  # ---- 付费档在哪儿 ------------------------------------------
  # 上面的回执已经把「多终端 / 工具链」那两行标成跳过了，但它没说去哪儿拿 ——
  # 用户刚看到换肤生效、正上头的这三秒是全链路最容易掏钱的时刻，也是唯一
  # 不用他去翻 README 的位置。**只在付费件缺席时打，且只打一行**：
  # 每次换肤都弹一大段广告，人只会学会无视它（同 release.sh 里指纹表那条教训）。
  # ⚠️ 这里只陈述本档事实 + 给个地址，别在这儿列付费功能清单 —— 那是落地页的活。
  if [ ! -f "$THEMES_DIR/_apply_pro.sh" ] && [ -n "${HKW_URL_BUY:-}" ]; then
    printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_PAID_WHERE "$HKW_URL_BUY")"
  fi
  echo
}

# Theme switching is a transaction: snapshot the explicit managed-file whitelist,
# run the existing apply path, and restore that snapshot if any required step fails.
apply() {
  local theme; theme="$(hkw_resolve_theme "${1:-}")"
  local tx="" rc=0
  tx="$(hkw_transaction_snapshot "theme:$theme" "$theme")" || {
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_TX_SNAPSHOT_FAIL)"
    return 1
  }
  printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_TX_SNAPSHOT "$(basename "$tx")")"
  # Do not put the apply subshell directly in an `if`: bash disables errexit for
  # commands used as conditions, which would turn the failure gate into a liar.
  set +e
  ( set -e; apply_impl "$theme" )
  rc=$?
  set -e
  if [ "$rc" = "0" ]; then
    return 0
  else
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_TX_APPLY_FAIL)"
    if hkw_transaction_rollback "$tx" >/dev/null; then
      printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_TX_AUTO_ROLLBACK)"
    else
      printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_TX_ROLLBACK_FAIL "$tx")"
    fi
    return "$rc"
  fi
}

transaction_plan() {
  local theme="$1"
  if ! is_theme_json "$THEMES_DIR/$theme.json"; then
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_NO_SUCH "$theme")"
    return 1
  fi
  printf "${c_purple}%s${c_off}\n" "$(t M_THEME_PLAN_HEAD "$theme")"
  hkw_transaction_plan "$theme" | while IFS=$'\t' read -r state path; do
    printf '  %-8s %s\n' "$state" "$path"
  done
  printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_PLAN_NOTE)"
}

transaction_rollback() {
  local tx
  if tx="$(hkw_transaction_rollback "${1:-latest}" 2>/dev/null)"; then
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_ROLLBACK_OK "$(basename "$tx")")"
    printf "  ${c_dim}%s${c_off}\n" "$(t M_THEME_ROLLBACK_NOTE)"
  else
    printf "${c_purple}%s${c_off}\n" "$(t M_THEME_ROLLBACK_NONE)"
    return 1
  fi
}


# ============================================================
case "${1:-}" in
  "")            pick ;;          # 有 fzf → 模糊选 + ANSI 预览；否则画廊
  --list)        list ;;          # 只要画廊、不进 fzf
  --pick)        pick ;;
  --preview|-p)  preview "$(hkw_resolve_theme "${2:-}")" ;;
  --gallery)     gallery_all ;;
  --plan)        transaction_plan "$(hkw_resolve_theme "${2:-}")" ;;
  --rollback)    transaction_rollback "${2:-latest}" ;;
  --history)     hkw_transaction_history ;;
  --audit)       shift || true; python3 "$SCRIPT_DIR/config/themes/_audit.py" "$@" ;;
  -h|--help)     blk_theme_help ;;
  *)
    # 未知选项一律当用法错误 —— 别把它当主题名去 apply（会先快照再失败）
    case "$1" in
      --*) blk_theme_help; exit 1 ;;
    esac
    # ./scripts/theme.sh <主题> [--font PostScript名] [--p3]
    # --font 给终端光学校准引擎 / font.sh 用：钉住某一套字体再换肤。
    _theme_arg="$(hkw_resolve_theme "$1")"; shift || true
    FORCE_FONT="${FORCE_FONT:-}"
    _p3=0
    _plain=0
    while [ $# -gt 0 ]; do
      case "$1" in
        --font) FORCE_FONT="${2:-}"; shift; [ $# -gt 0 ] && shift ;;
        --font=*) FORCE_FONT="${1#--font=}"; shift ;;
        --p3) _p3=1; shift ;;
        --srgb) _p3=0; shift ;;
        --plain) _plain=1; shift ;;
        *) shift ;;
      esac
    done
    if [ "$_p3" = "1" ]; then export HKW_P3=1; else unset HKW_P3; fi
    if [ "$_plain" = "1" ]; then export HKW_PLAIN=1; else unset HKW_PLAIN; fi
    apply "$_theme_arg"
    ;;
esac
