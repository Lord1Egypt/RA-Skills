#!/usr/bin/env python3
"""Lint prose for clarity, fidelity, and common forms of empty language.

This dependency-free tool checks deterministic patterns. It cannot certify
conformance with an external standard or judge factual accuracy, meaning, or
voice.
"""

from __future__ import annotations

import argparse
import bisect
import glob
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

VERSION = "1.0.0"
MODES = ("strict", "technical", "natural")
SEVERITIES = ("off", "warning", "error")

WORD_RE = re.compile(r"\b[A-Za-z0-9]+(?:[’'-][A-Za-z0-9]+)*\b")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
LIST_PREFIX_RE = re.compile(r"^(\s*)(?:[-+*]|\d+[.)])\s+")
HEADING_RE = re.compile(r"^(\s*)#{1,6}\s+")
BLOCKQUOTE_RE = re.compile(r"^(\s*)>\s?")
TABLE_RULE_RE = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
IMAGE_RE = re.compile(r"!\[[^\]]*]\([^)\n]*\)")
LINK_RE = re.compile(r"\[([^\]]+)]\(([^)\n]*)\)")
AUTOLINK_RE = re.compile(r"<(?:https?://|mailto:)[^>\n]+>")
URL_RE = re.compile(r"https?://[^\s)>]+")
HTML_TAG_RE = re.compile(r"</?[A-Za-z][^>\n]*>")

BE = r"(?:am|is|are|was|were|be|been|being)"
PARTICIPLE = (
    r"(?:\w+(?:ed|en)|built|bought|brought|caught|done|drawn|driven|found|"
    r"given|got|gotten|held|kept|known|made|put|read|run|seen|sent|set|"
    r"shown|sold|spoken|taken|taught|thrown|told|written)"
)
PASSIVE_RE = re.compile(
    rf"\b{BE}\s+(?:\w+ly\s+)?(?P<participle>{PARTICIPLE})\b", re.IGNORECASE
)
PROGRESSIVE_RE = re.compile(rf"\b{BE}\s+(?:\w+ly\s+)?\w+ing\b", re.IGNORECASE)
CONTRACTION_RE = re.compile(
    r"\b(?:ain['’]t|aren['’]t|can['’]t|couldn['’]t|didn['’]t|doesn['’]t|"
    r"don['’]t|hadn['’]t|hasn['’]t|haven['’]t|he['’]d|he['’]ll|he['’]s|"
    r"I['’]d|I['’]ll|I['’]m|I['’]ve|isn['’]t|it['’]d|it['’]ll|it['’]s|"
    r"let['’]s|mightn['’]t|mustn['’]t|shan['’]t|she['’]d|she['’]ll|"
    r"she['’]s|shouldn['’]t|that['’]s|there['’]s|they['’]d|they['’]ll|"
    r"they['’]re|they['’]ve|wasn['’]t|we['’]d|we['’]ll|we['’]re|we['’]ve|"
    r"weren['’]t|what['’]s|where['’]s|who['’]s|won['’]t|wouldn['’]t|"
    r"you['’]d|you['’]ll|you['’]re|you['’]ve)\b",
    re.IGNORECASE,
)
REPEATED_WORD_RE = re.compile(r"\b([A-Za-z][A-Za-z'-]*)\s+\1\b", re.IGNORECASE)
FORMULAIC_CONTRAST_RE = re.compile(
    r"\b(?:not\s+(?:just|only)\b(?:(?![.!?\n]).){0,120}?\bbut(?:\s+also)?\b|"
    r"(?:the\s+)?(?:question|issue|challenge|goal|point)\s+(?:is|was)"
    r"(?:n['’]t| not)\b(?:(?![.!?\n]).){0,120}?"
    r"\b(?:but|it['’]s|it is)\b)",
    re.IGNORECASE,
)
DIRECT_BINARY_RE = re.compile(
    r"(?:\b(?:this|that|it)\s+is\s+not\b(?:(?![.!?\n]).){1,100}[.!?]\s*"
    r"(?:it\s+is|it['’]s|this\s+is|that['’]s)\b|"
    r"\b(?:is|are|was|were)\s+not\s+(?:just|only)\b|"
    r"\b(?:is|are|was|were)\s+not\b(?:(?![.!?\n]).){1,100}[,;]\s*"
    r"(?:but\b|rather\b|it\s+is\b|it['’]s\b))",
    re.IGNORECASE,
)
FAUX_INSIGHT_RE = re.compile(
    r"\b(?:this\s+is\s+the\s+part\s+(?:most\s+people|everyone)\s+"
    r"(?:skip|miss)|what\s+(?:most\s+people|everyone)\s+gets?\s+wrong|"
    r"here['’]s\s+what\s+(?:nobody|no\s+one)\s+tells\s+you|"
    r"the\s+part\s+everyone\s+misses)\b",
    re.IGNORECASE,
)
COLON_REVEAL_RE = re.compile(
    r"(?m)^(?!\s*(?:[-+*]|\d+[.)]|#|>))\s*[A-Z][^:\n.!?]{2,48}:[ \t]+[a-z]"
)
TECHNICAL_LABEL_RE = re.compile(
    r"^(?:error\s+(?:code|message)|site\s+address|hook|status|url|uri|path|"
    r"version|date|time|id|identifier|command|file|host|hostname)$",
    re.IGNORECASE,
)
NEGATIVE_LIST_RE = re.compile(
    r"(?:^|(?<=[.!?])\s+)Not\s+[^.!?\n]{1,80}[.!?]\s+"
    r"Not\s+[^.!?\n]{1,80}[.!?]",
    re.IGNORECASE,
)
DRAMATIC_STACK_RE = re.compile(
    r"(?:^|(?<=[.!?])\s+)(?:And|But)\s+[^.!?\n]{1,60}[.!?]\s+"
    r"(?:And|But)\s+[^.!?\n]{1,60}[.!?]",
)
QUESTION_ANSWER_RE = re.compile(
    r"(?:^|(?<=[.!?])[ \t]+)[A-Z][^?\n]{2,100}\?[ \t]+"
    r"[A-Z][^.!?\n]{1,100}[.!?]"
)
SYNTHESIS_RE = re.compile(
    r"\b(?:same\s+problem,\s+different\s+angle|"
    r"both\s+cases?\s+come\s+down\s+to\s+the\s+same\s+thing|"
    r"the\s+tricky\s+part\s+is\s+the\s+cycle)\b",
    re.IGNORECASE,
)
CONCESSIVE_LOOP_RE = re.compile(
    r"\b[^.!?\n]{1,100}\bwill\s+help,\s+but\s+[^.!?\n]{1,100}"
    r"\b(?:can|could|may|might|will)\b[^.!?\n]{0,80}",
    re.IGNORECASE,
)
GENERIC_HEADING_RE = re.compile(
    r"(?mi)^\s*#{1,6}\s+(?:where\s+we\s+are|why\s+(?:this|it)\s+matters|"
    r"what\s+we(?:['’]re|\s+are)\s+hearing|the\s+bigger\s+picture|"
    r"what\s+comes\s+next|key\s+takeaways?|in\s+conclusion)"
)
HEADING_EMOJI_RE = re.compile(
    r"(?m)^\s*#{1,6}\s+.*[\U0001F300-\U0001FAFF\u2600-\u27BF]"
)
BOLD_EMPHASIS_RE = re.compile(r"(?<!\*)\*\*(?!\s)[^*\n]{1,80}\*\*(?!\*)")
NARRATOR_SCAFFOLD_RE = re.compile(
    r"\b(?:"
    r"(?:the|this|current|available|new|fresh)\s+evidence\s+"
    r"(?:shows?|suggests?|indicates?|confirms?|demonstrates?)|"
    r"(?:the\s+)?(?:log|trace|sequence|data|results?|failures?|timing)\s+"
    r"(?:shows?|suggests?|indicates?|confirms?|demonstrates?)|"
    r"this\s+(?:shows?|suggests?|indicates?|confirms?|demonstrates?|means)|"
    r"there\s+is\s+(?:a\s+)?direct\s+precedent|"
    r"(?:a\s+)?(?:fresh|new)\s+query\s+(?:found|shows?)"
    r")\b",
    re.IGNORECASE,
)
ABSTRACT_EVIDENCE_RE = re.compile(
    r"\b(?:"
    r"documented\s+(?:customer|real-world)\s+(?:impact|damage)|"
    r"(?:including|with|plus)\s+(?:documented\s+)?"
    r"(?:customer|real-world)\s+(?:impact|damage)"
    r")\b",
    re.IGNORECASE,
)
PARTICIPIAL_GLOSS_RE = re.compile(
    r",\s*(?:highlighting|underscoring|showcasing|demonstrating|illustrating|"
    r"reflecting|reinforcing|signaling|symbolizing)\b",
    re.IGNORECASE,
)

