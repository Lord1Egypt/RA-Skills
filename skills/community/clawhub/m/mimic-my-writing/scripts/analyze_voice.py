#!/usr/bin/env python3
"""
analyze_voice.py -- Extract a writing-voice fingerprint from sample text.

Usage:
    analyze_voice.py <file_or_dir> [<file_or_dir> ...]
    analyze_voice.py samples/chad/

Prints a JSON-ish report to stdout: stats, top vocab, signature moves,
quirks. Designed to be loaded into context so the model can imitate
the author. Stdlib only -- no installs.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from statistics import mean, pstdev

# --- tokenization -----------------------------------------------------------

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")
CONTRACTION_RE = re.compile(r"\b\w+'(s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PROFANITY = {
    "fuck", "fucking", "fucked", "shit", "shitty", "bullshit", "ass",
    "asshole", "damn", "damned", "hell", "bitch", "piss", "crap",
    "dick", "bastard", "goddamn", "motherfucker",
}
FILLER_AI = {
    "delve", "tapestry", "vibrant", "crucial", "comprehensive", "robust",
    "seamless", "groundbreaking", "leverage", "synergy", "transformative",
    "myriad", "cornerstone", "empower", "catalyst", "furthermore",
    "moreover", "holistic", "utilize", "facilitate", "nuanced",
    "illuminate", "encompasses", "ubiquitous", "quintessential",
}
HEDGES = {"perhaps", "maybe", "possibly", "arguably", "somewhat", "rather"}
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on",
    "at", "for", "with", "by", "from", "as", "is", "are", "was", "were",
    "be", "been", "being", "it", "its", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "our", "their", "do", "does", "did",
    "have", "has", "had", "not", "no", "yes", "so", "than", "then",
    "there", "here", "what", "which", "who", "whom", "how", "when",
    "where", "why", "will", "would", "could", "should", "can", "may",
    "might", "must", "into", "out", "up", "down", "over", "under",
    "just", "also", "any", "some", "all", "more", "most", "other",
    "such", "only", "own", "same", "too", "very", "one", "two", "now",
    "get", "got", "go", "goes", "going", "gone", "make", "made", "like",
    "about", "after", "before", "between", "through",
}

# --- loaders ----------------------------------------------------------------


def gather_files(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.is_file() and f.suffix.lower() in {".md", ".txt", ".markdown"}:
                    out.append(f)
        elif path.is_file():
            out.append(path)
    return out


def load_text(files: list[Path]) -> str:
    chunks: list[str] = []
    for f in files:
        try:
            chunks.append(f.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
    return "\n\n".join(chunks)


# --- analyzers --------------------------------------------------------------


def split_sentences(text: str) -> list[str]:
    # strip code fences and inline code so they don't poison stats
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", " ", text)
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]


def burstiness(lengths: list[int]) -> float:
    if len(lengths) < 2:
        return 0.0
    m = mean(lengths)
    if m == 0:
        return 0.0
    sd = pstdev(lengths)
    # normalized: sd/mean, capped at 2.0 for readability
    return round(min(sd / m, 2.0), 3)


def punctuation_profile(text: str) -> dict:
    total_chars = max(len(text), 1)
    return {
        "em_dash_per_1k": round(text.count("--") * 1000 / total_chars, 2),
        "ellipsis_per_1k": round(text.count("...") * 1000 / total_chars, 2),
        "exclaim_per_1k": round(text.count("!") * 1000 / total_chars, 2),
        "question_per_1k": round(text.count("?") * 1000 / total_chars, 2),
        "semicolon_per_1k": round(text.count(";") * 1000 / total_chars, 2),
        "parens_per_1k": round(text.count("(") * 1000 / total_chars, 2),
        "caps_words": len(re.findall(r"\b[A-Z]{2,}\b", text)),
    }


def caps_for_emphasis(text: str) -> list[str]:
    """ALL-CAPS words used for emphasis (excluding common acronyms)."""
    common = {"AI", "API", "CEO", "CTO", "URL", "USA", "ID", "OK", "TV", "PC", "FBI"}
    found = [w for w in re.findall(r"\b[A-Z]{2,}\b", text) if w not in common]
    return [w for w, _ in Counter(found).most_common(15)]


def signature_phrases(text: str, n: int = 3, top: int = 20) -> list[tuple[str, int]]:
    tokens = [t.lower() for t in WORD_RE.findall(text)]
    grams = [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
    # drop ones that are all stopwords
    filtered = [
        g for g in grams
        if not all(tok in STOPWORDS for tok in g.split())
    ]
    return Counter(filtered).most_common(top)


def vocab_profile(text: str) -> dict:
    tokens = [t.lower() for t in WORD_RE.findall(text)]
    counts = Counter(tokens)
    content = {w: c for w, c in counts.items() if w not in STOPWORDS and len(w) > 2}
    top_content = sorted(content.items(), key=lambda x: -x[1])[:30]
    total = max(len(tokens), 1)
    return {
        "total_words": total,
        "unique_words": len(counts),
        "type_token_ratio": round(len(counts) / total, 3),
        "top_content_words": top_content,
        "profanity_hits": sum(counts.get(w, 0) for w in PROFANITY),
        "profanity_per_1k_words": round(
            sum(counts.get(w, 0) for w in PROFANITY) * 1000 / total, 2
        ),
        "ai_filler_hits": sum(counts.get(w, 0) for w in FILLER_AI),
        "hedge_hits": sum(counts.get(w, 0) for w in HEDGES),
    }


def sentence_profile(sents: list[str]) -> dict:
    lengths = [len(WORD_RE.findall(s)) for s in sents]
    if not lengths:
        return {"sentence_count": 0}
    short = sum(1 for l in lengths if l <= 5)
    long = sum(1 for l in lengths if l >= 25)
    return {
        "sentence_count": len(lengths),
        "mean_words": round(mean(lengths), 2),
        "stdev_words": round(pstdev(lengths), 2) if len(lengths) > 1 else 0,
        "burstiness": burstiness(lengths),
        "min_words": min(lengths),
        "max_words": max(lengths),
        "fragment_share": round(short / len(lengths), 3),  # <=5 words
        "long_sentence_share": round(long / len(lengths), 3),  # >=25 words
    }


def opener_profile(sents: list[str], top: int = 10) -> list[tuple[str, int]]:
    openers = []
    for s in sents:
        m = WORD_RE.match(s.lstrip("-*>#0123456789. ").strip())
        if m:
            openers.append(m.group(0).lower())
    return Counter(openers).most_common(top)


def contraction_rate(text: str) -> float:
    words = len(WORD_RE.findall(text))
    if words == 0:
        return 0.0
    return round(len(CONTRACTION_RE.findall(text)) * 1000 / words, 2)


def quirks(text: str) -> list[str]:
    found: list[str] = []
    if re.search(r"\bfuck", text, re.IGNORECASE):
        found.append("uses 'fuck' as intensifier (not just expletive)")
    if re.search(r"--", text):
        found.append("em-dash equivalent ('--') is a structural device")
    if re.search(r"\bain't\b", text, re.IGNORECASE):
        found.append("uses 'ain't'")
    if re.search(r"\by'?all\b", text, re.IGNORECASE):
        found.append("uses 'y'all'")
    if re.search(r"\bgonna\b|\bwanna\b|\bgotta\b", text, re.IGNORECASE):
        found.append("uses spoken contractions: gonna/wanna/gotta")
    if re.search(r"\bdude\b|\bbro\b|\bman\b\s*[.,!?]", text, re.IGNORECASE):
        found.append("uses casual address: dude/bro/man")
    if text.count("--") > text.count(",") * 0.1:
        found.append("dash-driven asides instead of parentheticals")
    if re.search(r"\?\s+[A-Z][^.?!]{0,40}\.", text):
        found.append("rhetorical questions answered by self")
    if len(re.findall(r"\b[A-Z]{3,}\b", text)) > 3:
        found.append("ALL-CAPS for emphasis (not headings)")
    if re.search(r"\b(lol|lmao|wtf|af|asf)\b", text, re.IGNORECASE):
        found.append("internet shorthand (lol/af/etc)")
    return found


# --- report -----------------------------------------------------------------


def build_report(paths: list[str]) -> dict:
    files = gather_files(paths)
    if not files:
        return {"error": f"No .md/.txt files found in: {paths}"}
    text = load_text(files)
    sents = split_sentences(text)
    return {
        "source_files": [str(f) for f in files],
        "char_count": len(text),
        "sentence_stats": sentence_profile(sents),
        "vocab": vocab_profile(text),
        "punctuation": punctuation_profile(text),
        "contractions_per_1k_words": contraction_rate(text),
        "caps_for_emphasis": caps_for_emphasis(text),
        "top_sentence_openers": opener_profile(sents),
        "signature_bigrams": signature_phrases(text, n=2, top=15),
        "signature_trigrams": signature_phrases(text, n=3, top=15),
        "quirks": quirks(text),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    report = build_report(argv[1:])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
