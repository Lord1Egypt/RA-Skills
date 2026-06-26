#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist
tar -czf dist/local-skill-package.tar.gz \
  SKILL.md README.md docs examples templates scripts assets
echo "created dist/local-skill-package.tar.gz"
