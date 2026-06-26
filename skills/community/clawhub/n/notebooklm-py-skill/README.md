# notebooklm-py-skill

OpenClaw skill for operating Google NotebookLM through the `notebooklm-py` CLI.

## What It Does

- Verifies NotebookLM authentication.
- Lists, creates, renames, and inspects notebooks.
- Adds URL, file, YouTube, Drive, research, and inline text sources.
- Asks NotebookLM questions and returns source-grounded answers.
- Generates and downloads NotebookLM artifacts such as audio, video, slide decks, reports, quizzes, flashcards, infographics, data tables, and mind maps.
- Uses safe defaults for destructive, long-running, and file-writing operations.

## Requirements

- `notebooklm-py` installed and available as `notebooklm`.
- A valid NotebookLM login profile.

Install:

```bash
pipx install notebooklm-py
notebooklm login
notebooklm auth check --test --json
```

## Skill Layout

```text
notebooklm-py/
├── SKILL.md
├── README.md
├── _meta.json
└── references/
    └── notebooklm-py-cli.md
```

## Usage Examples

```bash
notebooklm list --json
notebooklm source add "https://example.com" -n NOTEBOOK_ID --json
notebooklm ask "What are the key points?" -n NOTEBOOK_ID --json
notebooklm generate report "Create a concise briefing" -n NOTEBOOK_ID --json
```

For generated text files, use stdin upload:

```bash
notebooklm source add - --type text --title "notes.md" -n NOTEBOOK_ID --json < /tmp/openclaw-attachments/notes.md
```

## Safety Notes

- The skill asks before destructive or long-running work.
- Automation should pass explicit notebook IDs rather than relying on shared CLI context.
- Temporary files should be created under a temporary directory and cleaned up after use.
- `notebooklm doctor --fix` requires explicit user confirmation.

## Version

Current public version: `1.0.1`.
