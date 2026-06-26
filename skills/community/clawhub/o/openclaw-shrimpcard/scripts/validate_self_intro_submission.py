#!/usr/bin/env python3
import argparse
from pathlib import Path

from skill_paths import SUBMISSION_SCHEMA_PATH, require_live_input
from validate_json import fail, load_json, validate


LIMITS = {
    "role": 32,
    "tagline": 42,
    "value_line": 52,
    "best_for": 60,
    "proof_anchor": 80,
    "poster_headline": 28,
    "poster_subline": 36,
    "share_caption": 48,
    "visual_brief": 72,
}


GENERIC_FRAGMENTS = [
    "强大的",
    "高效的",
    "智能助手",
    "general-purpose",
    "powerful",
    "helpful assistant",
    "multi-tool",
    "strong reasoning",
]


TEMPLATE_FRAGMENTS = [
    "format reference only",
    "format example only",
    "schema reference",
    "preview mode",
    "empty preview state",
    "not actual submission result",
]


PLACEHOLDER_IDENTITIES = {
    "sample agent",
    "sample owner",
}


FIXTURE_AGENT_NAMES = {
    "hermes agent",
}


FIXTURE_OWNER_NAMES = {
    "nous research",
}


ABSTRACT_IMAGE_FRAGMENTS = [
    "abstract",
    "geometric",
    "icon only",
    "symbol only",
    "just shapes",
    "纯抽象",
    "几何图形",
    "只有图标",
    "只有符号",
]


RECOGNIZABLE_CHARACTER_CUES = [
    "character",
    "agent",
    "robot",
    "avatar",
    "mascot",
    "courier",
    "messenger",
    "humanoid",
    "creature",
    "lobster",
    "crab",
    "角色",
    "代理",
    "机器人",
    "形象",
    "信使",
    "人形",
    "龙虾",
    "螃蟹",
]


def text_len(value: str) -> int:
    return len(str(value).strip())


def require_text_limit(path: str, value: str, limit: int):
    if text_len(value) == 0:
        fail(f"{path}: must not be empty")
    if text_len(value) > limit:
        fail(f"{path}: too long ({text_len(value)} > {limit})")


def reject_generic(path: str, value: str):
    lowered = str(value).lower()
    for fragment in GENERIC_FRAGMENTS:
        if fragment.lower() in lowered:
            fail(f"{path}: too generic, contains disallowed fragment `{fragment}`")


def walk_strings(value, path: str):
    if isinstance(value, dict):
        for key, item in value.items():
            next_path = f"{path}.{key}" if path else str(key)
            yield from walk_strings(item, next_path)
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_strings(item, f"{path}[{index}]")
        return
    if isinstance(value, str):
        yield path, value


def reject_template_payload(payload: dict):
    if "_sample_notice" in payload:
        fail("payload: sample notice must be removed from real submissions")

    for path, value in walk_strings(payload, ""):
        lowered = value.strip().lower()
        if lowered in PLACEHOLDER_IDENTITIES:
            fail(f"{path}: placeholder sample identity is not allowed in a real submission")
        for fragment in TEMPLATE_FRAGMENTS:
            if fragment in lowered:
                fail(f"{path}: contains template/sample fragment `{fragment}`")

    agent_name = str(payload.get("agent", {}).get("name", "")).strip().lower()
    owner_name = str(payload.get("owner", {}).get("name", "")).strip().lower()
    memory_basis = str(payload.get("identity", {}).get("memory_basis", "")).lower()
    proof_anchor = str(payload.get("identity", {}).get("proof_anchor", "")).lower()

    if agent_name in FIXTURE_AGENT_NAMES and "official" in memory_basis:
        fail("agent.name: fixture/example agent identities are not allowed in a real submission")
    if agent_name in FIXTURE_AGENT_NAMES and "official" in proof_anchor:
        fail("agent.name: fixture/example agent identities are not allowed in a real submission")
    if owner_name in FIXTURE_OWNER_NAMES and "official" in memory_basis and "repo" in memory_basis:
        fail("owner.name: fixture/example owner identity appears to come from example public docs, not current-agent evidence")


def validate_distinct_list(path: str, items: list[str], exact_count: int):
    if len(items) != exact_count:
        fail(f"{path}: must contain exactly {exact_count} items")
    normalized = [str(item).strip() for item in items]
    if any(not item for item in normalized):
        fail(f"{path}: items must not be empty")
    if len(set(normalized)) != len(normalized):
        fail(f"{path}: items must be distinct")


def validate_capabilities(items: list[str]):
    validate_distinct_list("identity.top_capabilities", items, 3)
    for item in items:
        if text_len(item) > 12:
            fail(f"identity.top_capabilities: capability `{item}` is too long (> 12)")
        reject_generic("identity.top_capabilities", item)


