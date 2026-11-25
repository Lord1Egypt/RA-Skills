#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 接管已有 .zshrc（而不是覆盖它）
#
# 用法:
#   ./scripts/migrate.sh              先看报告，再决定要不要写
#   ./scripts/migrate.sh --apply      直接执行（仍然会先备份）
#
# 为什么要有这个脚本：install.sh 是拿模板覆盖 ~/.zshrc 的。新机器没问题，
# 但你要是已经用了几年、里面攒了一堆 alias / PATH / 公司环境变量，
# 覆盖 = 一次性全丢（虽然有 .bak，但你得自己一行行捞回来）。
#
# 这个脚本干的事：把你 .zshrc 里「只有你才有」的行挑出来搬进 ~/.zshrc.local，
# 把「模板本来就会提供」的行（omz 初始化、starship、fzf/zoxide/atuin 的 init、
# 插件 source 等）丢掉 —— 因为模板会用更好的顺序重新给你一份。
#
# 判定是保守的：拿不准的一律算「你的」，宁可多搬也不漏搬。
# 搬完 ~/.zshrc.local 会被模板自动 source，所以你的东西一条都不会少。
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$HOME/.config/hekouwang-terminal"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init migrate "$@"
eval set -- "$HKW_ARGS"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/bak.sh"
ZRC="$HOME/.zshrc"
LOCAL="$HOME/.zshrc.local"
APPLY=0; FORCE=0
for a in "$@"; do
  case "$a" in
    --apply) APPLY=1 ;;
    --force) FORCE=1 ;;
    -h|--help) blk_migrate_help; exit 0 ;;
  esac
done

b='\033[1;34m'; g='\033[1;32m'; y='\033[1;33m'; r='\033[1;31m'; d='\033[2m'; o='\033[0m'

printf "${b}%s${o}\n" "$(t M_MIG_HEAD)"
if [ ! -f "$ZRC" ]; then
  printf "${y}%s${o}\n" "$(t M_MIG_NO_ZSHRC)"
  exit 0
fi

OUT="$(mktemp -d)"
trap 'rm -rf "$OUT"' EXIT

# ---- 前置判断：你的 .zshrc 是不是本来就是这套模板 -------------
# 常见情况：装过旧版本、现在只是想升级。这时候「迁移」是个错误的动作 ——
# 模板里的东西会被当成「你的」搬进 .zshrc.local，结果两边各留一份，
# 插件重复加载、别名重复定义。直接跑 install.sh 才对。
OVERLAP="$(python3 - "$ZRC" "$SCRIPT_DIR/config/zshrc.template" <<'PY'
import sys
def code(p):
    return [l.rstrip() for l in open(p, encoding='utf-8', errors='replace').read().splitlines()
            if l.strip() and not l.strip().startswith('#')]
a, t = code(sys.argv[1]), set(code(sys.argv[2]))
print(round(100 * sum(1 for l in a if l in t) / max(len(a), 1)))
PY
)"
if [ "${OVERLAP:-0}" -ge 60 ] && [ "$FORCE" = "0" ]; then
  printf "\n${y}%s${o}\n" "$(t M_MIG_OVERLAP "$OVERLAP")"
  printf "%s\n\n" "$(t M_MIG_OVERLAP_1)"
  printf "  ${b}%s${o}%s\n" "$(t M_MIG_OVERLAP_2)" "$(t M_MIG_OVERLAP_3)"
  printf "%s\n\n" "$(t M_MIG_OVERLAP_4)"
  printf "  ${b}%s${o}%s\n" "$(t M_MIG_OVERLAP_5)" "$(t M_MIG_OVERLAP_6)"
  printf "  ${d}%s\n" "$(t M_MIG_OVERLAP_7)"
  printf "    diff ~/.zshrc %s/config/zshrc.template\n" "$SCRIPT_DIR"
  printf "  %s\n" "$(t M_MIG_OVERLAP_8)"
  printf "  %s${o}\n" "$(t M_MIG_OVERLAP_9)"
  exit 0
fi

python3 - "$ZRC" "$OUT" <<'PY'
import os, re, sys

src_path, outdir = sys.argv[1], sys.argv[2]
lines = open(src_path, encoding='utf-8', errors='replace').read().splitlines()

# 「模板会重新提供」的行 —— 丢掉是安全的，因为模板给的版本顺序更对。
# 每条都写清楚为什么，报告里会原样打给用户看。
# 理由写成 (英文, 中文) 一对，按 HKW_LANG 取 —— 这段会原样打进报告给用户看。
_ZH = os.environ.get('HKW_LANG', 'en') == 'zh'


def _r(en, zh):
    return zh if _ZH else en


