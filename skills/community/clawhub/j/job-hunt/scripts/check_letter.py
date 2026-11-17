#!/usr/bin/env python3
"""Gate: the letter constraints render_letter.py will not enforce.

render_letter passes each body string straight into Markdown and LaTeX
with no stripping (Word now refuses source markup), so '**bold**' prints four
asterisks on the PDF and a sender
name written into `closing` prints twice — the renderer appends it already.
These are exact string and count checks documented only in prose today, which is
the same failure class as a format string rendered raw onto a slide.

Misspelling the company or role is called disqualifying in the reference and is
checked by reading. posting.yaml is a required artifact, so it can be checked by
comparing.

Exit 0 = clean. Exit 1 = findings. Exit 2 = missing letter.yaml or posting.yaml.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import unicodedata


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal
import render_letter

import prose_tells

GATE = "check_letter"
# motivation-letter.md:119 — "250–350 words optimal for the body … 400 words is
# the hard ceiling". :121 — "3–4 paragraphs total … Never more than 4 unless a
# specific structure requires it (rare)." A gate that permitted 5 would be
# enforcing a rule the reference it cites does not contain.
WORD_MIN, WORD_MAX = 250, 400
PARA_MIN, PARA_MAX = 3, 4

MARKUP = [
    ("**", re.compile(r"\*\*")),
    ("__", re.compile(r"__")),
    ("`", re.compile(r"`")),
    ("a leading bullet", re.compile(r"(^|\n)\s*[-*+]\s+")),
    ("a leading heading", re.compile(r"(^|\n)\s*#{1,6}\s+")),
]
_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def _norm(s) -> str:
    s = unicodedata.normalize("NFKC", str(s or "")).lower()
    return " ".join(_PUNCT.sub(" ", s).split())


# The gender marker a German, Austrian, Swiss, French or Dutch posting appends to
# its title by law or custom: "Data Scientist (m/w/d)", "(f/m/x)", "(H/F)",
# "(m/v)", "(all genders)". It is part of the advert, never of the role, and no
# letter repeats it — so ROLE_NOT_NAMED fired on a letter that named
# "Data Scientist" exactly as it should.
_GENDER_TOKEN = r"(?:m|w|f|d|x|h|v|div\.?|divers|diverse)"
_GENDER_MARKER = re.compile(
    r"[(\[]\s*" + _GENDER_TOKEN + r"(?:\s*[/|,]\s*" + _GENDER_TOKEN + r"){1,3}\s*[)\]]"
    r"|[(\[]\s*(?:all genders|alle geschlechter|gn|genderneutral)\s*[)\]]"
    r"|(?:^|\s)[-–—|,]?\s*" + _GENDER_TOKEN + r"(?:\s*/\s*" + _GENDER_TOKEN
    + r"){1,3}\s*$",
    re.IGNORECASE)


def role_without_gender_marker(role) -> str:
    return " ".join(_GENDER_MARKER.sub(" ", str(role or "")).split())


# `——` is ONE punctuation mark in Chinese (破折号), typed as two U+2014. Counted
# per character it doubled the em-dash density of every Chinese letter, so two
# ordinary uses read as four and tripped EM_DASH_DENSITY's floor of three.
_DOUBLE_EM_DASH = re.compile("\u2014{2,}")


def _dash_marks_as_written(text: str) -> str:
    return _DOUBLE_EM_DASH.sub("\u2014", text)


# Salutation and sign-off forms whose language is unambiguous, for the languages
# render_letter has sourced lines for (references/motivation-letter.md §4) plus
# Portuguese, which the body detector also names. A line that matches none of
# these is not judged: an unrecognised greeting is not evidence of a mismatch.
_LINE_MARKERS = {
    "en": re.compile(r"^(dear|hi|hello)\b|^to whom it may concern|\b(sincerely|"
                     r"(kind|best|warm) regards|regards|yours (sincerely|faithfully|"
                     r"truly)|best wishes|respectfully)\b", re.I),
    "de": re.compile(r"^(sehr geehrte[rs]?|liebe[rs]?|guten tag)\b|\b(mit "
                     r"freundlichen grü(ß|ss)en|freundliche grü(ß|ss)e|beste "
                     r"grü(ß|ss)e|viele grü(ß|ss)e|hochachtungsvoll)\b", re.I),
    "nl": re.compile(r"^(geachte|beste)\b(?!\s+grü)|\b(met vriendelijke groet(en)?|"
                     r"vriendelijke groet(en)?|met hartelijke groet(en)?|"
                     r"hoogachtend)\b", re.I),
    "fr": re.compile(r"^(madame|monsieur|bonjour|chère|cher)\b|\b(cordialement|"
                     r"bien à vous|veuillez agréer|salutations distinguées)\b", re.I),
    "es": re.compile(r"^(estimad[oa]s?|apreciad[oa]s?|señor[ae]s?)\b|\b(atentamente|"
                     r"un saludo|saludos cordiales|cordialmente)\b", re.I),
    "it": re.compile(r"^(gentil[ei]|egregi[oa]|spettabile|caro|cara)\b|\b(cordiali "
                     r"saluti|distinti saluti|cordialmente)\b", re.I),
    "pt": re.compile(r"^(prezad[oa]s?|caro|cara)\b|\b(atenciosamente|cordialmente|"
                     r"com os melhores cumprimentos)\b", re.I),
}
_CJK_LANGUAGES_SET = frozenset({"zh", "ja", "ko"})
_LANGUAGE_NAMES = {"en": "English", "de": "German", "nl": "Dutch", "fr": "French",
                   "es": "Spanish", "it": "Italian", "pt": "Portuguese",
                   "zh": "Chinese", "ja": "Japanese", "ko": "Korean"}
# A CJK greeting on a letter whose body is a few per cent CJK (a company name)
# is a mismatch; on a body that is a sixth CJK it is a mixed Chinese letter.
_CJK_SHARE_FOR_MIXED = 0.10


def _named(lang) -> str:
    return f"{_LANGUAGE_NAMES.get(lang, lang)} ({lang})"


def _line_language(line: str):
    """A set of Latin-script language codes when the line carries a known form
    ("Dear 张伟," is English), else 'cjk' for a line in CJK script, else None."""
    found = {lang for lang, rx in _LINE_MARKERS.items() if rx.search(line.strip())}
    if found:
        return found
    if render_letter.cjk_count(render_letter.script_counts(line)):
        return "cjk"
    return None


def language_mismatches(resolved: dict) -> list:
    """SALUTATION_/CLOSING_LANGUAGE_MISMATCH for a rendered line in another language.

    The reference is the body's own language when the body settles it, and the
    declared `meta.language` (or the workspace profile's) when it does not.
    `motivation-letter.md`: never mix languages in one letter — and the commonest
    way to mix them was the renderer's own English default on a letter whose
    language it had not been told.
    """
    body = render_letter.body_text(resolved)
    reference = render_letter.infer_language(body)
    source = "the body reads as"
    if reference is None:
        reference = render_letter.declared_language(resolved) or None
        source = "meta.language is"
    if reference is None:
        return []
    counts = render_letter.script_counts(body)
    cjk = render_letter.cjk_count(counts)
    body_cjk_share = cjk / max(1, cjk + counts["latin"])
    out = []
    for field, line in (("salutation", render_letter.salutation_for(resolved)),
                        ("closing", render_letter.closing_for(resolved))):
        line = str(line or "").strip()
        if not line:
            continue
        found = _line_language(line)
        if isinstance(found, set):
            line_is = "is " + " or ".join(_named(x) for x in sorted(found))
        elif found == "cjk":
            line_is = "is in CJK script"
        else:
            line_is = "is not in CJK script"
        if reference in _CJK_LANGUAGES_SET:
            wrong = found != "cjk"
        elif found == "cjk":
            wrong = body_cjk_share < _CJK_SHARE_FOR_MIXED
        else:
            wrong = isinstance(found, set) and reference not in found
        if not wrong:
            continue
        written = bool(str(resolved.get(field) or "").strip())
        fix = ("Rewrite it in the letter's own language" if written else
               f"It is render_letter's default for language "
               f"{render_letter._language(resolved)!r}; set meta.language to the "
               f"letter's language, or write the {field} yourself")
        out.append(f"{field.upper()}_LANGUAGE_MISMATCH: the {field} {line!r} "
                   f"{line_is}, but {source} {_named(reference)} — "
                   f"motivation-letter.md: never mix languages in one letter. {fix}")
    return out


def findings_for(letter: dict, posting: dict, workspace=None) -> list:
    """`workspace` is the application directory: the letter's meta is completed
    from it exactly as render_letter completes it, so the gate judges the letter
    that is actually rendered."""
    out = []
    resolved, _ = render_letter.resolved_letter(letter, workspace)
    body = letter.get("body") or []
    if isinstance(body, str):
        body = [body]

    # The letter is where machine prose is most detectable — a CV bullet is terse
    # by design, a letter is 300 words of connected prose — and until now it was
    # the ONE artifact with no cliché or AI-tell check at all. A letter carrying
    # results-driven, spearheading, pivotal, leverage, robust, delve, intricate,
    # realm, showcasing, "not just X — it is Y", three tricolons and three em
    # dashes passed this gate reporting only its word count.
    joined = "\n".join(str(p) for p in body)
    out += prose_tells.vocabulary_findings(joined, "letter.yaml body")
    out += prose_tells.prose_findings(_dash_marks_as_written(joined), "letter.yaml body")

    for i, para in enumerate(body):
        hits = [label for label, rx in MARKUP if rx.search(str(para))]
        if hits:
            out.append(f"MARKDOWN_IN_BODY: body[{i}] contains "
                       f"{', '.join(repr(h) for h in hits)} — render_letter prints "
                       f"body strings verbatim, so this renders literally "
                       f"(**bold** prints four asterisks)")

    # A salutation or sign-off the skill cannot source is a hole the WRITER has
    # to fill, and the gate is what stops it shipping. render_letter used to put
    # "Dear Hiring Manager," / "Sincerely," on every letter regardless of
    # language — against motivation-letter.md:272, "Never mix languages in one
    # letter" — and nothing said so.
    # `resolved`, not `letter`: with no meta.language the renderer now takes the
    # language from the body, and the gate has to judge that same choice. It used
    # to read meta.language alone with "en" as the default, so a Chinese letter
    # written to the documented schema — no meta — was told it was covered by
    # "Dear Hiring Team," and passed.
    language = render_letter._language(resolved)
    for field, code in (("salutation", "NO_SALUTATION"), ("closing", "NO_CLOSING")):
        if str(letter.get(field) or "").strip():
            continue
        if getattr(render_letter, f"{field}_for")(resolved):
            continue          # a sourced default covers this language
        out.append(f"{code}: letter.yaml has no {field} and this skill has no "
                   f"sourced {field} for language {language!r}, so the rendered "
                   f"letter has none. Write one in the letter's own language "
                   f"(motivation-letter.md: never mix languages in one letter)")
    out += language_mismatches(resolved)

    joined = " ".join(str(p) for p in body)
    if not cjk_dominant(joined, _letter_language(letter)):
        words = sum(len(str(p).split()) for p in body)
        if not (WORD_MIN <= words <= WORD_MAX):
            out.append(f"WORD_COUNT: the body is {words} words; the target is "
                       f"{WORD_MIN}–350 with {WORD_MAX} as the hard ceiling")
    if not (PARA_MIN <= len(body) <= PARA_MAX):
        out.append(f"PARA_COUNT: the body has {len(body)} paragraphs; "
                   f"{PARA_MIN}–{PARA_MAX} is the range (motivation-letter.md: "
                   f"never a single monolithic block, never more than 4)")

    sender = str((letter.get("sender") or {}).get("name") or "").strip()
    closing = str(letter.get("closing") or "")
    if sender and _norm(sender) and _norm(sender) in _norm(closing):
        out.append(f"NAME_DUPLICATED: closing contains the sender name {sender!r}; "
                   f"render_letter appends it automatically, so it prints twice")

    posted_company = str(posting.get("company") or "").strip()
    letter_company = str((letter.get("recipient") or {}).get("company") or "").strip()
    if not posted_company:
        out.append("NO_COMPANY_IN_POSTING: posting.yaml has no `company` field, so the "
                   "letter's recipient cannot be verified — add it to the extracted "
                   "posting (misspelling the employer is disqualifying)")
    elif not letter_company:
        out.append(f"COMPANY_MISMATCH: letter.yaml has no recipient.company; the "
                   f"posting names {posted_company!r}")
    else:
        a, b = _norm(letter_company), _norm(posted_company)
        if a not in b and b not in a:
            out.append(f"COMPANY_MISMATCH: recipient.company {letter_company!r} does "
                       f"not match the posting's company {posted_company!r}")

    role = str(posting.get("role_title") or "").strip()
    needle = _norm(role_without_gender_marker(role)) or _norm(role)
    if role and needle not in _norm(" ".join(str(p) for p in body)):
        out.append(f"ROLE_NOT_NAMED: the body never names the role {role!r} as the "
                   f"posting writes it — name it exactly once, early")
    return out


# `250-350 words` comes from motivation-letter.md:120, which is a rule about
# ENGLISH words, and `len(str(p).split())` is a rule about spaces. Chinese and
# Japanese have neither: a 306-character Chinese letter counted as "3 words" and
# failed WORD_COUNT, and a 702-character Japanese one as "3". The gate could
# never pass for those languages, and a gate that cannot be satisfied is one
# people route around.
#
# The band is NOT rescaled here, because this skill has no sourced length
# convention for a CJK letter and inventing one would be the fabrication it bans
# everywhere else. What the word count is really protecting — "stays comfortably
# on one page when rendered", motivation-letter.md:120 — is measured directly by
# check_pages on the rendered letter PDF. So the honest report is the real count
# and no verdict.
_CJK_RANGE = (
    ("\u3040", "\u30ff"),   # kana
    ("\u3400", "\u4dbf"),   # CJK ext A
    ("\u4e00", "\u9fff"),   # CJK unified
    ("\uac00", "\ud7af"),   # hangul
)


def _letter_language(letter) -> str:
    meta = letter.get("meta") if isinstance(letter.get("meta"), dict) else {}
    return str(meta.get("language") or "").strip().lower()[:2]


def _cjk_count(text: str) -> int:
    return sum(1 for ch in text
               if any(lo <= ch <= hi for lo, hi in _CJK_RANGE))


# The languages whose letters this band cannot measure at all.
_CJK_LANGUAGES = ("zh", "ja", "ko")


def cjk_dominant(text: str, language=None) -> bool:
    """Whether the English word band can measure this letter.

    `meta.language` wins when it names one of these, and the ratio is only the
    fallback. A Chinese letter to a multinational keeps team names, levels and
    tool names in English — the ordinary, honest register — and enough of them
    flips a character ratio, at which point a 105-word Chinese letter was
    scored against a 250-word English band it can never meet. The candidate
    declared the language; that is better evidence than counting glyphs.
    """
    if str(language or "").strip().lower()[:2] in _CJK_LANGUAGES:
        return True
    latin = sum(1 for ch in text if "a" <= ch.lower() <= "z")
    return _cjk_count(text) > latin


def notices_for(letter: dict) -> list:
    """Reports that are not verdicts. Printed to stderr; never a finding."""
    body = letter.get("body") or []
    body = [body] if isinstance(body, str) else body
    joined = " ".join(str(p) for p in body)
    if not joined.strip() or not cjk_dominant(joined, _letter_language(letter)):
        return []
    return [
        f"NOTICE_CJK_LENGTH_UNSCORED: the body is {_cjk_count(joined)} CJK "
        f"characters in {len(body)} paragraphs. The {WORD_MIN}-350 band is an "
        f"English word count and this skill has no sourced length convention for "
        f"a CJK letter, so it is not applied. The one-page constraint behind it "
        f"is checked by check_pages on the rendered PDF."
    ]


def profile_inputs(letter: dict, workspace) -> list:
    """The workspace profiles this verdict depends on, in render_letter's order.

    `findings_for` reads the letter as render_letter resolves it, and the one
    resolved key that changes a finding is `language`: it picks the sourced
    salutation and closing (NO_SALUTATION / NO_CLOSING) and is the reference for
    the *_LANGUAGE_MISMATCH lines. It comes from the workspace profile only when
    letter.yaml states no `meta.language` and the body does not settle it — then
    a tailored-profile.yaml edit alone can turn this gate's pass into a fail, and
    a receipt that hashed only letter.yaml and posting.yaml went on vouching for
    a letter whose verdict had changed (check_apply's STALE_RECEIPT re-hashes
    exactly the files a receipt names, nothing else).

    Each profile up to and including the first one with a `meta` mapping counts:
    the earlier ones decide by HAVING no meta which file is read. When the letter
    settles its own language the list is empty, so a CV edit does not stale the
    letter's receipt.
    """
    if (render_letter.declared_language(letter)
            or render_letter.infer_language(render_letter.body_text(letter))):
        return []
    ws = pathlib.Path(workspace)
    out = []
    for name in render_letter._WORKSPACE_PROFILES:
        path = ws / name
        if not path.is_file():
            continue
        out.append(path)
        if journal.as_mapping(render_letter._read_mapping(path).get("meta")):
            break
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--letter", default=None, help="default: <workspace>/letter.yaml")
    ap.add_argument("--posting", default=None, help="default: <workspace>/posting.yaml")
    args = ap.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    lp = pathlib.Path(args.letter) if args.letter else ws / "letter.yaml"
    pp = pathlib.Path(args.posting) if args.posting else ws / "posting.yaml"
    for p in (lp, pp):
        if not p.exists():
            journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {p}"])
            print(f"cannot run {GATE}: {p} does not exist", file=sys.stderr)
            return 2
    try:
        letter = journal.load_yaml(lp)
        posting = journal.load_yaml(pp)
    except journal.YamlUnreadable as exc:
        journal.receipt(ws, GATE, {}, "could_not_run", [exc.finding])
        print(f"cannot run {GATE}: {exc}", file=sys.stderr)
        return 2
    findings = findings_for(letter, posting, workspace=ws)
    for f in findings:
        print(f)
    for notice in notices_for(letter):
        print(notice, file=sys.stderr)
    hashes = {lp.name: journal.sha256_file(lp), pp.name: journal.sha256_file(pp)}
    hashes.update({p.name: journal.sha256_file(p) for p in profile_inputs(letter, ws)})
    journal.receipt(ws, GATE, hashes, "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
