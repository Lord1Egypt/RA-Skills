# Command Reference

Use this file when the task needs exact CLI invocations.

Package/install note:

- npm package name: `nanobana`
- installed binaries: `nano-img`, `nano-image`

## Global Discovery

Preferred:

- `nano-img help`
- `nano-img help generate`
- `nano-img generate --help`
- `nano-img models --help`
- `nano-img save-dir --help`

Repo-local equivalents:

- `npm run dev -- help`
- `npm run dev -- generate --help`

## Generate

Use for one-shot image creation:

```bash
nano-img generate "a minimal editorial thumbnail"
nano-img generate --save-to ./renders "a product poster"
nano-img generate -w 1600 -h 840 -f webp "a dark blog hero"
nano-img generate --ref ./extra.png --no-default-refs "a controlled studio shot"
```

Behavior:

- `-w` only: resize to requested width, preserve aspect ratio
- `-h` only: resize to requested height, preserve aspect ratio
- `-w` + `-h`: force exact output size
- `-f`: final output format, default `png`

## Models

Use for model discovery or saved model changes:

```bash
nano-img models
nano-img models --no-interactive
nano-img models --json
nano-img model
nano-img model gemini-3.1-flash-image-preview
nano-img model --clear-model
```

Notes:

- In a TTY, `nano-img models` opens an arrow-key picker.
- Enter saves the selected model.
- `q` or `Esc` cancels.

## Save Directory

Use for persistent output location:

```bash
nano-img save-dir
nano-img save-dir --set "~/nano-image"
nano-img save-dir /absolute/or/relative/path
nano-img save-dir --clear-save-dir
```

Generation precedence:

1. `--save-to` / `--output`
2. saved `outputDir` in `~/.nano-img/config.json`
3. current working directory

## Inspect Defaults

Use these before debugging:

```bash
nano-img config --json
nano-img refs --json
```

`config --json` is the fastest way to confirm:

- current model
- saved model
- saved output dir
- instruction/style paths
- detected default references
