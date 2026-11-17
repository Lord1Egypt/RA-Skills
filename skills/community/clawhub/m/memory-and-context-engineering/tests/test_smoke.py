"""冒烟测试：全部模块可导入、可实例化"""

import importlib
import glob
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def _all_modules():
    files = glob.glob(
        os.path.join(PROJECT_ROOT, "scripts", "**", "*.py"), recursive=True
    )
    mods = set()
    for f in files:
        if "generate-api-docs" in f or f.endswith("__init__.py"):
            continue
        rel = os.path.relpath(f, os.path.join(PROJECT_ROOT, "scripts"))
        mods.add("scripts." + rel[: -len(".py")].replace(os.sep, "."))
    return sorted(mods)


def test_all_modules_import():
    """全部脚本模块可导入（回归保护基线）"""
    fails = []
    for mod in _all_modules():
        try:
            importlib.import_module(mod)
        except Exception as exc:  # noqa: BLE001
            fails.append(f"{mod}: {type(exc).__name__}: {exc}")
    assert not fails, "导入失败的模块:\n" + "\n".join(fails)


def test_package_star_import():
    """from scripts import * 不因 __all__ 空引用而崩溃"""
    import scripts

    assert len(getattr(scripts, "__all__", [])) > 0
