#!/bin/sh
# p2claw installer.
#
# Usage:
#   curl -fsSL https://p2claw.com/install | sh
#   curl -fsSL https://p2claw.com/install | sh -s -- --version v0.1.0
#   curl -fsSL https://p2claw.com/install | sh -s -- --prefix /usr/local/bin
#
# Env overrides:
#   P2CLAW_VERSION       pin to a release tag (e.g. v0.1.0)
#   P2CLAW_INSTALL_DIR   install destination (default: $HOME/.local/bin)
#   P2CLAW_REPO          override release source (default: phact/p2claw-skill)
#
# Behaviour:
#   - macOS (Darwin) and Linux: downloads the matching binary from
#     GitHub releases, verifies SHA-256 if SHA256SUMS is published,
#     installs to ~/.local/bin/p2claw (no sudo).
#   - Windows (MINGW / MSYS / Cygwin): refuses with a clear pointer
#     to WSL; the agent's UDS local API + signal handling are
#     POSIX-only (`docs/local-api-auth.md §3`).
#
# This script is POSIX sh; no bashisms. `set -eu` makes any
# unhandled failure abort instead of silently moving on.

set -eu

REPO="${P2CLAW_REPO:-phact/p2claw-skill}"
INSTALL_DIR="${P2CLAW_INSTALL_DIR:-$HOME/.local/bin}"
VERSION="${P2CLAW_VERSION:-}"
BIN_NAME="p2claw"

# ---------- ANSI helpers (only when stdout is a tty) ------------------
if [ -t 1 ] && command -v tput >/dev/null 2>&1 && [ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]; then
  RED=$(printf '\033[31m'); YEL=$(printf '\033[33m'); GRN=$(printf '\033[32m')
  BLD=$(printf '\033[1m');  DIM=$(printf '\033[2m');  RST=$(printf '\033[0m')
else
  RED=; YEL=; GRN=; BLD=; DIM=; RST=
fi

say()  { printf '%s%s%s %s\n'  "$DIM" "→" "$RST" "$*"; }
ok()   { printf '%s✓%s %s\n'   "$GRN" "$RST" "$*"; }
warn() { printf '%swarn:%s %s\n' "$YEL" "$RST" "$*" >&2; }
err()  { printf '%serror:%s %s\n' "$RED" "$RST" "$*" >&2; exit 1; }

# ---------- argv parse ------------------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --version)        VERSION="$2"; shift 2 ;;
    --version=*)      VERSION="${1#*=}"; shift ;;
    --prefix)         INSTALL_DIR="$2"; shift 2 ;;
    --prefix=*)       INSTALL_DIR="${1#*=}"; shift ;;
    -h|--help)
      sed -n '/^# Usage:/,/^# Behaviour:/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    *) err "unknown flag: $1 (try --help)" ;;
  esac
done

# ---------- platform detection ----------------------------------------
OS_RAW="$(uname -s)"
case "$OS_RAW" in
  Darwin) OS="macos" ;;
  Linux)  OS="linux" ;;
  MINGW*|MSYS*|CYGWIN*|Windows_NT)
    printf '%sWindows detected — p2claw needs WSL.%s\n' "$YEL" "$RST" >&2
    cat >&2 <<EOF

The p2claw agent's local API + signal handling are POSIX-only
(docs/local-api-auth.md §3). On Windows, run it under WSL:

  1. Install WSL                ${BLD}wsl --install${RST}
  2. Open your Linux distro     (Ubuntu, Debian, …)
  3. Re-run inside WSL:         ${BLD}curl -fsSL https://p2claw.com/install | sh${RST}

If you already have WSL, open it now and try again.
EOF
    exit 1 ;;
  *) err "unsupported OS: $OS_RAW" ;;
esac

ARCH_RAW="$(uname -m)"
case "$ARCH_RAW" in
  x86_64|amd64)        ARCH="x86_64" ;;
  arm64|aarch64)       ARCH="aarch64" ;;
  armv7l|armv7|armhf)  err "32-bit ARM is not currently published; please open an issue at https://github.com/$REPO" ;;
  *) err "unsupported arch: $ARCH_RAW" ;;
esac

TARGET="${OS}-${ARCH}"

# ---------- prerequisites --------------------------------------------
require() { command -v "$1" >/dev/null 2>&1 || err "missing dependency: $1"; }
require curl
require uname
require tar

# Pick a SHA-256 verifier — Linux usually has sha256sum, macOS has shasum.
if   command -v sha256sum >/dev/null 2>&1; then SHA256_CMD="sha256sum"
elif command -v shasum    >/dev/null 2>&1; then SHA256_CMD="shasum -a 256"
else SHA256_CMD=""
fi

