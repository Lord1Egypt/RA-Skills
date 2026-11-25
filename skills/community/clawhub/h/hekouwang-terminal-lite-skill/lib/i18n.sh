#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 运行时语言层（i18n）
#
# 每个脚本开头三行接上：
#   . "$SCRIPT_DIR/lib/i18n.sh"
#   hkw_i18n_init install "$@"
#   eval set -- "$HKW_ARGS"        # --lang 已被摘掉，后面照常解析自己的参数
#
# 之后所有对外输出走词条 key：say M_INSTALL_BREW / info M_PKG_OK "$pkg"
#
# 语言优先级：--lang zh > HKW_LANG=zh > ~/.config/hekouwang-terminal/lang > en
# 默认英文 —— 这套东西挂在 GitHub 上，第一屏得让英文用户看得懂；
# 中文用户装的时候落一次盘（install.sh），之后一直是中文，不用每次带参数。
#
# ⚠️ macOS 自带 bash 是 3.2（2007 年），**没有关联数组**：`declare -A` 直接语法错，
#    脚本连解析都过不去。所以词条表是一堆普通变量 + ${!name} 间接展开，不是 map。
#    别看着「像个 map 会更整洁」就改回去 —— 那等于只在装了 bash 5 的机器上能跑。
# ⚠️ 词条表按「先 en 后 zh」**叠加**加载：zh 缺哪条就自动落回英文，永远不会打出空串。
#    加新词条时只加 en 也不会崩，翻译可以后补。
# ============================================================

HKW_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HKW_I18N_DIR="$HKW_LIB_DIR/i18n"
HKW_LANG_FILE="${HKW_LANG_FILE:-$HOME/.config/hekouwang-terminal/lang}"

# 对外链接（$HKW_URL_BUY / $HKW_URL_REPO）。搭在 i18n.sh 上是有意的：
# 每个脚本开头都已经 source 了本文件，链接跟着进来就不用在五个脚本里各加一行。
# 链接**不是**词条 —— 它不随语言变，中英文页面是同一个地址，所以不放 i18n/ 下面。
# shellcheck disable=SC1091
[ -f "$HKW_LIB_DIR/links.sh" ] && . "$HKW_LIB_DIR/links.sh"
# 万一 links.sh 缺席（有人只拷了半个 lib/），给个空串兜底，别让 set -u 把脚本打死
HKW_URL_BUY="${HKW_URL_BUY:-}"
HKW_URL_REPO="${HKW_URL_REPO:-}"

# 各种写法归一成 en / zh；认不出返回空串（好让调用方继续往下一档找）
hkw_lang_normalize() {
  local v
  v="$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')"
  case "$v" in
    zh|zh-cn|zh_cn|zh-hans|zh_hans|cn|chinese|中文) printf 'zh' ;;
    en|en-us|en_us|english)                          printf 'en' ;;
    # auto 是**显式**选项，不是默认行为：写 HKW_LANG=auto 才跟随系统 locale
    auto)
      case "${LC_ALL:-${LC_MESSAGES:-${LANG:-}}}" in
        zh*|*[Zz][Hh]_*) printf 'zh' ;;
        *)               printf 'en' ;;
      esac ;;
    *) printf '' ;;
  esac
  return 0
}

# 加载某个模块的词条表。先 en 打底，再用当前语言覆盖。
hkw_i18n_load() {
  local mod="$1"
  if [ -f "$HKW_I18N_DIR/en/$mod.sh" ]; then
    # shellcheck disable=SC1090
    . "$HKW_I18N_DIR/en/$mod.sh"
  fi
  if [ "${HKW_LANG:-en}" != "en" ] && [ -f "$HKW_I18N_DIR/${HKW_LANG}/$mod.sh" ]; then
    # shellcheck disable=SC1090
    . "$HKW_I18N_DIR/${HKW_LANG}/$mod.sh"
  fi
  return 0
}

