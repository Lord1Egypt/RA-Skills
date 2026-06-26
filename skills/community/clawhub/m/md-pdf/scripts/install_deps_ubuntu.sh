#!/usr/bin/env bash
set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "[ERROR] apt-get not found. This installer is for Ubuntu/Debian." >&2
  echo "Install manually: pandoc texlive-xetex fonts-noto-cjk" >&2
  exit 1
fi

SUDO=""
if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "[ERROR] Need root or sudo to install packages." >&2
    exit 1
  fi
fi

$SUDO apt-get update
$SUDO apt-get install -y pandoc texlive-xetex texlive-latex-extra fonts-noto-cjk nodejs npm

echo "[OK] Installed: pandoc, texlive-xetex, texlive-latex-extra, fonts-noto-cjk, nodejs, npm"
