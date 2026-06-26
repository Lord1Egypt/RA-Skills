#!/usr/bin/env python3
"""Semantic PDF highlighter for academic papers.

The script first pre-reads the whole PDF, scores reusable sentences with a
small stable label set, and only then adds highlights to the output PDF.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

try:
    import fitz  # type: ignore
except ImportError:
    fitz = None


COLOR_PALETTE: Dict[str, Tuple[float, float, float]] = {
    "goal": (0.99, 0.92, 0.55),
    "motivation": (0.98, 0.75, 0.45),
    "method": (0.58, 0.78, 0.97),
    "contribution": (0.98, 0.72, 0.83),
    "result": (0.61, 0.84, 0.60),
    "definitions": (0.76, 0.69, 0.95),
    "limitations": (0.78, 0.78, 0.78),
}

OPACITY = {
    "light": 0.50,
    "dark": 0.72,
}

CATEGORY_LABELS = {
    "goal": "goal",
    "motivation": "motivation",
    "method": "method",
    "contribution": "contribution",
    "result": "result",
    "definitions": "definitions",
    "limitations": "limitations",
}

CATEGORY_PRIORITY = {
    "contribution": 0,
    "method": 1,
    "result": 2,
    "goal": 3,
    "motivation": 4,
    "definitions": 5,
    "limitations": 6,
}

CORE_CATEGORIES = ("goal", "motivation", "method", "contribution", "result")
OPTIONAL_CATEGORIES = ("definitions", "limitations")

BASE_CATEGORY_CAPS = {
    "goal": 7,
    "motivation": 9,
    "method": 20,
    "contribution": 7,
    "result": 13,
    "definitions": 7,
    "limitations": 5,
}

LEVEL_PROFILES = {
    "low": {
        "max_per_page": 14,
        "max_total": 90,
        "min_score": 2.15,
        "max_per_block": 4,
        "category_scale": 2.4,
        "target_multiplier": 1.0,
        "score_bonus": 0.0,
        "allow_heuristic_fallback": False,
    },
    "medium": {
        "max_per_page": 16,
        "max_total": 110,
        "min_score": 1.95,
        "max_per_block": 5,
        "category_scale": 3.0,
        "target_multiplier": 1.25,
        "score_bonus": 0.2,
        "allow_heuristic_fallback": True,
    },
    "high": {
        "max_per_page": 18,
        "max_total": 130,
        "min_score": 1.75,
        "max_per_block": 6,
        "category_scale": 3.6,
        "target_multiplier": 1.5,
        "score_bonus": 0.4,
        "allow_heuristic_fallback": True,
    },
    "extreme": {
        "max_per_page": 20,
        "max_total": 150,
        "min_score": 1.55,
        "max_per_block": 7,
        "category_scale": 4.4,
        "target_multiplier": 2.0,
        "score_bonus": 0.7,
        "allow_heuristic_fallback": True,
    },
}

NOTE_MODE_ALIASES = {
    "default": "flow",
    "flow": "flow",
    "none": "none",
}

NOTE_MODE_CONFIG = {
    "none": {
        "add_tldr": False,
        "add_section_flow": False,
        "section_items": 0,
    },
    "flow": {
        "add_tldr": True,
        "add_section_flow": True,
        "section_items": 3,
    },
    "default": {
        "add_tldr": True,
        "add_section_flow": True,
        "section_items": 3,
    },
    "full": {
        "add_tldr": True,
        "add_section_flow": True,
        "section_items": 4,
    },
}

HEADING_MAP = {
    "abstract": "abstract",
    "introduction": "introduction",
    "related work": "related work",
    "background": "background",
    "preliminary": "background",
    "preliminaries": "background",
    "method": "method",
    "methods": "method",
    "approach": "method",
    "approaches": "method",
    "framework": "method",
    "experiments": "experiments",
    "experimental setup": "experiments",
    "experimental results": "experiments",
    "implementation details": "experiments",
    "results": "experiments",
    "analysis": "experiments",
    "discussion": "discussion",
    "limitations": "limitations",
    "limitation": "limitations",
    "conclusion": "conclusion",
    "conclusions": "conclusion",
    "future work": "limitations",
    "references": "references",
    "acknowledgements": "acknowledgements",
    "acknowledgments": "acknowledgements",
    "appendix": "appendix",
    "appendices": "appendix",
    "supplementary material": "appendix",
    "supplemental material": "appendix",
}

SECTION_BIAS = {
    "goal": {"abstract": 1.0, "introduction": 1.0, "conclusion": 0.4},
    "motivation": {"abstract": 0.7, "introduction": 1.2, "related work": 0.9},
    "method": {"abstract": 0.6, "introduction": 0.4, "method": 1.2},
    "contribution": {"abstract": 0.8, "introduction": 1.2, "method": 0.3},
    "result": {"abstract": 0.9, "experiments": 1.2, "conclusion": 1.0},
    "definitions": {"method": 1.0, "experiments": 0.4, "background": 0.6},
    "limitations": {"experiments": 0.6, "discussion": 1.0, "limitations": 1.2, "conclusion": 0.8},
}

GENERIC_BACKGROUND_PATTERNS = [
    re.compile(r"^(deep learning|machine learning|artificial intelligence)\b"),
    re.compile(r"^(in recent years|recent years have seen)\b"),
    re.compile(r"^(many|numerous|various|several)\s+(studies|works|approaches|methods)\b"),
    re.compile(r"^it is well known that\b"),
]

NON_REUSABLE_PATTERNS = [
    re.compile(r"^\s*(figure|table|appendix)\b"),
    re.compile(r"^\s*(see|refer to)\b"),
    re.compile(r"\bthe rest of this paper\b"),
    re.compile(r"\bmore details? (?:are|is) (?:shown|provided)\b"),
    re.compile(r"\bdue to space limitations\b"),
    re.compile(r"\bequal contribution\b"),
    re.compile(r"\bresearch intern\b"),
    re.compile(r"\bwork done as\b"),
    re.compile(r"\barxiv:\d"),
    re.compile(r"\bhttps?://"),
]

SKIP_SECTIONS = {"front matter", "references", "appendix", "acknowledgements"}

WEAK_METHOD_PATTERN = re.compile(
    r"\b(use|uses|using|adopt|adopts|adopting|apply|applies|applying|concatenate|concatenates|project|projects|conditioning|sample|sampling|train|training|fine-?tun|pre-?train|tokeni[sz]|reconstruct|reconstruction|encode|encoder|decode|decoder|mask|leverag|utili[sz]e|scale)\b"
)
WEAK_RESULT_PATTERN = re.compile(
    r"\b(achiev|improv|outperform|better|higher|lower|quality|score|fid|throughput|benchmark|comparable|effective|consistent|gain|significant|performance)\b"
)
WEAK_MOTIVATION_PATTERN = re.compile(
    r"\b(challenge|difficult|insufficient|limited|resource|cost|private data|reproduc|noisy|gap|limitation)\b"
)
WEAK_GOAL_PATTERN = re.compile(
    r"\b(aim|goal|study|investigate|objective|task|problem|focus)\b"
)
WEAK_CONTRIBUTION_PATTERN = re.compile(
    r"\b(release|open-weight|open data|open-data|first|novel)\b"
)

CATEGORY_PATTERNS: Dict[str, Sequence[Tuple[re.Pattern[str], float, str]]] = {
    "goal": (
        (re.compile(r"\bwe (?:study|investigate|consider|address|focus on|aim to|target)\b"), 2.6, "goal verb"),
        (re.compile(r"\bthis paper (?:studies|investigates|considers|addresses|focuses on)\b"), 2.6, "paper goal"),
        (re.compile(r"\bcan we (?:develop|build|design|create)\b"), 2.5, "research question"),
        (re.compile(r"\bour goal is to\b"), 2.5, "explicit goal"),
        (re.compile(r"\btask\b|\bproblem\b|\bobjective\b|\bsetting\b"), 0.9, "task framing"),
        (re.compile(r"\binput\b.{0,40}\boutput\b"), 1.2, "input output setup"),
    ),
    "motivation": (
        (re.compile(r"\bhowever\b|\bunfortunately\b|\bnevertheless\b"), 0.7, "contrast cue"),
        (re.compile(r"\b(existing|prior|previous)\s+(methods?|work|approaches?)\b"), 1.7, "prior work"),
        (re.compile(r"\b(limitation|challenge|gap|bottleneck|trade-off|tradeoff|insufficient|hard|difficult)\b"), 1.6, "motivation claim"),
        (re.compile(r"\bfail(?:s|ed)? to\b|\bstruggle(?:s|d)? to\b"), 1.6, "failure of prior work"),
        (re.compile(r"\bmotivat(?:e|ion)\b"), 1.1, "motivation cue"),
    ),
    "method": (
        (re.compile(r"\bwe (?:propose|introduce|present|develop|design)\b"), 3.0, "proposal verb"),
        (re.compile(r"\bour (?:method|approach|framework|model|pipeline)\b"), 2.0, "method noun"),
        (re.compile(r"\bconsists of\b|\bcomposed of\b"), 1.2, "structure"),
        (re.compile(r"\bmodule\b|\barchitecture\b|\bobjective\b|\bloss\b|\btraining\b|\binference\b"), 1.0, "method mechanism"),
        (re.compile(r"\bregulari[sz]ation\b|\bguidance\b|\bdecoder\b|\bencoder\b"), 1.0, "technical mechanism"),
    ),
    "contribution": (
        (re.compile(r"\bcontributions?\b"), 3.1, "contribution cue"),
        (re.compile(r"\bnovel(?:ty)?\b|\bnew\b"), 1.2, "novelty wording"),
        (re.compile(r"\bdifferent from\b|\bunlike (?:prior|previous)\b"), 2.0, "difference from prior work"),
        (re.compile(r"\bwe are the first to\b"), 2.4, "first claim"),
        (re.compile(r"\bmain contribution\b"), 2.8, "main contribution"),
    ),
    "result": (
        (re.compile(r"\bresults? show\b|\bexperiments? demonstrate\b"), 3.0, "result statement"),
        (re.compile(r"\bwe conclude\b|\bwe find that\b"), 2.6, "conclusion cue"),
        (re.compile(r"\boutperform(?:s|ed)?\b|\bachiev(?:e|es|ed)\b|\bimprov(?:e|es|ed)\b"), 1.6, "performance claim"),
        (re.compile(r"\bstate[- ]of[- ]the[- ]art\b|\bsota\b"), 1.4, "benchmark claim"),
        (re.compile(r"\btakeaway\b"), 1.2, "takeaway cue"),
    ),
    "definitions": (
        (re.compile(r"\bwe define\b|\bdenote\b|\bassume\b|\blet\b"), 2.8, "formal definition"),
        (re.compile(r"\bnotation\b|\bprotocol\b|\bmetric\b"), 1.5, "formal setup"),
        (re.compile(r"\bevaluation setup\b|\bproblem formulation\b"), 2.0, "setup summary"),
        (re.compile(r"\bunder this setting\b|\bin this setting\b"), 1.2, "setting"),
    ),
    "limitations": (
        (re.compile(r"\blimitation(?:s)?\b|\bcaveat(?:s)?\b"), 3.0, "limitations cue"),
        (re.compile(r"\bfailure case(?:s)?\b|\bfuture work\b"), 2.6, "scope boundary"),
        (re.compile(r"\bdoes not\b|\bdo not\b|\bcannot\b|\bcan not\b"), 1.0, "boundary statement"),
        (re.compile(r"\bnot handle\b|\bremain(?:s|ed)? open\b"), 1.8, "open problem"),
        (re.compile(r"\bwe leave\b.{0,40}\bfuture work\b"), 2.3, "future work"),
    ),
}


@dataclass
class WordInfo:
    text: str
    rect: "fitz.Rect"
    block_no: int
    line_no: int
    word_no: int


@dataclass
class LogicalToken:
    surface: str
    normalized: str
    word_indices: List[int]


@dataclass
class BlockInfo:
    page_index: int
    block_no: int
    section: str
    bbox: "fitz.Rect"
    line_texts: List[str]
    words: List[WordInfo]
    logical_tokens: List[LogicalToken]
    text: str


@dataclass
class HeadingInfo:
    page_index: int
    section: str
    text: str
    bbox: "fitz.Rect"


@dataclass
class TitleInfo:
    page_index: int
    text: str
    bbox: "fitz.Rect"


@dataclass
class Candidate:
    page_index: int
    block_no: int
    section: str
    text: str
    category: str
    score: float
    reasons: List[str]
    word_ranges: List[Tuple[int, int]]
    block: BlockInfo = field(repr=False)

    @property
    def normalized_text(self) -> str:
        return normalize_space(self.text.lower())


@dataclass
class NoteItem:
    page_index: int
    point: "fitz.Point"
    text: str
    kind: str
    icon: str
    color: Tuple[float, float, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Pre-read an academic PDF, score reusable sentences, and add "
            "semantic highlights with a stable color legend."
        )
    )
    parser.add_argument("input_pdf", help="Input paper PDF path")
    parser.add_argument(
        "-o",
        "--output",
        help="Output highlighted PDF path. Default: <input>.highlighted.pdf",
    )
    parser.add_argument(
        "--opacity",
        choices=sorted(OPACITY),
        default="light",
        help="Highlight opacity preset. Default: light",
    )
    parser.add_argument(
        "--highlight-level",
        choices=tuple(LEVEL_PROFILES),
        default="medium",
        help="Highlight density preset. Default: medium",
    )
    parser.add_argument(
        "--note-mode",
        choices=tuple(NOTE_MODE_ALIASES),
        default="default",
        help="Explanation-layer note mode. Default: default",
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="Enable optional colors for definitions and limitations",
    )
    parser.add_argument(
        "--disable-optional",
        nargs="*",
        choices=sorted(OPTIONAL_CATEGORIES),
        default=[],
        help="Disable specific optional categories after --include-optional",
    )
    parser.add_argument(
        "--max-per-page",
        type=int,
        help="Soft cap for highlights per page. Overrides --highlight-level",
    )
    parser.add_argument(
        "--max-total",
        type=int,
        help="Global cap for highlights. Overrides --highlight-level",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        help="Minimum category score required for a sentence to be eligible. Overrides --highlight-level",
    )
    parser.add_argument(
        "--report-json",
        help="Write the selected highlight plan to this JSON file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and print the highlight plan without writing a PDF",
    )
    return parser.parse_args()


def require_fitz() -> None:
    if fitz is None:
        raise SystemExit(
            "PyMuPDF is not installed. Install it with: python3 -m pip install pymupdf"
        )


def resolve_level_settings(args: argparse.Namespace) -> argparse.Namespace:
    profile = LEVEL_PROFILES[args.highlight_level]
    args.note_mode = NOTE_MODE_ALIASES[args.note_mode]
    args.max_per_page = args.max_per_page if args.max_per_page is not None else profile["max_per_page"]
    args.max_total = args.max_total if args.max_total is not None else profile["max_total"]
    args.min_score = args.min_score if args.min_score is not None else profile["min_score"]
    args.max_per_block = profile["max_per_block"]
    args.category_scale = profile["category_scale"]
    args.target_multiplier = profile["target_multiplier"]
    args.score_bonus = profile["score_bonus"]
    args.allow_heuristic_fallback = profile["allow_heuristic_fallback"]
    return args


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_token(token: str) -> str:
    token = token.lower()
    token = re.sub(r"^[^a-z0-9]+|[^a-z0-9]+$", "", token)
    return token


def tokenize_for_match(text: str) -> List[str]:
    return [tok for tok in (normalize_token(piece) for piece in text.split()) if tok]


def sentence_split(text: str) -> List[str]:
    compact = normalize_space(text)
    if not compact:
        return []
    if compact.count(".") + compact.count("!") + compact.count("?") == 0:
        return [compact] if len(compact.split()) >= 5 else []
    parts = re.split(r"(?<=[.!?])\s+(?=(?:[A-Z0-9(\"\']))", compact)
    results = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(part.split()) < 5:
            continue
        results.append(part)
    return results


def heading_key(line: str) -> Optional[str]:
    compact = normalize_space(line).strip(":. ")
    lowered = compact.lower()
    if lowered.startswith("appendix"):
        return "appendix"
    if lowered in HEADING_MAP:
        return HEADING_MAP[lowered]
    numbered = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", lowered)
    if numbered in HEADING_MAP:
        return HEADING_MAP[numbered]
    roman = re.sub(r"^[ivxlcdm]+\.\s+", "", numbered)
    if roman in HEADING_MAP:
        return HEADING_MAP[roman]
    if re.match(r"^[a-z]\.\s+[a-z]", lowered):
        return "appendix"
    return None


def extract_blocks(doc: "fitz.Document") -> List[BlockInfo]:
    blocks: List[BlockInfo] = []
    current_section = "front matter"

    for page_index, page in enumerate(doc):
        words_raw = page.get_text("words")
        words_raw.sort(key=lambda item: (item[5], item[6], item[7]))
        grouped: Dict[int, List[WordInfo]] = defaultdict(list)
        lines: Dict[Tuple[int, int], List[WordInfo]] = defaultdict(list)

        for item in words_raw:
            word = WordInfo(
                text=str(item[4]),
                rect=fitz.Rect(item[:4]),
                block_no=int(item[5]),
                line_no=int(item[6]),
                word_no=int(item[7]),
            )
            grouped[word.block_no].append(word)
            lines[(word.block_no, word.line_no)].append(word)

        line_text_lookup: Dict[int, List[str]] = defaultdict(list)
        line_bbox_lookup: Dict[int, List[Tuple[float, "fitz.Rect", str]]] = defaultdict(list)
        for (block_no, line_no), line_words in sorted(lines.items()):
            line_words.sort(key=lambda item: item.word_no)
            text = " ".join(word.text for word in line_words).strip()
            if text:
                line_text_lookup[block_no].append(text)
                bbox = fitz.Rect(line_words[0].rect)
                for word in line_words[1:]:
                    bbox |= word.rect
                line_bbox_lookup[block_no].append((bbox.y0, bbox, text))

        block_bboxes: Dict[int, "fitz.Rect"] = {}
        page_headings: List[Tuple[float, str]] = []
        for block_no, block_words in grouped.items():
            bbox = fitz.Rect(block_words[0].rect)
            for word in block_words[1:]:
                bbox |= word.rect
            block_bboxes[block_no] = bbox
            for _y0, bbox_line, text in line_bbox_lookup.get(block_no, []):
                if len(text.split()) <= 12:
                    section = heading_key(text)
                    if section:
                        page_headings.append((bbox_line.y0, section))

        page_headings.sort(key=lambda item: item[0])

        for block_no in sorted(grouped, key=lambda value: (block_bboxes[value].y0, block_bboxes[value].x0)):
            block_words = grouped[block_no]
            line_texts = line_text_lookup.get(block_no, [])
            if any(heading_key(line) for line in line_texts if len(line.split()) <= 12):
                for line in line_texts:
                    section = heading_key(line)
                    if section:
                        current_section = section
                        break
                continue

            logical_tokens = build_logical_tokens(block_words)
            text = normalize_space(" ".join(token.surface for token in logical_tokens))
            if not text:
                continue

            section = current_section
            block_y = block_bboxes[block_no].y0
            for heading_y, heading in page_headings:
                if heading_y <= block_y + 2:
                    section = heading
                else:
                    break

            blocks.append(
                BlockInfo(
                    page_index=page_index,
                    block_no=block_no,
                    section=section,
                    bbox=block_bboxes[block_no],
                    line_texts=line_texts,
                    words=block_words,
                    logical_tokens=logical_tokens,
                    text=text,
                )
            )

        if page_headings:
            current_section = page_headings[-1][1]

    return blocks


def extract_outline(doc: "fitz.Document") -> Tuple[Optional[TitleInfo], List[HeadingInfo]]:
    headings: List[HeadingInfo] = []
    title_info: Optional[TitleInfo] = None

    for page_index, page in enumerate(doc):
        words_raw = page.get_text("words")
        words_raw.sort(key=lambda item: (item[5], item[6], item[7], item[0]))
        lines: Dict[Tuple[int, int], List[Tuple[float, float, float, float, str]]] = defaultdict(list)
        for x0, y0, x1, y1, text, block_no, line_no, word_no in words_raw:
            del word_no
            lines[(int(block_no), int(line_no))].append((x0, y0, x1, y1, str(text)))

        line_entries: List[Tuple["fitz.Rect", str]] = []
        for (_block_no, _line_no), items in sorted(lines.items(), key=lambda item: (item[0][0], item[0][1])):
            items.sort(key=lambda value: value[0])
            text = " ".join(value[4] for value in items).strip()
            if not text:
                continue
            bbox = fitz.Rect(items[0][:4])
            for value in items[1:]:
                bbox |= fitz.Rect(value[:4])
            line_entries.append((bbox, text))

        line_entries.sort(key=lambda item: (item[0].y0, item[0].x0))

        for bbox, text in line_entries:
            if len(text.split()) > 12:
                continue
            section = heading_key(text)
            if section:
                headings.append(HeadingInfo(page_index=page_index, section=section, text=text, bbox=bbox))

        if page_index == 0:
            first_heading_y = min(
                (heading.bbox.y0 for heading in headings if heading.page_index == 0),
                default=page.rect.height * 0.35,
            )
            title_lines: List[Tuple["fitz.Rect", str]] = []
            for bbox, text in line_entries:
                if bbox.y0 >= first_heading_y - 6:
                    break
                if re.search(r"https?://|arxiv:|^\d+\s", text.lower()):
                    continue
                if bbox.width < page.rect.width * 0.35 and len(text) < 28:
                    continue
                title_lines.append((bbox, text))
                if len(title_lines) == 2:
                    break

            if title_lines:
                title_bbox = fitz.Rect(title_lines[0][0])
                for bbox, _ in title_lines[1:]:
                    title_bbox |= bbox
                title_text = " ".join(text for _, text in title_lines)
            else:
                title_bbox = fitz.Rect(24, 24, min(page.rect.width - 24, 220), 72)
                title_text = input_path_name_fallback(doc)

            title_info = TitleInfo(page_index=0, text=normalize_space(title_text), bbox=title_bbox)

    return title_info, headings


def input_path_name_fallback(doc: "fitz.Document") -> str:
    name = getattr(doc, "name", "") or "Paper"
    return Path(str(name)).stem.replace("_", " ")


INLINE_CITATION_PATTERN = re.compile(r"\[[0-9,\-\s]+\]|\([A-Z][A-Za-z\-]+(?: et al\.)?, \d{4}\)")
CONTRIBUTION_NOTE_PATTERN = re.compile(
    r"\b(contributions?|novel(?:ty)?|first study|first work|to the best of our knowledge|different from|unlike prior|unlike previous|open-?weight|open data)\b"
)

NOTE_USE_PHRASES = {
    "goal": "remember the paper's core research goal and task setup",
    "motivation": "explain why the problem matters or where prior work falls short",
    "method": "reconstruct the method's main mechanism when revisiting the paper",
    "contribution": "state the paper's novelty claim in related work or review notes",
    "result": "remember the main empirical takeaway or conclusion",
    "definitions": "recover the key definition, assumption, or evaluation setup",
    "limitations": "remember the method's boundary, caveat, or future-work direction",
}

SECTION_TOPIC_LABELS = {
    "goal": "the research goal",
    "motivation": "the motivation",
    "method": "the method",
    "contribution": "the contribution",
    "result": "the results",
    "definitions": "the setup",
    "limitations": "the limitations",
}


def ensure_sentence(text: str) -> str:
    text = normalize_space(text)
    if not text:
        return ""
    if text[-1] not in ".!?":
        return f"{text}."
    return text


def clean_note_source_text(text: str) -> str:
    text = INLINE_CITATION_PATTERN.sub("", text)
    text = normalize_space(text)
    return text.strip(" -;:,")


NOTE_REWRITE_RULES = [
    (re.compile(r"\bstate-ofthe-art\b", re.IGNORECASE), "state-of-the-art"),
    (re.compile(r"^however,\s*", re.IGNORECASE), ""),
    (re.compile(r"^moreover,\s*", re.IGNORECASE), ""),
    (re.compile(r"^additionally,\s*", re.IGNORECASE), ""),
    (re.compile(r"^for example,\s*", re.IGNORECASE), ""),
    (re.compile(r"^to the best of our knowledge,\s*", re.IGNORECASE), "The authors claim that "),
    (re.compile(r"^in contrast to [^,]+,\s*we find that\s*", re.IGNORECASE), ""),
    (re.compile(r"^results? show\s*", re.IGNORECASE), "The experiments suggest "),
    (re.compile(r"^experiments? demonstrate\s*", re.IGNORECASE), "The experiments show "),
    (re.compile(r"^we find that\s*", re.IGNORECASE), ""),
    (re.compile(r"^we conclude that\s*", re.IGNORECASE), ""),
    (re.compile(r"^to [^,]{0,140},\s*we propose\s*", re.IGNORECASE), "The paper proposes "),
    (re.compile(r"^to [^,]{0,140},\s*we introduce\s*", re.IGNORECASE), "The paper introduces "),
    (re.compile(r"^to [^,]{0,140},\s*we present\s*", re.IGNORECASE), "The paper presents "),
    (re.compile(r"^to [^,]{0,140},\s*we develop\s*", re.IGNORECASE), "The paper develops "),
    (re.compile(r"^to [^,]{0,140},\s*we design\s*", re.IGNORECASE), "The paper designs "),
    (re.compile(r"^we also propose\s*", re.IGNORECASE), "The paper also proposes "),
    (re.compile(r"^we also presented\s*", re.IGNORECASE), "The paper also presents "),
    (re.compile(r"^we propose to\s*", re.IGNORECASE), "The paper proposes to "),
    (re.compile(r"^we propose\s*", re.IGNORECASE), "The paper proposes "),
    (re.compile(r"^we introduce\s*", re.IGNORECASE), "The paper introduces "),
    (re.compile(r"^we present\s*", re.IGNORECASE), "The paper presents "),
    (re.compile(r"^we develop\s*", re.IGNORECASE), "The paper develops "),
    (re.compile(r"^we design\s*", re.IGNORECASE), "The paper designs "),
    (re.compile(r"^we consider\s*", re.IGNORECASE), "The paper studies "),
    (re.compile(r"^we study\s*", re.IGNORECASE), "The paper studies "),
    (re.compile(r"^we investigate\s*", re.IGNORECASE), "The paper investigates "),
    (re.compile(r"^the present study\s*", re.IGNORECASE), "The paper "),
]


def shorten_note_text(text: str, max_words: int) -> str:
    cleaned = clean_note_source_text(text)
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned
    for delimiter in [",", ";", " which ", " that ", " especially ", " while "]:
        if delimiter not in cleaned:
            continue
        head = cleaned.split(delimiter, 1)[0].strip(" ,;:")
        head_words = head.split()
        if 8 <= len(head_words) <= max_words:
            return head
    clipped = words[:max_words]
    while clipped and clipped[-1].lower() in {
        "a",
        "an",
        "and",
        "at",
        "by",
        "for",
        "from",
        "in",
        "is",
        "of",
        "on",
        "or",
        "that",
        "the",
        "to",
        "with",
    }:
        clipped.pop()
    return " ".join(clipped).rstrip(" ,;:") + "..."


def rewrite_note_text(text: str, max_words: int) -> str:
    text = clean_note_source_text(text)
    for pattern, replacement in NOTE_REWRITE_RULES:
        text = pattern.sub(replacement, text)
    text = normalize_space(text)
    text = re.sub(r"\bthus\b", "therefore", text, flags=re.IGNORECASE)
    text = re.sub(r"\bleads to slow inference\b", "keeps inference slow", text, flags=re.IGNORECASE)
    text = re.sub(r"\bleads to\b", "causes", text, flags=re.IGNORECASE)
    text = re.sub(r"\bis crucial for\b", "is important for", text, flags=re.IGNORECASE)
    text = re.sub(r"^(also shown is|shown is)\s+", "", text, flags=re.IGNORECASE)
    text = text.strip(" -;:,")
    return shorten_note_text(text, max_words)


def lower_first(text: str) -> str:
    for index, char in enumerate(text):
        if char.isalpha():
            if char.isupper() and (index + 1 >= len(text) or text[index + 1].islower()):
                return text[:index] + char.lower() + text[index + 1 :]
            return text
    return text


def to_embedded_clause(text: str) -> str:
    text = normalize_space(text).rstrip(".!?")
    return lower_first(text)


def note_summary_fragment(candidate: Candidate, max_words: int = 18) -> str:
    summary = candidate_note_sentence(candidate, max_words).rstrip(".!?")
    prefixes = [
        "The paper's main goal is ",
        "The paper is motivated by the fact that ",
        "The core method is ",
        "The main contribution is ",
        "The main result is ",
        "The key setup here is ",
        "The main limitation here is ",
    ]
    for prefix in prefixes:
        if summary.lower().startswith(prefix.lower()):
            summary = summary[len(prefix) :]
            break
    return lower_first(summary)


def candidate_note_sentence(candidate: Candidate, max_words: int = 24) -> str:
    summary = rewrite_note_text(candidate.text, max_words)
    if not summary:
        summary = "the paper makes a reusable claim here"

    if candidate.category == "goal":
        if summary.lower().startswith(("the paper ", "this paper ", "the authors claim that")):
            return ensure_sentence(summary)
        return ensure_sentence(f"The paper's main goal is {lower_first(summary)}")

    if candidate.category == "motivation":
        summary = re.sub(r"^(the paper|this paper)\s+", "", summary, flags=re.IGNORECASE)
        return ensure_sentence(f"The paper is motivated by the fact that {lower_first(summary)}")

    if candidate.category == "method":
        if summary.lower().startswith(("the paper ", "the method ")):
            return ensure_sentence(summary)
        return ensure_sentence(f"The core method is {lower_first(summary)}")

    if candidate.category == "contribution":
        summary = re.sub(r"^(the authors claim that|the paper)\s+", "", summary, flags=re.IGNORECASE)
        return ensure_sentence(f"The main contribution is {lower_first(summary)}")

    if candidate.category == "result":
        summary = re.sub(r"^(the experiments (?:suggest|show)\s+)", "", summary, flags=re.IGNORECASE)
        return ensure_sentence(f"The main result is {lower_first(summary)}")

    if candidate.category == "definitions":
        summary = re.sub(r"^(the paper|this paper)\s+", "", summary, flags=re.IGNORECASE)
        return ensure_sentence(f"The key setup here is {lower_first(summary)}")

    summary = re.sub(r"^(the paper|this paper)\s+", "", summary, flags=re.IGNORECASE)
    return ensure_sentence(f"The main limitation here is {lower_first(summary)}")


def note_fitness(candidate: Candidate) -> float:
    lower = candidate.text.lower()
    bonus = 0.0
    word_count = len(candidate.text.split())
    digit_count = sum(ch.isdigit() for ch in candidate.text)
    symbol_count = sum(ch in "{}[]=<>/" for ch in candidate.text)

    if 10 <= word_count <= 32:
        bonus += 0.5
    if word_count > 40:
        bonus -= 0.5
    if digit_count >= 4:
        bonus -= 0.5
    if symbol_count >= 2:
        bonus -= 0.8
    if INLINE_CITATION_PATTERN.search(candidate.text):
        bonus -= 0.25

    if candidate.category == "motivation" and re.search(
        r"\b(however|prior|previous|existing|slow inference|computational demands|challenge|limitation|bottleneck|trade-?off|cost)\b",
        lower,
    ):
        bonus += 1.0
    if candidate.category == "goal" and re.search(
        r"\b(we (?:study|address|aim|focus|target|tackle)|this paper|the present study)\b",
        lower,
    ):
        bonus += 0.8
    if candidate.category == "method" and re.search(
        r"\b(we (?:propose|introduce|present|develop|design)|our (?:method|approach|framework|model))\b",
        lower,
    ):
        bonus += 0.9
    if candidate.category == "result" and re.search(
        r"\b(results? show|we find|outperform|improv|competitive performance|state[- ]of[- ]the[- ]art)\b",
        lower,
    ):
        bonus += 0.8
    if candidate.category == "contribution" or CONTRIBUTION_NOTE_PATTERN.search(lower):
        bonus += 1.1

    return candidate.score + bonus


def top_candidates(
    candidates: Sequence[Candidate],
    limit: int,
    *,
    categories: Optional[Sequence[str]] = None,
    exclude: Optional[set[str]] = None,
) -> List[Candidate]:
    allowed = set(categories) if categories else None
    seen = set(exclude or set())
    picked: List[Candidate] = []
    for item in sorted(
        candidates,
        key=lambda entry: (-note_fitness(entry), -entry.score, entry.page_index, CATEGORY_PRIORITY[entry.category]),
    ):
        if allowed is not None and item.category not in allowed:
            continue
        if item.normalized_text in seen:
            continue
        seen.add(item.normalized_text)
        picked.append(item)
        if len(picked) >= limit:
            break
    return picked


def human_join(parts: Sequence[str]) -> str:
    values = [part for part in parts if part]
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def build_tldr_text(selections: Sequence[Candidate], note_mode: str) -> str:
    used: set[str] = set()

    def pick(options: Sequence[str]) -> Optional[Candidate]:
        matches = top_candidates(selections, 1, categories=options, exclude=used)
        if not matches:
            return None
        used.add(matches[0].normalized_text)
        return matches[0]

    motivation = pick(["motivation"])
    if motivation is None:
        motivation = pick(["goal"])
    method = pick(["method"])
    contribution = pick(["contribution"])
    contribution_fallback = None
    if contribution is None:
        contribution_fallback = pick(["result", "goal"])
    takeaway = pick(["result"]) if note_mode == "full" else None

    sentences: List[str] = []
    if motivation is not None:
        sentences.append(candidate_note_sentence(motivation, 22))
    if method is not None:
        sentences.append(candidate_note_sentence(method, 22))
    if contribution is not None:
        sentences.append(candidate_note_sentence(contribution, 22))
    elif contribution_fallback is not None:
        sentences.append(candidate_note_sentence(contribution_fallback, 22))
    if takeaway is not None:
        sentences.append(candidate_note_sentence(takeaway, 18))

    if not sentences:
        return "TLDR: This paper is worth revisiting for its reusable claims about the problem, method, and outcome."
    return "TLDR: " + " ".join(sentences)


def build_section_flow_text(
    section: str,
    section_items: Sequence[Candidate],
    max_items: int,
) -> str:
    chosen = top_candidates(section_items, max_items)
    if not chosen:
        return ensure_sentence(
            f"This {section} section introduces the main thread of this part of the paper and prepares the next step of the argument"
        )

    topic_names = []
    seen_topics = set()
    ordered_categories = sorted({item.category for item in chosen}, key=lambda category: CATEGORY_PRIORITY[category])
    for category in ordered_categories:
        topic = SECTION_TOPIC_LABELS[category]
        if topic in seen_topics:
            continue
        seen_topics.add(topic)
        topic_names.append(topic)

    topics = human_join(topic_names)
    fragments = [note_summary_fragment(item, 14) for item in chosen[:2]]
    if len(fragments) >= 2:
        return ensure_sentence(
            f"This {section} section mainly covers {topics} by explaining that {fragments[0]} and that {fragments[1]}"
        )
    if fragments:
        return ensure_sentence(f"This {section} section mainly covers {topics} by explaining that {fragments[0]}")
    return ensure_sentence(f"This {section} section mainly covers {topics}")


def note_point_from_bbox(page: "fitz.Page", bbox: "fitz.Rect", x_offset: float = 10.0) -> "fitz.Point":
    x = bbox.x1 + x_offset
    if x > page.rect.width - 18:
        x = max(18, bbox.x0 - 10)
    y = min(max(18, bbox.y0 + 4), page.rect.height - 18)
    return fitz.Point(x, y)


def build_note_plan(
    doc: "fitz.Document",
    selections: Sequence[Candidate],
    title_info: Optional[TitleInfo],
    headings: Sequence[HeadingInfo],
    args: argparse.Namespace,
) -> List[NoteItem]:
    config = NOTE_MODE_CONFIG[args.note_mode]
    notes: List[NoteItem] = []

    if config["add_tldr"] and title_info is not None:
        page = doc[title_info.page_index]
        notes.append(
            NoteItem(
                page_index=title_info.page_index,
                point=note_point_from_bbox(page, title_info.bbox, x_offset=14.0),
                text=build_tldr_text(selections, args.note_mode),
                kind="tldr",
                icon="Note",
                color=COLOR_PALETTE["goal"],
            )
        )

    if config["add_section_flow"]:
        seen_sections = set()
        for heading in headings:
            if heading.section in SKIP_SECTIONS or heading.section in seen_sections:
                continue
            seen_sections.add(heading.section)
            section_items = [item for item in selections if item.section == heading.section]
            if not section_items and heading.section not in {"abstract", "introduction", "method", "experiments", "conclusion"}:
                continue
            page = doc[heading.page_index]
            notes.append(
                NoteItem(
                    page_index=heading.page_index,
                    point=note_point_from_bbox(page, heading.bbox, x_offset=12.0),
                    text=build_section_flow_text(heading.section, section_items, config["section_items"]),
                    kind="flow",
                    icon="Note",
                    color=COLOR_PALETTE["method"],
                )
            )

    return notes


def build_logical_tokens(words: Sequence[WordInfo]) -> List[LogicalToken]:
    tokens: List[LogicalToken] = []
    index = 0
    while index < len(words):
        word = words[index].text
        merged = False
        if (
            word.endswith("-")
            and index + 1 < len(words)
            and words[index + 1].text
            and words[index + 1].text[0].islower()
        ):
            merged_surface = word[:-1] + words[index + 1].text
            normalized = normalize_token(merged_surface)
            if normalized:
                tokens.append(
                    LogicalToken(
                        surface=merged_surface,
                        normalized=normalized,
                        word_indices=[index, index + 1],
                    )
                )
                index += 2
                merged = True
        if merged:
            continue

        normalized = normalize_token(word)
        if normalized:
            tokens.append(
                LogicalToken(
                    surface=word,
                    normalized=normalized,
                    word_indices=[index],
                )
            )
        index += 1
    return tokens


def is_reusable_sentence(text: str) -> bool:
    lower = text.lower().strip()
    if len(lower) < 28 or len(lower.split()) < 5:
        return False
    if re.search(r"\btable\s+\d|\bfig(?:ure)?\.?\s+\d|\btab\.?\s+\d", lower):
        return False
    if any(pattern.search(lower) for pattern in NON_REUSABLE_PATTERNS):
        return False
    if any(pattern.search(lower) for pattern in GENERIC_BACKGROUND_PATTERNS):
        if not re.search(r"\b(we|our|this paper|this work)\b", lower):
            return False
    digit_count = sum(ch.isdigit() for ch in lower)
    punctuation_count = sum(ch in "%=<>/" for ch in lower)
    if digit_count >= 10 and punctuation_count >= 3:
        return False
    if digit_count >= 16:
        return False
    if re.search(r"\b(batch size|optimizer|lr warmup|weight decay|beta1|beta2|hyper-?parameters?)\b", lower):
        return False
    alpha_count = sum(ch.isalpha() for ch in lower)
    if alpha_count < max(25, len(lower) * 0.45):
        return False
    return True


def reusable_score(text: str) -> float:
    lower = text.lower()
    score = 0.0
    word_count = len(lower.split())
    if word_count >= 12:
        score += 0.8
    if word_count >= 20:
        score += 0.4
    if re.search(r"\b(we|our|this paper|this work|results show|experiments demonstrate)\b", lower):
        score += 0.8
    if re.search(r"\b(therefore|thus|in summary|overall|in conclusion)\b", lower):
        score += 0.6
    citation_count = len(re.findall(r"\[[0-9,\-\s]+\]|\([A-Z][A-Za-z\-]+(?: et al\.)?, \d{4}\)", text))
    if citation_count >= 2:
        score -= 0.6
    if lower.count("%") >= 2 and not re.search(r"\b(show|improv|outperform|achiev)\b", lower):
        score -= 0.5
    return score


def category_scores(text: str, section: str) -> Dict[str, Tuple[float, List[str]]]:
    lower = text.lower()
    scores: Dict[str, Tuple[float, List[str]]] = {}
    reusable = reusable_score(text)
    for category, patterns in CATEGORY_PATTERNS.items():
        score = reusable
        reasons: List[str] = []
        for pattern, weight, label in patterns:
            if pattern.search(lower):
                score += weight
                reasons.append(label)
        score += SECTION_BIAS.get(category, {}).get(section, 0.0)
        if category == "contribution" and lower.startswith(("we summarize", "our contributions", "in summary")):
            score += 1.0
            reasons.append("summary framing")
        if category == "result" and re.search(r"\btable\b|\bfigure\b", lower):
            score += 0.3
            reasons.append("result context")
        scores[category] = (score, reasons)
    return scores


def find_token_span(block: BlockInfo, sentence: str) -> Optional[Tuple[int, int]]:
    wanted = tokenize_for_match(sentence)
    haystack = [token.normalized for token in block.logical_tokens]
    if not wanted or not haystack or len(wanted) > len(haystack):
        return None
    for start in range(0, len(haystack) - len(wanted) + 1):
        if haystack[start : start + len(wanted)] == wanted:
            return start, start + len(wanted) - 1
    return None


def collect_candidates(blocks: Sequence[BlockInfo], args: argparse.Namespace) -> List[Candidate]:
    allowed_categories = list(CORE_CATEGORIES)
    if args.include_optional:
        allowed_categories.extend(
            category for category in OPTIONAL_CATEGORIES if category not in set(args.disable_optional)
        )

    candidates: List[Candidate] = []
    seen_texts = set()
    for block in blocks:
        if block.section in SKIP_SECTIONS:
            continue
        for sentence in sentence_split(block.text):
            if not is_reusable_sentence(sentence):
                continue
            span = find_token_span(block, sentence)
            if span is None:
                continue
            scores = category_scores(sentence, block.section)
            ranked = [
                (category, scores[category][0], scores[category][1])
                for category in allowed_categories
            ]
            ranked.sort(key=lambda item: (-item[1], CATEGORY_PRIORITY[item[0]]))
            best_category, best_score, reasons = choose_category(sentence, ranked)
            if reasons:
                best_score += args.score_bonus

            if (best_score < args.min_score or not reasons) and args.allow_heuristic_fallback:
                fallback = heuristic_category(sentence, block.section, allowed_categories)
                if fallback is not None:
                    fallback_category, fallback_reason, fallback_bonus = fallback
                    base_score = reusable_score(sentence) + SECTION_BIAS.get(fallback_category, {}).get(block.section, 0.0)
                    best_category = fallback_category
                    best_score = max(best_score, base_score + fallback_bonus + args.score_bonus)
                    reasons = [fallback_reason]

            if best_score < args.min_score or not reasons:
                continue

            normalized = normalize_space(sentence.lower())
            if normalized in seen_texts:
                continue
            seen_texts.add(normalized)

            candidates.append(
                Candidate(
                    page_index=block.page_index,
                    block_no=block.block_no,
                    section=block.section,
                    text=sentence,
                    category=best_category,
                    score=round(best_score, 2),
                    reasons=reasons[:3],
                    word_ranges=[span],
                    block=block,
                )
            )
    return candidates


def heuristic_category(
    sentence: str,
    section: str,
    allowed_categories: Sequence[str],
) -> Optional[Tuple[str, str, float]]:
    lower = sentence.lower()
    rules: List[Tuple[str, Tuple[str, ...], re.Pattern[str], str, float]] = [
        ("method", ("method", "experiments", "background"), WEAK_METHOD_PATTERN, "section method cue", 1.05),
        ("result", ("experiments", "conclusion", "discussion", "method"), WEAK_RESULT_PATTERN, "section result cue", 1.10),
        ("motivation", ("introduction", "related work", "background"), WEAK_MOTIVATION_PATTERN, "section motivation cue", 0.95),
        ("goal", ("abstract", "introduction", "background", "conclusion"), WEAK_GOAL_PATTERN, "section goal cue", 0.90),
        ("contribution", ("abstract", "introduction", "conclusion"), WEAK_CONTRIBUTION_PATTERN, "section contribution cue", 0.90),
    ]

    for category, sections, pattern, reason, bonus in rules:
        if category not in allowed_categories:
            continue
        if section in sections and pattern.search(lower):
            return category, reason, bonus

    return None


def choose_category(
    sentence: str,
    ranked: Sequence[Tuple[str, float, List[str]]],
) -> Tuple[str, float, List[str]]:
    best_category, best_score, reasons = ranked[0]
    lookup = {category: (score, why) for category, score, why in ranked}
    lower = sentence.lower()

    if "?" in sentence and "goal" in lookup and lookup["goal"][0] >= best_score - 0.8:
        return "goal", lookup["goal"][0], lookup["goal"][1]

    has_result_shape = bool(
        re.search(r"\b(outperform|achiev|improv|results? show|experiments? demonstrate|significant)\b", lower)
    )
    if has_result_shape and "result" in lookup and lookup["result"][0] >= best_score - 0.6:
        return "result", lookup["result"][0], lookup["result"][1]

    if "contribution" in lookup and lookup["contribution"][0] >= best_score - 0.4:
        if re.search(r"\b(contributions?|novel|different from|first)\b", lower):
            return "contribution", lookup["contribution"][0], lookup["contribution"][1]

    return best_category, best_score, reasons


def category_cap(category: str, args: argparse.Namespace) -> int:
    return max(1, round(BASE_CATEGORY_CAPS[category] * args.category_scale))


def select_candidates(
    candidates: Sequence[Candidate],
    page_count: int,
    args: argparse.Namespace,
    baseline_low_count: Optional[int] = None,
) -> List[Candidate]:
    if args.highlight_level == "low" or baseline_low_count is None:
        target_total = min(args.max_total, len(candidates))
    else:
        target_total = min(args.max_total, round(baseline_low_count * args.target_multiplier))
        target_total = max(len(CORE_CATEGORIES), target_total)

    per_page_counts: Counter[int] = Counter()
    category_counts: Counter[str] = Counter()
    block_counts: Counter[Tuple[int, int]] = Counter()
    selected: List[Candidate] = []
    selected_keys = set()

    def can_take(candidate: Candidate) -> bool:
        if (candidate.page_index, candidate.block_no, candidate.normalized_text) in selected_keys:
            return False
        if per_page_counts[candidate.page_index] >= args.max_per_page:
            return False
        if category_counts[candidate.category] >= category_cap(candidate.category, args):
            return False
        if block_counts[(candidate.page_index, candidate.block_no)] >= args.max_per_block:
            return False
        return True

    def add(candidate: Candidate) -> None:
        key = (candidate.page_index, candidate.block_no, candidate.normalized_text)
        selected.append(candidate)
        selected_keys.add(key)
        per_page_counts[candidate.page_index] += 1
        category_counts[candidate.category] += 1
        block_counts[(candidate.page_index, candidate.block_no)] += 1

    sorted_candidates = sorted(
        candidates,
        key=lambda item: (
            -item.score,
            item.page_index,
            CATEGORY_PRIORITY[item.category],
            item.block_no,
        ),
    )

    for category in CORE_CATEGORIES:
        category_items = [item for item in sorted_candidates if item.category == category]
        for candidate in category_items:
            if can_take(candidate):
                add(candidate)
                break

    for candidate in sorted_candidates:
        if len(selected) >= target_total:
            break
        if can_take(candidate):
            add(candidate)

    selected.sort(key=lambda item: (item.page_index, item.block_no, -item.score))
    return selected


def highlight_rects(candidate: Candidate) -> List["fitz.Rect"]:
    rects: List[fitz.Rect] = []
    words = candidate.block.words
    current_line = None
    line_rect: Optional[fitz.Rect] = None

    logical_tokens = candidate.block.logical_tokens
    for start, end in candidate.word_ranges:
        for token_index in range(start, end + 1):
            token = logical_tokens[token_index]
            token_words = [words[index] for index in token.word_indices]
            for word in token_words:
                if current_line != word.line_no:
                    if line_rect is not None:
                        rects.append(line_rect)
                    line_rect = fitz.Rect(word.rect)
                    current_line = word.line_no
                else:
                    line_rect |= word.rect
        if line_rect is not None:
            rects.append(line_rect)
            line_rect = None
            current_line = None

    merged: List[fitz.Rect] = []
    for rect in rects:
        if not merged:
            merged.append(rect)
            continue
        previous = merged[-1]
        same_line = abs(previous.y0 - rect.y0) < 2.0 and abs(previous.y1 - rect.y1) < 2.0
        close = rect.x0 - previous.x1 < 12.0
        if same_line and close:
            merged[-1] = fitz.Rect(previous.x0, previous.y0, rect.x1, previous.y1)
        else:
            merged.append(rect)
    return merged


def annotate_pdf(
    doc: "fitz.Document",
    selections: Sequence[Candidate],
    notes: Sequence[NoteItem],
    output_path: Path,
    opacity: float,
) -> None:
    page_map: Dict[int, List[Candidate]] = defaultdict(list)
    for candidate in selections:
        page_map[candidate.page_index].append(candidate)

    for page_index, items in page_map.items():
        page = doc[page_index]
        for candidate in items:
            rects = highlight_rects(candidate)
            if not rects:
                continue
            annot = page.add_highlight_annot(rects)
            annot.set_colors(stroke=COLOR_PALETTE[candidate.category])
            annot.set_opacity(opacity)
            annot.update()

    for note in notes:
        page = doc[note.page_index]
        annot = page.add_text_annot(note.point, note.text, icon=note.icon)
        annot.set_colors(stroke=note.color)
        annot.set_info(title="paper-highlight", subject=note.kind)
        annot.update()

    doc.save(str(output_path), garbage=4, deflate=True)


def plan_to_json(
    candidates: Sequence[Candidate],
    notes: Sequence[NoteItem],
    input_path: Path,
    output_path: Optional[Path],
    args: argparse.Namespace,
) -> Dict[str, object]:
    by_category = Counter(item.category for item in candidates)
    return {
        "input_pdf": str(input_path),
        "output_pdf": str(output_path) if output_path else None,
        "highlight_level": args.highlight_level,
        "note_mode": args.note_mode,
        "settings": {
            "max_per_page": args.max_per_page,
            "max_total": args.max_total,
            "min_score": args.min_score,
            "max_per_block": args.max_per_block,
        },
        "total_highlights": len(candidates),
        "total_notes": len(notes),
        "category_counts": dict(by_category),
        "highlights": [
            {
                "page": item.page_index + 1,
                "section": item.section,
                "category": CATEGORY_LABELS[item.category],
                "score": item.score,
                "reasons": item.reasons,
                "text": item.text,
            }
            for item in candidates
        ],
        "notes": [
            {
                "page": item.page_index + 1,
                "kind": item.kind,
                "text": item.text,
            }
            for item in notes
        ],
    }


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.highlighted.pdf")


def main() -> int:
    raw_args = parse_args()
    args = resolve_level_settings(raw_args)
    require_fitz()

    input_path = Path(args.input_pdf).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output else default_output_path(input_path)

    if not input_path.exists():
        raise SystemExit(f"Input PDF not found: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        raise SystemExit(f"Input file must be a PDF: {input_path}")

    doc = fitz.open(str(input_path))
    try:
        blocks = extract_blocks(doc)
        title_info, headings = extract_outline(doc)
        baseline_low_count: Optional[int] = None
        if args.highlight_level != "low":
            low_args = argparse.Namespace(**vars(raw_args))
            low_args.highlight_level = "low"
            low_args.max_per_page = None
            low_args.max_total = None
            low_args.min_score = None
            low_args = resolve_level_settings(low_args)
            low_candidates = collect_candidates(blocks, low_args)
            low_selections = select_candidates(low_candidates, len(doc), low_args)
            baseline_low_count = len(low_selections)

        candidates = collect_candidates(blocks, args)
        selections = select_candidates(candidates, len(doc), args, baseline_low_count=baseline_low_count)
        notes = build_note_plan(doc, selections, title_info, headings, args)
        report = plan_to_json(selections, notes, input_path, None if args.dry_run else output_path, args)

        if args.report_json:
            report_path = Path(args.report_json).expanduser().resolve()
            report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        print(
            f"Selected {len(selections)} highlights across {len(doc)} pages "
            f"(level={args.highlight_level}, opacity={args.opacity}, notes={args.note_mode}/{len(notes)}): "
            + ", ".join(f"{name}={count}" for name, count in sorted(report["category_counts"].items()))
        )
        if args.dry_run:
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 0

        annotate_pdf(doc, selections, notes, output_path, OPACITY[args.opacity])
        print(f"Wrote highlighted PDF to: {output_path}")
        return 0
    finally:
        doc.close()


if __name__ == "__main__":
    sys.exit(main())
