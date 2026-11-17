"""Blueprint schema validation and the first chapter gate."""

from pathlib import Path

from .io import parse_frontmatter, read_frontmatter, read_json, safe_id
from .state import read_chapter_state, transition_chapter


class BlueprintError(ValueError):
    pass


_DEPENDENCY_KEYS = ("entities", "hooks", "relations", "events", "characters", "locations", "items", "factions")


def find_blueprint_file(root, chapter):
    root = Path(root).resolve()
    candidates = (
        root / "blueprints" / (chapter + ".md"),
        root / "blueprints" / (chapter + ".json"),
        root / "wiki" / "blueprints" / (chapter + ".md"),
        root / "wiki" / "blueprints" / (chapter + ".json"),
    )
    for path in candidates:
        if path.is_file():
            return path
    return None


def read_blueprint_document(path):
    path = Path(path)
    if path.suffix == ".md":
        meta, _body = read_frontmatter(path)
        return meta
    return read_json(path)


def validate_blueprint_document(blueprint, chapter):
    if not safe_id(chapter) or not isinstance(blueprint, dict):
        raise BlueprintError("blueprint must be an object with a path-safe chapter id")
    if blueprint.get("id") != chapter or not isinstance(blueprint.get("phase"), str) or not blueprint["phase"].strip():
        raise BlueprintError("blueprint requires matching id and phase")
    dependencies = blueprint.get("dependencies")
    if not isinstance(dependencies, dict) or set(dependencies) - set(_DEPENDENCY_KEYS):
        raise BlueprintError("blueprint dependencies contain unknown fields")
    for key in dependencies:
        if not isinstance(dependencies.get(key, []), list) or any(not safe_id(item) for item in dependencies.get(key, [])):
            raise BlueprintError("blueprint dependency lists must contain strings")
    if "scene_types" in blueprint and (
        not isinstance(blueprint["scene_types"], list)
        or any(not isinstance(item, str) or not item for item in blueprint["scene_types"])
    ):
        raise BlueprintError("blueprint scene_types must be non-empty strings")
    if "state" in blueprint and not isinstance(blueprint["state"], dict):
        raise BlueprintError("blueprint state must be an object")
    if "scenes" in blueprint:
        scenes = blueprint["scenes"]
        if not isinstance(scenes, list):
            raise BlueprintError("blueprint scenes must be a list")
        for scene in scenes:
            required = ("id", "location", "characters", "goal", "pressure", "information_change", "exit_state")
            if (
                not isinstance(scene, dict)
                or not safe_id(scene.get("id"))
                or not isinstance(scene.get("location"), str)
                or not isinstance(scene.get("characters"), list)
                or any(not isinstance(value, str) for value in scene["characters"])
                or any(not isinstance(scene.get(key), str) for key in required[3:])
            ):
                raise BlueprintError("blueprint scene is invalid")
    if "settlement" in blueprint:
        settlement = blueprint["settlement"]
        if (
            not isinstance(settlement, dict)
            or not isinstance(settlement.get("changes", []), list)
            or not isinstance(settlement.get("next_question", ""), str)
        ):
            raise BlueprintError("blueprint settlement is invalid")
    return blueprint


def validate_blueprint(root, chapter):
    root = Path(root).resolve()
    if not safe_id(chapter):
        raise BlueprintError("chapter id must be path-safe")
    path = find_blueprint_file(root, chapter)
    if path is None:
        raise BlueprintError("missing blueprint: {}".format(chapter))
    blueprint = validate_blueprint_document(read_blueprint_document(path), chapter)
    state = read_chapter_state(root, chapter)
    if state["status"] == "PLANNED":
        transition_chapter(root, chapter, "BLUEPRINT_VALID", {"blueprint": str(path.name)})
    elif state["status"] != "BLUEPRINT_VALID":
        raise BlueprintError("blueprint cannot be validated from {}".format(state["status"]))
    return blueprint
