#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
git -C "$ROOT" config core.hooksPath .githooks
echo "OK: 已安装 $ROOT/.githooks/pre-push"
