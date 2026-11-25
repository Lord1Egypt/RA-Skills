#!/usr/bin/env bash
# ============================================================
# 把技能库装进某个 agent 的技能目录（26 个技能，可只装几个）
#
# 用法:
#   bash tools/install_skills.sh --list                     # 先看有哪些技能
#   bash tools/install_skills.sh --target ~/.claude/skills   # 全部装进去
#   bash tools/install_skills.sh --target ~/.codex/skills --only owner-sell-home-advisor,broker-lease-sop
#   bash tools/install_skills.sh --target ./skills --link     # 符号链接（开发时改本仓库即生效）
#   bash tools/install_skills.sh --target ./skills --dry-run  # 只打印计划，不动文件
#
# 设计原则:
#   1. 只写 target 目录，不碰别处；拒绝把 / 或 $HOME 本身当 target
#   2. 目标里已有内容时默认不覆盖（防止冲掉别人改过的版本），要覆盖加 --force
#   3. 每次安装写一份 house-skills-kit.manifest.json（版本 + 每个技能 SKILL.md 的 sha256），
#      升级时能一眼看出哪些技能变了
# 退出码: 0 成功；2 有技能因已存在被跳过（需要 --force）；1 参数或环境错误
# ============================================================
set -uo pipefail

KIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="$KIT_DIR/skills"
CHANGELOG="$KIT_DIR/CHANGELOG.md"
MANIFEST_NAME="house-skills-kit.manifest.json"

TARGET=""
ONLY=""
MODE="copy"     # copy | link
FORCE=0
DRY=0
LIST=0

usage() {
  sed -n '3,18p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --target=*) TARGET="${1#*=}"; shift ;;
    --only) ONLY="${2:-}"; shift 2 ;;
    --only=*) ONLY="${1#*=}"; shift ;;
    --link) MODE="link"; shift ;;
    --force) FORCE=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    -h|--help) usage 0 ;;
    *) echo "[x] 不认识的参数: $1"; usage 1 ;;
  esac
done

[[ -d "$SKILLS_SRC" ]] || { echo "[x] 找不到 $SKILLS_SRC（请在仓库里运行这个脚本）"; exit 1; }

# ---------- 版本号：取 CHANGELOG 第一个版本段 ----------
kit_version() {
  if [[ -f "$CHANGELOG" ]]; then
    grep -m1 -oE '^## \[v[0-9]+\.[0-9]+\.[0-9]+\]' "$CHANGELOG" | sed -E 's/^## \[|\]$//g' || true
  fi
}

# ---------- 技能清单 ----------
all_skills() { ( cd "$SKILLS_SRC" && ls -1d */ 2>/dev/null | tr -d '/' ); }

skill_desc() {  # 每个技能的一句话：取 README 第一段正文（跳过标题/引用/代码块/表格/列表）
  local name="$1" f="$SKILLS_SRC/$1/README.md"
  [[ -f "$f" ]] || { echo ""; return; }
  awk '
    /^[[:space:]]*```/ { fence = !fence; next }
    fence { next }
    /^[[:space:]]*[|>`#-]/ { next }
    /^[[:space:]]*\*\*/ { gsub(/\*\*/, ""); sub(/^[[:space:]]+/, ""); print; exit }
    NF { print; exit }
  ' "$f" | python3 -c 'import sys; t=sys.stdin.read().strip(); print(t[:64] + ("…" if len(t) > 64 else ""))'
}

if [[ "$LIST" -eq 1 ]]; then
  n=0
  for s in $(all_skills); do
    n=$((n+1))
    printf '%2d. %-32s %s\n' "$n" "$s" "$(skill_desc "$s")"
  done
  echo
  echo "共 $n 个技能；版本 $(kit_version)"
  exit 0
fi

if [[ -z "$TARGET" ]]; then
  echo "[x] 缺少 --target（装到哪里）。先跑 --list 看清单，再用："
  echo "    bash tools/install_skills.sh --target ~/.claude/skills"
  exit 1
fi

# ---------- target 安全护栏 ----------
case "$TARGET" in
  /|"$HOME"|"$HOME"/) echo "[x] 拒绝把 $TARGET 当技能目录（会把技能直接铺在家目录/根目录）"; exit 1 ;;
esac
mkdir -p "$TARGET" 2>/dev/null || { echo "[x] 无法创建目录 $TARGET"; exit 1; }
TARGET_ABS="$(cd "$TARGET" && pwd)"

# ---------- 决定装哪些 ----------
if [[ -n "$ONLY" ]]; then
  WANT=()
  IFS=',' read -r -a raw <<< "$ONLY"
  for r in "${raw[@]}"; do
    r="$(echo "$r" | xargs)"
    [[ -z "$r" ]] && continue
    if [[ ! -d "$SKILLS_SRC/$r" ]]; then
      echo "[x] 没有这个技能: $r"
      echo "    可用清单: $(all_skills | tr '\n' ' ')"
      exit 1
    fi
    WANT+=("$r")
  done
