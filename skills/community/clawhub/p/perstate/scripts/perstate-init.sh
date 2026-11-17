#!/bin/bash
# perstate-init.sh — perstate 初始化或更新配置
# 用法: perstate-init.sh [--repo <url-or-path>] [--branch <branch>] [--yes]
# 首次使用需指定 --repo；后续执行可省略，从 config 读取
# --yes: 跳过交互确认（由 Agent 在调用前确认）
# 默认分支: main

set -euo pipefail

# --- 参数解析 ---
REPO=""
BRANCH=""
YES=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)   REPO="$2"; shift 2 ;;
    --branch) BRANCH="$2"; shift 2 ;;
    --yes)    YES=true; shift ;;
    *) echo "未知参数: $1"; exit 1 ;;
  esac
done

# --- 从 config 读取默认值（如已配置）---
CONFIG=~/.perstate/config.yml
DEFAULT_REPO=""
DEFAULT_BRANCH=""
if [ -f "$CONFIG" ]; then
  DEFAULT_REPO=$(grep "^default_repo:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
  DEFAULT_BRANCH=$(grep "^default_branch:" "$CONFIG" | sed 's/^[^:]*: *//' || true)
fi
REPO="${REPO:-$DEFAULT_REPO}"
BRANCH="${BRANCH:-${DEFAULT_BRANCH:-main}}"

if [ -z "$REPO" ]; then
  echo "用法: perstate-init.sh --repo <url-or-path> [--branch <branch>] [--yes]"
  echo "首次使用需指定 --repo。"
  exit 1
fi

# --- 确认 ---
if [ "$YES" = false ]; then
  echo "仓库: $REPO"
  echo "分支: $BRANCH"
  echo ""
  echo "确认以上配置？(y/n)"
  read -r CONFIRM
  if [ "$CONFIRM" != "y" ]; then
    echo "已取消"
    exit 0
  fi
fi

# --- 环境检查 ---
if ! command -v git &>/dev/null; then
  echo "错误: git 未安装。请先安装 git。"
  exit 1
fi

# 检查 repo 协议：非 SSH 给安全警告
case "$REPO" in
  git@*|ssh://*)
    # SSH 协议，安全
    if [ ! -f ~/.ssh/id_ed25519 ] && [ ! -f ~/.ssh/id_rsa ]; then
      echo "警告: 使用 SSH 协议但未检测到 SSH key。"
      echo "  生成: ssh-keygen -t ed25519 -C \"your_email@example.com\""
      echo "  添加: cat ~/.ssh/id_ed25519.pub → GitHub Settings → SSH Keys"
      echo ""
    fi
    ;;
  *)
    # 非 SSH（HTTPS 或本地路径）
    echo "⚠ 安全警告: 仓库地址不是 SSH 协议。"
    echo "  state 包含隐私知识，强烈推荐使用 SSH 协议接入。"
    echo "  SSH URL 格式: git@github.com:user/repo.git"
    echo ""
    ;;
esac

# --- 写入配置（幂等）---
mkdir -p ~/.perstate
CONFIG=~/.perstate/config.yml

if [ -f "$CONFIG" ]; then
  # 更新 default_repo
  if [ "$(uname)" = "Darwin" ]; then
    sed -i '' "s|^default_repo:.*|default_repo: $REPO|" "$CONFIG"
    sed -i '' "s|^default_branch:.*|default_branch: $BRANCH|" "$CONFIG"
  else
    sed -i "s|^default_repo:.*|default_repo: $REPO|" "$CONFIG"
    sed -i "s|^default_branch:.*|default_branch: $BRANCH|" "$CONFIG"
  fi
else
  cat > "$CONFIG" << EOF
default_repo: $REPO
default_branch: $BRANCH
sessions:
EOF
fi

echo "配置已写入: $CONFIG"

# --- 获取仓库（bare clone + worktree，远程和本地统一）---
REPO_NAME=$(basename "$REPO" .git)
BARE_REPO="$HOME/.perstate/$REPO_NAME.git"
WORKTREE_DIR="$HOME/.perstate/worktrees/$REPO_NAME"
WORKTREE="$WORKTREE_DIR/$BRANCH"

# 本地路径不是 git 仓库时，先初始化
case "$REPO" in
  git@*|https://*|http://*|ssh://*) ;;
  *)
    # 检查是否已是 git 仓库（regular repo 有 .git 目录，bare repo 有 HEAD 文件）
    if [ ! -d "$REPO/.git" ] && [ ! -f "$REPO/HEAD" ]; then
      echo "本地路径不是 git 仓库，自动初始化..."
      mkdir -p "$REPO"
      cd "$REPO"
      git init -b "$BRANCH" 2>/dev/null || { git init && git checkout -b "$BRANCH"; }
      # 初始提交确保分支 born
      echo "# Perstate Knowledge Graph" > README.md
      git add . && git commit -m "init" 2>/dev/null || true
    fi
    # 允许 bare clone push 回本地仓库（非裸仓库默认拒绝 push 到 checked-out 分支）
    git -C "$REPO" config receive.denyCurrentBranch updateInstead 2>/dev/null || true
    ;;
