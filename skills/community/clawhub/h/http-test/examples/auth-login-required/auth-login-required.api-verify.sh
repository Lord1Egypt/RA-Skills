#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"
exec bash "${SCRIPT_DIR}/../../templates/basic.api-verify.sh" "${SCRIPT_DIR}/auth-login-required.api-tests.http.txt" "$@"
