#!/usr/bin/env bash
#
# build-gog-safe.sh — Build a safety-profiled gog binary from PR #366
#
# Usage:
#   ./build-gog-safe.sh <level> [--arch <GOARCH>] [--os <GOOS>] [--output <path>]
#
# Levels: L1 (draft), L2 (collaborate), L3 (standard)
#
# Examples:
#   ./build-gog-safe.sh L1                           # Build L1 for current platform
#   ./build-gog-safe.sh L2 --arch arm64 --os linux   # Cross-compile for Linux ARM64
#   ./build-gog-safe.sh L1 --output /tmp/gog-safe    # Custom output path
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROFILES_DIR="$SKILL_DIR/references"
BUILD_DIR="/tmp/gogcli-safety-build"
UPSTREAM_BRANCH="feat/safety-profiles"
UPSTREAM_REPO="https://github.com/drewburchfield/gogcli-safe.git"

# Defaults
LEVEL=""
GOARCH_OVERRIDE=""
GOOS_OVERRIDE=""
OUTPUT=""

usage() {
  echo "Usage: $0 <L1|L2|L3> [--arch <GOARCH>] [--os <GOOS>] [--output <path>]"
  echo ""
  echo "Safety Levels:"
  echo "  L1  Draft & Organize — no outbound messaging"
  echo "  L2  Draft & Collaborate — comments, RSVP, but no direct messaging"
  echo "  L3  Full Write (No Admin) — messaging allowed, admin ops blocked"
  echo ""
  echo "Options:"
  echo "  --arch    Target architecture (amd64, arm64). Default: current."
  echo "  --os      Target OS (linux, darwin). Default: current."
  echo "  --output  Output binary path. Default: bin/gog-<level>-safe"
  exit 1
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    L1|l1) LEVEL="L1"; shift ;;
    L2|l2) LEVEL="L2"; shift ;;
    L3|l3) LEVEL="L3"; shift ;;
    --arch) GOARCH_OVERRIDE="$2"; shift 2 ;;
    --os) GOOS_OVERRIDE="$2"; shift 2 ;;
    --output|-o) OUTPUT="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown argument: $1"; usage ;;
  esac
done

if [[ -z "$LEVEL" ]]; then
  echo "Error: safety level required (L1, L2, or L3)"
  usage
fi

# Map level to profile YAML
case "$LEVEL" in
  L1) PROFILE="$PROFILES_DIR/l1-draft.yaml" ;;
  L2) PROFILE="$PROFILES_DIR/l2-collaborate.yaml" ;;
  L3) PROFILE="$PROFILES_DIR/l3-standard.yaml" ;;
esac

if [[ ! -f "$PROFILE" ]]; then
  echo "Error: profile not found: $PROFILE"
  exit 1
fi

if [[ -z "$OUTPUT" ]]; then
  OUTPUT="$BUILD_DIR/bin/gog-$(echo "$LEVEL" | tr '[:upper:]' '[:lower:]')-safe"
fi

echo "=== gog Safety Build ==="
echo "Level:    $LEVEL"
echo "Profile:  $PROFILE"
echo "Output:   $OUTPUT"
[[ -n "$GOOS_OVERRIDE" ]] && echo "GOOS:     $GOOS_OVERRIDE"
[[ -n "$GOARCH_OVERRIDE" ]] && echo "GOARCH:   $GOARCH_OVERRIDE"
echo ""

# Step 1: Clone or update the PR branch
if [[ -d "$BUILD_DIR/.git" ]]; then
  echo "Updating existing checkout..."
  cd "$BUILD_DIR"
  git fetch origin "$UPSTREAM_BRANCH" 2>/dev/null || true
  git checkout "$UPSTREAM_BRANCH" 2>/dev/null
  git pull origin "$UPSTREAM_BRANCH" 2>/dev/null || true
else
  echo "Cloning gogcli PR #366 branch..."
  rm -rf "$BUILD_DIR"
  git clone --branch "$UPSTREAM_BRANCH" --depth 1 "$UPSTREAM_REPO" "$BUILD_DIR"
  cd "$BUILD_DIR"
fi

# Step 2: Copy our profile into the build tree
cp "$PROFILE" "$BUILD_DIR/safety-profile.yaml"
echo "Copied profile to build tree."

# Step 3: Generate command structs (must run on host platform)
echo "Generating command structs from profile..."
rm -f internal/cmd/*_cmd_gen.go
CGO_ENABLED=0 go run ./cmd/gen-safety --strict safety-profile.yaml

# Step 4: Build with cross-compilation if requested
VERSION=$(git describe --tags --always --dirty 2>/dev/null || echo "dev")
COMMIT=$(git rev-parse --short=12 HEAD 2>/dev/null || echo "")
DATE=$(date -u +%Y-%m-%dT%H:%M:%SZ)
LDFLAGS="-X github.com/steipete/gogcli/internal/cmd.version=${VERSION}-safe -X github.com/steipete/gogcli/internal/cmd.commit=${COMMIT} -X github.com/steipete/gogcli/internal/cmd.date=${DATE}"

mkdir -p "$(dirname "$OUTPUT")"

export CGO_ENABLED=0
[[ -n "$GOOS_OVERRIDE" ]] && export GOOS="$GOOS_OVERRIDE"
[[ -n "$GOARCH_OVERRIDE" ]] && export GOARCH="$GOARCH_OVERRIDE"

echo "Building with -tags safety_profile..."
go build -tags safety_profile -ldflags "$LDFLAGS" -o "$OUTPUT" ./cmd/gog/

echo ""
echo "Built: $OUTPUT"
echo "Profile: safety-profile.yaml"
"$OUTPUT" --version 2>/dev/null || echo "(cross-compiled — cannot run locally)"

echo ""
echo "=== Build Complete ==="
echo "Binary: $OUTPUT"
echo ""
echo "To deploy to a remote host:"
echo "  scp $OUTPUT <host>:/tmp/gog-safe"
echo "  ssh <host> 'sudo mv /usr/local/bin/gog /usr/local/bin/gog-backup && sudo mv /tmp/gog-safe /usr/local/bin/gog && sudo chmod +x /usr/local/bin/gog'"
echo "  ssh <host> 'gog --version'"
