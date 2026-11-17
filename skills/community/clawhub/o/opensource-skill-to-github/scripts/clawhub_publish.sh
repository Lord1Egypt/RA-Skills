#!/usr/bin/env bash
# clawhub_publish.sh — Step 10 (optional): clawhub publish
# Usage: CLAWHUB_TOKEN=clh_xxx ./clawhub_publish.sh <fork-abs-path>
set -euo pipefail
# 提前声明 WHO 为空（set -u 只报「未声明」不报「空值」），避免命令替换边界下的 unbound 误报
WHO=""

FORK="${1:-}"

if [[ -z "$FORK" ]]; then
  cat <<EOF >&2
Usage: CLAWHUB_TOKEN=clh_xxx $0 <fork-abs-path>

  example: CLAWHUB_TOKEN=clh_xxx $0 /home/node/.openclaw/workspace/opensourceskills/my-skill

⚠️  必须用绝对路径（相对路径偶发 SKILL.md required 报错）。
⚠️  CLAWHUB_TOKEN 与 GitHub token 完全独立；临时 token 分别撤销，长期配置分别管理。
⚠️  Publish 成功后请立刻去 clawhub.com 撤销该 token。
EOF
  exit 1
fi

# 强制绝对路径
case "$FORK" in
  /*) ;;
  *)  echo "❌ 必须用绝对路径（相对路径偶发 SKILL.md required 报错）" >&2; exit 2 ;;
esac

[[ -d "$FORK" ]] || { echo "❌ fork-path not a directory: $FORK" >&2; exit 3; }
[[ -f "$FORK/SKILL.md" ]] || { echo "❌ SKILL.md not found in $FORK" >&2; exit 4; }

# 发布前清理派生缓存（__pycache__/*.pyc 等，避免进 clawhub 包）
. "$(dirname "$0")/_lib_exclude.sh"
osg_clean_fork "$FORK"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "❌ clawhub CLI 未安装，请先：npm install -g clawhub" >&2
  exit 6
fi

# 鉴权：优先用已登录态（clawhub login 后本地已持久化 token）；
# 仅当未登录时才要求 CLAWHUB_TOKEN 环境变量。
if clawhub whoami >/dev/null 2>&1; then
  # whoami 输出解析必须容错：新版 CLI 带 spinner 行（"- Checking token" / "✔ <user>"），
  # 且 grep 无匹配会返回非零 → 在 set -e + pipefail 下会静默杀脚本。
  # 先给 WHO 默认值（避免 set -u 下 unbound variable），解析结果单独存 WHO_PARSED，
  # 非空才覆盖；管道失败用 `|| true` 兜底，不影响后续发布（whoami 已确认登录成功）。
  WHO="已登录用户"
  # 注意：clawhub whoami 的 spinner / ✔ 都在 **stderr**（stdout 为空），
  # 必须用 2>&1 捕获；管道末尾 `|| true` 防 SIGPIPE 在 pipefail 下非零杀脚本。
  WHO_PARSED="$(clawhub whoami 2>&1 | sed $'s/\033\\[[0-9;]*m//g' | tr -d '✔' | grep -vi 'checking' | tail -1 | xargs)" || true
  # 用 if 而非 `&&` 赋值：bash set -u 在命令替换 + `&&` 边界会误把变量标为 unbound
  if [[ -n "$WHO_PARSED" ]]; then
    WHO="$WHO_PARSED"
  fi
  # echo 用 ${WHO:-默认}：nounset 安全，即使极端情况下 WHO 未设置也不报错
  echo "ℹ️  clawhub 已登录（${WHO:-已登录用户}），使用已登录态发布"
elif [[ -n "${CLAWHUB_TOKEN:-}" ]]; then
  echo "ℹ️  clawhub 未登录，使用 CLAWHUB_TOKEN 环境变量"
else
  echo "❌ clawhub 未登录且未设 CLAWHUB_TOKEN" >&2
  echo "   请任选：① clawhub login  ② CLAWHUB_TOKEN=clh_xxx $0 $FORK" >&2
  exit 5
fi

# 从 SKILL.md 提取版本（clawhub publish 强制 semver --version），缺则默认 1.0.0
VERSION="$(grep -m1 -o '\*\*Version\*\*:[[:space:]]*[0-9]*\.[0-9]*\.[0-9]*' "$FORK/SKILL.md" 2>/dev/null | grep -o '[0-9]*\.[0-9]*\.[0-9]*' || echo '1.0.0')"
VERSION="${VERSION:-1.0.0}"
echo "ℹ️  version: $VERSION"

echo "🚀 Publishing to clawhub.com ..."

# 重试（rate limit / 网络抖动 → sleep 30s 重试）
# 注：已登录态直接 clawhub；设了 CLAWHUB_TOKEN 则前缀 env 注入。
# 不能用空数组前缀 "${ARR[@]}"（bash 3.2/macOS 下 unbound；"${ARR[@]:-}" 又生成空命令名 → exit 126），
# 故显式 if/else 分支，两条路径在 bash 3.2(Linux/macOS) 与 4/5 下都安全。
for i in 1 2 3; do
  if [[ -n "${CLAWHUB_TOKEN:-}" ]]; then
    OUT="$(env "CLAWHUB_TOKEN=$CLAWHUB_TOKEN" clawhub publish "$FORK" --version "$VERSION" 2>&1)"; rc=$?
  else
    OUT="$(clawhub publish "$FORK" --version "$VERSION" 2>&1)"; rc=$?
  fi
  echo "$OUT"
  if [[ $rc -eq 0 && "$OUT" != *"already exists"* ]]; then
    echo ""
    echo "✅ Published to clawhub.com ($VERSION)"
    break
  fi
  # 幂等：版本已存在 = 上一次（或本次首轮）其实已发成功，不是错误，不重试
  if [[ "$OUT" == *"already exists"* ]]; then
    echo ""
    echo "ℹ️  clawhub 上 $VERSION 已存在（视为已发布成功，跳过重试）"
    echo "    如需重发请先 bump 版本号（clawhub 任何内容改动重发都必须换版本号）"
    break
  fi
  if [[ $i -lt 3 ]]; then
    echo "⚠️  Attempt $i failed (rc=$rc), retrying after 30s..."
    sleep 30
  else
    echo "❌ Publish failed after 3 retries" >&2
    exit $rc
  fi
done

# 提醒 LICENSE 平台特性
echo ""
echo "ℹ️  关于 LICENSE："
echo "   clawhub 强制 LICENSE 为 MIT-0（本地 LICENSE 文件被忽略，三渠道 license 不一致是平台特性，不是 bug）"
echo ""
echo "🔐 Token hygiene reminder:"
echo "   立刻去 clawhub.com 撤销刚才用的 token"
echo ""
echo "📝 Next steps:"
echo "   - skills.sh 通过 GitHub repo 自动同步（24h 后才在 npx skills list 可见）"
echo "   - 沉淀 memory: memory/project_$(basename "$FORK")_opensource_fork.md"
