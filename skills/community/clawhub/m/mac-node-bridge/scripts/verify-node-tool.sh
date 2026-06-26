#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  verify-node-tool.sh --host USER@HOST [--bin /abs/path/to/bin | --tool TOOL]
                      [--brew-prefix PREFIX]

Checks SSH reachability and whether the requested binary exists on the remote Mac node.

Resolution order for --tool:
  1. command -v TOOL on the remote Mac
  2. BREW_PREFIX/bin/TOOL where BREW_PREFIX comes from --brew-prefix
  3. brew --prefix on the remote Mac
  4. Common prefixes: /opt/homebrew/bin and /usr/local/bin
EOF
}

resolve_remote_tool() {
  local host="$1"
  local tool="$2"
  local brew_prefix="$3"
  local remote_script='set -e
TOOL="$1"
BREW_PREFIX="${2:-}"
if command -v "$TOOL" >/dev/null 2>&1; then
  path=$(command -v "$TOOL")
  test -x "$path"
  printf "OK %s\n" "$path"
  exit 0
fi
if [[ -n "$BREW_PREFIX" && -x "$BREW_PREFIX/bin/$TOOL" ]]; then
  printf "OK %s/bin/%s\n" "$BREW_PREFIX" "$TOOL"
  exit 0
fi
if command -v brew >/dev/null 2>&1; then
  prefix=$(brew --prefix 2>/dev/null || true)
  if [[ -n "$prefix" && -x "$prefix/bin/$TOOL" ]]; then
    printf "OK %s/bin/%s\n" "$prefix" "$TOOL"
    exit 0
  fi
fi
for prefix in /opt/homebrew /usr/local; do
  if [[ -x "$prefix/bin/$TOOL" ]]; then
    printf "OK %s/bin/%s\n" "$prefix" "$TOOL"
    exit 0
  fi
done
printf "MISSING %s\n" "$TOOL" >&2
exit 1'
  ssh -T "$host" bash -lc "$(printf '%q' "$remote_script")" -- "$tool" "$brew_prefix"
}

HOST=""
REMOTE_BIN=""
TOOL=""
BREW_PREFIX=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --host) HOST="${2:-}"; shift 2 ;;
    --bin) REMOTE_BIN="${2:-}"; shift 2 ;;
    --tool) TOOL="${2:-}"; shift 2 ;;
    --brew-prefix) BREW_PREFIX="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -n "$HOST" ]] || {
  usage
  exit 1
}

if [[ -n "$REMOTE_BIN" && -n "$TOOL" ]]; then
  echo "Pass either --bin or --tool, not both" >&2
  exit 1
fi

if [[ -n "$TOOL" ]]; then
  resolve_remote_tool "$HOST" "$TOOL" "$BREW_PREFIX"
  exit 0
fi

[[ -n "$REMOTE_BIN" ]] || {
  usage
  exit 1
}

[[ "$REMOTE_BIN" = /* ]] || { echo "bin must be an absolute path" >&2; exit 1; }

ssh -T "$HOST" "test -x '$REMOTE_BIN' && printf 'OK %s\n' '$REMOTE_BIN' || { printf 'MISSING %s\n' '$REMOTE_BIN' >&2; exit 1; }"
