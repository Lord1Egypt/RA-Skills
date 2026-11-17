#!/usr/bin/env bash
# 开发环境体检 · 只读扫描器
#
# ⛔ 铁律：本脚本【只读】。全文不含 rm / rmdir / trash / unlink / mv / truncate 等任何破坏性命令。
#    它只负责「量体温」，判定与建议交给模型，删除动作永远交给用户本人执行。
#
# 用法：bash scan.sh                      # 全量扫描
#      bash scan.sh --quick               # 跳过耗时的家目录发现扫描
#      bash scan.sh --profile ai-dev      # AI 开发机快扫（Agent 宿主 + 跳过大户发现）
#      bash scan.sh --quick --profile ai-dev
#
# 输出为分节纯文本，供模型按 references/rules.md 判定。

set -uo pipefail
QUICK=0
PROFILE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --quick) QUICK=1 ;;
    --profile)
      shift
      PROFILE="${1:-}"
      ;;
    --profile=*) PROFILE="${1#--profile=}" ;;
  esac
  shift
done
[ "$PROFILE" = "ai-dev" ] && QUICK=1

human() {  # KB -> 人类可读
  local kb=${1:-0}
  if   [ "$kb" -ge 1048576 ]; then awk -v k="$kb" 'BEGIN{printf "%.1f GB", k/1048576}'
  elif [ "$kb" -ge 1024 ];    then awk -v k="$kb" 'BEGIN{printf "%.0f MB", k/1024}'
  else echo "${kb} KB"; fi
}

size_kb() { du -sk "$1" 2>/dev/null | awk '{print $1}'; }

echo "# 开发环境体检 · 原始数据"
echo "# 采集时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "# 主机: $(uname -s) $(uname -m)"
echo

# ── 1. 磁盘大盘 ──────────────────────────────────────────
# macOS 自 Catalina 起系统卷/数据卷分离，查 / 会严重低估，必须查数据卷
echo "## DISK"
if [ -d /System/Volumes/Data ]; then
  df -h /System/Volumes/Data 2>/dev/null | tail -1 | awk '{print "volume\t"$1"\ttotal\t"$2"\tused\t"$3"\tavail\t"$4"\tpct\t"$5}'
  printf "note\tmacOS 数据卷（df -h / 会低估，勿用）\n"
else
  df -h "$HOME" 2>/dev/null | tail -1 | awk '{print "volume\t"$1"\ttotal\t"$2"\tused\t"$3"\tavail\t"$4"\tpct\t"$5}'
fi
echo

# ── 2. 候选目录体积 ──────────────────────────────────────
# 覆盖：版本管理器 / 包管理器缓存 / 构建缓存 / 容器 / AI 模型
echo "## SIZES"
printf "# size_kb\thuman\tpath\n"
CANDIDATES=(
  "$HOME/.cache" "$HOME/.npm" "$HOME/.yarn" "$HOME/.bun" "$HOME/.deno"
  "$HOME/.m2" "$HOME/.gradle" "$HOME/.ivy2" "$HOME/.sbt"
  "$HOME/.cargo" "$HOME/.rustup" "$HOME/go/pkg" "$HOME/.gem"
  "$HOME/.nvm" "$HOME/.pyenv" "$HOME/.rbenv" "$HOME/.rvm" "$HOME/.asdf"
  "$HOME/.sdkman" "$HOME/.jenv" "$HOME/.volta" "$HOME/.local/share/mise"
  "$HOME/.local/share/uv" "$HOME/.local/share/virtualenvs" "$HOME/.virtualenvs"
  "$HOME/miniforge3" "$HOME/anaconda3" "$HOME/miniconda3"
  "$HOME/.ollama" "$HOME/.lmstudio" "$HOME/.cache/huggingface" "$HOME/.cache/torch"
  "$HOME/Library/Caches" "$HOME/Library/Caches/Homebrew"
  "$HOME/Library/Containers/com.docker.docker" "$HOME/.docker"
  "$HOME/Library/Developer/Xcode/DerivedData"
  "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
  "$HOME/Library/Developer/CoreSimulator/Devices"
  "$HOME/Library/pnpm" "$HOME/Library/Caches/pip"
)
AI_CANDIDATES=(
  "$HOME/.claude" "$HOME/.cursor" "$HOME/.codex" "$HOME/.codebuddy"
  "$HOME/.agents" "$HOME/.npm/_npx"
  "$HOME/Library/Application Support/Cursor"
  "$HOME/Library/Application Support/Claude"
  "$HOME/Library/Caches/ms-playwright" "$HOME/.cache/ms-playwright"
)
if [ "$PROFILE" = "ai-dev" ]; then
  CANDIDATES=("${AI_CANDIDATES[@]}" "${CANDIDATES[@]}")
else
  CANDIDATES+=("${AI_CANDIDATES[@]}")
fi
for d in "${CANDIDATES[@]}"; do
  [ -e "$d" ] || continue
  kb=$(size_kb "$d"); [ -z "${kb:-}" ] && continue
  [ "$kb" -lt 1024 ] && continue   # <1MB 不列，降噪
  printf "%s\t%s\t%s\n" "$kb" "$(human "$kb")" "${d/#$HOME/~}"
done | sort -rn
echo

# ── 3. 版本管理器活跃性判定（本 skill 的差异化核心）──────────
# 判定「这个工具你还在用吗」：目录在不在 + shell 有没有加载 + PATH 里有没有 + 谁在真正提供运行时
echo "## MANAGERS"
printf "# tool\tdir\tdir_size\tshell_loaded\tcmd_in_path\tlast_modified\n"
SHELL_RC=""
for rc in "$HOME/.zshrc" "$HOME/.zprofile" "$HOME/.zshenv" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile" "$HOME/.config/fish/config.fish"; do
  [ -f "$rc" ] && SHELL_RC="$SHELL_RC $rc"
