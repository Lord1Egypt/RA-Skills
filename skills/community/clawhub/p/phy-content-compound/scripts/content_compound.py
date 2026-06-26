#!/usr/bin/env python3
"""
phy-content-compound — Content Atom Library Builder

Scans a directory of your past content (markdown, text files), extracts
reusable "content atoms" (claims, data points, anecdotes, frameworks,
contrarian takes, questions), tags each with topic keywords, and retrieves
the most relevant atoms when you need to write about a new topic.

Every post you write makes the next one easier. The library compounds.

Research basis:
- Zettelkasten: atomic notes + serendipity effect at 50-100 connected notes
- Justin Welsh: 5 styles × 5 topics = 75+ ideas; performance-graded recycling
- Content atomization: hub-and-spoke model for derivative content
- NLP extraction: text segmentation + keyword extraction + entity recognition

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


# ─── Atom types ───────────────────────────────────────────────────────

ATOM_TYPES = {
    "data_point": "Specific number, percentage, metric, or measurement",
    "claim": "Strong assertion or thesis statement",
    "anecdote": "Personal story or experience",
    "framework": "Structured list, step-by-step, or mental model",
    "contrarian": "Challenges conventional wisdom or common belief",
    "question": "Thought-provoking or discussion-driving question",
}


# ─── Extraction patterns ─────────────────────────────────────────────

DATA_POINT_RE = re.compile(
    r'[^.!?\n]*\b\d+(?:\.\d+)?[%$€£¥KkMmBbx]\b[^.!?\n]*[.!?]?'
    r'|[^.!?\n]*\b\d{2,}(?:,\d{3})*\b[^.!?\n]*[.!?]?'
)

CLAIM_STARTERS = re.compile(
    r'(?i)^(?:the (?:key|real|most important|biggest|core|main|critical|fundamental) '
    r'(?:insight|lesson|takeaway|finding|problem|issue|thing|difference)|'
    r'(?:here\'s (?:the thing|what|why)|the (?:truth|reality|secret|trick) is|'
    r'(?:this|that|it) (?:means|shows|proves|demonstrates)|'
    r'(?:turns out|it turns out|the bottom line)|'
    r'(?:nobody|everyone|most people) (?:talks|knows|realizes|understands)))'
)

ANECDOTE_STARTERS = re.compile(
    r'(?i)^(?:i (?:built|wrote|shipped|launched|tried|failed|learned|found|discovered|spent|got|made|'
    r'started|stopped|quit|switched|realized|noticed|used to|remember)|'
    r'we (?:built|shipped|launched|tried|found|discovered|spent|made|started)|'
    r'last (?:week|month|year|quarter|time|spring|summer|fall|winter)|'
    r'(?:in|back in|during) 20\d\d|'
    r'(?:when i|after i|before i|my first|my last|three|two|six|one) )'
)

CONTRARIAN_STARTERS = re.compile(
    r'(?i)^(?:stop|don\'t|never|forget|(?:here\'s )?why (?:you shouldn\'t|most|everyone is wrong)|'
    r'(?:unpopular|hot|controversial) (?:take|opinion)|'
    r'(?:the|this) (?:myth|lie|misconception|mistake)|'
    r'(?:actually|contrary to)|'
    r'(?:nobody|no one) (?:needs|wants|should|tells you)|'
    r'(?:wrong|broken|dead|overrated|overhyped))'
)

FRAMEWORK_RE = re.compile(
    r'(?:^[\s]*[-•*]\s+.+\n){3,}'
    r'|(?:^[\s]*\d+[.)]\s+.+\n){3,}',
    re.MULTILINE,
)

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "because", "but", "and", "or", "if", "while", "about",
    "this", "that", "these", "those", "it", "its", "my", "your", "his",
    "her", "our", "their", "what", "which", "who", "whom", "i", "me",
    "we", "us", "you", "he", "she", "they", "them", "up", "also", "get",
    "got", "like", "one", "two", "new", "way", "make", "much", "many",
    "well", "back", "even", "still", "thing", "things", "don't",
}


@dataclass
class ContentAtom:
    """A single reusable content building block."""
    text: str
    atom_type: str          # data_point, claim, anecdote, framework, contrarian, question
    keywords: list[str] = field(default_factory=list)
    source_file: str = ""
    line_number: int = 0
    word_count: int = 0
    engagement_hint: str = ""  # optional: high/medium/low if filename contains signal


@dataclass
class AtomLibrary:
    """Collection of extracted content atoms."""
    atoms: list[ContentAtom] = field(default_factory=list)
    files_scanned: int = 0
    total_atoms: int = 0
    type_counts: dict[str, int] = field(default_factory=dict)


# ─── Keyword extraction ──────────────────────────────────────────────

def extract_keywords(text: str, top_n: int = 5) -> list[str]:
    """Extract top keywords from text using simple TF approach."""
    words = re.findall(r'[a-z][a-z-]+', text.lower())
    # Filter stop words and very short words
    meaningful = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    counts = Counter(meaningful)
    return [w for w, _ in counts.most_common(top_n)]


def extract_context_keywords(lines: list[str], line_idx: int, window: int = 5) -> list[str]:
    """Extract keywords from surrounding context."""
    start = max(0, line_idx - window)
    end = min(len(lines), line_idx + window + 1)
    context = " ".join(lines[start:end])
    return extract_keywords(context, top_n=8)


# ─── Atom extraction ─────────────────────────────────────────────────

def _sentences(text: str) -> list[tuple[str, int]]:
    """Split into sentences with approximate line numbers."""
    lines = text.split("\n")
    results = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 10:
            continue
        # Split on sentence boundaries within a line
        sents = re.split(r'(?<=[.!?])\s+', line)
        for s in sents:
            s = s.strip()
            if len(s) > 15:
                results.append((s, i + 1))
    return results


def extract_atoms_from_text(text: str, source_file: str = "",
                            engagement_hint: str = "") -> list[ContentAtom]:
    """Extract all content atoms from a text."""
    atoms: list[ContentAtom] = []
    lines = text.split("\n")
    sentences = _sentences(text)
    seen_texts: set[str] = set()

    def _add_atom(raw_text: str, atom_type: str, line_no: int) -> None:
        cleaned = raw_text.strip()
        # Deduplicate
        norm = cleaned.lower()[:80]
        if norm in seen_texts:
            return
        if len(cleaned) < 20 or len(cleaned) > 500:
            return
        seen_texts.add(norm)

        keywords = extract_context_keywords(lines, line_no - 1)
        atoms.append(ContentAtom(
            text=cleaned,
            atom_type=atom_type,
            keywords=keywords,
            source_file=source_file,
            line_number=line_no,
            word_count=len(cleaned.split()),
            engagement_hint=engagement_hint,
        ))

    # 1. Data points (sentences with specific numbers)
    for match in DATA_POINT_RE.finditer(text):
        matched = match.group().strip()
        if len(matched) > 20:
            # Find approximate line number
            pos = match.start()
            line_no = text[:pos].count("\n") + 1
            _add_atom(matched, "data_point", line_no)

    # 2-5. Sentence-level extraction
    for sent, line_no in sentences:
        sent_stripped = sent.strip()

        # Claims
        if CLAIM_STARTERS.search(sent_stripped):
            _add_atom(sent_stripped, "claim", line_no)

        # Anecdotes
        elif ANECDOTE_STARTERS.search(sent_stripped):
            _add_atom(sent_stripped, "anecdote", line_no)

        # Contrarian takes
        elif CONTRARIAN_STARTERS.search(sent_stripped):
            _add_atom(sent_stripped, "contrarian", line_no)

        # Questions
        elif sent_stripped.endswith("?") and len(sent_stripped) > 25:
            _add_atom(sent_stripped, "question", line_no)

    # 6. Frameworks (multi-line lists)
    for match in FRAMEWORK_RE.finditer(text):
        matched = match.group().strip()
        if len(matched) > 50:
            pos = match.start()
            line_no = text[:pos].count("\n") + 1
            _add_atom(matched, "framework", line_no)

    return atoms


# ─── Directory scanning ───────────────────────────────────────────────

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


def scan_directory(directory: str) -> AtomLibrary:
    """Scan a directory for content files and extract atoms."""
    library = AtomLibrary()
    root = Path(directory)

    if not root.exists():
        return library

    # Find all .md and .txt files
    files = []
    for ext in ("*.md", "*.txt"):
        for f in root.rglob(ext):
            # Skip hidden/build dirs
            if any(part in SKIP_DIRS for part in f.parts):
                continue
            files.append(f)

    for fpath in sorted(files):
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if len(text.strip()) < 50:
            continue

        # Guess engagement hint from filename
        engagement = ""
        fname = fpath.stem.lower()
        if any(w in fname for w in ["viral", "top", "best", "hit", "popular"]):
            engagement = "high"
        elif any(w in fname for w in ["draft", "wip", "idea", "rough"]):
            engagement = "low"

        rel_path = str(fpath.relative_to(root))
        atoms = extract_atoms_from_text(text, source_file=rel_path, engagement_hint=engagement)
        library.atoms.extend(atoms)
        library.files_scanned += 1

    library.total_atoms = len(library.atoms)
    library.type_counts = dict(Counter(a.atom_type for a in library.atoms))

    return library


# ─── Topic retrieval ──────────────────────────────────────────────────

def retrieve_atoms(library: AtomLibrary, topic: str, top_n: int = 5,
                   atom_type: Optional[str] = None) -> list[tuple[ContentAtom, float]]:
    """Retrieve the most relevant atoms for a given topic."""
    topic_keywords = set(extract_keywords(topic, top_n=10))

    if not topic_keywords:
        # Fallback: use raw words
        topic_keywords = set(re.findall(r'[a-z]{4,}', topic.lower())) - STOP_WORDS

    scored: list[tuple[ContentAtom, float]] = []

    for atom in library.atoms:
        if atom_type and atom.atom_type != atom_type:
            continue

        # Keyword overlap score
        atom_kw_set = set(atom.keywords)
        overlap = len(topic_keywords & atom_kw_set)

        # Text-level keyword presence (bonus)
        atom_text_lower = atom.text.lower()
        text_hits = sum(1 for kw in topic_keywords if kw in atom_text_lower)

        # Engagement bonus
        eng_bonus = 0.0
        if atom.engagement_hint == "high":
            eng_bonus = 0.5
        elif atom.engagement_hint == "low":
            eng_bonus = -0.2

        # Final score
        score = overlap * 2.0 + text_hits * 1.5 + eng_bonus

        if score > 0:
            scored.append((atom, round(score, 1)))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# ─── Outline generator ───────────────────────────────────────────────

def generate_outline(topic: str, atoms: list[tuple[ContentAtom, float]]) -> str:
    """Generate a suggested post outline from retrieved atoms."""
    lines = [f"📝  Suggested Outline for: \"{topic}\"\n"]

    # Group atoms by type
    by_type: dict[str, list[ContentAtom]] = defaultdict(list)
    for atom, _ in atoms:
        by_type[atom.atom_type].append(atom)

    # Build outline
    lines.append("  1. HOOK:")
    if by_type.get("contrarian"):
        lines.append(f"     Use contrarian take: \"{by_type['contrarian'][0].text[:80]}...\"")
    elif by_type.get("data_point"):
        lines.append(f"     Lead with data: \"{by_type['data_point'][0].text[:80]}...\"")
    elif by_type.get("anecdote"):
        lines.append(f"     Open with story: \"{by_type['anecdote'][0].text[:80]}...\"")
    else:
        lines.append("     Start with a specific, attention-grabbing fact or question")

    lines.append("\n  2. BODY:")
    if by_type.get("claim"):
        lines.append(f"     Core argument: \"{by_type['claim'][0].text[:80]}...\"")
    if by_type.get("data_point"):
        for dp in by_type["data_point"][:2]:
            lines.append(f"     Supporting data: \"{dp.text[:80]}...\"")
    if by_type.get("framework"):
        lines.append(f"     Structure: Use framework from {by_type['framework'][0].source_file}")
    if by_type.get("anecdote") and len(by_type["anecdote"]) > 0:
        lines.append(f"     Personal proof: \"{by_type['anecdote'][0].text[:80]}...\"")

    lines.append("\n  3. CTA:")
    if by_type.get("question"):
        lines.append(f"     Close with: \"{by_type['question'][0].text[:80]}\"")
    else:
        lines.append("     End with a genuine question for your audience")

    return "\n".join(lines)


# ─── Report formatter ─────────────────────────────────────────────────

def format_library_report(library: AtomLibrary) -> str:
    """Format the atom library summary."""
    lines: list[str] = []
    w = lines.append

    w("=" * 66)
    w("  phy-content-compound — Content Atom Library")
    w("=" * 66)
    w(f"  Files scanned  : {library.files_scanned}")
    w(f"  Total atoms    : {library.total_atoms}")
    w("=" * 66)

    w("\n📊  Atoms by Type:\n")
    type_icons = {
        "data_point": "📊", "claim": "💡", "anecdote": "📖",
        "framework": "🔧", "contrarian": "🔥", "question": "❓",
    }
    for atype, count in sorted(library.type_counts.items(), key=lambda x: -x[1]):
        icon = type_icons.get(atype, "•")
        desc = ATOM_TYPES.get(atype, "")
        w(f"  {icon} {atype:<14} {count:>4} atoms  — {desc}")

    return "\n".join(lines)


def format_retrieval_report(topic: str, results: list[tuple[ContentAtom, float]],
                            outline: str) -> str:
    """Format the retrieval results."""
    lines: list[str] = []
    w = lines.append

    w(f"\n🔍  Top atoms for: \"{topic}\"\n")

    if not results:
        w("  No relevant atoms found. Try a broader topic or add more content to your library.")
        return "\n".join(lines)

    for i, (atom, score) in enumerate(results, 1):
        type_icon = {"data_point": "📊", "claim": "💡", "anecdote": "📖",
                     "framework": "🔧", "contrarian": "🔥", "question": "❓"}.get(atom.atom_type, "•")
        eng_badge = {"high": " ⭐", "low": "", "": ""}.get(atom.engagement_hint, "")

        w(f"  {i}. {type_icon} [{atom.atom_type}] (relevance: {score}){eng_badge}")
        # Wrap long text
        wrapped = textwrap.fill(atom.text, width=60, initial_indent="     ", subsequent_indent="     ")
        w(wrapped)
        w(f"     — Source: {atom.source_file}:{atom.line_number}")
        w(f"     — Keywords: {', '.join(atom.keywords[:5])}")
        w("")

    w("\n" + outline)

    return "\n".join(lines)


def format_json(library: AtomLibrary, topic: str = "",
                results: list[tuple[ContentAtom, float]] = None) -> str:
    """JSON output."""
    output = {
        "library": {
            "files_scanned": library.files_scanned,
            "total_atoms": library.total_atoms,
            "type_counts": library.type_counts,
        },
        "atoms": [
            {
                "text": a.text,
                "type": a.atom_type,
                "keywords": a.keywords,
                "source": a.source_file,
                "line": a.line_number,
                "words": a.word_count,
            }
            for a in library.atoms
        ],
    }
    if topic and results:
        output["query"] = {
            "topic": topic,
            "results": [
                {"text": a.text, "type": a.atom_type, "score": s,
                 "source": a.source_file, "keywords": a.keywords}
                for a, s in results
            ],
        }
    return json.dumps(output, indent=2)


# ─── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-content-compound: Content Atom Library Builder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              # Build library from a directory
              python3 content_compound.py ~/Desktop/content-ideas/

              # Build library + query for a topic
              python3 content_compound.py ~/Desktop/content-ideas/ --topic "developer tools"

              # Query specific atom type
              python3 content_compound.py ~/posts/ --topic "AI" --type data_point

              # JSON output
              python3 content_compound.py ~/posts/ --topic "security" --format json
        """),
    )
    parser.add_argument("directory", help="Directory of .md/.txt files to scan")
    parser.add_argument("--topic", "-t", help="Topic to retrieve atoms for")
    parser.add_argument("--type", choices=list(ATOM_TYPES.keys()),
                        help="Filter by atom type")
    parser.add_argument("--top", "-n", type=int, default=5,
                        help="Number of atoms to retrieve (default: 5)")
    parser.add_argument("--format", default="text", choices=["text", "json"],
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Build library
    library = scan_directory(args.directory)

    if library.total_atoms == 0:
        print(f"No content atoms found in {args.directory}")
        print("Make sure the directory contains .md or .txt files with substantive content.")
        sys.exit(1)

    if args.format == "json":
        results = None
        if args.topic:
            results = retrieve_atoms(library, args.topic, top_n=args.top, atom_type=args.type)
        print(format_json(library, args.topic or "", results))
    else:
        # Print library summary
        print(format_library_report(library))

        # If topic provided, retrieve and show
        if args.topic:
            results = retrieve_atoms(library, args.topic, top_n=args.top, atom_type=args.type)
            outline = generate_outline(args.topic, results)
            print(format_retrieval_report(args.topic, results, outline))


if __name__ == "__main__":
    main()
