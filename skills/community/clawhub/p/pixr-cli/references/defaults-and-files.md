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
- `config.json`: saved defaults for provider, base URL, API key env var name, model, output directory, per-command overrides, and profile-level overrides. The API key itself is never stored; only the env var name (`apiKeyEnv`).

Example:

```json
{
  "model": "gemini-3.1-flash-image-preview",
  "outputDir": "/absolute/path/to/renders",
  "profiles": {
    "social": {
      "provider": "openrouter",
      "apiKeyEnv": "OPENROUTER_API_KEY",
      "model": "vendor/model-id",
      "providerOptions": { "quality": "high" },
      "outputDir": "/absolute/path/to/social-renders",
      "format": "webp",
      "width": 1600,
      "height": 900
    }
  },
  "commands": {
    "edit": { "provider": "fal", "apiKeyEnv": "FAL_KEY", "model": "endpoint/id" }
  }
}
```

## Preferred Commands

- model: `pixr model <name>`
- output dir: `pixr save-dir --set "<path>"`
- scaffold home dir: `pixr config --init`
- scaffold profile: `pixr profile init <name>`
- non-interactive profile config: `pixr profile init <name> --provider ... --base-url ... --api-key-env ... --model ... --save-dir ...`

Model ids above are placeholders: always list real ones with `pixr models`. `commands.<name>` sets a different provider/model per command (`generate`, `edit`, `vary`); a profile or CLI flag overrides it.

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
