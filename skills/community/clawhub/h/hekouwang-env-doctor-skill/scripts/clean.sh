#!/usr/bin/env bash
# 开发环境体检器 · 清理选择器
#
# 设计约束（改动前先读 references/safety.md）：
#   1. 数据类【锁死】，不可勾选——模型权重、容器卷永远不进清理清单
#   2. 默认【全不选】，每一项都必须你亲手勾
#   3. 只执行【白名单内的固定命令】，不接受任意路径输入
#   4. 执行前逐条列出将要跑的命令，输入 yes 才动手
#   5. 删除版本管理器目录后提示手动清理 shell 配置（脚本不碰你的 .zshrc）
#
# 用法：
#   bash clean.sh              # 交互选择
#   bash clean.sh --dry-run    # 只演示不执行（推荐第一次用）
#
set -uo pipefail

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

# ── 配色 ────────────────────────────────────────────────
if [ -t 1 ]; then
  B=$'\033[1m'; D=$'\033[2m'; R=$'\033[0m'
  O=$'\033[38;5;208m'; Y=$'\033[38;5;179m'; RD=$'\033[38;5;167m'
  G=$'\033[38;5;71m'; C=$'\033[38;5;73m'; GY=$'\033[38;5;245m'
else
  B=""; D=""; R=""; O=""; Y=""; RD=""; G=""; C=""; GY=""
fi

# ── 版本管理器活跃性判定 ─────────────────────────────────
# 与 scan.sh 同一套信号：shell 配置是否加载、命令是否在 PATH、最近是否动过。
# 还在用的版本管理器一律锁成 data，不当作残留提供删除。
SHELL_RC=""
for rc in "$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.zshenv" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile" "$HOME/.config/fish/config.fish"; do
  [ -f "$rc" ] && SHELL_RC="$SHELL_RC $rc"
done

mgr_pattern() {
  case "$1" in
    "$HOME/.nvm")   echo 'NVM_DIR|nvm\.sh' ;;
    "$HOME/.pyenv") echo 'PYENV_ROOT|pyenv init' ;;
    "$HOME/.rbenv") echo 'RBENV_ROOT|rbenv init' ;;
    "$HOME/.asdf")  echo 'asdf\.sh|ASDF_DIR' ;;
    "$HOME/.volta") echo 'VOLTA_HOME|volta' ;;
    *) return 1 ;;
  esac
}

mgr_in_use() {  # 还在用 → 0
  local dir="$1" pat loaded=0 inpath=0
  # 1) shell 配置里有非注释的加载行
  pat=$(mgr_pattern "$dir") || return 1
  if [ -n "$SHELL_RC" ]; then
    grep -h -E "$pat" $SHELL_RC 2>/dev/null | grep -v -E '^\s*#' | grep -q . && loaded=1
  fi
  # 2) 对应命令仍在 PATH
  case "$dir" in
    "$HOME/.nvm")   command -v node   >/dev/null 2>&1 && inpath=1 ;;
    "$HOME/.pyenv") command -v pyenv  >/dev/null 2>&1 && inpath=1 ;;
    "$HOME/.rbenv") command -v rbenv  >/dev/null 2>&1 && inpath=1 ;;
    "$HOME/.asdf")  command -v asdf   >/dev/null 2>&1 && inpath=1 ;;
    "$HOME/.volta") command -v volta  >/dev/null 2>&1 && inpath=1 ;;
  esac
  [ "$loaded" -eq 1 ] && [ "$inpath" -eq 1 ] && return 0
  # 3) 当前运行时真的由它提供（nvm/pyenv 换了但没删的典型）
  local rt
  for rt in node python3 ruby; do
    command -v "$rt" 2>/dev/null | grep -qF "$dir/" && return 0
  done
  # 4) 最近 30 天动过
  find "$dir" -maxdepth 0 -mtime -30 2>/dev/null | grep -q . && return 0
  return 1
}

