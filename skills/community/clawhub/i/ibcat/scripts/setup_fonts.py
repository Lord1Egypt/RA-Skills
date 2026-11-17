#!/usr/bin/env python3
"""
Font setup and patching script for BabelDOC.
Patches BabelDOC's font loading to use local Noto CJK fonts
without hash verification, enabling offline/restricted-network operation.

Usage:
  python3 setup_fonts.py           # Apply patches
  python3 setup_fonts.py --check   # Check patch status
"""

import os
import re
import shutil
import sys
from pathlib import Path

# BabelDOC font cache directory
CACHE_DIR = Path(os.path.expanduser("~/.cache/babeldoc/fonts"))

# System Noto CJK font directories (try multiple locations)
NOTO_CJK_DIRS = [
    Path("/usr/share/fonts/opentype/noto-cjk-otf"),
    Path("/usr/share/fonts/opentype/noto-cjk"),
    Path("/usr/share/fonts/truetype/noto"),
]

# BabelDOC source file to patch
ASSETS_FILE = Path(sys.prefix) / "lib" / "python3" / "site-packages" / "babeldoc" / "assets" / "assets.py"
# Fallback: dist-packages
if not ASSETS_FILE.exists():
    for p in sys.path:
        candidate = Path(p) / "babeldoc" / "assets" / "assets.py"
        if candidate.exists():
            ASSETS_FILE = candidate
            break

# Mapping: BabelDOC expected font name -> system Noto CJK font filename
FONT_MAPPING = {
    # Simplified Chinese (SC)
    "SourceHanSansCN-Regular.ttf": "NotoSansCJKsc-Regular.otf",
    "SourceHanSansCN-Bold.ttf": "NotoSansCJKsc-Bold.otf",
    "SourceHanSerifCN-Regular.ttf": "NotoSerifCJKsc-Regular.otf",
    "SourceHanSerifCN-Bold.ttf": "NotoSerifCJKsc-Bold.otf",
    # Traditional Chinese (TC)
    "SourceHanSansTW-Regular.ttf": "NotoSansCJKtc-Regular.otf",
    "SourceHanSansTW-Bold.ttf": "NotoSansCJKtc-Bold.otf",
    "SourceHanSerifTW-Regular.ttf": "NotoSerifCJKtc-Regular.otf",
    "SourceHanSerifTW-Bold.ttf": "NotoSerifCJKtc-Bold.otf",
    # Hong Kong (HK)
    "SourceHanSansHK-Regular.ttf": "NotoSansCJKhk-Regular.otf",
    "SourceHanSansHK-Bold.ttf": "NotoSansCJKhk-Bold.otf",
    "SourceHanSerifHK-Regular.ttf": "NotoSerifCJKhk-Regular.otf",
    "SourceHanSerifHK-Bold.ttf": "NotoSerifCJKhk-Bold.otf",
    # Korean (KR)
    "SourceHanSansKR-Regular.ttf": "NotoSansCJKkr-Regular.otf",
    "SourceHanSansKR-Bold.ttf": "NotoSansCJKkr-Bold.otf",
    "SourceHanSerifKR-Regular.ttf": "NotoSerifCJKkr-Regular.otf",
    "SourceHanSerifKR-Bold.ttf": "NotoSerifCJKkr-Bold.otf",
    # Japanese (JP)
    "SourceHanSansJP-Regular.ttf": "NotoSansCJKjp-Regular.otf",
    "SourceHanSansJP-Bold.ttf": "NotoSansCJKjp-Bold.otf",
    "SourceHanSerifJP-Regular.ttf": "NotoSerifCJKjp-Regular.otf",
    "SourceHanSerifJP-Bold.ttf": "NotoSerifCJKjp-Bold.otf",
    # Latin fonts (fallback to CJK SC which includes Latin)
    "NotoSans-Regular.ttf": "NotoSansCJKsc-Regular.otf",
    "NotoSans-Bold.ttf": "NotoSansCJKsc-Bold.otf",
    "NotoSerif-Regular.ttf": "NotoSerifCJKsc-Regular.otf",
    "NotoSerif-Bold.ttf": "NotoSerifCJKsc-Bold.otf",
    "NotoSans-Italic.ttf": "NotoSansCJKsc-Regular.otf",
    "NotoSans-BoldItalic.ttf": "NotoSansCJKsc-Bold.otf",
    "NotoSerif-Italic.ttf": "NotoSerifCJKsc-Regular.otf",
    "NotoSerif-BoldItalic.ttf": "NotoSerifCJKsc-Bold.otf",
    # Script/handwriting fonts (fallback to CJK)
    "LXGWWenKaiGB-Regular.1.520.ttf": "NotoSansCJKsc-Regular.otf",
    "LXGWWenKaiTC-Regular.1.520.ttf": "NotoSansCJKtc-Regular.otf",
    "MaruBuri-Regular.ttf": "NotoSerifCJKjp-Regular.otf",
    "KleeOne-Regular.ttf": "NotoSansCJKjp-Regular.otf",
    "GoNotoKurrent-Regular.ttf": "NotoSansCJKsc-Regular.otf",
    "GoNotoKurrent-Bold.ttf": "NotoSansCJKsc-Bold.otf",
}


def find_noto_dir():
    """Find the directory containing Noto CJK fonts."""
    for d in NOTO_CJK_DIRS:
        if d.exists() and any(d.glob("NotoSansCJK*.otf")):
            return d
    return None


