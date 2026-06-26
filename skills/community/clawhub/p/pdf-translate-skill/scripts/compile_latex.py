#!/usr/bin/env python3
"""
LaTeX to PDF Compiler
Compiles LaTeX source files to PDF using XeLaTeX (for Chinese/CJK support).
Handles multiple compilation passes for references and TOC.

Requirements:
    - TeX Live or MiKTeX with XeLaTeX installed
    - ctex package for Chinese support

Usage:
    python compile_latex.py <input.tex> [output_dir] [--passes 3]

Output:
    Compiled PDF file in the same directory as input .tex file.

Note:
    For documents with citations (\cite{}) and references (\ref{}),
    use --passes 3 to ensure proper resolution:
    - Pass 1: Initial compilation
    - Pass 2: Resolve citations/references
    - Pass 3: Final resolution
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple


def find_xelatex() -> Optional[str]:
    """Find xelatex executable in PATH."""
    return shutil.which("xelatex")


def find_pdflatex() -> Optional[str]:
    """Find pdflatex executable in PATH."""
    return shutil.which("pdflatex")


def check_latex_installation() -> Tuple[bool, str]:
    """Check if LaTeX is properly installed."""
    xelatex = find_xelatex()
    pdflatex = find_pdflatex()

    if xelatex:
        return True, f"XeLaTeX found: {xelatex}"
    elif pdflatex:
        return True, f"pdfLaTeX found: {pdflatex} (limited CJK support)"
    else:
        return False, "No LaTeX installation found. Please install TeX Live or MiKTeX."


def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def compile_latex(
    tex_path: str,
    output_dir: Optional[str] = None,
    passes: int = 3,
    use_xelatex: bool = True,
) -> dict:
    """
    Compile LaTeX file to PDF.

    Args:
        tex_path: Path to the input .tex file
        output_dir: Directory for output (default: same as tex file)
        passes: Number of compilation passes (default: 3 for proper citation/reference resolution)
        use_xelatex: Use XeLaTeX instead of pdfLaTeX (recommended for CJK)

    Returns:
        Dict containing compilation results
    """
    tex_path = Path(tex_path).resolve()

    if not tex_path.exists():
        raise FileNotFoundError(f"LaTeX file not found: {tex_path}")

    if tex_path.suffix.lower() != ".tex":
        raise ValueError(f"Input file must be .tex, got: {tex_path.suffix}")

    # Check LaTeX installation
    installed, message = check_latex_installation()
    if not installed:
        raise RuntimeError(message)

    # Determine compiler
    if use_xelatex and find_xelatex():
        compiler = find_xelatex()
        compiler_name = "xelatex"
    elif find_pdflatex():
        compiler = find_pdflatex()
        compiler_name = "pdflatex"
        use_xelatex = False
    else:
        raise RuntimeError("No LaTeX compiler available")

    # Read tex content to check for Chinese
    tex_content = tex_path.read_text(encoding="utf-8")
    contains_chinese = has_chinese(tex_content)

    if contains_chinese and not use_xelatex:
        print(
            "Warning: Document contains Chinese but using pdfLaTeX. Consider using XeLaTeX for better support.",
            file=sys.stderr,
        )

    # Set output directory
    if output_dir:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = tex_path.parent

    # Prepare result dict
    result = {
        "input_file": str(tex_path),
        "compiler": compiler_name,
        "output_dir": str(output_dir),
        "passes_requested": passes,
        "passes_completed": 0,
        "success": False,
        "output_pdf": None,
        "log_file": None,
        "errors": [],
        "warnings": [],
    }

    # Compiler options
    cmd_base = [
        compiler,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={output_dir}",
        str(tex_path),
    ]

    print(f"Compiling with {compiler_name}...")
    print(f"Input: {tex_path}")
    print(f"Output directory: {output_dir}")

    # Run compilation passes
    for pass_num in range(1, passes + 1):
        print(f"\nPass {pass_num}/{passes}...")

        try:
            process = subprocess.run(
                cmd_base,
                capture_output=True,
                text=True,
                cwd=tex_path.parent,
                timeout=300,  # 5 minute timeout
            )

            result["passes_completed"] = pass_num

            # Check for errors
            if process.returncode != 0:
                # Parse log for errors
                log_content = process.stdout + process.stderr
                errors = re.findall(r"! (.+)", log_content)
                warnings = re.findall(r"LaTeX Warning: (.+)", log_content)

                result["errors"].extend(errors)
                result["warnings"].extend(warnings)

                if pass_num == passes:
                    result["log_file"] = str(
                        output_dir / tex_path.with_suffix(".log").name
                    )
                    print(f"Compilation failed with {len(errors)} error(s)")
                    for err in errors[:5]:  # Show first 5 errors
                        print(f"  Error: {err}")

        except subprocess.TimeoutExpired:
            result["errors"].append("Compilation timeout (>5 minutes)")
            print("Compilation timed out")
            break
        except Exception as e:
            result["errors"].append(str(e))
            print(f"Compilation error: {e}")
            break

    # Check for output PDF
    pdf_path = output_dir / tex_path.with_suffix(".pdf").name
    if pdf_path.exists():
        result["success"] = True
        result["output_pdf"] = str(pdf_path)
        print(f"\nSuccess! PDF created: {pdf_path}")
    else:
        result["success"] = False
        print(f"\nFailed to create PDF")

    # Save log file
    log_path = output_dir / tex_path.with_suffix(".log").name
    if log_path.exists():
        result["log_file"] = str(log_path)

    # Clean up auxiliary files
    aux_extensions = [
        ".aux",
        ".log",
        ".out",
        ".toc",
        ".lof",
        ".lot",
        ".fls",
        ".fdb_latexmk",
        ".synctex.gz",
    ]
    for ext in aux_extensions:
        aux_file = output_dir / tex_path.with_suffix(ext).name
        if aux_file.exists() and ext != ".pdf":
            try:
                aux_file.unlink()
            except:
                pass

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Compile LaTeX to PDF with XeLaTeX/pdfLaTeX"
    )
    parser.add_argument("input_tex", help="Path to the input .tex file")
    parser.add_argument(
        "--output-dir",
        "-o",
        default=None,
        help="Output directory for PDF (default: same as .tex file)",
    )
    parser.add_argument(
        "--passes",
        "-p",
        type=int,
        default=3,
        help="Number of compilation passes (default: 3 for proper citation/reference resolution)",
    )
    parser.add_argument(
        "--pdflatex", action="store_true", help="Use pdfLaTeX instead of XeLaTeX"
    )

    args = parser.parse_args()

    try:
        result = compile_latex(
            args.input_tex, args.output_dir, args.passes, use_xelatex=not args.pdflatex
        )

        # Print summary
        print("\n" + "=" * 50)
        print("COMPILATION SUMMARY")
        print("=" * 50)
        print(f"Compiler: {result['compiler']}")
        print(f"Passes: {result['passes_completed']}/{result['passes_requested']}")
        print(f"Success: {result['success']}")
        if result["output_pdf"]:
            print(f"Output: {result['output_pdf']}")
        if result["errors"]:
            print(f"Errors: {len(result['errors'])}")
        if result["warnings"]:
            print(f"Warnings: {len(result['warnings'])}")

        return 0 if result["success"] else 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