# ── 白名单：组|路径|名称|清理命令|代价 ─────────────────────
# group: residue(残留·可清) / cache(缓存·可清) / data(数据·锁死)
# ⛔ 命令写死在这里，不从外部输入拼装
ENTRIES=(
  "residue|$HOME/.nvm|nvm（node 版本管理器）|rm -rf \"\$HOME/.nvm\"|以后要用 nvm 需重装；记得删 shell 里 NVM_DIR 那几行"
  "residue|$HOME/.pyenv|pyenv（python 版本管理器）|rm -rf \"\$HOME/.pyenv\"|以后要用 pyenv 需重装；记得删 shell 里 pyenv init 那几行"
  "residue|$HOME/.rbenv|rbenv（ruby 版本管理器）|rm -rf \"\$HOME/.rbenv\"|同上，注意 shell 配置"
  "residue|$HOME/.asdf|asdf（多语言版本管理器）|rm -rf \"\$HOME/.asdf\"|同上，注意 shell 配置"
  "residue|$HOME/.volta|volta（node 工具链）|rm -rf \"\$HOME/.volta\"|同上，注意 shell 配置"
  "cache|$HOME/.npm|npm 缓存|npm cache clean --force|下次装包重下"
  "cache|$HOME/.cache/yarn|yarn 缓存|yarn cache clean|重下依赖"
  "cache|$HOME/Library/pnpm|pnpm store|pnpm store prune|只清无引用的包，很安全"
  "cache|$HOME/Library/Caches/Homebrew|Homebrew 下载缓存|brew cleanup|重下安装包"
  "cache|$HOME/Library/Caches/pip|pip 缓存|pip cache purge|重下 wheel"
  "cache|$HOME/.cache/uv|uv 缓存|uv cache clean|重下依赖"
  "cache|$HOME/Library/Developer/Xcode/DerivedData|Xcode 构建产物|rm -rf \"\$HOME/Library/Developer/Xcode/DerivedData\"|下次编译变慢，Xcode 会重建"
  "data|$HOME/.cache/huggingface|Hugging Face 模型权重|—|⛔ 重下要几小时，用 hf cache rm 精确删"
  "data|$HOME/Library/Containers/com.docker.docker|Docker 容器数据|—|⛔ 卷里可能有数据库数据"
  "data|$HOME/.ollama|Ollama 模型|—|⛔ 重下耗时，用 ollama rm 精确删"
)

# ── 采集：只保留实际存在且 >10MB 的项 ─────────────────────
declare -a G_ARR P_ARR N_ARR C_ARR W_ARR S_ARR SEL
printf "%s扫描中%s %s（并行测体积，约几秒）%s" "$B$C" "$R" "$D" "$R"

# 并行 du：15 个目录串行要半分钟，并行只等最慢的那个
TMPD=$(mktemp -d "${TMPDIR:-/tmp}/envdoctor.XXXXXX")
trap 'rm -rf "$TMPD"' EXIT INT TERM
i=0
for e in "${ENTRIES[@]}"; do
  IFS='|' read -r _g p _n _c _w <<< "$e"
  [ -e "$p" ] && { du -sk "$p" 2>/dev/null | awk '{print $1}' > "$TMPD/$i" & }
  i=$((i+1))
done
wait
printf "\r\033[K"

