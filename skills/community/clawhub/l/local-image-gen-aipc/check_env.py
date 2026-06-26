#!/usr/bin/env python
"""Check runtime environment and model availability for the image-gen skill."""

import json
import os
import string
import subprocess
import sys
from pathlib import Path
from threading import Thread


def find_state() -> dict | None:
    """Locate state.json written by setup.py."""
    username = os.environ.get("USERNAME", "user").lower()
    for drive in string.ascii_uppercase:
        state_file = (
            Path(f"{drive}:\\") / f"{username}_openvino" / "imagegen" / "state.json"
        )
        if state_file.exists():
            try:
                return json.loads(state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
    return None


def _read_skill_version() -> str:
    """Read SKILL_VERSION from SKILL.md next to this script — single source of truth."""
    skill_md = Path(__file__).parent / "SKILL.md"
    if skill_md.exists():
        for line in skill_md.read_text(encoding="utf-8").splitlines():
            if "SKILL_VERSION" in line and "`" in line:
                parts = line.split("`")
                if len(parts) >= 2:
                    return parts[1]
    return "unknown"


def _read_deployed_version(script_path: Path) -> str | None:
    """Read SKILL_VERSION embedded in the deployed generate_image.py."""
    if not script_path.exists():
        return None
    for line in script_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("SKILL_VERSION") and "=" in line:
            return line.split("=")[1].strip().strip("\"'")
    return None


def model_layout_ready(model_dir: Path) -> tuple[bool, list[str], float]:
    """Check model completeness by statting key subdirs and .bin files.

    Returns (ready, missing_dirs, total_gb).
    Each required subdir must exist and contain at least one .bin file >= 1 MB.
    Total GB is computed only when all dirs are present (rglob scan).
    """
    required = ["transformer", "vae_decoder", "text_encoder"]
    missing: list[str] = []
    for name in required:
        subdir = model_dir / name
        if not subdir.is_dir():
            missing.append(name)
            continue
        bins = list(subdir.glob("*.bin"))
        if not bins or max(f.stat().st_size for f in bins) < 1024 * 1024:
            # directory exists but contains no real weights — treat as missing
            missing.append(name)

    if missing:
        return False, missing, 0.0

    total = sum(f.stat().st_size for f in model_dir.rglob("*") if f.is_file()) / 1024**3
    return True, [], total


def check_venv_async(venv_py: Path, result_holder: list) -> None:
    """Validate venv: executable + all key packages importable.

    Runs in a background thread so model stat and venv check can overlap.
    Appends True, False, or a "PACKAGES_MISSING: ..." string to result_holder.
    """
    try:
        # 1. venv Python itself must be executable
        proc = subprocess.run(
            [str(venv_py), "--version"],
            capture_output=True,
            timeout=3,
        )
        if proc.returncode != 0:
            result_holder.append(False)
            return

        # 2. All runtime packages must be importable
        check_script = (
            "import openvino; import torch; import PIL; "
            "import modelscope; from optimum.intel import OVZImagePipeline"
        )
        proc2 = subprocess.run(
            [str(venv_py), "-c", check_script],
            capture_output=True,
            timeout=15,
        )
        if proc2.returncode != 0:
            detail = proc2.stderr.decode(errors="replace").strip()
            result_holder.append(f"PACKAGES_MISSING: {detail}")
            return

        result_holder.append(True)
    except Exception:
        result_holder.append(False)


def main() -> int:
    state = find_state()
    if not state:
        print("STATE=MISSING")
        return 1

    venv_py = Path(state["VENV_PY"])
    imagegen_dir = Path(state["IMAGE_GEN_DIR"])
    model_dir = imagegen_dir / "Z-Image-Turbo-int4-ov"

    # Start venv check in background; stat model files in main thread — both run in parallel
    venv_ok: list = []
    venv_thread = Thread(target=check_venv_async, args=(venv_py, venv_ok), daemon=True)
    venv_thread.start()

    # Model check (main thread — stat only, no imports needed)
    model_ready, missing_dirs, total_gb = model_layout_ready(model_dir)

    # Wait for venv result (model stat already consumed most of the wait time)
    venv_thread.join(timeout=10)

    if not venv_ok or venv_ok[0] is False:
        print("VENV_PY=BROKEN")
        return 1

    if isinstance(venv_ok[0], str):
        print(venv_ok[0])  # PACKAGES_MISSING: <detail>
        return 1

    if not model_ready:
        print(f"MODEL_STATUS=MISSING  missing={missing_dirs}")
        return 1

    print(f"VENV_PY={venv_py}")
    print(f"IMAGE_GEN_DIR={imagegen_dir}")
    print(f"MODEL_STATUS=READY  ({total_gb:.2f} GB)")

    # Script staleness check — compare deployed generate_image.py against SKILL.md
    skill_ver = _read_skill_version()
    deployed_ver = _read_deployed_version(imagegen_dir / "generate_image.py")
    if deployed_ver is None:
        print(f"SCRIPTS_STALE=missing->{skill_ver}")
    elif deployed_ver != skill_ver:
        print(f"SCRIPTS_STALE={deployed_ver}->{skill_ver}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
