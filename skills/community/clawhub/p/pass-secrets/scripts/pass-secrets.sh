#!/usr/bin/env bash
# pass-secrets helper script

set -euo pipefail

GPG_KEY="4FA146198B574BE88C2FCE607BCA61011E422C14"
STORE_DIR="${PASSWORD_STORE_DIR:-$HOME/.password-store}"

cmd="${1:-}"
path="${2:-}"

usage() {
    cat << 'EOF'
Usage: pass-secrets <cmd> [path]

Commands:
  get <path>      Retrieve a secret
  set <path>      Store a secret (reads from stdin)
  ls [path]       List secrets
  rm <path>       Remove a secret
  env <path>      Export secret as env var (prints export command)
EOF
}

case "$cmd" in
    get)
        [ -z "$path" ] && { echo "Error: path required"; exit 1; }
        pass show "$path" 2>/dev/null || { echo "Error: secret not found: $path"; exit 1; }
        ;;
    set)
        [ -z "$path" ] && { echo "Error: path required"; exit 1; }
        pass insert -m "$path"
        ;;
    ls)
        pass ls "$path" 2>/dev/null || pass ls
        ;;
    rm)
        [ -z "$path" ] && { echo "Error: path required"; exit 1; }
        pass rm "$path"
        ;;
    env)
        [ -z "$path" ] && { echo "Error: path required"; exit 1; }
        value=$(pass show "$path" 2>/dev/null) || { echo "Error: secret not found: $path"; exit 1; }
        var_name=$(basename "$path" | tr '[:lower:]-' '[:upper:]_')_KEY
        echo "export $var_name=\"$value\""
        ;;
    *)
        usage
        exit 1
        ;;
esac