i=0
for e in "${ENTRIES[@]}"; do
  IFS='|' read -r g p n c w <<< "$e"
  kb=$(cat "$TMPD/$i" 2>/dev/null)
  i=$((i+1))
  [ -z "${kb:-}" ] && continue
  [ "$kb" -lt 10240 ] && continue          # <10MB 不值得列
  # 版本管理器：先判活跃，还在用的锁成 data，不提供删除
  if [ "$g" = "residue" ] && mgr_pattern "$p" >/dev/null 2>&1 && mgr_in_use "$p"; then
    g="data"; c="—"; w="⛔ 检测到仍在使用（shell 配置 / PATH / 运行时指向它），已锁定"
  fi
  G_ARR+=("$g"); P_ARR+=("$p"); N_ARR+=("$n"); C_ARR+=("$c"); W_ARR+=("$w"); S_ARR+=("$kb")
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
  printf "\n  %s%s◆ 开发环境清理选择器%s\n" "$B" "$C" "$R"
  printf "  %s空格%s勾选   %s↑↓%s移动   %sa%s全选   %sn%s全不选   %s回车%s确认   %sq%s退出%s\n" \
    "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$B" "$D" "$R"
  printf "  %s────────────────────────────────────────────────%s\n" "$GY" "$R"

  local lastg=""
  for ((i=0;i<N;i++)); do
    local g=${G_ARR[$i]} mark box color locked=0
    if [ "$g" != "$lastg" ]; then
      case "$g" in
        residue) printf "\n %s%s🟠 残留%s%s  —— 你已经不用的工具，清了是净赚%s\n" "$O" "$B" "$R" "$O" "$R" ;;
        cache)   printf "\n %s%s🟡 缓存%s%s  —— 在用，删了会重下（拿时间换空间）%s\n" "$Y" "$B" "$R" "$Y" "$R" ;;
        data)    printf "\n %s%s🔴 数据%s%s  —— 已锁定，不可勾选%s\n" "$RD" "$B" "$R" "$RD" "$R" ;;
      esac
      lastg="$g"
    fi
    case "$g" in
      residue) color="$O" ;; cache) color="$Y" ;; data) color="$RD"; locked=1 ;;
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
NEEDS_SHELL_NOTE=0
for i in "${CHOSEN[@]}"; do
  printf " %s%s%s  %s\n" "$B" "$(short "${P_ARR[$i]}")" "$R" "$D$(human "${S_ARR[$i]}")$R"
  printf "   %s$%s %s\n" "$D" "$R" "${C_ARR[$i]}"
  printf "   %s代价：%s%s\n\n" "$D" "${W_ARR[$i]}" "$R"
  [ "${G_ARR[$i]}" = "residue" ] && NEEDS_SHELL_NOTE=1
done

if [ "$NEEDS_SHELL_NOTE" -eq 1 ]; then
  printf "%s⚠ 你选了版本管理器目录。删完记得手动清理 shell 配置里对应的初始化行%s\n" "$Y" "$R"
  printf "%s  （本脚本不会替你改 .zshrc —— 那比删目录更危险）%s\n\n" "$D" "$R"
fi

if [ "$DRY" -eq 1 ]; then
  printf "%s※ dry-run：以上命令均未执行。去掉 --dry-run 再跑一次即可真清。%s\n" "$C" "$R"
  exit 0
fi

printf "%s确认执行？输入 %syes%s%s 继续，其他任意键取消：%s " "$B" "$G" "$R" "$B" "$R"
read -r ans
[ "$ans" != "yes" ] && { printf "%s已取消，什么都没动。%s\n" "$D" "$R"; exit 0; }

# ── 执行（只跑白名单里的固定命令）──────────────────────────
printf "\n"
OK=0; FAIL=0; FREED=0
for i in "${CHOSEN[@]}"; do
  printf " %s▸%s %s … " "$C" "$R" "$(short "${P_ARR[$i]}")"
  if eval "${C_ARR[$i]}" >/dev/null 2>&1; then
    printf "%s✓%s\n" "$G" "$R"; OK=$((OK+1)); FREED=$((FREED+${S_ARR[$i]}))
  else
    printf "%s✗ 失败（可能需要手动处理）%s\n" "$RD" "$R"; FAIL=$((FAIL+1))
  fi
done

printf "\n %s完成：成功 %d 项，失败 %d 项，回收约 %s%s%s\n" "$B" "$OK" "$FAIL" "$G" "$(human "$FREED")" "$R"
[ "$NEEDS_SHELL_NOTE" -eq 1 ] && printf " %s别忘了清理 shell 配置里的初始化行。%s\n" "$Y" "$R"