FALSE_PASSIVE_PARTICIPLES = {
    "advanced",
    "aged",
    "concerned",
    "gifted",
    "learned",
    "red",
    "talented",
    "tired",
    "united",
    "wicked",
}
ALLOWED_REPEATS = {"had", "that"}

INFLATED = {
    "a plethora of": "name the amount or use many",
    "a variety of": "name the items or use various",
    "acquire": "use get or buy",
    "acquires": "use gets or buys",
    "additionally": "use also or delete the transition",
    "aforementioned": "name the item",
    "amongst": "use among",
    "begin": "use start",
    "begins": "use starts",
    "commence": "use start",
    "commences": "use starts",
    "comprehensive": "state what the text covers",
    "demonstrate": "use show",
    "demonstrates": "use shows",
    "due to the fact that": "use because",
    "facilitate": "use help, enable, or a precise verb",
    "facilitates": "use helps, enables, or a precise verb",
    "furthermore": "use also or delete the transition",
    "henceforth": "state the time or rule directly",
    "in order to": "use to",
    "in the event that": "use if",
    "initiate": "use start",
    "initiates": "use starts",
    "leverage": "use use or name the exact action",
    "leverages": "use uses or name the exact action",
    "leveraging": "use using or name the exact action",
    "moreover": "use also or delete the transition",
    "myriad": "name the amount or use many",
    "numerous": "give a number or use many",
    "obtain": "use get",
    "obtains": "use gets",
    "prior to": "use before",
    "subsequent to": "use after",
    "therein": "name the place or document",
    "utilization": "use use",
    "utilize": "use use",
    "utilizes": "use uses",
    "utilizing": "use using",
    "whilst": "use while",
}

PROMOTIONAL = {
    "battle-tested",
    "best-in-class",
    "blazing",
    "cutting-edge",
    "delightful",
    "effortless",
    "effortlessly",
    "elegant",
    "enterprise-grade",
    "first-class",
    "game-changing",
    "lightning-fast",
    "next-generation",
    "powerful",
    "revolutionary",
    "robust",
    "seamless",
    "seamlessly",
    "state-of-the-art",
    "supercharge",
    "turnkey",
    "world-class",
}

AI_DICTION = {
    "beacon",
    "delve",
    "elevate",
    "embark",
    "empower",
    "ever-evolving",
    "foster",
    "harness",
    "intricate",
    "meticulous",
    "multifaceted",
    "paramount",
    "realm",
    "streamline",
    "tapestry",
    "transformative",
}

