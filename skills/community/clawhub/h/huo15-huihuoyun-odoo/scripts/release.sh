#!/usr/bin/env bash
#
# scripts/release.sh — @huo15/openclaw-enhance 一键串行发版
#
# 用法：
#   bash scripts/release.sh <version>            # 正式发版
#   bash scripts/release.sh --dry-run <version>  # 仅跑预检 + 模拟，不发任何动作
#
# 例：
#   bash scripts/release.sh 5.7.27
#   bash scripts/release.sh --dry-run 5.7.27
#   npm run release -- 5.7.27                    # 走 npm scripts
#
# 设计原则（参考 ~/CLAUDE.md §11.5 跨会话开工 + §11.3 发版自查）：
#
#   1. 预检（11 项）必须全部通过；任何一项失败立刻退出，零副作用
#   2. 不可逆动作按依赖顺序串行；任何一步失败 set -e 退出
#   3. 不修改任何源文件——脚本只校验对齐，bump 由调用者预先完成
#   4. 三处版本必须对齐：package.json / SKILL.md frontmatter / CHANGELOG 顶部段
#   5. 解决长期遗留：杜绝 SKILL.md frontmatter 落后于 npm 的情况
#
# 不可逆动作清单（依赖顺序）：
#   git tag v$VERSION
#   git push origin main + tag
#   git push github main + tag（如 github remote 存在）
#   npm publish
#   clawhub publish "$(pwd)" --version $VERSION

set -euo pipefail

# ---------- 颜色 + 日志 helper ----------
if [[ -t 1 ]]; then
  C_BLUE=$'\033[34m'
  C_GREEN=$'\033[32m'
  C_RED=$'\033[31m'
  C_YELLOW=$'\033[33m'
  C_DIM=$'\033[2m'
  C_RESET=$'\033[0m'
else
  C_BLUE=""; C_GREEN=""; C_RED=""; C_YELLOW=""; C_DIM=""; C_RESET=""
fi

log_step() { echo "${C_BLUE}▶${C_RESET} $*"; }
log_ok()   { echo "${C_GREEN}✓${C_RESET} $*"; }
log_warn() { echo "${C_YELLOW}⚠${C_RESET} $*"; }
log_err()  { echo "${C_RED}✗${C_RESET} $*" >&2; }
log_dim()  { echo "${C_DIM}  $*${C_RESET}"; }

# ---------- 参数解析 ----------
DRY_RUN=0
VERSION=""

for arg in "$@"; do
  case "$arg" in
    --dry-run|-n)
      DRY_RUN=1
      ;;
    --help|-h)
      sed -n '3,16p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    -*)
      log_err "未知 flag: $arg"
      exit 64
      ;;
    *)
      if [[ -n "$VERSION" ]]; then
        log_err "version 只能传一次（已经是 $VERSION，又传了 $arg）"
        exit 64
      fi
      VERSION="$arg"
      ;;
  esac
done

if [[ -z "$VERSION" ]]; then
  log_err "缺 version 参数"
  echo "用法: bash scripts/release.sh [--dry-run] <version>"
  exit 64
fi

if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.-]+)?$ ]]; then
  log_err "version 格式不对：$VERSION（要 SemVer 例如 5.7.27 或 5.7.27-rc.1）"
  exit 64
fi

TAG="v$VERSION"
PKG_NAME="$(node -p "require('./package.json').name")"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [[ $DRY_RUN -eq 1 ]]; then
  log_warn "DRY-RUN 模式：只跑预检和模拟，不会发版任何东西"
fi
echo "📦 包：${C_BLUE}$PKG_NAME${C_RESET}"
echo "🏷  版本：${C_BLUE}$VERSION${C_RESET}"
echo "📍 路径：$REPO_ROOT"
echo

# ---------- 预检 ----------
log_step "[1/11] 工作树干净 + main 分支"
if [[ -n "$(git status --porcelain)" ]]; then
  log_err "工作树有未提交改动；请先 commit 或 stash"
  git status --short
  exit 1
fi
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" != "main" ]]; then
  log_err "当前在 '$BRANCH' 分支；发版必须在 main"
  exit 1
fi
log_ok "工作树干净，在 main"

log_step "[2/11] 远端同步（git fetch + ahead/behind 检查）"
# 不带 --tags：避免本地老 tag 跟远端不同 SHA 时报 "would clobber existing tag"
# 阻塞 fetch；脚本后续只校验本地 tag 状态，不依赖远端 tag 同步
git fetch origin main 2>&1 | sed 's/^/  /'
AHEAD="$(git log --oneline origin/main..HEAD | wc -l | tr -d ' ')"
BEHIND="$(git log --oneline HEAD..origin/main | wc -l | tr -d ' ')"
if [[ "$BEHIND" -gt 0 ]]; then
  log_err "本地落后 origin/main $BEHIND 个 commit；先 pull / rebase 再发版"
  git log --oneline HEAD..origin/main | head -5
  exit 1
fi
if [[ "$AHEAD" -eq 0 ]]; then
  log_warn "本地领先 origin/main 0 个 commit（可能是已发版重跑）"
