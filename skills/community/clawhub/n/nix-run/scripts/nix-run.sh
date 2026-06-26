#!/usr/bin/env bash
set -euo pipefail

# nix-run: Auto-find and run commands via nix
# Usage: nix-run.sh [--pkg <package>] [--search <keyword>] [--update] <command> [args...]

SCRIPT_NAME="$(basename "$0")"

# Use nixpkgs-unstable flake reference for latest package versions
NIXPKGS_REF="github:NixOS/nixpkgs/nixpkgs-unstable"

usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS] <command> [args...]
       $SCRIPT_NAME --shell <pkg1,pkg2,...> -- <command> [args...]
       $SCRIPT_NAME --search <keyword> [--limit N]
       $SCRIPT_NAME --update

Run a command via nix, auto-detecting the package if needed.

Options:
  --pkg <package>     Skip auto-detection, use specified nix package
  --shell <packages>  Multi-package environment (comma-separated), use -- before command
  --search <keyword>  Search nixpkgs for packages matching keyword
  --limit <N>         Max results for --search (default: 20)
  --update            Update nix-locate database (nix-index) to latest nixpkgs
  --help              Show this help message

Examples:
  $SCRIPT_NAME jq '.name' file.json
  $SCRIPT_NAME --pkg ffmpeg ffmpeg -version
  $SCRIPT_NAME rg --version
  $SCRIPT_NAME --search "json processor"
  $SCRIPT_NAME --search "pdf" --limit 10
  $SCRIPT_NAME --update
  $SCRIPT_NAME --shell python3,nodejs -- python3 script.py
  $SCRIPT_NAME --shell jq,curl -- bash -c 'jq --version && curl --version'
EOF
  exit 0
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

info() {
  echo ":: $*" >&2
}

# --- Update mode ---
do_update() {
  info "Updating nix-locate database (nix-index)..."
  if command -v nix-index &>/dev/null; then
    nix-index
  else
    info "nix-index not found, running via nix..."
    nix shell "${NIXPKGS_REF}#nix-index" -c nix-index
  fi
  info "nix-locate database updated successfully."
}

# --- Search mode ---
do_search() {
  local keyword="$1"
  local limit="$2"

  info "Searching nixpkgs-unstable for '$keyword'..."

  local json
  json="$(nix search "${NIXPKGS_REF}" "$keyword" --json 2>/dev/null)" || die "nix search failed. Check your nix installation."

  if [[ "$json" == "{}" || -z "$json" ]]; then
    echo "No packages found for '$keyword'."
    exit 0
  fi

  # Parse JSON: extract pname, version, description; dedupe by pname; limit results
  # Output format: pname (version) - description
  echo "$json" | nix run "${NIXPKGS_REF}#python3" -- -c "
import json, sys
data = json.load(sys.stdin)
seen = {}
for key, val in data.items():
    pname = val.get('pname', key.split('.')[-1])
    # skip python/perl/ruby/haskell library bindings - usually not CLI tools
    parts = key.split('.')
    if any(p.startswith(('python3', 'perl5', 'ruby', 'haskell')) for p in parts):
        continue
    if pname not in seen:
        seen[pname] = val
items = list(seen.items())[:$limit]
if not items:
    # fallback: show all including library bindings
    seen2 = {}
    for key, val in data.items():
        pname = val.get('pname', key.split('.')[-1])
        if pname not in seen2:
            seen2[pname] = val
    items = list(seen2.items())[:$limit]
for pname, val in items:
    ver = val.get('version', '?')
    desc = val.get('description', 'No description')
    print(f'  {pname} ({ver}) - {desc}')
"
}

