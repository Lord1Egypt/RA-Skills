#!/usr/bin/env python3
"""
Check whether the local Document AI skill is ready for MinerU 2.5 with
OpenVINO GenAI.
"""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import sys
from pathlib import Path

from _local_vendor import bootstrap_local_vendor


LOCAL_RUNTIME_PATHS = bootstrap_local_vendor()


MINERU_REQUIRED_MODEL_FILES = (
    "openvino_language_model.xml",
    "openvino_vision_embeddings_model.xml",
    "openvino_tokenizer.xml",
    "openvino_detokenizer.xml",
)

OPTIONAL_MODULES = {
    "openvino": "Base OpenVINO runtime",
    "openvino_genai": "OpenVINO GenAI runtime for MinerU VLM inference",
    "mineru_vl_utils": "MinerU two-step parsing helpers and post-processors",
    "pypdfium2": "PDF rasterization for MinerU page rendering",
    "PIL": "Pillow image loading",
    "fitz": "Optional PyMuPDF text/PDF smoke backend",
    "pypdf": "Optional pure-Python PDF smoke backend",
    "gradio": "Optional local demo UI",
}


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def module_importable(name: str) -> tuple[bool, str | None]:
    if not module_available(name):
        return False, None
    try:
        __import__(name)
    except Exception as exc:
        return False, str(exc)
    return True, None


def mineru_backend_importable() -> tuple[bool, str | None]:
    try:
        from mineru_openvino_backend import OVMinerUClient  # noqa: F401
    except Exception as exc:
        return False, str(exc)
    return True, None


def is_valid_mineru_model_dir(path: Path) -> bool:
    return path.is_dir() and all((path / filename).exists() for filename in MINERU_REQUIRED_MODEL_FILES)


