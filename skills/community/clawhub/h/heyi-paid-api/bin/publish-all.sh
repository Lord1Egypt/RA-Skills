#!/usr/bin/env bash
# publish-all.sh — 把 heyi-paid-api Skill 一键发布到所有支持的市场
#
# 用法：
#   bin/publish-all.sh                    # status：每个平台读出当前已发布版本
#   bin/publish-all.sh skillhub           # 单独发布到 SkillHub
#   bin/publish-all.sh npm                # 单独发布到 npm
#   bin/publish-all.sh clawhub            # 单独检查 ClawHub（GitHub-based）
#   bin/publish-all.sh all                # 按顺序跑所有可自动化的平台
#
# 单一事实源：CHANGELOG.md 第一行 `## [x.y.z] - 日期` 读出版本号；package.json
# 与 SKILL.md frontmatter 在发布前必须已经 bump 到同一版本。
#
# 凭据通过环境变量提供（避免写进文件/日志）：
#   SKILLHUB_TOKEN          — SkillHub 的 skh_xxx
#   NPM_TOKEN               — npm 的 npm_xxx（或用 ~/.npmrc）
#   GITHUB_TOKEN            — 用于 ClawHub GitHub linking / SkillsMP 自动索引
#   LOBEHUB_TOKEN           — LobeHub API（如支持）

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHANGELOG="$SKILL_DIR/CHANGELOG.md"
PACKAGE_JSON="$SKILL_DIR/package.json"
SKILL_MD="$SKILL_DIR/SKILL.md"

SKILLHUB_API="${SKILLHUB_API:-https://api.skillhub.cn}"
CLAWHUB_API="${CLAWHUB_API:-https://api.clawdhub.ai}"
SKILLSMP_API="${SKILLSMP_API:-https://skillsmp.com/api/v1}"
LOBEHUB_API="${LOBEHUB_API:-https://lobehub.com}"
IFLYTEK_API="${IFLYTEK_API:-https://skill.xfyun.cn/api/web}"
NPM_REGISTRY="${NPM_REGISTRY:-https://registry.npmjs.org}"

C_RESET=$'\033[0m'; C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'
C_RED=$'\033[31m'; C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_BLUE=$'\033[34m'

say()  { printf '%s\n' "$*"; }
info() { printf '%s==>%s %s\n' "$C_BLUE" "$C_RESET" "$*"; }
ok()   { printf '%s✓%s %s\n' "$C_GREEN" "$C_RESET" "$*"; }
warn() { printf '%s!%s %s\n' "$C_YELLOW" "$C_RESET" "$*"; }
err()  { printf '%s✗%s %s\n' "$C_RED" "$C_RESET" "$*" >&2; }

usage() {
  sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# 从 CHANGELOG.md 顶部的 `## [x.y.z] - 日期` 读出当前版本
read_version() {
  awk '/^## \[[0-9]+\.[0-9]+\.[0-9]+\]/ { gsub(/[\[\]]/, "", $2); print $2; exit }' "$CHANGELOG"
}

# 从 package.json 读出版本
pkg_version() {
  /usr/bin/env python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['version'])" "$PACKAGE_JSON" 2>/dev/null || echo ""
}

assert_versions_match() {
  local v_changelog v_pkg v_md
  v_changelog="$(read_version)"
  v_pkg="$(pkg_version)"
  v_md="$(awk '/^version:/ { gsub(/^version: *|["'\'']/, ""); print; exit }' "$SKILL_MD")"

  if [[ -z "$v_changelog" ]]; then
    err "CHANGELOG.md 顶部找不到 ## [x.y.z] - 日期"
    exit 1
  fi
  if [[ "$v_changelog" != "$v_pkg" || "$v_changelog" != "$v_md" ]]; then
    err "版本不一致: CHANGELOG=$v_changelog package.json=$v_pkg SKILL.md=$v_md"
    err "请先 bump 到同一版本再发布"
    exit 1
  fi
  VERSION="$v_changelog"
  info "版本对齐：$VERSION"
}

