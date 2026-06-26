# Defaults And Files

Use this file when the task is about persistent defaults, reusable prompts, or local assets.

## Home Directory Layout

```text
~/.nano-img/
├── assets/
├── INSTRUCTION.md
├── STYLE.md
└── config.json
```

Fallback style path:

```text
~/.nano-image/STYLE.md
```

## What Lives Where

- `assets/`: default reference images used unless `--no-default-refs` is passed
- `INSTRUCTION.md`: persistent generation instructions
- `STYLE.md`: persistent style guidance
- `config.json`: saved model and saved output directory

## Supported Saved Config Keys

Current keys used by this CLI:

```json
{
  "model": "gemini-3.1-flash-image-preview",
  "outputDir": "/absolute/path"
}
```

## Preferred Ways To Change Defaults

Prefer commands over manual file edits:

- model: `nano-img model <name>`
- output dir: `nano-img save-dir --set "<path>"`

Only edit `INSTRUCTION.md`, `STYLE.md`, or `assets/` directly when the user wants to change reusable creative defaults.

## Useful Inspection Commands

```bash
nano-img config --json
nano-img refs --json
find ~/.nano-img -maxdepth 2 -type f | sort
```

## Path Handling

- `save-dir --set "~/nano-image"` expands `~` to the current user's home directory
- relative paths are resolved from the current working directory at the time the command is run
- saved `outputDir` is stored as an absolute path in config
