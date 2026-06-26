#!/usr/bin/env python3
"""
Dependencies checker and auto-installer for markitdown-file-converter.

Features:
- Dependency detection with clear status reporting
- Auto-installation of missing packages
- Version checking
- OS-specific installation hints
"""

import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Dependencies config
DEPENDENCIES = {
    'markitdown': {
        'packages': ['markitdown'],
        'optional': [],
        'install': 'pip install "markitdown[all]"',
    },
    'mammoth': {
        'packages': ['mammoth'],
        'optional': [],
        'install': 'pip install mammoth',
    },
    'rapidocr': {
        'packages': ['rapidocr_onnxruntime'],
        'optional': [],
        'install': 'pip install rapidocr-onnxruntime',
    },
    'pix2tex': {
        'packages': ['pix2tex'],
        'optional': ['torch', 'torchvision'],
        'install': 'pip install pix2tex',
    },
    'pdf2image': {
        'packages': ['pdf2image'],
        'optional': [],
        'install': 'pip install pdf2image',
    },
    'beautifulsoup': {
        'packages': ['bs4'],
        'optional': [],
        'install': 'pip install beautifulsoup4',
    },
    'pandoc': {
        'binary': 'pandoc',
        'install': 'winget install JohnMacFarlane.Pandoc' if platform.system() == 'Windows' else 'brew install pandoc',
    },
}


def check_module(name: str) -> bool:
    """Check if Python module is available."""
    return importlib.util.find_spec(name) is not None


def check_binary(name: str) -> bool:
    """Check if system binary is available."""
    return shutil.which(name) is not None


def check_pandoc() -> Tuple[bool, str]:
    """Check pandoc availability."""
    if check_binary('pandoc'):
        return True, "installed"
    if platform.system() == "Windows":
        p = Path(r"C:\Program Files\Pandoc\pandoc.EXE")
        if p.exists():
            return True, "installed (manual path)"
    return False, "not found"


def check_all_dependencies(verbose: bool = False) -> Dict[str, Dict]:
    """Check all dependencies and return status."""
    results = {}
    
    for name, config in DEPENDENCIES.items():
        if 'binary' in config:
            # System binary
            available, status = check_pandoc() if name == 'pandoc' else (check_binary(name), "installed")
            results[name] = {
                'available': available,
                'status': status,
                'type': 'binary',
            }
        else:
            # Python packages
            missing = []
            for pkg in config['packages']:
                if not check_module(pkg):
                    missing.append(pkg)
            
            results[name] = {
                'available': len(missing) == 0,
                'missing': missing,
                'optional': config.get('optional', []),
                'install': config['install'],
                'type': 'python',
            }
    
    if verbose:
        print("\n=== Dependency Status ===")
        for name, res in results.items():
            status = "OK" if res['available'] else "MISSING"
            print(f"  [{status}] {name}")
    
    return results


def auto_install_missing(verbose: bool = False) -> List[str]:
    """Auto-install missing Python packages."""
    results = check_all_dependencies()
    installed = []
    
    python = Path(sys.executable)
    
    for name, res in results.items():
        if res['type'] != 'python':
            continue
        if res['available']:
            continue
        
        install_cmd = res.get('install')
        if not install_cmd:
            continue
        
        if verbose:
            print(f"[install] Installing {name} ...")
        
        try:
            subprocess.run(
                [str(python), "-m", "pip", "install"] + install_cmd.split()[1:],
                check=True, capture_output=True, timeout=120
            )
            installed.append(name)
            if verbose:
                print(f"[install] {name} installed successfully")
        except Exception as e:
            if verbose:
                print(f"[install] {name} failed: {e}")
    
    return installed


def check_and_report() -> None:
    """Check dependencies and print report."""
    print("\n" + "="*50)
    print("markitdown-file-converter Dependencies Check")
    print("="*50)
    
    results = check_all_dependencies(verbose=True)
    
    all_available = all(r['available'] for r in results.values())
    
    print("\n" + "="*50)
    if all_available:
        print("All dependencies ready!")
    else:
        print("Some dependencies missing. Run with --install to auto-install.")
    print("="*50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check dependencies")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--install", action="store_true", help="Auto-install missing")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    if args.check:
        check_and_report()
    elif args.install:
        installed = auto_install_missing(verbose=args.verbose)
        print(f"\nInstalled: {installed}")
    else:
        check_and_report()