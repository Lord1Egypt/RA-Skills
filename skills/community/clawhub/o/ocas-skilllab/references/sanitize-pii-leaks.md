# Reference-File PII Leak Prevention

Reference files are part of the published skill package. Anything placed in
`references/` will be visible in the repo and may be scraped by security
scanners. These rules are in addition to the credential patterns in
`skill-sanitize-checklist.md`.

## Must abstract, not copy session artifacts

A good reference file teaches a reusable pattern. A bad one copies incident-specific evidence:

- **Wrong:** `verify.py failed with Traceback (most recent call last): File "<fs-root>/.../finch_scan.py", line 182, in <module> ...`
- **Right:** Re-run failures often stem from JSONL field escaping. Parse raw text, split on stable ASCII anchors, and validate `json.load()` after every edit; see the taREDACTED-SECRET reference for the exact recipe.

Rule: if a reference file names a local path, internal script, dated incident ID, or real person/contact, it is NOT publish-ready.

## ban list for references/

Remove or replace with generic placeholders:

| Leak type | Example bad | Generic replacement |
|-----------|-------------|---------------------|
| Local paths | `~/.hermes/commons/journals/...` | `{agent_root}/journals/...` |
| Internal script names | `verify_sepagree_signature.py` | `canonical_verifier.py` |
| Contact names | "Jacqui", "John at FooCorp" | "contact", "counterparty" |
| Session IDs / dates | `20260721_001605_f2a47966` | `latest_interactive_session` |
| Private repo names | `<agent-handle>/private-tooling` | omit or name only public repos |
| Changelog stubs with no content | `- 2026-07-21: ...` | delete entirely |

## Session logs must never be in skills

Session logs belong in `journals/` or `state.db`, not in `references/`.
During sanitize, remove any reference file that is just a session transcript
or dispatch record. If a small excerpt is genuinely load-bearing, inline the
lesson in the SKILL.md body in generic form and delete the raw log file.

## Pre-publish scrub procedure

1. `grep -RsnE '(session|dispatch|2026|2025|Traceback|File "/root|/home/|@gmail\.com|[A-Z][a-z]+ [A-Z][a-z]+)' references/`
2. Replace matches per the ban list above.
3. Re-run until the grep returns only intentional, generic references.
4. Run `scripts/secret-scan.sh --working-tree <skill-dir>` and confirm CLEAN.
