#!/usr/bin/env bash
# github_push.sh — Step 9: GitHub push（内网 Basic Auth header 注入 + 5 次重试）
# Usage: ./github_push.sh <fork-path> <handle/repo | repo-name>
# 第二个参数若不含 /，自动用 OSG_GITHUB_HANDLE / profile.env 拼前缀
set -euo pipefail

. "$(dirname "$0")/_lib_profile.sh"
osg_resolve_identity

FORK="${1:-}"
REPO_RAW="${2:-}"

if [[ -z "$FORK" || -z "$REPO_RAW" ]]; then
  cat <<EOF >&2
Usage: $0 <fork-path> <repo-spec>

  repo-spec 可以是:
    full     <handle>/<repo>   例: alice/my-skill
    short    <repo>            自动拼 \$OSG_GITHUB_HANDLE/<repo>

  example:
    $0 ~/opensourceskills/my-skill my-skill
    $0 ~/opensourceskills/my-skill alice/my-skill

GitHub token 来源优先级:
  1. GITHUB_TOKEN
  2. OSG_GITHUB_TOKEN
  3. OSG_GITHUB_TOKEN_CMD（推荐配置项，如 "gh auth token" 或 macOS Keychain 读取命令）
  4. gh auth token（已登录 GitHub CLI 时自动读取）

⚠️  不会把 token 写入 git remote 或命令输出。若使用一次性 PAT，推送完成后请撤销。

首次配置 OSG_GITHUB_HANDLE: bash $(dirname "$0")/setup_profile.sh
EOF
  exit 1
fi

