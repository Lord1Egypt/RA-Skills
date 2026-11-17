---
name: ingest
description: Build or refresh the CGIS code graph for this repository
argument-hint: "[source path — defaults to autodetected]"
disable-model-invocation: true
---

Build the CGIS semantic graph for this repository so the `cgis_*` tools can answer structural questions.

**Source path:** $ARGUMENTS

If no path was given above, work out the source root yourself rather than asking:

- a `src/` directory if one exists
- otherwise the package directory named in `pyproject.toml`, `package.json`, or `tsconfig.json`
- otherwise the repository root

Never point ingestion at `node_modules`, `.venv`, `venv`, `dist`, `build`, or `.git` — they add minutes and pollute the graph with code nobody will ask about.

Then:

1. Call `cgis_ingest` with that path. Leave `db_path` at its default so the graph lands in `graph.db` at the project root, where every other tool looks for it.
2. Call `cgis_validate` and read the resolution breakdown.
3. Report back concisely: how many files, nodes and edges landed, and the share of unresolved edges.

On the unresolved share, interpret rather than just quoting the number. A residue in the low tens of percent is normal and consists mostly of runtime-dispatched calls — `logger.info`, `response.json`, injected clients. If it is unusually high, the likely cause is ingesting the wrong root or a codebase leaning heavily on dynamic dispatch; say which you think it is.

If the repository contains languages CGIS has no extractor for — anything other than Python and TypeScript — name them, so it is clear up front which parts of the codebase the graph will not be able to answer for.

Finally, mention that `graph.db` should be added to `.gitignore` if it is not already there, and that the graph goes stale as code changes: re-run this command after substantial edits.
