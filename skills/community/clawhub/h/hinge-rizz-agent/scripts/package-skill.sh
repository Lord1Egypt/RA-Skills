#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
OUT_DIR="${1:-$(cd "${SKILL_DIR}/.." && pwd)}"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

mkdir -p "${OUT_DIR}"

rsync -a \
  --exclude=".git/" \
  --exclude=".DS_Store" \
  --exclude="hinge-data/" \
  --exclude="node_modules/" \
  --exclude="__pycache__/" \
  --exclude="*.zip" \
  --exclude="*.tar.gz" \
  --exclude="agent.log" \
  "${SKILL_DIR}/" "${TMP_DIR}/barney/"

(
  cd "${TMP_DIR}"
  zip -rq "${OUT_DIR}/barney-clawhub-ready.zip" "barney"
  zip -rq "${OUT_DIR}/barney-github-ready.zip" "barney"
)

echo "Packaged:"
echo "  ${OUT_DIR}/barney-clawhub-ready.zip"
echo "  ${OUT_DIR}/barney-github-ready.zip"
