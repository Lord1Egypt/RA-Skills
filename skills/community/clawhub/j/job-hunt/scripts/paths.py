#!/usr/bin/env python3
"""Every filesystem location job-hunt uses, in one module.

The <company>-<role>-<YYYY-MM-DD> workspace shape is load-bearing: the
"resume an in-progress application" lookup finds a prior run by that shape, so
a mode that invents its own layout orphans the previous workspace and
re-interviews the user from scratch with no error anywhere. Changing
`workspace()` changes that behaviour for every mode at once — which is the
point of it living here rather than in four mode files.

These are pure path builders: nothing here touches the disk. A helper that
created directories would materialise an empty workspace on a typo, and the
resume lookup would then find a shell and offer to continue from it.
"""
from __future__ import annotations

import os
import pathlib
import re
import unicodedata

# `JOBHUNT_PROFILES_ROOT` relocates the whole store. The default stays under
# `.claude` even on another host, on purpose: someone who runs this skill from
# two agents should get ONE set of CVs, not two half-populated ones.
#
# This was added once before and reverted, and the difference matters. The first
# justification was isolating eval runs from the real store, and it was false:
# subagents run in-process and inherit no per-call environment, so the variable
# could not reach them and the comment claiming it did would have been wrong.
# The cross-agent case is a different mechanism — the user exports it in their
# own shell and every script invoked from that shell sees it — which is why it
# is here now. See references/portability.md.
#
# Read once, at import: a run must not move the store halfway through and leave
# half its artifacts behind.
_PROFILES_ENV = os.environ.get("JOBHUNT_PROFILES_ROOT", "").strip()
PROFILES_ROOT = (pathlib.Path(_PROFILES_ENV).expanduser()
                 if _PROFILES_ENV else pathlib.Path.home() / ".claude" / "job-profiles")
# The repo root IS the skill. Every script that needs it asks here rather than
# writing `.parent.parent` again: a hand-derived root is correct until someone
# moves one file, and then it is wrong in a way that only shows up at runtime.
SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Latin letters that no amount of decomposition reduces to an ASCII base. NFKD
# turns é into e+◌́ but leaves ß, ø, ł, đ and æ whole, so they are spelled out.
_LATIN_SPECIALS = str.maketrans({
    "ß": "ss", "ẞ": "ss", "ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae",
    "œ": "oe", "Œ": "oe", "ł": "l", "Ł": "l", "đ": "d", "Đ": "d",
    "þ": "th", "Þ": "th", "ð": "d", "Ð": "d", "ı": "i", "ŧ": "t", "ħ": "h",
})


def _fold_latin(ch: str) -> str:
    """Strip diacritics from LATIN letters only, leaving every other script alone.

    Folding by script matters in both directions. `Müller` and `Möller` were
    both becoming `m-ller` -- two different employers sharing one workspace, so
    the resume lookup offers the wrong prior application, which is precisely the
    failure this module's docstring says it exists to prevent. And folding
    indiscriminately would decompose Thai and Devanagari vowel signs, which are
    letters there, not accents.
    """
    if not unicodedata.name(ch, "").startswith("LATIN"):
        return ch
    return "".join(c for c in unicodedata.normalize("NFKD", ch)
                   if not unicodedata.combining(c))


def _keepable(ch: str) -> bool:
    """Letters and digits of ANY script, plus the combining marks that spell
    words in Thai, Devanagari, Arabic and Hebrew.

    The old rule was an allowlist of four scripts, so a Cyrillic, Greek, Arabic,
    Thai or Devanagari employer slugged to the EMPTY STRING -- and an empty slug
    makes `profile_dir` return PROFILES_ROOT itself, i.e. the shared parent of
    every candidate's private data. `unicodedata.category` is the general rule
    the allowlist was approximating.
    """
    return ch.isalnum() or unicodedata.category(ch).startswith("M")


