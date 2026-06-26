from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


def _expand_vars(s: str, ctx: Dict[str, str]) -> str:
    # ${HOME} and ${workdir} style
    for k, v in ctx.items():
        s = s.replace("${" + k + "}", v)
    s = os.path.expandvars(s)
    return s


def load_config() -> Dict[str, Any]:
    here = Path(__file__).resolve().parents[1]
    cfg_path = here / "config" / "progress_selfcheck_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    workdir = cfg.get("workdir") or str(Path.cwd())
    ctx = {
        "HOME": str(Path.home()),
        "workdir": workdir,
        "output_dir": cfg.get("output_dir") or str(Path(workdir) / "output"),
        "memory_dir": cfg.get("memory_dir") or str(Path(workdir) / "memory"),
    }

    def walk(x):
        if isinstance(x, str):
            return _expand_vars(x, ctx)
        if isinstance(x, list):
            return [walk(i) for i in x]
        if isinstance(x, dict):
            return {k: walk(v) for k, v in x.items()}
        return x

    cfg = walk(cfg)
    return cfg
