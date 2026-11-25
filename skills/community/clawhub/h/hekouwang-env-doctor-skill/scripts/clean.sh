#!/usr/bin/env bash
# 开发环境体检器 · 缓存清理选择器
#
# 范围声明（改脚本前先读 references/safety.md）：
#   本脚本【只跑各工具官方的缓存清理/旧版本清理命令】。
#   它不删除版本管理器目录（~/.nvm、~/.pyenv 等）、不删除项目源码、
#   不删除模型权重与容器数据，也不改写 shell 配置。
#   版本管理器被判定为「残留」时，报告只给手动卸载步骤，由用户自己执行。
#
# 设计约束：
#   1. 数据类【锁死】，不可勾选——模型权重、容器卷永远不进清理清单
#   2. 默认【全不选】，每一项都必须你亲手勾
#   3. 只执行【白名单内的固定命令】，不接受任意路径输入，不做动态拼接
#   4. 执行前逐条列出命令与代价，输入 yes 才动手；执行时每项再确认一次
#
# 用法：
#   bash clean.sh              # 交互选择
#   bash clean.sh --dry-run    # 只演示不执行（推荐第一次用）
#
set -uo pipefail

DRY=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
  esac
done

# ── 配色 ────────────────────────────────────────────────
if [ -t 1 ]; then
  B=$'\033[1m'; D=$'\033[2m'; R=$'\033[0m'
  O=$'\033[38;5;208m'; Y=$'\033[38;5;179m'; RD=$'\033[38;5;167m'
  G=$'\033[38;5;71m'; C=$'\033[38;5;73m'; GY=$'\033[38;5;245m'
else
  B=""; D=""; R=""; O=""; Y=""; RD=""; G=""; C=""; GY=""
fi

# ── 白名单：组|id|探测命令|路径|名称|展示命令|代价 ──────────
# group: cache(缓存·可清) / data(数据·锁死)
# 只收录有官方清理子命令的项；命令在 run_cleaner 里按 id 静态分派。
# ⛔ 不接受外部输入拼装命令，也不做动态求值。
HOMEBREW_CELLAR=""
command -v brew >/dev/null 2>&1 && HOMEBREW_CELLAR=$(brew --cellar 2>/dev/null)
ENTRIES=(
  "cache|brew-old|brew|$HOMEBREW_CELLAR|Homebrew 旧版本（官方 brew cleanup）|brew cleanup|只删过期旧版本、保留当前版本；体积显示为 Cellar 总量上限"
  "cache|brew-cache|brew|$HOME/Library/Caches/Homebrew|Homebrew 下载缓存|brew cleanup --scrub|清下载缓存，已安装版本不动；重装时需重下安装包"
  "cache|npm|npm|$HOME/.npm|npm 缓存|npm cache clean --force|下次装包重下"
  "cache|yarn|yarn|$HOME/.cache/yarn|yarn 缓存|yarn cache clean|重下依赖"
  "cache|pnpm|pnpm|$HOME/Library/pnpm|pnpm store|pnpm store prune|只清无引用的包，很安全"
  "cache|pip|pip3|$HOME/Library/Caches/pip|pip 缓存|pip3 cache purge|重下 wheel"
  "cache|uv|uv|$HOME/.cache/uv|uv 缓存|uv cache clean|重下依赖"
  "data|hf|-|$HOME/.cache/huggingface|Hugging Face 模型权重|—|⛔ 重下要几小时，用 hf cache rm 精确删"
  "data|docker|-|$HOME/Library/Containers/com.docker.docker|Docker 容器数据|—|⛔ 卷里可能有数据库数据"
  "data|ollama|-|$HOME/.ollama|Ollama 模型|—|⛔ 重下耗时，用 ollama rm 精确删"
)

# ── 静态命令分派：按 id 跑官方清理子命令 ─────────────────
run_cleaner() {
  case "$1" in
    brew-old)   brew cleanup ;;
    brew-cache) brew cleanup --scrub ;;
    npm)        npm cache clean --force ;;
    yarn)       yarn cache clean ;;
    pnpm)       pnpm store prune ;;
    pip)        pip3 cache purge ;;
    uv)         uv cache clean ;;
    *)          return 1 ;;
  esac
}

# ── 采集：只保留实际存在且 >10MB 的项 ─────────────────────
declare -a G_ARR ID_ARR P_ARR N_ARR C_ARR W_ARR S_ARR SEL
printf "%s扫描中%s %s（并行测体积，约几秒）%s" "$B$C" "$R" "$D" "$R"

