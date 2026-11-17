#!/usr/bin/env bash
# Run a command inside a test-environment variant.
#
# This wrapper constructs every mount itself and forwards no arbitrary Docker
# flags. That is deliberate: it is what makes "no real authenticated profile can
# be mounted" a property of the documented run path rather than a convention.
#
#   containers/run.sh <variant> [command ...]
#
# No port is published. Nothing is externally reachable unless a command run
# inside the container starts an outbound tunnel itself.
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image="${LINE_OA_TEST_IMAGE:-line-oa-test}"

usage() {
  cat <<'EOF'
Usage: containers/run.sh <variant> [command ...]

Variants:
  full              every dependency present
  no-runtime        no Python/Playwright runtime (and no uv)
  no-handoff-deps   no display/VNC/tunnel dependencies
  unauth-profile    every dependency present, profile exists but has no session

Default command is an interactive shell.
The repository is mounted read-only at /workspace.
The browser profile lives on a per-variant Docker volume, never a host path.
EOF
}

(( $# >= 1 )) || { usage >&2; exit 2; }
variant="$1"; shift
case "$variant" in
  full|no-runtime|no-handoff-deps|unauth-profile) ;;
  -h|--help) usage; exit 0 ;;
  *) printf 'ERROR: unknown variant: %s\n\n' "$variant" >&2; usage >&2; exit 2 ;;
esac

normalize_arch() {
  case "$1" in
    arm64|aarch64) printf 'arm64' ;;
    amd64|x86_64) printf 'amd64' ;;
    *) printf '%s' "$1" ;;
  esac
}
host_arch="$(normalize_arch "$(uname -m)")"

# The container is credential-free by construction. Refuse an inherited profile
# override rather than silently ignoring it, so an attempt to point the
# container at a real session is visible instead of quiet.
if [[ -n "${LINE_OA_SEND_CHAT_CHROMIUM_PROFILE:-}" ]]; then
  printf 'ERROR: LINE_OA_SEND_CHAT_CHROMIUM_PROFILE is set in this shell (%s).\n' \
    "$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE" >&2
  printf 'The test container never uses a host profile. Unset it before running.\n' >&2
  exit 2
fi

volume="line-oa-profile-${variant}"

# macOS ships bash 3.2, where expanding an empty array under `set -u` is an
# error, so both optional expansions use the +-guarded form.
tty_args=()
if [[ -t 0 && -t 1 ]]; then tty_args=(-it); fi
(( $# )) || set -- bash

# Two container-level concessions, both absent on the target host and both
# recorded as fidelity gaps in the change's design notes:
#
#   seccomp=unconfined  Docker's default seccomp filter blocks the namespace
#                       creation Chromium's zygote needs, so it aborts with
#                       "Failed to move to new namespace". Dropping the outer
#                       filter lets Chromium build its own sandbox, which stays
#                       intact -- this weakens the container's confinement, not
#                       the browser's. Preferred over --no-sandbox, which would
#                       mean teaching the scripts a container-only flag.
#   shm-size            Chromium exhausts the 64MB default under real page
#                       loads and dies with a broken zygote pipe.
# A stable hostname is required, not cosmetic. Chromium writes a SingletonLock
# into the profile recording the hostname that holds it. Docker assigns a random
# hostname per container, so a lock left by a killed container is seen as held
# "on another computer" and every later run is refused. With a fixed hostname
# Chromium recognizes the stale lock as its own, checks the dead PID, and breaks
# it. The same stale lock can strand a hard-killed Chromium on the target host.
exec docker run --rm ${tty_args[@]+"${tty_args[@]}"} \
  --platform "linux/${host_arch}" \
  --hostname "line-oa-test-${variant}" \
  --security-opt seccomp=unconfined \
  --shm-size=1g \
  -e LINE_OA_CONTAINER_HOST_ARCH="$host_arch" \
  -v "$repo_root:/workspace:ro" \
  -v "${volume}:/opt/data/chromium" \
  -w /workspace \
  "${image}:${variant}" \
  "$@"
