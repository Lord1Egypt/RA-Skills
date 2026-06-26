# Slides handling

## Detecting slide-style outputs

Common cases:
- Manus returns a `.pptx` directly
- Manus returns a JSON bundle describing slides/pages
- Manus returns HTML slide files plus assets

## Preferred handling order

1. If `.pptx` already exists, send it directly.
2. If a slides JSON bundle exists, convert it with `scripts/manus_slides_json_to_pptx.mjs`.
3. If only HTML/assets exist, keep the raw files and decide whether to package or send a task URL.

## Convert JSON to PPTX

```bash
node scripts/manus_slides_json_to_pptx.mjs <slides.json> <output.pptx>
```

## Suggested filenames

- Use the task title if available.
- Otherwise use `manus-slides-<task_id>.pptx`.

## Return strategy

- Send the generated PPTX first.
- If conversion fails, tell the user it is a slides bundle and attach/send the raw JSON when useful.