MANAGED = [
    (r'source\s+\$?\{?ZSH\}?/oh-my-zsh\.sh',      _r('the template re-initialises oh-my-zsh', '模板会重新初始化 oh-my-zsh')),
    (r'^\s*export\s+ZSH=',                        _r('the template sets $ZSH', '模板会设 $ZSH')),
    (r'^\s*ZSH_THEME=',                           _r('the template hands the prompt to starship', '模板把 prompt 交给 starship')),
    (r'^\s*plugins=\(',                           _r('the template has its own trimmed plugin list', '模板有自己的精简插件表')),
    (r'starship\s+init',                          _r('the template initialises starship', '模板会初始化 starship')),
    (r'zoxide\s+init',                            _r('the template initialises zoxide', '模板会初始化 zoxide')),
    (r'atuin\s+init',                             _r('the template initialises atuin', '模板会初始化 atuin')),
    (r'fnm\s+env|NVM_DIR|vfox\s+activate|opt/node',
     _r('the template sources one Node manager via ~/.config/hekouwang-terminal/node.sh',
        '模板通过 ~/.config/hekouwang-terminal/node.sh 只加载一套 Node 管理器')),
    (r'fzf\s+--zsh|\.fzf\.zsh',                   _r('the template initialises fzf', '模板会初始化 fzf')),
    (r'zsh-syntax-highlighting\.zsh',             _r('the template puts it in the right spot, second to last', '模板把它放在正确的倒数第二位')),
    (r'zsh-autosuggestions\.zsh',                 _r('the template sources it', '模板会 source 它')),
    (r'iterm2_shell_integration',                 _r('the template puts it on the last line', '模板把它放在最后一行')),
    (r'brew\s+shellenv',                          _r('the template detects brew on Intel/ARM by itself', '模板会自适应 Intel/ARM 探测 brew')),
    (r'znap\.zsh|zsh-snap',                       _r('the template ships znap', '模板自带 znap')),
    (r'^\s*(alias\s+)?(ls|ll|la|lt)=.*eza',       _r('the template has the same eza aliases', '模板有同名 eza 别名')),
    (r'^\s*(alias\s+)?cat=.*bat',                 _r('the template has the same bat alias', '模板有同名 bat 别名')),
    (r'^\s*export\s+(BAT_THEME|FZF_DEFAULT_OPTS|LS_COLORS|EZA_COLORS)=',
     _r('these are generated per theme and follow every theme switch', '这些由主题生成，换肤时自动跟着变')),
    (r'^\s*source\s+.*hekouwang-terminal',        _r("this skill's own line", '本套装自己的行')),
    # ⛔ 这条最要命：模板末尾的 `[ -f ~/.zshrc.local ] && source ~/.zshrc.local`
    #    要是被搬进 .zshrc.local，它就会 source 自己 —— 无限递归。
    #    症状不是报错而是**终端起不来**：zsh 卡几十秒后吐
    #    `is-at-least: job table full or recursion limit exceeded`。
    #    2026-07-22 在作者自己机器上真踩了一次（启动 50s），必须永远拦在这。
    (r'\.zshrc\.local',                           _r('the template loads .zshrc.local; moving this here makes it source itself', '模板负责加载 .zshrc.local，搬进来会自我递归')),
]
# 明确「一定是你的」——即使长得像上面某条也优先留下
YOURS_STRONG = [
    (r'^\s*alias\s+',            'alias'),
    (r'^\s*(export\s+)?[A-Z_][A-Z0-9_]*=',  _r('env var', '环境变量')),
    (r'^\s*function\s+\w+|^\s*\w+\s*\(\)\s*\{', _r('function', '函数')),
    (r'^\s*export\s+PATH=',      'PATH'),
    (r'^\s*source\s+|^\s*\.\s+', _r('sources another file', 'source 别的文件')),
    (r'^\s*bindkey\s+',          _r('key binding', '键位绑定')),
    (r'^\s*setopt\s+|^\s*unsetopt\s+', _r('zsh option', 'zsh 选项')),
    (r'^\s*zstyle\s+',           'zstyle'),
    (r'^\s*eval\s+',             _r('eval init', 'eval 初始化')),
]

def is_managed(line):
    for pat, why in MANAGED:
        if re.search(pat, line):
            return why
    return None

def is_yours(line):
    for pat, what in YOURS_STRONG:
        if re.match(pat, line):
            return what
    return None

# ⚠️ 判定单位必须是「段落」而不是「行」。
# 按行判会把多行结构拦腰砍断 —— for/done 只删中间那行、续行的
# `git clone … \` 只删下半截 —— 搬过去就是一份语法错的 .zshrc.local，
# 比不迁移还糟。所以：空行分段，一段里**每一行代码都是模板会重新提供的**
# 才丢整段；只要有一行拿不准，整段留下。
# 代价是有些初始化会重复出现（omz/znap 之类都是幂等的，最多慢几毫秒），
# 但绝不会把你的配置切碎 —— 这个取舍是刻意的。
paras, cur = [], []
for raw in lines:
    if raw.strip():
        cur.append(raw.rstrip('\n'))
    else:
        if cur:
            paras.append(cur)
        cur = []
        paras.append([])          # 保留空行，搬过去的排版不走样
