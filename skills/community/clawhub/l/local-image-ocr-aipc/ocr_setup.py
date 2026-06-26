"""
OCR Setup — unified preflight, install, and download utility.

Usage:
  python ocr_setup.py                    # Auto: check + install/download only what's missing
  python ocr_setup.py --check            # Preflight only (workdir + llama + models)
  python ocr_setup.py --workdir          # Locate / create OCR working directory
  python ocr_setup.py --llama [--tag TX] # Download and install llama.cpp Vulkan binary
  python ocr_setup.py --disk             # Check available disk space
  python ocr_setup.py --download [hf|ms] # Download GLM-OCR models (hf=HuggingFace, ms=ModelScope)
  python ocr_setup.py --verify           # Verify downloaded model file sizes
  python ocr_setup.py --custom-dir PATH  # Use a specific OCR working directory
"""

import argparse
import os
import re
import shutil
import string
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ocr_cfg import OCR_DIR as _INITIAL_OCR_DIR

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_CFG_FILE = os.path.join(_THIS_DIR, ".ocr_dir")

# Minimum required llama.cpp build; update TAG when a newer release is available.
MIN_BUILD = 8400
LLAMA_TAG = "b8400"   # https://github.com/ggml-org/llama.cpp/releases/latest


# ─────────────────────────────────────────────────────────────────────────────
# Working directory
# ─────────────────────────────────────────────────────────────────────────────

def cmd_workdir(custom_ocr_dir: str = "") -> str:
    """Locate or create the OCR working directory. Returns the resolved path."""
    if custom_ocr_dir:
        parent = os.path.dirname(custom_ocr_dir.rstrip("\\/")) or custom_ocr_dir
        if os.path.exists(parent):
            ocr_dir = custom_ocr_dir
            os.makedirs(ocr_dir, exist_ok=True)
            print(f"OCR_DIR={ocr_dir} (user-specified)")
        else:
            print(f"[WARN] Custom path parent does not exist: {parent}. Falling back to auto-select.")
            custom_ocr_dir = ""

    if not custom_ocr_dir:
        best_drive, best_free = None, -1
        for d in string.ascii_uppercase:
            root = f"{d}:\\"
            if os.path.exists(root):
                try:
                    free = shutil.disk_usage(root).free
                    if free > best_free:
                        best_free, best_drive = free, d
                except Exception:
                    pass
        ocr_dir = os.path.join(f"{best_drive}:\\", "image-ocr")
        os.makedirs(ocr_dir, exist_ok=True)
        print(f"OCR_DIR={ocr_dir} (auto-selected drive: {best_drive})")

    os.environ["OCR_DIR"] = ocr_dir
    with open(_CFG_FILE, "w", encoding="utf-8") as f:
        f.write(ocr_dir)
    print(f"Config saved to: {_CFG_FILE}")
    return ocr_dir


def _get_ocr_dir(custom_ocr_dir: str = "") -> str:
    """Return OCR_DIR, running workdir setup if not yet resolved."""
    if custom_ocr_dir:
        return cmd_workdir(custom_ocr_dir)
    ocr_dir = _INITIAL_OCR_DIR
    if not ocr_dir:
        print("[INFO] OCR_DIR not set — running workdir setup...")
        ocr_dir = cmd_workdir()
    return ocr_dir


# ─────────────────────────────────────────────────────────────────────────────
# Preflight checks
# ─────────────────────────────────────────────────────────────────────────────

def check_llama(ocr_dir: str) -> tuple[str, int]:
    """Return (status, build) where status ∈ {'READY', 'OUTDATED', 'MISSING'}."""
    server_exe = os.path.join(ocr_dir, "llama.cpp", "llama-server.exe")
    if not os.path.exists(server_exe):
        print(f"ERROR: llama-server.exe not found")
        print(f"   Checked: {server_exe}")
        print("LLAMA_STATUS=MISSING")
        return "MISSING", 0

    result = subprocess.run([server_exe, "--version"], capture_output=True, text=True)
    output = result.stdout + result.stderr
    m = re.search(r"version:\s*(\d+)", output)
    if m:
        build = int(m.group(1))
        if build >= MIN_BUILD:
            print(f"OK: llama.cpp build {build} >= b{MIN_BUILD}, skip Step 1")
            print("LLAMA_STATUS=READY")
            return "READY", build
        else:
            print(f"WARN: llama.cpp build {build} < b{MIN_BUILD}, upgrade required")
            print("LLAMA_STATUS=OUTDATED")
            return "OUTDATED", build
    else:
        print("WARN: could not parse version output")
        print("LLAMA_STATUS=OUTDATED")
        return "OUTDATED", 0


