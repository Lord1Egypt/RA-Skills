# Subproject Playbook

**Status:** field-tested. Everything here is derived from the《奉天1928》(`-1928`)
subproject after 288 released chapters, 227 review reports and 558+ ledger rulings.

**Authority:** where this playbook and `SKILL.md` disagree, **this playbook wins**
for subprojects in production. `SKILL.md` describes the generic contract; this
file describes what actually survives contact with a long serial.

---

## 1. Why this file exists

The generic contract assumes a greenfield novel with a handful of chapters. A
serial that runs for months hits problems the contract never mentions: where do
cross-session rulings live, how do you keep a report from vanishing, why does
every Markdown file turn into CRLF. The answers below were paid for in rework.

---

## 2. Directory layout (as built)

```
<root>/
  chapters/                 release text — the only authoritative copy
    <第X卷 卷名>/
      <第Y幕 幕名>/
        第NNN章 四字标题.md
  worldbuilding/            setting docs, plus OUTLINE/
  characters/               character dossiers, usually tiered (核心/重要/次要/背景)
  notes-personal/           working drafts — never published from here
  issues/                   per-arc discussion notes
  .workbuddy/reports/       review reports + index
  .workbuddy/memory/        layered session memory
```

**Naming.** `第NNN章 四字标题.md` (three-digit zero-padded chapter number, exactly
four Chinese characters as the title, unique across the book). The generic
contract's `ch-{number}-{title}.md` is the default for a new subproject with no
constraints; a subproject may adopt its own convention provided:

1. it is written down in the subproject's `CONTRIBUTING.md`,
2. the shared scripts still recognise it (they accept both forms),
3. lexical sort still equals numeric sort within an arc directory.

**Volume / arc directories** are part of the path, not metadata. Never encode
them only in frontmatter — the filesystem is the index.

Run `scripts/init_subproject.py` to create this skeleton instead of rebuilding it.

---

## 3. State: what actually replaced `state/`

`SKILL.md` prescribes five state files under `state/`. In production none of them
were used, and forcing them would have duplicated three systems that already
worked. The mapping:

| Generic contract | What production uses instead |
|---|---|
| `state/timeline` | `worldbuilding/时间线` — kept next to the setting, so a change to one is visible against the other |
| `state/character-states` | `characters/<tier>/<name>.md` — the dossier *is* the state |
| `state/thread-ledger` | `issues/` (per-arc) + the decision ledger (§4) |
| `state/location-states` | folded into the setting docs |
| `state/continuity-snapshots/` | git history + `_promote_draft.py`'s pre-write snapshot |

**Rule:** a subproject picks one home for each kind of state and writes it down.
Splitting the same fact across `state/` and `worldbuilding/` is worse than
choosing either.

---

## 4. Decision ledger (编号制裁定)

Every cross-session ruling gets a number. **A ruling that is not on the ledger is
not a ruling** — the next session will re-litigate it.

```
| ID  | Date | Subject | Ruling | Where it landed | Report |
|-----|------|---------|--------|-----------------|--------|
| D558| ...  | ...     | ...    | 第605章          | #216   |
```

Rules that make it work:

- **Append only.** A ruling that has been applied is never edited in place.
- **Superseded rulings stay.** Mark them superseded and point at the new ID.
- **`Where it landed` names a concrete file or chapter.** This is the single
  field that turns "did we do this?" into a check instead of a re-decision.
- **When a criterion changes, re-scan the old verdicts.** A ruling recorded under
  an old rule does not automatically remain correct.

---

## 5. Reports and the three indexes

A report is **not archived** until it is listed. Unlisted == never happened.

Three indexes must agree after every change:

1. `reports/README` (under `.workbuddy/`) — the report index
2. `CHANGELOG.md` — the chronological record
3. `progress.md` — the progress record (when chapters moved)

Rules:

- Number sequentially and never reuse a number.
- Word counts use one convention (the humanizer-reported count), so the column is
  comparable across rows.
- Long content goes under a `####` detail section below the table, never inside a
  table cell — a table cell with a paragraph in it cannot be reviewed in a diff.
- **Reports go through the same gate as the text.** A report that fails the
  AI-tone check while judging AI tone is the most common self-inflicted failure.

---

## 6. Layered memory

```
year -> quarter -> month -> day
```

Upper layers hold **index and distilled conclusions only**. Detail lives in the
day files. Side halls hold cross-time conventions and are not archived by date.

Maintenance:

