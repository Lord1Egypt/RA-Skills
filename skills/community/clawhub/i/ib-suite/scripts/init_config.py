# skills/ib-suite/scripts/init_config.py
"""First-run config generator: template -> config.yaml with the one decision
that matters (paper vs live -> connection.port). Deterministic and offline.

Never overwrites an existing config unless --force. Never reads or writes any
token. The IB read-only boundary is unaffected: this only writes config.yaml.
"""
from __future__ import annotations
import argparse
from pathlib import Path

from ruamel.yaml import YAML

_PORT_BY_MODE = {"live": 4001, "paper": 4002}


def init_config(template: str | Path, out: str | Path, mode: str = "live",
                force: bool = False) -> dict:
    """Generate config.yaml from the template, overriding only the port.

    Reads the template round-trip (comments preserved), sets
    connection.port from `mode`, leaves storage.root / base_currency /
    thresholds at their template values, and writes to `out`.
    """
    if mode not in _PORT_BY_MODE:
        raise ValueError(f"mode must be one of {sorted(_PORT_BY_MODE)}, got {mode!r}")
    out_path = Path(out)
    if out_path.exists() and not force:
        raise FileExistsError(
            f"{out_path} already exists; pass --force to rebuild it")

    yaml = YAML(typ="rt")
    with open(template, "r", encoding="utf-8") as f:
        doc = yaml.load(f)

    port = _PORT_BY_MODE[mode]
    doc.setdefault("connection", {})
    doc["connection"]["port"] = port

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(doc, f)

    return {"config": str(out_path), "mode": mode, "port": port}


if __name__ == "__main__":
    default_template = Path(__file__).resolve().parent.parent / "ib-common" / "config.example.yaml"
    parser = argparse.ArgumentParser(description="Generate config.yaml for first-run setup (read-only project).")
    parser.add_argument("--template", default=str(default_template),
                        help="path to config.example.yaml")
    parser.add_argument("--out", default=".ib-suite/config.yaml",
                        help="target config path (workspace-local)")
    parser.add_argument("--mode", choices=sorted(_PORT_BY_MODE), default="live",
                        help="live => port 4001, paper => port 4002")
    parser.add_argument("--force", action="store_true",
                        help="overwrite an existing config")
    args = parser.parse_args()
    print(init_config(args.template, args.out, args.mode, args.force))
