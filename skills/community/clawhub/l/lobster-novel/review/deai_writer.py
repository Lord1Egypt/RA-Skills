#!/usr/bin/env python3
"""
lobster-novel: De-AI rewrite engine (inspired by 马良写作 去AI味改写).
Detects AIGC patterns and rewrites them to sound more human.

Two modes:
- Static: rule-based replacement (fast, no API cost)
- LLM: rewrite via SenseNova API (better quality, cost)
"""
import re, json, os, sys, urllib.request
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

# Ensure sibling modules are importable
_review_dir = Path(__file__).parent
if str(_review_dir) not in sys.path:
    sys.path.insert(0, str(_review_dir))

from aigc_detect import AIGCDetector

# Patterns to simply remove (empty replacement)
REMOVE_PATTERNS = [
    r'只见',
    r'[，,]?就在这时[，,]?',
    r'[，,]?原来如此[，。！]?',
    r'[，,]?不得不说[，,]?',
    r'[，,]?这[一]?刻[，,]?',
    r'[，,]?就在这[一]?[刻时][，,]?',
]

# Substitution patterns (pattern → replacement)
SUBSTITUTE_PATTERNS = [
    # emotion tell → action show
    (r'他很生气', '他攥紧拳头，指节发白'),
    (r'她很高兴', '她嘴角不自觉地扬起'),
    (r'他很伤心', '他喉咙发紧，说不出话来'),
    (r'她很难过', '她眼眶发红，拼命忍着泪'),
    (r'他很紧张', '他手心全是汗'),
    (r'她松了口气', '她肩膀一松'),
    (r'他感到恐惧', '他后背一阵发凉'),
    (r'她感到恐惧', '她脸色刷地白了'),
    (r'内心充满[^。！？，,]{2,12}', '心里'),
    (r'心中涌起[^！？。，,]{2,12}', '心里'),
]


@dataclass
class RewriteResult:
    original: str = ""
    rewritten: str = ""
    changes: int = 0
    method: str = "static"  # static / llm
    details: List[str] = field(default_factory=list)

    def diff_preview(self, max_chars: int = 200) -> str:
        """Show a snippet of what changed."""
        if self.original == self.rewritten:
            return "(no changes)"
        # Find first difference
        for i in range(min(len(self.original), len(self.rewritten))):
            if self.original[i] != self.rewritten[i]:
                start = max(0, i - 20)
                preview = (f"  Before: ...{self.original[start:start+60]}...\n"
                           f"  After:  ...{self.rewritten[start:start+60]}...")
                return preview
        return f"  Length changed: {len(self.original)} → {len(self.rewritten)}"


class DeAIWriter:
    """De-AI rewrite engine."""

    @staticmethod
    def rewrite_static(text: str) -> RewriteResult:
        """Apply static rule-based rewrites (no API cost)."""
        changes = 0
        details = []
        original = text

        # Scan for hits first
        hits = AIGCDetector.scan(text)
        hit_categories = set(h["category"] for h in hits)
        if hit_categories:
            details.append(f"AIGC patterns: {', '.join(hit_categories)}")

        # Remove patterns
        for pat in REMOVE_PATTERNS:
            new_text = re.sub(pat, '', text)
            if new_text != text:
                changes += 1
                text = new_text

        # Substitute patterns
        for pat, replacement in SUBSTITUTE_PATTERNS:
            new_text = re.sub(pat, replacement, text)
            if new_text != text:
                changes += text.count(pat[:3])  # rough count
                details.append(f"replace: {pat[:20]} → {replacement[:20]}")
                text = new_text

        # Cleanup residual punctuation artifacts
        text = re.sub(r'[，,][。！？!?]', lambda m: m.group(0)[1:], text)
        text = re.sub(r'[，,]{2,}', '，', text)
        text = re.sub(r'[。!?！？]{2,}', lambda m: m.group(0)[0], text)
        # Static rewriting is best-effort. For high-quality de-AI,
        # use --llm mode (rewrite_llm) which handles sentence boundaries.

        return RewriteResult(
            original=original,
            rewritten=text,
            changes=changes,
            method="static",
            details=details,
        )

    @staticmethod
    def rewrite_llm(text: str, api_key: str = "",
                    temperature: float = 0.5) -> RewriteResult:
        """Use SenseNova API for higher-quality de-AI rewrite."""
        api_key = api_key or os.environ.get("SENSENOVA_API_KEY", "")
        if not api_key:
            return DeAIWriter.rewrite_static(text)

        hits = AIGCDetector.scan(text)
        if not hits:
            return RewriteResult(original=text, rewritten=text, changes=0,
                                 method="llm")

        hit_examples = "\n".join(
            f'- "{h["match"]}" (line {h["line"]})' for h in hits[:8])

        system = ("你是一位资深小说编辑，专门去除AI写作痕迹。"
                  "你的任务是将AI典型表达方式改写为真人作家的自然写法。"
                  "要求：1) 保持原文意思和情节 2) 去AI味但不改变风格 3) "
                  "使用show-don't-tell原则 4) 返回完整改写后的文本")
        prompt = (
            f"以下段落包含AI写作痕迹，请改写为更自然的表达：\n\n"
            f"## 检测到的AI模式\n{hit_examples}\n\n"
            f"## 原文\n{text[:6000]}\n\n"
            f"输出完整改写后的文本："
        )

        payload = json.dumps({
            "model": "sensenova-6.7-flash-lite",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": 8192,
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://token.sensenova.cn/v1/chat/completions", data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            })
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            rewritten = data["choices"][0]["message"]["content"]
            # Strip code blocks if present
            rewritten = re.sub(r'^```[\w]*\n', '', rewritten)
            rewritten = re.sub(r'\n```$', '', rewritten)
            return RewriteResult(
                original=text, rewritten=rewritten.strip(),
                changes=len(hits), method="llm",
                details=[f"LLM rewrite: {len(hits)} patterns addressed"])
        except Exception as e:
            return RewriteResult(
                original=text, rewritten=text, changes=0,
                method="llm", details=[f"LLM failed: {str(e)[:60]}"])

    @classmethod
    def rewrite(cls, text: str, api_key: str = "",
                use_llm: bool = False) -> RewriteResult:
        """Auto-select best rewrite method."""
        if use_llm and os.environ.get("SENSENOVA_API_KEY"):
            return cls.rewrite_llm(text, api_key)
        return cls.rewrite_static(text)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="de-AI rewrite")
    parser.add_argument("file", help="chapter file to rewrite")
    parser.add_argument("--output", "-o", help="output file")
    parser.add_argument("--llm", action="store_true", help="use LLM rewrite")
    args = parser.parse_args()

    text = Path(args.file).read_text(encoding="utf-8")
    result = DeAIWriter.rewrite(text, use_llm=args.llm)

    print(f"Method: {result.method}")
    print(f"Changes: {result.changes}")
    print(f"Length: {len(result.original)} → {len(result.rewritten)} chars")
    print()
    if result.details:
        for d in result.details:
            print(f"  - {d}")
    print()
    print(result.diff_preview())

    if args.output:
        Path(args.output).write_text(result.rewritten, encoding="utf-8")
        print(f"\nSaved: {args.output}")
