#!/usr/bin/env bash
set -euo pipefail
cd dist
sha256sum -- * > SHA256SUMS
gh release upload "$TAG" -R "$REPO" SHA256SUMS --clobber
