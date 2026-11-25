#!/usr/bin/env python3
"""
Check if required bioinformatics tools are installed.

Covers the external command-line tools, the Python packages, and the R
plotting engine (ggplot2) used for publication figures.
"""

import os
import shutil
import subprocess
import sys

required_tools = {
    'miranda': 'miRanda 3.3a (default engine)',
}
optional_tools = {
    'targetscan': 'TargetScan',
    'RNAhybrid': 'RNAhybrid (refinement)',
    'cytoscape': 'Cytoscape',
}

required_packages = ['pandas', 'numpy']
optional_packages = {
    'mygene': 'gene annotation (annotate_targets.py)',
    'matplotlib': 'Python fallback plots (used only when R is unavailable)',
}

R_PLOT_PKGS = ['ggplot2', 'dplyr', 'stringr', 'scales']

# R code is passed as a fixed expression; package names travel as separate
# argv entries, so no user-controlled string is ever interpolated into R code.
R_PKG_CHECK = ('args <- commandArgs(TRUE); '
               'ok <- vapply(args, function(p) requireNamespace(p, quietly=TRUE), '
               'logical(1)); cat(all(ok))')


def find_tool(tool_name):
    """PATH first, then the usual conda prefixes (base env may be inactive)."""
    found = shutil.which(tool_name)
    if found:
        return found
    prefixes = []
    if os.environ.get("CONDA_PREFIX"):
        prefixes.append(os.environ["CONDA_PREFIX"])
    home = os.path.expanduser("~")
    prefixes.extend([os.path.join(home, p) for p in
                     ("anaconda3", "miniconda3", "mambaforge", "micromamba")])
    prefixes.extend(["/opt/conda", "/opt/miniconda3"])
    for prefix in prefixes:
        candidate = os.path.join(prefix, "bin", tool_name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def check_tool(tool_name):
    return find_tool(tool_name) is not None


def miranda_version(path):
    """Return the version string reported by `miranda --version` (or '')."""
    try:
        proc = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=30)
        text = (proc.stdout or '') + (proc.stderr or '')
        for line in text.splitlines():
            if 'miranda' in line.lower() and 'v' in line.lower():
                return line.strip()
        return text.strip().splitlines()[0] if text.strip() else ''
    except Exception:
        return


def r_engine_status():
    """Return (ok, version_or_message)."""
    rscript = find_tool('Rscript')
    if rscript is None:
        return False, 'Rscript not found on PATH or in a conda prefix'
    try:
        proc = subprocess.run([rscript, '--vanilla', '-e', 'cat(R.version.string)'],
                              capture_output=True, text=True, timeout=180)
        version = proc.stdout.strip() or 'version unknown'
    except Exception as exc:
        return False, 'Rscript failed: %s' % exc
    try:
        proc = subprocess.run([rscript, '--vanilla', '-e', R_PKG_CHECK] + R_PLOT_PKGS,
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

    print("Required external tools:")
    for tool, display in required_tools.items():
        resolved = find_tool(tool)
        if not resolved:
            print("  MISSING  %s" % display)
            print("           install with: bash %s/install_miranda_conda.sh" % _script_dir())
            all_found = False
            continue
        version = miranda_version(resolved) if tool == 'miranda' else ''
        if tool == 'miranda' and '3.3a' not in version.lower():
            print("  OK       %s (%s) but version is %r, expected 3.3a"
                  % (display, resolved, version or 'unknown'))
            print("           reinstall with: bash %s/install_miranda_conda.sh" % _script_dir())
            all_found = False
        else:
            print("  OK       %s (%s%s)"
                  % (display, resolved, (', ' + version) if version else ''))

    print("\nOptional external tools:")
    for tool, display in optional_tools.items():
        resolved = find_tool(tool)
        if resolved:
            print("  OK       %s (%s)" % (display, resolved))
        else:
            print("  MISSING  %s (optional)" % display)

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
        print("  bash %s/install_miranda_conda.sh   # required: real miRanda 3.3a" % _script_dir())
        print("  bash %s/install_dependencies.sh    # optional extras" % _script_dir())
        return 1
    return 0


def _script_dir():
    import os
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    sys.exit(main())
