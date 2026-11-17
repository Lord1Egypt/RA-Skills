#!/usr/bin/env bash
# Guard against emulated execution, then run the requested command.
# Emulated containers make every timing observation meaningless and every test
# slow enough to abandon, so a mismatch fails loudly instead of running.
set -euo pipefail

normalize_arch() {
  case "$1" in
    arm64|aarch64) printf 'arm64' ;;
    amd64|x86_64) printf 'amd64' ;;
    *) printf '%s' "$1" ;;
  esac
}

container_arch="$(normalize_arch "$(uname -m)")"
build_arch="$(normalize_arch "${LINE_OA_CONTAINER_BUILD_ARCH:-unknown}")"
host_arch="$(normalize_arch "${LINE_OA_CONTAINER_HOST_ARCH:-}")"

if [[ -z "$host_arch" ]]; then
  printf 'ERROR: LINE_OA_CONTAINER_HOST_ARCH is unset, so emulation cannot be ruled out.\n' >&2
  printf 'Run this container through containers/run.sh, which supplies the host architecture.\n' >&2
  exit 2
fi

if [[ "$container_arch" != "$host_arch" ]]; then
  printf 'ERROR: architecture mismatch (host=%s, container=%s).\n' "$host_arch" "$container_arch" >&2
  printf 'This container would run under emulation. Rebuild natively for %s.\n' "$host_arch" >&2
  exit 2
fi

if [[ "$build_arch" != "unknown" && "$build_arch" != "$container_arch" ]]; then
  printf 'ERROR: image was built for %s but is running as %s.\n' "$build_arch" "$container_arch" >&2
  exit 2
fi

exec "$@"
