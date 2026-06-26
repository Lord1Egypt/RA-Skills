#!/usr/bin/env python3
"""Download MiniCPM-o 4.5 from the fastest available source, with model verification.

Auto mode uses huggingface_hub and modelscope SDKs to download a single
small file (config.json) from each source, then picks whichever is fastest
for the full model download.

Usage:
    python download_model.py [--local-dir /path/to/save] [--source auto|huggingface|modelscope]
    python download_model.py --verify /path/to/model
    python download_model.py --verify openbmb/MiniCPM-o-4_5

The script can also be imported:
    from download_model import detect_best_source, download_model, verify_model
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from typing import Optional

MODEL_HF_ID = "openbmb/MiniCPM-o-4_5"
MODEL_MS_ID = "OpenBMB/MiniCPM-o-4_5"
DEFAULT_LOCAL_DIR = "./model/MiniCPM-o-4_5"
PROBE_FILE = "config.json"

EXPECTED_MODEL_TYPE = "minicpmo"
EXPECTED_ARCHITECTURE = "MiniCPMO"
EXPECTED_VERSION = "4.5"


def _ensure_package(package: str, pip_name: Optional[str] = None):
    """Import a package, installing it via pip if missing."""
    try:
        __import__(package)
    except ImportError:
        install_name = pip_name or package
        print(f"[*] Installing {install_name}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-U", install_name],
            stdout=subprocess.DEVNULL,
        )


# ============ Model Verification ============


def _load_config_from_local(model_path: str) -> Optional[dict]:
    """Load config.json from a local directory."""
    config_path = os.path.join(model_path, PROBE_FILE)
    if not os.path.isfile(config_path):
        return None
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_config_from_hub(model_id: str) -> Optional[dict]:
    """Download config.json from HuggingFace Hub and return as dict."""
    _ensure_package("huggingface_hub")
    from huggingface_hub import hf_hub_download  # type: ignore

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = hf_hub_download(
                repo_id=model_id,
                filename=PROBE_FILE,
                local_dir=tmpdir,
                force_download=True,
            )
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return None


def _resolve_config(model_path: str) -> Optional[dict]:
    """Load config.json from local path or HuggingFace Hub ID."""
    if os.path.isdir(model_path):
        return _load_config_from_local(model_path)
    if "/" in model_path and not os.path.exists(model_path):
        return _load_config_from_hub(model_path)
    return None


def verify_model(model_path: str) -> bool:
    """Verify that a model path points to a valid MiniCPM-o 4.5 model.

    Checks config.json for model_type, architectures, and version.
    Supports both local directories and HuggingFace Hub IDs.

    Returns True if valid, False otherwise.
    """
    print(f"[*] Verifying model: {model_path}")

    config = _resolve_config(model_path)
    if config is None:
        print(f"[FAIL] Cannot load {PROBE_FILE} from: {model_path}")
        if os.path.isdir(model_path):
            print(f"       {PROBE_FILE} not found in directory")
        else:
            print(f"       Path is not a local directory nor a valid Hub ID")
        return False

    errors = []

    model_type = config.get("model_type")
    if model_type != EXPECTED_MODEL_TYPE:
        errors.append(
            f"model_type: expected '{EXPECTED_MODEL_TYPE}', got '{model_type}'"
        )

    architectures = config.get("architectures", [])
    if EXPECTED_ARCHITECTURE not in architectures:
        errors.append(
            f"architectures: expected '{EXPECTED_ARCHITECTURE}' in {architectures}"
        )

    version = config.get("version")
    if version != EXPECTED_VERSION:
        errors.append(
            f"version: expected '{EXPECTED_VERSION}', got '{version}'"
        )

    if errors:
        print(f"[FAIL] Model verification failed:")
        for err in errors:
            print(f"       - {err}")
        return False

    print(f"[OK] Valid MiniCPM-o {EXPECTED_VERSION} model")
    print(f"     model_type:    {model_type}")
    print(f"     architectures: {architectures}")
    print(f"     version:       {version}")
    print(f"     torch_dtype:   {config.get('torch_dtype', 'N/A')}")
    return True


# ============ Source Benchmarking ============


def _probe_hf() -> Optional[float]:
    """Download config.json via huggingface_hub SDK. Returns elapsed seconds or None."""
    _ensure_package("huggingface_hub")
    from huggingface_hub import hf_hub_download  # type: ignore

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            start = time.monotonic()
            hf_hub_download(
                repo_id=MODEL_HF_ID,
                filename=PROBE_FILE,
                local_dir=tmpdir,
                force_download=True,
            )
            return time.monotonic() - start
    except Exception:
        return None


def _probe_modelscope() -> Optional[float]:
    """Download config.json via modelscope SDK. Returns elapsed seconds or None."""
    _ensure_package("modelscope")
    from modelscope.hub.api import HubApi  # type: ignore

    try:
        api = HubApi()
        with tempfile.TemporaryDirectory() as tmpdir:
            start = time.monotonic()
            api.download_model(
                model_id=MODEL_MS_ID,
                include=[PROBE_FILE],
                local_dir=tmpdir,
            )
            return time.monotonic() - start
    except Exception:
        return None


PROBES = {
    "huggingface": _probe_hf,
    "modelscope":  _probe_modelscope,
}


def detect_best_source() -> str:
    """Benchmark each source by downloading config.json via SDK, return the fastest."""
    print(f"[*] Benchmarking sources (downloading {PROBE_FILE} via SDK)...\n")

    results: dict[str, float] = {}
    for name, probe_fn in PROBES.items():
        elapsed = probe_fn()
        if elapsed is not None:
            results[name] = elapsed
            print(f"  {name:14s}  {elapsed:.3f}s")
        else:
            print(f"  {name:14s}  FAILED")

    print()

    if not results:
        print("[!] All sources failed, defaulting to huggingface")
        return "huggingface"

    best = min(results, key=results.get)  # type: ignore[arg-type]
    print(f"[*] Fastest source: {best} ({results[best]:.3f}s)\n")
    return best


# ============ Download ============


def download_model(source: str, local_dir: str):
    """Download the full model using the specified source."""
    local_dir = os.path.abspath(local_dir)
    os.makedirs(local_dir, exist_ok=True)

    print(f"{'='*50}")
    print(f"  Source:    {source}")
    print(f"  Save to:   {local_dir}")
    print(f"{'='*50}\n")

    if source == "modelscope":
        _ensure_package("modelscope")
        from modelscope import snapshot_download  # type: ignore
        snapshot_download(MODEL_MS_ID, local_dir=local_dir)

    elif source == "huggingface":
        _ensure_package("huggingface_hub")
        from huggingface_hub import snapshot_download  # type: ignore
        snapshot_download(MODEL_HF_ID, local_dir=local_dir)

    else:
        print(f"[!] Unknown source: {source}")
        sys.exit(1)

    print(f"\n[OK] Model downloaded to: {local_dir}")
    print(f"[*]  Set model_path in config.json:")
    print(f'     "model": {{ "model_path": "{local_dir}" }}')


# ============ CLI ============


def main():
    parser = argparse.ArgumentParser(
        description="Download MiniCPM-o 4.5 model with automatic source selection"
    )
    parser.add_argument(
        "--local-dir",
        default=DEFAULT_LOCAL_DIR,
        help=f"Directory to save the model (default: {DEFAULT_LOCAL_DIR})",
    )
    parser.add_argument(
        "--source",
        choices=["auto", "huggingface", "modelscope"],
        default="auto",
        help="Download source (default: auto-detect by speed benchmark)",
    )
    parser.add_argument(
        "--verify",
        metavar="MODEL_PATH",
        help="Verify a model path (local dir or Hub ID) without downloading",
    )
    args = parser.parse_args()

    if args.verify:
        ok = verify_model(args.verify)
        sys.exit(0 if ok else 1)

    source = args.source
    if source == "auto":
        source = detect_best_source()

    download_model(source, args.local_dir)

    print(f"\n[*] Verifying downloaded model...")
    verify_model(args.local_dir)


if __name__ == "__main__":
    main()
