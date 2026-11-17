import argparse
import re
from pathlib import Path


REQUIRED_HEADINGS = [
    "需求摘要",
    "背景、目标与成功结果",
    "角色与权限边界",
    "核心业务场景与用户故事",
    "关联页面、完整路由与截图证据",
    "页面现状与目标差距",
    "目标业务流程",
    "业务规则",
    "异常与边界场景",
    "范围内",
    "范围外",
    "验收标准",
    "产品决策记录",
    "未验证事项",
    "变更记录",
]

ID_TYPES = {
    "ROLE": "role",
    "US": "user story",
    "REQ": "requirement",
    "EX": "exception",
    "AC": "acceptance criterion",
}

VAGUE_OR_PLACEHOLDER = [
    r"\bTBD\b",
    r"\bTODO\b",
    r"\bXXX\b",
    r"待补充",
    r"视情况",
    r"酌情",
    r"适当处理",
    r"正常处理",
    r"尽快",
    r"按需处理",
]


def ids(text, prefix):
    return sorted({int(value) for value in re.findall(rf"\b{prefix}-(\d{{2,}})\b", text)})


def validate_contiguous(found, label, problems):
    if not found:
        problems.append(f"no {label} IDs")
        return
    expected = list(range(1, max(found) + 1))
    if found != expected:
        problems.append(f"non-contiguous {label} IDs: found={found} expected={expected}")


def acceptance_blocks(text):
    matches = list(re.finditer(r"\bAC-\d{2,}\b", text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield match.group(0), text[match.start():end]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-status", choices=["draft", "confirmed"], required=True)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    problems = []

    for heading in REQUIRED_HEADINGS:
        if not re.search(rf"^##\s+\d*\.?\s*{re.escape(heading)}\s*$", text, re.M):
            problems.append(f"missing heading: {heading}")

    for prefix, label in ID_TYPES.items():
        validate_contiguous(ids(text, prefix), label, problems)

    for ac_id, block in acceptance_blocks(text):
        if not re.search(r"\b(?:REQ|US|EX)-\d{2,}\b", block):
            problems.append(f"{ac_id} has no REQ/US/EX reference")
        has_gwt = all(token in block for token in ("Given", "When", "Then"))
        has_chinese = all(token in block for token in ("前提", "操作", "结果"))
        if not (has_gwt or has_chinese):
            problems.append(f"{ac_id} is not Given/When/Then or 前提/操作/结果")

    if not re.search(r"https?://[^\s)>]+", text):
        problems.append("no complete URL found")
    if not re.search(r"!\[[^\]]*\]\([^\)]+\)", text) and "无法取证" not in text:
        problems.append("no screenshot/image evidence found")

    if args.expected_status == "draft":
        if "草案（待产品确认）" not in text:
            problems.append("draft status missing")
    else:
        if "已确认（可发布到飞书）" not in text:
            problems.append("confirmed status missing")
        if re.search(r"确认日期：\s*(待确认|TBD)", text):
            problems.append("confirmation date is not frozen")
        for pattern in VAGUE_OR_PLACEHOLDER:
            if re.search(pattern, text, re.I):
                problems.append(f"confirmed document contains vague/placeholder wording: {pattern}")

    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)

    counts = " ".join(f"{prefix}={len(ids(text, prefix))}" for prefix in ID_TYPES)
    print(f"OK: {args.path} | {counts} status={args.expected_status}")


if __name__ == "__main__":
    main()