def validate_tags(items: list[str]):
    validate_distinct_list("identity.persona_tags", items, 3)
    for item in items:
        if text_len(item) > 12:
            fail(f"identity.persona_tags: tag `{item}` is too long (> 12)")


def validate_keywords(items: list[str]):
    if not (3 <= len(items) <= 4):
        fail("identity.share_keywords: must contain 3 to 4 items")
    normalized = [str(item).strip() for item in items]
    if any(not item for item in normalized):
        fail("identity.share_keywords: items must not be empty")
    if len(set(normalized)) != len(normalized):
        fail("identity.share_keywords: items must be distinct")


def validate_character_style(agent: dict, character_style: str):
    joined = " ".join(
        str(agent.get(field, "")).lower()
        for field in ["name", "product_type", "species", "visual_hint", "positioning_hint"]
    )
    explicit_brand = any(token in joined for token in ["openclaw", "lobster", "shrimp", "crab", "claw", "龙虾"])
    if character_style == "lobster" and not explicit_brand:
        fail("identity.character_style: `lobster` is only allowed when live evidence explicitly establishes claw/lobster branding")


def validate_prompt(identity: dict):
    prompt = str(identity["selfie_prompt"]).strip()
    if text_len(prompt) < 40:
        fail("identity.selfie_prompt: too short to be useful")
    lowered = prompt.lower()
    if "8-bit" not in lowered and "pixel art" not in lowered and "像素风" not in prompt:
        fail("identity.selfie_prompt: must explicitly indicate 8-bit / pixel art direction")
    if not any(cue in lowered or cue in prompt for cue in RECOGNIZABLE_CHARACTER_CUES):
        fail("identity.selfie_prompt: must describe a recognizable character, not abstract graphics")
    for fragment in ABSTRACT_IMAGE_FRAGMENTS:
        if fragment in lowered or fragment in prompt:
            fail(f"identity.selfie_prompt: abstract image direction is not allowed (`{fragment}`)")


def validate_visual_brief(identity: dict):
    brief = str(identity["visual_brief"]).strip()
    lowered = brief.lower()
    if not any(cue in lowered or cue in brief for cue in RECOGNIZABLE_CHARACTER_CUES):
        fail("identity.visual_brief: must describe a recognizable character concept")
    for fragment in ABSTRACT_IMAGE_FRAGMENTS:
        if fragment in lowered or fragment in brief:
            fail(f"identity.visual_brief: abstract image direction is not allowed (`{fragment}`)")


def validate_submission(payload: dict):
    validate(payload, load_json(SUBMISSION_SCHEMA_PATH))
    reject_template_payload(payload)

    identity = payload["identity"]

    require_text_limit("identity.role", identity["role"], LIMITS["role"])
    require_text_limit("identity.tagline", identity["tagline"], LIMITS["tagline"])
    reject_generic("identity.tagline", identity["tagline"])
    require_text_limit("identity.best_for", identity["best_for"], LIMITS["best_for"])
    require_text_limit("identity.proof_anchor", identity["proof_anchor"], LIMITS["proof_anchor"])
    require_text_limit("identity.poster_headline", identity["poster_headline"], LIMITS["poster_headline"])
    require_text_limit("identity.poster_subline", identity["poster_subline"], LIMITS["poster_subline"])
    require_text_limit("identity.share_caption", identity["share_caption"], LIMITS["share_caption"])
    require_text_limit("identity.visual_brief", identity["visual_brief"], LIMITS["visual_brief"])
    validate_visual_brief(identity)

    if identity.get("value_line"):
        require_text_limit("identity.value_line", identity["value_line"], LIMITS["value_line"])
        reject_generic("identity.value_line", identity["value_line"])

    validate_capabilities(identity["top_capabilities"])
    validate_tags(identity["persona_tags"])
    validate_keywords(identity["share_keywords"])
    validate_character_style(payload["agent"], identity["character_style"])
    validate_prompt(identity)

    if str(identity["source_count"]).strip() == "0":
        fail("identity.source_count: must be at least 1")

    proof_anchor = str(identity["proof_anchor"])
    if not any(token in proof_anchor for token in ["记忆", "evidence", "memory", "来源", "基于"]):
        fail("identity.proof_anchor: must mention evidence or memory basis")


def main():
    parser = argparse.ArgumentParser(description="Validate an agent-authored self-intro submission")
    parser.add_argument("submission_json", help="Path to the self-intro submission JSON")
    args = parser.parse_args()

    input_path = Path(args.submission_json)
    require_live_input(input_path, "submission_json")
    payload = load_json(input_path)
    validate_submission(payload)
    print("[OK] Self-intro submission is valid")


if __name__ == "__main__":
    main()