fi
log_ok "远端同步：领先 $AHEAD / 落后 0"

log_step "[3/11] package.json.version == $VERSION"
PKG_VERSION="$(node -p "require('./package.json').version")"
if [[ "$PKG_VERSION" != "$VERSION" ]]; then
  log_err "package.json.version=$PKG_VERSION ≠ 传入的 $VERSION"
  log_dim "先改 package.json + commit，再跑 release"
  exit 1
fi
log_ok "package.json.version=$VERSION"

log_step "[4/11] SKILL.md frontmatter version == $VERSION"
if [[ -f SKILL.md ]]; then
  SKILL_VERSION="$(awk '/^---$/{f++;next} f==1 && /^version:/{print $2; exit}' SKILL.md)"
  if [[ "$SKILL_VERSION" != "$VERSION" ]]; then
    log_err "SKILL.md frontmatter version=$SKILL_VERSION ≠ $VERSION"
    log_dim "先改 SKILL.md + commit，再跑 release（防 ClawHub plugin tag 落后于 npm）"
    exit 1
  fi
  log_ok "SKILL.md frontmatter version=$VERSION"
else
  log_warn "无 SKILL.md（非 ClawHub 项目？跳过）"
fi

log_step "[5/11] CHANGELOG.md 顶部段是 ## $VERSION"
if [[ -f CHANGELOG.md ]]; then
  if ! grep -qE "^## $VERSION( |\$|—|-)" CHANGELOG.md; then
    log_err "CHANGELOG.md 找不到 '## $VERSION ...' 段"
    log_dim "先在 CHANGELOG 顶部加 v$VERSION 段 + commit，再跑 release"
    exit 1
  fi
  TOP_VERSION="$(grep -m1 -E '^## ' CHANGELOG.md | sed -E 's/^## ([^ ]+).*/\1/')"
  if [[ "$TOP_VERSION" != "$VERSION" ]]; then
    log_err "CHANGELOG 顶部段是 '## $TOP_VERSION'，不是 '## $VERSION'"
    log_dim "v$VERSION 段必须在最上面（最新版本在最前）"
    exit 1
  fi
  log_ok "CHANGELOG 顶部段=## $VERSION"
else
  log_warn "无 CHANGELOG.md（跳过）"
fi

log_step "[6/11] typecheck (npx tsc --noEmit)"
if [[ -f tsconfig.json ]]; then
  if ! npx tsc --noEmit 2>&1 | tee /tmp/release-typecheck.log; then
    log_err "typecheck 失败；详见 /tmp/release-typecheck.log"
    exit 1
  fi
  log_ok "typecheck 通过"
else
  log_warn "无 tsconfig.json（非 TS 项目？跳过）"
fi

log_step "[7/11] openclaw.compat.pluginApi 是 ranged spec"
RAW_PA="$(node -p "require('./package.json').openclaw?.compat?.pluginApi || ''")"
RAW_PEER="$(node -p "require('./package.json').peerDependencies?.openclaw || ''")"
check_ranged() {
  local field="$1" val="$2"
  [[ -z "$val" ]] && return 0
  if [[ "$val" =~ ^(\>=|\<=|\>|\<|\^|~|=|\*) ]] || [[ "$val" =~ \  ]]; then
    log_dim "$field=$val（ranged ✓）"
    return 0
  fi
  if [[ "$val" =~ ^[0-9] ]]; then
    log_err "$field=$val 是 bare 版本；改成 \">=$val\" 或 \"^$val\"（CLAUDE.md §6.1 红线）"
    return 1
  fi
}
RANGED_OK=0
check_ranged "openclaw.compat.pluginApi" "$RAW_PA" || RANGED_OK=1
check_ranged "peerDependencies.openclaw" "$RAW_PEER" || RANGED_OK=1
[[ $RANGED_OK -eq 0 ]] || exit 1
log_ok "pluginApi / peerDep 都是 ranged"

log_step "[8/11] 无 child_process / execSync / spawnSync import（CLAUDE.md §6.2 红线）"
HITS="$(grep -rE "^\s*import .*from .['\"](node:)?child_process['\"]" --include="*.ts" --include="*.js" src/ index.ts 2>/dev/null || true)"
if [[ -n "$HITS" ]]; then
  log_err "命中 child_process import："
  echo "$HITS" | sed 's/^/  /'
  exit 1
fi
log_ok "无 child_process import"

log_step "[9/11] npm latest != $VERSION（防幽灵占用）"
NPM_LATEST="$(npm view "$PKG_NAME" version 2>/dev/null || echo "")"
if [[ "$NPM_LATEST" == "$VERSION" ]]; then
  log_err "npm 上 $PKG_NAME 已经是 $VERSION（幽灵占用？）；bump 到下一个 patch（如 ${VERSION}.1）"
  exit 1
fi
log_ok "npm latest=$NPM_LATEST，可发 $VERSION"

