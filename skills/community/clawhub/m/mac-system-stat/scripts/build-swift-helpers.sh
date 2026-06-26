#!/bin/zsh
set -euo pipefail

ROOT=${0:A:h}
SWIFT_DIR="$ROOT/swift"
BIN_DIR="$ROOT/bin"
mkdir -p "$BIN_DIR"

build_powerstat() {
  swiftc \
    -import-objc-header "$SWIFT_DIR/power_bridge.h" \
    "$SWIFT_DIR/powerstat_helper.swift" \
    -Xlinker -lIOReport \
    -o "$BIN_DIR/powerstat"
}

build_fanstat() {
  swiftc \
    "$SWIFT_DIR/fanstat_helper.swift" \
    -o "$BIN_DIR/fanstat"
}

build_gpustat() {
  swiftc \
    "$SWIFT_DIR/gpustat_helper.swift" \
    -o "$BIN_DIR/gpustat"
}

build_tempstat() {
  swiftc \
    "$SWIFT_DIR/tempstat_helper.swift" \
    -o "$BIN_DIR/tempstat"
}

TARGETS=("$@")
if (( ${#TARGETS[@]} == 0 )); then
  TARGETS=(powerstat fanstat gpustat tempstat)
fi

for target in "${TARGETS[@]}"; do
  case "$target" in
    powerstat) build_powerstat ;;
    fanstat) build_fanstat ;;
    gpustat) build_gpustat ;;
    tempstat) build_tempstat ;;
    *)
      echo "Unknown helper: $target" >&2
      exit 2
      ;;
  esac
done

echo "Built:"
for target in "${TARGETS[@]}"; do
  echo "  $BIN_DIR/$target"
done
