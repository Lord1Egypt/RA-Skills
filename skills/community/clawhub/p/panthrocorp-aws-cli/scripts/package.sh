#!/usr/bin/env bash
set -euo pipefail

VERSION=""
ARCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) VERSION="$2"; shift 2 ;;
    --arch)    ARCH="$2";    shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$VERSION" || -z "$ARCH" ]]; then
  echo "Usage: package.sh --version <version> --arch <amd64|arm64>" >&2
  exit 1
fi

case "$ARCH" in
  arm64)  AWS_ARCH="aarch64" ;;
  amd64)  AWS_ARCH="x86_64"  ;;
  *) echo "Unsupported arch: $ARCH (must be amd64 or arm64)" >&2; exit 1 ;;
esac

HOST_ARCH="$(uname -m)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="${SKILL_DIR}/dist"
WORK_DIR="$(mktemp -d)"

cleanup() { rm -rf "$WORK_DIR"; }
trap cleanup EXIT

echo "Downloading AWS CLI v2 for linux/${ARCH}..."
curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-${AWS_ARCH}.zip" -o "${WORK_DIR}/awscli.zip"

ZIP_SIZE=$(stat --format=%s "${WORK_DIR}/awscli.zip")
MIN_ZIP_SIZE=$((30 * 1024 * 1024))
if [[ "$ZIP_SIZE" -lt "$MIN_ZIP_SIZE" ]]; then
  echo "Downloaded zip too small (${ZIP_SIZE} bytes), likely truncated" >&2
  exit 1
fi
echo "Download OK: $(numfmt --to=iec "$ZIP_SIZE")"

echo "Extracting installer..."
unzip -q "${WORK_DIR}/awscli.zip" -d "${WORK_DIR}"

STAGING="${WORK_DIR}/staging"
INSTALLER_DIR="${WORK_DIR}/aws"
INSTALLER_DIST="${INSTALLER_DIR}/dist"

if [[ "$AWS_ARCH" == "$HOST_ARCH" ]]; then
  echo "Native arch build, using official installer..."
  mkdir -p "${STAGING}/bin"
  "${INSTALLER_DIR}/install" \
    --install-dir "${STAGING}/aws-cli" \
    --bin-dir "${STAGING}/bin" \
    > /dev/null
  AWS_CLI_VERSION=$("${STAGING}/aws-cli/v2/current/bin/aws" --version 2>&1)
  echo "Bundled version: ${AWS_CLI_VERSION}"
else
  echo "Cross-arch build (host=${HOST_ARCH}, target=${AWS_ARCH}), manual install..."
  AWS_EXE_VERSION="latest"
  INSTALL_DIR="${STAGING}/aws-cli/v2/${AWS_EXE_VERSION}"
  mkdir -p "${INSTALL_DIR}/bin" "${STAGING}/bin"
  cp -r "${INSTALLER_DIST}" "${INSTALL_DIR}/dist"
  ln -s "../dist/aws" "${INSTALL_DIR}/bin/aws"
  ln -s "../dist/aws_completer" "${INSTALL_DIR}/bin/aws_completer"
  ln -snf "${AWS_EXE_VERSION}" "${STAGING}/aws-cli/v2/current"
  ln -sf "../aws-cli/v2/current/bin/aws" "${STAGING}/bin/aws"
  ln -sf "../aws-cli/v2/current/bin/aws_completer" "${STAGING}/bin/aws_completer"
fi

echo "Fixing symlinks to be relative..."
mapfile -t versions < <(find "${STAGING}/aws-cli/v2/" -maxdepth 1 -mindepth 1 -type d ! -name current -printf '%f\n')
if [[ ${#versions[@]} -ne 1 ]]; then
  echo "Expected exactly 1 version dir, found: ${versions[*]}" >&2
  exit 1
fi
AWS_VER_DIR="${versions[0]}"

if [[ -L "${STAGING}/aws-cli/v2/current" ]]; then
  rm -f "${STAGING}/aws-cli/v2/current"
  ln -s "${AWS_VER_DIR}" "${STAGING}/aws-cli/v2/current"
fi
if [[ -L "${STAGING}/bin/aws" ]]; then
  rm -f "${STAGING}/bin/aws" "${STAGING}/bin/aws_completer"
  ln -s ../aws-cli/v2/current/bin/aws "${STAGING}/bin/aws"
  ln -s ../aws-cli/v2/current/bin/aws_completer "${STAGING}/bin/aws_completer"
fi

mkdir -p "$DIST_DIR"
TARBALL="aws-cli_${VERSION}_linux_${ARCH}.tar.gz"

echo "Packaging ${TARBALL}..."
tar -czf "${DIST_DIR}/${TARBALL}" -C "${STAGING}" aws-cli bin

TARBALL_SIZE=$(stat --format=%s "${DIST_DIR}/${TARBALL}")
MIN_SIZE=$((10 * 1024 * 1024))
if [[ "$TARBALL_SIZE" -lt "$MIN_SIZE" ]]; then
  echo "Tarball too small (${TARBALL_SIZE} bytes), expected at least 10 MB" >&2
  exit 1
fi

echo "Done: ${DIST_DIR}/${TARBALL}"
ls -lh "${DIST_DIR}/${TARBALL}"
