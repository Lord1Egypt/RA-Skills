#!/usr/bin/env bash
# check_myl.sh — One-shot detection of `myl` installation.
#
# Exits 0 if myl is installed and runnable, prints the resolved path and
# version. Exits 1 otherwise with a one-line reason.
#
# Used by the imap-client skill to decide whether to run the install workflow
# in non-OpenClaw runtimes. (OpenClaw gates this skill on requires.bins=["myl"]
# and won't even load it without the binary on PATH.)

set -u

if ! command -v myl >/dev/null 2>&1; then
  echo "myl: NOT INSTALLED — not on PATH"
  exit 1
fi

MYL_PATH=$(command -v myl)
MYL_VERSION=$(myl --version 2>/dev/null | head -1 || echo "unknown")

# Sanity-check that --help exits cleanly. Catches half-broken installs where
# the wrapper script exists but the Python module / dependencies are missing.
if ! myl --help >/dev/null 2>&1; then
  echo "myl: BROKEN — found at $MYL_PATH but '--help' fails (likely missing deps)"
  exit 1
fi

echo "myl: OK — $MYL_PATH (version: $MYL_VERSION)"
exit 0
