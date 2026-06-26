#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RELEASE_DIR="${SKILL_DIR}/assets/releases"
RUNTIME_DIR="${SKILL_DIR}/assets/runtime"

detect_target() {
  local os arch
  os="$(uname -s)"
  arch="$(uname -m)"

  case "${os}:${arch}" in
    Darwin:arm64)
      printf '%s\n' "darwin-arm64"
      ;;
    Darwin:x86_64)
      printf '%s\n' "darwin-x64"
      ;;
    Linux:aarch64|Linux:arm64)
      printf '%s\n' "linux-arm64"
      ;;
    Linux:x86_64)
      printf '%s\n' "linux-x64"
      ;;
    *)
      printf 'Unsupported environment: %s %s\n' "${os}" "${arch}" >&2
      printf '%s\n' "Supported targets: darwin-arm64, darwin-x64, linux-arm64, linux-x64" >&2
      exit 1
      ;;
  esac
}

TARGET="$(detect_target)"
ARCHIVE="${RELEASE_DIR}/ashen-cli-${TARGET}.tar.gz"
TARGET_DIR="${RUNTIME_DIR}/${TARGET}"
BINARY="${TARGET_DIR}/ashen-cli-${TARGET}"

if [[ "${1:-}" == "--print-target" ]]; then
  printf '%s\n' "${TARGET}"
  exit 0
fi

if [[ ! -f "${ARCHIVE}" ]]; then
  printf 'Missing release archive: %s\n' "${ARCHIVE}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

if [[ ! -x "${BINARY}" ]]; then
  rm -f "${BINARY}"
  tar -xzf "${ARCHIVE}" -C "${TARGET_DIR}"
  chmod +x "${BINARY}"
fi

if [[ "${1:-}" == "--" ]]; then
  shift
fi

if [[ "$#" -eq 0 ]]; then
  exec "${BINARY}" --help
fi

exec "${BINARY}" "$@"
