#!/bin/bash
set -euo pipefail

# 1. 自动识别路径：以脚本所在目录的上一级作为项目根目录
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 2. 声明必需的环境变量 (无默认值，强制外部注入，符合审核规范)
: "${SERVER_IP:?Required env var SERVER_IP is missing}"
: "${REMOTE_DIR:?Required env var REMOTE_DIR is missing}"

# 3. 可选环境变量及默认值
readonly SERVER_PORT="${SERVER_PORT:-22}"
readonly REMOTE_USER="${REMOTE_USER:-deploy}"
readonly BUILD_PATH="${PROJECT_ROOT}/docs/.vitepress/dist"

# 4. 依赖项检查
for cmd in pnpm rsync ssh; do
  command -v "$cmd" &> /dev/null || { echo "Error: $cmd is not installed."; exit 1; }
done

# 5. 安全校验：禁止操作系统核心目录
if [[ "$REMOTE_DIR" =~ ^/($|boot|root|etc|usr/bin|usr/lib) ]]; then
  echo "Error: Deployment to system directories is forbidden."
  exit 1
fi

# 6. 执行任务
cd "$PROJECT_ROOT"
echo "Building VitePress..."
pnpm install && pnpm run docs:build

if [ ! -d "$BUILD_PATH" ]; then
  echo "Error: Build directory $BUILD_PATH not found."
  exit 1
fi

echo "Deploying to ${SERVER_IP}..."
# 显式声明：要求用户环境已配置 SSH Key 认证
rsync -avz -e "ssh -p ${SERVER_PORT}" "$BUILD_PATH/" "${REMOTE_USER}@${SERVER_IP}:${REMOTE_DIR}"

echo "Deployment finished successfully."