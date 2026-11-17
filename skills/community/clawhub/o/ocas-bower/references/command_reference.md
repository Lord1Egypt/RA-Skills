# Bower Command Reference

Full command descriptions and flags.

## Scan commands

`bower.scan.deep [--founding] [--analyze-now]` — Full Drive crawl processed folder-by-folder. Phase 1 discovers the folder tree (fast). Phase 2 scans one top-level folder at a time — listing files, reading contents, building file records — and writes results to `scans/{folder_id}.json` after each folder. Progress saved to `scan_progress.json` after every folder. Resumes automatically across sessions. With `--founding` (first use only): after all folders scanned, presents high-confidence proposals as a batch for approval. With `--analyze-now`: analyzes whatever has been scanned so far without waiting for completion.

`bower.scan.light` — Incremental scan of recently modified files and known outlier zones. Runs drift detection before proceeding; aborts if drift exceeds threshold. After scan, checks for arrival matches against promoted patterns and auto-applies them immediately if quiet mode is enabled.

## Analysis & simulation

`bower.analyze` — Runs analysis against current folder scans and preference profile. Applies domain logic first then generic rules, expires stale proposals, auto-approves pattern-matched proposals, generates ranked move/rename/description proposals. Does not touch Drive.

`bower.simulate [--path "Folder/Subfolder"] [--depth N]` — Scans the specified folder without touching anything or writing any state. Produces a narrative report showing exactly what Bower would do. Purely read-only.

## Proposal management

`bower.proposals.review [--type move|rename|describe] [--domain taxes|projects|home|...]` — Lists pending proposals grouped by destination folder with confidence tier, domain tag, and reasoning.

`bower.proposals.approve [--tier high] [--ids p_xxx,p_yyy] [--all] [--type move|rename|describe]` — Approves a subset of proposals for execution. Requires explicit scope.

`bower.proposals.reject [--ids p_xxx,p_yyy]` — Rejects specific proposals and records feedback. Rejected patterns are suppressed and may trigger demotion.

## Execution

`bower.apply [--dry-run]` — Executes pending proposals that have been approved by the user (up to `apply_cap`) and description writes to empty fields (up to `describe_auto_cap`). Each proposal is staleness-checked immediately before execution. With `--dry-run`, previews the digest without touching Drive.

`bower.undo [--ids mvl_xxx,mvl_yyy] [--last N]` — Reverses executed moves, renames, and description writes. Triggers pattern demotion if the undone proposal was auto-approved.

## Preferences

`bower.preferences.show` — Displays the current preference profile: detected naming conventions, depth preference, domains, auto-approved patterns, suppressed outliers, sacred folders.

`bower.preferences.lock [--field naming|depth|domain:taxes|...] [--pattern key]` — Locks a specific preference field or pattern so inference never overwrites it.

`bower.preferences.quiet [--on|--off]` — Enables/disables quiet mode. Suppresses digest output for successful runs; never changes what requires approval.

`bower.feedback.clear [--pattern key] [--all]` — Clears learned suppression patterns or demotions.

## Status & init

`bower.status [--trend]` — Prints SkillStatus: last scan, preference summary, active domains, quiet mode, drift rate, proposal counts, last apply, caps remaining. With `--trend`: Drive health over last 8 weeks.

`bower.init` — Initializes storage, registers background jobs, writes default config. Runs automatically on first use.
