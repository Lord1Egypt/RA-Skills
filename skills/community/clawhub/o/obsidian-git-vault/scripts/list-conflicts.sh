#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_common.sh"
V="$(resolve_vault "${1:-}")" || exit 1
V="$(cd "$V" && pwd)"
git -C "$V" diff --name-only --diff-filter=U
