#!/usr/bin/env python3
"""
arXiv Source Downloader
Downloads source TeX files from arXiv.

Usage:
    python download_arxiv_source.py <arxiv_id_or_url> [output_dir]

Examples:
    python download_arxiv_source.py 2310.12345
    python download_arxiv_source.py https://arxiv.org/abs/2310.12345
    python download_arxiv_source.py https://arxiv.org/pdf/2310.12345.pdf ./output
"""

import argparse
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional, Tuple


def extract_arxiv_id(input_str: str) -> Optional[str]:
    """Extract arXiv ID from URL or direct ID."""
    input_str = input_str.strip()

    # Check if it's a URL
    if "arxiv.org" in input_str.lower():
        # Handle different arXiv URL formats
        # https://arxiv.org/abs/2310.12345
        # https://arxiv.org/pdf/2310.12345.pdf
        # https://arxiv.org/abs/hep-th/9901001
        match = re.search(r"arxiv\.org/(?:abs|pdf|e-print)/([^/\s]+)", input_str)
        if match:
            return match.group(1)

    # Assume it's a direct ID
    # New format: YYMM.NNNNN or old format: archive/YYMMNNN
    if re.match(r"^\d{4}\.\d{4,5}$|^\w+-\w+/\d{7}$|^\d{7}$", input_str):
        return input_str

    return None


def download_source(arxiv_id: str, output_dir: str) -> Tuple[bool, str]:
    """
    Download arXiv source file.

    Args:
        arxiv_id: The arXiv paper ID
        output_dir: Directory to extract files to

    Returns:
        Tuple of (success, message)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Download the source
    url = f"https://arxiv.org/e-print/{arxiv_id}"

    print(f"Downloading from: {url}")

    # Create a temporary file for the download
    with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp_file:
        temp_path = tmp_file.name

    try:
        # Download with curl (more reliable for large files)
        curl_cmd = [
            "curl",
            "-L",  # Follow redirects
            "-o",
            temp_path,
            "--retry",
            "3",
            "--retry-delay",
            "5",
            url,
        ]

        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            # Try wget as fallback
            print("curl failed, trying wget...")
            wget_cmd = ["wget", "-O", temp_path, "-e", "tries=3", url]
            result = subprocess.run(
                wget_cmd, capture_output=True, text=True, timeout=300
            )

            if result.returncode != 0:
                return False, f"Download failed: {result.stderr}"

        # Check if file is valid
        if os.path.getsize(temp_path) < 100:
            return (
                False,
                "Downloaded file is too small - paper may not have source available",
            )

        # Check if it's actually a tar file (arXiv returns tar.gz)
        # If it's HTML error page, it won't be a valid tar
        with open(temp_path, "rb") as f:
            header = f.read(2)
            # Check for gzip magic number
            if header != b"\x1f\x8b":
                # Might be an error page
                with open(temp_path, "r", encoding="utf-8", errors="ignore") as ef:
                    content = ef.read(500)
                    if "not found" in content.lower() or "error" in content.lower():
                        return (
                            False,
                            f"Paper not found or source not available. Response: {content[:200]}",
                        )

        # Extract the tar file
        print(f"Extracting to: {output_path}")
        with tarfile.open(temp_path, "r:gz") as tar:
            # Get the main directory in the archive
            members = tar.getmembers()
            if not members:
                return False, "Archive is empty"

            # Find the main directory
            main_dir = None
            for member in members:
                parts = member.name.split("/")
                if len(parts) > 1:
                    main_dir = parts[0]
                    break

            if main_dir:
                print(f"Main source directory: {main_dir}")

            # Extract all files
            tar.extractall(output_path)

        # Find the main .tex file
        tex_files = list(output_path.glob("**/*.tex"))

        if tex_files:
            main_tex = None
            # Prefer files named after the paper ID or 'main'
            for tex in tex_files:
                if main_dir and tex.name.replace(".tex", "") in [
                    main_dir,
                    arxiv_id.split(".")[0],
                ]:
                    main_tex = tex
                    break

            if not main_tex:
                main_tex = tex_files[0]

            print(f"Found {len(tex_files)} .tex files")
            print(f"Main TeX file: {main_tex.name}")

            return (
                True,
                f"Downloaded and extracted successfully. Main tex: {main_tex.name}",
            )
        else:
            return (
                True,
                f"Downloaded but no .tex files found. Check contents of {output_path}",
            )

    except subprocess.TimeoutExpired:
        return False, "Download timed out"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def main():
    parser = argparse.ArgumentParser(description="Download arXiv source TeX files")
    parser.add_argument(
        "arxiv_id_or_url",
        help="arXiv ID (e.g., 2310.12345) or URL (e.g., https://arxiv.org/abs/2310.12345)",
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=".",
        help="Output directory (default: current directory)",
    )

    args = parser.parse_args()

    # Extract arXiv ID
    arxiv_id = extract_arxiv_id(args.arxiv_id_or_url)

    if not arxiv_id:
        print(f"Error: Could not extract arXiv ID from: {args.arxiv_id_or_url}")
        print("\nSupported formats:")
        print("  - arXiv ID: 2310.12345, hep-th/9901001")
        print("  - arXiv URL: https://arxiv.org/abs/2310.12345")
        print("  - PDF URL: https://arxiv.org/pdf/2310.12345.pdf")
        return 1

    print(f"Detected arXiv ID: {arxiv_id}")

    # Download source
    success, message = download_source(arxiv_id, args.output_dir)

    print(message)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