HEDGES = {
    "as mentioned above": "delete it or name the relevant fact",
    "as noted above": "delete it or name the relevant fact",
    "at the end of the day": "state the conclusion",
    "generally speaking": "state the scope or evidence",
    "going forward": "state what changes and when",
    "here's the thing": "delete the lead-in and state the point",
    "here's what i mean": "delete the lead-in and state the point",
    "i'll be honest": "delete the lead-in unless it adds necessary candor",
    "in conclusion": "end on the conclusion without announcing it",
    "in terms of": "name the subject directly",
    "in this article": "delete the self-reference and start with the subject",
    "it is important to note": "delete the lead-in and state the point",
    "it should be noted": "delete the lead-in and state the point",
    "it is worth noting": "delete the lead-in and state the point",
    "let me be clear": "delete the lead-in and state the point",
    "let's dive in": "delete the stock invitation and start",
    "moving forward": "state what changes and when",
    "needless to say": "delete the phrase",
    "please note that": "delete the lead-in and state the point",
    "the reality is": "delete the lead-in and state the fact",
    "the truth is": "delete the lead-in and state the fact",
    "when it comes to": "name the subject directly",
    "when all is said and done": "state the conclusion",
    "with regard to": "name the subject directly",
    "what if i told you": "state the claim",
    "what most people get wrong": "state the claim and evidence",
    "have you ever wondered": "ask a necessary question or state the point",
    "the answer is simple": "state the answer and its basis",
    "the answer might surprise you": "state the answer",
    "think about it": "state the point",
    "you might be wondering": "state the likely question directly",
}

CLICHES = {
    "at its core": "state the central fact",
    "dive into": "use examine, explain, or a precise verb",
    "drill down": "use inspect or analyze",
    "in today's fast-paced world": "delete the stock opening",
    "low-hanging fruit": "name the easy task or gain",
    "move the needle": "name the measured change",
    "navigate the landscape": "name the work or decision",
    "paradigm shift": "describe the specific change",
    "silver bullet": "name the proposed solution and its limits",
    "tip of the iceberg": "state what remains unknown or unseen",
}

PHRASAL = {
    "circle back": "use return or reply",
    "kick off": "use start",
    "ramp up": "use increase",
    "reach out": "use contact",
    "roll out": "use release or deploy",
    "spin down": "use stop or remove",
    "spin up": "use start, create, or provision",
    "tear down": "use remove, stop, or dismantle",
    "touch base": "use contact or meet",
}

VAGUE = {
    "a number of": "give the number or name the items",
    "extremely": "give a measure or delete the intensifier",
    "highly": "give a measure or delete the intensifier",
    "incredibly": "give a measure or delete the intensifier",
    "quite": "give a measure or delete the intensifier",
    "really": "give a measure or delete the intensifier",
    "various": "name the items",
    "very": "give a measure or delete the intensifier",
}

NOMINAL_PHRASES = {
    "carry out an analysis": "analyze",
    "carry out an inspection": "inspect",
    "conduct a review": "review",
    "give consideration to": "consider",
    "make a decision": "decide",
    "make use of": "use",
    "perform an analysis": "analyze",
    "provide assistance": "help",
}

WEASEL_ATTRIBUTIONS = {
    "best practices suggest": "name the practice and source",
    "experts agree": "name the experts and source",
    "industry experts widely agree": "name the experts and source",
    "industry reports suggest": "name the reports and link or cite them",
    "it is broadly recognized": "name the source or state the evidence",
    "it is widely understood": "name the source or state the evidence",
    "many argue": "name the people or narrow the claim",
    "research shows": "name the research and link or cite it",
    "some observers believe": "name the observers or narrow the claim",
    "studies show": "name the studies and link or cite them",
    "widely regarded as": "name the source or state the evidence",
}

IMPORTANCE_PUFFERY = {
    "marks a pivotal moment": "state what changed and why it matters",
    "plays a vital role": "state what the subject does",
    "solidifies its position": "state the measured or observed result",
    "stands as a testament": "state the evidence",
    "this changes everything": "state the specific effect and scope",
    "this is huge": "state the effect or measure",
    "underscores its significance": "state the concrete consequence",
}

GENERIC_ENDINGS = {
    "are you ready": "delete the engagement bait or ask for a specific action",
    "the best is yet to come": "end with the concrete result or next action",
    "the future belongs to": "state the supported claim or action",
    "the future is ours to create": "state who will do what",
    "the journey has just begun": "state the next step",
    "this is just the beginning": "state the next step",
    "this is only the beginning": "state the next step",
    "together we can move forward": "name the actors and next action",
    "welcome to the future": "state what changed",
    "welcome to what's next": "state what changed",
    "who else needed to hear this": "delete the engagement bait",
}


@dataclass(frozen=True)
class Rule:
    code: str
    title: str
    suggestion: str


