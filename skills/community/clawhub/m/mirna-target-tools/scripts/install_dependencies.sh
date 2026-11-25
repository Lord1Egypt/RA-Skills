#!/usr/bin/env bash
# Install optional dependencies for mirna-target-tools.
#
# Security posture:
#   * never calls sudo and never installs system packages
#   * installs the real miRanda 3.3a from bioconda (no source-build fallback)
#   * Python packages go to the user site; R packages go to ~/R/library
#
# Usage:
#   bash scripts/install_dependencies.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
}

case "${1:-}" in
    -h|--help) usage; exit 0 ;;
    "") ;;
    *) echo "Error: unknown option '$1'" >&2; exit 2 ;;
esac

echo "Installing optional dependencies for mirna-target-tools..."
echo "System packages are NEVER installed automatically (no sudo in this script)."
echo

echo "Installing Python packages (user site, no sudo) ..."
if ! python3 -m pip install --user --upgrade pandas numpy mygene matplotlib; then
    echo "  pip install failed. Use a virtualenv or your distro packages instead." >&2
    exit 1
fi

echo
echo "Installing the real miRanda 3.3a with conda (no sudo, no source build) ..."
bash "${SCRIPT_DIR}/install_miranda_conda.sh"

cat <<'EOF'

TargetScan is not distributed here. Download it yourself from:
  https://www.targetscan.org/cgi-bin/targetscan/data_download.cgi

Cytoscape (optional GUI) is available from:
  https://cytoscape.org/download.html

Finally, verify the environment:
  python3 scripts/check_env.py

Real miRanda 3.3a is required by the default workflow.
Verify it directly with:
  bash scripts/install_miranda_conda.sh --check
EOF
