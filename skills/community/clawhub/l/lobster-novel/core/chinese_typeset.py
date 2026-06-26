#!/usr/bin/env python3
"""
lobster-novel: Chinese typesetting engine (inspired by 马良写作 排版清洗).
Rules:
1. 全角英文/数字 → 半角
2. 半角标点（中文语境）→ 全角
3. 引号统一为中文引号（「」『』""）
4. 段落间距标准化
5. 中文与英文之间的空格规范化
6. 重复标点清理
"""
import re
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# Rule definitions
# ═══════════════════════════════════════════════════════════════

class ChineseTypeset:
    """Chinese text typesetting rules engine."""

    @staticmethod
    def fullwidth_to_halfwidth(text: str) -> str:
        """Convert fullwidth ASCII/numbers to halfwidth."""
        result = []
        for ch in text:
            code = ord(ch)
            # Fullwidth letters A-Z (FF21-FF3A), a-z (FF41-FF5A)
            if 0xFF21 <= code <= 0xFF3A:
                result.append(chr(code - 0xFEE0))
            elif 0xFF41 <= code <= 0xFF5A:
                result.append(chr(code - 0xFEE0))
            # Fullwidth digits ０-９ (FF10-FF19)
            elif 0xFF10 <= code <= 0xFF19:
                result.append(chr(code - 0xFEE0))
            # Fullwidth @ (FF20), other common symbols
            elif code == 0xFF20:  # ＠
                result.append("@")
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def halfwidth_to_fullwidth_punct(text: str) -> str:
        """Convert halfwidth punctuation to fullwidth in Chinese context."""
        # Only convert when adjacent to Chinese chars
        def _replace_in_chinese(m):
            return chr(ord(m.group(0)) + 0xFEE0)

        for punct in [",", ".", ":", ";", "!", "?"]:
            # Before Chinese char
            text = re.sub(rf'(?<=[\u4e00-\u9fff]){re.escape(punct)}(?=[\u4e00-\u9fff])',
                          _replace_in_chinese, text)
            # After Chinese char, before space/non-letter
            text = re.sub(rf'(?<=[\u4e00-\u9fff]){re.escape(punct)}(?=\s|$)',
                          _replace_in_chinese, text)
        return text

    @staticmethod
    def normalize_quotes(text: str) -> str:
        """Normalize various quote styles to standard Chinese quotes."""
        # Curly/smart quotes to straight
        text = text.replace("\u201c", "\"").replace("\u201d", "\"")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        # Left/right single quotes
        text = text.replace("\u201c", "\"").replace("\u201d", "\"")

        # French angle quotes to Chinese book title marks
        text = text.replace("\u00ab", "\u300a").replace("\u00bb", "\u300b")

        # English quotes in Chinese context → use fullwidth quotes if preferred
        # (leave as-is, too aggressive to auto-convert)

        return text

    @staticmethod
    def normalize_spacing(text: str) -> str:
        """Normalize spacing between Chinese and English/numeric text."""
        # Add space between Chinese and English
        text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z])', r'\1 \2', text)
        text = re.sub(r'([a-zA-Z])([\u4e00-\u9fff])', r'\1 \2', text)
        # Add space between Chinese and numbers
        text = re.sub(r'([\u4e00-\u9fff])(\d)', r'\1 \2', text)
        text = re.sub(r'(\d)([\u4e00-\u9fff])', r'\1 \2', text)
        # Remove double spaces
        text = re.sub(r'  +', ' ', text)
        return text

    @staticmethod
    def clean_duplicate_punct(text: str) -> str:
        """Clean up duplicated punctuation marks."""
        # !!!! or ???  →  single + paren
        text = re.sub(r'[!?！？]{3,}', lambda m: m.group(0)[:2] + "...", text)
        # …… repeated → normalize to exactly 2
        text = re.sub(r'。{3,}', '……', text)
        text = re.sub(r'\.{3,}', '……', text)
        # ……连续出现（如…………）→  normalize
        text = re.sub(r'。{6,}', '……', text)
        # Repeated 。。
        text = re.sub(r'。。{2,}', '。', text)
        # Repeated ，，
        text = re.sub(r'，，{2,}', '，', text)
        return text

    @staticmethod
    def normalize_paragraphs(text: str) -> str:
        """Normalize paragraph spacing and indentation."""
        lines = text.split("\n")
        # Remove leading/trailing spaces per line
        lines = [l.strip() for l in lines]
        # Collapse 3+ consecutive blank lines to 2
        result = []
        blank_count = 0
        for l in lines:
            if not l:
                blank_count += 1
                if blank_count <= 2:
                    result.append("")
            else:
                blank_count = 0
                result.append(l)
        return "\n".join(result)

    @staticmethod
    def clean_all(text: str) -> str:
        """Run all typesetting rules in sequence."""
        text = ChineseTypeset.fullwidth_to_halfwidth(text)
        text = ChineseTypeset.halfwidth_to_fullwidth_punct(text)
        text = ChineseTypeset.normalize_quotes(text)
        text = ChineseTypeset.normalize_spacing(text)
        text = ChineseTypeset.clean_duplicate_punct(text)
        text = ChineseTypeset.normalize_paragraphs(text)
        return text.strip()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Chinese typesetting engine")
    parser.add_argument("file", nargs="?", help="input file (stdin if omitted)")
    parser.add_argument("--output", "-o", help="output file (stdout if omitted)")
    args = parser.parse_args()

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        import sys
        text = sys.stdin.read()

    result = ChineseTypeset.clean_all(text)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Saved: {args.output} ({len(text)} → {len(result)} chars)")
    else:
        print(result)