if cur:
    paras.append(cur)

kept, dropped = [], []
for para in paras:
    code = [l for l in para if l.strip() and not l.strip().startswith('#')]
    if not code:                                  # 纯注释/空行段：跟着后面的段走
        kept.extend(para)
        continue
    reasons = []
    all_managed = True
    for line in code:
        why = is_managed(line)
        # MANAGED 命中即算「模板会给」；两边都命中时也算（例如 export BAT_THEME=）
        if why:
            reasons.append((line, why))
        else:
            all_managed = False
    if all_managed:
        dropped.extend(reasons)
    else:
        kept.extend(para)

# 去掉首尾多余空行
while kept and not kept[0].strip():
    kept.pop(0)
while kept and not kept[-1].strip():
    kept.pop()

kept_code = len([k for k in kept if k.strip() and not k.strip().startswith('#')])
with open(os.path.join(outdir, 'kept.txt'), 'w', encoding='utf-8') as f:
    f.write(('\n'.join(kept) + '\n') if kept else '')
with open(os.path.join(outdir, 'report.txt'), 'w', encoding='utf-8') as f:
    f.write(f'TOTAL {len(lines)}\nKEPT {kept_code}\nDROPPED {len(dropped)}\n')
    f.write('---DROPPED---\n')
    for line, why in dropped:
        f.write(f'{why}\t{line.strip()[:100]}\n')
PY

# ⚠️ 最后一道闸：搬走的内容必须自己就是合法 zsh。
# 上面已经按段落切了，但用户的 .zshrc 千奇百怪，宁可在这儿拦下也不能写出去。
if [ -s "$OUT/kept.txt" ] && command -v zsh >/dev/null 2>&1; then
  if ! zsh -n "$OUT/kept.txt" 2>"$OUT/synerr.txt"; then
    printf "\n${y}%s${o}\n" "$(t M_MIG_SYNTAX_FAIL)"
    sed 's/^/  /' "$OUT/synerr.txt" | head -5
    printf "\n${d}%s\n" "$(t M_MIG_SYNTAX_FIX1)"
    printf "%s${o}\n" "$(t M_MIG_SYNTAX_FIX2 "$SCRIPT_DIR")"
    exit 1
  fi
fi

TOTAL=$(grep '^TOTAL' "$OUT/report.txt" | awk '{print $2}')
KEPT=$(grep '^KEPT' "$OUT/report.txt" | awk '{print $2}')
DROPPED=$(grep '^DROPPED ' "$OUT/report.txt" | awk '{print $2}')

printf "\n%s\n" "$(t M_MIG_TOTAL "$TOTAL")"
printf "  ${g}%s${o}\n" "$(t M_MIG_KEPT "$KEPT")"
printf "  ${d}%s${o}\n" "$(t M_MIG_DROPPED "$DROPPED")"

printf "\n${b}%s${o}\n" "$(t M_MIG_DROP_HEAD)"
# ⚠️ 这一列**不能用 awk/printf 的 %-34s 补齐**：那是按**字节**数补的，
#    中文一个字 3 字节、显示宽 2，中文理由那一列必歪（英文全对、中文全歪，
#    所以只用英文测是测不出来的）。交给 Python 按显示宽度补，中日韩算 2 格。
python3 - "$OUT/report.txt" <<'PYCOL'
import sys, unicodedata


def width(t):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in t)


lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
rows = [l.split("\t", 1) for l in lines[lines.index("---DROPPED---") + 1:] if "\t" in l][:40]
# 列宽取「最长的那条」，但**封顶 44 格**：英文理由比中文长得多，
# 不封顶的话第二列会被推到屏幕外，窄窗口里更难看。超过封顶的那几条自己占一行宽度。
pad = min(max((width(r[0]) for r in rows), default=0), 44) + 2
for why, line in rows:
    gap = pad - width(why)
    print(f"  \033[2m{why}{' ' * gap if gap > 0 else ' '}\033[0m{line}")
PYCOL

printf "\n${b}%s${o}\n" "$(t M_MIG_KEEP_HEAD)"
if [ -s "$OUT/kept.txt" ]; then
  grep -v '^\s*$' "$OUT/kept.txt" | head -30 | sed 's/^/  /'
  LEFT=$(( $(grep -vc '^\s*$' "$OUT/kept.txt") - 30 ))
  [ "$LEFT" -gt 0 ] && printf "  ${d}%s${o}\n" "$(t M_MIG_KEEP_MORE "$LEFT")"
