#!/usr/bin/env python3
"""
MarkItDown wrapper script for OpenClaw
Provides simplified interface for common document conversion tasks
"""

import argparse
import sys
import subprocess
from pathlib import Path
from typing import Optional


def run_markitdown(
    input_path: str,
    output_path: Optional[str] = None,
    format_type: str = "markdown",
    pages: Optional[str] = None,
    quiet: bool = False
) -> str:
    """
    Run markitdown conversion
    
    Args:
        input_path: Path to input file or URL
        output_path: Path to output file (optional)
        format_type: Output format (markdown, json, html, text)
        pages: Specific pages to extract (e.g., "1,3,5-7")
        quiet: Suppress console output
    
    Returns:
        Converted content as string
    """
    
    cmd = ["markitdown", input_path]
    
    if output_path:
        cmd.extend(["-o", output_path])
    
    if format_type != "markdown":
        cmd.extend(["--format", format_type])
    
    if pages:
        cmd.extend(["--pages", pages])
    
    if quiet:
        cmd.append("--quiet")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e.stderr}", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("markitdown not found. Install with: pipx install 'markitdown[all]'", file=sys.stderr)
        sys.exit(1)


def batch_convert(
    input_paths: list[str],
    output_dir: str,
    format_type: str = "markdown"
) -> list[tuple[str, str]]:
    """
    Batch convert multiple files
    
    Args:
        input_paths: List of input file paths
        output_dir: Directory for output files
        format_type: Output format
    
    Returns:
        List of (input_path, output_path) tuples
    """
    
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    for input_path in input_paths:
        input_file = Path(input_path)
        output_file = output_dir_path / f"{input_file.stem}.md"
        
        try:
            run_markitdown(input_path, str(output_file), format_type)
            results.append((input_path, str(output_file)))
            print(f"✓ Converted: {input_path} -> {output_file}")
        except Exception as e:
            print(f"✗ Failed: {input_path} - {e}")
            results.append((input_path, None))
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Convert documents to Markdown using markitdown"
    )
    
    parser.add_argument(
        "input",
        help="Input file path, URL, or directory"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "-f", "--format",
        default="markdown",
        choices=["markdown", "json", "html", "text"],
        help="Output format (default: markdown)"
    )
    
    parser.add_argument(
        "-p", "--pages",
        help="Specific pages to extract (e.g., '1,3,5-7')"
    )
    
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Batch mode: input is a directory"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress console output"
    )
    
    args = parser.parse_args()
    
    if args.batch:
        # Batch mode
        input_dir = Path(args.input)
        if not input_dir.is_dir():
            print(f"Error: {args.input} is not a directory", file=sys.stderr)
            sys.exit(1)
        
        output_dir = args.output or str(input_dir / "converted")
        
        # Find all supported files
        supported_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".html", ".htm"}
        files = [
            str(f) for f in input_dir.iterdir()
            if f.suffix.lower() in supported_extensions
        ]
        
        if not files:
            print(f"No supported files found in {args.input}", file=sys.stderr)
            sys.exit(1)
        
        results = batch_convert(files, output_dir, args.format)
        
        success_count = sum(1 for _, out in results if out is not None)
        print(f"\nConverted {success_count}/{len(results)} files to {output_dir}")
        
    else:
        # Single file mode
        try:
            result = run_markitdown(
                args.input,
                args.output,
                args.format,
                args.pages,
                args.quiet
            )
            
            if not args.output:
                print(result)
            else:
                print(f"✓ Converted: {args.input} -> {args.output}")
                
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
