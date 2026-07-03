import os
from pathlib import Path


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[4]