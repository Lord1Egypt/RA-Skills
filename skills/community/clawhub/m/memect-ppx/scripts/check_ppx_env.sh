#!/usr/bin/env bash
set -euo pipefail

if ! command -v ppx >/dev/null 2>&1; then
  echo "missing: ppx"
  exit 1
fi

if ! ppx --help >/dev/null 2>&1; then
  echo "broken: ppx"
  exit 1
fi

echo "ok: ppx"
