"""Validated, state-aware narrative engine loading."""

import json
import re
from pathlib import Path

from .manifest import verify_manifest


class EngineValidationError(ValueError):
    pass


_ID = re.compile(r"^[A-Z][A-Z0-9_-]+$")
_HARDNESS = {"required", "recommended", "optional"}


def _read(path):
    try:
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as exc:
        raise EngineValidationError("invalid engine JSON: {}".format(path)) from exc


def load_engine(engine_root, require_manifest=True):
    input_root = Path(engine_root)
    if input_root.is_symlink():
        raise EngineValidationError("engine root must not be a symlink")
    root = input_root.resolve()
    if any(path.is_symlink() for path in root.rglob("*")):
        raise EngineValidationError("engine must not contain symlinks")
    for required in ("applicability.md", "limits.md"):
        if not (root / required).is_file():
            raise EngineValidationError("engine is missing required file: {}".format(required))
    manifest = _read(root / "engine.json")
    if not isinstance(manifest, dict) or not re.match(r"^[a-z][a-z0-9-]+$", str(manifest.get("id", ""))):
        raise EngineValidationError("engine.json requires a path-safe id")
    if manifest.get("kind") != "narrative-engine":
        raise EngineValidationError("engine.json kind must be narrative-engine")
    if "activation" in manifest and not isinstance(manifest["activation"], str):
        raise EngineValidationError("engine.json activation must be a string")
    if "language_imitation" in manifest and not isinstance(manifest["language_imitation"], bool):
        raise EngineValidationError("engine.json language_imitation must be boolean")
    if not isinstance(manifest.get("version"), int) or isinstance(manifest.get("version"), bool):
        raise EngineValidationError("engine.json requires integer version")
    card_files = manifest.get("card_files", [])
    if not isinstance(card_files, list) or any(not isinstance(relative, str) or not relative for relative in card_files):
        raise EngineValidationError("engine.json card_files must be a string list")
    manifest_path = root / "manifest.json"
    if require_manifest and not manifest_path.is_file():
        raise EngineValidationError("engine is missing required file: manifest.json")
    if manifest_path.is_file() and not verify_manifest(root):
        raise EngineValidationError("engine manifest is missing or invalid")
    cards = []
    for relative in card_files:
        path = root / relative
        try:
            path.resolve().relative_to(root)
        except ValueError:
            raise EngineValidationError("unsafe card file: {}".format(relative))
        if not path.is_file():
            raise EngineValidationError("missing or unsafe card file: {}".format(relative))
        data = _read(path)
        if not isinstance(data, list):
            raise EngineValidationError("card file must contain a list: {}".format(relative))
        cards.extend(data)
    ids = set()
    for card in cards:
        if not isinstance(card, dict) or not _ID.match(str(card.get("id", ""))):
            raise EngineValidationError("each method card needs an uppercase id")
        if card["id"] in ids:
            raise EngineValidationError("duplicate method card: {}".format(card["id"]))
        ids.add(card["id"])
        when = card.get("when", {})
        if not isinstance(when, dict):
            raise EngineValidationError("method card when must be an object")
        for key in ("phase", "scene_types", "requires"):
            if key in when and (
                not isinstance(when[key], list)
                or any(not isinstance(value, str) or not value for value in when[key])
            ):
                raise EngineValidationError("method card when.{} must be a string list".format(key))
        if "requires" in card and (
            not isinstance(card["requires"], list)
            or any(not isinstance(value, str) or not value for value in card["requires"])
        ):
            raise EngineValidationError("method card requires must be a string list")
        if not isinstance(card.get("kind"), str) or not card["kind"]:
            raise EngineValidationError("method card kind is required")
        if not isinstance(card.get("name"), str) or not card["name"]:
            raise EngineValidationError("method card name is required")
        if card.get("hardness") not in _HARDNESS:
            raise EngineValidationError("method card hardness is invalid")
        if not isinstance(card.get("prompt"), str) or not card["prompt"]:
            raise EngineValidationError("method card prompt is required")
    manifest["root"] = str(root)
    manifest["cards"] = cards
    return manifest


def _matches(card, state):
    when = card.get("when", {})
    for key, expected in when.items():
        actual = state.get(key)
        if key == "requires":
            for requirement in expected:
                value = state
                for part in str(requirement).split("."):
                    if not isinstance(value, dict) or part not in value:
                        return False
                    value = value[part]
            continue
        if key == "phase" and isinstance(expected, list):
            if actual not in expected:
                return False
        elif key == "scene_types":
            actual_types = state.get("scene_types", [state.get("scene_type")])
            if not any(value in expected for value in actual_types if value is not None):
                return False
        elif isinstance(expected, list):
            if actual not in expected:
                return False
        elif actual != expected:
            return False
    for key in card.get("requires", []):
        value = state
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return False
            value = value[part]
    return True


def select_cards(engine_root, state):
    engine = load_engine(engine_root)
    return [card for card in engine["cards"] if _matches(card, state)]