RULES = {
    "CLR001": Rule("CLR001", "long sentence", "Split the sentence or remove words."),
    "CLR002": Rule("CLR002", "long paragraph", "Split the paragraph by topic."),
    "CLR003": Rule("CLR003", "semicolon", "Use a period or a short conjunction."),
    "CLR004": Rule("CLR004", "contraction", "Write the words in full."),
    "CLR005": Rule(
        "CLR005",
        "possible passive voice",
        "Name the actor and use an active verb when the actor matters.",
    ),
    "CLR006": Rule(
        "CLR006",
        "possible progressive verb",
        "Use a simple verb form unless duration is necessary.",
    ),
    "CLR007": Rule(
        "CLR007", "nominalized action", "Replace the phrase with a direct verb."
    ),
    "CLR008": Rule("CLR008", "phrasal verb", "Use one precise verb."),
    "WRD001": Rule(
        "WRD001", "inflated wording", "Use a short, exact word or rewrite the sentence."
    ),
    "WRD002": Rule(
        "WRD002",
        "promotional wording",
        "Replace the claim with a fact, measure, or evidence.",
    ),
    "WRD003": Rule(
        "WRD003", "empty lead-in or hedge", "State the point, scope, or uncertainty."
    ),
    "WRD004": Rule(
        "WRD004", "stale expression", "Use literal language or a fresh, useful image."
    ),
    "WRD005": Rule(
        "WRD005", "vague intensifier", "Give a measure, name the items, or cut the word."
    ),
    "WRD006": Rule(
        "WRD006",
        "unsupported attribution",
        "Name the source, narrow the claim, or remove it.",
    ),
    "WRD007": Rule(
        "WRD007",
        "importance puffery",
        "State the fact, evidence, or concrete consequence.",
    ),
    "WRD008": Rule(
        "WRD008",
        "formulaic contrast",
        "State the actual distinction without a canned not-X-but-Y frame.",
    ),
    "WRD009": Rule(
        "WRD009",
        "generic ending or audience bait",
        "End with the concrete result, decision, or next action.",
    ),
    "WRD010": Rule(
        "WRD010",
        "unsupported participial gloss",
        "State the evidence and inference separately, or delete the gloss.",
    ),
    "WRD011": Rule(
        "WRD011",
        "common AI diction",
        "Use a concrete term unless this word has a precise, literal purpose.",
    ),
    "STR001": Rule(
        "STR001", "binary contrast", "State the supported point directly."
    ),
    "STR002": Rule(
        "STR002", "faux-insight setup", "Delete the setup and state the claim."
    ),
    "STR003": Rule(
        "STR003",
        "possible colon reveal",
        "Use a plain sentence unless the colon introduces a list, label, or quote.",
    ),
    "STR004": Rule(
        "STR004", "negative listing", "State the positive claim directly."
    ),
    "STR005": Rule(
        "STR005", "dramatic fragment stack", "Join the related thoughts."
    ),
    "STR006": Rule(
        "STR006",
        "rhetorical question and answer",
        "State the answer directly unless the question serves the reader.",
    ),
    "STR007": Rule(
        "STR007",
        "unsupported synthesis frame",
        "Delete the frame and keep only the supported relationship.",
    ),
    "STR008": Rule(
        "STR008", "generic heading", "Use a specific navigation label or remove it."
    ),
    "STR009": Rule(
        "STR009", "emoji in heading", "Remove decorative emoji from the heading."
    ),
    "STR010": Rule(
        "STR010",
        "decorative bold emphasis",
        "Use structure and wording for emphasis; keep bold for labels or scan tasks.",
    ),
    "STR011": Rule(
        "STR011",
        "very short headed section",
        "Merge the section unless the heading provides useful navigation.",
    ),
    "STR012": Rule(
        "STR012",
        "possible bullet inflation",
        "Use prose unless the items are parallel or need to be scanned.",
    ),
    "STR013": Rule(
        "STR013",
        "repeated sentence opening",
        "Vary the opening only if the repetition is accidental or robotic.",
    ),
    "STR014": Rule(
        "STR014",
        "unsupported concessive loop",
        "Keep only supported effects and state the condition with its real certainty.",
    ),
    "STR015": Rule(
        "STR015",
        "possible narrator scaffolding",
        "Delete the abstract recap if concrete evidence follows; do not replace it with a synonym. Keep necessary inference or uncertainty.",
    ),
    "STR016": Rule(
        "STR016",
        "abstract evidence recap",
        "Delete the recap and state the concrete evidence once.",
    ),
    "TXT001": Rule("TXT001", "repeated word", "Delete the accidental repetition."),
    "TXT002": Rule(
        "TXT002",
        "em-dash overuse",
        "Use a period, comma, or parentheses unless the dash improves the sentence.",
    ),
}

MODE_CONFIG = {
    "strict": {
        "sentence_limit": 20,
        "paragraph_limit": 6,
        "severity": {
            "CLR001": "error",
            "CLR002": "error",
            "CLR003": "error",
            "CLR004": "error",
            "CLR005": "error",
            "CLR006": "error",
            "CLR007": "error",
            "CLR008": "error",
            "WRD001": "error",
            "WRD002": "error",
            "WRD003": "error",
            "WRD004": "warning",
            "WRD005": "warning",
            "WRD006": "error",
            "WRD007": "error",
            "WRD008": "warning",
            "WRD009": "error",
            "WRD010": "warning",
            "WRD011": "warning",
            "TXT001": "error",
            "TXT002": "warning",
        },
    },
    "technical": {
        "sentence_limit": 25,
        "paragraph_limit": 6,
        "severity": {
            "CLR001": "warning",
            "CLR002": "warning",
            "CLR003": "warning",
            "CLR004": "off",
            "CLR005": "warning",
            "CLR006": "warning",
            "CLR007": "warning",
            "CLR008": "warning",
            "WRD001": "warning",
            "WRD002": "error",
            "WRD003": "error",
            "WRD004": "warning",
            "WRD005": "warning",
            "WRD006": "error",
            "WRD007": "error",
            "WRD008": "warning",
            "WRD009": "warning",
            "WRD010": "warning",
            "WRD011": "warning",
            "TXT001": "error",
            "TXT002": "warning",
        },
    },
    "natural": {
        "sentence_limit": 40,
        "paragraph_limit": 10,
        "severity": {
            "CLR001": "warning",
            "CLR002": "warning",
            "CLR003": "off",
            "CLR004": "off",
            "CLR005": "warning",
            "CLR006": "off",
            "CLR007": "warning",
            "CLR008": "off",
            "WRD001": "warning",
            "WRD002": "error",
            "WRD003": "error",
            "WRD004": "warning",
            "WRD005": "warning",
            "WRD006": "error",
            "WRD007": "error",
            "WRD008": "warning",
            "WRD009": "warning",
            "WRD010": "warning",
            "WRD011": "warning",
            "TXT001": "error",
            "TXT002": "warning",
        },
    },
}