# --- Shell (multi-package) mode ---
do_shell() {
  local pkgs_csv="$1"
  shift
  # remaining args are the command + arguments (after --)

  [[ $# -lt 1 ]] && die "--shell requires a command after '--'. Usage: $SCRIPT_NAME --shell pkg1,pkg2 -- <command> [args...]"

  # Parse comma-separated packages, trim whitespace, skip empty entries
  local -a nix_args=()
  local pkg
  while IFS= read -r pkg; do
    # trim leading/trailing whitespace
    pkg="$(echo "$pkg" | xargs)"
    [[ -z "$pkg" ]] && continue
    nix_args+=("${NIXPKGS_REF}#${pkg}")
  done <<< "${pkgs_csv//,/$'\n'}"

  [[ ${#nix_args[@]} -eq 0 ]] && die "--shell requires at least one package name"

  info "Opening multi-package shell with: ${nix_args[*]}"
  exec nix shell "${nix_args[@]}" -c "$@"
}

# --- Parse arguments ---
PKG=""
SHELL_PKGS=""
SEARCH_KEYWORD=""
SEARCH_LIMIT=20
DO_UPDATE=false

while [[ $# -gt 0 ]]; do
  case "${1:-}" in
    --help)
      usage
      ;;
    --pkg)
      [[ -z "${2:-}" ]] && die "--pkg requires a package name"
      PKG="$2"
      shift 2
      ;;
    --shell)
      [[ -z "${2:-}" ]] && die "--shell requires comma-separated package names"
      SHELL_PKGS="$2"
      shift 2
      ;;
    --search)
      [[ -z "${2:-}" ]] && die "--search requires a keyword"
      SEARCH_KEYWORD="$2"
      shift 2
      ;;
    --limit)
      [[ -z "${2:-}" ]] && die "--limit requires a number"
      SEARCH_LIMIT="$2"
      shift 2
      ;;
    --update)
      DO_UPDATE=true
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      break
      ;;
  esac
done

# Handle update mode
if [[ "$DO_UPDATE" == true ]]; then
  do_update
  exit 0
fi

# Mutual exclusion checks
if [[ -n "$SHELL_PKGS" && -n "$PKG" ]]; then
  die "--shell and --pkg are mutually exclusive. Use one or the other."
fi
if [[ -n "$SHELL_PKGS" && -n "$SEARCH_KEYWORD" ]]; then
  die "--shell and --search are mutually exclusive. Use one or the other."
fi

# Handle search mode
if [[ -n "$SEARCH_KEYWORD" ]]; then
  do_search "$SEARCH_KEYWORD" "$SEARCH_LIMIT"
  exit 0
fi

# Handle shell (multi-package) mode
if [[ -n "$SHELL_PKGS" ]]; then
  do_shell "$SHELL_PKGS" "$@"
  exit 0
fi

[[ $# -lt 1 ]] && die "No command specified. Run '$SCRIPT_NAME --help' for usage."

CMD="$1"
shift

# 1) If command is already available locally, just run it
if command -v "$CMD" &>/dev/null; then
  exec "$CMD" "$@"
fi

# 2) If --pkg was specified, skip lookup
if [[ -n "$PKG" ]]; then
  info "Running '$CMD' from ${NIXPKGS_REF}#$PKG"
  exec nix shell "${NIXPKGS_REF}#$PKG" -c "$CMD" "$@"
fi

# 3) Use nix-locate to find the package
command -v nix-locate &>/dev/null || die "nix-locate not found. Install nix-index: nix profile install nixpkgs#nix-index && nix-index (or run: $SCRIPT_NAME --update)"

info "Looking up package for '$CMD'..."
CANDIDATES=()
while IFS= read -r line; do
  # nix-locate --minimal outputs attribute paths like "nixpkgs.jq" or "jq"
  # Strip "nixpkgs." prefix if present
  pkg="${line#nixpkgs.}"
  # Also strip any .out or .bin suffix (e.g. "package.out" -> "package")
  pkg="${pkg%.out}"
  pkg="${pkg%.bin}"
  CANDIDATES+=("$pkg")
done < <(nix-locate --minimal --whole-name --at-root "/bin/$CMD" 2>/dev/null || true)

# Deduplicate candidates
if [[ ${#CANDIDATES[@]} -gt 0 ]]; then
  readarray -t CANDIDATES < <(printf '%s\n' "${CANDIDATES[@]}" | sort -u)
fi

# 4) Evaluate candidates
if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
  die "No nix package found providing '/bin/$CMD'. Verify the command name is correct."
fi

if [[ ${#CANDIDATES[@]} -eq 1 ]]; then
  PKG="${CANDIDATES[0]}"
  info "Found package: $PKG"
  exec nix shell "${NIXPKGS_REF}#$PKG" -c "$CMD" "$@"
fi

# Multiple candidates: check for exact match (package name == command name)
for candidate in "${CANDIDATES[@]}"; do
  if [[ "$candidate" == "$CMD" ]]; then
    PKG="$candidate"
    info "Found exact match: $PKG"
    exec nix shell "${NIXPKGS_REF}#$PKG" -c "$CMD" "$@"
  fi
done

# Multiple candidates, no exact match: list them and exit
echo "MULTIPLE_CANDIDATES: Multiple packages provide '/bin/$CMD':" >&2
echo "" >&2
for candidate in "${CANDIDATES[@]}"; do
  echo "  - $candidate" >&2
done
echo "" >&2
echo "Re-run with --pkg to specify:" >&2
echo "  $SCRIPT_NAME --pkg <package> $CMD $*" >&2
exit 2
