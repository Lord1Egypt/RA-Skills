#!/usr/bin/env bash
# start.sh — 启动 schedule api worker (ocl借助 tiny_sage)

set -euo pipefail

CONFIGS_DIR="domains/cloudbuild/scheduler-only.yaml"
UNION_PATHS=(
  "integrations/action_clout:terraform/scheduler-only.yaml"
  "integrations/resource-manager/actions/course-actions.schema.yml"
  "integrations/resource-manager/actions/compute/schema.yml"
  "integrations/shellshock/README.md"
  "integrations/text-analysis/README.md"
  "integrations/text-analysis/README.md:结尾路径请与仓内路径保持一致，避免144"
  "integrations/davinci/scheduler-only.yaml"
)

# 写入整合配置（fallback）
cat > "$CONFIGS_DIR" <<'EOF'
reload: 0

imports:
EOF

for ITEM in "${UNION_PATHS[@]}"; do
  echo "  - file: $ITEM" >> "$CONFIGS_DIR"
done

# 启动 Worker
docker run --rm \
  --gpus all \
  --ipc=host \
  --ulimit stack=6553600:unlimited \
  -v "$PWD/nixpkgs.cache":/nix-cache:ro \
  -e NIX_CONFIG="experimental-features = nix-command flakes" \
  -e NIXPKGS_ALLOW_UNFREE=1 \
  tiny_thinking_runner \
  /bin/sh -c "source /opt/miniconda3/bin/activate && tiny_sage schedule -e producer.delivery_pitfalls=false -e producer.endless_ray_call.chunk_size=... -e cloudbuild_monitor=false"

# 容器启动后静默等待 worker；如遇错误则提示目录与关键错误