def check_models(ocr_dir: str) -> str:
    """Return 'READY' or 'MISSING'."""
    model_dir   = os.path.join(ocr_dir, "models", "GLM-OCR-GGUF")
    model_file  = os.path.join(model_dir, "GLM-OCR-Q8_0.gguf")
    mmproj_file = os.path.join(model_dir, "mmproj-GLM-OCR-Q8_0.gguf")

    model_ok  = os.path.exists(model_file)
    mmproj_ok = os.path.exists(mmproj_file)

    if model_ok and mmproj_ok:
        print("OK: GLM-OCR model files ready, skip Step 2")
        print("MODEL_STATUS=READY")
        return "READY"
    else:
        if not model_ok:  print("ERROR: Missing GLM-OCR-Q8_0.gguf")
        if not mmproj_ok: print("ERROR: Missing mmproj-GLM-OCR-Q8_0.gguf")
        print("MODEL_STATUS=MISSING")
        print(f"   Checked: {model_dir}")
        return "MISSING"


def cmd_check(ocr_dir: str) -> tuple[str, str]:
    """Run full preflight and return (llama_status, model_status)."""
    print(f"\n[Preflight] OCR_DIR={ocr_dir}")
    llama_status, _ = check_llama(ocr_dir)
    model_status    = check_models(ocr_dir)
    return llama_status, model_status


# ─────────────────────────────────────────────────────────────────────────────
# Install llama.cpp
# ─────────────────────────────────────────────────────────────────────────────

def cmd_install_llama(ocr_dir: str, tag: str | None = None) -> None:
    """Download and extract the llama.cpp Vulkan prebuilt binary."""
    tag = tag or LLAMA_TAG
    llama_dir = os.path.join(ocr_dir, "llama.cpp")
    url = (
        f"https://github.com/ggml-org/llama.cpp/releases/download/{tag}"
        f"/llama-{tag}-bin-win-vulkan-x64.zip"
    )
    print(f"Downloading llama.cpp {tag} ...")
    zip_path = os.path.join(tempfile.gettempdir(), "llama-vulkan.zip")
    urllib.request.urlretrieve(url, zip_path)

    os.makedirs(llama_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(llama_dir)
    os.remove(zip_path)
    print("LLAMA_INSTALL=DONE")


# ─────────────────────────────────────────────────────────────────────────────
# Disk check
# ─────────────────────────────────────────────────────────────────────────────

def cmd_disk(ocr_dir: str) -> bool:
    """Print free disk space and return False if space is critically low."""
    free_gb = shutil.disk_usage(ocr_dir).free / 1024 ** 3
    print(f"DISK_FREE={round(free_gb, 1)}GB")
    if free_gb < 2:
        print("DISK_STATUS=LOW")
        print("[WARN] Less than 2 GB available — download may fail")
        return False
    print("DISK_STATUS=OK")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Download models
# ─────────────────────────────────────────────────────────────────────────────

def cmd_download(ocr_dir: str, source: str = "hf") -> None:
    """Download GLM-OCR model files. source ∈ {'hf', 'ms'}."""
    model_dir = os.path.join(ocr_dir, "models", "GLM-OCR-GGUF")
    os.makedirs(model_dir, exist_ok=True)
    files = ["GLM-OCR-Q8_0.gguf", "mmproj-GLM-OCR-Q8_0.gguf"]

    if source == "ms":
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "modelscope", "-q"], check=True
        )
        from modelscope.hub.file_download import model_file_download
        for fname in files:
            print(f"Downloading {fname} ...")
            model_file_download("ggml-org/GLM-OCR-GGUF", file_path=fname, local_dir=model_dir)
    else:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "huggingface_hub", "-q"], check=True
        )
        # Uncomment the next line to use the HF mirror (recommended in China):
        # os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        from huggingface_hub import hf_hub_download
        for fname in files:
            print(f"Downloading {fname} ...")
            hf_hub_download(
                repo_id="ggml-org/GLM-OCR-GGUF", filename=fname, local_dir=model_dir
            )

    print("MODEL_DOWNLOAD=DONE")