ANTI_SLOP_SEVERITY = {
    "STR001": "error",
    "STR002": "error",
    "STR003": "warning",
    "STR004": "error",
    "STR005": "error",
    "STR006": "warning",
    "STR007": "error",
    "STR008": "warning",
    "STR009": "error",
    "STR010": "warning",
    "STR011": "warning",
    "STR012": "warning",
    "STR013": "warning",
    "STR014": "error",
    "STR015": "warning",
    "STR016": "error",
}


@dataclass
class Finding:
    path: str
    line: int
    column: int
    code: str
    severity: str
    message: str
    suggestion: str
    excerpt: str


@dataclass
class LintResult:
    path: str
    words: int
    sentences: int
    paragraphs: int
    findings: list[Finding]

    @property
    def errors(self) -> int:
        return sum(item.severity == "error" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "warning" for item in self.findings)

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "words": self.words,
            "sentences": self.sentences,
            "paragraphs": self.paragraphs,
            "errors": self.errors,
            "warnings": self.warnings,
            "findings": [asdict(item) for item in self.findings],
        }


def blank_match(text: str, match: re.Match[str]) -> str:
    """Replace a match with spaces while retaining newlines and offsets."""
    return "".join("\n" if char == "\n" else " " for char in match.group(0))


def sanitize_markdown(text: str) -> str:
    """Hide common non-prose Markdown while retaining source offsets."""
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    in_frontmatter = bool(lines and lines[0].strip() == "---")
    frontmatter_closed = not in_frontmatter
    in_html_comment = False

    for index, original in enumerate(lines):
        line = original
        stripped = line.strip()

        if in_frontmatter and not frontmatter_closed:
            output.append("".join("\n" if char == "\n" else " " for char in line))
            if index > 0 and stripped in {"---", "..."}:
                frontmatter_closed = True
            continue

        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            output.append("".join("\n" if char == "\n" else " " for char in line))
            continue

        if in_fence:
            output.append("".join("\n" if char == "\n" else " " for char in line))
            continue

        if in_html_comment:
            end = line.find("-->")
            if end < 0:
                output.append("".join("\n" if char == "\n" else " " for char in line))
                continue
            prefix = "".join("\n" if char == "\n" else " " for char in line[: end + 3])
            line = prefix + line[end + 3 :]
            in_html_comment = False

        while "<!--" in line:
            start = line.find("<!--")
            end = line.find("-->", start + 4)
            if end < 0:
                line = line[:start] + "".join(
                    "\n" if char == "\n" else " " for char in line[start:]
                )
                in_html_comment = True
                break
            hidden = "".join(
                "\n" if char == "\n" else " " for char in line[start : end + 3]
            )
            line = line[:start] + hidden + line[end + 3 :]

        if TABLE_RULE_RE.match(line):
            output.append("".join("\n" if char == "\n" else " " for char in line))
            continue

        if line.count("|") >= 2:
            first_pipe = line.find("|")
            line = line[:first_pipe] + "\n" + line[first_pipe + 1 :]

        line = IMAGE_RE.sub(lambda match: blank_match(line, match), line)
        line = INLINE_CODE_RE.sub(lambda match: blank_match(line, match), line)
        line = AUTOLINK_RE.sub(lambda match: blank_match(line, match), line)
        line = URL_RE.sub(lambda match: blank_match(line, match), line)
        line = HTML_TAG_RE.sub(lambda match: blank_match(line, match), line)

        def keep_link_label(match: re.Match[str]) -> str:
            prefix = match.group(1)
            suffix_length = len(match.group(0)) - len(prefix)
            return prefix + (" " * suffix_length)

        line = LINK_RE.sub(keep_link_label, line)
        line = HEADING_RE.sub(lambda match: " " * len(match.group(0)), line)

        def separate_list_item(match: re.Match[str]) -> str:
            """Make each Markdown list item a logical paragraph."""
            return "\n" + (" " * (len(match.group(0)) - 1))

        line = LIST_PREFIX_RE.sub(separate_list_item, line)
        line = BLOCKQUOTE_RE.sub(lambda match: " " * len(match.group(0)), line)
        line = line.replace("|", " ")
        output.append(line)

    return "".join(output)


def line_starts(text: str) -> list[int]:
    starts = [0]
    starts.extend(match.end() for match in re.finditer(r"\n", text))
    return starts


def location(starts: Sequence[int], offset: int) -> tuple[int, int]:
    line_index = bisect.bisect_right(starts, offset) - 1
    return line_index + 1, offset - starts[line_index] + 1


