# Contributing to OpenCode ACP Control

Thanks for your interest in improving this skill. Most changes here are
documentation or examples — the core capability is the `SKILL.md` instruction
set that any ACP-compatible AI agent can load.

## Quick start

```bash
git clone https://github.com/berriosb/Opencode-Acp-Control.git
cd Opencode-Acp-Control
```

Edits to `SKILL.md` are validated by CI:

- `markdownlint-cli` (rules in `.markdownlint.json`)
- `lychee` link checker for every URL referenced in docs
- `ruff check` and `python3 -m py_compile` on `examples/acp_demo.py`

## Where to make changes

| File | What it controls |
|---|---|
| `SKILL.md` | The instruction set agents load. Keep it tool-agnostic. |
| `examples/acp_demo.py` | Runnable end-to-end demo against a real `opencode acp` process. |
| `README.md` | Public-facing project description and quick start. |
| `CHANGELOG.md` | Release notes, Keep a Changelog format. |
| `_meta.json` | Registry metadata (do not edit `ownerId`/`slug`; only bump `version`/`publishedAt` on release). |

## Style

- Markdown follows the existing tone: short sections, tables, code blocks with
  JSON-RPC frames, no marketing fluff.
- Tool references in `SKILL.md` use generic names (`terminal`, `process.write`,
  `process.poll`, `process.kill`, `web_fetch`, `ask_user`). Map them to your
  platform in `README.md` instead.
- Python in `examples/` uses stdlib only (no third-party deps).
- `acp_demo.py` exposes `--dry-run` and `--no-prompt` modes so the workflow
  can be exercised without a configured LLM provider.

## Tests

```bash
# Markdown lint
markdownlint SKILL.md README.md CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md

# Python syntax + ruff
ruff check examples/acp_demo.py
python3 -m py_compile examples/acp_demo.py

# Run the demo in dry-run mode (no opencode binary required)
python3 examples/acp_demo.py --dry-run
```

## Commit messages

Conventional commits in English: `feat:`, `fix:`, `docs:`, `chore:`. The
release pipeline uses standard-version to bump the version and update
`CHANGELOG.md`, so commit messages become changelog entries.

## Reporting issues

Open an issue at <https://github.com/berriosb/Opencode-Acp-Control/issues>
with:

- Which agent platform you are loading the skill into (Hermes Agent,
  Clawdbot, custom, etc.)
- The exact `opencode --version` you are running
- A minimal reproduction of the unexpected behavior

## License

By contributing, you agree that your contributions will be licensed under the
MIT License (see [`LICENSE`](./LICENSE)).