esac

# bare clone（如果不存在）
if [ ! -d "$BARE_REPO" ]; then
  echo "克隆仓库: $REPO → $BARE_REPO"
  if ! git clone --bare "$REPO" "$BARE_REPO" >&2 2>/dev/null; then
    echo "错误: 克隆仓库失败。请检查仓库地址和权限。" >&2
    rm -rf "$BARE_REPO" 2>/dev/null
    exit 1
  fi
  # 配置远程跟踪 ref（bare clone 默认不生成 refs/remotes/origin/*）
  git -C "$BARE_REPO" config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
  git -C "$BARE_REPO" fetch origin >&2 2>/dev/null || true
fi

cd "$BARE_REPO"
git worktree prune
git fetch origin >&2 2>/dev/null || true

# 分支处理：本地不存在时从远程创建
if ! git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
  if git show-ref --verify --quiet "refs/remotes/origin/$BRANCH" 2>/dev/null; then
    git branch "$BRANCH" "origin/$BRANCH" >&2
  elif git rev-parse --verify HEAD 2>/dev/null; then
    DEFAULT_REMOTE=$(git symbolic-ref --short HEAD 2>/dev/null || git remote show origin 2>/dev/null | grep "HEAD branch" | sed 's/^[^:]*: *//' || echo "main")
    git branch "$BRANCH" "origin/$DEFAULT_REMOTE" >&2
  fi
fi

# 创建或复用 worktree
mkdir -p "$WORKTREE_DIR"
if [ -d "$WORKTREE" ] && [ -f "$WORKTREE/.git" ]; then
  echo "复用已有 worktree: $WORKTREE"
elif git show-ref --verify --quiet "refs/heads/$BRANCH" 2>/dev/null; then
  git worktree add "$WORKTREE" "$BRANCH" 2>/dev/null && echo "worktree 已创建: $WORKTREE" || {
    echo "错误: 分支 '${BRANCH}' 已在其他 worktree checkout。请等待或使用其他分支。" >&2
    exit 1
  }
else
  # 分支不存在（空仓库）— 创建 detached worktree 后新建分支
  git worktree add --detach "$WORKTREE" 2>/dev/null || true
fi
cd "$WORKTREE"
# 如果在 detached 状态，创建并切换到目标分支
git rev-parse --abbrev-ref HEAD 2>/dev/null | grep -q "^HEAD$" && git checkout -b "$BRANCH" 2>/dev/null || true

# --- 创建初始结构（如不存在）---
mkdir -p schema entities

if [ ! -f schema/ontology.md ]; then
  cat > schema/ontology.md << 'ONTOLOGY'
# Ontology

## Entity Types

| Type | Description |
|------|-------------|
| domain | 领域 |
| concept | 概念 |
| technology | 技术 |
| framework | 框架 |
| person | 人物 |
| insight | 洞察结晶 |

## Relation Types

| Type | Description | Inverse |
|------|-------------|---------|
| depends-on | A 依赖 B | enables |
| enables | A 赋能 B | depends-on |
| evolves-from | A 从 B 演化 | evolves-to |
| contradicts | A 与 B 矛盾 | contradicts |
| specializes | A 是 B 的特化 | generalizes |
| part-of | A 是 B 的部分 | contains |
| applies-to | A 适用于 B | applied-by |

## Properties

Schema is open — any YAML frontmatter field is valid.
ONTOLOGY
  echo "已创建: schema/ontology.md"
fi

if [ ! -f README.md ]; then
  cat > README.md << 'README'
# Perstate Knowledge Graph

This repo is a file-system knowledge graph maintained by the perstate skill.

## Branch Isolation Design

Each branch in this repo corresponds to one agent's or person's persistent state:

- `main` — personal personality & knowledge (default branch)
- Other branches — individual agents' states

Branches are isolated. Use `git fork` / `git merge` / `git cherry-pick` to share knowledge between agents.

## Structure

- `entities/<id>/entity.md` — entity metadata + content
- `entities/<id>/<relation-type>/<target>.md` — relations
- `schema/ontology.md` — schema documentation

## Query

- `ls entities/` — list all entities
- `ls entities/<id>/` — list out-relation types
- `grep -rl "keyword" entities/` — full-text search
README
  echo "已创建: README.md"
fi

# --- 提交并推送 ---
git add .
git commit -m "perstate: initialize knowledge graph" 2>/dev/null && echo "已提交" || echo "无变更需要提交"
git push origin "$BRANCH" && echo "已推送" || echo "推送失败（远程可能需要配置或权限不足）"

echo ""
echo "初始化完成。"
echo "  仓库: $REPO"
echo "  分支: $BRANCH"
echo "  bare repo: $BARE_REPO"
echo "  worktree: $WORKTREE"