log_step "[10/11] tag $TAG 不存在或指向当前 HEAD"
HEAD_SHA="$(git rev-parse HEAD)"
if git rev-parse "$TAG" >/dev/null 2>&1; then
  TAG_SHA="$(git rev-parse "$TAG^{commit}")"
  if [[ "$TAG_SHA" != "$HEAD_SHA" ]]; then
    log_err "tag $TAG 已存在且指向 $TAG_SHA ≠ HEAD $HEAD_SHA"
    log_dim "先 'git tag -d $TAG && git push origin :refs/tags/$TAG'，或者 bump 到下一个版本"
    exit 1
  fi
  TAG_REUSING=1
  log_warn "tag $TAG 已指向当前 HEAD，跳过 git tag"
else
  TAG_REUSING=0
  log_ok "tag $TAG 不存在，可创建"
fi

log_step "[11/11] github remote 探测"
HAS_GITHUB=0
if git remote get-url github >/dev/null 2>&1; then
  HAS_GITHUB=1
  GITHUB_URL="$(git remote get-url github)"
  log_ok "github remote: $GITHUB_URL（会一起 push）"
else
  log_warn "无 github remote，跳过镜像 push"
fi

echo
log_ok "${C_GREEN}全部 11 项预检通过${C_RESET}"
echo

# ---------- 不可逆动作 ----------
if [[ $DRY_RUN -eq 1 ]]; then
  echo "${C_YELLOW}=== DRY-RUN：以下动作 NOT 执行 ===${C_RESET}"
  [[ $TAG_REUSING -eq 0 ]] && echo "  • git tag $TAG"
  echo "  • git push origin main"
  echo "  • git push origin $TAG"
  if [[ $HAS_GITHUB -eq 1 ]]; then
    echo "  • git push github main"
    echo "  • git push github $TAG"
  fi
  echo "  • npm publish"
  echo "  • clawhub publish \"\$(pwd)\" --slug huo15-huihuoyun-odoo --version $VERSION --tags latest,plugin"
  echo
  log_ok "DRY-RUN 完成。去掉 --dry-run 即正式发版"
  exit 0
fi

echo "${C_YELLOW}=== 正式发版（不可逆，从这里起任何失败需手动收拾）===${C_RESET}"
echo

if [[ $TAG_REUSING -eq 0 ]]; then
  log_step "git tag $TAG"
  git tag "$TAG"
  log_ok "tag $TAG 已创建"
fi

log_step "git push origin main + $TAG"
git push origin main 2>&1 | sed 's/^/  /'
git push origin "$TAG" 2>&1 | sed 's/^/  /'
log_ok "origin（cnb）同步完成"

if [[ $HAS_GITHUB -eq 1 ]]; then
  log_step "git push github main + $TAG"
  if ! git push github main 2>&1 | sed 's/^/  /'; then
    log_err "github main push 失败——npm/clawhub 还没发，可重新跑"
    exit 1
  fi
  if ! git push github "$TAG" 2>&1 | sed 's/^/  /'; then
    log_err "github tag push 失败——cnb 已同步但 github 镜像滞后；手动补 'git push github $TAG'"
  fi
  log_ok "github 镜像同步完成"
fi

log_step "npm publish"
if ! npm publish 2>&1 | sed 's/^/  /'; then
  log_err "npm publish 失败——git tag 已推但 npm 没发；不要重打 tag，重跑 'npm publish' 即可"
  exit 1
fi
log_ok "npm publish 完成"

log_step "clawhub publish $VERSION"
if [[ -z "${CLAWHUB_TOKEN:-}" ]]; then
  log_warn "CLAWHUB_TOKEN 未设；从 ~/CLAUDE.md §2 取或 export 后重跑这一步"
  log_warn "${C_YELLOW}手动收尾：CLAWHUB_TOKEN=clh_... clawhub publish \"\$(pwd)\" --slug huo15-huihuoyun-odoo --version $VERSION --tags latest,plugin${C_RESET}"
  exit 1
fi
# v1.21.0 起锁 ClawHub slug + 加 --tags latest,plugin 让每次发版同时刷两个 tag。
# SKILL.md frontmatter name=huo15-claude-odoo 跟实际 slug huo15-huihuoyun-odoo 不同——显式指定避免歧义。
CLAWHUB_SLUG="huo15-huihuoyun-odoo"
if ! clawhub publish "$(pwd)" --slug "$CLAWHUB_SLUG" --version "$VERSION" --tags latest,plugin 2>&1 | sed 's/^/  /'; then
  log_err "clawhub publish 失败——npm 已发；手动重跑 'CLAWHUB_TOKEN=... clawhub publish \"\$(pwd)\" --slug $CLAWHUB_SLUG --version $VERSION --tags latest,plugin'"
  exit 1
fi
log_ok "clawhub publish 完成（slug=$CLAWHUB_SLUG，已刷 latest+plugin 两个 tag）"

echo
log_ok "${C_GREEN}🎉 $PKG_NAME@$VERSION 全链路发版成功${C_RESET}"
log_dim "  cnb:     git tag $TAG → main"
[[ $HAS_GITHUB -eq 1 ]] && log_dim "  github:  $TAG → main"
log_dim "  npm:     $PKG_NAME@$VERSION"
log_dim "  clawhub: huo15-openclaw-enhance@$VERSION"
