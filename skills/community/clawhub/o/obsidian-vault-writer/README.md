# obsidian-vault-writer

Write and append content to Obsidian vaults from AI agents using `notesmd-cli`. No Obsidian desktop app or Obsidian Sync subscription required — designed for servers, VPS, and headless environments.

## Use Cases

- Save X post drafts to today's daily note (called from x-post-strategist)
- Append structured notes or summaries to daily notes
- Create new notes in the vault from agent output
- Write to a vault on a remote server without the Obsidian desktop app

## Requirements

`notesmd-cli` installed and a vault directory accessible as a local path. No Obsidian app required.

**Install:**
```bash
brew tap yakitrak/yakitrak
brew install yakitrak/yakitrak/notesmd-cli
```

Or build from source — see [references/notesmd-cli.md](references/notesmd-cli.md).

## References

- [notesmd-cli.md](references/notesmd-cli.md) — CLI command reference and install guide
- [obsidian-markdown.md](references/obsidian-markdown.md) — Obsidian Flavored Markdown syntax
- [obsidian-canvas.md](references/obsidian-canvas.md) — JSON Canvas file format
- [obsidian-bases.md](references/obsidian-bases.md) — Obsidian Bases (.base files)

## Feedback & Contributions

Found a bug or want a feature? [Open an issue](https://github.com/archlab-space/Open-Skill-Hub/issues).