def slugify(text: str) -> str:
    """A filesystem-safe, script-preserving slug.

    Latin is transliterated down to ASCII so that `Société Générale` and
    `Societe Generale` are one directory; every other script is kept as written,
    because there is no transliteration of `阿里巴巴` or `Яндекс` that a human
    would recognise in a path.
    """
    s = unicodedata.normalize("NFKC", str(text or "")).translate(_LATIN_SPECIALS)
    s = "".join(_fold_latin(ch) for ch in s).casefold()
    out, pending = [], False
    for ch in s:
        if _keepable(ch):
            out.append(ch)
            pending = False
        elif out and not pending:
            out.append("-")
            pending = True
    return "".join(out).strip("-")


def profile_dir(name: str) -> pathlib.Path:
    """<PROFILES_ROOT>/<slug>. Refuses a name that slugs to nothing.

    Without this, `profile_dir("")` returns PROFILES_ROOT itself — the shared
    parent of every candidate's private data — and the caller then writes a
    master profile, an answer bank and every application into the root. Loud is
    the only safe direction: an empty slug is always a caller bug, never a real
    candidate.
    """
    slug = slugify(name)
    if not slug:
        raise ValueError(
            f"name {name!r} contains no letters or digits, so it has no profile "
            f"directory; PROFILES_ROOT is not a profile")
    return PROFILES_ROOT / slug


# One candidate, several CVs — one per language. A returning user who has an
# English CV and then supplies a Chinese one has TWO masters, not a replacement:
# a Chinese CV is a different document with different conventions, not a
# translation of the English one, and overwriting is silent data loss the user
# only discovers when they next need the file that is gone.
#
# The language lives in the FILE (`meta.language`), and the filename only mirrors
# it. `master_profiles` reads the file rather than trusting the name, because a
# name is a claim and the content is the fact.
_LANGUAGE_ALIASES = {
    "english": "en", "en": "en", "en-us": "en", "en-gb": "en", "英文": "en",
    "chinese": "zh", "zh": "zh", "zh-cn": "zh", "zh-hans": "zh", "mandarin": "zh",
    "中文": "zh", "简体中文": "zh", "汉语": "zh",
    "zh-tw": "zh-tw", "zh-hant": "zh-tw", "繁體中文": "zh-tw",
    "dutch": "nl", "nl": "nl", "nederlands": "nl",
    "german": "de", "de": "de", "deutsch": "de",
    "french": "fr", "fr": "fr", "français": "fr", "francais": "fr",
    "spanish": "es", "es": "es", "español": "es", "espanol": "es",
    "italian": "it", "it": "it", "italiano": "it",
    "japanese": "ja", "ja": "ja", "jp": "ja", "日本語": "ja",
    "korean": "ko", "ko": "ko", "kr": "ko", "한국어": "ko",
}


def normalise_language(language) -> str:
    """A language tag reduced to one stable key, or "" when there is none.

    Case, region subtags and the endonym all collapse to the same slot, so
    "English", "en-US" and "英文" cannot become three masters for one CV. An
    unknown language is slugified rather than rejected: this skill writes CVs in
    languages this table has not been taught, and refusing them would be worse
    than filing them under their own name.
    """
    raw = str(language or "").strip().lower()
    if not raw or raw in ("true", "false", "none", "null"):
        # YAML turns `language: no` into False (Norwegian), `on`/`yes` into True.
        # Treating those as a language filed a Norwegian CV under "true".
        return "" if raw in ("true", "false", "none", "null") else ""
    for candidate in (raw, raw.split("-")[0].split("_")[0]):
        if candidate in _LANGUAGE_ALIASES:
            return _LANGUAGE_ALIASES[candidate]
    slug = slugify(raw)
    # The slug can expose a known base the raw form hid: "Chinese (Simplified)"
    # slugs to "chinese-simplified", whose first token IS an alias. Without this
    # the function was NOT IDEMPOTENT — f(x) = "chinese-simplified" while
    # f(f(x)) = "zh" — and `save_profile` looked the master up under one key while
    # `master_profile` built the filename from the other. Measured 2026-09-06: a
    # profile whose meta.language read "Chinese (Simplified)" reported "new slot"
    # and "no other master profiles", took no backup, and overwrote the user's
    # existing profile.zh.yaml. Same for "English (US)", "Dutch (Netherlands)",
    # "French Canadian" and "Japanese (business)".
    head = slug.split("-")[0]
    if head in _LANGUAGE_ALIASES:
        return _LANGUAGE_ALIASES[head]
    return slug


