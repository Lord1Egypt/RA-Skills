#!/bin/sh
# ─── Admirarr Installer ──────────────────────────────────────────────
# One command, any platform:
#
#   curl -fsSL https://get.admirarr.dev | sh
#
# Or with wget:
#   wget -qO- https://get.admirarr.dev | sh
#
# Options (environment variables):
#   ADMIRARR_INSTALL_DIR  — install location (default: ~/.local/bin or /usr/local/bin)
#   ADMIRARR_VERSION      — pin to a specific version (default: latest)
#   NO_COLOR              — disable colored output
# ──────────────────────────────────────────────────────────────────────
set -e

REPO="maxtechera/admirarr"
BINARY="admirarr"

# ── Colors ──

if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  BOLD='\033[1m' DIM='\033[2m' GREEN='\033[32m'
  RED='\033[31m' GOLD='\033[33m' RESET='\033[0m'
else
  BOLD='' DIM='' GREEN='' RED='' GOLD='' RESET=''
fi

info()  { printf "  ${GREEN}✓${RESET} %s\n" "$1"; }
warn()  { printf "  ${GOLD}!${RESET} %s\n" "$1"; }
fail()  { printf "  ${RED}✗${RESET} %s\n" "$1" >&2; exit 1; }
step()  { printf "  ${DIM}→${RESET} %s\n" "$1"; }

# ── Banner ──

printf "\n  ${GOLD}⚓${RESET} ${BOLD}ADMIRARR${RESET} ${DIM}installer${RESET}\n"
printf "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

# ── Detect platform ──

OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
  Linux*)          OS="linux"   ;;
  Darwin*)         OS="darwin"  ;;
  MINGW*|MSYS*|CYGWIN*) OS="windows" ;;
  *)               fail "Unsupported OS: $OS" ;;
esac

case "$ARCH" in
  x86_64|amd64)   ARCH="amd64" ;;
  aarch64|arm64)   ARCH="arm64" ;;
  armv7l)          ARCH="armv7" ;;
  *)               fail "Unsupported architecture: $ARCH" ;;
esac

step "Platform: ${OS}/${ARCH}"

# ── Check dependencies ──

HAS_CURL=false
HAS_WGET=false
command -v curl >/dev/null 2>&1 && HAS_CURL=true
command -v wget >/dev/null 2>&1 && HAS_WGET=true
$HAS_CURL || $HAS_WGET || fail "curl or wget is required"
command -v tar >/dev/null 2>&1 || fail "tar is required"

fetch() {
  if $HAS_CURL; then
    curl -fsSL "$1"
  else
    wget -qO- "$1"
  fi
}

download() {
  if $HAS_CURL; then
    curl -fsSL "$1" -o "$2"
  else
    wget -q "$1" -O "$2"
  fi
}

# ── Check Docker (warn, don't fail) ──

if command -v docker >/dev/null 2>&1; then
  DOCKER_VERSION=$(docker --version 2>/dev/null | head -1)
  info "Docker found: ${DOCKER_VERSION}"
else
  warn "Docker not found — required for 'admirarr setup' to deploy services"
  printf "    ${DIM}Install: https://docs.docker.com/get-docker/${RESET}\n"
fi

# ── Determine version ──

if [ -n "${ADMIRARR_VERSION:-}" ]; then
  VERSION="$ADMIRARR_VERSION"
  step "Version: ${VERSION} (pinned)"
else
  step "Fetching latest release..."
  RELEASE_JSON=$(fetch "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null) || fail "Cannot reach GitHub API. Set ADMIRARR_VERSION to install offline."
  VERSION=$(printf '%s' "$RELEASE_JSON" | grep '"tag_name"' | head -1 | sed 's/.*"tag_name": *"//;s/".*//')
  [ -z "$VERSION" ] && fail "Could not determine latest version"
  step "Version: ${VERSION}"
fi

VERSION_NUM="${VERSION#v}"

# ── Build download URL ──

EXT="tar.gz"
[ "$OS" = "windows" ] && EXT="zip"

FILENAME="${BINARY}_${VERSION_NUM}_${OS}_${ARCH}.${EXT}"
URL="https://github.com/${REPO}/releases/download/${VERSION}/${FILENAME}"

# ── Determine install directory ──

if [ -n "${ADMIRARR_INSTALL_DIR:-}" ]; then
  INSTALL_DIR="$ADMIRARR_INSTALL_DIR"
elif [ -w /usr/local/bin ]; then
  INSTALL_DIR="/usr/local/bin"
else
  INSTALL_DIR="${HOME}/.local/bin"
fi

# ── Download and extract ──

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

step "Downloading ${FILENAME}..."
download "$URL" "${TMPDIR}/${FILENAME}" || fail "Download failed: ${URL}"

step "Extracting..."
cd "$TMPDIR"
if [ "$EXT" = "zip" ]; then
  command -v unzip >/dev/null 2>&1 || fail "unzip is required for Windows archives"
  unzip -q "$FILENAME"
else
  tar -xzf "$FILENAME"
fi

# ── Find binary ──

FOUND=""
for candidate in \
  "${BINARY}" \
  "${BINARY}.exe" \
  */"${BINARY}" \
  */"${BINARY}.exe"; do
  if [ -f "$candidate" ]; then
    FOUND="$candidate"
    break
  fi
done
[ -z "$FOUND" ] && fail "Binary not found in archive"

# ── Install ──

mkdir -p "$INSTALL_DIR"

TARGET="${INSTALL_DIR}/${BINARY}"
[ "$OS" = "windows" ] && TARGET="${TARGET}.exe"

rm -f "$TARGET"
cp "$FOUND" "$TARGET"
chmod +x "$TARGET"

info "Installed to ${TARGET}"

# ── Verify ──

if "$TARGET" --version >/dev/null 2>&1; then
  INSTALLED=$("$TARGET" --version 2>&1 | head -1)
  info "${INSTALLED}"
fi

# ── PATH check ──

case ":${PATH}:" in
  *":${INSTALL_DIR}:"*) ;;
  *)
    printf "\n"
    warn "${INSTALL_DIR} is not in your PATH. Add it:\n"
    printf "    ${DIM}echo 'export PATH=\"%s:\$PATH\"' >> ~/.bashrc${RESET}\n" "$INSTALL_DIR"
    printf "    ${DIM}echo 'export PATH=\"%s:\$PATH\"' >> ~/.zshrc${RESET}\n" "$INSTALL_DIR"
    ;;
esac

# ── Done ──

printf "\n  ${GOLD}⚓${RESET} ${BOLD}Ready.${RESET} Run ${GOLD}admirarr setup${RESET} to deploy your stack.\n"
printf "  ${DIM}Or ${RESET}${GOLD}admirarr doctor${RESET}${DIM} if you already have one running.${RESET}\n\n"