def is_abbreviation(text: str, index: int) -> bool:
    prefix = text[max(0, index - 8) : index + 1].lower()
    if re.search(r"\b(?:e\.g|i\.e|etc|vs|mr|mrs|ms|dr|fig|no)\.$", prefix):
        return True
    if index > 0 and index + 1 < len(text):
        if text[index - 1].isdigit() and text[index + 1].isdigit():
            return True
    return bool(re.search(r"\b[A-Z]\.$", text[max(0, index - 2) : index + 1]))


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Return sentence-like spans without changing source offsets."""
    spans: list[tuple[int, int]] = []
    start: int | None = None
    index = 0

    while index < len(text):
        char = text[index]
        if start is None and not char.isspace():
            start = index

        if start is not None:
            paragraph_break = char == "\n" and re.match(r"\n[ \t]*\n", text[index:])
            sentence_end = char in ".!?"
            if sentence_end and char == "." and is_abbreviation(text, index):
                sentence_end = False

            if sentence_end:
                look = index + 1
                while look < len(text) and text[look] in "\"')]}":
                    look += 1
                while look < len(text) and text[look] in " \t":
                    look += 1
                if look < len(text) and text[look] == "\n":
                    look += 1
                    while look < len(text) and text[look] in " \t":
                        look += 1
                if look < len(text) and text[look].islower():
                    sentence_end = False

            if sentence_end or paragraph_break:
                end = index + 1 if sentence_end else index
                if text[start:end].strip():
                    spans.append((start, end))
                start = None

        index += 1

    if start is not None and text[start:].strip():
        spans.append((start, len(text)))
    return spans


def paragraph_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for match in re.finditer(r"(?:^|\n[ \t]*\n)(?P<body>\s*\S.*?)(?=\n[ \t]*\n|\Z)", text, re.DOTALL):
        start, end = match.span("body")
        if WORD_RE.search(text[start:end]):
            spans.append((start, end))
    return spans


def excerpt(text: str, start: int, end: int, width: int = 120) -> str:
    value = re.sub(r"\s+", " ", text[start:end]).strip()
    if len(value) <= width:
        return value
    return value[: width - 1].rstrip() + "…"


def phrase_matches(text: str, phrases: Iterable[str]) -> Iterable[tuple[str, re.Match[str]]]:
    for phrase in sorted(phrases, key=len, reverse=True):
        pattern = re.compile(
            r"(?<![A-Za-z])" + re.escape(phrase) + r"(?![A-Za-z])",
            re.IGNORECASE,
        )
        for match in pattern.finditer(text):
            yield phrase, match


def severity_for(mode: str, code: str) -> str:
    if code.startswith("STR"):
        if mode == "natural" and code == "STR005":
            return "warning"
        return ANTI_SLOP_SEVERITY[code]
    return str(MODE_CONFIG[mode]["severity"][code])


def lint_text(
    text: str,
    *,
    path: str = "<stdin>",
    mode: str = "technical",
    sentence_limit: int | None = None,
) -> LintResult:
    if mode not in MODES:
        raise ValueError(f"unknown mode: {mode}")

    view = sanitize_markdown(text)
    starts = line_starts(text)
    sentences = sentence_spans(view)
    paragraphs = paragraph_spans(view)
    findings: list[Finding] = []
    configured_limit = int(MODE_CONFIG[mode]["sentence_limit"])
    limit = sentence_limit if sentence_limit is not None else configured_limit

    def add(
        code: str,
        start: int,
        end: int,
        detail: str = "",
        suggestion: str | None = None,
    ) -> None:
        severity = severity_for(mode, code)
        if severity == "off":
            return
        rule = RULES[code]
        line, column = location(starts, start)
        message = rule.title + (f": {detail}" if detail else "")
        findings.append(
            Finding(
                path=path,
                line=line,
                column=column,
                code=code,
                severity=severity,
                message=message,
                suggestion=suggestion or rule.suggestion,
                excerpt=excerpt(text, start, end),
            )
        )

    for start, end in sentences:
        words = WORD_RE.findall(view[start:end])
        if len(words) > limit:
            add(
                "CLR001",
                start,
                end,
                f"{len(words)} words; limit is {limit} in {mode} mode",
            )

    paragraph_limit = int(MODE_CONFIG[mode]["paragraph_limit"])
    for start, end in paragraphs:
        count = sum(
            child_start >= start and child_end <= end
            for child_start, child_end in sentences
        )
        if count > paragraph_limit:
            add(
                "CLR002",
                start,
                end,
                f"{count} sentences; limit is {paragraph_limit} in {mode} mode",
            )

    for match in re.finditer(";", view):
        add("CLR003", match.start(), match.end())

    for match in CONTRACTION_RE.finditer(view):
        add("CLR004", match.start(), match.end())

    for match in PASSIVE_RE.finditer(view):
        participle = match.group("participle").lower()
        if participle not in FALSE_PASSIVE_PARTICIPLES:
            add("CLR005", match.start(), match.end())

    for match in PROGRESSIVE_RE.finditer(view):
        add("CLR006", match.start(), match.end())

    for phrase, match in phrase_matches(view, NOMINAL_PHRASES):
        add(
            "CLR007",
            match.start(),
            match.end(),
            repr(phrase),
            f"Use {NOMINAL_PHRASES[phrase]!r}.",
        )

    general_nominal = re.compile(
        r"\b(?:perform|performs|performed|conduct|conducts|conducted|provide|"
        r"provides|provided)\s+(?:an?|the)\s+\w{4,}(?:tion|ment|ance|ence)\b",
        re.IGNORECASE,
    )
    for match in general_nominal.finditer(view):
        if not any(
            item.code == "CLR007"
            and item.line == location(starts, match.start())[0]
            and item.column == location(starts, match.start())[1]
            for item in findings
        ):
            add("CLR007", match.start(), match.end())

    for phrase, match in phrase_matches(view, PHRASAL):
        add(
            "CLR008",
            match.start(),
            match.end(),
            repr(phrase),
            f"Use {PHRASAL[phrase]}.",
        )

    for phrase, match in phrase_matches(view, INFLATED):
        add(
            "WRD001",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {INFLATED[phrase]}.",
        )

    for phrase, match in phrase_matches(view, PROMOTIONAL):
        if phrase == "robust" and re.match(
            r"\s+(?:regression|statistic(?:s|al)?|estimator|standard errors?|control)\b",
            view[match.end() :],
            re.IGNORECASE,
        ):
            continue
        add("WRD002", match.start(), match.end(), repr(phrase))

    for phrase, match in phrase_matches(view, HEDGES):
        add(
            "WRD003",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {HEDGES[phrase]}.",
        )

    for phrase, match in phrase_matches(view, CLICHES):
        add(
            "WRD004",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {CLICHES[phrase]}.",
        )

    for phrase, match in phrase_matches(view, VAGUE):
        add(
            "WRD005",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {VAGUE[phrase]}.",
        )

    for phrase, match in phrase_matches(view, WEASEL_ATTRIBUTIONS):
        add(
            "WRD006",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {WEASEL_ATTRIBUTIONS[phrase]}.",
        )

    for phrase, match in phrase_matches(view, IMPORTANCE_PUFFERY):
        add(
            "WRD007",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {IMPORTANCE_PUFFERY[phrase]}.",
        )

    for match in FORMULAIC_CONTRAST_RE.finditer(view):
        add("WRD008", match.start(), match.end())

    for phrase, match in phrase_matches(view, GENERIC_ENDINGS):
        add(
            "WRD009",
            match.start(),
            match.end(),
            repr(phrase),
            f"Rewrite: {GENERIC_ENDINGS[phrase]}.",
        )

    for match in PARTICIPIAL_GLOSS_RE.finditer(view):
        sentence_start = max(
            view.rfind(".", 0, match.start()),
            view.rfind("!", 0, match.start()),
            view.rfind("?", 0, match.start()),
            view.rfind("\n", 0, match.start()),
        )
        evidence = view[sentence_start + 1 : match.start()]
        if re.search(
            r"(?:\d|according to|benchmark|data|measure|report|study|test)",
            evidence,
            re.IGNORECASE,
        ):
            continue
        add("WRD010", match.start(), match.end())

    for phrase, match in phrase_matches(view, AI_DICTION):
        add("WRD011", match.start(), match.end(), repr(phrase))

    for match in DIRECT_BINARY_RE.finditer(view):
        add("STR001", match.start(), match.end())
    for match in FAUX_INSIGHT_RE.finditer(view):
        add("STR002", match.start(), match.end())
    for match in COLON_REVEAL_RE.finditer(view):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end == -1:
            line_end = len(text)
        original_line = text[line_start:line_end]
        if re.match(r"\s*(?:[-+*]|\d+[.)]|#|>)\s+", original_line):
            continue
        label = view[match.start() : match.end()].split(":", 1)[0].strip()
        if TECHNICAL_LABEL_RE.fullmatch(label):
            continue
        add("STR003", match.start(), match.end())
    for match in NEGATIVE_LIST_RE.finditer(view):
        add("STR004", match.start(), match.end())
    for match in DRAMATIC_STACK_RE.finditer(view):
        add("STR005", match.start(), match.end())
    for match in QUESTION_ANSWER_RE.finditer(view):
        add("STR006", match.start(), match.end())
    for match in SYNTHESIS_RE.finditer(view):
        add("STR007", match.start(), match.end())
    for match in CONCESSIVE_LOOP_RE.finditer(view):
        add("STR014", match.start(), match.end())
    for match in NARRATOR_SCAFFOLD_RE.finditer(view):
        add("STR015", match.start(), match.end())
    for match in ABSTRACT_EVIDENCE_RE.finditer(view):
        add("STR016", match.start(), match.end())
    for match in GENERIC_HEADING_RE.finditer(text):
        add("STR008", match.start(), match.end())
    for match in HEADING_EMOJI_RE.finditer(text):
        add("STR009", match.start(), match.end())
    for match in BOLD_EMPHASIS_RE.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end].strip()
        value = match.group()[2:-2].strip()
        if re.match(r"\s*(?:[-+*]|\d+[.)])\s+", text[line_start:match.start()]):
            continue
        if line == match.group().strip():
            continue
        if value.endswith(":") or (
            re.fullmatch(r"[A-Za-z0-9_./:@#-]+", value)
            and re.search(r"[0-9_./:@#-]", value)
        ):
            continue
        add("STR010", match.start(), match.end())

    heading_matches = list(re.finditer(r"(?m)^\s*#{1,6}\s+.+$", text))
    for index, match in enumerate(heading_matches):
        section_end = (
            heading_matches[index + 1].start()
            if index + 1 < len(heading_matches)
            else len(text)
        )
        body = sanitize_markdown(text[match.end():section_end])
        if 0 < len(sentence_spans(body)) <= 2 and len(WORD_RE.findall(body)) < 55:
            add("STR011", match.start(), match.end())

    list_runs: list[list[re.Match[str]]] = []
    current: list[re.Match[str]] = []
    previous_line = -2
    for match in re.finditer(r"(?m)^\s*(?:[-+*]|\d+[.)])\s+(.+)$", text):
        line = text.count("\n", 0, match.start())
        if line > previous_line + 1 and current:
            list_runs.append(current)
            current = []
        current.append(match)
        previous_line = line
    if current:
        list_runs.append(current)
    for run in list_runs:
        long_items = sum(len(WORD_RE.findall(item.group(1))) >= 12 for item in run)
        if len(run) >= 5 and long_items >= 3:
            add(
                "STR012",
                run[0].start(),
                run[-1].end(),
                f"{len(run)} items; {long_items} read like prose",
            )

    for paragraph_start, paragraph_end in paragraphs:
        opening_counts: dict[str, list[tuple[int, int]]] = {}
        for start, end in sentences:
            if start < paragraph_start or end > paragraph_end:
                continue
            words = [word.lower() for word in WORD_RE.findall(view[start:end])[:2]]
            if len(words) == 2:
                opening_counts.setdefault(" ".join(words), []).append((start, end))
        for opening, spans in opening_counts.items():
            if len(spans) >= 4:
                start, end = spans[3]
                add(
                    "STR013",
                    start,
                    end,
                    f"{opening!r} starts {len(spans)} sentences in one paragraph",
                )

    for match in REPEATED_WORD_RE.finditer(view):
        if match.group(1).lower() not in ALLOWED_REPEATS:
            add("TXT001", match.start(), match.end(), repr(match.group(0)))

    em_dashes = list(re.finditer("—", view))
    word_total = len(WORD_RE.findall(view))
    dash_limit = max(1, (word_total + 199) // 200)
    for match in em_dashes[dash_limit:]:
        add(
            "TXT002",
            match.start(),
            match.end(),
            f"{len(em_dashes)} em dashes; review starts after {dash_limit}",
        )

    findings.sort(key=lambda item: (item.line, item.column, item.code))
    return LintResult(
        path=path,
        words=len(WORD_RE.findall(view)),
        sentences=len(sentences),
        paragraphs=len(paragraphs),
        findings=findings,
    )


def expand_paths(patterns: Sequence[str]) -> list[Path]:
    paths: list[Path] = []
    seen: set[str] = set()
    for pattern in patterns:
        matches = sorted(glob.glob(pattern, recursive=True)) if glob.has_magic(pattern) else [pattern]
        for item in matches:
            resolved = str(Path(item))
            if resolved not in seen:
                paths.append(Path(item))
                seen.add(resolved)
    return paths


def render_human(results: Sequence[LintResult], mode: str) -> str:
    lines: list[str] = []
    for result in results:
        for item in result.findings:
            lines.append(
                f"{item.path}:{item.line}:{item.column}: "
                f"{item.severity} {item.code} {item.message}"
            )
            if item.excerpt:
                lines.append(f"  {item.excerpt}")
            lines.append(f"  Fix: {item.suggestion}")
        lines.append(
            f"{result.path}: {result.errors} error(s), {result.warnings} warning(s), "
            f"{result.words} word(s), {result.sentences} sentence(s)"
        )
    errors = sum(result.errors for result in results)
    warnings = sum(result.warnings for result in results)
    lines.append(
        f"Summary: {errors} error(s), {warnings} warning(s) in "
        f"{len(results)} input(s); mode={mode}"
    )
    return "\n".join(lines)


def render_json(results: Sequence[LintResult], mode: str) -> str:
    errors = sum(result.errors for result in results)
    warnings = sum(result.warnings for result in results)
    payload = {
        "tool": "plain-writing",
        "version": VERSION,
        "mode": mode,
        "certification": "none",
        "summary": {
            "files": len(results),
            "errors": errors,
            "warnings": warnings,
        },
        "files": [result.to_dict() for result in results],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def threshold_failed(results: Sequence[LintResult], fail_on: str) -> bool:
    if fail_on == "never":
        return False
    if fail_on == "warning":
        return any(result.errors or result.warnings for result in results)
    return any(result.errors for result in results)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Lint prose for clarity, fidelity, and common forms of empty "
            "language. This tool does not certify an external standard."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Text or Markdown files and glob patterns. Read stdin when omitted.",
    )
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="technical",
        help="Language mode. Default: technical.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        dest="output_format",
        help="Output format. Default: human.",
    )
    parser.add_argument(
        "--fail-on",
        choices=("error", "warning", "never"),
        default="error",
        help="Finding level that returns exit status 1. Default: error.",
    )
    parser.add_argument(
        "--sentence-limit",
        type=int,
        help="Override the selected mode's sentence word limit.",
    )
    parser.add_argument(
        "--list-rules",
        action="store_true",
        help="List rule IDs and their levels for the selected mode.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser


def list_rules(mode: str) -> str:
    lines = []
    for code, rule in RULES.items():
        lines.append(f"{code}\t{severity_for(mode, code)}\t{rule.title}")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.sentence_limit is not None and args.sentence_limit < 1:
        parser.error("--sentence-limit must be greater than zero")

    if args.list_rules:
        print(list_rules(args.mode))
        return 0

    results: list[LintResult] = []
    try:
        if args.paths:
            paths = expand_paths(args.paths)
            if not paths:
                raise OSError("no input files matched")
            for path in paths:
                if not path.exists():
                    raise OSError(f"input does not exist: {path}")
                if not path.is_file():
                    raise OSError(f"input is not a file: {path}")
                text = path.read_text(encoding="utf-8")
                results.append(
                    lint_text(
                        text,
                        path=str(path),
                        mode=args.mode,
                        sentence_limit=args.sentence_limit,
                    )
                )
        else:
            results.append(
                lint_text(
                    sys.stdin.read(),
                    path="<stdin>",
                    mode=args.mode,
                    sentence_limit=args.sentence_limit,
                )
            )
    except (OSError, UnicodeError) as error:
        print(f"lint_prose.py: error: {error}", file=sys.stderr)
        return 2

    if args.output_format == "json":
        print(render_json(results, args.mode))
    else:
        print(render_human(results, args.mode))

    return 1 if threshold_failed(results, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