| Layer | Rule |
|---|---|
| Day | append only, never rewrite |
| Month | distilled from the day layer at month end |
| Quarter | distilled from the month layer |
| Year | distilled from the quarter layer |
| Side hall | written when a convention is established, not on a schedule |

After editing any layer, re-check that the index above it still resolves.

**Trap:** quoting a banned word inside the document that bans it makes the
document fail its own gate. Write "category + count, see §X" instead of
enumerating the words.

---

## 7. File hygiene and the LF rule

**The rule, non-negotiable:**

> 凡写文本，一律 `io.open(p, 'w', encoding='utf-8', newline='\n')`

On Windows, `io.open(p, 'w', encoding='utf-8')` defaults to `newline=None`: it
normalises CRLF to LF on read **and converts LF back to CRLF on write**. Any
Markdown file a Python script touches — even for a one-line edit — is rewritten
entirely as CRLF. `.gitattributes` cannot prevent this, because the conversion
happens inside the script at write time.

Enforce with:

```
python scripts/scan_hygiene.py --root . --fail-on crlf,junk,mojibake
```

**Backups.** One retained backup per unit, dated (`原名.bak-YYYY-MM-DD`). Before
removing an older backup, record its diff against the newer one in `CHANGELOG.md`;
never drop a backup without a trace.

---

## 8. Change order (draft-first)

```
1. edit the draft in notes-personal/
2. humanizer_check.py <file>            # gate on the draft
3. archive the review report + index it
4. gate passes
5. _promote_draft.py <chapter>          # sync into chapters/
6. CHANGELOG.md / progress.md
```

Reverse direction (`_sync_draft.py`) is **errata only**. A PR that edits release
text without a draft behind it is not reviewable — the reviewer cannot tell an
aesthetic edit from an accidental deletion.

**Serialise change and verify.** Chain them with `&&` in one command. Issuing
"edit the index" and "run the check" concurrently lets the check read the
pre-edit version and report a false failure.

---

## 9. Reference integrity

**The rule:** release files reference release files only. Non-release files may
reference anything.

A *release* file ships: `SKILL.md`, `README.md`, `modules/`, `references/`,
`scripts/`, `.github/`. A *non-release* file lives in a private work area:
`notes-personal/`, `_trash/`, `.workbuddy/` (reports, memory, ad-hoc scripts).
Reports and working notes legitimately point at drafts and private ledgers;
shipped documentation must not point at something the reader cannot open.

```
python scripts/check_refs.py --root .
```

Buckets: `OK / LOCAL / TEMPLATE / BARE / PRIVATE_OK / NONRELEASE / MISSING /
PRIVATE_MISSING`.

- `NONRELEASE` — a release file pointing into a private area. **Always a defect.**
- `MISSING` — a release file pointing at something that does not exist.
  **Always a defect**, unless the target is a path this repository only
  describes (subproject state files, example manuscripts). Those exemptions
  are declared in `.refsignore`, one regex per line, with the reason next to
  each — the same file is read locally, in pre-commit and in CI.
- `PRIVATE_OK` — a non-release file pointing into a private area. Allowed by
  the rule.
- `PRIVATE_MISSING` — a report or working note pointing at something absent.
  Expected: those are written about another tree. Listed, never gated on.

Gate on `NONRELEASE,MISSING`. A growing `.refsignore` is the signal that the
convention is being described rather than followed.

---

## 10. The 500-line rule, applied honestly

The 500-line budget exists to keep files readable in review. It was written for
prose and method documents. Three kinds of file legitimately exceed it, and
pretending otherwise makes the whole rule ignorable:

| Kind | Examples | Treatment |
|---|---|---|
| Ledger / log | `CHANGELOG.md`, `progress.md`, decision ledger | exempt — chronological append, never read end-to-end |
| Reference table | setting compendia | split by domain; if one domain is genuinely 3000 lines, split by section and link |
| Generated / seed | `README FOR AI.md` | exempt, but never edited by hand |

Declare exemptions explicitly (`scan_hygiene.py --allow ...`) rather than
letting them accumulate silently. **A rule with unstated exceptions is a rule
nobody follows.**

---

## 11. Standing up a new subproject

```
python scripts/init_subproject.py --name "<title>" --root <path>
cd <path>
git init && git remote add origin <url>
```

Then:

1. Replace `@OWNER` in `.github/CODEOWNERS` — GitHub silently ignores lines whose
   owner does not exist, so an unedited CODEOWNERS provides false comfort.
2. Fill in `SYNOPSIS.md` before writing a single chapter.
3. Register the subproject in `SUBPROJECTS.md`.