# ──────────────────────────────────────────────────────────────────────────────
# SkillHub
# ──────────────────────────────────────────────────────────────────────────────
publish_skillhub() {
  info "SkillHub ($SKILLHUB_API) — 当前 $VERSION"

  if [[ -z "${SKILLHUB_TOKEN:-}" ]]; then
    warn "SKILLHUB_TOKEN 未设置，跳过"
    return 1
  fi

  # 1. 先查当前是否就是最新版（用公开 API，无需 token）
  local cur
  cur=$(/usr/bin/curl -sL --max-time 10 \
    "$SKILLHUB_API/api/v1/skills/heyi-paid-api" \
    | /usr/bin/env python3 -c "import json,sys; d=json.load(sys.stdin); print((d.get('latestVersion') or {}).get('version',''))" 2>/dev/null || echo "")
  if [[ "$cur" == "$VERSION" ]]; then
    ok "SkillHub 已是 $VERSION，跳过"
    return 0
  fi

  # 2. 上传 logo（idempotent）
  local logo_url=""
  local logo_path="/Users/heyi/work/gitcode/bot-frontend/public/logo.png"
  if [[ -f "$logo_path" ]]; then
    local icon_resp
    icon_resp=$(/usr/bin/curl -sL --max-time 30 -X POST \
      -H "Authorization: Bearer $SKILLHUB_TOKEN" \
      -F "files=@${logo_path};type=image/png" \
      "$SKILLHUB_API/api/v1/community/skill-icons/upload" 2>/dev/null || true)
    logo_url=$(printf '%s' "$icon_resp" | /usr/bin/env python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('iconUrl') or d.get('url') or '')" 2>/dev/null || echo "")
  fi

  # 3. 读 SKILL.md，去掉触发词/iconUrl；包成 multipart payload
  local payload
  payload=$(/usr/bin/env python3 - "$SKILL_MD" "$logo_url" <<'PY'
import sys, re, yaml, json
path, icon_url = sys.argv[1], sys.argv[2]
with open(path, encoding='utf-8') as f:
    text = f.read()
m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
fm = yaml.safe_load(m.group(1))
body = m.group(2)
# SkillHub frontmatter 是行级 last-wins，把嵌套 description 改名为 note 避免被外层覆盖
flat_yaml = re.sub(r'^(\s+)description:', r'\1note:', m.group(1), flags=re.MULTILINE)
fm = yaml.safe_load(flat_yaml)
fm['iconUrl'] = icon_url or fm.get('iconUrl', '')
fm.pop('triggers', None)
fm['readme'] = body.strip()
print(json.dumps({'skill': fm}, ensure_ascii=False))
PY
)

  /usr/bin/curl -sL --max-time 60 -X POST \
    -H "Authorization: Bearer $SKILLHUB_TOKEN" \
    -F "payload=${payload}" \
    -F "files=@${SKILL_MD}" \
    "$SKILLHUB_API/api/v1/community/skills/publish" \
    -o /tmp/skillhub_publish.json -w "  HTTP %{http_code}\n"

  if /usr/bin/env python3 -c "import json,sys; d=json.load(open('/tmp/skillhub_publish.json')); sys.exit(0 if d.get('version') else 1)" 2>/dev/null; then
    ok "SkillHub 发布成功 $VERSION"
  else
    err "SkillHub 发布失败，响应："
    cat /tmp/skillhub_publish.json >&2
    return 1
  fi
}