# 短格式自动拼前缀
if [[ "$REPO_RAW" == */* ]]; then
  REPO="$REPO_RAW"
else
  if [[ -z "${OSG_GITHUB_HANDLE:-}" ]]; then
    echo "❌ repo-spec 不含 '/' 且 OSG_GITHUB_HANDLE 未配置" >&2
    echo "   解决: bash $(dirname "$0")/setup_profile.sh 或显式传 <handle>/<repo>" >&2
    exit 7
  fi
  REPO="$OSG_GITHUB_HANDLE/$REPO_RAW"
  echo "ℹ️  Short form detected, expanded to: $REPO"
fi

if ! osg_resolve_github_token; then
  cat <<EOF >&2
❌ GitHub token 未配置

任选一种方式配置：
  ① 临时一次性：GITHUB_TOKEN=ghp_xxx $0 <fork-path> <repo-spec>
  ② 长期环境变量：export OSG_GITHUB_TOKEN=ghp_xxx
  ③ 推荐配置项：在 $(osg_profile_path) 写入
       OSG_GITHUB_TOKEN_CMD="gh auth token"
     或 macOS Keychain 读取命令，例如：
       OSG_GITHUB_TOKEN_CMD="security find-generic-password -a \$USER -s opensource-skill-to-github.github-token -w"

如果用一次性 PAT，推送完成后请去 GitHub Settings → Tokens 撤销。
EOF
  exit 2
fi
GITHUB_TOKEN_VALUE="$OSG_RESOLVED_GITHUB_TOKEN"
echo "ℹ️  GitHub token source: $OSG_RESOLVED_GITHUB_TOKEN_SOURCE"

[[ -d "$FORK/.git" ]] || { echo "❌ Not a git repo: $FORK" >&2; exit 3; }

# 发布前清理派生缓存（__pycache__/*.pyc 等，避免被 git add 进仓库）
. "$(dirname "$0")/_lib_exclude.sh"
osg_clean_fork "$FORK"

cd "$FORK"

# 添加 remote（如果不存在，URL 不含 token）
REMOTE_URL="https://github.com/$REPO.git"
if git remote get-url origin >/dev/null 2>&1; then
  current="$(git remote get-url origin)"
  if [[ "$current" != "$REMOTE_URL" ]]; then
    echo "ℹ️  origin 已存在但 URL 不一致，更新："
    echo "    old: $current"
    echo "    new: $REMOTE_URL"
    git remote set-url origin "$REMOTE_URL"
  fi
else
  git remote add origin "$REMOTE_URL"
  echo "✅ git remote add origin $REMOTE_URL"
fi

# Basic Auth header 注入（bearer 已不认）
AUTH_B64="$(printf "x-access-token:%s" "$GITHUB_TOKEN_VALUE" | base64 -w0 2>/dev/null || \
           printf "x-access-token:%s" "$GITHUB_TOKEN_VALUE" | base64 | tr -d '\n')"

# ─── 预探测：repo 是否已在 GitHub 上存在 ─────────
echo ""
echo "🔎 探测 GitHub repo 是否已存在..."
if command -v curl >/dev/null 2>&1; then
  http_code=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Basic $AUTH_B64" \
    -H "Accept: application/vnd.github+json" \
    --max-time 10 \
    "https://api.github.com/repos/$REPO" 2>/dev/null || echo "000")
  case "$http_code" in
    200)
      echo "✅ Repo 已存在，可以 push"
      ;;
    404)
      cat <<EOF >&2
❌ Repo $REPO 不存在！请用户先在浏览器创建：
   https://github.com/new
   - Repository name: $(basename "$REPO")
   - 不要勾 README / LICENSE / .gitignore（本地已生成）
   - 默认分支选 main
EOF
      exit 5
      ;;
    401|403)
      echo "❌ PAT 鉴权失败 (HTTP $http_code)。请检查 GITHUB_TOKEN 是否有效 + 是否有 repo scope。" >&2
      exit 6
      ;;
    000)
      echo "⚠️  网络探测失败（无法访问 api.github.com），跳过预检直接 push 尝试"
      ;;
    *)
      echo "⚠️  HTTP ${http_code}（继续尝试 push）"
      ;;
  esac
else
  echo "ℹ️  curl 不可用，跳过预探测"
fi

# ─── mono-repo 安全护栏：检测目标 repo 是否已含 skills/ 多 skill 结构 ───
# 背景：2026-08-02 better-office-work-flow 仓库被本流程冲掉（skills/ 4 个 skill → 1 个）
# 本流程把单个 skill 当 repo 根目录推到 main，会 force-overwrite mono-repo 结构。
if command -v curl >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  echo ""
  echo "🔎 检测目标 repo 是否为 mono-repo（根目录含 skills/ 目录）..."
  ROOT_JSON="$(curl -s --max-time 15 \
    -H "Authorization: Basic $AUTH_B64" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$REPO/contents/" 2>/dev/null || echo "")"
  HAS_SKILLS_DIR="$(printf '%s' "$ROOT_JSON" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    print("False"); sys.exit()
if not isinstance(d, list):
    print("False"); sys.exit()
print("True" if any(isinstance(x, dict) and x.get("name") == "skills" and x.get("type") == "dir" for x in d) else "False")
' 2>/dev/null)"
  HAS_SKILLS_DIR="${HAS_SKILLS_DIR:-False}"
  if [[ "$HAS_SKILLS_DIR" == "True" ]]; then
    cat >&2 <<EOF
❌❌ 检测到目标 repo $REPO 是 mono-repo（根目录含 skills/ 目录）！

   本流程会把单个 skill 当 repo 根目录推到 main，这会 force-overwrite 掉
   skills/ 里的所有其它 skill（2026-08-02 better-office-work-flow 仓库就是
   这样被冲掉的：4 个 skill → 1 个，事后从孤立提交 63ae4858 才恢复）。

   对 mono-repo，请改用「子目录模式」手动发布：
     1. git clone https://github.com/$REPO.git /tmp/mono-repo
     2. rsync -a --exclude=.git <fork>/ /tmp/mono-repo/skills/<slug>/
     3. cd /tmp/mono-repo && git add -A && git commit -m "update <slug>" \\
        && git push origin main
     4. 删除 /tmp/mono-repo

   如确需覆盖（清空 repo 只留这一个 skill），显式设环境变量再跑：
     OSG_ALLOW_MONOREPO_OVERWRITE=1 $0 ...
EOF
    if [[ -z "${OSG_ALLOW_MONOREPO_OVERWRITE:-}" ]]; then
      exit 8
    fi
    echo "⚠️  OSG_ALLOW_MONOREPO_OVERWRITE=1 已设置，继续覆盖（危险！）" >&2
  else
    echo "✅ 目标 repo 非 mono-repo（无 skills/ 目录），可安全 push"
  fi
fi

echo ""
echo "🚀 Pushing to $REMOTE_URL (with retry up to 5 times)..."

# 大文件 + 弱网/内网→GitHub 抖动兜底（默认 HTTP/2 在大文件推送时易 502/断流）
git config http.version HTTP/1.1
git config http.postBuffer 524288000

# macOS 兼容：优先 gtimeout（brew coreutils），回退无 timeout 直接跑
TIMEOUT_CMD=""
if command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD="gtimeout 150"
elif command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout 150"
fi

success=0
for i in 1 2 3 4 5; do
  if $TIMEOUT_CMD git -c http.extraHeader="Authorization: Basic $AUTH_B64" \
                    push -u origin main; then
    success=1
    break
  fi
  echo "⚠️  Attempt $i failed, retrying after 8s..."
  sleep 8
done

if [[ $success -eq 0 ]]; then
  echo "" >&2
  echo "❌ Push failed after 5 retries. Common causes:" >&2
  echo "   - GitHub repo 还没在浏览器创建（必须用户先在 https://github.com/new 建空 repo）" >&2
  echo "   - PAT 权限不够（需要 'repo' scope）" >&2
  echo "   - 内网到 GitHub 网络异常（502/连接 timeout，可稍后再跑）" >&2
  exit 4
fi

# ⚠️ push 命令 exit 0 不等于真的推上去了（内网抖动/timeout 包装/502 后被 kill
#    都可能 exit 0 但远端未更新）。必须用独立读路径验真：比对本地 HEAD 与远端 sha。
echo ""
echo "🔎 验真 push（比对本地/远端 sha）..."
LOCAL_SHA="$(git rev-parse HEAD 2>/dev/null)"
REMOTE_SHA=""
# 优先 GitHub API（比 ls-remote 更抗抖动），失败回退 ls-remote
if command -v curl >/dev/null 2>&1; then
  REMOTE_SHA="$(curl -s --max-time 40 \
      -H "Authorization: Bearer $GITHUB_TOKEN_VALUE" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/$REPO/commits/main" 2>/dev/null \
    | grep -m1 '"sha"' | sed -E 's/.*"sha"[^"]*"([0-9a-f]+)".*/\1/')"
fi
if [[ -z "$REMOTE_SHA" ]]; then
  TIMEOUT_CMD_LS=""
  if command -v gtimeout >/dev/null 2>&1; then TIMEOUT_CMD_LS="gtimeout 60"
  elif command -v timeout >/dev/null 2>&1; then TIMEOUT_CMD_LS="timeout 60"; fi
  REMOTE_SHA="$($TIMEOUT_CMD_LS git -c http.extraHeader="Authorization: Basic $AUTH_B64" \
      ls-remote origin main 2>/dev/null | awk '{print $1}')"
fi

if [[ -n "$REMOTE_SHA" && "$LOCAL_SHA" == "$REMOTE_SHA" ]]; then
  echo "✅ push verified — 本地=远端 ($LOCAL_SHA)"
elif [[ -z "$REMOTE_SHA" ]]; then
  echo "⚠️  无法获取远端 sha（网络抖动），请手动验真：" >&2
  echo "     git ls-remote origin main   或   GitHub 网页刷新" >&2
else
  echo "❌ push 未生效！本地 $LOCAL_SHA ≠ 远端 $REMOTE_SHA" >&2
  echo "   push 报了成功但远端 sha 不一致（假成功），请重跑本脚本。" >&2
  exit 7
fi

echo ""
echo "✅ Pushed successfully to https://github.com/$REPO"

# 主动清理 credential 残留（git -c 是临时但部分版本会写入 helper 缓存）
echo ""
echo "🧹 清理 credential 残留..."
git config --unset http.extraHeader 2>/dev/null || true
# 提示用户检查 credential helper 缓存
if [[ -f "$HOME/.git-credentials" ]]; then
  if grep -q "github.com" "$HOME/.git-credentials" 2>/dev/null; then
    echo "⚠️  ~/.git-credentials 含 github.com 条目，请检查是否包含此次 PAT："
    echo "     grep github.com ~/.git-credentials"
    echo "     如有残留，手工删除该行后再 revoke PAT"
  fi
fi
echo "✅ 本仓库 .git/config 已清"

echo ""
echo "🔐 Token hygiene reminder:"
echo "   立刻去 https://github.com/settings/tokens 撤销刚才用的 PAT"
echo ""
echo "📝 Next steps:"
echo "   - (Optional) clawhub publish: CLAWHUB_TOKEN=clh_xxx scripts/clawhub_publish.sh $FORK"
echo "   - Sediment memory: memory/project_$(basename "$FORK")_opensource_fork.md"