# hkw_i18n_init <模块名> "$@"
#   · 从参数里摘掉 --lang / --lang=xx（不摘的话 theme.sh 会把 "zh" 当成主题名）
#   · 定语言、载词条表
#   · 把剩下的参数按 %q 转义存进 $HKW_ARGS，调用方 `eval set -- "$HKW_ARGS"` 还原
hkw_i18n_init() {
  local mod="${1:-common}"; shift || true
  local want="" a lang=""
  local rest=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --lang)   want="${2:-}"; shift; [ $# -gt 0 ] && shift ;;
      --lang=*) want="${1#--lang=}"; shift ;;
      *)        rest[${#rest[@]}]="$1"; shift ;;
    esac
  done
  HKW_ARGS=""
  # ⚠️ set -u 下空数组展开在 bash 3.2 里会报 unbound variable，必须带 ${x+"..."} 守卫
  for a in ${rest+"${rest[@]}"}; do
    HKW_ARGS="$HKW_ARGS $(printf '%q' "$a")"
  done

  lang="$(hkw_lang_normalize "$want")"
  if [ -z "$lang" ]; then lang="$(hkw_lang_normalize "${HKW_LANG:-}")"; fi
  if [ -z "$lang" ] && [ -f "$HKW_LANG_FILE" ]; then
    lang="$(hkw_lang_normalize "$(cat "$HKW_LANG_FILE" 2>/dev/null)")"
  fi
  if [ -z "$lang" ]; then lang="en"; fi

  HKW_LANG="$lang"; export HKW_LANG
  HKW_LANG_EXPLICIT=""; [ -n "$want" ] && HKW_LANG_EXPLICIT=1
  hkw_i18n_load common
  [ "$mod" = "common" ] || hkw_i18n_load "$mod"
  return 0
}

# 把当前语言记到 ~/.config/hekouwang-terminal/lang（install.sh 用）
hkw_lang_persist() {
  local dir; dir="$(dirname "$HKW_LANG_FILE")"
  mkdir -p "$dir" 2>/dev/null || return 0
  printf '%s\n' "${HKW_LANG:-en}" > "$HKW_LANG_FILE" 2>/dev/null || true
  return 0
}

# hkw_pad <文本> <目标显示宽度> → 打印文本 + 补足的空格（**按显示宽度，不是字节数**）
#
# ⛔ 别再用 printf "%-16s" 打可能含中文的列：那是按**字节**补的，
#    一个汉字 3 字节、显示只占 2 格，于是中文列必歪 —— 而英文列全对，
#    所以「只用英文跑一遍」永远测不出这个 bug。
# 宽度算法：ASCII 1 格；3 字节的中日韩字符 2 格。
#    width = 字符数 + (字节数 - 字符数)/2，对这两类都精确。
hkw_pad() {
  local txt="${1:-}" want="${2:-0}" chars bytes w gap
  chars=${#txt}
  bytes=$(LC_ALL=C; printf '%s' "$txt" | wc -c)
  bytes=$(printf '%s' "$bytes" | tr -d '[:space:]')
  w=$(( chars + (bytes - chars) / 2 ))
  gap=$(( want - w ))
  [ "$gap" -lt 1 ] && gap=1
  printf '%s%*s' "$txt" "$gap" ''
}

# t <词条key> [printf 参数…] → 把翻译好的整句打到 stdout（不带换行、不带颜色）
#
# 认不出的 key 原样打印 —— 这样调用方偶尔传个动态拼好的字符串也不会变成空行，
# 加词条的过程可以一个脚本一个脚本来，中间态永远是能跑的。
t() {
  local __k="${1:-}"; shift || true
  local __v=""
  # ⚠️ ${!x} 碰到不是合法变量名的内容会直接报 bad substitution（set -e 下就是猝死），
  #    所以先拿正则卡一道：只有长得像 key 的才做间接展开。
  if [[ "$__k" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]]; then
    __v="${!__k-}"
  fi
  # ⚠️ 必须带 `--`：词条正文以「-」开头是很常见的（"--check mode, nothing was touched"），
  #    不加的话 printf 把它当自己的选项，报 `printf: --: invalid option` 然后什么都不打。
  #    2026-07-23 就是这么翻的车 —— 中文词条碰不到，英文词条一堆以 -- 开头。
  if [ -n "$__v" ]; then
    # shellcheck disable=SC2059
    printf -- "$__v" ${1+"$@"}
  else
    printf -- '%s' "$__k"
  fi
  return 0
}
