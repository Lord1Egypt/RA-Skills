#!/usr/bin/env bash
# Install (or verify) the real miRanda 3.3a binary from bioconda.
#
# The default workflow of mirna-target-tools uses a real miRanda 3.3a binary;
# there is no stub and no silent seed-only fallback when --method auto is used.
#
# Usage:
#   bash scripts/install_miranda_conda.sh            # install into the active/base env
#   bash scripts/install_miranda_conda.sh --check    # verify only, do not install
#   bash scripts/install_miranda_conda.sh --name env # install into a named conda env
#
# This script never calls sudo. It uses an existing conda/mamba/micromamba;
# if none is present it prints the Miniconda bootstrap commands and exits.
set -euo pipefail

CHECK_ONLY=0
ENV_NAME=""

usage() {
    sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --check) CHECK_ONLY=1; shift ;;
        --name)
            [ "$#" -ge 2 ] || { echo "Error: --name needs a value" >&2; exit 2; }
            ENV_NAME="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Error: unknown option '$1'" >&2; exit 2 ;;
    esac
done

find_conda() {
    local name path
    for name in conda mamba micromamba; do
        path="$(command -v "$name" 2>/dev/null || true)"
        if [ -n "$path" ]; then printf '%s\n' "$path"; return 0; fi
    done
    for path in \
        "${HOME:-/nonexistent}/anaconda3/bin/conda" \
        "${HOME:-/nonexistent}/miniconda3/bin/conda" \
        "${HOME:-/nonexistent}/mambaforge/bin/mamba" \
        /opt/conda/bin/conda \
        /opt/miniconda3/bin/conda; do
        if [ -x "$path" ]; then printf '%s\n' "$path"; return 0; fi
    done
    return 1
}

find_miranda() {
    local path
    path="$(command -v miranda 2>/dev/null || true)"
    if [ -n "$path" ]; then printf '%s\n' "$path"; return 0; fi
    for path in \
        "${CONDA_PREFIX:-/nonexistent}/bin/miranda" \
        "${HOME:-/nonexistent}/anaconda3/bin/miranda" \
        "${HOME:-/nonexistent}/miniconda3/bin/miranda" \
        "${HOME:-/nonexistent}/mambaforge/bin/miranda" \
        /opt/conda/bin/miranda \
        /opt/miniconda3/bin/miranda; do
        if [ -x "$path" ]; then printf '%s\n' "$path"; return 0; fi
    done
    return 1
}

miranda_version() {
    "$1" --version 2>&1 | tr -d '\r' | grep -oE 'v?3\.3a' | head -n 1 || true
}

verify() {
    local exe version
    if ! exe="$(find_miranda)"; then
        echo "Error: real miRanda 3.3a was not found." >&2
        echo "       Run: bash $0" >&2
        return 1
    fi
    version="$(miranda_version "$exe")"
    if [ "$version" != "3.3a" ] && [ "$version" != "v3.3a" ]; then
        echo "Error: found $exe but its version is not 3.3a (got '${version:-unknown}')." >&2
        echo "       Install the pinned build with: bash $0" >&2
        return 1
    fi
    echo "OK: real miRanda 3.3a -> $exe"
    return 0
}

if [ "$CHECK_ONLY" -eq 1 ]; then
    verify
    exit $?
fi

CONDA_BIN="$(find_conda || true)"
if [ -z "$CONDA_BIN" ]; then
    cat >&2 <<'EOF'
No conda/mamba/micromamba found. Real miRanda 3.3a is a prerequisite for the
default workflow. Install Miniconda first (no sudo), then re-run this script:

  curl -fsSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
       -o /tmp/miniconda.sh
  bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
  "$HOME/miniconda3/bin/conda" init bash
  exec "$SHELL" -l
  bash scripts/install_miranda_conda.sh

On macOS use Miniconda3-latest-MacOSX-x86_64.sh (Intel) or
Miniconda3-latest-MacOSX-arm64.sh (Apple Silicon).
EOF
    exit 1
fi

echo "Using conda: $CONDA_BIN"
case "$(basename "$CONDA_BIN")" in
    micromamba)
        if [ -n "$ENV_NAME" ]; then
            "$CONDA_BIN" install -y -n "$ENV_NAME" -c conda-forge -c bioconda "miranda=3.3a"
        else
            "$CONDA_BIN" install -y -c conda-forge -c bioconda "miranda=3.3a"
        fi
        ;;
    *)
        if [ -n "$ENV_NAME" ]; then
            "$CONDA_BIN" install -y -n "$ENV_NAME" -c bioconda -c conda-forge "miranda=3.3a"
        else
            "$CONDA_BIN" install -y -c bioconda -c conda-forge "miranda=3.3a"
        fi
        ;;
esac

verify
