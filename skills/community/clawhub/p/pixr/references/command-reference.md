# Command Reference

## Identity

- npm package name: `pixr-cli`
- installed binary: `pixr`

## Help

- `pixr help`
- `pixr help edit`
- `pixr help vary`
- `pixr help generate`
- `pixr help profile`
- `pixr edit --help`
- `pixr vary --help`
- `pixr generate --help`
- `pixr profile --help`
- `pixr models --help`
- `pixr save-dir --help`

## Generate

Use for one-shot image creation:

```bash
pixr gen "a minimal editorial thumbnail"
pixr generate "a minimal editorial thumbnail"
pixr generate --save-to ./renders "a product poster"
pixr generate -w 1600 -h 840 -f webp "a dark blog hero"
pixr generate --ref ./extra.png --no-default-refs "a controlled studio shot"
```

## Edit

Use for text-guided image edits:

```bash
pixr edit ./hero.png "turn this into a premium ad with softer lighting"
pixr edit --input ./hero.png --count 2 "replace the label and keep the bottle shape"
pixr edit ./hero.png --ref ./logo.png "integrate this logo into the design"
```

## Vary

Use for Gemini-based variations of an existing image:

```bash
pixr vary ./hero.png
pixr vary ./hero.png --count 3
pixr vary ./hero.png "keep the same subject, explore bolder compositions"
```

## Models

```bash
pixr models
pixr models --no-interactive
pixr models --json
pixr model
pixr model gemini-3.1-flash-image-preview
pixr model --clear-model
```

Notes:

- In a TTY, `pixr models` opens an arrow-key picker.
- The chosen model is saved to config on Enter.

## Profiles

```bash
pixr config --init
pixr profile list
pixr profile show social
pixr profile init social
pixr profile init social --model gemini-3.1-flash-image-preview --save-dir "~/Pictures/pixr/social"
```

Notes:

- `config --init` scaffolds `~/.pixr/` without overwriting existing files.
- `profile init <name>` creates `INSTRUCTION.md`, `STYLE.md`, and `assets/` for that profile.
- In a TTY, `profile init <name>` asks for model, format, save dir, dimensions, prefix, and default-profile choice unless you pass flags or `--no-interactive`.
- Profiles can save their own `model` and `outputDir`, so `pixr config --profile <name> --json` can resolve differently from the global defaults.
- `profile show <name>` reports whether the profile comes from config, files, or both.

## Output Directory

```bash
pixr save-dir
pixr save-dir --set "~/Pictures/pixr"
pixr save-dir /absolute/or/relative/path
pixr save-dir --clear-save-dir
```

Resolution order:

1. explicit `--save-to` or `--output`
2. saved `outputDir` in `~/.pixr/config.json`
3. current working directory

## Inspect

```bash
pixr config --json
pixr refs --json
```

Notes:

- If more than three default asset images exist, `pixr` uses the latest three by modified time and emits a warning.
