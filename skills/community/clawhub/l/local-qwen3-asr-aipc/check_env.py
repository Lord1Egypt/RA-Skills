#!/usr/bin/env python
"""Check runtime environment and model availability for the ASR skill."""

import json
import os
import re
import string
import subprocess
import sys
from pathlib import Path
from threading import Thread


def _read_skill_version() -> str:
    """Read SKILL_VERSION from SKILL.md next to this script."""
    try:
        md = Path(__file__).parent / "SKILL.md"
        m = re.search(r"\*\*SKILL_VERSION\*\*[^'\"]*['\"]([^'\"]+)['\"]", md.read_text(encoding="utf-8"))
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


def find_state() -> dict | None:
    """Locate state.json across all drives."""
    username = os.environ.get("USERNAME", "user").lower()
    for drive in string.ascii_uppercase:
        state_file = Path(f"{drive}:\\") / f"{username}_openvino" / "asr" / "state.json"
        if state_file.exists():
            try:
                return json.loads(state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
    return None


def model_layout_ready(model_dir: Path) -> bool:
    """Check model completeness by stat-ing key files (no recursive scan)."""
    thinker = model_dir / "thinker"

    def ok(items: list[tuple[Path, float]]) -> bool:
        return all(
            p.exists() and p.stat().st_size / 1024**2 >= min_mb
            for p, min_mb in items
        )

    thinker_layout = [
        (thinker / "openvino_thinker_language_model.bin",      1000),   # actual ~1126 MB
        (thinker / "openvino_thinker_audio_encoder_model.bin",  300),   # actual ~342 MB
        (thinker / "openvino_thinker_audio_model.bin",           18),   # actual ~21 MB
        (thinker / "openvino_thinker_embedding_model.bin",      270),   # actual ~303 MB
        (model_dir / "config.json",                           0.001),
    ]

    root_layout = [
        (model_dir / "openvino_language_model.bin",        800),
        (model_dir / "openvino_audio_encoder_model.bin",    50),
        (model_dir / "config.json",                       0.001),
    ]

    return ok(thinker_layout) or ok(root_layout)


def check_venv_async(venv_py: Path, result_holder: list):
    """Validate the venv in a background thread: Python works + key packages present + native intact."""
    try:
        # 1. check Python itself is executable
        proc = subprocess.run(
            [str(venv_py), "--version"],
            capture_output=True,
            timeout=5,
        )
        if proc.returncode != 0:
            result_holder.append(False)
            return

        # 2. check packages exist + locate site-packages for native check (instant, no import)
        check_script = (
            "import importlib.util, sys, pathlib; "
            "missing = [p for p in ['openvino','soundfile','qwen_asr'] if importlib.util.find_spec(p) is None]; "
            "print(pathlib.Path(importlib.util.find_spec('openvino').origin).parent) if not missing else None; "
            "sys.exit(len(missing))"
        )
        proc2 = subprocess.run(
            [str(venv_py), "-c", check_script],
            capture_output=True,
            timeout=10,
        )
        if proc2.returncode != 0:
            result_holder.append("PACKAGES_MISSING: openvino/soundfile/qwen_asr not all installed")
            return

        # 3. verify openvino core native library is present and has reasonable size (>10 MB)
        #    catches partial/corrupt installs that find_spec alone cannot detect
        ov_pkg_dir = Path(proc2.stdout.decode().strip())
        ov_core_dll = ov_pkg_dir / "libs" / "openvino.dll"
        if not ov_core_dll.exists() or ov_core_dll.stat().st_size < 10 * 1024 * 1024:
            result_holder.append("PACKAGES_MISSING: openvino native library incomplete or missing")
            return

        result_holder.append(True)
    except Exception as e:
        result_holder.append(False)


def main() -> int:
    state = find_state()
    if not state:
        print("STATE=MISSING")
        return 1

    venv_py = Path(state["VENV_PY"])
    asr_dir = Path(state["ASR_DIR"])
    model_dir = asr_dir / "Qwen3-ASR-0.6B-fp16-ov"

    # start venv thread first, then check model — both run in parallel
    venv_ok: list[bool] = []
    venv_thread = Thread(target=check_venv_async, args=(venv_py, venv_ok), daemon=True)
    venv_thread.start()

    # main thread: stat key files only, no recursive scan
    model_ready = model_layout_ready(model_dir)

    # wait for venv result — timeout must exceed max subprocess time (5 + 10 = 15s)
    venv_thread.join(timeout=20)

    if not venv_ok or not venv_ok[0]:
        if venv_ok and isinstance(venv_ok[0], str):
            print(venv_ok[0])   # print PACKAGES_MISSING: ... details
        else:
            print("VENV_PY=BROKEN")
        return 1

    if not model_ready:
        print("MODEL_STATUS=MISSING")
        return 1

    print(f"VENV_PY={venv_py}")
    print(f"ASR_DIR={asr_dir}")
    print("MODEL_STATUS=READY")

    # version staleness check — both deployed runtime scripts must match SKILL.md
    skill_ver = _read_skill_version()
    deployed_versions = []
    transcribe_dst = asr_dir / "transcribe.py"
    if transcribe_dst.exists():
        try:
            m = re.search(
                r'SKILL_VERSION\s*=\s*["\'](.+?)["\']',
                transcribe_dst.read_text(encoding="utf-8", errors="ignore"),
            )
            if m:
                deployed_versions.append(m.group(1))
        except Exception:
            pass

    engine_dst = asr_dir / "asr_engine.py"
    if engine_dst.exists():
        try:
            m = re.search(
                r'SKILL_VERSION\s*=\s*["\'](.+?)["\']',
                engine_dst.read_text(encoding="utf-8", errors="ignore"),
            )
            if m:
                deployed_versions.append(m.group(1))
        except Exception:
            pass

    if skill_ver != "unknown":
        mismatched = [ver for ver in deployed_versions if ver != skill_ver]
        if mismatched or len(deployed_versions) < 2:
            current = ",".join(deployed_versions) if deployed_versions else "unknown"
            print(f"SCRIPTS_STALE={current}->{skill_ver}")

    return 0


if __name__ == "__main__":
    sys.exit(main())