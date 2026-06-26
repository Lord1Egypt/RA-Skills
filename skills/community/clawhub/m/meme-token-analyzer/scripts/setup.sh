#!/bin/bash
set -eo pipefail

# 初始化目录
if [ "$COZE_PROJECT_ENV" = "DEV" ]; then
  if [ ! -d "${COZE_WORKSPACE_PATH}/assets" ]; then
    mkdir -p "${COZE_WORKSPACE_PATH}/assets"
  fi
fi

# 双模式安装：优先 uv，回退 pip（确保旧镜像回滚兼容）
if command -v uv &>/dev/null && [ -f "pyproject.toml" ]; then
  # uv 模式
  if [ -n "$PIP_TARGET" ]; then
    echo "[setup] Deploy mode (uv): installing to PIP_TARGET=$PIP_TARGET"
    uv export --frozen --no-hashes --no-dev | uv pip install --no-cache --target "$PIP_TARGET" -r -
  else
    echo "[setup] Devbox mode (uv): installing to .venv"
    if [ -f "uv.lock" ]; then
      uv sync --frozen || uv sync
    else
      uv sync
    fi
    touch .venv/.uv_ready
  fi
else
  # pip 回退模式（旧镜像没有 uv 或项目未迁移到 pyproject.toml）
  if [ -f "requirements.txt" ]; then
    echo "[setup] Fallback mode (pip): installing from requirements.txt"
    pip install -r requirements.txt
  else
    echo "[setup] Warning: no pyproject.toml or requirements.txt found, skipping install"
  fi
fi
