#!/usr/bin/env bash
# Install R plus the R packages used for plotting by mirna-target-tools.
#
#   bash scripts/install_r_deps.sh             # R + required + optional packages
#   bash scripts/install_r_deps.sh --minimal   # required packages only
#
# Packages install into the user library (~/R/library), so no sudo is needed
# once R itself is present. If R is missing we try conda/mamba first and then
# print the system-package commands to run with sudo.
set -u

MINIMAL=0
[ "${1:-}" = "--minimal" ] && MINIMAL=1

have() { command -v "$1" >/dev/null 2>&1; }

# ---- 1. R itself ----------------------------------------------------------
if ! have Rscript; then
  echo "R is not installed."
  if have conda; then
    echo "-> installing R into your conda environment (no sudo needed) ..."
    conda install -y -c conda-forge r-base r-ggplot2 r-dplyr r-stringr r-scales \
      || echo "   conda install failed - install R manually (see below)"
  elif have mamba; then
    echo "-> installing R with mamba ..."
    mamba install -y -c conda-forge r-base r-ggplot2 r-dplyr r-stringr r-scales \
      || echo "   mamba install failed - install R manually (see below)"
  else
    cat <<'EOF'
No conda/mamba found. Install R with your system package manager, e.g.:

  Ubuntu/Debian : sudo apt-get update && sudo apt-get install -y r-base r-base-dev
  macOS (brew)  : brew install r
  Fedora        : sudo dnf install -y R R-devel

Then re-run this script.
EOF
    exit 1
  fi
fi

if ! have Rscript; then
  echo "R is still unavailable after the attempt - stopping." >&2
  exit 1
fi
echo "R found: $(Rscript -e 'cat(R.version.string)' 2>/dev/null)"

# ---- 2. R packages --------------------------------------------------------
REQUIRED="ggplot2 dplyr stringr scales"
OPTIONAL="svglite ggrepel patchwork ggsci forcats"
[ "${MINIMAL}" = "1" ] && OPTIONAL=""

echo "Installing R packages into: $(Rscript -e 'cat(.libPaths()[1])')"
Rscript -e '
pkg <- commandArgs(TRUE)
repos <- c(CRAN = "https://cloud.r-project.org")
missing <- setdiff(pkg, rownames(installed.packages()))
if (length(missing) == 0) {
  cat("all requested packages are already installed\n")
} else {
  cat("installing:", paste(missing, collapse = ", "), "\n")
  install.packages(missing, repos = repos, quiet = FALSE)
}
still <- setdiff(pkg, rownames(installed.packages()))
if (length(still)) {
  cat("WARNING: still missing:", paste(still, collapse = ", "), "\n")
  quit(status = 1)
}
cat("R plotting dependencies OK\n")
' $REQUIRED $OPTIONAL

echo
echo "Done. Plotting engine: R (ggplot2)."
echo "If a package failed to build, install the usual system headers and retry:"
echo "  sudo apt-get install -y libpng-dev libfreetype6-dev libfontconfig1-dev libxml2-dev"
