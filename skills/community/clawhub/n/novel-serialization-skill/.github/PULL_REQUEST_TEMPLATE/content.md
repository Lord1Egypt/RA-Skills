<!-- Template for novel content: chapters, setting docs, character dossiers.
     Use with ?template=content.md
     Novel content is normally committed in the subproject repository, not here.
     Use this template only when content lands in this repository (examples, worked samples). -->

## What this PR contains

- Type: [ ] new content  [ ] revision  [ ] errata  [ ] hygiene
- Object: chapter ___ / file ___

## Summary

<!-- What changed. One paragraph. -->

## Draft-first flow

Content in this repository still follows the draft-first rule:

- [ ] Change landed in a working draft first, not directly in the release file
- [ ] `python scripts/humanizer_check.py <file>` — PASS, or WARN reviewed by a human
- [ ] Review report archived and indexed
- [ ] Release sync done through `_promote_draft.py`, or this is an errata-only edit

## Content gates

- [ ] `python scripts/review_all.py` (or the relevant single-dimension script)
- [ ] `python scripts/scan_hygiene.py --root . --fail-on crlf,junk,mojibake`
- [ ] `python scripts/check_refs.py --root . --kind NONRELEASE` — zero

## Licence

- [ ] Generated content carries the CC BY-NC-SA 4.0 header
- [ ] Chapter files carry YAML frontmatter at byte 0, before the licence header

## Updated

- [ ] CHANGELOG.md
- [ ] progress record (when chapter counts move)

---

Commit format: `type(scope): concise description`
