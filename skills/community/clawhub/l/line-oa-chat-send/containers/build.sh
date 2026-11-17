#!/usr/bin/env bash
# Build the test-environment variants. All four derive from one Dockerfile, so
# a change to the base reaches every variant without a separate edit.
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
image="${LINE_OA_TEST_IMAGE:-line-oa-test}"

normalize_arch() {
  case "$1" in
    arm64|aarch64) printf 'arm64' ;;
    amd64|x86_64) printf 'amd64' ;;
    *) printf '%s' "$1" ;;
  esac
}
host_arch="$(normalize_arch "$(uname -m)")"

# Variant name -> build arguments. This table is the only place variants differ.
variant_args() {
  case "$1" in
    full)            printf '%s' "" ;;
    no-runtime)      printf '%s' "--build-arg WITH_RUNTIME=0" ;;
    no-handoff-deps) printf '%s' "--build-arg WITH_HANDOFF_DEPS=0" ;;
    unauth-profile)  printf '%s' "--build-arg WITH_PROFILE=1" ;;
    *) return 1 ;;
  esac
}

variants=("$@")
if (( ${#variants[@]} == 0 )); then
  variants=(full no-runtime no-handoff-deps unauth-profile)
fi

for variant in "${variants[@]}"; do
  if ! args="$(variant_args "$variant")"; then
    printf 'ERROR: unknown variant: %s\n' "$variant" >&2
    printf 'Known variants: full no-runtime no-handoff-deps unauth-profile\n' >&2
    exit 2
  fi
  printf '\n=== building %s:%s (native %s) ===\n' "$image" "$variant" "$host_arch"
  # shellcheck disable=SC2086
  docker build \
    --platform "linux/${host_arch}" \
    -f "$repo_root/containers/Dockerfile" \
    --target variant \
    $args \
    -t "${image}:${variant}" \
    "$repo_root"
done

printf '\nBuilt: %s\n' "${variants[*]}"
