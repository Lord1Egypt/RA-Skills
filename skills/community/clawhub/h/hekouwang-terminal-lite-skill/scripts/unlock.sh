#!/bin/bash
# ============================================================
# hekouwang-terminal-skill — 一条命令装上付费包
#
#   ./scripts/unlock.sh ~/Downloads/hekouwang-terminal-skill-paid-20260723.zip
#   ./scripts/unlock.sh <zip> --dry-run     只说要做什么，不动任何文件
#   ./scripts/unlock.sh <zip> --no-apply    解压并重新生成，但不重新部署主题
#
# 为什么要有这个脚本：
# 手工装付费包是「解压 → cd → 跑生成器 → 重新 apply 主题」四步，
# 其中最后一步最容易被跳过 —— 而跳过它的后果是**静默的**：
# 主题文件已经在盘上了，但 iTerm2 用的还是旧 Profile、bat 缓存里还没有新主题，
# 表现为「买了付费包，好像没什么变化」或者「只有 cat 的颜色不对」。
# 本脚本把四步收成一条，并且每步都验证结果。
#
# 走 private 仓的买家用不上这个脚本 —— 那边 git pull 完直接跑
# `cd config/themes && python3 _generate.py && cd ../.. && ./scripts/theme.sh <主题>` 即可。
# ============================================================
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/i18n.sh"
hkw_i18n_init unlock "$@"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/lib/aliases.sh"
eval set -- "$HKW_ARGS"
cd "$SCRIPT_DIR"

g='\033[1;32m'; r='\033[1;31m'; y='\033[1;33m'; b='\033[1;34m'; d='\033[2m'; o='\033[0m'
say()  { printf "${b}%s${o}\n" "$(t "$@")"; }
ok()   { printf "  ${g}✓${o} %s\n" "$(t "$@")"; }
bad()  { printf "  ${r}✗${o} %s\n" "$(t "$@")"; }
dim()  { printf "${d}%s${o}\n" "$(t "$@")"; }

RUNTIME="$HOME/.config/hekouwang-terminal"
# 付费包的指纹文件：这个在，才算真的是付费包
MARKER="config/themes/palettes/brand.py"

# ⚠️ 列包内文件别用 `unzip -Z1`：macOS 自带的是 Info-ZIP 6.00（2009 年），
#    它的**列表模式**会把非 ASCII 文件名里的字节替换成 `?`，吐出的不是合法 UTF-8。
#    后果有两层：① 屏幕上「速查卡.pdf」显示成乱码；② 这串非法字节喂给 BSD sed
#    会直接 `RE error: illegal byte sequence`，在正常流程里蹦出一行吓人的报错。
#    （**解压本身是好的** —— 实测 docs/速查卡.pdf 落盘文件名完全正确、`[ -f ]` 找得到，
#      因为打包时打了 UTF-8 标记 0x800。坏的只有列表模式。）
#    走 python3 的 zipfile 读文件名，它按 0x800 正确解码。python3 本来就是硬依赖
#    （后面要跑 _generate.py），不算新增依赖。
zip_names() {
  python3 -c '
import sys, zipfile
for n in zipfile.ZipFile(sys.argv[1]).namelist():
    if not n.endswith("/"):
        print(n)
' "$1"
}

ZIP=""; DRY=0; APPLY=1; ALLOW_DOWNGRADE=0; ROLLBACK=0; UPDATE_TX=""; UPDATE_ACTIVE=0
for a in "$@"; do
  case "$a" in
    --dry-run|-n) DRY=1 ;;
    --no-apply)   APPLY=0 ;;
    --allow-downgrade) ALLOW_DOWNGRADE=1 ;;
    --rollback) ROLLBACK=1 ;;
    -h|--help)    blk_unlock_help; exit 0 ;;
    -*)           printf "${r}%s${o}\n" "$(t M_UL_UNKNOWN_ARG "$a")"; exit 1 ;;
    *)            ZIP="$a" ;;
  esac
done

if [ "$ROLLBACK" = "1" ]; then
  if TX="$(python3 "$SCRIPT_DIR/lib/transaction.py" rollback latest-paid-update 2>/dev/null)"; then
    ok M_UL_ROLLBACK_OK "$(basename "$TX")"
    exit 0
  fi
  bad M_UL_ROLLBACK_NONE
  exit 1
fi

if [ -z "$ZIP" ]; then
  printf "${y}%s${o}\n\n" "$(t M_UL_USAGE)"
  dim M_UL_USAGE_1
  dim M_UL_USAGE_2
  dim M_UL_USAGE_3
  dim M_UL_USAGE_4
  exit 1
fi

