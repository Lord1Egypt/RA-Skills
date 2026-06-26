import argparse
import json
import re
import sys
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "hexagrams.json"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def load_hexagrams() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def parse_moving_lines(raw: str | None) -> list[int]:
    if not raw:
        return []
    values = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        value = int(part)
        if value < 1 or value > 6:
            raise ValueError("动爻必须在 1 到 6 之间。")
        values.append(value)
    return sorted(set(values))


def parse_coin_face(raw: str) -> tuple[str, str]:
    lowered = raw.strip().lower()
    normalized = (
        lowered.replace("正面", "正")
        .replace("反面", "反")
        .replace("heads", "正")
        .replace("head", "正")
        .replace("tails", "反")
        .replace("tail", "反")
    )
    compact = (
        normalized.replace(" ", "")
        .replace("/", "")
        .replace("|", "")
        .replace("-", "")
        .replace("，", "")
    )
    if compact == "正":
        return "1", compact
    if compact == "反":
        return "0", compact
    raise ValueError("硬币结果只支持单次记录 `正`、`反`、`H` 或 `T`。")


def parse_coin_lines(raw: str) -> tuple[str, list[int], list[dict]]:
    compact = raw.strip().replace(" ", "").replace("\n", "").replace("\r", "")
    if len(compact) == 6 and all(char in {"0", "1"} for char in compact):
        line_details = []
        for index, bit in enumerate(compact, start=1):
            line_details.append(
                {
                    "line": index,
                    "raw": bit,
                    "normalized": bit,
                    "kind": "阳爻" if bit == "1" else "阴爻",
                    "is_moving": False,
                }
            )
        return compact, [], line_details

    groups = [part.strip() for part in re.split(r"[,\n;]+", raw) if part.strip()]
    if len(groups) != 6:
        raise ValueError(
            "铜钱起卦需要按从下往上提供 6 次结果，或直接提供 6 位二进制串，例如 `000111`。"
        )

    bits: list[str] = []
    line_details: list[dict] = []
    for index, group in enumerate(groups, start=1):
        bit, normalized = parse_coin_face(group)
        bits.append(bit)
        line_details.append(
            {
                "line": index,
                "raw": group,
                "normalized": normalized,
                "kind": "阳爻" if bit == "1" else "阴爻",
                "is_moving": False,
            }
        )
    return "".join(bits), [], line_details


def flip_lines(binary: str, moving_lines: list[int]) -> str:
    bits = list(binary)
    for line in moving_lines:
        index = line - 1
        bits[index] = "1" if bits[index] == "0" else "0"
    return "".join(bits)


def find_by_id(entries: list[dict], hexagram_id: int) -> dict:
    for entry in entries:
        if entry["id"] == hexagram_id:
            return entry
    raise ValueError(f"未找到卦序 {hexagram_id}。")


def find_by_binary(entries: list[dict], binary: str) -> dict:
    for entry in entries:
        if entry["binary"] == binary:
            return entry
    raise ValueError(f"未找到二进制卦象 {binary} 对应的条目。")


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(
        description="根据本卦动爻或手动抛币结果推导变卦。"
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--hexagram", type=int, help="本卦卦序，1-64。")
    input_group.add_argument(
        "--coin-lines",
        help=(
            "六次抛币结果，按从下往上输入；既可传 `反,正,反,正,反,反`，"
            "也可直接传 `000111`。"
        ),
    )
    parser.add_argument("--moving-lines", help="动爻列表，逗号分隔，例如 2,5。")
    args = parser.parse_args()

    entries = load_hexagrams()
    line_details = None
    if args.coin_lines:
        if args.moving_lines:
            parser.error("使用 --coin-lines 时不需要再额外传入 --moving-lines。")
        base_binary, moving_lines, line_details = parse_coin_lines(args.coin_lines)
        base_hexagram = find_by_binary(entries, base_binary)
        source_method = "manual_coin_toss"
    else:
        base_hexagram = find_by_id(entries, args.hexagram)
        moving_lines = parse_moving_lines(args.moving_lines)
        source_method = "standardized_hexagram"
    changed_binary = flip_lines(base_hexagram["binary"], moving_lines)
    changed_hexagram = find_by_binary(entries, changed_binary)

    result = {
        "source_method": source_method,
        "base_hexagram": {
            "id": base_hexagram["id"],
            "name_zh": base_hexagram["name_zh"],
            "slug": base_hexagram["slug"],
            "binary": base_hexagram["binary"],
        },
        "moving_lines": moving_lines,
        "changed_hexagram": {
            "id": changed_hexagram["id"],
            "name_zh": changed_hexagram["name_zh"],
            "slug": changed_hexagram["slug"],
            "binary": changed_hexagram["binary"],
        },
    }
    if line_details is not None:
        result["coin_line_details"] = line_details
        result["coin_rule"] = {
            "input_order": "从下往上（初爻到上爻）",
            "side_mapping": {"正": "阳爻", "反": "阴爻"},
            "binary_mapping": {"1": "阳爻", "0": "阴爻"},
            "moving_lines_note": "这种单次正反记录法只生成本卦，不直接产生动爻。",
        }

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
