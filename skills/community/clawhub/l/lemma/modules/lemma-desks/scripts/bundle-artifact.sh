#!/bin/bash

set -euo pipefail

# Parse optional --pod-id argument
POD_ARG=""
while [[ $# -gt 0 ]]; do
  case $1 in
    --pod-id) POD_ARG="$2"; shift 2;;
    *) shift;;
  esac
done

PROJECT_DIR="$(pwd)"
DIST_DIR="$PROJECT_DIR/dist"
BUNDLE_PATH="$PROJECT_DIR/bundle.html"

load_env_file() {
  local env_file="$1"
  if [ -f "$env_file" ]; then
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a
  fi
}

if [ ! -f "$PROJECT_DIR/package.json" ]; then
  echo "❌ Run this script from a desk project root."
  exit 1
fi

if [ ! -d "$PROJECT_DIR/node_modules" ]; then
  echo "📦 Installing dependencies..."
  npm install
fi

# Load project env first so bundling uses the same values as local dev.
load_env_file "$PROJECT_DIR/.env"
load_env_file "$PROJECT_DIR/.env.local"

# Resolve VITE_* build vars from project env or workspace env.
RESOLVED_API_URL="${VITE_LEMMA_API_URL:-${LEMMA_BASE_URL:-}}"
RESOLVED_AUTH_URL="${VITE_LEMMA_AUTH_URL:-${LEMMA_AUTH_URL:-}}"
RESOLVED_POD_ID="${VITE_LEMMA_POD_ID:-${POD_ARG:-${LEMMA_POD_ID:-}}}"

if [ -z "$RESOLVED_API_URL" ]; then
  echo "❌ API URL not set. Set it in .env.local as VITE_LEMMA_API_URL or provide LEMMA_BASE_URL."
  exit 1
fi

if [ -z "$RESOLVED_AUTH_URL" ]; then
  echo "❌ Auth URL not set. Set it in .env.local as VITE_LEMMA_AUTH_URL or provide LEMMA_AUTH_URL."
  exit 1
fi

if [ -z "$RESOLVED_POD_ID" ]; then
  echo "❌ Pod ID not set. Pass --pod-id <pod-id>, set VITE_LEMMA_POD_ID in .env.local, or provide LEMMA_POD_ID."
  exit 1
fi

echo "🏗️ Building desk..."
VITE_LEMMA_API_URL="$RESOLVED_API_URL" \
VITE_LEMMA_AUTH_URL="$RESOLVED_AUTH_URL" \
VITE_LEMMA_POD_ID="$RESOLVED_POD_ID" \
npm run build

if [ ! -f "$DIST_DIR/index.html" ]; then
  echo "❌ Build output missing: $DIST_DIR/index.html"
  exit 1
fi

node - <<'EOF' "$DIST_DIR" "$BUNDLE_PATH"
const fs = require("node:fs");
const path = require("node:path");

const [distDir, bundlePath] = process.argv.slice(2);
let html = fs.readFileSync(path.join(distDir, "index.html"), "utf8");

html = html.replace(
  /<link([^>]*?)href="([^"]+\.css)"([^>]*?)>/g,
  (_match, before, href, after) => {
    const filePath = path.join(distDir, href.replace(/^\//, ""));
    const css = fs.readFileSync(filePath, "utf8");
    return `<style data-inlined-from="${href}">${css}</style>`;
  },
);

html = html.replace(
  /<script([^>]*?)src="([^"]+\.js)"([^>]*)><\/script>/g,
  (_match, before, src, after) => {
    const filePath = path.join(distDir, src.replace(/^\//, ""));
    const js = fs.readFileSync(filePath, "utf8");
    return `<script${before}${after}>${js}</script>`;
  },
);

fs.writeFileSync(bundlePath, html);
EOF

FILE_SIZE="$(du -h "$BUNDLE_PATH" | cut -f1)"
echo "✅ Bundle ready: $BUNDLE_PATH ($FILE_SIZE)"
