import argparse
import json
import sys
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "hexagrams.json"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_hexagrams() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    return text.strip().lower().replace(" ", "")


def find_hexagram(entries: list[dict], hexagram_id: int | None, name: str | None) -> dict | None:
    if hexagram_id is not None:
        for entry in entries:
            if entry["id"] == hexagram_id:
                return entry
        return None

    if not name:
        return None

    target = normalize(name)
    for entry in entries:
        aliases = {
            str(entry["id"]),
            normalize(entry["name_zh"]),
            normalize(entry["slug"]),
            normalize(entry["code"]),
            normalize(entry["binary"]),
        }
        aliases.update(normalize(alias) for alias in entry.get("aliases", []))
        if target in aliases:
            return entry
    return None


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="按卦序或名称查询六十四卦基础信息。")
    parser.add_argument("--id", type=int, help="卦序编号，1-64。")
    parser.add_argument("--name", help="卦名、代号或别名。")
    args = parser.parse_args()

    entries = load_hexagrams()
    result = find_hexagram(entries, args.id, args.name)
    if not result:
        raise SystemExit("未找到对应卦象，请检查卦序、名称或别名。")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
