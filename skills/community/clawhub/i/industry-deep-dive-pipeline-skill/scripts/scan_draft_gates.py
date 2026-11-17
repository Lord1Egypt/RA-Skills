from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SECRET_PATTERNS = {
    "notion_token": re.compile(r"ntn_[A-Za-z0-9]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "openai_style_key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
UUID_PATTERN = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
PERSONAL_PATH_PATTERN = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/)[^\s`\"']+", re.I)
NUMBER_PATTERN = re.compile(r"(?<![A-Za-z])(?:US\$|HK\$|[$￥¥€£])?\d+(?:[.,]\d+)*(?:%|倍|万亿|亿|万|千|百万|十亿|百亿|年|月|日|小时|分钟|tokens?|Token)?", re.I)

GENERIC_RED_LINES = {
    "paired_contrast_zh": re.compile(r"不是.{0,40}而是|并非.{0,40}而是|不在.{0,30}在|而非"),
    "paired_contrast_en": re.compile(r"\bnot\b.{0,50}\bbut\b|\brather than\b", re.I),
    "meta_commentary": re.compile(r"本文将|本篇将|先说结论|一句话收口|下面将|接下来我们|延伸问题|这一篇(?:要|会|将)|this (?:article|piece) (?:will|explores|examines)", re.I),
    "marketing_jargon": re.compile(r"赋能|闭环|端到端|颠覆性|革命性|game[- ]changing|revolutionary|disruptive", re.I),
    "spoken_buffer": re.compile(r"我觉得|差不多|其实|更像|I think\b", re.I),
    "publication_material": re.compile(r"^\s*(?:#\S+\s*){2,}$|话题标签|发布信息|封面提示词|LinkedIn caption|Notion 入库", re.I),
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def normalize_number(token: str) -> str:
    return re.sub(r"[\s,，]", "", token).lower()


def load_profile_patterns(path: Path | None) -> list[tuple[str, re.Pattern[str]]]:
    if path is None or not path.is_file():
        return []
    try:
        data = json.loads(read_text(path))
    except Exception:
        return []
    patterns: list[str] = []
    if isinstance(data.get("negative_rules"), list):
        for item in data["negative_rules"]:
            if isinstance(item, str):
                patterns.append(item)
            elif isinstance(item, dict) and isinstance(item.get("literal_pattern"), str):
                patterns.append(item["literal_pattern"])
    elif isinstance(data.get("negative_rules"), dict):
        patterns.extend(x for x in data["negative_rules"].get("literal_patterns", []) if isinstance(x, str))
    return [(f"profile_{idx + 1}", re.compile(re.escape(pattern), re.I)) for idx, pattern in enumerate(patterns)]


def line_hits(text: str, name: str, pattern: re.Pattern[str], severity: str) -> list[dict]:
    hits = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            hits.append({"severity": severity, "category": name, "line": line_no, "excerpt": line.strip()[:180]})
    return hits


def extract_numbers(text: str) -> set[str]:
    return {normalize_number(match.group(0)) for match in NUMBER_PATTERN.finditer(text) if len(re.sub(r"\D", "", match.group(0))) >= 1}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a deep-dive article draft for deterministic gates")
    parser.add_argument("--draft", required=True)
    parser.add_argument("--facts", required=True)
    parser.add_argument("--profile")
    parser.add_argument("--output", required=True)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    draft_path = Path(args.draft)
    facts_path = Path(args.facts)
    profile_path = Path(args.profile) if args.profile else None
    issues: list[dict] = []

    if not draft_path.is_file():
        issues.append({"severity": "P0", "category": "input", "line": None, "excerpt": "draft file missing"})
        draft = ""
    else:
        draft = read_text(draft_path)
    if not facts_path.is_file():
        issues.append({"severity": "P0", "category": "input", "line": None, "excerpt": "fact table missing"})
        facts = ""
    else:
        facts = read_text(facts_path)

    for name, pattern in SECRET_PATTERNS.items():
        issues.extend(line_hits(draft, name, pattern, "P0"))
    issues.extend(line_hits(draft, "uuid", UUID_PATTERN, "P0"))
    issues.extend(line_hits(draft, "personal_path", PERSONAL_PATH_PATTERN, "P0"))

    for name, pattern in GENERIC_RED_LINES.items():
        severity = "P0" if name in {"meta_commentary", "publication_material"} else "P1"
        issues.extend(line_hits(draft, name, pattern, severity))
    for name, pattern in load_profile_patterns(profile_path):
        issues.extend(line_hits(draft, name, pattern, "P1"))

    draft_numbers = extract_numbers(draft)
    fact_numbers = extract_numbers(facts)
    unregistered = sorted(token for token in draft_numbers - fact_numbers if token not in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"})
    for token in unregistered:
        issues.append({"severity": "P0", "category": "unregistered_number", "line": None, "excerpt": token})

    max_em_dash = None
    if profile_path and profile_path.is_file():
        try:
            profile = json.loads(read_text(profile_path))
            rules = profile.get("negative_rules", {})
            if isinstance(rules, dict):
                max_em_dash = rules.get("max_em_dash")
        except Exception:
            pass
    if isinstance(max_em_dash, int) and draft.count("——") > max_em_dash:
        issues.append({"severity": "P1", "category": "em_dash_limit", "line": None, "excerpt": f"{draft.count('——')} > {max_em_dash}"})

    p0 = sum(1 for issue in issues if issue["severity"] == "P0")
    p1 = sum(1 for issue in issues if issue["severity"] == "P1")
    result = {
        "status": "pass" if p0 == 0 and p1 == 0 else "fail",
        "draft": str(draft_path),
        "facts": str(facts_path),
        "counts": {"P0": p0, "P1": p1},
        "unregisteredNumbers": unregistered,
        "issues": issues,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=False))
    if args.enforce and result["status"] != "pass":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