# ---- 1. 校验：这个 zip 能用吗 --------------------------------
say M_UL_S1
[ -f "$ZIP" ] || { bad M_UL_NO_FILE "$ZIP"; exit 1; }
ok M_UL_FILE_OK "$(du -h "$ZIP" | cut -f1 | tr -d ' ')"

# ⚠️ 别跳过完整性校验：网盘/微信传输被截断的 zip 解压时会「部分成功」——
#    解出一半文件、退出码却可能是 0，然后生成器拿着残缺的色板跑出半套主题。
if unzip -tqq "$ZIP" >/dev/null 2>&1; then
  ok M_UL_ZIP_OK
else
  bad M_UL_ZIP_BAD; exit 1
fi

if zip_names "$ZIP" 2>/dev/null | grep -qx "$MARKER"; then
  ok M_UL_IS_PAID "$MARKER"
else
  bad M_UL_NOT_PAID "$MARKER"
  dim M_UL_YOUR_ZIP "$ZIP"
  exit 1
fi

# ---- 2. 校验：当前目录对吗 -----------------------------------
say M_UL_S2
if [ -f "$SCRIPT_DIR/scripts/theme.sh" ] && [ -f "$SCRIPT_DIR/config/themes/_generate.py" ]; then
  ok M_UL_DIR_OK "$SCRIPT_DIR"
else
  bad M_UL_DIR_BAD
  dim M_UL_DIR_FIX
  exit 1
fi

if [ -f "$MARKER" ]; then
  printf "  ${y}!${o} %s\n" "$(t M_UL_ALREADY)"
fi

# ⚠️ 版本比对：买家手里的免费仓可能停在旧版，而付费包是新的。
#    两边不一致时树里会同时存在两个版本号（VERSION 与包内 SKILL.md），
#    功能不会崩，但更新提示和 VS Code 扩展的版本号会对不上 —— 提醒一句，不拦。
ZIP_VER="$(python3 - "$ZIP" 2>/dev/null <<'PYVER'
import sys, zipfile
try:
    print(zipfile.ZipFile(sys.argv[1]).read("VERSION").decode().strip())
except Exception:
    pass
PYVER
)"
LOCAL_VER="$(tr -d '[:space:]' < "$SCRIPT_DIR/VERSION" 2>/dev/null)"
version_cmp() {
  python3 - "$1" "$2" <<'PY'
import re, sys
def v(s):
    return tuple(int(x) for x in re.findall(r'\d+', s)[:3])
print((v(sys.argv[1]) > v(sys.argv[2])) - (v(sys.argv[1]) < v(sys.argv[2])))
PY
}
if [ -n "$ZIP_VER" ] && [ -n "$LOCAL_VER" ] \
   && [ "$(version_cmp "$ZIP_VER" "$LOCAL_VER")" = "-1" ] \
   && [ "$ALLOW_DOWNGRADE" != "1" ]; then
  bad M_UL_DOWNGRADE_BLOCKED "$LOCAL_VER" "$ZIP_VER"
  dim M_UL_DOWNGRADE_HINT
  exit 1
fi
if [ -n "$ZIP_VER" ] && [ -n "$LOCAL_VER" ] && [ "$ZIP_VER" != "$LOCAL_VER" ]; then
  printf "  ${y}!${o} %s\n" "$(t M_UL_VER_SKEW "$LOCAL_VER" "$ZIP_VER")"
  printf "    ${d}%s${o}\n" "$(t M_UL_VER_SKEW_FIX)"
fi

# ---- 3. 预演 / 执行 ------------------------------------------
FILES="$(zip_names "$ZIP" 2>/dev/null | wc -l | tr -d ' ')"
say M_UL_S3 "$FILES"
if [ "$DRY" = "1" ]; then
  printf "\n${b}%s${o}\n\n" "$(t M_UL_DRY_HEAD)"
  printf "%s\n" "$(t M_UL_DRY_1 "$SCRIPT_DIR")"
  # 纯 shell 缩进，不走 sed —— 文件名里有中文时 BSD sed 是个雷
  zip_names "$ZIP" 2>/dev/null | head -20 | while IFS= read -r l; do printf '  %s\n' "$l"; done
  [ "$FILES" -gt 20 ] && printf "  ${d}%s${o}\n" "$(t M_UL_DRY_MORE "$((FILES - 20))")"
  printf "\n%s\n" "$(t M_UL_DRY_THEN)"
  printf "  cd config/themes && python3 _generate.py    ${d}%s${o}\n" "$(t M_UL_DRY_GEN)"
  [ "$APPLY" = "1" ] && printf "  ./scripts/theme.sh <theme>                          ${d}%s${o}\n" "$(t M_UL_DRY_APPLY)"
  printf "\n${d}%s${o}\n" "$(t M_UL_DRY_KEEP)"
  printf "${y}%s${o}\n" "$(t M_UL_DRY_TAIL)"
  exit 0
