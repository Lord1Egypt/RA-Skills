"""Shared entity-name normalization helpers (stdlib-only).

Used by entity_resolution.py and timing_analysis.py.
"""
from __future__ import annotations

import re
import sys
import unicodedata

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 _normalize.py")
    sys.exit(0)


# Legal suffixes / corporate boilerplate to strip during normalization.
_SUFFIX_TOKENS = {
    "INC", "INCORPORATED", "LLC", "LLP", "LP", "LTD", "LIMITED",
    "CORP", "CORPORATION", "CO", "COMPANY",
    "GROUP", "GRP", "HOLDINGS", "HOLDING",
    "PARTNERS", "ASSOCIATES",
    "INTERNATIONAL", "INTL",
    "ENTERPRISES", "ENTERPRISE",
    "SERVICES", "SERVICE", "SVCS",
    "SOLUTIONS", "MANAGEMENT", "MGMT", "CONSULTING",
    "TECHNOLOGY", "TECHNOLOGIES", "TECH",
    "INDUSTRIES", "INDUSTRY",
    "AMERICA", "AMERICAN",
    "USA", "US",
    "PLLC", "PC",
    "TRUST", "FOUNDATION",
}

_PUNCT_RE = re.compile(r"[^\w\s]")
_WS_RE = re.compile(r"\s+")


def normalize_name(name: str | None) -> str:
    """Standard normalization: uppercase, strip suffixes, drop punctuation."""
    if not name:
        return ""
    # Fold accents FIRST. _PUNCT_RE treats any non-alphanumeric character as
    # punctuation, so an accented letter was replaced by a space and the name split
    # in two, and every downstream consumer saw a mangled string which
    # cannot occur in real text. 19 contacts carried names this destroyed.
    s = _PUNCT_RE.sub(" ", fold_accents(name).upper())
    s = _WS_RE.sub(" ", s).strip()
    tokens = [t for t in s.split() if t and t not in _SUFFIX_TOKENS]
    return " ".join(tokens)


def normalize_aggressive(name: str | None) -> str:
    """Aggressive normalization: sorted unique tokens (word-bag)."""
    base = normalize_name(name)
    if not base:
        return ""
    return " ".join(sorted(set(base.split())))


# Nobiliary particles and connectives, shared by unrelated people ("van Dijk"
# / "van Gogh", "de Silva" / "de Souza"), so they must not count as agreement.
# Dropped ONLY in a MIDDLE position, because several are ordinary names in their
# own right and position is the only thing that tells the two senses apart:
#   final   — the family name, the most identifying part of a name
#             (Das, Le, Santa)
#   first   — a given name (Ben, Al, Van) or the head of a surname. Three
#             contacts named Ben tokenised to their surname alone until this
#             case was added, so they could not match even themselves.
#   middle  — a connective joining the two ("Jan van Dijk"), which is the case
#             this set exists for.
# The same applies to the initials E and Y, which are connectives in Portuguese
# and Spanish but a first initial when they lead a name.
_NAME_PARTICLES = {
    "VAN", "VON", "DER", "DEN", "DE", "DEL", "DELLA", "DI", "DA", "DOS", "DAS",
    "DU", "LA", "LE", "LES", "EL", "AL", "BIN", "IBN", "BEN", "AP", "MAC", "MC",
    "SAN", "SANTA", "ST", "TER", "TEN", "OP", "AM", "ZU", "Y", "E", "OF", "THE",
}

# Personal suffixes and honorifics. Two unrelated people both holding a PhD is
# not evidence they are the same person. These were previously excluded only by
# accident, because min_len=4 happened to drop most of them.
_PERSONAL_SUFFIXES = {
    "PHD", "MD", "DDS", "DVM", "ESQ", "JD", "MBA", "RN", "CPA", "MSW", "PE",
    "DO", "MPH", "EDD", "PSYD", "JR", "SR", "II", "III", "IV", "V",
    "MR", "MRS", "MS", "DR", "PROF",
}


_ACCENT_TRANS = str.maketrans({
    "æ": "ae", "Æ": "AE", "ø": "o", "Ø": "O",
    "ß": "ss", "đ": "d", "Đ": "D", "ł": "l", "Ł": "L",
    "ı": "i", "œ": "oe", "Œ": "OE",
})


def fold_accents(text: str | None) -> str:
    """Base letters only: 'café' -> 'cafe', 'Straße' -> 'Strasse', 'naïve' -> 'naive'.

    Names were matched by stripping every non-[a-z0-9] character from the name being
    looked for while leaving the searched text untouched, so an accented name became
    a string that could not occur at all. Folding BOTH sides is what
    makes them comparable.
    """
    if not text:
        return ""
    text = text.translate(_ACCENT_TRANS)
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))

def name_tokens(name: str | None, min_len: int = 2,
                keep_initials: bool = False) -> set[str]:
    """Token set used for overlap matching.

    min_len is 2 so that real short surnames participate. It was 4, which
    silently deleted Ng, Li, Wu, Xu, Ho, Oh, Mun, Kim, Lee, Liu, Ngo, Das and
    short given names — measured at roughly one contact in seven, skewed
    heavily toward East Asian names. The effect was severe: two IDENTICAL
    strings ("Rhea Ott" vs "Rhea Ott") scored 1 shared token instead of 2 and
    fell below the corroboration threshold, so those contacts were
    systematically under-identified.

    Single characters (initials) are excluded by default, because a middle initial
    is noise when comparing two spelled-out names. Callers that compare a contact
    against a profile's displayed name pass keep_initials=True: without it a name
    whose GIVEN part is initials tokenises to the surname alone, so
    the name cannot even match itself and such contacts are permanently capped at
    family-name agreement. Whoever opts in must also require the family name to be
    among the shared tokens, or "<Given> A. <Family1>" and "<Given> A. <Family2>"
    share two tokens while naming different people.

    Particles and honorifics are excluded by MEANING rather than by length, and a
    particle in final position is kept because there it is the family name
    (Ravi Das, Jenny Le).
    """
    base = normalize_name(name)
    if not base:
        return set()
    parts = base.split()
    last = len(parts) - 1
    out = set()
    for i, t in enumerate(parts):
        if t in _PERSONAL_SUFFIXES:
            continue
        # A single character is an initial: dropped by default, kept for identity
        # corroboration so a name whose given part is initials can match itself.
        if len(t) < min_len and not (keep_initials and len(t) == 1
                                     and t.isalpha()):
            continue
        # Dropped only in a middle position. In final position it is the family
        # name (Ravi Das, Jenny Le); in first position it is either a given name in
        # its own right ("Ben") or part of the surname, and either way it is signal.
        if t in _NAME_PARTICLES and i != last and i != 0:
            continue
        out.add(t)
    return out


def token_overlap_ratio(left: str | None, right: str | None,
                        keep_initials: bool = False) -> tuple[float, int]:
    """Return (jaccard-like ratio, shared token count) over min-len tokens.

    keep_initials is forwarded to name_tokens; see the note there on why identity
    corroboration needs it and what else it requires.
    """
    a = name_tokens(left, keep_initials=keep_initials)
    b = name_tokens(right, keep_initials=keep_initials)
    if not a or not b:
        return 0.0, 0
    shared = a & b
    if not shared:
        return 0.0, 0
    union = a | b
    return len(shared) / len(union), len(shared)
