"""Safely persist local IBKR Flex credentials and window map in config.yaml."""
from __future__ import annotations

import argparse
from collections.abc import Mapping
import json
import os
from pathlib import Path
import sys
import tempfile

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from ib_common.config import load_config


_CONFIG_ERROR = "configuration could not be read or validated; repair config.yaml and retry"


_WINDOW_FORMAT = (
    "window must use the format <days|mtd|ytd>=<id>, e.g. 7=1575544 or ytd=1590003"
)


def parse_window(spec: str) -> tuple[str, str]:
    """Parse a '<days|mtd|ytd>=<query-id>' spec into (key, query_id)."""
    key_text, sep, query_id = spec.partition("=")
    key = key_text.strip().lower()
    if not sep or not key or not query_id.strip():
        raise ValueError(_WINDOW_FORMAT)
    if key in ("mtd", "ytd"):
        return key, query_id.strip()
    if not key.isdigit() or int(key) <= 0:
        raise ValueError(_WINDOW_FORMAT)
    return key, query_id.strip()


def configure_flex(
    config_path: str | Path,
    token: str | None = None,
    windows: Mapping[str, str] | None = None,
    force: bool = False,
    target: str | None = None,
) -> dict:
    """Persist a Flex token and/or per-skill window map, preserving comments."""
    windows = {str(day): qid for day, qid in dict(windows or {}).items()}
    if token is not None and not token.strip():
        raise ValueError("Flex token must not be blank")
    if token is None and not windows:
        raise ValueError("provide a token or at least one window")
    if windows and target not in ("trade_history", "dividend"):
        raise ValueError(
            "writing Flex windows requires --target trade_history|dividend"
        )
    map_key = f"{target}_query_ids" if windows else None

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing; run ib-suite first-run setup before configuring Flex"
        )

    yaml = YAML(typ="rt")
    try:
        contents = path.read_text(encoding="utf-8")
        doc = yaml.load(contents)
        if doc is None:
            doc = yaml.load(f"{contents}\n{{}}\n")
    except (OSError, YAMLError):
        raise ValueError(_CONFIG_ERROR) from None

    if not isinstance(doc, Mapping):
        raise ValueError(_CONFIG_ERROR)

    flex = doc.get("flex")
    if flex is not None and not isinstance(flex, Mapping):
        raise ValueError(_CONFIG_ERROR)
    if flex is None:
        doc["flex"] = {}
        flex = doc["flex"]

    existing_norm: dict[str, str] = {}
    if map_key is not None:
        existing = flex.get(map_key)
        if existing is not None and not isinstance(existing, Mapping):
            raise ValueError(_CONFIG_ERROR)
        existing_norm = {str(day): qid for day, qid in dict(existing or {}).items()}

    if not force:
        if token is not None and flex.get("token") is not None:
            raise FileExistsError(
                "Flex token already exists; pass --force to replace it"
            )
        clashes = [day for day in windows if day in existing_norm]
        if clashes:
            raise FileExistsError(
                f"Flex windows already exist for {sorted(clashes)}; pass --force to replace"
            )

    if token is not None:
        flex["token"] = token
    if windows:
        merged = dict(existing_norm)
        merged.update(windows)
        ordered = sorted(merged, key=lambda k: (0, int(k)) if k.isdigit() else (1, k))
        flex[map_key] = {k: merged[k] for k in ordered}

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as file:
            temporary_path = Path(file.name)
            yaml.dump(doc, file)

        config = load_config(temporary_path)
        if token is not None and config.flex.token != token:
            raise ValueError("staged Flex token did not reload exactly")
        for day, query_id in windows.items():
            if getattr(config.flex, map_key).get(day) != query_id:
                raise ValueError("staged Flex windows did not reload exactly")
        os.replace(temporary_path, path)
        temporary_path = None
    except Exception:
        raise ValueError(_CONFIG_ERROR) from None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return {"config": str(path), "ready": True}


def main() -> None:
    """Parse local configuration arguments and print the public setup result."""
    parser = argparse.ArgumentParser(
        description="Persist local IBKR Flex credentials for the read-only trade-history skill"
    )
    parser.add_argument("--config", required=True, help="path to config.yaml")
    token_group = parser.add_mutually_exclusive_group()
    token_group.add_argument("--token", help=argparse.SUPPRESS)
    token_group.add_argument(
        "--token-stdin",
        action="store_true",
        help="read the IBKR Flex token from one stdin line",
    )
    parser.add_argument(
        "--window", action="append", default=[],
        help="window spec '<days|mtd|ytd>=<query-id>', repeatable",
    )
    parser.add_argument(
        "--target", choices=["trade_history", "dividend"],
        help="which skill's window map to write when using --window",
    )
    parser.add_argument(
        "--force", action="store_true", help="replace an existing token or window"
    )
    args = parser.parse_args()
    try:
        windows = dict(parse_window(spec) for spec in args.window)
        token = sys.stdin.readline().rstrip("\r\n") if args.token_stdin else args.token
        result = configure_flex(args.config, token, windows, args.force, args.target)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result))


if __name__ == "__main__":
    main()
