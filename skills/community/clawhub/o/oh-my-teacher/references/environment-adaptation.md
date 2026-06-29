# Environment Adaptation

Use this file before `/materials`, `/visual`, `/video`, `/code-demo`, `/flashcards`, snapshot persistence, or any task that depends on host capabilities. For named agent runtimes, also use `references/agent-adapter-contract.md`, `references/agent-optimization.md`, `references/agent-inventory.md`, `agents/registry.json`, and the matching adapter file when available.

## Principle

Detect capabilities, not product names. Product names are hints only; the same product can expose different tools depending on plan, plugin, workspace, or permissions.

## Environment Labels

Set the Current Course Snapshot `Environment` field to one of these labels:

| Label | Typical hosts | Capabilities |
|---|---|---|
| `ima-native` | ima with ask_user/fetch/search/memory/task_plan/use_skill tools | Knowledge-base and note retrieval, memory, native note/report/PPT skills, optional shell/files |
| `agent-shell` | Codex, Claude Code, OpenClaw, Hermes, WorkBuddy, Qoder Work, Trae, other coding agents | May read/write files, run shell commands, execute scripts, render artifacts |
| `rag-notebook` | NotebookLM, document-chat notebooks, knowledge-base Q&A tools | Has uploaded document context or retrieval, usually no filesystem writes |
| `notes-app` | Obsidian, markdown note tools, local PKM plugins | Markdown notes, backlinks/tags, sometimes local files, usually limited execution |
| `plain-chat` | ordinary AI chat boxes | No reliable files, shell, persistence, or retrieval unless explicitly provided |
| `unknown` | unclear host | Use plain-chat behavior until a capability is confirmed |

## Capability Checklist

Before using host-specific behavior, check these capabilities:

- **Read files**: Can the model inspect local paths or uploaded files directly?
- **Write files**: Can it save snapshots, plans, flashcards, or generated artifacts?
- **Run shell/scripts**: Can it execute `python scripts/...`?
- **Retrieve/cite**: Does it have document retrieval and source citation?
- **Read images/PDFs**: Can it inspect screenshots, note photos, PDFs, or OCR output?
- **Render math**: Does the chat render LaTeX, Mermaid, tables, or HTML?
- **Persist state**: Can it keep `.oh-my-teacher/` files, note blocks, or only inline summaries?
- **Proactive reminders**: Can it send proactive messages or schedule recurring
  jobs after explicit user opt-in?
- **Call paid/high-cost APIs**: Image/video/TTS/API calls require explicit confirmation.

If a capability is missing or uncertain, downgrade without stopping the learning task.

## Detection Order

Detect once, at session start or when the host changes, in this fixed order — stop at the first label that matches and set the snapshot `Environment` field. Do not re-probe per command.

1. **ima-native** — any ima tool is present (`ask_user`, `fetch`, `search`, `memory_recall`, `memory_write`, `task_plan`, `subagent_spawn`, `use_skill`). Read `references/ima-adaptation.md`.
2. **agent-shell** — file read/write and shell/script execution are available (you can run `python scripts/...`).
3. **rag-notebook** — document retrieval/citation context exists but no reliable file writes.
4. **notes-app** — Markdown persistence with tags/backlinks but no reliable shell.
5. **plain-chat** — none of the above is confirmed.
6. **unknown** — cannot tell yet; behave as plain-chat until a capability is confirmed.

Probe a single capability inline only when a specific task depends on it and detection was inconclusive (use the one-line probe below). Never block a conceptual explanation or single practice question on a probe — proceed with `plain-chat` defaults.

## Product Hints

Use these hints only after checking actual capabilities:

- **Codex / Claude Code / OpenClaw / Hermes / WorkBuddy / Qoder Work / Trae**: treat as `agent-shell` when file and shell tools exist. Prefer scripts for snapshots, SRS, flashcard export, and validation only after capabilities are confirmed.
- **ima**: treat as `ima-native` when ima tools such as `ask_user`, `fetch`, `search`, `memory_recall`, `memory_write`, `task_plan`, `subagent_spawn`, or `use_skill` are available. Read `references/ima-adaptation.md` before using knowledge, note, memory, report, or PPT workflows.
- **NotebookLM / RAG notebooks**: treat as `rag-notebook`. Use retrieved document context and citations. Do not assume file writing or shell execution.
- **Obsidian / markdown note apps**: treat as `notes-app`. Prefer Markdown blocks, tags, backlinks, and copyable snapshots. Do not assume scripts can run unless a local plugin exposes execution.
- **Ordinary AI chat**: treat as `plain-chat`. Keep all artifacts inline and copyable.

