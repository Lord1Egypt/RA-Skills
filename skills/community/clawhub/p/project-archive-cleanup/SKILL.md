---
name: project-archive-cleanup
description: "Archive-clean finished, long-idle project directories — retain planning documents and result artifacts, strip execution traces (one-off scripts, import intermediates, scrape snapshots, console logs, superseded versions, byte-identical duplicates). Use when asked to clean up project leftovers, reduce process noise, or archive completed work. Always read-only scan first, then a two-phase backup-and-delete with batching for the safe-delete threshold."
description_zh: "项目归档清理：保留策划与结果，剥离执行过程痕迹"
description_en: "Project archive cleanup"
disable: false
agent_created: true
version: "1.0.0"
---

# project-archive-cleanup

## When to use

- A project is described as finished or long-idle and the ask is to reduce process residue — keep the planning and result layer, drop the execution layer.
- Periodic workspace hygiene alongside a disk health check.
- After iterative work left several near-identical versions of one deliverable.

Do **not** use for: active projects (last activity < ~14 days), the runtime dir itself (`~/.workbuddy`, a disk-health job), or any unit holding private or company-restricted data without explicit sign-off.

## Steps

1. **Scope the units.** Enumerate top-level dirs plus one level under the main project root. Skip `.git`, `.venv`, `node_modules`, `__pycache__`, `site-packages`. Record size / file count / last-activity / process-file ratio per unit.
   - Reusable scanner: an `outputs/scan_projects.py`-style walk that reports `size / files / last activity / process-file count` per unit.

2. **Classify each unit** before touching anything:
   - **Active** (last activity < 14d) → out of scope.
   - **Restricted** (company or brand campaign material, anything with holdings or PII) → list as "needs sign-off", do not clean.
   - **Finished + idle + unrestricted** → in scope.

3. **Apply the keep/strip rule:**
   | | keep | strip |
   | --- | --- | --- |
   | planning | PRD, strategy, checklists, changelog, history index | — |
   | result | latest deliverable, report, source, cloud functions, config, result data | byte-identical duplicate copies |
   | process | — | one-off scripts, import intermediates, scrape snapshots, console logs, superseded versions |

4. **Prove "duplicate" with sha256, never by name or size.** Size equality is not identity. Recurring shapes: two identical page snapshots from the same browser run; report copies identical to files already in the result dir; a `before-*.docx` identical to the final stage output.

5. **Check references before deleting a script.** Grep the project for the base name, then judge the *source* of the hit:
   - hit only in workspace memory logs or a changelog → process trace, safe to strip.
   - hit in a **result doc** (e.g. a test report) or it is an **operational script** → keep, otherwise the result file loses its referent.

6. **Never delete a skill or dependency copy without checking installation.** Compare against `{p.name for p in (~/.workbuddy/skills).iterdir()}` — if the local copy is not installed there, it is the only copy and long idle time says nothing about disposability.

7. **Two-phase execution.** Dry-run script prints every item with size + reason; only `--apply` writes.
   - **Batch by shape**: single-file batch and directory batch run in *separate processes*. The safe-delete hook counts expanded files, threshold 50, scope=turn, and terminates the whole run — already-deleted items do **not** roll back.
   - Directory deletes via .NET: `[System.IO.Directory]::Delete($p, $true)` in PowerShell, then verify with `[System.IO.Directory]::Exists($p)`.

8. **Back up before delete** to `<workspace>/outputs/_archive_<date>/`, then verify by **comparing file counts src vs bak** for every entry. Do not trust the script's success echo.

9. **Clean up directories your own deletes emptied**; leave pre-existing empty dirs alone (they are often tool-expected paths such as template output dirs or sync audit scratch dirs).

10. **Write the outcome** into the health/archive report: what was stripped, what was kept and why, the backup location, and a "needs your call" table for restricted or private items.

## Pitfalls

- **"Long idle" is not "dead".** Check whether a copy is the only surviving instance before judging it disposable.
- **Same size ≠ same file.** Always hash. Files that look like a pair by name can differ by tens of KB.
- **Version series are the trap.** Keep the newest + the history index; superseded chains (earlier `vN` when a later version exists elsewhere) are the noise, but recent mid-series versions (last few days) belong in "archive, don't delete".
- **Volume is a poor success metric.** A cleanup of many items may reclaim very little disk — the value is structural, say so instead of selling a number.
- **Do not blanket-delete 0-byte files.** Virtualenv trees are full of legitimate empty `__init__.py` / `py.typed`.
- **Windows reserved names** (`nul`, `con`) break Python `exists()` (always True) and `os.remove`; use .NET `File.Delete` with the `\\?\` prefix and verify via `os.listdir`.

## Verification

- Per-item `exists()` recheck after deletion; for reserved names use directory enumeration, not `Path.exists()`.
- Backup integrity: every entry's src file count == bak file count.
- Re-run the unit scanner and report before/after file counts and process-file counts per project.
- Confirm no result file lost its referent: spot-check docs that named a deleted script.

## Reference

Worked case (a 26-item run across 7 projects, with the keep/strip decisions and the near-miss on uninstalled skill copies) is recorded in the workspace health report for that date — see `<workspace>/outputs/workbuddy-health-report-<date>.md`, project-archive section.
