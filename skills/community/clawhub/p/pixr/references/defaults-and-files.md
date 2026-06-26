# Defaults And Files

## Home Directory Layout

```text
~/.pixr/
├── config.json
├── INSTRUCTION.md
├── STYLE.md
├── prompts/
│   ├── generate.md
│   ├── edit.md
│   └── vary.md
├── assets/
│   ├── common/
│   ├── generate/
│   ├── edit/
│   └── vary/
└── profiles/
    └── social/
        ├── INSTRUCTION.md
        ├── STYLE.md
        └── assets/
```

Legacy paths still read when present:

```text
~/.nano-img/
~/.nano-image/STYLE.md
```

## File Roles

- `INSTRUCTION.md`: persistent non-style guidance
- `STYLE.md`: persistent style guidance
- `prompts/<command>.md`: prompt prefix applied per command
- `assets/`: default reference images used unless `--no-default-refs` is passed
- `profiles/<name>/...`: profile-specific overrides for instructions, style, and assets
- `config.json`: saved defaults for model, output directory, and profile-level overrides

Example:

```json
{
  "model": "gemini-3.1-flash-image-preview",
  "outputDir": "/absolute/path/to/renders",
  "profiles": {
    "social": {
      "model": "gemini-3.1-flash-image-preview",
      "outputDir": "/absolute/path/to/social-renders",
      "format": "webp",
      "width": 1600,
      "height": 900
    }
  }
}
```

## Preferred Commands

- model: `pixr model <name>`
- output dir: `pixr save-dir --set "<path>"`
- scaffold home dir: `pixr config --init`
- scaffold profile: `pixr profile init <name>`
- non-interactive profile config: `pixr profile init <name> --model ... --save-dir ...`

## Inspect

```bash
pixr config --json
pixr refs --json
find ~/.pixr -maxdepth 2 -type f | sort
```

## Notes

- `save-dir --set "~/Pictures/pixr"` expands `~` to the current user's home directory
- `--save-to` and `--output` are aliases
- if more than three default asset images exist, `pixr` keeps the latest three by modified time
