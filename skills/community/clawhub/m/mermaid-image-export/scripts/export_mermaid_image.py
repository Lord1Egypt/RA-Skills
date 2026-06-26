#!/usr/bin/env python3
"""
Mermaid Diagram Image Exporter

Export Mermaid diagrams to PNG, SVG, or PDF using mermaid-cli.
Supports batch processing, custom themes, and quality settings.
"""

import sys
import os
import subprocess
import argparse
import tempfile
import json
import yaml
from pathlib import Path
from typing import List, Optional

def check_dependencies():
    """Check if mermaid-cli is available."""
    # Try mmdc (global) first
    try:
        subprocess.run(["mmdc", "--version"], capture_output=True, check=True)
        return "mmdc"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Try npx mmdc
    try:
        subprocess.run(["npx", "mmdc", "--version"], capture_output=True, check=True)
        return "npx mmdc"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    return None

def run_mermaid_cli(
    input_file: str,
    output_file: str,
    format: str = "png",
    theme: str = "default",
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: float = 1.0,
    background: str = "transparent",
    css_file: Optional[str] = None,
    config_file: Optional[str] = None,
    quiet: bool = False,
    mermaid_cmd: str = "mmdc"
):
    """Run mermaid-cli to export diagram."""
    
    cmd = mermaid_cmd.split() if isinstance(mermaid_cmd, str) else mermaid_cmd
    
    # Base arguments
    cmd.extend([
        "-i", input_file,
        "-o", output_file,
        "-t", theme,
        "-b", background,
    ])
    
    # Format specific
    if format.lower() == "pdf":
        cmd.append("-p", "puppeteerConfig.json")
    
    # Optional arguments
    if width:
        cmd.extend(["-w", str(width)])
    if height:
        cmd.extend(["-H", str(height)])
    if scale != 1.0:
        cmd.extend(["-s", str(scale)])
    if css_file:
        cmd.extend(["-c", css_file])
    if config_file:
        cmd.extend(["-C", config_file])
    if quiet:
        cmd.append("-q")
    
    if not quiet:
        print(f"Exporting: {input_file} -> {output_file}")
        print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        if result.returncode != 0:
            print(f"Error exporting {input_file}:", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return False
        
        if not quiet:
            print(f"✅ Successfully exported to {output_file}")
            if result.stdout:
                print(result.stdout.strip())
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"Timeout exporting {input_file}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error exporting {input_file}: {e}", file=sys.stderr)
        return False

def validate_format(format: str) -> bool:
    """Validate output format."""
    valid_formats = ["png", "svg", "pdf"]
    return format.lower() in valid_formats

def get_output_filename(input_path: Path, output_dir: Optional[Path], 
                       format: str, suffix: str = "") -> Path:
    """Generate output filename."""
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        if suffix:
            stem = f"{input_path.stem}_{suffix}"
        else:
            stem = input_path.stem
        return output_dir / f"{stem}.{format}"
    else:
        if suffix:
            stem = f"{input_path.stem}_{suffix}"
        else:
            stem = input_path.stem
        return input_path.with_name(f"{stem}.{format}")

def create_puppeteer_config(width: Optional[int], height: Optional[int]) -> str:
    """Create Puppeteer config for PDF export."""
    config = {
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
        "headless": "new"
    }
    
    if width or height:
        config["defaultViewport"] = {}
        if width:
            config["defaultViewport"]["width"] = width
        if height:
            config["defaultViewport"]["height"] = height
    
    return json.dumps(config, indent=2)

def export_single(
    input_path: Path,
    output_path: Path,
    format: str,
    theme: str,
    width: Optional[int],
    height: Optional[int],
    scale: float,
    background: str,
    css_file: Optional[str],
    config_file: Optional[str],
    quiet: bool,
    mermaid_cmd: str
):
    """Export a single diagram."""
    
    # Validate format
    if not validate_format(format):
        print(f"Error: Invalid format '{format}'. Must be one of: png, svg, pdf", 
              file=sys.stderr)
        return False
    
    # Check input file exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return False
    
    # Create parent directories for output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # For PDF, create Puppeteer config
    if format.lower() == "pdf":
        config_content = create_puppeteer_config(width, height)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(config_content)
            config_file = f.name
        
        try:
            success = run_mermaid_cli(
                str(input_path), str(output_path), format, theme,
                width, height, scale, background, css_file, config_file,
                quiet, mermaid_cmd
            )
        finally:
            if os.path.exists(config_file):
                os.unlink(config_file)
    else:
        success = run_mermaid_cli(
            str(input_path), str(output_path), format, theme,
            width, height, scale, background, css_file, config_file,
            quiet, mermaid_cmd
        )
    
    return success