def master_profile(name: str, language=None) -> pathlib.Path:
    """The master for one language. No language means the unsuffixed slot.

    `profile.yaml` stays exactly where it was — every profile saved before this
    existed lives there, and moving it would break `check_claims`' fingerprint,
    apply mode's resume lookup and every path a user has already written down.
    A language-tagged master is `profile.<lang>.yaml` beside it.
    """
    key = normalise_language(language)
    if not key:
        return profile_dir(name) / "profile.yaml"
    return profile_dir(name) / f"profile.{key}.yaml"


def master_profiles(name: str) -> dict:
    """{language key: path} for every master on disk, language read from content.

    The filename is a mirror, not the source: a file called `profile.en.yaml`
    whose `meta.language` says `zh` is filed under `zh`, because the renderer,
    the heading tables and the letter salutations all key off `meta.language`
    and the filename reaches none of them.

    A master with no readable `meta.language` is filed under `""` — the
    unsuffixed slot's ordinary state for profiles written before languages were
    tracked. Unreadable YAML is skipped rather than raising: one corrupt file
    must not hide the others.
    """
    # Imported here, not at module scope: paths.py is imported by scripts that
    # never touch YAML, and journal.py imports nothing from paths.
    import journal

    out = {}
    directory = profile_dir(name)
    if not directory.is_dir():
        return out
    for path in sorted(directory.glob("profile*.yaml")):
        if ".bak" in path.name:
            continue
        try:
            loaded = journal.load_yaml(path)
        except journal.YamlUnreadable:
            continue
        key = normalise_language((loaded.get("meta") or {}).get("language"))
        out.setdefault(key, path)
    return out


def master_profile_collisions(name: str) -> dict:
    """{language: [every file claiming it]} for languages claimed more than once.

    `master_profiles` keeps the first and drops the rest, which is the only
    answer a mapping can give — but dropping SILENTLY meant a candidate with
    `profile.yaml` (language: zh) beside `profile.zh.yaml` (language: 中文) had
    one of the two invisible to the provenance gate, never listed and never
    backed up, while `save_profile` printed "no other master profiles". A caller
    that is about to overwrite has to be able to see the other one.
    """
    import journal

    claims: dict = {}
    directory = profile_dir(name)
    if not directory.is_dir():
        return {}
    for path in sorted(directory.glob("profile*.yaml")):
        if ".bak" in path.name:
            continue
        try:
            loaded = journal.load_yaml(path)
        except journal.YamlUnreadable:
            continue
        claims.setdefault(
            normalise_language((loaded.get("meta") or {}).get("language")), []
        ).append(path)
    return {k: v for k, v in claims.items() if len(v) > 1}


def master_for_language(name: str, language) -> pathlib.Path:
    """The master a run in THIS language must be checked against.

    Existing files win over a computed path, exactly as `save_profile.py`
    resolves a write: a legacy `profile.yaml` holding a Chinese CV IS the Chinese
    master, and `master_profile(name, "zh")` would point past it at a file that
    does not exist.

    WHY THIS EXISTS. `modes/apply.md` told the run to compute
    `paths.master_profile('<name>')` with no language, which always returns
    `profile.yaml`. Once one candidate could have several masters, that pointed
    `check_claims.py` at the wrong one, and the provenance gate — the thing that
    stops this skill inventing credentials — failed in both directions.
    Reproduced 2026-09-06 on a candidate with an English and a Chinese master:

        tailoring the Chinese CV, checked against profile.yaml
          "CUDA" is in the Chinese master and was reported UNSOURCED
          "Kubernetes" is in NEITHER Chinese file and passed, exit 0

    The first is a gate crying wolf at a truthful CV. The second is an unsourced
    claim reaching a rendered CV with the gate green, which is the failure this
    whole skill is built around.
    """
    existing = master_profiles(name)
    key = normalise_language(language)
    if key in existing:
        return existing[key]
    # A master written before languages were tracked carries no meta.language and
    # is filed under "". It is the ONLY CV a pre-existing user has, so falling
    # through to a computed path pointed `check_claims --master` at a file that
    # does not exist and apply mode could not record its baseline at all —
    # `cannot run check_claims: --master must point at an existing profile.yaml`,
    # exit 2, for every candidate onboarded before today.
    if "" in existing:
        return existing[""]
    return master_profile(name, language)


