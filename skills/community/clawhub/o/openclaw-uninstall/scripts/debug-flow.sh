#!/usr/bin/env bash
# debug-flow.sh — Local debug: install → verify → uninstall flow
# Usage: ./scripts/debug-flow.sh [step]
# step: 1=install 2=verify 3=uninstall(confirm) or omit=interactive

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== OpenClaw Uninstall Skill — Debug Flow ==="
echo "Skill path: $SKILL_DIR"
echo ""

step="${1:-}"

# Step 1: Install (simulate — copy to ~/.openclaw/skills/)
do_install() {
  echo "[Step 1] Install"
  echo "  - From ClawHub: clawhub install openclaw-uninstall"
  echo "  - Or local copy: cp -r $SKILL_DIR ~/.openclaw/skills/"
  if [[ -d "$HOME/.openclaw/skills/openclaw-uninstall" ]]; then
    echo "  ✓ Already at ~/.openclaw/skills/openclaw-uninstall"
  else
    echo "  Running: cp -r $SKILL_DIR ~/.openclaw/skills/openclaw-uninstall"
    cp -r "$SKILL_DIR" ~/.openclaw/skills/openclaw-uninstall
    echo "  ✓ Copied"
  fi
  echo ""
}

# Step 2: Verify residue (read-only)
do_verify() {
  echo "[Step 2] Verify residue (read-only)"
  "$SCRIPT_DIR/verify-clean.sh" || true
  echo ""
}

# Step 3: Uninstall (confirm)
do_uninstall() {
  echo "[Step 3] Uninstall"
  echo "  Option A — IM-initiated (requires host=gateway):"
  echo "    $SCRIPT_DIR/schedule-uninstall.sh"
  echo ""
  echo "  Option B — CLI one-shot:"
  echo "    openclaw uninstall --all --yes --non-interactive"
  echo ""
  echo "  Option C — Direct one-shot:"
  echo "    $SCRIPT_DIR/uninstall-oneshot.sh"
  echo ""
  read -p "Run Option C (direct uninstall)? [y/N] " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    exec "$SCRIPT_DIR/uninstall-oneshot.sh"
  else
    echo "  Skipped. Run one of the commands above manually."
  fi
}

case "$step" in
  1) do_install ;;
  2) do_verify ;;
  3) do_uninstall ;;
  *)
    do_install
    do_verify
    echo "Next: run ./scripts/debug-flow.sh 3 for uninstall step"
    ;;
esac