def export_batch(
    input_files: List[Path],
    output_dir: Optional[Path],
    format: str,
    theme: str,
    width: Optional[int],
    height: Optional[int],
    scale: float,
    background: str,
    css_file: Optional[str],
    config_file: Optional[str],
    quiet: bool,
    mermaid_cmd: str
):
    """Export multiple diagrams."""
    success_count = 0
    total_count = len(input_files)
    
    print(f"Batch exporting {total_count} files to {format.upper()}...")
    
    for i, input_path in enumerate(input_files, 1):
        if not quiet:
            print(f"\n[{i}/{total_count}] Processing: {input_path.name}")
        
        output_path = get_output_filename(input_path, output_dir, format)
        
        success = export_single(
            input_path, output_path, format, theme,
            width, height, scale, background, css_file, config_file,
            True, mermaid_cmd  # Always quiet in batch mode
        )
        
        if success:
            success_count += 1
            if not quiet:
                print(f"  → {output_path.name}")
        else:
            if not quiet:
                print(f"  ❌ Failed")
    
    print(f"\nBatch complete: {success_count}/{total_count} successful")
    return success_count == total_count

def main():
    parser = argparse.ArgumentParser(
        description="Export Mermaid diagrams to images using mermaid-cli",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export single diagram to PNG
  %(prog)s diagram.mmd -o output.png
  
  # Export to SVG with dark theme
  %(prog)s diagram.mmd -f svg -t dark -o diagram.svg
  
  # Export with high resolution
  %(prog)s diagram.mmd --scale 2.0 -o highres.png
  
  # Batch export all .mmd files
  %(prog)s *.mmd -d outputs/
  
  # Export to PDF with custom width
  %(prog)s diagram.mmd -f pdf -w 1200 -o diagram.pdf
"""
    )
    
    # Input/output
    parser.add_argument(
        "input", nargs="+",
        help="Input Mermaid file(s) (.mmd) or directory"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file (for single file export)"
    )
    parser.add_argument(
        "-d", "--output-dir",
        help="Output directory (for batch export)"
    )
    
    # Format and quality
    parser.add_argument(
        "-f", "--format", default="png",
        choices=["png", "svg", "pdf"],
        help="Output format (default: png)"
    )
    parser.add_argument(
        "-t", "--theme", default="default",
        help="Mermaid theme (default, forest, dark, neutral)"
    )
    parser.add_argument(
        "-w", "--width", type=int,
        help="Image width in pixels"
    )
    parser.add_argument(
        "-H", "--height", type=int,
        help="Image height in pixels"
    )
    parser.add_argument(
        "-s", "--scale", type=float, default=1.0,
        help="Scale factor (default: 1.0)"
    )
    parser.add_argument(
        "-b", "--background", default="transparent",
        help="Background color (default: transparent)"
    )
    
    # Advanced
    parser.add_argument(
        "-c", "--css",
        help="Custom CSS file for styling"
    )
    parser.add_argument(
        "-C", "--config",
        help="Mermaid config file"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Quiet mode (suppress output)"
    )
    parser.add_argument(
        "--mermaid-cmd", default="mmdc",
        help="mermaid-cli command (default: mmdc, use 'npx mmdc' for local)"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    mermaid_cmd = check_dependencies()
    if not mermaid_cmd:
        print("Error: mermaid-cli not found.", file=sys.stderr)
        print("Install with: npm install -g @mermaid-js/mermaid-cli", file=sys.stderr)
        print("Or use: npx @mermaid-js/mermaid-cli", file=sys.stderr)
        return 1
    
    # Resolve input files
    input_files = []
    for input_pattern in args.input:
        path = Path(input_pattern)
        if path.is_dir():
            input_files.extend(path.glob("*.mmd"))
        elif path.exists():
            input_files.append(path)
        else:
            # Try glob pattern
            input_files.extend(Path.cwd().glob(input_pattern))
    
    if not input_files:
        print("Error: No input files found", file=sys.stderr)
        return 1
    
    # Validate single file mode
    if args.output and len(input_files) > 1:
        print("Error: --output can only be used with single file", file=sys.stderr)
        return 1
    
    # Prepare output path
    output_path = None
    if args.output:
        output_path = Path(args.output)
    
    output_dir = None
    if args.output_dir:
        output_dir = Path(args.output_dir)
    
    # Single file export
    if len(input_files) == 1 and output_path:
        success = export_single(
            input_files[0], output_path, args.format, args.theme,
            args.width, args.height, args.scale, args.background,
            args.css, args.config, args.quiet, args.mermaid_cmd
        )
        return 0 if success else 1
    
    # Batch export
    else:
        success = export_batch(
            input_files, output_dir, args.format, args.theme,
            args.width, args.height, args.scale, args.background,
            args.css, args.config, args.quiet, args.mermaid_cmd
        )
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())