# ---------- resolve version ------------------------------------------
if [ -z "$VERSION" ]; then
  say "resolving latest release from $REPO …"
  # GitHub's "latest" redirects to the tag; pull tag_name out of the
  # JSON without jq (sed is everywhere).
  VERSION="$(
    curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null \
      | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p' \
      | head -n1
  )"
  [ -n "$VERSION" ] || err "could not resolve latest release for $REPO (rate-limited or no releases yet?). Pin one with --version or P2CLAW_VERSION."
fi
say "target: ${BLD}$TARGET${RST}, version: ${BLD}$VERSION${RST}"

# ---------- download --------------------------------------------------
ASSET="p2claw-${VERSION}-${TARGET}.tar.gz"
URL="https://github.com/$REPO/releases/download/$VERSION/$ASSET"

TMP="$(mktemp -d 2>/dev/null || mktemp -d -t p2claw)"
trap 'rm -rf "$TMP"' EXIT INT TERM

say "downloading $URL"
if ! curl -fSL --progress-bar -o "$TMP/$ASSET" "$URL"; then
  err "download failed. Verify that ${BLD}$ASSET${RST} exists at https://github.com/$REPO/releases/$VERSION"
fi

# ---------- verify checksum (best-effort) -----------------------------
SUMS_URL="https://github.com/$REPO/releases/download/$VERSION/SHA256SUMS"
if [ -n "$SHA256_CMD" ] && curl -fsSL -o "$TMP/SHA256SUMS" "$SUMS_URL" 2>/dev/null; then
  say "verifying SHA-256 …"
  EXPECTED="$(grep -E "[[:space:]]$ASSET\$" "$TMP/SHA256SUMS" | awk '{print $1}' | head -n1)"
  if [ -z "$EXPECTED" ]; then
    warn "SHA256SUMS published but didn't list $ASSET; skipping check"
  else
    GOT="$(cd "$TMP" && $SHA256_CMD "$ASSET" | awk '{print $1}')"
    if [ "$EXPECTED" = "$GOT" ]; then
      ok "checksum verified"
    else
      err "checksum mismatch (expected $EXPECTED, got $GOT)"
    fi
  fi
else
  warn "SHA256SUMS not published or no sha256 tool available; skipping integrity check"
fi

# ---------- extract + install ----------------------------------------
say "extracting …"
tar -xzf "$TMP/$ASSET" -C "$TMP"

# Most release tarballs unpack the binary at the root or in a single
# top-level dir. Find it either way.
SRC=""
if [ -f "$TMP/$BIN_NAME" ]; then
  SRC="$TMP/$BIN_NAME"
else
  SRC="$(find "$TMP" -type f -name "$BIN_NAME" -perm -u+x 2>/dev/null | head -n1 || true)"
fi
[ -n "$SRC" ] && [ -f "$SRC" ] || err "tarball did not contain an executable named $BIN_NAME"

mkdir -p "$INSTALL_DIR"
DEST="$INSTALL_DIR/$BIN_NAME"
mv "$SRC" "$DEST"
chmod +x "$DEST"
ok "installed $DEST"

# ---------- PATH hint -------------------------------------------------
case ":${PATH-}:" in
  *":$INSTALL_DIR:"*) ;;
  *)
    warn "$INSTALL_DIR is not on \$PATH"
    cat >&2 <<EOF

Add it once and reopen the shell:

  ${BLD}echo 'export PATH="$INSTALL_DIR:\$PATH"' >> ~/.zshrc${RST}     # zsh
  ${BLD}echo 'export PATH="$INSTALL_DIR:\$PATH"' >> ~/.bashrc${RST}    # bash

Or invoke the binary by its full path: ${BLD}$DEST${RST}
EOF
    ;;
esac

# ---------- next steps ------------------------------------------------
cat <<EOF

${GRN}p2claw $VERSION ready.${RST}

Recommended next:

  ${BLD}$BIN_NAME service install${RST}              # always-on user-scope service (no sudo)
  ${BLD}$BIN_NAME expose <name> <port>${RST}     # publish a localhost upstream as a peer URL

Alternatives:

  ${BLD}$BIN_NAME run${RST}                          # foreground daemon (one-off sharing)
  ${BLD}$BIN_NAME service install --help${RST}       # --system adds MagicDNS for direct-P2P box-to-box

Docs and skill setup: ${DIM}https://github.com/$REPO${RST}
EOF
