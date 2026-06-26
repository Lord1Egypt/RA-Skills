#!/usr/bin/env bash
# Deploy NexPix Cloudflare Worker
# Deploys the sage-image-gen worker to Cloudflare Workers
#
# Prerequisites:
#   - wrangler CLI installed (npm i -g wrangler)
#   - Cloudflare account authenticated (wrangler login)
#
# Usage:
#   bash scripts/deploy-worker.sh

set -euo pipefail

WORKER_DIR="${HOME}/.openclaw/workspace/workers/sage-image-gen"

if [ ! -d "$WORKER_DIR" ]; then
  echo "❌ Worker directory not found: $WORKER_DIR"
  echo "   Create the worker first with wrangler init"
  exit 1
fi

echo "🚀 Deploying NexPix worker..."
cd "$WORKER_DIR"
npx wrangler deploy

echo "✅ Worker deployed!"
echo "   URL: https://sage-image-gen.sageimg.workers.dev"
