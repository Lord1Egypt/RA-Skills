#!/bin/bash
set -e

echo "Installing Polymarket CLI..."

# Try pre-built binary first
if curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh 2>/dev/null; then
  # Verify it works (GLIBC compatibility)
  if polymarket --version 2>/dev/null; then
    echo "✅ Polymarket CLI installed (pre-built)"
    exit 0
  fi
  echo "Pre-built binary incompatible, building from source..."
fi

# Build from source
if ! command -v cargo &>/dev/null; then
  echo "Installing Rust..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  source "$HOME/.cargo/env"
fi

TMPDIR=$(mktemp -d)
git clone --depth 1 https://github.com/Polymarket/polymarket-cli.git "$TMPDIR/polymarket-cli"
cd "$TMPDIR/polymarket-cli"
cargo install --path .
rm -rf "$TMPDIR"

echo "✅ Polymarket CLI installed (from source)"
polymarket --version
