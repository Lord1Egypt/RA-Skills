import os
from pathlib import Path


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[4]


def vault_root() -> Path:
    env = os.environ.get("LYGO_VAULT_ROOT")
    if env:
        return Path(env)
    return stack_root() / "lygo_second_brain" / "vault"