def search_prefs(name: str) -> pathlib.Path:
    return profile_dir(name) / "search-preferences.yaml"


ANSWER_BANK_NAME = "answer-bank.md"


def answer_bank(name: str) -> pathlib.Path:
    return profile_dir(name) / ANSWER_BANK_NAME


ONLINE_PRESENCE_NAME = "online-presence.yaml"


def online_presence(name: str) -> pathlib.Path:
    """The per-person record of public profiles (GitHub, Scholar, website)."""
    return profile_dir(name) / ONLINE_PRESENCE_NAME


def online_presence_dir(name: str) -> pathlib.Path:
    """Snapshots and raw captures of those profiles, beside the record."""
    return profile_dir(name) / "online-presence"


DIGEST_SETTINGS_NAME = "digest.yaml"
DIGEST_SEEN_NAME = "digest-seen.yaml"


def digest_settings(name: str) -> pathlib.Path:
    """The weekly digest's settings and state (references/weekly-digest.md)."""
    return profile_dir(name) / DIGEST_SETTINGS_NAME


def digest_seen(name: str) -> pathlib.Path:
    """Every role a weekly digest has already sent."""
    return profile_dir(name) / DIGEST_SEEN_NAME


def digest_workspace(name: str, date: str) -> pathlib.Path:
    """A fresh discover-shaped workspace for one digest run, never an existing one.

    A retry on the same day gets `-2`, `-3`…: reusing a failed run's directory
    would mix its captures into the new round.
    """
    if not _ISO_DATE.match(str(date)):
        raise ValueError(f"date must be YYYY-MM-DD, got {date!r}")
    base = profile_dir(name) / "searches" / f"{date}-weekly-digest"
    candidate, n = base, 1
    while candidate.exists():
        n += 1
        candidate = base.with_name(f"{base.name}-{n}")
    return candidate


def online_presence_of(workspace) -> pathlib.Path:
    """The online-presence record of the profile that owns an apply or discover workspace.

    Unlike profile_dir_of (applications only, because it routes the answer bank),
    a discover round under searches/ owns a record too.
    """
    workspace = pathlib.Path(workspace)
    if workspace.parent.name not in ("applications", "searches") or len(workspace.parents) < 2:
        raise ValueError(
            f"{workspace} is not a workspace: expected "
            "<profile_dir>/applications/<name> or <profile_dir>/searches/<name>")
    return workspace.parents[1] / ONLINE_PRESENCE_NAME


def search_dir(name: str, slug: str) -> pathlib.Path:
    return profile_dir(name) / "searches" / slugify(slug)


def workspace(name: str, company: str, role: str, date: str) -> pathlib.Path:
    """<profile_dir>/applications/<company>-<role>-<YYYY-MM-DD>.

    `date` is validated rather than slugified: it is the only part of the name
    another run parses back out, and an unparseable one is a workspace nobody
    finds again.
    """
    if not _ISO_DATE.match(str(date)):
        raise ValueError(f"date must be YYYY-MM-DD, got {date!r}")
    for label, value in (("company", company), ("role", role)):
        if not slugify(value):
            raise ValueError(
                f"{label} {value!r} contains no letters or digits, so the "
                f"workspace name would collapse; two such runs would share one "
                f"directory and the resume lookup would offer the wrong one")
    stem = f"{slugify(company)}-{slugify(role)}-{date}"
    return profile_dir(name) / "applications" / stem


def profile_dir_of(workspace) -> pathlib.Path:
    """The profile directory that owns `workspace` — the inverse of workspace().

    Relative to the path given, not to PROFILES_ROOT, so it works on a copied
    workspace or a test fixture. Refuses anything that is not the documented shape
    rather than guessing: a wrong guess here silently writes the answer bank — the one
    artifact that compounds across applications — into the wrong profile.
    """
    workspace = pathlib.Path(workspace)
    if workspace.parent.name != "applications" or len(workspace.parents) < 2:
        raise ValueError(
            f"{workspace} is not a workspace: expected "
            "<profile_dir>/applications/<company>-<role>-<YYYY-MM-DD>"
        )
    return workspace.parents[1]


