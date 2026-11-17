# lifeos-skill

Agent skill for working with a [LifeOS / Obsidian PARA vault](https://lifeos.md/)
through the public `@life-os/cli` command-line tool.

The skill teaches coding agents how to read, search, append to, and update
LifeOS notes, tasks, periodic notes, PARA theme notes, tags, and LifeOS AI Wiki
pages without opening Obsidian or Aino.

## Features

- Uses `npx -y @life-os/cli`, so no global CLI install is required
- Works with the user's real vault settings, PARA folders, templates, and
  periodic-note formats
- Covers common workflows such as daily capture, task review, theme-note
  creation, periodic review, note search, safe task toggling, and LifeOS AI Wiki
  `.AI.md` topic-page maintenance
- Includes command and AI Wiki references in `references/`

## Installation

```bash
npx skills add quanru/lifeos-skill
```

For Codex project-local installation:

```bash
npx skills add quanru/lifeos-skill -a codex
```

## Usage

In your coding agent, ask for LifeOS vault work:

```text
What is on my LifeOS task list today?
```

```text
Add this thought to today's daily note: ...
```

```text
Create a project note for my quarterly planning work.
```

```text
Update AI Wiki for every topic under 2 Projects/
```

The skill will call `npx -y @life-os/cli` as needed.

## Prerequisites

- Node.js 18+
- A [LifeOS / Obsidian PARA vault](https://lifeos.md/) accessible on disk
- `@life-os/cli` available through npm, invoked by the skill with `npx -y`

## License

MIT
