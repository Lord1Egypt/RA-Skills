#!/usr/bin/env bash
# Read version output only; never open the user's archive or credentials.
set -euo pipefail

require_version() {
  local name="$1" flag="$2" want_major="$3" want_minor="$4" want_patch="$5"
  local output major minor patch prerelease
  if ! command -v "$name" >/dev/null 2>&1; then
    printf '%s is required but was not found on PATH.\n' "$name" >&2
    return 1
  fi
  if ! output=$("$name" "$flag" 2>/dev/null); then
    printf 'Could not read %s version; check its installation.\n' "$name" >&2
    return 1
  fi
  if [[ "$output" =~ (^|[[:space:]])v?([0-9]{1,9})\.([0-9]{1,9})\.([0-9]{1,9})(-[0-9A-Za-z.-]+)?(\+[0-9A-Za-z.-]+)?([[:space:]]|$) ]]; then
    major=$((10#${BASH_REMATCH[2]}))
    minor=$((10#${BASH_REMATCH[3]}))
    patch=$((10#${BASH_REMATCH[4]}))
    prerelease="${BASH_REMATCH[5]}"
  else
    printf 'Could not identify a released %s version; install %s.%s.%s or newer.\n' "$name" "$want_major" "$want_minor" "$want_patch" >&2
    return 1
  fi
  if (( major > want_major || (major == want_major && minor > want_minor) ||
        (major == want_major && minor == want_minor && patch > want_patch) )) ||
     { (( major == want_major && minor == want_minor && patch == want_patch )) && [[ -z "$prerelease" ]]; }; then
    return 0
  fi
  printf '%s %s.%s.%s or newer is required.\n' "$name" "$want_major" "$want_minor" "$want_patch" >&2
  return 1
}

require_version openclaw --version 2026 8 1
require_version gmcli version 1 1 0
printf 'Runtime compatible: OpenClaw >=2026.8.1 and gmcli >=1.1.0.\n'
