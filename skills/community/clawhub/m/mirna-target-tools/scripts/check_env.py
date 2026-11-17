#!/usr/bin/env python3
"""
Check if required bioinformatics tools are installed.

Covers the external command-line tools, the Python packages, and the R
plotting engine (ggplot2) used for publication figures.
"""

import shutil
import subprocess
import sys

required_tools = {
    'targetscan': 'TargetScan',
    'miranda': 'miRanda',
    'cytoscape': 'Cytoscape'
}

required_packages = ['pandas', 'numpy']
optional_packages = {
    'mygene': 'gene annotation (annotate_targets.py)',
    'matplotlib': 'Python fallback plots (used only when R is unavailable)',
}

R_PLOT_PKGS = ['ggplot2', 'dplyr', 'stringr', 'scales']


def check_tool(tool_name):
    return shutil.which(tool_name) is not None


def r_engine_status():
    """Return (ok, version_or_message)."""
    if shutil.which('Rscript') is None:
        return False, 'Rscript not found on PATH'
    try:
        proc = subprocess.run(['Rscript', '-e', 'cat(R.version.string)'],
                              capture_output=True, text=True, timeout=180)
        version = proc.stdout.strip() or 'version unknown'
    except Exception as exc:
        return False, 'Rscript failed: %s' % exc
    check = ' && '.join('requireNamespace("%s", quietly=TRUE)' % p for p in R_PLOT_PKGS)
    try:
        proc = subprocess.run(['Rscript', '-e', 'cat(%s)' % check],
                              capture_output=True, text=True, timeout=240)
        ok = proc.stdout.strip().upper().startswith('TRUE')
    except Exception:
        ok = False
    if ok:
        return True, '%s + %s' % (version, '/'.join(R_PLOT_PKGS))
    return False, '%s, but missing packages: %s' % (version, ', '.join(R_PLOT_PKGS))


def main():
    print("Checking bioinformatics environment...\n")

    all_found = True

    print("External tools:")
    for tool, display in required_tools.items():
        if check_tool(tool):
            print("  OK       %s" % display)
        else:
            print("  MISSING  %s (optional - needed only for that step)" % display)

    print("\nPython packages:")
    for pkg in required_packages:
        try:
            __import__(pkg)
            print("  OK       %s (required)" % pkg)
        except ImportError:
            print("  MISSING  %s (required)" % pkg)
            all_found = False
    for pkg, purpose in optional_packages.items():
        try:
            __import__(pkg)
            print("  OK       %s (optional, for %s)" % (pkg, purpose))
        except ImportError:
            print("  MISSING  %s (optional, for %s)" % (pkg, purpose))

    print("\nR plotting engine (default for all figures):")
    ok, info = r_engine_status()
    if ok:
        print("  OK       R plotting available - %s" % info)
    else:
        print("  MISSING  R plotting unavailable - %s" % info)
        print("           Figures fall back to matplotlib; to enable the R engine run:")
        print("             bash %s/install_r_deps.sh" % _script_dir())

    print("\n%s" % ("All required dependencies installed!"
                    if all_found else "Missing required dependencies detected."))
    if not all_found:
        print("\nTo install missing dependencies, run:")
        print("  bash %s/install_dependencies.sh" % _script_dir())
        return 1
    return 0


def _script_dir():
    import os
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    sys.exit(main())