else
  printf "  ${d}%s${o}\n" "$(t M_MIG_KEEP_NONE)"
fi

if [ "$APPLY" = "0" ]; then
  printf "\n${y}%s${o}\n" "$(t M_MIG_PREVIEW_ONLY)"
  printf "${b}%s${o}\n" "$(t M_MIG_PREVIEW_NEXT)"
  printf "${d}%s${o}\n" "$(t M_MIG_PREVIEW_WHAT)"
  exit 0
fi

# ---- 真正执行 ----------------------------------------------
printf "\n${b}%s${o}\n" "$(t M_MIG_RUNNING)"
hkw_bak_sweep_legacy
BAK="$(hkw_bak_copy "$ZRC" zshrc)"
printf "  ${g}·${o} %s\n" "$(t M_MIG_BAK "$BAK")"

if [ -s "$OUT/kept.txt" ]; then
  # ⛔ 先备份 ~/.zshrc.local 再追加。原来这里直接 >> 上去，而下面回滚分支引用的
  #    $LOCAL_BAK 从来没人赋值 —— 于是「自动回滚」只还原得了 .zshrc，
  #    追加进 .zshrc.local 的那一坨永远留着，回滚是假的。2026-07-23 补。
  if [ -f "$LOCAL" ]; then
    LOCAL_BAK="$(hkw_bak_copy "$LOCAL" zshrc.local)"
    printf "  ${g}·${o} %s\n" "$(t M_MIG_LOCAL_BAK "$LOCAL_BAK")"
  fi
  {
    printf '\n# ============================================================\n'
    printf '# %s\n' "$(t M_MIG_BANNER1 "$(date '+%Y-%m-%d %H:%M')")"
    printf '# %s\n' "$(t M_MIG_BANNER2 "$BAK")"
    printf '# ============================================================\n'
    cat "$OUT/kept.txt"
  } >> "$LOCAL"
  printf "  ${g}·${o} %s\n" "$(t M_MIG_APPENDED "$LOCAL")"
else
  [ -f "$LOCAL" ] || cp "$SCRIPT_DIR/config/zshrc.local.example" "$LOCAL"
fi

cp "$SCRIPT_DIR/config/zshrc.template" "$ZRC"
printf "  ${g}·${o} %s\n" "$(t M_MIG_TEMPLATE)"

# ---- 最后一道闸：结果必须真的能起一个 shell ------------------
# 前面的静态检查（按段落切、zsh -n 验语法）挡不住「语法对但跑起来是死循环」
# 这类问题 —— 2026-07-22 实测过一次：模板末尾的 source ~/.zshrc.local 被搬进
# .zshrc.local 自己，语法完全合法，但 shell 启动要 50 秒并报
# `job table full or recursion limit exceeded`。所以必须真起一个 shell 验。
printf "\n${b}%s${o}\n" "$(t M_MIG_VERIFY)"
if command -v zsh >/dev/null 2>&1; then
  START=$(date +%s)
  if perl -e 'alarm 25; exec @ARGV' zsh -i -c 'exit' >/dev/null 2>&1; then
    COST=$(( $(date +%s) - START ))
    if [ "$COST" -ge 5 ]; then
      printf "  ${y}%s${o}\n" "$(t M_MIG_VERIFY_SLOW "$COST")"
      printf "  ${d}%s${o}\n" "$(t M_MIG_VERIFY_SLOW_FIX)"
    else
      printf "  ${g}%s${o}\n" "$(t M_MIG_VERIFY_OK "$COST")"
    fi
  else
    printf "  ${r}%s${o}\n" "$(t M_MIG_VERIFY_FAIL)"
    cp "$BAK" "$ZRC"
    if [ -n "${LOCAL_BAK:-}" ] && [ -f "$LOCAL_BAK" ]; then
      cp "$LOCAL_BAK" "$LOCAL"
      printf "  ${g}·${o} %s\n" "$(t M_MIG_ROLLED_BOTH)"
    else
      printf "  ${g}·${o} %s\n" "$(t M_MIG_ROLLED_ONE)"
    fi
    printf "\n  ${d}%s\n" "$(t M_MIG_ROLLED_NOTE)"
    printf "  %s\n" "$(t M_MIG_ROLLED_NOTE2)"
    printf "  %s${o}\n" "$(t M_MIG_ROLLED_NOTE3 "$SCRIPT_DIR")"
    exit 1
  fi
fi

printf "\n${g}%s${o}%s ${b}cp %s ~/.zshrc${o}\n" "$(t M_MIG_DONE)" "$(t M_MIG_DONE_NOTE)" "$BAK"
printf "${d}%s${o}\n" "$(t M_MIG_DONE_DOCTOR)"
