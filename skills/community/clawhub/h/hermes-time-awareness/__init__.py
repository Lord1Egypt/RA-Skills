"""Hermes Time Awareness plugin — entry point."""

import importlib.util
import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))


def _load_register_hooks():
    hooks_path = _repo_root / "hooks.py"
    module_name = f"{__name__}._hooks"
    spec = importlib.util.spec_from_file_location(module_name, hooks_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load hooks module from {hooks_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module.register_hooks


register_hooks = _load_register_hooks()


def register(ctx) -> None:
    register_hooks(ctx)