status_skillhub() {
  local resp ver
  resp=$(/usr/bin/curl -sL --max-time 10 \
    ${SKILLHUB_TOKEN:+-H "Authorization: Bearer $SKILLHUB_TOKEN"} \
    "$SKILLHUB_API/api/v1/skills/heyi-paid-api" 2>/dev/null || echo "")
  ver=$(printf '%s' "$resp" | /usr/bin/env python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    v=d.get('latestVersion') or {}
    print(v.get('version','?'))
except Exception:
    print('?')
" 2>/dev/null)
  if [[ "$ver" == "$VERSION" ]]; then
    printf "  %-12s %-10s  %s\n" "SkillHub" "$ver" "✓ up-to-date"
  elif [[ "$ver" == "?" ]]; then
    printf "  %-12s %-10s  %s\n" "SkillHub" "?" "未收录"
  else
    printf "  %-12s %-10s  %s\n" "SkillHub" "$ver" "← 当前 $VERSION"
  fi
}

# ──────────────────────────────────────────────────────────────────────────────
# npm
# ──────────────────────────────────────────────────────────────────────────────
publish_npm() {
  info "npm ($NPM_REGISTRY) — 当前 $VERSION"
  if ! command -v npm >/dev/null; then
    warn "npm 未安装，跳过"
    return 1
  fi

  local pkg_name
  pkg_name=$(/usr/bin/env python3 -c "import json; print(json.load(open('$PACKAGE_JSON'))['name'])")

  local cur
  cur=$(/usr/bin/curl -sL --max-time 10 "$NPM_REGISTRY/$pkg_name" \
    | /usr/bin/env python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('version', 'none'))" 2>/dev/null || echo "none")
  if [[ "$cur" == "$VERSION" ]]; then
    ok "$pkg_name@$VERSION 已发布，跳过"
    return 0
  fi

  (
    cd "$SKILL_DIR"
    # npm publish 必须能登录
    if [[ -n "${NPM_TOKEN:-}" ]]; then
      NPM_CONFIG_TOKEN="$NPM_TOKEN" npm publish --registry="$NPM_REGISTRY"
    else
      npm publish --registry="$NPM_REGISTRY"
    fi
  )
  ok "$pkg_name@$VERSION 发布成功"
}

status_npm() {
  local pkg_name ver
  pkg_name=$(/usr/bin/env python3 -c "import json; print(json.load(open('$PACKAGE_JSON'))['name'])")
  ver=$(/usr/bin/curl -sL --max-time 10 "$NPM_REGISTRY/$pkg_name" \
    | /usr/bin/env python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    print(d.get('dist-tags',{}).get('latest','?'))
except Exception:
    print('?')
" 2>/dev/null)
  if [[ "$ver" == "$VERSION" ]]; then
    printf "  %-12s %-10s  %s\n" "npm" "$ver" "✓ up-to-date"
  elif [[ "$ver" == "?" ]]; then
    printf "  %-12s %-10s  %s\n" "npm" "404" "← 当前 $VERSION · 包名待发布"
  else
    printf "  %-12s %-10s  %s\n" "npm" "$ver" "← 当前 $VERSION"
  fi
}

# ──────────────────────────────────────────────────────────────────────────────
# ClawHub (clawdhub.ai) — npm CLI + GitHub OAuth device flow
# ──────────────────────────────────────────────────────────────────────────────
CLAWHUB_BIN="${CLAWHUB_BIN:-npx -y clawhub@latest --registry=$CLAWHUB_API}"

publish_clawhub() {
  info "ClawHub ($CLAWHUB_API) — 当前 $VERSION"

  if [[ -n "${CLAWHUB_TOKEN:-}" ]]; then
    info "用 CLAWHUB_TOKEN 直接登录"
    echo "$CLAWHUB_TOKEN" | $CLAWHUB_BIN login --label "publish-all.sh @ $VERSION" --no-input >/dev/null 2>&1 || true
  elif ! $CLAWHUB_BIN whoami --no-input >/dev/null 2>&1; then
    info "未登录，启动 device flow："
    warn "执行： npx clawhub login --no-browser"
    warn "它会打印 verification URL + user_code。"
    warn "你在浏览器打开 URL、输入 code、用 GitHub 授权 clawdhub。授权完成后 CLI 自动收到 token 并保存到 ~/.config/clawhub/credentials。"
    warn "授权完成后重跑本脚本即可。"
    return 1
  fi

  # 检查是否已发布该版本
  local cur owner
  owner="${CLAWHUB_OWNER:-heyi-byte}"
  cur=$($CLAWHUB_BIN inspect "heyi-paid-api" --no-input 2>/dev/null \
    | /usr/bin/env python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('latestVersion',{}).get('version',''))" 2>/dev/null || echo "")
  if [[ "$cur" == "$VERSION" ]]; then
    ok "ClawHub 已是 $VERSION，跳过"
    return 0
  fi

  # publish：把 skill 目录作为 path 传过去
  # --source-commit 必须与 --source-repo 同时给，自动从 git 读
  local commit_sha
  commit_sha="$(git -C "$SKILL_DIR" rev-parse HEAD 2>/dev/null || echo "")"
  $CLAWHUB_BIN skill publish "$SKILL_DIR" \
    --slug heyi-paid-api \
    --owner "$owner" \
    --version "$VERSION" \
    ${commit_sha:+--source-repo "${GITHUB_REPO:-heyi-byte/heyihub-skill}"} \
    ${commit_sha:+--source-commit "$commit_sha"} \
    --source-ref "${CLAWHUB_SOURCE_REF:-main}" \
    --source-path "docs/skills/heyi-paid-api/SKILL.md" \
    --tags "${CLAWHUB_TAGS:-latest}" \
    --changelog "$(awk '/^## \['"$VERSION"'\]/{f=1; next} f && /^## /{exit} f' "$CHANGELOG" | sed '/^$/d' | head -10 | paste -sd ' ' -)"
  ok "ClawHub 发布请求已提交，registry 端审核通过即生效"
}

status_clawhub() {
  local resp ver
  resp=$(/usr/bin/curl -sL --max-time 10 "$CLAWHUB_API/skills/heyi-paid-api" 2>/dev/null || echo "")
  ver=$(printf '%s' "$resp" | /usr/bin/env python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    print(d.get('latestVersion',{}).get('version','?'))
except Exception:
    print('?')
" 2>/dev/null)
  if [[ "$ver" == "$VERSION" ]]; then
    printf "  %-12s %-10s  %s\n" "ClawHub" "$ver" "✓ up-to-date"
  elif [[ "$ver" == "?" ]]; then
    printf "  %-12s %-10s  %s\n" "ClawHub" "—" "未收录 · 跑 publish-all.sh clawhub"
  else
    printf "  %-12s %-10s  %s\n" "ClawHub" "$ver" "← 当前 $VERSION"
  fi
}

# ──────────────────────────────────────────────────────────────────────────────
# SkillsMP — auto-indexed search engine
# ──────────────────────────────────────────────────────────────────────────────
publish_skillsmp() {
  info "SkillsMP — 自动索引 GitHub 仓库"
  warn "无需发布。确保 ${GITHUB_REPO:-heyi-byte/heyihub-skill} 公开，"
  warn "GitHub Actions / robots / README 中含 SKILL.md 链接，爬虫会自己抓。"
  warn "手动触发：https://skillsmp.com/submit (如该页面存在)"
  return 0
}

status_skillsmp() {
  local hit
  hit=$(/usr/bin/curl -sL --max-time 10 "$SKILLSMP_API/skills/search?q=heyi-paid-api" \
    | /usr/bin/env python3 -c "import json,sys; d=json.load(sys.stdin); skills=d.get('data',{}).get('skills',[]); print(skills[0].get('name','no') if skills else 'no')" 2>/dev/null || echo "?")
  printf "  %-12s %-10s  %s\n" "SkillsMP" "$hit" " ← 自动索引 GitHub"
}

# ──────────────────────────────────────────────────────────────────────────────
# LobeHub
# ──────────────────────────────────────────────────────────────────────────────
publish_lobehub() {
  info "LobeHub — 暂未找到稳定的发布 API"
  warn "手动步骤：打开 https://lobehub.com/mcp 或 https://lobehub.com/discover"
  warn "检查是否能 'Submit a Skill' 走 GitHub 链接。"
  warn "如已开通，把 LOBEHUB_TOKEN 设进环境变量重跑。"
  return 0
}

status_lobehub() {
  local hit
  hit=$(/usr/bin/curl -sLI --max-time 6 "https://lobehub.com/skills/heyi-paid-api" -o /dev/null -w "%{http_code}")
  printf "  %-12s %-10s  %s\n" "LobeHub" "$hit" " ← 404 = 还没收录"
}

# ──────────────────────────────────────────────────────────────────────────────
# iFlytek SkillHub (skill.xfyun.cn)
# ──────────────────────────────────────────────────────────────────────────────
status_iflytek() {
  warn "iFlytek Skill Hub 当前 ${C_RED}不可自助注册${C_RESET}（POST /api/v1/auth/local/register 返回 403）"
  warn "需 iFlytek 内部邀请开通账号后再走 ${IFLYTEK_API}/skills/{ns}/{slug}/submit-review"
}

# ──────────────────────────────────────────────────────────────────────────────
# Driver
# ──────────────────────────────────────────────────────────────────────────────
cmd="${1:-status}"
case "$cmd" in
  -h|--help|help) usage ;;
esac

assert_versions_match

say ""
say "${C_BOLD}heyi-paid-api Skill 多平台发布器${C_RESET}"
say "版本: $VERSION"
say ""

# 默认 status：跑 read-only 检查
if [[ "$cmd" == "status" || "$cmd" == "all" ]]; then
  say "${C_BOLD}Status${C_RESET}"
  status_skillhub
  status_npm
  status_clawhub
  status_skillsmp
  status_lobehub
  say ""
  status_iflytek
fi

if [[ "$cmd" == "skillhub" || "$cmd" == "all" ]]; then
  say ""
  say "${C_BOLD}SkillHub${C_RESET}"
  publish_skillhub || true
fi

if [[ "$cmd" == "npm" || "$cmd" == "all" ]]; then
  say ""
  say "${C_BOLD}npm${C_RESET}"
  publish_npm || true
fi

if [[ "$cmd" == "clawhub" || "$cmd" == "all" ]]; then
  say ""
  say "${C_BOLD}ClawHub${C_RESET}"
  publish_clawhub || true
fi

if [[ "$cmd" == "skillsmp" || "$cmd" == "all" ]]; then
  say ""
  say "${C_BOLD}SkillsMP${C_RESET}"
  publish_skillsmp || true
fi

if [[ "$cmd" == "lobehub" || "$cmd" == "all" ]]; then
  say ""
  say "${C_BOLD}LobeHub${C_RESET}"
  publish_lobehub || true
fi

say ""
say "${C_DIM}Done.${C_RESET}"
