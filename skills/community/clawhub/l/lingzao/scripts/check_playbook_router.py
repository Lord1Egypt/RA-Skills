#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK_DIR = SKILL_ROOT / "playbooks"
INDEX_PATH = PLAYBOOK_DIR / "router-index.json"
CASES_PATH = PLAYBOOK_DIR / "router-cases.json"
REQUIRED_FIELDS = {
    "id",
    "file",
    "role",
    "category",
    "platforms",
    "signals",
    "required_inputs",
    "outputs",
    "avoid_when",
    "companions",
}
ALLOWED_ROLES = {"router", "primary", "gate", "support"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    raise SystemExit(f"router check failed: {message}")


def normalize_text(value: str) -> str:
    return "".join(character.lower() for character in value if character.isalnum())


def select_primary_route(prompt: str, routing_signals: list[str], routes: list[dict]) -> str:
    normalized_prompt = normalize_text(prompt)
    normalized_signals = [normalize_text(signal) for signal in routing_signals]
    candidates = []
    for route in routes:
        if route["role"] != "primary":
            continue
        declared_signals = [normalize_text(signal) for signal in route["signals"]]
        if not all(
            any(case_signal in declared_signal for declared_signal in declared_signals)
            for case_signal in normalized_signals
        ):
            continue
        if any(normalize_text(value) in normalized_prompt for value in route["avoid_when"]):
            continue
        candidates.append(route["id"])

    if len(candidates) != 1:
        fail(
            "routing signals must select exactly one primary route, "
            f"got {candidates or 'none'}"
        )
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    args = parser.parse_args()

    index = load_json(INDEX_PATH)
    routes = index.get("routes")
    if not isinstance(routes, list) or not routes:
        fail("router-index.json must contain a non-empty routes list")

    policy = index.get("routing_policy", {})
    if policy.get("max_primary_playbooks") != 1:
        fail("max_primary_playbooks must be 1")
    if policy.get("max_supporting_playbooks") != 2:
        fail("max_supporting_playbooks must be 2")

    ids: set[str] = set()
    files: set[str] = set()
    for position, route in enumerate(routes, start=1):
        if not isinstance(route, dict):
            fail(f"route #{position} is not an object")
        missing = REQUIRED_FIELDS - route.keys()
        if missing:
            fail(f"route #{position} missing fields: {sorted(missing)}")
        route_id = route["id"]
        filename = route["file"]
        if route_id in ids:
            fail(f"duplicate route id: {route_id}")
        if filename in files:
            fail(f"duplicate playbook file: {filename}")
        if route["role"] not in ALLOWED_ROLES:
            fail(f"invalid role for {route_id}: {route['role']}")
        if not route["signals"]:
            fail(f"route has no user-like signals: {route_id}")
        if not route["outputs"]:
            fail(f"route has no outputs: {route_id}")
        ids.add(route_id)
        files.add(filename)

    actual_files = {path.name for path in PLAYBOOK_DIR.glob("*.md")}
    missing_routes = actual_files - files
    stale_routes = files - actual_files
    if missing_routes:
        fail(f"unregistered playbooks: {sorted(missing_routes)}")
    if stale_routes:
        fail(f"routes point to missing playbooks: {sorted(stale_routes)}")

    routes_by_id = {route["id"]: route for route in routes}
    for route in routes:
        for companion in route["companions"]:
            if companion not in ids:
                fail(f"{route['id']} references unknown companion: {companion}")
            if companion == route["id"]:
                fail(f"{route['id']} cannot reference itself as a companion")
            companion_role = routes_by_id[companion]["role"]
            if companion_role not in {"gate", "support"}:
                fail(
                    f"{route['id']} companion {companion} must be gate/support, "
                    f"got {companion_role}"
                )

    cases = load_json(args.cases).get("cases")
    if not isinstance(cases, list) or not cases:
        fail("router-cases.json must contain a non-empty cases list")
    for position, case in enumerate(cases, start=1):
        prompt = case.get("prompt")
        expected = case.get("expected_primary")
        routing_signals = case.get("routing_signals")
        if not isinstance(prompt, str) or not prompt.strip():
            fail(f"routing case #{position} has no prompt")
        if (
            not isinstance(routing_signals, list)
            or not routing_signals
            or not all(isinstance(signal, str) and normalize_text(signal) for signal in routing_signals)
        ):
            fail(f"routing case #{position} has no routing_signals")
        normalized_prompt = normalize_text(prompt)
        for signal in routing_signals:
            if normalize_text(signal) not in normalized_prompt:
                fail(f"routing case #{position} signal is absent from prompt: {signal}")
        if expected not in ids:
            fail(f"routing case #{position} references unknown route: {expected}")
        actual = select_primary_route(prompt, routing_signals, routes)
        if actual != expected:
            fail(f"routing case #{position} expected {expected}, got {actual}")

    print(
        f"Playbook router valid: {len(routes)} routes, "
        f"{len(actual_files)} playbooks, {len(cases)} routing cases."
    )


if __name__ == "__main__":
    main()
