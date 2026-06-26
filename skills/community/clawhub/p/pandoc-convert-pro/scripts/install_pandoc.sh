#!/usr/bin/env bash
set -euo pipefail

YES=0

show_help() {
    cat <<'EOF'
Usage: install_pandoc.sh [--yes]

Detects whether Pandoc is installed and recommends an installation command.
By default this script is dry-run only and does not modify the system.
Pass --yes to execute the detected install command.

Supported package managers: Homebrew, Conda, apt-get, dnf, pacman.
PDF engines are not installed by this script.
EOF
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --yes|-y)
            YES=1
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Error: unknown option: $1" >&2
            show_help >&2
            exit 1
            ;;
    esac
done

if command -v pandoc >/dev/null 2>&1; then
    echo "Pandoc is already installed:"
    pandoc --version | sed -n '1p'
    exit 0
fi

echo "Pandoc is not installed or not found in PATH."

OS_NAME="$(uname -s 2>/dev/null || printf 'unknown')"
INSTALL_CMD=""
MANAGER_NOTE=""

if command -v brew >/dev/null 2>&1; then
    INSTALL_CMD="brew install pandoc"
    MANAGER_NOTE="Homebrew detected."
elif command -v conda >/dev/null 2>&1; then
    INSTALL_CMD="conda install -c conda-forge pandoc"
    MANAGER_NOTE="Conda detected."
elif command -v apt-get >/dev/null 2>&1; then
    INSTALL_CMD="sudo apt-get update && sudo apt-get install -y pandoc"
    MANAGER_NOTE="apt-get detected."
elif command -v dnf >/dev/null 2>&1; then
    INSTALL_CMD="sudo dnf install -y pandoc"
    MANAGER_NOTE="dnf detected."
elif command -v pacman >/dev/null 2>&1; then
    INSTALL_CMD="sudo pacman -S --needed pandoc"
    MANAGER_NOTE="pacman detected."
fi

if [ -n "$INSTALL_CMD" ]; then
    echo "$MANAGER_NOTE"
    echo "Recommended command:"
    echo "  $INSTALL_CMD"
else
    echo "No supported package manager was detected automatically."
    case "$OS_NAME" in
        Darwin)
            echo "Recommended options for macOS: install Homebrew and run 'brew install pandoc', use Conda, or download the official installer."
            ;;
        Linux)
            echo "Recommended options for Linux: use your package manager, Conda, or Pandoc's official tarball."
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "Recommended options for Windows: use winget/choco, Conda, or the official installer."
            ;;
        *)
            echo "See https://pandoc.org/installing.html for platform-specific installers."
            ;;
    esac
    echo "This script will not install anything without a detected package manager."
    exit 1
fi

if [ "$YES" -ne 1 ]; then
    echo "Dry run only. Re-run with --yes to execute the command."
    echo "PDF output may still require a separate PDF engine such as xelatex, lualatex, pdflatex, or tectonic."
    exit 0
fi

echo "Executing install command..."
# shellcheck disable=SC2086
sh -c "$INSTALL_CMD"

if command -v pandoc >/dev/null 2>&1; then
    echo "Pandoc installation verified:"
    pandoc --version | sed -n '1p'
    echo "PDF output may still require a separate PDF engine such as xelatex, lualatex, pdflatex, or tectonic."
else
    echo "Error: install command finished, but pandoc is still not found in PATH." >&2
    exit 1
fi