def setup_fonts():
    """Create symlinks from system fonts to BabelDOC cache directory."""
    noto_dir = find_noto_dir()
    if not noto_dir:
        print("ERROR: Noto CJK fonts not found in standard locations.")
        print("Install with: apt-get install fonts-noto-cjk")
        return False

    print(f"Source fonts: {noto_dir}")
    print(f"Cache dir: {CACHE_DIR}")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    linked = 0
    skipped = 0
    missing = 0
    for expected_name, system_name in FONT_MAPPING.items():
        cache_path = CACHE_DIR / expected_name
        if cache_path.exists():
            skipped += 1
            continue
        system_path = noto_dir / system_name
        if system_path.exists():
            try:
                os.symlink(system_path, cache_path)
                linked += 1
            except OSError:
                shutil.copy2(system_path, cache_path)
                linked += 1
        else:
            missing += 1

    print(f"Fonts: {linked} linked, {skipped} already exist, {missing} source missing")
    return True


def patch_source():
    """Patch BabelDOC source to skip font hash verification."""
    if not ASSETS_FILE.exists():
        print(f"ERROR: BabelDOC assets.py not found at {ASSETS_FILE}")
        return False

    with open(ASSETS_FILE, 'r') as f:
        content = f.read()

    # Check if already patched
    if "LOCAL PATCH" in content:
        print("Source already patched.")
        return True

    patches_applied = 0

    # Patch 1: get_font_and_metadata_async - skip hash verification
    old_font = '''    cache_file_path = get_cache_file_path(font_file_name, "fonts")
    if font_file_name in EMBEDDING_FONT_METADATA and verify_file(
        cache_file_path, EMBEDDING_FONT_METADATA[font_file_name]["sha3_256"]
    ):
        return cache_file_path, EMBEDDING_FONT_METADATA[font_file_name]

    logger.info(f"Font {cache_file_path} not found or corrupted, downloading...")'''

    new_font = '''    cache_file_path = get_cache_file_path(font_file_name, "fonts")
    # LOCAL PATCH: Use local fonts without hash verification
    if cache_file_path.exists():
        if font_file_name in EMBEDDING_FONT_METADATA:
            return cache_file_path, EMBEDDING_FONT_METADATA[font_file_name]
        return cache_file_path, {"ascent": 1160, "descent": -288, "encoding_length": 2}
    # END LOCAL PATCH

    logger.info(f"Font {cache_file_path} not found or corrupted, downloading...")'''

    if old_font in content:
        content = content.replace(old_font, new_font, 1)
        patches_applied += 1
        print("  [OK] Font hash verification patched")
    else:
        print("  [SKIP] Font hash patch target not found (may already be patched differently)")

    # Patch 2: get_cmap_file_path_async - skip hash verification
    old_cmap = '''    cache_file_path = get_cache_file_path(file_name, "cmap")
    if verify_file(cache_file_path, meta["sha3_256"]):
        return cache_file_path

    logger.info(f"CMap {cache_file_path} not found or corrupted, downloading...")'''

    new_cmap = '''    cache_file_path = get_cache_file_path(file_name, "cmap")
    # LOCAL PATCH: Use local cmap files without hash verification
    if cache_file_path.exists():
        return cache_file_path
    # END LOCAL PATCH

    logger.info(f"CMap {cache_file_path} not found or corrupted, downloading...")'''

    if old_cmap in content:
        content = content.replace(old_cmap, new_cmap, 1)
        patches_applied += 1
        print("  [OK] CMap hash verification patched")
    else:
        print("  [SKIP] CMap hash patch target not found")

    # Patch 3: get_fastest_upstream_for_font - avoid network calls
    pattern = re.compile(
        r'async def get_fastest_upstream_for_font\([^)]*\):.*?(?=\nasync def |\ndef |\nclass )',
        re.DOTALL
    )
    replacement = 'async def get_fastest_upstream_for_font(client=None, exclude_upstream=None):\n    """Patched: return local upstream without network."""\n    return "github", {}\n\n\n'
    if pattern.search(content):
        content = pattern.sub(replacement, content, count=1)
        patches_applied += 1
        print("  [OK] Fastest upstream function patched")
    else:
        print("  [SKIP] Fastest upstream patch target not found")

    if patches_applied > 0:
        with open(ASSETS_FILE, 'w') as f:
            f.write(content)
        print(f"Applied {patches_applied} patches to {ASSETS_FILE}")
    else:
        print("No patches were applied (all targets not found)")

    return patches_applied > 0


def check_patch():
    """Check if patches are applied."""
    if not ASSETS_FILE.exists():
        print(f"BabelDOC assets.py not found at {ASSETS_FILE}")
        return

    with open(ASSETS_FILE, 'r') as f:
        content = f.read()

    if "LOCAL PATCH" in content:
        print("PATCHED: YES")
    else:
        print("PATCHED: NO")

    # Check font symlinks
    existing = sum(1 for f in FONT_MAPPING if (CACHE_DIR / f).exists())
    print(f"Font symlinks: {existing}/{len(FONT_MAPPING)}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        check_patch()
    else:
        print("=== Setting up local fonts ===")
        setup_fonts()
        print("\n=== Patching BabelDOC source ===")
        patch_source()
        print("\n=== Verifying ===")
        check_patch()
        print("\nDone! BabelDOC is ready for offline CJK font usage.")
