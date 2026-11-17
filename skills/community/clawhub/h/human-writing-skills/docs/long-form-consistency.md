# Chunked Long-Form Audit, Style Unification, and Character Consistency

This workflow is for novels, article series, research reports, annual reports, and
other material too large for one reliable review pass. It gives bounded chunks the
same evidence-backed style baseline and canonical outline, then reconciles local
findings across the whole work.

Discovery terms: **long-form audit, chunked manuscript audit, writing style
unification, style consistency review, character consistency audit, cross-chapter
continuity, novel audit, and report review**.

## Why Naive Chunking Still Drifts

A model that sees only the current block has to reinvent narrative distance, rhythm,
speaker voice, and terminology. Repeating the entire manuscript and every audit module
in each request wastes context. `chunk-audit` instead carries three bounded layers:

1. **Baseline evidence:** explicit approved references take priority; otherwise use a
   user-selected candidate manuscript chunk that is confirmed during baseline extraction.
2. **Canonical context:** an outline, character bible, or continuity ledger for fiction;
   a section plan, terminology contract, and claim boundaries for reports.
3. **Current body:** every draft character belongs to one audit body. A short preceding
   tail is included only as read-only continuity context and is not audited twice.

## Commands

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --output-dir novel-consistency-audit
```

Use an approved reference when a model or prompt change has altered recent prose:

```powershell
human-writing-skills chunk-audit `
  --draft annual-report.md `
  --style formal-document `
  --context report-plan.md `
  --reference approved-2025-report.md `
  --chunk-size 10000 `
  --output-dir report-style-audit
```

Without `--reference`, chunk one is the default candidate baseline. Confirm it before
repair, or select another block with `--baseline-chunk 3` when the opening is atypical.

## Package Contents

- `00-baseline-prompt.md`: extracts a compact style contract, character cards, or report rules.
- `00-style-drift.md/json`: deterministic triage statistics, not defect or authorship claims.
- `0001-chunk-audit.md` and following files: independent body audits with read-only lead-ins.
- `9999-reconcile-prompt.md`: compares narrator, speaker, character, terminology, and section drift.
- `manifest.json`: records unique body ranges, lead-in ranges, and baseline provenance.
- `agent-plan.json`: lists independently runnable reviewer tasks, dependencies, and expected report paths.
- `reports/`: destination directory for baseline, chunk, specialist, and reconciliation reports.

Run the baseline prompt, the numbered chunks, then reconciliation. Each numbered pass
can use a fresh conversation or API request with the approved compact contract. The
model does not need hidden memory of the whole manuscript.

## Verified Parallel Agent Review

Use the default package when one careful review per block is sufficient. When complete
inspection matters, add `--agent-mode deep`:

```powershell
human-writing-skills chunk-audit `
  --draft full-novel.md `
  --style fiction `
  --outline novel-outline.md `
  --agent-mode deep `
  --output-dir novel-agent-audit
```

Run the baseline first. Tasks that depend only on `baseline` may then run in parallel in
fresh model sessions. Each response must be saved at the exact path in `agent-plan.json`
and include its Coverage Receipt: task ID, audited scope, checked units, findings, and
blocked material. This is a visible completeness contract, not proof that a model is right.

```powershell
human-writing-skills verify-chunk-audit --package-dir novel-agent-audit
```

Do not reconcile while this command reports missing or invalid receipts. Deep mode adds a
paragraph-level prose pass to every block, interaction review where dialogue or directed actions occur, and
source-grounding only for serious documents with explicit `--source` files. Use
`--translationese` only for an explicitly translated or localized work.

## Optional Whole-Book Story Review

For a fiction or webnovel manuscript with at least three identifiable chapter
headings, add `--book-level`. This writes one extra `9000-book-architecture-prompt.md`
after the chunk tasks, not another module in every chunk. The pass maps chapter
decisions and consequences, conflict change, time movement, and whether the work
repeatedly explains away its own ambiguities. It uses completed chunk reports and
the canonical outline. `00-chapter-map.json` records chapter headings, body offsets,
and intersecting chunk IDs so source spans can be reopened; missing evidence is
requested rather than invented.

```powershell
human-writing-skills chunk-audit --draft novel.md --style fiction --outline outline.md --book-level --output-dir book-audit
```

Run the book task after the chunk reports and before `verify-chunk-audit` and final
reconciliation. It is an evidence-backed model review, not a deterministic plot
grader. Formal reports and single chapters do not load it.

## Outline-Backed Character Consistency

The audit compiles supported goals, knowledge, relationships, limits, capabilities,
public/private posture, address forms, disclosure habits, and valid change events. It
then checks each block against those cards. Growth, deception, audience shifts, and
stress responses remain valid when the draft earns them; unexplained contradictions do not.

Approved changes go back into the ledger so later blocks use the new state instead of
being forced toward an obsolete opening description.

## Token Control

- Defaults: 8,000-character bodies and 600-character read-only lead-ins.
- Context is sampled to 6,000 characters and baseline evidence to 4,000 by default.
- Fiction loads authoritative character checks only when context exists and dialogue
  voice checks only for chunks that contain dialogue or directed interpersonal actions.
- Serious styles load protected-content rules instead of fiction-only modules.
- Tune `--chunk-size`, `--context-budget`, and `--baseline-budget` for smaller models,
  while keeping complete scenes or argument units together when possible.
