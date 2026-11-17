#!/usr/bin/env bash
set -euo pipefail
umask 077
TASK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:---help}" in
  --check-only)
    if [ "$#" -ne 1 ]; then echo 'Usage: setup.sh --check-only' >&2; exit 2; fi
    exec python3 "$TASK_ROOT/tools/browser.py" doctor
    ;;
  --set-password)
    if [ "$#" -ne 2 ] || [[ "$2" != /* ]]; then
      echo 'Usage: setup.sh --set-password /absolute/path/to/new/passfile' >&2
      exit 2
    fi
    command -v x11vnc >/dev/null || { echo 'Install x11vnc first' >&2; exit 1; }
    if [ -e "$2" ] || [ -L "$2" ]; then echo 'Refusing to overwrite an existing passfile' >&2; exit 1; fi
    (set -o noclobber; : > "$2")
    trap 'rm -f -- "$2"' EXIT
    x11vnc -storepasswd "$2"
    chmod 600 "$2"
    if [ "$(wc -c < "$2" | tr -d ' ')" != 8 ]; then echo 'Invalid rfbauth output' >&2; exit 1; fi
    trap - EXIT
    echo "Set VNC_PASSFILE=$2 in .env (chmod 600) or your environment."
    ;;
  --help|--hints)
    cat <<'HELP'
Linux host setup (manual; review commands for your distribution):

Debian 12/13:
  sudo apt-get update
  sudo apt-get install -y xvfb xauth x11vnc x11-utils fluxbox chromium fonts-noto-cjk
Optional browser-based operator UI:
  sudo apt-get install -y novnc websockify

Install Node.js >=22 and Python >=3.10 from trusted distribution/vendor packages.
Then from the skill directory:
  npm ci --omit=dev
  ./scripts/setup.sh --set-password /absolute/path/to/new/passfile
  ./scripts/setup.sh --check-only

Ubuntu's chromium-browser may require Snap; use a vendor-packaged Chrome instead.
No package managers, remote scripts, or services are run by this installer.
Legacy --auto-install/--yes are no longer supported.
HELP
    ;;
  *) echo "Unsupported setup option: $1 (see --help)" >&2; exit 2 ;;
esac