def answer_bank_of(workspace) -> pathlib.Path:
    """The profile-level answer bank for the profile that owns `workspace`."""
    return profile_dir_of(workspace) / ANSWER_BANK_NAME


def _same_directory(a: pathlib.Path, b: pathlib.Path) -> bool:
    try:
        return os.path.samefile(a, b)
    except OSError:
        return False


def skill_workspace_refusal(workspace, root=None) -> str:
    """Why `workspace` must not hold a run, as one line, or "" when it may.

    A run never lives inside the skill. `modes/discover.md` told agents to run
    `python3 scripts/<gate>.py --workspace .`, and `scripts/` only resolves from
    the skill root, so `.` WAS the skill root: snapshot_profile wrote the
    candidate's private candidate-profile.yaml into the skill directory, which
    git does not ignore, and four discover gates appended journal.jsonl beside
    SKILL.md. Nothing failed, so nothing said so.

    The whole repository is refused, not only its root, because nothing
    legitimately takes a workspace inside it. The in-repo fixtures
    (evals/fixtures/workspaces, scripts/tests/fixtures/mock-dryrun) are copied to
    a temporary directory before anything runs against them, and running a gate
    on the originals would append a receipt to a tracked fixture journal that a
    test pins line for line.

    Resolved the way the calling script resolves it: relative to the current
    directory, symlinks followed, no `~` expansion. `.`, `scripts/..` and a
    symlinked install path are all the same directory, and `samefile` on each
    existing ancestor also catches another spelling of it on a case-insensitive
    disk. Reads the filesystem; never writes to it.
    """
    skill = pathlib.Path(root).resolve() if root else SKILL_ROOT
    try:
        target = pathlib.Path(workspace).resolve()
    except (OSError, RuntimeError, ValueError):
        return ""          # the script reports an unusable path in its own words
    for candidate in (target, *target.parents):
        if candidate == skill or _same_directory(candidate, skill):
            where = "is" if candidate == target else "is inside"
            return (f"WORKSPACE_IN_SKILL: --workspace {str(workspace)!r} {where} the "
                    f"job-hunt skill directory {skill}, so this run's journal, profile "
                    f"snapshot and documents would be written into the skill itself. "
                    f"Pass the run's own directory by absolute path (under "
                    f"{PROFILES_ROOT}/<name>/applications/ or .../searches/), not '.' "
                    f"from the skill root.")
    return ""


def mode_file(mode: str, root=None) -> pathlib.Path:
    """<skill root>/modes/<mode>.md — the layer-1.5 file for a mode."""
    return (pathlib.Path(root) if root else SKILL_ROOT) / "modes" / f"{mode}.md"


def lossless_allowlist(root=None) -> pathlib.Path:
    return (pathlib.Path(root) if root else SKILL_ROOT) / "scripts" / \
        "lossless-allowlist.json"


def main(argv=None) -> int:
    """`paths.py --name … --company … --role …` creates one application workspace
    and prints its absolute path.

    The mode files used to say only "create `paths.workspace(...)`". Every agent
    in the 2026-10-29 simulation then read this file to write its own `python -c`
    call — three runs, three slightly different invocations of the same function.
    """
    import argparse
    import datetime
    import sys

    parser = argparse.ArgumentParser(
        description="Create the application workspace for one posting and print its path.")
    parser.add_argument("--name", required=True, help="the candidate's name as in profile meta.name")
    parser.add_argument("--company", required=True, help="the exact public employer name")
    parser.add_argument("--role", required=True, help="the posting's role title")
    parser.add_argument("--date", help="YYYY-MM-DD; default: today's local date")
    args = parser.parse_args(argv)
    try:
        path = workspace(args.name, args.company, args.role,
                         args.date or datetime.date.today().isoformat())
    except ValueError as exc:
        print(f"cannot run: {exc}", file=sys.stderr)
        return 2
    path.mkdir(parents=True, exist_ok=True)
    print(path.resolve())
    return 0


if __name__ == "__main__":
    import sys

    from cli_io import configure_output

    configure_output()
    sys.exit(main())