def find_model_assets(base_dir: Path) -> dict[str, object]:
    env_dir = os.environ.get("MINERU_OPENVINO_MODEL_DIR")
    alt_env_dir = os.environ.get("MINERU_MODEL_DIR")
    candidates: list[Path] = []
    if env_dir:
        candidates.append(Path(env_dir).expanduser())
    if alt_env_dir:
        candidates.append(Path(alt_env_dir).expanduser())

    local_models = base_dir / "models"
    candidates.extend(
        [
            local_models / "MinerU2.5-Pro-2604-1.2B-int4-ov",
            local_models / "mineru2.5-int4-ov",
            local_models / "MinerU2.5-Pro-2604-1.2B-ov",
        ]
    )

    cache_root = Path.home() / ".cache" / "modelscope" / "hub" / "models" / "snake7gun"
    if cache_root.exists():
        candidates.extend(path for path in cache_root.iterdir() if path.is_dir())

    inspected: list[str] = []
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        inspected.append(str(candidate))
        if is_valid_mineru_model_dir(candidate):
            present_files = [name for name in MINERU_REQUIRED_MODEL_FILES if (candidate / name).exists()]
            optional_files = sorted(
                path.name
                for path in candidate.iterdir()
                if path.is_file() and path.suffix.lower() in {".xml", ".bin", ".json", ".jinja"}
            )
            return {
                "env_vars": {
                    "MINERU_OPENVINO_MODEL_DIR": env_dir,
                    "MINERU_MODEL_DIR": alt_env_dir,
                    "MINERU_OPENVINO_DEVICE": os.environ.get("MINERU_OPENVINO_DEVICE"),
                    "MINERU_OPENVINO_DPI": os.environ.get("MINERU_OPENVINO_DPI"),
                },
                "found": True,
                "model_dir": str(candidate),
                "required_files": present_files,
                "optional_files": optional_files,
                "detokenizer_patched": (candidate / ".mineru_detokenizer_patched").exists(),
                "inspected_candidates": inspected,
            }

    return {
        "env_vars": {
            "MINERU_OPENVINO_MODEL_DIR": env_dir,
            "MINERU_MODEL_DIR": alt_env_dir,
            "MINERU_OPENVINO_DEVICE": os.environ.get("MINERU_OPENVINO_DEVICE"),
            "MINERU_OPENVINO_DPI": os.environ.get("MINERU_OPENVINO_DPI"),
        },
        "found": False,
        "model_dir": None,
        "required_files": [],
        "optional_files": [],
        "detokenizer_patched": False,
        "inspected_candidates": inspected,
    }


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    modules = {}
    module_ok: dict[str, bool] = {}
    for name, purpose in OPTIONAL_MODULES.items():
        available, import_error = module_importable(name)
        modules[name] = {
            "available": available,
            "purpose": purpose,
        }
        if import_error:
            modules[name]["import_error"] = import_error
        module_ok[name] = available

    has_mineru_stack = (
        module_ok["openvino"]
        and module_ok["openvino_genai"]
        and module_ok["mineru_vl_utils"]
    )
    has_page_renderer = module_ok["pypdfium2"]
    has_image_loader = module_ok["PIL"]
    has_pdf_smoke_backend = module_ok["fitz"] or module_ok["pypdf"]
    model_assets = find_model_assets(base_dir)
    model_dir_ready = bool(model_assets["found"])
    backend_ready, backend_error = mineru_backend_importable()
    mineru_ready = has_mineru_stack and has_page_renderer and has_image_loader and backend_ready and model_dir_ready

    warnings: list[str] = []
    if not module_ok["openvino"]:
        warnings.append("OpenVINO is missing; local inference is unavailable.")
    if not module_ok["openvino_genai"]:
        warnings.append("openvino-genai is missing; MinerU VLM inference cannot start.")
    if not module_ok["mineru_vl_utils"]:
        warnings.append("mineru-vl-utils is missing; MinerU two-step post-processing cannot run.")
    if not module_ok["pypdfium2"]:
        warnings.append("pypdfium2 is missing; PDF pages cannot be rendered for MinerU.")
    if not module_ok["PIL"]:
        warnings.append("Pillow is missing; image inputs cannot be loaded.")
    if backend_error:
        warnings.append(f"MinerU backend import failed: {backend_error}")
    if not model_dir_ready:
        warnings.append(
            "MinerU OpenVINO model assets were not found. Download the preconverted ModelScope bundle and "
            "set MINERU_OPENVINO_MODEL_DIR, or place it under {baseDir}/models/."
        )
    elif not model_assets["detokenizer_patched"]:
        warnings.append(
            "The detected model bundle is missing .mineru_detokenizer_patched. Prefer the prepatched "
            "ModelScope OpenVINO bundle to avoid layout token stripping."
        )

    if mineru_ready:
        next_step = "MinerU OpenVINO runtime is ready. Run scripts/run_skill.py on a real PDF or image next."
    elif has_mineru_stack and not model_dir_ready:
        next_step = (
            "Download snake7gun/MinerU2.5-Pro-2604-1.2B-int4-ov, set MINERU_OPENVINO_MODEL_DIR to that folder, "
            "then rerun scripts/check_env.py."
        )
    else:
        next_step = (
            "Create a virtual environment, install requirements.txt, download the preconverted MinerU OV model, "
            "and rerun scripts/check_env.py."
        )

    payload = {
        "ok": mineru_ready,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "skill_dir": str(base_dir),
        "local_runtime_paths": LOCAL_RUNTIME_PATHS,
        "capabilities": {
            "mineru_openvino_ready": mineru_ready,
            "openvino_runtime": module_ok["openvino"],
            "openvino_genai_runtime": module_ok["openvino_genai"],
            "mineru_vl_utils": module_ok["mineru_vl_utils"],
            "mineru_backend_importable": backend_ready,
            "pdf_page_renderer": has_page_renderer,
            "image_loader": has_image_loader,
            "model_dir_ready": model_dir_ready,
            "pdf_text_smoke_backend": has_pdf_smoke_backend,
            "optional_demo_ui": module_ok["gradio"],
        },
        "model_assets": model_assets,
        "modules": modules,
        "warnings": warnings,
        "next_step": next_step,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
