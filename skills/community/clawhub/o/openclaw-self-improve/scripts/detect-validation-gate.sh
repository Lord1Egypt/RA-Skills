#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  detect-validation-gate.sh --repo <path> [--verbose]

Detects common validation gates (test/build commands) in a repository
and prints the most likely one. Use --verbose to list all candidates.

Options:
  --repo <path>   Repository path to scan
  --verbose       Print all detected candidates
  -h, --help      Show this message
USAGE
}

REPO=""
VERBOSE="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --verbose) VERBOSE="true"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$REPO" ]]; then
  echo "Missing required --repo <path>" >&2; usage >&2; exit 1
fi
if [[ ! -d "$REPO" ]]; then
  echo "Repository path does not exist: $REPO" >&2; exit 1
fi

# Initialize as empty array to avoid `set -u` issues.
gates=()

add_gate() {
  local g="$1"
  # Dedup by checking each existing entry explicitly (no implicit join).
  local existing
  for existing in "${gates[@]:-}"; do
    [[ "$existing" == "$g" ]] && return 0
  done
  gates+=("$g")
}

# Node.js / package.json
if [[ -f "$REPO/package.json" ]]; then
  if grep -q '"test"' "$REPO/package.json"; then
    if [[ -f "$REPO/pnpm-lock.yaml" ]]; then
      add_gate "pnpm test"
    elif [[ -f "$REPO/yarn.lock" ]]; then
      add_gate "yarn test"
    else
      add_gate "npm test"
    fi
  fi
  if grep -q '"build"' "$REPO/package.json"; then
    if [[ -f "$REPO/pnpm-lock.yaml" ]]; then
      add_gate "pnpm build"
    else
      add_gate "npm run build"
    fi
  fi
fi

# Python
if [[ -f "$REPO/setup.py" || -f "$REPO/pyproject.toml" || -f "$REPO/requirements.txt" ]]; then
  if [[ -f "$REPO/pytest.ini" || -d "$REPO/tests" || -d "$REPO/test" ]]; then
    add_gate "pytest"
  else
    add_gate "python3 -m pytest"
  fi
fi

# Go
if [[ -f "$REPO/go.mod" ]]; then
  add_gate "go test ./..."
fi

# Rust
if [[ -f "$REPO/Cargo.toml" ]]; then
  add_gate "cargo test"
fi

# Java / Maven
if [[ -f "$REPO/pom.xml" ]]; then
  add_gate "mvn test"
fi

# Java / Gradle
if [[ -f "$REPO/build.gradle" || -f "$REPO/build.gradle.kts" ]]; then
  if [[ -x "$REPO/gradlew" ]]; then
    add_gate "./gradlew test"
  else
    add_gate "gradle test"
  fi
fi

# Make
if [[ -f "$REPO/Makefile" ]]; then
  if grep -qE "^test:" "$REPO/Makefile"; then
    add_gate "make test"
  fi
  if grep -qE "^check:" "$REPO/Makefile"; then
    add_gate "make check"
  fi
fi

# Docker
if [[ -f "$REPO/Dockerfile" ]]; then
  add_gate "docker build ."
fi

# Shell
for cand in test.sh run-tests.sh tests.sh; do
  if [[ -f "$REPO/$cand" ]]; then
    add_gate "bash $cand"
  fi
done

if [[ "$VERBOSE" == "true" ]]; then
  if [[ ${#gates[@]} -eq 0 ]]; then
    echo "No validation gates detected."
    exit 3
  else
    echo "Detected validation gates:"
    for g in "${gates[@]}"; do echo "  - $g"; done
    exit 0
  fi
else
  if [[ ${#gates[@]} -eq 0 ]]; then
    # Be honest: don't fabricate a default, but signal the user via exit code
    # so a calling script can distinguish "no gates found" (exit 3) from
    # "detection succeeded" (exit 0).
    echo "No validation gates detected. Pass --verbose to see what was scanned." >&2
    exit 3
  fi
  printf '%s\n' "${gates[0]}"
fi
