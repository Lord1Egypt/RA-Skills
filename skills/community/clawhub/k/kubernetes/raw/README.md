# raw/ — Source Documents

Drop source files here. Supported formats:
- `.md` — Markdown articles, notes
- `.txt` — Plain text
- `.pdf` — PDFs (agent can extract text)
- `.png`, `.jpg`, `.gif` — Images (go in `assets/`)

## Conventions

- Files are **immutable** — the agent reads but never modifies them
- Use descriptive filenames: `YYYY-MM-DD-title.md`
- Images go in `assets/` subdirectory
- The agent creates wiki summaries in `wiki/` pointing back to these sources
