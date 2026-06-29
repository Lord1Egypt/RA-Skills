# Agent Adapter Contract

Use this contract when adapting Oh My Teacher to any agent runtime. No agent gets
special treatment: every runtime is represented by an inventory record, a thin
adapter, and the same shared teaching protocol.

## Core Rule

Keep teaching behavior in `SKILL.md` and command behavior in `references/INDEX.md`
plus the command reference files. Agent adapters must only describe host
capabilities, tool use, constraints, and fallbacks.

Proactive reminders are shared behavior, not agent-specific behavior. Use
`references/opt-in-reminders.md` only after the user explicitly asks for
reminders or daily/weekly knowledge digests; never enable background messages
because an adapter name suggests they might be possible.

## Adapter Files

Each supported agent has one file under `agents/` and one registry entry. A valid
adapter must:

- Reference `SKILL.md` as the authoritative teaching workflow.
- Reference this file for capability and fallback rules.
- Reference `references/agent-optimization.md` for choosing the best capability
  path after tools are detected.
- Reference `references/agent-inventory.md` for researched or unknown platform
  facts.
- Treat product identity as a hint only; actual tools win over the product name.
- Refuse to claim that files were read, scripts ran, citations were retrieved, or
  memory was written unless the host actually exposes that capability and the
  operation succeeds.
- Avoid restating slash-command workflows. Duplicating command details causes
  drift from `references/INDEX.md`.

## Capability Tags

Use these tags in the registry and inventory:

- `file-read`: can inspect local or uploaded files.
- `file-write`: can create or edit persistent artifacts.
- `shell`: can run local commands or scripts.
- `sandbox`: tool calls may require approval or may be scoped.
- `search`: can retrieve web or workspace information.
- `kb-retrieval`: can search a knowledge base or uploaded corpus.
- `citations`: can attach source references to retrieved content.
- `memory`: can persist facts across sessions.
- `task-plan`: exposes a native planning or task list tool.
- `subagents`: can delegate to worker agents.
- `ide`: can use code index, diagnostics, editor context, or project metadata.
- `rendering`: can render Markdown tables, LaTeX, Mermaid, HTML, images, or PDFs.
- `proactive-message`: can send messages without an immediate user prompt after
  explicit user opt-in.
- `scheduler`: can schedule delayed or recurring jobs after explicit user
  opt-in.
- `unknown`: capability is not verified yet; use conservative fallbacks.

## Detection Order

At runtime, detect capabilities in this order:

1. Inspect exposed tools and permissions.
2. Inspect workspace files, manifests, adapter metadata, or user-provided runtime
   notes.
3. Use the product name only as a weak hint.
4. If the required capability is still unknown, ask one compact probe only when
   the current task depends on it.
5. Otherwise proceed with inline Markdown fallbacks.

## State And Script Policy

- If `file-write` and `shell` are both available, prefer deterministic scripts:
  `scripts/snapshot.py`, `scripts/srs.py`, and `scripts/export_flashcards.py`.
- If `file-write` exists but `shell` does not, save Markdown artifacts directly
  and do not mention script execution.
- If neither `file-write` nor `shell` exists, emit copyable Markdown snapshots,
  SRS tables, flashcards, and plans inline.
- If a script fails, report the failure and switch to the matching fallback.

## Inventory Policy

Before adding or changing an adapter:

1. Add or update the agent record in `references/agent-inventory.md`.
2. Mark the source status as `official`, `observed`, `community`, or `unknown`.
3. Record unknown capabilities explicitly instead of guessing.
4. Choose an `optimization_profile` from `references/agent-optimization.md`.
5. Add the agent to `agents/registry.json`.
6. Add or update the thin adapter under `agents/`.
7. Run `python scripts/package_check.py`.

## Runtime Prompt Policy

For runtimes that do not load multi-file skills, generate a bundled prompt with:

```bash
python scripts/build_runtime_prompt.py --agent <agent-id>
```

Use `--agent generic` for unverified or newly added agents. The generated prompt
must include the adapter, this contract, the inventory, `SKILL.md`, and the shared
reference map.
