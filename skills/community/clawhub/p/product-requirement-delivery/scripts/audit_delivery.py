import argparse
import json
from pathlib import Path


ID_KEYS = [
    "required_role_ids",
    "required_story_ids",
    "required_req_ids",
    "required_exception_ids",
    "required_ac_ids",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--published", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    artifacts = [
        (args.source, args.source.read_text(encoding="utf-8")),
        (args.published, args.published.read_text(encoding="utf-8")),
    ]
    problems = []

    status = manifest.get("confirmed_status")
    if status:
        for path, text in artifacts:
            if status not in text:
                problems.append(f"{path.name}: missing confirmed status: {status}")

    required = list(manifest.get("required_phrases", []))
    required.extend(manifest.get("required_urls", []))
    for key in ID_KEYS:
        required.extend(manifest.get(key, []))

    for path, text in artifacts:
        for phrase in required:
            if phrase not in text:
                problems.append(f"{path.name}: missing required content: {phrase}")
        for phrase in manifest.get("forbidden_phrases", []):
            if phrase in text:
                problems.append(f"{path.name}: contains forbidden phrase: {phrase}")

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)

    print(f"OK: source and published Feishu content audited ({len(required)} required items)")


if __name__ == "__main__":
    main()
