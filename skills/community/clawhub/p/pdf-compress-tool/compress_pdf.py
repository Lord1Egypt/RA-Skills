#!/usr/bin/env python3
"""PDF Compress Tool — supports target size and percentage compression modes

Three-stage compression pipeline: pikepdf structural optimization → Ghostscript progressive compression → QPDF secondary optimization
Supports quality floor protection and batch processing.
"""

import argparse
import platform
import re
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

# Ghostscript quality levels, tried from highest to lowest
GS_QUALITY_LEVELS = ["prepress", "printer", "ebook", "screen"]

# DPI values corresponding to each GS preset
PRESET_DPI = {"prepress": 300, "printer": 300, "ebook": 150, "screen": 72}

# Custom DPI levels for further compression beyond screen preset
CUSTOM_DPI_LEVELS = [100, 72, 50, 36]

# JPEG QFactor levels for refinement search (lower = higher quality)
# QFactor 0.05 ~ JPEG quality 95, 0.10 ~ 90, 0.15 ~ 85, 0.20 ~ 80, 0.30 ~ 70, 0.40 ~ 60
QFACTOR_LEVELS = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40]

# Quality floor mapping: limits the lowest GS preset allowed and whether custom DPI is permitted
QUALITY_LIMITS = {
    "high": {
        "max_gs_index": 1,       # lowest: printer (index 1)
        "allow_custom_dpi": False,
        "min_dpi": 150,          # refinement won't go below 150 dpi
        "label": "high (printer/300dpi)",
    },
    "medium": {
        "max_gs_index": 2,       # lowest: ebook (index 2)
        "allow_custom_dpi": False,
        "min_dpi": 72,           # refinement won't go below 72 dpi
        "label": "medium (ebook/150dpi)",
    },
    "low": {
        "max_gs_index": 3,       # all levels including screen (index 3)
        "allow_custom_dpi": True,
        "min_dpi": 36,           # allow very aggressive compression
        "label": "low (screen/72dpi and below)",
    },
}


def _install_hint(pkg: str) -> str:
    """Return a platform-specific install command for the given package."""
    s = platform.system()
    if s == "Darwin":
        return f"brew install {pkg}"
    elif s == "Linux":
        if shutil.which("apt-get"):
            return f"sudo apt-get install {pkg}"
        elif shutil.which("dnf"):
            return f"sudo dnf install {pkg}"
        elif shutil.which("yum"):
            return f"sudo yum install {pkg}"
        elif shutil.which("pacman"):
            return f"sudo pacman -S {pkg}"
        return f"sudo apt-get install {pkg}  (or use your distro's package manager)"
    elif s == "Windows":
        if shutil.which("choco"):
            return f"choco install {pkg}"
        elif shutil.which("winget"):
            return f"winget install {pkg}"
        # Ghostscript Windows download page
        if pkg == "ghostscript":
            return "Download from https://ghostscript.com/releases/gsdnld.html  (or: choco install ghostscript)"
        if pkg == "qpdf":
            return "Download from https://github.com/qpdf/qpdf/releases  (or: choco install qpdf)"
        return f"choco install {pkg}  (or download manually)"
    return f"Install {pkg} using your system package manager"


def parse_size(s: str) -> int:
    """Parse a size string into bytes. Supports MB and KB units.

    >>> parse_size("2MB")
    2097152
    >>> parse_size("500KB")
    512000
    """
    s = s.strip().upper()
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(MB|KB)$", s)
    if not m:
        raise argparse.ArgumentTypeError(
            f"Invalid size format '{s}', use formats like 2MB or 500KB"
        )
    value = float(m.group(1))
    unit = m.group(2)
    if value <= 0:
        raise argparse.ArgumentTypeError("Size must be greater than 0")
    if unit == "MB":
        return int(value * 1024 * 1024)
    else:  # KB
        return int(value * 1024)


