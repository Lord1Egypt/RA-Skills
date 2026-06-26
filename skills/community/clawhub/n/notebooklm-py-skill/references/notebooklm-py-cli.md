# notebooklm-py CLI Reference

## Setup

- Install CLI with `pipx install notebooklm-py` or `pip install notebooklm-py`.
- Authenticate with `notebooklm login`.
- Verify real auth with `notebooklm auth check --test --json`; `notebooklm status` only reports local context.
- Use `NOTEBOOKLM_HOME` or `NOTEBOOKLM_PROFILE` for account/profile isolation.

## Version Notes

- Verified against `notebooklm-py 0.5.0`.
- `source add` auto-detects URL, YouTube URL, existing file path, or text.
- `source add -` reads inline text from stdin.
- `source delete` and `source clean` support `--yes`.
- `source list --json` returns status strings such as `ready` and `preparing`.
- For text files, prefer stdin upload; `source add --type text FILE` uploads the literal file path text in 0.5.0.

## Command Groups

- Session/auth: `login`, `status`, `clear`, `doctor`, `auth check|inspect|refresh|logout`, `profile *`
- Notebooks: `list`, `create`, `delete`, `rename`, `summary`, `metadata`
- Sources: `source add|add-drive|add-research|clean|delete|delete-by-title|fulltext|get|guide|list|refresh|rename|stale|wait`
- Chat: `ask`, `configure`, `history`
- Artifacts: `generate *`, `artifact list|get|wait|delete|export|suggestions`, `download *`
- Notes, sharing, language: `note *`, `share *`, `language get|set|list`

## Artifacts

Generation examples:

```bash
notebooklm generate audio "instructions" -n NOTEBOOK_ID --json
notebooklm generate video "instructions" -n NOTEBOOK_ID --json
notebooklm generate slide-deck "instructions" -n NOTEBOOK_ID --json
notebooklm generate report "instructions" --format briefing-doc -n NOTEBOOK_ID --json
notebooklm generate quiz "instructions" -n NOTEBOOK_ID --json
notebooklm generate flashcards "instructions" -n NOTEBOOK_ID --json
notebooklm generate infographic "instructions" -n NOTEBOOK_ID --json
notebooklm generate data-table "instructions" -n NOTEBOOK_ID --json
notebooklm generate mind-map -n NOTEBOOK_ID --json
```

Download examples:

```bash
notebooklm download audio ./output.mp3 -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download video ./output.mp4 -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download slide-deck ./slides.pdf -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download slide-deck ./slides.pptx --format pptx -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download report ./report.md -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download mind-map ./map.json -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download data-table ./table.csv -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download quiz ./quiz.md --format markdown -n NOTEBOOK_ID -a ARTIFACT_ID
notebooklm download flashcards ./cards.md --format markdown -n NOTEBOOK_ID -a ARTIFACT_ID
```

## Deep Research

```bash
notebooklm source add-research "topic query" -n NOTEBOOK_ID --mode fast --import-all
notebooklm source add-research "topic query" -n NOTEBOOK_ID --mode deep --no-wait
notebooklm research wait -n NOTEBOOK_ID --timeout 600 --import-all --json
```

Use `--prompt-file` for long research queries.

## Text Source Upload

For generated Markdown/text files, prefer stdin text upload:

```bash
notebooklm source add - --type text --title "title.md" -n NOTEBOOK_ID --json < /tmp/openclaw-attachments/title.md
```

For binary or native files, upload as files:

```bash
notebooklm source add ./document.pdf -n NOTEBOOK_ID --json
notebooklm source add ./deck.pptx -n NOTEBOOK_ID --json
```

## Error Handling

- Auth failure: run `notebooklm auth check --test --json`; if stale, ask before `notebooklm login`.
- Ambiguous notebook: use full UUIDs rather than partial IDs.
- Newly added sources not usable yet: run `source wait SOURCE_ID -n NOTEBOOK_ID --json`.
- Parallel agents overwriting context: pass explicit notebook IDs or isolate with `NOTEBOOKLM_PROFILE`.
- Long generation/download: confirm destination and expected output before starting.
