#!/usr/bin/env python3
"""Save a master profile without destroying the ones already there.

One candidate has one CV per language, not one CV. A returning user with an
English master who supplies a Chinese one has TWO masters: a Chinese CV is a
different document with different conventions, length rules and personal-data
expectations, not a translation of the English one. Overwriting is silent data
loss the user discovers only when they next need the file that is gone.

So:

  same language as an existing master  -> overwrite it, after a dated backup
  a language no master covers yet      -> a new file; nothing else is touched
  no `meta.language` at all            -> refused, because the unsuffixed slot
                                          is where a legacy English master
                                          usually lives and dropping an untagged
                                          CV there is exactly the overwrite this
                                          script exists to prevent

**The language comes from the file, never from the filename.** The renderer, the
heading tables and the letter salutations all key off `meta.language`; a filename
reaches none of them, so a `profile.en.yaml` whose content says `zh` is a Chinese
master and is treated as one.

**The legacy slot is resolved, not recomputed.** A user whose only master is
`profile.yaml` with `meta.language: en` gets a NEW English CV written back to
`profile.yaml` — not to a second file called `profile.en.yaml`. Two masters for
one language is the same defect as an overwrite, arriving from the other side.

Exit codes follow the gate contract although this is not a gate: 0 saved,
2 could not run. Never 1.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import shutil
import sys

import journal
import paths


def language_of(profile: dict) -> str:
    return paths.normalise_language((profile.get("meta") or {}).get("language"))


def resolve_target(name: str, language: str) -> tuple[pathlib.Path, pathlib.Path | None]:
    """(where this language's master goes, the file it replaces or None).

    Existing masters win over a computed path. `master_profiles` reads each
    file's own `meta.language`, so a legacy `profile.yaml` holding an English CV
    IS the English slot and a new English CV belongs in it.
    """
    existing = paths.master_profiles(name)
    if language in existing:
        return existing[language], existing[language]
    return paths.master_profile(name, language), None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True, help="candidate name or slug")
    ap.add_argument("--profile", required=True, type=pathlib.Path,
                    help="the profile YAML to save as a master")
    ap.add_argument("--dry-run", action="store_true",
                    help="say what would happen and write nothing")
    args = ap.parse_args(argv)

    src = args.profile.expanduser()
    if not src.is_file():
        print(f"SAVE_NO_PROFILE: {src} is not a file", file=sys.stderr)
        return 2
    try:
        loaded = journal.load_yaml(src)
    except journal.YamlUnreadable as exc:
        print(f"SAVE_UNREADABLE: {exc.finding}", file=sys.stderr)
        return 2

    language = language_of(loaded)
    if not language:
        print("SAVE_NO_LANGUAGE: this profile sets no meta.language, and the "
              "unsuffixed profile.yaml slot is where a legacy master usually "
              "lives — writing an untagged CV there is the overwrite this script "
              "exists to prevent. Set meta.language (e.g. en, zh, nl) and re-run. "
              "It is also what the renderer, the heading tables and the letter "
              "salutations key off, so a CV without it cannot render correctly "
              "either.", file=sys.stderr)
        return 2

    try:
        target, replaced = resolve_target(args.name, language)
    except ValueError as exc:
        print(f"SAVE_BAD_NAME: {exc}", file=sys.stderr)
        return 2

    others = {lang: p for lang, p in paths.master_profiles(args.name).items()
              if p != target}

    if args.dry_run:
        print(f"would write {target}")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        if replaced is not None and replaced.exists():
            # A counter, because three saves in one day left the ORIGINAL
            # unrecoverable: each `.bak-<date>` overwrote the last while both runs
            # printed "backed up".
            stem = f"{replaced.name}.bak-{datetime.date.today().isoformat()}"
            backup = replaced.with_name(stem)
            n = 2
            while backup.exists():
                backup = replaced.with_name(f"{stem}-{n}")
                n += 1
            shutil.copy2(replaced, backup)
            print(f"backed up {replaced.name} -> {backup.name}")
        shutil.copy2(src, target)
        print(f"saved {target}")

    print(f"  language: {language}")
    print(f"  {'replaced' if replaced else 'new slot'}: {target.name}")
    collisions = paths.master_profile_collisions(args.name)
    if collisions:
        for lang, files in sorted(collisions.items()):
            print(f"  WARNING: {lang or '(untagged)'} is claimed by more than one "
                  f"file: {', '.join(f.name for f in files)}. Only "
                  f"{files[0].name} is used; the others are invisible to the "
                  f"provenance gate. Give each a distinct meta.language, or "
                  f"delete the one you do not want.", file=sys.stderr)
    if others:
        print("  untouched masters in other languages:")
        for lang, p in sorted(others.items()):
            print(f"    {lang or '(untagged)'}: {p.name}")
    else:
        print("  no other master profiles for this candidate")
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
