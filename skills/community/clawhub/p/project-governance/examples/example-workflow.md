# Example: Onboarding an AI agent into a messy project

This walkthrough shows the skill in action. It is a realistic scenario, not a
toy: a project that grew organically and now has scattered files, unrecorded
parameter changes, and repeated mistakes.

## Scenario

A team has a long-running AI-assisted project (a content generation pipeline).
The agent keeps making the same mistakes: it searches files by keyword instead
of using the directory map, it changes parameters without recording them, and
it repeats errors that were already fixed weeks ago. There is no protocol file,
no error log, and no parameter registry.

## Step 1 — Scaffold

```bash
python scripts/governance.py init \
  --project-dir /path/to/project \
  --project-name "Content Pipeline"
```

Output:

```
Created 10 governance files in /path/to/project
  + AGENTS.md
  + ARCHITECTURE.md
  + PROJECT.md
  + index.md
  + LESSONS.md
  + session_handoff.md
  + CHANGELOG.md
  + VERSIONS.md
  + blacklist.json
  + whitelist.json
```

## Step 2 — Customize the protocol

The team edits `AGENTS.md` to reflect real constraints:

- **Directory permission zones**: `pipeline/` and `core/` are 🟡 core code (must
  explain impact before modifying); `assets/` is 📂 read-only; `output/` is 🟢
  free to edit.
- **Artifact placement**: all generated files go under `output/`, named
  `[type]_[date]_[version]_[description]`.
- **Autonomy levels**: the agent may freely edit `output/` (Level 1) but must
  wait for confirmation before touching `pipeline/` (Level 2).

## Step 3 — Record the first lessons and registry entries

The team backfills `LESSONS.md` with the two most painful historical errors,
each following the phenomenon → root cause → correction → lesson format.

They add one `blacklist.json` entry for a parameter combination that is known to
fail, and one `whitelist.json` entry for the verified baseline:

```json
{
  "id": "shared_checkpoint_single_model",
  "reason": "Background and character shared one checkpoint variable, so the background used the character model.",
  "permanent_ban": true,
  "alternative": "Use separate CHECKPOINT variables for background and character.",
  "test_ref": "pipeline_v1",
  "judge": "human",
  "scope": "pipeline",
  "status": "active"
}
```

## Step 4 — Validate the registries

```bash
python scripts/governance.py validate --project-dir /path/to/project
```

```
VALIDATION PASSED: blacklist.json and whitelist.json conform to the schema.
```

## Step 5 — Maintain during sessions

- On session start, the agent reads `index.md` → `session_handoff.md` →
  `LESSONS.md`.
- Before generating parameters, it reads `blacklist.json` and `whitelist.json`
  and inherits the `whitelist` baseline instead of starting from scratch.
- On session end, it updates `session_handoff.md`, appends to `CHANGELOG.md`,
  and refreshes `index.md`:

```bash
python scripts/governance.py index --project-dir /path/to/project
```

## Result

Within a few sessions the agent stops repeating known mistakes, parameters are
traceable, and any session can resume cleanly from the handoff file. The
governance files become the single source of truth for how the project is run.