else
  mapfile -t WANT < <(all_skills)
fi

echo "技能库版本: $(kit_version)  来源: $SKILLS_SRC"
echo "安装目标  : $TARGET_ABS  方式: $MODE"
[[ "$DRY" -eq 1 ]] && echo "（dry-run：只打印计划，不写文件）"
echo

# ---------- 逐个安装 ----------
added=0; updated=0; skipped=0; failed=0
declare -a SKIP_LIST=()
declare -a JSON_LINES=()

for s in "${WANT[@]}"; do
  src="$SKILLS_SRC/$s"
  dst="$TARGET_ABS/$s"
  sha_src="$(sha256sum "$src/SKILL.md" 2>/dev/null | cut -d' ' -f1)"
  nfiles="$(cd "$src" && find . -type f -name '*.md' | wc -l | tr -d ' ')"

  state="new"
  if [[ -e "$dst" ]]; then
    if [[ "$MODE" == "link" ]]; then
      state="skip-link"
    else
      sha_dst="$(sha256sum "$dst/SKILL.md" 2>/dev/null | cut -d' ' -f1)"
      if [[ -n "$sha_dst" && "$sha_dst" == "$sha_src" ]]; then
        state="unchanged"
      else
        state="exists-diff"
      fi
    fi
  fi

  case "$state" in
    unchanged)
      skipped=$((skipped+1)); echo "  = $s（已是最新，跳过）" ;;
    exists-diff)
      if [[ "$FORCE" -eq 1 ]]; then
        state="force"
      else
        skipped=$((skipped+1)); SKIP_LIST+=("$s"); echo "  ! $s（目标已存在且内容不同，未覆盖；要覆盖加 --force）"
      fi ;;
  esac

  if [[ "$DRY" -eq 1 ]]; then
    case "$state" in
      new)         echo "  + $s（将新增）"; added=$((added+1)) ;;
      force)       echo "  ↑ $s（将覆盖）"; updated=$((updated+1)) ;;
      skip-link)   echo "  ! $s（将替换为符号链接）"; updated=$((updated+1)) ;;
      unchanged)   : ;;
    esac
    JSON_LINES+=("{\"name\":\"$s\",\"files\":$nfiles,\"sha256\":\"$sha_src\"}")
    continue
  fi

  case "$state" in
    new|force|skip-link)
      rm -rf "$dst" 2>/dev/null || true
      if [[ "$MODE" == "link" ]]; then
        ln -sfn "$src" "$dst" && { echo "  → $s（符号链接）"; added=$((added+1)); } || { echo "  x $s 链接失败"; failed=$((failed+1)); }
      else
        if cp -R "$src" "$dst" 2>/dev/null; then
          [[ "$state" == "force" ]] && { echo "  ↑ $s（已覆盖）"; updated=$((updated+1)); } || { echo "  + $s"; added=$((added+1)); }
        else
          echo "  x $s 复制失败"; failed=$((failed+1))
        fi
      fi ;;
    unchanged) : ;;
  esac
  JSON_LINES+=("{\"name\":\"$s\",\"files\":$nfiles,\"sha256\":\"$sha_src\"}")
done

# ---------- 写 manifest ----------
if [[ "$DRY" -eq 0 && ${#JSON_LINES[@]} -gt 0 ]]; then
  {
    printf '{\n'
    printf '  "kit": "house-skills-kit",\n'
    printf '  "version": "%s",\n' "$(kit_version)"
    printf '  "installedAt": "%s",\n' "$(date -Iseconds)"
    printf '  "mode": "%s",\n' "$MODE"
    printf '  "target": "%s",\n' "$TARGET_ABS"
    printf '  "skills": [\n'
    total=${#JSON_LINES[@]}
    i=0
    for line in "${JSON_LINES[@]}"; do
      i=$((i+1))
      sep=","; [[ "$i" -eq "$total" ]] && sep=""
      printf '    %s%s\n' "$line" "$sep"
    done
    printf '  ]\n}\n'
  } > "$TARGET_ABS/$MANIFEST_NAME"
fi

echo
echo "结果：新增 $added ｜ 覆盖 $updated ｜ 跳过 $skipped ｜ 失败 $failed"
[[ "$DRY" -eq 0 ]] && echo "清单已写：$TARGET_ABS/$MANIFEST_NAME"
if [[ ${#SKIP_LIST[@]} -gt 0 ]]; then
  echo "未覆盖（需 --force）: ${SKIP_LIST[*]}"
  exit 2
fi
[[ "$failed" -gt 0 ]] && exit 1
exit 0
