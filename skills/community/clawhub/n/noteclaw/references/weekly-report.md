# Weekly / periodic report flow

A report is a **review of the user's own recent work**: an objective summary of how note content changed over the previous period (new / edited / deleted), and what those changes add up to. The report covers note content only.

## Flow

Prerequisite: the data directory (the working directory) holds a synced `store/` and git history; `$SKILL` = the skill path (see SKILL.md). The report compares the complete git history from "previous report → now", so syncing more often than reporting does not affect the completeness of the period.

Both `store/` and `reports/` are split into per-notebook directories. Below, `<notebook>` = the `store/` subdirectory name matching `notebook.displayName` in the data directory's `manifest.json` (`ls store/` shows it, in the same segment as the store); the git path and the report path are both scoped by it.

1. **Resolve the base commit** — the starting point of the period. The base is the commit of the previous report (syncing can be more frequent than reporting, so sync snapshots are not used). Resolve the base first, then sync. Order of judgement: check for an existing report → then count the notebook's store commits and take the matching branch:
   - **`reports/<notebook>/` already holds a report** → base = the most recent commit that wrote into that directory; the period's changes = this notebook's store history from that base to the current HEAD:
     ```bash
     BASE=$(git log -1 --format=%H -- reports/<notebook>/)       # commit of the previous report
     ```
   - **No previous report, and the store has exactly 1 commit (first cold start)** → treat the whole store as new, base = the git empty tree, and the first report says "first snapshot: N pages":
     ```bash
     BASE=4b825dc642cb6eb9a060e54bf8d69288fbee4904   # git empty tree constant = parent of the first commit
     ```
   - **No previous report, but the notebook already has 2 or more store commits (the first commit is the historical start and cannot serve as base)** → base = the snapshot commit before the current HEAD:
     ```bash
     BASE=$(git log -2 --format=%H -- store/<notebook>/ | tail -1)
     ```
2. **Run the incremental sync** (pull the latest changes into the store as the period's endpoint):
   ```bash
   cd <data directory>
   python3 $SKILL/scripts/graph_sync.py && python3 $SKILL/scripts/html2md.py
   ```
   `html2md.py` already runs `git add -A` + commit for one snapshot at the end, so no manual commit is needed here.
3. **Get the list of pages changed in the period**:
   ```bash
   python3 $SKILL/scripts/notequery.py diff --from "$BASE" --name-only
   ```
   This yields the pages added / edited / deleted in this round; if there are none, write a zero-change report.
4. **Read the changed pages**: fetch the body of each page from the step 3 list; when there are many, **read them in batches and note the key points batch by batch** instead of queueing it all up at once:
   ```bash
   python3 $SKILL/scripts/notequery.py fetch --page "<section>/<NNN>"
   ```
   ⚠ Do not substitute `since --full` — it selects pages by **Graph timestamps**, which is not the same set as the changed pages here (from git `diff`); it would mix in unchanged pages and miss pages that changed while their timestamps stayed put.
5. **Write the report**: `mkdir -p reports/<notebook>` → `reports/<notebook>/weekly-YYYY-Www.md` (ISO week number; for a longer custom period use the matching file name), then commit it.
6. **Give the report to the user**: present the full contents of `reports/<notebook>/weekly-YYYY-Www.md` directly, with the file path; do not produce a separate summary.

## Report template

```markdown
# Weekly report — <start> ~ <end> (ISO week)

## One-line overview
<N> pages changed this week (A new / B edited / C deleted); overall: ...

## Main threads this week
Group the changed pages into 2–4 threads, one line each on what the notes advanced.

## Details
- New: <page> (<section>) — what it records, 1–2 lines
- Edited: <page> (<section>) — what changed, 1–2 lines
- Deleted: "<page>" was deleted (content remains in git history)

## Observations (optional)
Factual notes on the distribution of changes over time or across sections.
```

## Tool reference

| Need | Command |
|---|---|
| List of changed pages | `$SKILL/scripts/notequery.py diff --from <rev> --name-only` |
| Content-level differences | `$SKILL/scripts/notequery.py diff --from <rev> --full` (budget gate `--max-bytes`) |
| Body of one page | `$SKILL/scripts/notequery.py fetch --page "<NNN or section/NNN or title substring>"` |
| Locate by keyword | `$SKILL/scripts/notequery.py grep --kw KEYWORD` |
| Page listing / timestamps | `$SKILL/scripts/notequery.py list [--section SECTION]` |
| Bulk bodies over a time window (with budget) | `$SKILL/scripts/notequery.py since --since <D> --full --max-pages N --max-bytes B` (selects by timestamp, not the changed-page set) |
