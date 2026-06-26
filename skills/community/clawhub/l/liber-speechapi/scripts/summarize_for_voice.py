from __future__ import annotations

import argparse
import re


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)]\([^)]+\)", r"\1", text)
    text = re.sub(r"^[>#\-*]+\s*", "", text, flags=re.M)
    text = re.sub(r"\|", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[。！？!?；;])", text)
    return [p.strip() for p in parts if p.strip()]


def summarize_text(text: str, limit: int = 100) -> str:
    cleaned = strip_markdown(text)
    if len(cleaned) <= limit:
        return cleaned

    sentences = split_sentences(cleaned)
    if not sentences:
        return cleaned[:limit]

    summary = ""
    for sentence in sentences:
        if len(summary + sentence) <= limit:
            summary += sentence
        else:
            break

    if not summary:
        summary = cleaned[:limit]

    return summary[:limit].rstrip("，,、；; ") + "。"


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize text for voice reply")
    parser.add_argument("text", help="Input text")
    parser.add_argument("--limit", type=int, default=100, help="Max character limit")
    args = parser.parse_args()

    print(summarize_text(args.text, args.limit))


if __name__ == "__main__":
    main()