## Agent Adapter Registry

When packaging or running under a named agent:

1. Look up the agent in `agents/registry.json`.
2. Read the matching `agents/<agent>.yaml` adapter if available.
3. Use `references/agent-optimization.md` to select the best capability path after detecting tools.
4. Use `references/agent-inventory.md` for researched, observed, or unknown platform facts.
5. If the agent is not listed, use the `generic` adapter and record new findings in the inventory before creating a new adapter.

Adapters describe host capability and fallback behavior only. They must not redefine slash-command workflows, grading rubrics, or teaching modes.

## Downgrade Matrix

| Need | Full capability | Downgrade |
|---|---|---|
| Persist course state | Save `.oh-my-teacher/snapshots/<slug>.md` with `scripts/snapshot.py` | Emit a copyable Current Course Snapshot block |
| Update SRS | Run `scripts/srs.py update` | Emit a Markdown SRS table and next review date |
| Send daily/weekly reminders | Use confirmed proactive-message or scheduler tools after explicit opt-in | Generate the digest inline and emit a copyable Reminder Config block |
| Export flashcards | Write Markdown then run `scripts/export_flashcards.py` | Emit card Markdown; ask user to export in their tool |
| Ingest PDFs/PPTs | Read files or use PDF/PPT tooling | Ask for table of contents, key pages, screenshots, or pasted sections |
| Cite materials | Retrieval/citation tools | Quote or reference only user-provided snippets; mark uncited claims as assumptions |
| Visual explanation | Mermaid/HTML/plot/image generation | Use ASCII diagram, Markdown table, or step list |
| Code demo | Write and run a file | Provide code block plus expected output and trace |
| Math rendering | LaTeX rendered | Use plain-text formulas and avoid display math |
| Audio/oral simulation | TTS/STT | Text-only examiner prompts and grading |

## Output Rules by Environment

### Agent Shell

- Prefer deterministic scripts for snapshots, SRS, and flashcards.
- Save generated artifacts only when useful.
- Before relying on a file, verify it exists and can be read.
- Report command failures and switch to inline fallback rather than inventing output.

### RAG Notebook

- Use retrieved context as materials.
- Cite sources when the host exposes citations.
- Avoid asking the user to upload files again if the document is already in context.
- If retrieval is thin, ask for a section title, page range, or pasted excerpt.

### ima Native

- Use `search source=kb` and `fetch` for course materials before asking the user to paste content.
- Use `search source=note`, `memory_recall`, and `memory_write` for course continuity.
- Use `task_plan` for workflows longer than three steps.
- Use `use_skill name=ima-knowledge` for knowledge-base organization, `ima-note` for course home/wrong-note/SRS updates, `ima-report` for reports, and `ima-ppt` for PPT.
- Run local Python only when `shell` is explicitly available and the script succeeds.
- Label evidence as `课程资料确认`, `ima 知识库检索`, `笔记历史`, `通用课程推断`, or `需要确认`.

### Notes App

- Keep outputs Markdown-native.
- Use headings, tags, backlinks, and copyable blocks:
  - `#课程/高数`
  - `#错题`
  - `[[极限]]`
- Emit snapshots and SRS tables inline so users can paste them into notes.
- Avoid shell commands unless the user confirms the note app has an execution plugin.

### Plain Chat

- Ask for the smallest missing context only.
- Work one topic at a time to avoid context loss.
- Provide copyable snapshots, SRS tables, flashcards, and plans.
- Never say a file was saved, a script ran, or a document was read unless the host actually supports it.

## Environment Probe

When the environment is unclear and the task depends on tools, ask at most one compact probe:

```markdown
我先按普通对话框处理。若你当前工具能读取文件、运行脚本或检索笔记，请告诉我；否则我会把计划、错题和复习卡片都以内联 Markdown 输出。
```

Do not ask this probe for simple conceptual explanations or single practice questions; proceed with `plain-chat` defaults.
