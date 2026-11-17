---
name: memory-review
description: Review daily memory logs and consolidate durable knowledge into the existing memory hierarchy. Use for scheduled or manual knowledge review, especially when deciding whether to update an existing canonical document, create a genuinely new document, skip a duplicate, defer an unstable signal, or propose merging overlapping documents.
---

# Memory Review

Turn daily logs into a small, current knowledge base. Treat daily logs as evidence, not as the authority.

## Required workflow

1. Read [references/spec.md](references/spec.md) before any write.
2. Read the workspace `AGENTS.md` and `MEMORY.md` for current hierarchy and owner rules.
3. Build the deterministic scan plan:

   ```bash
   python3 skills/memory-review/scripts/memory_review.py scan \
     --root . \
     --output /tmp/memory-review-scan.json
   ```

4. Read every file in `changed_sources`. Ignore `*-memory-review.md`; the scanner excludes them.
5. Extract only durable signals. Exclude transient status, unverified ideas, routine execution logs, and secrets.
6. Resolve every signal against existing memory before writing. Use exact references, `memory_search`, `rg`, and the helper when useful:

   ```bash
   python3 skills/memory-review/scripts/memory_review.py candidates \
     --root . --query "主题或结论"
   ```

7. Create a decision plan using the schema in the spec. Validate it before editing:

   ```bash
   python3 skills/memory-review/scripts/memory_review.py validate-plan \
     --root . --plan /tmp/memory-review-decisions.json
   ```

8. Apply decisions in this order:
   - `update_existing`
   - `skip_duplicate`
   - `review_merge`
   - `create_new`
   - `defer`
9. Verify the diff, references, and current conclusion. A second run over unchanged inputs must not change canonical memory.
10. Write the report and execution log, then commit scan state only after all writes and checks succeed:

   ```bash
   python3 skills/memory-review/scripts/memory_review.py commit-state \
     --root . --scan /tmp/memory-review-scan.json
   ```

## Hard rules

- Update-first: prefer the best existing canonical document over creating a near-synonym.
- Never create a third document when two candidates already overlap; emit `review_merge` instead.
- Resolve conflicts; do not append mutually contradictory conclusions as if both were current.
- Knowledge and hot memory outrank daily logs unless newer verified evidence explicitly supersedes them.
- Do not automatically edit `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, `SOUL.md`, or `ENVIRONMENT.md`. Record a proposal unless the current request explicitly authorizes that edit.
- Do not put dates in new `memory/knowledge/` filenames. Git history tracks time.
- Do not advance state after partial failure.
- Do not send reports unless the caller or cron prompt specifies a destination.

## Outputs

- Report: `memory/daily/YYYY-MM/YYYY-MM-DD-memory-review.md`
- Execution log: `data/exec-logs/memory-review/YYYY-MM-DD.md`
- State: `data/exec-logs/memory-review/state.json`
- Canonical targets: `memory/knowledge/`, `memory/glossary.md`, `memory/projects/`, `memory/post-mortems.md`
