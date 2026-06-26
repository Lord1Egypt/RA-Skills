# Troubleshooting

Use this file only when the normal workflow fails.

## Models Do Not List

Checks:

1. Verify `NANO_IMAGE_API_KEY` is set.
2. Run `nano-img models --no-interactive`.
3. If still failing, inspect the API error message directly.

Common causes:

- missing API key
- quota or billing limits
- network or upstream Gemini API failures

## Generation Fails

Start with:

```bash
nano-img config --json
```

Then verify:

1. the selected model is valid
2. refs exist and are readable
3. instruction/style files exist if the task depends on them
4. the output directory is writable

Common failures:

- `RESOURCE_EXHAUSTED` or `429`: quota exhausted
- no image parts returned: upstream model response issue
- missing refs: bad file path or unsupported extension

## Picker Or Saved Defaults Behave Unexpectedly

Checks:

1. inspect `~/.nano-img/config.json`
2. run `nano-img model`
3. run `nano-img save-dir`
4. rerun with an explicit override to isolate precedence

Examples:

```bash
nano-img model gemini-2.5-flash-image
nano-img save-dir --set "~/nano-image"
nano-img generate --save-to ./tmp "test prompt"
```

## Size Or Format Confusion

Remember:

- Gemini native image generation supports preset image settings, not arbitrary pixel output
- the CLI applies exact resize and format conversion locally after generation
- `png` is the default final format

Use:

```bash
nano-img generate -w 1600 -h 840 -f webp "test prompt"
```

to verify the final file behavior explicitly.
