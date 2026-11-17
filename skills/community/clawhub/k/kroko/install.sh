#!/usr/bin/env bash
# Build KROKO and install it into the default Hermes profile and every named profile.
set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
NAME="kroko"
BINARY="$SOURCE/rust/target/release/kroko"

echo "KROKO install from: $SOURCE"
echo

echo "== 1. Build and test: the gate must be green before it polices anything =="
if ! command -v cargo >/dev/null 2>&1; then
    echo "kroko: cargo not found. KROKO is a Rust binary; install Rust from https://rustup.rs" >&2
    exit 2
fi
(cd "$SOURCE/rust" && cargo test --release --quiet && cargo build --release --quiet)
echo "   built and tested: $BINARY"
echo

echo "== 2. Targets =="
TARGETS=("$HERMES_HOME/skills/$NAME")
for profile in "$HERMES_HOME"/profiles/*/; do
    if [ -d "$profile/skills" ]; then
        TARGETS+=("${profile}skills/$NAME")
    fi
done
for target in "${TARGETS[@]}"; do
    echo "   $target"
done
echo

echo "== 3. Install, then verify the installed binary where it now lives =="
for target in "${TARGETS[@]}"; do
    mkdir -p "$target/bin"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete \
            --exclude '.git' --exclude 'target' --exclude '__pycache__' --exclude '*.pyc' \
            "$SOURCE/SKILL.md" "$SOURCE/README.md" "$SOURCE/LICENSE" "$SOURCE/install-hook.sh" \
            "$SOURCE/assets" "$SOURCE/references" "$SOURCE/rust" "$SOURCE/templates" \
            "$SOURCE/tests" "$SOURCE/tools" "$target/"
    else
        rm -rf "$target"
        mkdir -p "$target"
        cp -R "$SOURCE/SKILL.md" "$SOURCE/README.md" "$SOURCE/LICENSE" "$SOURCE/install-hook.sh" \
            "$SOURCE/assets" "$SOURCE/references" "$SOURCE/rust" "$SOURCE/templates" \
            "$SOURCE/tests" "$SOURCE/tools" "$target/"
    fi
    cp "$BINARY" "$target/bin/kroko"
    chmod +x "$target/bin/kroko"
    REPORT="$("$target/bin/kroko" "$target/tests/fixtures/bad_recursion.py" 2>&1 || true)"
    if ! printf '%s' "$REPORT" | grep -q "K001"; then
        echo "kroko: installed binary failed its own check in $target" >&2
        exit 1
    fi
    echo "   ok, verified in place: $target"
done

echo
echo "KROKO installed and verified in ${#TARGETS[@]} location(s)."