def format_size(size_bytes: int) -> str:
    """Format byte count as a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def detect_tools() -> dict:
    """Detect available compression tools and print their status."""
    tools = {}

    # Ghostscript
    gs_cmd = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    tools["gs"] = gs_cmd
    if gs_cmd:
        try:
            result = subprocess.run(
                [gs_cmd, "--version"], capture_output=True, text=True, timeout=5
            )
            gs_ver = result.stdout.strip()
        except Exception:
            gs_ver = "unknown"
        print(f"  \u2713 ghostscript ({gs_ver})")
    else:
        print(f"  \u2717 ghostscript (not installed, recommended: {_install_hint('ghostscript')})")

    # QPDF
    qpdf_cmd = shutil.which("qpdf")
    tools["qpdf"] = qpdf_cmd
    if qpdf_cmd:
        try:
            result = subprocess.run(
                [qpdf_cmd, "--version"], capture_output=True, text=True, timeout=5
            )
            qpdf_ver = result.stdout.strip().split("\n")[0]
        except Exception:
            qpdf_ver = "unknown"
        print(f"  \u2713 qpdf ({qpdf_ver})")
    else:
        print(f"  \u2717 qpdf (not installed, optional: {_install_hint('qpdf')})")

    # pikepdf
    try:
        import pikepdf
        tools["pikepdf"] = True
        print(f"  \u2713 pikepdf ({pikepdf.__version__})")
    except ImportError:
        tools["pikepdf"] = False
        print("  \u2717 pikepdf (not installed, will be auto-installed)")

    return tools


def _ensure_pikepdf():
    """Ensure pikepdf is available, auto-installing if necessary."""
    try:
        import pikepdf
        return pikepdf
    except ImportError:
        print("  pikepdf not installed, attempting to install...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pikepdf"],
            check=True, capture_output=True,
        )
        import pikepdf
        return pikepdf


def compress_with_pikepdf(input_path: str, output_path: str) -> bool:
    """Compress PDF using pikepdf (remove redundant objects, compress streams)."""
    pikepdf = _ensure_pikepdf()
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.remove_unreferenced_resources()
            pdf.save(
                output_path,
                compress_streams=True,
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
                recompress_flate=True,
            )
        return True
    except Exception:
        return False


def compress_with_ghostscript(
    input_path: str, output_path: str, quality: str = None,
    dpi: int = None, qfactor: float = None
) -> bool:
    """Compress PDF using Ghostscript.

    When qfactor is set, uses custom JPEG quality control instead of a preset.
    qfactor: 0.05 (highest quality) to 0.40 (lowest quality).
    """
    gs_cmd = shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c")
    if not gs_cmd:
        return False

    args = [
        gs_cmd,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.5",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dDetectDuplicateImages=true",
        "-dColorImageDownsampleType=/Bicubic",
        "-dGrayImageDownsampleType=/Bicubic",
        "-dMonoImageDownsampleType=/Bicubic",
    ]

    if qfactor is not None:
        # Custom JPEG quality mode: bypass preset, set explicit quality
        args.extend([
            "-dAutoFilterColorImages=false",
            "-dAutoFilterGrayImages=false",
            "-dColorImageFilter=/DCTEncode",
            "-dGrayImageFilter=/DCTEncode",
        ])
        if dpi:
            args.extend([
                f"-dColorImageResolution={dpi}",
                f"-dGrayImageResolution={dpi}",
                f"-dMonoImageResolution={dpi}",
                "-dDownsampleColorImages=true",
                "-dDownsampleGrayImages=true",
                "-dDownsampleMonoImages=true",
            ])
        args.extend([
            f"-sOutputFile={output_path}",
            "-c",
            f"<< /ColorImageDict << /QFactor {qfactor} /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >> /GrayImageDict << /QFactor {qfactor} /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >> >> setdistillerparams",
            "-f",
            input_path,
        ])
    else:
        if quality:
            args.append(f"-dPDFSETTINGS=/{quality}")

        if dpi:
            args.extend([
                f"-dColorImageResolution={dpi}",
                f"-dGrayImageResolution={dpi}",
                f"-dMonoImageResolution={dpi}",
                "-dDownsampleColorImages=true",
                "-dDownsampleGrayImages=true",
                "-dDownsampleMonoImages=true",
            ])

        args.extend([f"-sOutputFile={output_path}", input_path])

    try:
        subprocess.run(args, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def compress_with_qpdf(input_path: str, output_path: str) -> bool:
    """Perform secondary structural optimization using QPDF (object streams, stream recompression)."""
    qpdf_cmd = shutil.which("qpdf")
    if not qpdf_cmd:
        return False

    try:
        subprocess.run(
            [
                qpdf_cmd,
                "--optimize-images",
                "--object-streams=generate",
                "--compress-streams=y",
                "--recompress-flate",
                "--compression-level=9",
                input_path,
                output_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def _find_optimal_compression(input_path: str, tmp_dir: str, target_bytes: int,
                               dpi_high: int, dpi_low: int, min_dpi: int) -> tuple:
    """Binary search on DPI with progressive JPEG quality to find the highest-quality
    result that still meets the target size.

    Searches between dpi_high (better quality, larger) and dpi_low (worse quality, smaller),
    constrained by min_dpi (quality floor).

    Returns (best_path, best_size, strategy_label) or (None, 0, "") if no improvement found.
    """
    dpi_low = max(dpi_low, min_dpi)
    if dpi_high <= dpi_low:
        return None, 0, ""

    best_path = None
    best_size = 0
    best_label = ""
    iteration = 0

    print(f"\n      Refining: searching DPI {dpi_high}-{dpi_low} for optimal quality...")

    lo, hi = dpi_low, dpi_high
    while hi - lo > 5:  # 5 dpi precision is sufficient
        mid = (lo + hi) // 2
        iteration += 1

        # Try this DPI with the highest JPEG quality first
        found = False
        for qf in QFACTOR_LEVELS:
            tag = f"refine_{iteration}_dpi{mid}_qf{qf}"
            out = str(Path(tmp_dir) / f"{tag}.pdf")
            if compress_with_ghostscript(input_path, out, dpi=mid, qfactor=qf):
                size = Path(out).stat().st_size
                if size <= target_bytes:
                    # This combination meets target — record it and try higher DPI
                    if best_path is None or mid > _extract_dpi(best_label) or (
                        mid == _extract_dpi(best_label) and qf < _extract_qf(best_label)
                    ):
                        best_path = out
                        best_size = size
                        best_label = f"{mid}dpi/qf{qf}"
                    found = True
                    break  # No need to try worse JPEG quality at this DPI

        if found:
            lo = mid + 1  # Try higher DPI (better quality)
        else:
            hi = mid - 1  # Need lower DPI (smaller file)

    # Also try the exact boundaries if not already tried
    for boundary_dpi in [hi, lo]:
        if boundary_dpi < min_dpi:
            continue
        for qf in QFACTOR_LEVELS:
            tag = f"refine_boundary_dpi{boundary_dpi}_qf{qf}"
            out = str(Path(tmp_dir) / f"{tag}.pdf")
            if compress_with_ghostscript(input_path, out, dpi=boundary_dpi, qfactor=qf):
                size = Path(out).stat().st_size
                if size <= target_bytes:
                    if best_path is None or boundary_dpi > _extract_dpi(best_label) or (
                        boundary_dpi == _extract_dpi(best_label) and qf < _extract_qf(best_label)
                    ):
                        best_path = out
                        best_size = size
                        best_label = f"{boundary_dpi}dpi/qf{qf}"
                    break

    if best_path:
        print(f"      Optimal: {best_label} -> {format_size(best_size)}")
    else:
        print(f"      No improvement found in refinement range")

    return best_path, best_size, best_label


def _extract_dpi(label: str) -> int:
    """Extract DPI value from a refinement label like '95dpi/qf0.05'."""
    m = re.match(r"(\d+)dpi", label)
    return int(m.group(1)) if m else 0


def _extract_qf(label: str) -> float:
    """Extract QFactor value from a refinement label like '95dpi/qf0.05'."""
    m = re.search(r"qf([\d.]+)", label)
    return float(m.group(1)) if m else 1.0


def compress_pdf(input_path: str, output_path: str, target_bytes: int,
                 quality: str = "medium") -> dict:
    """Compress a PDF file to below the target size.

    Returns a structured result:
      {"status": "success"|"skipped"|"warning",
       "original_size": int, "compressed_size": int,
       "output_path": str, "strategy": str, "message": str}
    """
    input_file = Path(input_path)
    original_size = input_file.stat().st_size
    q_limit = QUALITY_LIMITS[quality]

    result = {
        "status": "success",
        "original_size": original_size,
        "compressed_size": original_size,
        "output_path": output_path,
        "strategy": "",
        "message": "",
    }

    print(f"Original: {input_file.name} ({format_size(original_size)})")
    print(f"Target:   \u2264 {format_size(target_bytes)}")
    print(f"Quality floor: {q_limit['label']}")

    if original_size <= target_bytes:
        print("\nFile is already below target size, no compression needed. Copied to output path.")
        shutil.copy2(input_path, output_path)
        result["status"] = "skipped"
        result["message"] = "Already within target, no compression needed"
        return result

    use_gs = bool(shutil.which("gs") or shutil.which("gswin64c") or shutil.which("gswin32c"))
    use_qpdf = bool(shutil.which("qpdf"))

    if not use_gs:
        print("\nNote: Ghostscript not installed, using pikepdf only (limited compression)")
        print(f"  Install: {_install_hint('ghostscript')}")

    best_path = None
    best_size = original_size
    strategy_used = ""

    with tempfile.TemporaryDirectory() as tmp_dir:
        current_input = input_path

        # === Stage 1: pikepdf structural optimization ===
        pikepdf_out = str(Path(tmp_dir) / "pikepdf.pdf")
        print(f"\n[1/3] pikepdf structural optimization...", end="  ")
        if compress_with_pikepdf(current_input, pikepdf_out):
            size = Path(pikepdf_out).stat().st_size
            print(f"{format_size(size)}")
            if size < best_size:
                best_size = size
                best_path = pikepdf_out
                current_input = pikepdf_out
                strategy_used = "pikepdf"
            if best_size <= target_bytes:
                print(f"  \u2713 Target met")
                # Still run QPDF secondary optimization
                if use_qpdf:
                    qpdf_out = str(Path(tmp_dir) / "qpdf_final.pdf")
                    print(f"\n[3/3] QPDF secondary optimization...", end="  ")
                    if compress_with_qpdf(best_path, qpdf_out):
                        qsize = Path(qpdf_out).stat().st_size
                        print(f"{format_size(qsize)}")
                        if qsize < best_size:
                            best_size = qsize
                            best_path = qpdf_out
                    else:
                        print("skipped")
                shutil.copy2(best_path, output_path)
                result["compressed_size"] = best_size
                result["strategy"] = strategy_used
                _print_result(original_size, best_size, output_path, strategy_used)
                return result
        else:
            print("skipped")

        # === Stage 2: Ghostscript progressive compression ===
        if use_gs:
            # 2a: GS preset quality levels — collect all results for refinement
            allowed_levels = GS_QUALITY_LEVELS[: q_limit["max_gs_index"] + 1]
            print(f"\n[2/3] Ghostscript progressive compression...")
            preset_results = {}  # {preset_name: size}
            first_met_preset = None  # first preset that meets target
            last_not_met_preset = None  # last preset that did NOT meet target
            for quality_level in allowed_levels:
                gs_out = str(Path(tmp_dir) / f"gs_{quality_level}.pdf")
                print(f"      Trying {quality_level}...", end=" ")
                if compress_with_ghostscript(current_input, gs_out, quality=quality_level):
                    size = Path(gs_out).stat().st_size
                    print(f"{format_size(size)}")
                    preset_results[quality_level] = size
                    if size < best_size:
                        best_size = size
                        best_path = gs_out
                        strategy_used = quality_level
                    if size <= target_bytes and first_met_preset is None:
                        first_met_preset = quality_level
                        print(f"      \u2713 Target met")
                        break
                    else:
                        last_not_met_preset = quality_level
                else:
                    print("failed")

            # 2b: Refinement — if a preset met target but over-compressed,
            # binary search between the last failing preset and the first
            # passing preset to find the highest-quality result
            if first_met_preset and last_not_met_preset and best_size <= target_bytes:
                over_compression_ratio = best_size / target_bytes
                # Only refine if over-compressed by >20% (result < 80% of target)
                if over_compression_ratio < 0.80:
                    dpi_high = PRESET_DPI[last_not_met_preset]
                    dpi_low = PRESET_DPI[first_met_preset]
                    ref_path, ref_size, ref_label = _find_optimal_compression(
                        current_input, tmp_dir, target_bytes,
                        dpi_high, dpi_low, q_limit["min_dpi"]
                    )
                    if ref_path and ref_size <= target_bytes:
                        # Prefer the refinement result if it's larger (= higher quality)
                        # but still under target
                        if ref_size > best_size or (ref_size == best_size):
                            best_size = ref_size
                            best_path = ref_path
                            strategy_used = ref_label

            # 2b-extra: If target not met but within reach, try refinement
            # within the allowed DPI range (e.g., ebook at 150dpi with custom JPEG quality)
            if best_size > target_bytes and not first_met_preset:
                # Try refining with custom JPEG quality at the lowest allowed preset's DPI
                lowest_preset = allowed_levels[-1]
                lowest_dpi = PRESET_DPI[lowest_preset]
                # Search from lowest_dpi down to min_dpi with custom JPEG quality
                if lowest_dpi > q_limit["min_dpi"]:
                    ref_path, ref_size, ref_label = _find_optimal_compression(
                        current_input, tmp_dir, target_bytes,
                        lowest_dpi, q_limit["min_dpi"], q_limit["min_dpi"]
                    )
                    if ref_path and ref_size <= target_bytes:
                        best_size = ref_size
                        best_path = ref_path
                        strategy_used = ref_label
                else:
                    # Try just JPEG quality adjustment at current DPI
                    for qf in QFACTOR_LEVELS:
                        qf_out = str(Path(tmp_dir) / f"gs_qf{qf}_dpi{lowest_dpi}.pdf")
                        if compress_with_ghostscript(current_input, qf_out, dpi=lowest_dpi, qfactor=qf):
                            size = Path(qf_out).stat().st_size
                            if size <= target_bytes:
                                if size > best_size or best_size > target_bytes:
                                    best_size = size
                                    best_path = qf_out
                                    strategy_used = f"{lowest_dpi}dpi/qf{qf}"
                                    print(f"      Refined: {strategy_used} -> {format_size(size)}")
                                break

            # 2c: Custom DPI (only allowed with low quality setting)
            if best_size > target_bytes and q_limit["allow_custom_dpi"]:
                print(f"\n[2/3] Further reducing image resolution...")
                for dpi in CUSTOM_DPI_LEVELS:
                    dpi_out = str(Path(tmp_dir) / f"gs_dpi{dpi}.pdf")
                    print(f"      Trying {dpi} dpi...", end=" ")
                    if compress_with_ghostscript(
                        current_input, dpi_out, quality="screen", dpi=dpi
                    ):
                        size = Path(dpi_out).stat().st_size
                        print(f"{format_size(size)}")
                        if size < best_size:
                            best_size = size
                            best_path = dpi_out
                            strategy_used = f"screen/{dpi}dpi"
                        if best_size <= target_bytes:
                            print(f"      \u2713 Target met")
                            break
                    else:
                        print("failed")

            # Quality floor warning
            if best_size > target_bytes and not q_limit["allow_custom_dpi"]:
                print(f"\n      \u2190 Quality floor reached ({q_limit['label']})")

        # === Stage 3: QPDF secondary optimization ===
        if use_qpdf and best_path:
            qpdf_out = str(Path(tmp_dir) / "qpdf_final.pdf")
            print(f"\n[3/3] QPDF secondary optimization...", end="  ")
            if compress_with_qpdf(best_path, qpdf_out):
                qsize = Path(qpdf_out).stat().st_size
                print(f"{format_size(qsize)}")
                if qsize < best_size:
                    best_size = qsize
                    best_path = qpdf_out
            else:
                print("skipped")

        # === Output result ===
        if best_path:
            shutil.copy2(best_path, output_path)
            result["compressed_size"] = best_size
            result["strategy"] = strategy_used
            _print_result(original_size, best_size, output_path, strategy_used)

            if best_size > target_bytes:
                result["status"] = "warning"
                msg = (
                    f"\n\u26a0 Target not met: {format_size(target_bytes)}"
                    f" (current: {format_size(best_size)})"
                )
                if quality != "low":
                    msg += (
                        f"\n  Quality floor reached: {q_limit['label']}"
                        f"\n  Use --quality low for stronger compression, but image quality will degrade noticeably"
                    )
                print(msg)
                result["message"] = msg
        else:
            print("\nCompression failed. Please check that dependencies are installed.")
            result["status"] = "warning"
            result["message"] = "Compression failed"

    return result


def _print_result(original_size: int, compressed_size: int, output_path: str,
                  strategy: str = ""):
    """Print compression result summary."""
    ratio = (1 - compressed_size / original_size) * 100
    print(f"\nDone: {Path(output_path).name}")
    print(f"  {format_size(original_size)} -> {format_size(compressed_size)} (reduced {ratio:.1f}%)")
    if strategy:
        print(f"  Strategy: {strategy}")


def compress_batch(directory: str, target_bytes: int, quality: str = "medium",
                   output_dir: str = None):
    """Batch compress all PDF files in a directory."""
    dir_path = Path(directory)
    pdf_files = sorted(dir_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory}.")
        return

    if output_dir is None:
        output_dir_path = dir_path.parent / (dir_path.name + "_compressed")
    else:
        output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    total = len(pdf_files)
    print(f"Batch compress: {directory} ({total} PDFs)")
    print(f"Target: \u2264 {format_size(target_bytes)}")
    print(f"Output: {output_dir_path}")
    print(f"{'=' * 60}")

    results = []
    total_original = 0
    total_compressed = 0

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n--- [{i}/{total}] {pdf_file.name} ---")
        out_path = str(output_dir_path / pdf_file.name)
        r = compress_pdf(str(pdf_file), out_path, target_bytes, quality)
        results.append(r)
        total_original += r["original_size"]
        total_compressed += r["compressed_size"]

    # Summary report
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    warnings = sum(1 for r in results if r["status"] == "warning")

    print(f"\n{'=' * 60}")
    print(f"Summary:")
    print(f"  Success: {success}/{total}  Skipped: {skipped}/{total}  Warnings: {warnings}/{total}")
    if total_original > 0:
        total_ratio = (1 - total_compressed / total_original) * 100
        print(
            f"  Total: {format_size(total_original)} -> {format_size(total_compressed)}"
            f" (reduced {total_ratio:.1f}%)"
        )


def main():
    parser = argparse.ArgumentParser(
        description="PDF Compress Tool — supports target size and percentage compression modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  %(prog)s report.pdf --target-size 2MB
  %(prog)s report.pdf --reduce 30
  %(prog)s report.pdf --reduce 50 --quality low -o small.pdf
  %(prog)s --batch ./papers --target-size 2MB
  %(prog)s --batch ./papers --reduce 40 --quality high
""",
    )

    parser.add_argument(
        "input", nargs="?", help="Input PDF file path (can be omitted in batch mode)"
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "--target-size", type=parse_size, metavar="SIZE",
        help="Target size mode (e.g. 2MB, 500KB)",
    )
    mode_group.add_argument(
        "--reduce", type=int, metavar="PERCENT",
        help="Percentage compression mode (1-99, percentage to reduce)",
    )

    parser.add_argument(
        "-o", "--output", metavar="PATH",
        help="Output path (default: <filename>_compressed.pdf)",
    )
    parser.add_argument(
        "--quality", choices=["high", "medium", "low"], default="medium",
        help="Quality floor: high / medium / low (default: medium)",
    )
    parser.add_argument(
        "--batch", metavar="DIR",
        help="Batch compress all PDFs in a directory",
    )

    args = parser.parse_args()

    # Argument validation
    if args.reduce is not None:
        if not 1 <= args.reduce <= 99:
            parser.error("--reduce value must be between 1 and 99")

    if args.batch:
        batch_dir = Path(args.batch)
        if not batch_dir.is_dir():
            parser.error(f"Directory not found: {args.batch}")

        # Batch mode
        print("Detecting dependencies:")
        detect_tools()
        print()

        if args.target_size:
            target = args.target_size
        else:
            # Percentage mode in batch: each file calculates its own target
            target = None

        if target is not None:
            compress_batch(args.batch, target, args.quality)
        else:
            # Percentage mode batch: calculate target per file
            _compress_batch_reduce(args.batch, args.reduce, args.quality)
        return

    # Single file mode
    if not args.input:
        parser.error("Please provide an input PDF file path, or use --batch for batch processing")

    input_file = Path(args.input)
    if not input_file.exists():
        parser.error(f"File not found: {args.input}")
    if input_file.suffix.lower() != ".pdf":
        parser.error("Please provide a PDF file")

    print("Detecting dependencies:")
    detect_tools()
    print()

    original_size = input_file.stat().st_size

    # Calculate target bytes
    if args.target_size:
        target_bytes = args.target_size
    else:
        target_bytes = int(original_size * (1 - args.reduce / 100))
        print(f"Percentage mode: reduce by {args.reduce}% (target \u2264 {format_size(target_bytes)})")
        print()

    # Output path
    if args.output:
        output_path = args.output
    else:
        output_path = str(input_file.with_name(input_file.stem + "_compressed" + input_file.suffix))

    compress_pdf(str(input_file), output_path, target_bytes, args.quality)