# ─────────────────────────────────────────────────────────────────────────────
# Verify models
# ─────────────────────────────────────────────────────────────────────────────

def cmd_verify(ocr_dir: str) -> bool:
    """Print model file sizes and return False if any file is missing."""
    model_dir = os.path.join(ocr_dir, "models", "GLM-OCR-GGUF")
    all_ok = True
    for fname in ["GLM-OCR-Q8_0.gguf", "mmproj-GLM-OCR-Q8_0.gguf"]:
        fpath = os.path.join(model_dir, fname)
        if os.path.exists(fpath):
            mb = round(os.path.getsize(fpath) / 1024 ** 2)
            print(f"{fname}: {mb} MB")
        else:
            print(f"MISSING: {fname}")
            all_ok = False
    return all_ok


# ─────────────────────────────────────────────────────────────────────────────
# Full auto setup
# ─────────────────────────────────────────────────────────────────────────────

def cmd_auto(download_source: str = "hf", custom_ocr_dir: str = "") -> None:
    """Check the environment and install / download only what's missing."""
    ocr_dir = _get_ocr_dir(custom_ocr_dir)
    if not ocr_dir:
        sys.exit(1)

    print(f"\n[Setup] OCR_DIR={ocr_dir}")

    llama_status, _ = check_llama(ocr_dir)
    if llama_status in ("MISSING", "OUTDATED"):
        print("\n[Step 1] Installing llama.cpp Vulkan...")
        cmd_install_llama(ocr_dir)

    model_status = check_models(ocr_dir)
    if model_status == "MISSING":
        print("\n[Step 2] Checking disk space...")
        if not cmd_disk(ocr_dir):
            print("[ERROR] Insufficient disk space. Free up space and retry.")
            sys.exit(1)
        print(f"\n[Step 2] Downloading models (source={download_source})...")
        cmd_download(ocr_dir, download_source)
        cmd_verify(ocr_dir)

    print(f"\n✅ Setup complete.")
    print(f"   OCR_DIR   : {ocr_dir}")
    print(f"   Run OCR   : python ocr_run.py <image_path>")
    print(f"\nINSTALL_DONE=1")
    print(f"OCR_DIR={ocr_dir}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="OCR environment setup — preflight, install, and download utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--workdir",     action="store_true", help="Locate / create OCR working directory")
    parser.add_argument("--check",       action="store_true", help="Preflight check only")
    parser.add_argument("--llama",       action="store_true", help="Install / update llama.cpp Vulkan binary")
    parser.add_argument("--disk",        action="store_true", help="Check available disk space")
    parser.add_argument("--download",    nargs="?", const="hf", metavar="SOURCE",
                        help="Download models: hf (HuggingFace, default) or ms (ModelScope)")
    parser.add_argument("--verify",      action="store_true", help="Verify downloaded model files")
    parser.add_argument("--tag",         default=None, metavar="TAG",
                        help=f"llama.cpp release tag to install (default: {LLAMA_TAG})")
    parser.add_argument("--custom-dir",  default="", metavar="PATH",
                        help="Custom OCR working directory path")
    args = parser.parse_args()

    if args.workdir:
        cmd_workdir(args.custom_dir)
    elif args.check:
        ocr_dir = _get_ocr_dir(args.custom_dir)
        if ocr_dir:
            cmd_check(ocr_dir)
    elif args.llama:
        ocr_dir = _get_ocr_dir(args.custom_dir)
        if ocr_dir:
            cmd_install_llama(ocr_dir, args.tag)
    elif args.disk:
        ocr_dir = _get_ocr_dir(args.custom_dir)
        if ocr_dir:
            cmd_disk(ocr_dir)
    elif args.download is not None:
        ocr_dir = _get_ocr_dir(args.custom_dir)
        if ocr_dir:
            cmd_download(ocr_dir, args.download)
    elif args.verify:
        ocr_dir = _get_ocr_dir(args.custom_dir)
        if ocr_dir:
            cmd_verify(ocr_dir)
    else:
        # No flags → full auto setup
        cmd_auto(download_source="hf", custom_ocr_dir=args.custom_dir)


if __name__ == "__main__":
    main()