# 并行 du：串行要半分钟，并行只等最慢的那个
TMPD=$(mktemp -d "${TMPDIR:-/tmp}/envdoctor.XXXXXX")
trap 'rm -r "${TMPD:?}" 2>/dev/null' EXIT INT TERM
i=0
for e in "${ENTRIES[@]}"; do
  IFS='|' read -r _g _id _bin p _n _c _w <<< "$e"
  [ -e "$p" ] && { du -sk "$p" 2>/dev/null | awk '{print $1}' > "$TMPD/$i" & }
  i=$((i+1))
done
wait
printf "\r\033[K"

i=0
for e in "${ENTRIES[@]}"; do
  IFS='|' read -r g id bin p n c w <<< "$e"
  kb=$(cat "$TMPD/$i" 2>/dev/null)
  i=$((i+1))
  [ -z "${kb:-}" ] && continue
  [ "$kb" -lt 10240 ] && continue          # <10MB 不值得列
  # 缓存项要求对应工具还在，否则命令跑不了，列出来只会误导
  if [ "$bin" != "-" ] && ! command -v "$bin" >/dev/null 2>&1; then
    continue
  fi
  G_ARR+=("$g"); ID_ARR+=("$id"); P_ARR+=("$p"); N_ARR+=("$n"); C_ARR+=("$c"); W_ARR+=("$w"); S_ARR+=("$kb")
  SEL+=(0)                                  # ⭐ 默认全不选
done
N=${#P_ARR[@]}
[ "$N" -eq 0 ] && { printf "%s没扫到值得清理的项。%s\n" "$G" "$R"; exit 0; }

human() {
  local kb=$1
  if   [ "$kb" -ge 1048576 ]; then awk -v k="$kb" 'BEGIN{printf "%.1f GB", k/1048576}'
  else awk -v k="$kb" 'BEGIN{printf "%.0f MB", k/1024}'; fi
}
short() { echo "${1/#$HOME/~}"; }

# ── 绘制 ────────────────────────────────────────────────
CUR=0
draw() {
  clear
  local seltot=0 i
  for ((i=0;i<N;i++)); do [ "${SEL[$i]}" -eq 1 ] && seltot=$((seltot+${S_ARR[$i]})); done

  # 不画边框：中文是双宽字符，固定宽度的框必然对不齐
  printf "\n  %s%s◆ 开发环境缓存清理选择器%s\n" "$B" "$C" "$R"
  printf "  %s空格%s勾选   %s↑↓%s移动   %sa%s全选   %sn%s全不选   %s回车%s确认   %sq%s退出%s\n" \
    "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$R"
  printf "  %s只跑官方缓存清理命令，不删版本管理器目录、不删模型与容器数据%s\n" "$D" "$R"
  printf "  %s────────────────────────────────────────────────%s\n" "$GY" "$R"

  local lastg=""
  for ((i=0;i<N;i++)); do
    local g=${G_ARR[$i]} mark box color locked=0
    if [ "$g" != "$lastg" ]; then
      case "$g" in
        cache)   printf "\n %s%s🟡 缓存%s%s  —— 在用，删了会重下（拿时间换空间）%s\n" "$Y" "$B" "$R" "$Y" "$R" ;;
        data)    printf "\n %s%s🔴 数据%s%s  —— 已锁定，不可勾选%s\n" "$RD" "$B" "$R" "$RD" "$R" ;;
      esac
      lastg="$g"
    fi
    case "$g" in
      cache) color="$Y" ;; data) color="$RD"; locked=1 ;;
    esac
    if [ "$locked" -eq 1 ]; then box="${D}[🔒]${R}"
    elif [ "${SEL[$i]}" -eq 1 ]; then box="${G}[✓]${R}"
    else box="${D}[ ]${R}"; fi
    [ "$i" -eq "$CUR" ] && mark="${C}❯${R}" || mark=" "
    printf " %s %s %s%-42s%s %s%8s%s  %s%s%s\n" \
      "$mark" "$box" "$color" "$(short "${P_ARR[$i]}")" "$R" \
      "$B" "$(human "${S_ARR[$i]}")" "$R" "$D" "${N_ARR[$i]}" "$R"
  done
  printf "\n %s已选 %s%s%s%s\n" "$D" "$B$G" "$(human "$seltot")" "$R" "$R"
  [ "$DRY" -eq 1 ] && printf " %s※ dry-run 模式：只演示，不会真的执行%s\n" "$C" "$R"
}