def _compress_batch_reduce(directory: str, reduce_percent: int, quality: str):
    """Batch compress in percentage mode: calculate target size per file."""
    dir_path = Path(directory)
    pdf_files = sorted(dir_path.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {directory}.")
        return

    output_dir_path = dir_path.parent / (dir_path.name + "_compressed")
    output_dir_path.mkdir(parents=True, exist_ok=True)

    total = len(pdf_files)
    print(f"Batch compress: {directory} ({total} PDFs)")
    print(f"Mode: reduce by {reduce_percent}%")
    print(f"Output: {output_dir_path}")
    print(f"{'=' * 60}")

    results = []
    total_original = 0
    total_compressed = 0

    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n--- [{i}/{total}] {pdf_file.name} ---")
        original_size = pdf_file.stat().st_size
        target_bytes = int(original_size * (1 - reduce_percent / 100))
        out_path = str(output_dir_path / pdf_file.name)
        r = compress_pdf(str(pdf_file), out_path, target_bytes, quality)
        results.append(r)
        total_original += r["original_size"]
        total_compressed += r["compressed_size"]

    # Summary report
    success = sum(1 for r in results if r["status"] == "success")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    warnings = sum(1 for r in results if r["status"] == "warning")

    print(f"\n{'=' * 60}")
    print(f"Summary:")
    print(f"  Success: {success}/{total}  Skipped: {skipped}/{total}  Warnings: {warnings}/{total}")
    if total_original > 0:
        total_ratio = (1 - total_compressed / total_original) * 100
        print(
            f"  Total: {format_size(total_original)} -> {format_size(total_compressed)}"
            f" (reduced {total_ratio:.1f}%)"
        )


if __name__ == "__main__":
    main()