done

check_mgr() {  # $1=工具名 $2=目录 $3=加载特征词
  local tool="$1" dir="$2" pat="$3"
  [ -e "$dir" ] || return 0
  local kb loaded inpath mtime
  kb=$(size_kb "$dir")
  # shell 配置里是否真的加载它（排除纯注释行，注释不算加载）
  loaded="no"
  if [ -n "$SHELL_RC" ]; then
    grep -h -E "$pat" $SHELL_RC 2>/dev/null | grep -v -E '^\s*#' | grep -q . && loaded="yes"
  fi
  command -v "$tool" >/dev/null 2>&1 && inpath="yes" || inpath="no"
  mtime=$(date -r "$dir" '+%Y-%m-%d' 2>/dev/null || echo "-")
  printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$tool" "${dir/#$HOME/~}" "$(human "${kb:-0}")" "$loaded" "$inpath" "$mtime"
}

check_mgr nvm     "$HOME/.nvm"                  'NVM_DIR|nvm\.sh'
check_mgr fnm     "$HOME/.local/share/fnm"      'fnm env|FNM_DIR'
check_mgr volta   "$HOME/.volta"                'VOLTA_HOME|volta'
check_mgr pyenv   "$HOME/.pyenv"                'PYENV_ROOT|pyenv init'
check_mgr rbenv   "$HOME/.rbenv"                'RBENV_ROOT|rbenv init'
check_mgr rvm     "$HOME/.rvm"                  'rvm/scripts|RVM'
check_mgr asdf    "$HOME/.asdf"                 'asdf\.sh|ASDF_DIR'
check_mgr mise    "$HOME/.local/share/mise"     'mise activate'
check_mgr sdk     "$HOME/.sdkman"               'SDKMAN_DIR|sdkman-init'
check_mgr jenv    "$HOME/.jenv"                 'jenv init|JENV_ROOT'
check_mgr conda   "$HOME/miniforge3"            'conda initialize|conda\.sh'
check_mgr conda   "$HOME/anaconda3"             'conda initialize|conda\.sh'
check_mgr conda   "$HOME/miniconda3"            'conda initialize|conda\.sh'
echo

# ── 4. 运行时实际来源（交叉验证，判定谁在真正干活）────────
echo "## RUNTIME"
printf "# runtime\tresolved_path\tversion\towner_guess\n"
for rt in node python3 ruby java go rustc; do
  p=$(command -v "$rt" 2>/dev/null) || continue
  [ -z "$p" ] && continue
  v=$("$rt" --version 2>/dev/null | head -1 | tr -d '\n')
  owner="system/other"
  case "$p" in
    *fnm*)        owner="fnm" ;;
    *"/.nvm/"*)   owner="nvm" ;;
    *volta*)      owner="volta" ;;
    *"/.pyenv/"*) owner="pyenv" ;;
    *"/.rbenv/"*) owner="rbenv" ;;
    *"/.rvm/"*)   owner="rvm" ;;
    *"/.asdf/"*)  owner="asdf" ;;
    *mise*)       owner="mise" ;;
    *conda*|*miniforge*|*anaconda*) owner="conda" ;;
    */homebrew/*|*/Cellar/*)        owner="homebrew" ;;
  esac
  printf "%s\t%s\t%s\t%s\n" "$rt" "${p/#$HOME/~}" "${v:--}" "$owner"
done
echo

# ── 4b. AI Agent 宿主快览（ai-dev 档重点看）──────────────
if [ "$PROFILE" = "ai-dev" ] || [ -d "$HOME/.claude" ] || [ -d "$HOME/.cursor" ]; then
  echo "## AI_AGENTS"
  printf "# host\tdir\tsize\tskills_count\thas_mcp\n"
  for host_dir in "$HOME/.claude" "$HOME/.cursor" "$HOME/.codex"; do
    [ -d "$host_dir" ] || continue
    kb=$(size_kb "$host_dir"); [ -z "${kb:-}" ] && kb=0
    sk=0
    for sd in "$host_dir/skills" "$host_dir/skills-cursor"; do
      [ -d "$sd" ] && sk=$((sk + $(find "$sd" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')))
    done
    mcp="no"
    [ -f "$host_dir/mcp.json" ] || [ -f "$host_dir/.mcp.json" ] && mcp="yes"
    name=$(basename "$host_dir")
    printf "%s\t%s\t%s\t%d\t%s\n" "$name" "${host_dir/#$HOME/~}" "$(human "$kb")" "$sk" "$mcp"
  done
  echo
fi

# ── 5. 隐藏大户发现（找规则库没覆盖到的）────────────────
if [ "$QUICK" -eq 0 ]; then
  echo "## DISCOVER"
  echo "# 家目录下 >500MB 的点目录（含规则库未覆盖的）"
  printf "# size_kb\thuman\tpath\n"
  for d in "$HOME"/.[!.]*; do
    [ -d "$d" ] || continue
    kb=$(size_kb "$d"); [ -z "${kb:-}" ] && continue
    [ "$kb" -ge 512000 ] && printf "%s\t%s\t%s\n" "$kb" "$(human "$kb")" "${d/#$HOME/~}"
  done | sort -rn
  echo
fi

echo "## END"
echo "# 本次扫描全程只读，未改动或删除任何文件。"
