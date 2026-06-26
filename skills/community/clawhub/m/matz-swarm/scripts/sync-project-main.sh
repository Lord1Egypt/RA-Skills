#!/bin/bash
# sync-project-main.sh - 同步指定项目到 origin/main 最新
# 用法: ./sync-project-main.sh <project-name>

set -e

SWARM_DIR="${HOME}/agent-swarm"
REGISTRY="${SWARM_DIR}/registry.json"
PROJECT="$1"

[ -z "$PROJECT" ] && { echo "Usage: $0 <project-name>"; exit 1; }

LOCAL_REPO=$(jq -r --arg p "$PROJECT" '.projects[$p].local_repo // empty' "$REGISTRY")
BASE_BRANCH=$(jq -r --arg p "$PROJECT" '.projects[$p].base_branch // "main"' "$REGISTRY")

if [ -z "$LOCAL_REPO" ] || [ ! -d "$LOCAL_REPO/.git" ]; then
  echo "❌ local_repo not found for project: $PROJECT"
  exit 1
fi

cd "$LOCAL_REPO"

echo "📦 Project: $PROJECT"
echo "📁 Repo: $LOCAL_REPO"
echo "🌿 Branch: $BASE_BRANCH"

git fetch origin

git checkout "$BASE_BRANCH"
git pull --ff-only origin "$BASE_BRANCH"

echo "✅ Synced to latest origin/$BASE_BRANCH"
git log --oneline -1
