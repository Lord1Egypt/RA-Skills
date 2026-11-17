# Decision Model Invariants

Key invariants that govern all Bower operations:

- Never propose a delete.
- Never move a starred file unless confidence is high and destination is unambiguous.
- Never flatten a folder with 3+ children.
- Never propose a move into a non-existent folder without a preceding create_folder proposal.
- Renames are `high` confidence only.
- Description overwrites require approval. Auto-writes to empty fields do not.
- Domain logic runs before generic outlier logic per file. Not both.
- Prescriptive domain logic only applies when domain is clearly started (5+ files or 2+ subfolders in domain root).
- Always preserve `previous_value` in move_log before any overwrite.
- Always run staleness check per-proposal immediately before execution.
- Auto-approved proposals still pass staleness gate and permission check.
- Arrival detection auto-approves only high-confidence pattern matches. Med-confidence matches stay pending.
- Founding run batch approval grants immediate pattern promotion credit for all executed proposals.
- Simulation writes nothing: no proposals, no logs, no journal, no state changes of any kind.
- Quiet mode suppresses digest output only. It never changes what requires approval.
- Load feedback suppressions and recalibration data before every `bower.analyze` run.
- Rebuild preference profile on every deep scan; respect locked fields.
- Medical file highlights in apply digest and simulation output: folder path and count only, never filenames or content.
- Full file text must never appear in logs, journals, or output.