# ── 交互 ────────────────────────────────────────────────
while true; do
  draw
  IFS= read -rsn1 key
  case "$key" in
    $'\x1b')  # 方向键是三字符转义序列，逐字符读（一次读两字符容易和输入流错位）
              IFS= read -rsn1 -t 1 k2
              if [ "${k2:-}" = "[" ]; then
                IFS= read -rsn1 -t 1 k3
                case "${k3:-}" in
                  'A') ((CUR>0)) && ((CUR--)) ;;
                  'B') ((CUR<N-1)) && ((CUR++)) ;;
                esac
              fi ;;
    ' ')      [ "${G_ARR[$CUR]}" = "data" ] || SEL[$CUR]=$(( 1 - ${SEL[$CUR]} )) ;;
    k) ((CUR>0)) && ((CUR--)) ;;
    j) ((CUR<N-1)) && ((CUR++)) ;;
    a) for ((i=0;i<N;i++)); do [ "${G_ARR[$i]}" = "data" ] || SEL[$i]=1; done ;;
    n) for ((i=0;i<N;i++)); do SEL[$i]=0; done ;;
    q|$'\x03') clear; printf "%s已退出，什么都没动。%s\n" "$D" "$R"; exit 0 ;;
    "")       break ;;
  esac
done

# ── 确认 ────────────────────────────────────────────────
clear
CHOSEN=(); TOT=0
for ((i=0;i<N;i++)); do [ "${SEL[$i]}" -eq 1 ] && { CHOSEN+=("$i"); TOT=$((TOT+${S_ARR[$i]})); }; done
[ ${#CHOSEN[@]} -eq 0 ] && { printf "%s一项都没选，什么都没动。%s\n" "$D" "$R"; exit 0; }

printf "%s%s即将执行以下命令%s（预计回收 %s%s%s）\n\n" "$B" "$C" "$R" "$B$G" "$(human "$TOT")" "$R"
for i in "${CHOSEN[@]}"; do
  printf " %s%s%s  %s\n" "$B" "$(short "${P_ARR[$i]}")" "$R" "$D$(human "${S_ARR[$i]}")$R"
  printf "   %s$%s %s\n" "$D" "$R" "${C_ARR[$i]}"
  printf "   %s代价：%s%s\n\n" "$D" "${W_ARR[$i]}" "$R"
done

if [ "$DRY" -eq 1 ]; then
  printf "%s※ dry-run：以上命令均未执行。去掉 --dry-run 再跑一次即可真清。%s\n" "$C" "$R"
  exit 0
fi

printf "%s确认执行？输入 %syes%s%s 继续，其他任意键取消：%s " "$B" "$G" "$R" "$B" "$R"
read -r ans
[ "$ans" != "yes" ] && { printf "%s已取消，什么都没动。%s\n" "$D" "$R"; exit 0; }

# ── 执行（只跑白名单里的固定命令；逐项打印路径并确认）──────────
printf "\n"
OK=0; FAIL=0; SKIP=0; FREED=0
for i in "${CHOSEN[@]}"; do
  printf "\n %s▸%s 将清理：%s%s%s\n" "$C" "$R" "$B" "$(short "${P_ARR[$i]}")" "$R"
  printf "   命令：%s%s%s\n" "$D" "${C_ARR[$i]}" "$R"
  printf "   %s确认清理这一项？输入 y 继续，其他跳过：%s " "$B" "$R"
  read -r one
  [ "$one" = "y" ] || { printf "   %s已跳过%s\n" "$D" "$R"; SKIP=$((SKIP+1)); continue; }
  printf "   执行中 … "
  if run_cleaner "${ID_ARR[$i]}" >/dev/null 2>&1; then
    printf "%s✓%s\n" "$G" "$R"; OK=$((OK+1)); FREED=$((FREED+${S_ARR[$i]}))
  else
    printf "%s✗ 失败（可能需要手动处理）%s\n" "$RD" "$R"; FAIL=$((FAIL+1))
  fi
done

printf "\n %s完成：成功 %d 项，失败 %d 项，跳过 %d 项，回收约 %s%s%s\n" "$B" "$OK" "$FAIL" "$SKIP" "$G" "$(human "$FREED")" "$R"