fi

# Snapshot only the product paths this update can overwrite. config/themes is
# one generated unit; other zip entries are listed individually.
UPDATE_PATHS="$(mktemp "${TMPDIR:-/tmp}/hkw-terminal-paid-update.XXXXXX")"
printf '%s\n' "$SCRIPT_DIR/config/themes" > "$UPDATE_PATHS"
zip_names "$ZIP" | while IFS= read -r rel; do
  case "$rel" in
    config/themes/*|把我解压到免费版目录里.txt) continue ;;
    *) printf '%s/%s\n' "$SCRIPT_DIR" "$rel" ;;
  esac
done >> "$UPDATE_PATHS"
UPDATE_TX="$(python3 "$SCRIPT_DIR/lib/transaction.py" snapshot --label "paid-update:$LOCAL_VER->$ZIP_VER" --paths "$UPDATE_PATHS")" || {
  rm -f "$UPDATE_PATHS"
  bad M_UL_SNAPSHOT_FAIL
  exit 1
}
rm -f "$UPDATE_PATHS"
UPDATE_ACTIVE=1
ok M_UL_SNAPSHOT_OK "$(basename "$UPDATE_TX")"
rollback_failed_update() {
  rc=$?
  if [ "$UPDATE_ACTIVE" = "1" ] && [ "$rc" != "0" ]; then
    if python3 "$SCRIPT_DIR/lib/transaction.py" rollback "$UPDATE_TX" >/dev/null 2>&1; then
      printf "  ${y}!${o} %s\n" "$(t M_UL_AUTO_ROLLBACK)"
    else
      printf "  ${r}✗${o} %s\n" "$(t M_UL_AUTO_ROLLBACK_FAIL "$UPDATE_TX")"
    fi
  fi
}
trap rollback_failed_update EXIT

# 付费包里那个「把我解压到免费版目录里.txt」是给手工装的人看的，
# 走本脚本就不需要它落在根目录了 —— 解完删掉，保持目录干净。
if unzip -o -q "$ZIP" -d "$SCRIPT_DIR"; then
  rm -f "$SCRIPT_DIR/把我解压到免费版目录里.txt"
  ok M_UL_UNPACKED "$FILES"
else
  bad M_UL_UNPACK_FAIL; exit 1
fi

# 解压完必须复验指纹落地了 —— unzip 对中文文件名的处理在个别环境下会出岔子，
# 光看退出码不够（打包时已打 UTF-8 标记 0x800，正常情况下不会有问题）。
[ -f "$MARKER" ] || { bad M_UL_MARKER_MISSING "$MARKER"; exit 1; }
ok M_UL_MARKER_OK

# ---- 4. 重新生成 ---------------------------------------------
say M_UL_S4
if OUT="$(cd "$SCRIPT_DIR/config/themes" && python3 _generate.py 2>&1)"; then
  printf '%s\n' "$OUT" | sed 's/^/  /'
  ok M_UL_GEN_OK
else
  printf '%s\n' "$OUT" | tail -10 | sed 's/^/  /'
  bad M_UL_GEN_FAIL; exit 1
fi

# ---- 5. 重新部署 ---------------------------------------------
if [ "$APPLY" = "0" ]; then
  say M_UL_S5_SKIP
  dim M_UL_S5_SKIP_NOTE
  exit 0
fi

say M_UL_S5
CUR="$(hkw_resolve_theme "$(cat "$RUNTIME/theme" 2>/dev/null || echo '')")"
if [ -n "$CUR" ] && [ -f "config/themes/$CUR.json" ]; then
  dim M_UL_KEEP_THEME "$CUR"
  TARGET="$CUR"
else
  # 没装过或当前主题是社区那三套之一 —— 直接给默认品牌主题，让人第一眼就看到买到了什么
  TARGET="ember"
  dim M_UL_SWITCH_THEME "$TARGET"
fi

if ./scripts/theme.sh "$TARGET"; then
  UPDATE_ACTIVE=0
  printf "\n${g}%s${o}\n" "$(t M_UL_DONE)"
  dim M_UL_DONE_1
  dim M_UL_DONE_2
  dim M_UL_DONE_3
  dim M_UL_DONE_4
  dim M_UL_DONE_5
  dim M_UL_DONE_6
else
  bad M_UL_APPLY_FAIL
  exit 1
fi
