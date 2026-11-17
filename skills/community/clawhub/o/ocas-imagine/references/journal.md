# Imagine Journal Schema

Every Imagine run writes exactly one journal file. Runs missing journals are invalid per `spec-ocas-journal.md`.

## Location

```
{agent_root}/commons/journals/ocas-imagine/YYYY-MM-DD/{run_id}.json
```

`run_id` format: `r_` + 6-char hex. Example: `r_a7f2c1`.

## Journal Types

| Command | Type | Rationale |
|---|---|---|
| `imagine.generate` | Action | Active text-to-image mode call; resulting image URL or file path persisted. |
| `imagine.style.save` | Action | Mutates persistent library. |
| `imagine.extract` | Observation | Analysis only; no external side effect beyond reading the input image. |
| `imagine.library.list` | Observation | Read-only enumeration. |

## Record Shape

All records share the `JournalEntry` envelope from `spec-ocas-shared-schemas.md`:

```json
{
  "id": "r_a7f2c1",
  "skill_id": "ocas-imagine",
  "skill_version": "1.0.2",
  "command": "imagine.generate",
  "journal_type": "action",
  "timestamp": "2026-04-14T17:22:10Z",
  "inputs": { /* command-specific, see below */ },
  "outputs": { /* command-specific, see below */ },
  "status": "success",
  "error": null
}
```

## Command-Specific Fields

### `imagine.generate` (Action)

```json
{
  "inputs": {
    "style_ref": "SOMA",
    "style_source": "default_styles.md",
    "content_prompt": "A raven perched on a craggy outcrop, wings half-spread, facing left.",
    "params": { "width": 1024, "height": 1024, "seed": 42 }
  },
  "outputs": {
    "final_prompt": "<concatenated Style + Content prompt>",
    "image": "<active-mode image URL or file path>",
    "latency_ms": 18420
  }
}
```

### `imagine.extract` (Observation)

```json
{
  "inputs": {
    "image_ref": "file:///path/to/ref.jpg | https://...",
    "analysis_model": "claude-opus-4-6"
  },
  "outputs": {
    "style_prompt": "<five-section Style Prompt>",
    "verification_image": "<active-mode image URL or file path>",
    "content_bleed_detected": false
  }
}
```

### `imagine.style.save` (Action)

```json
{
  "inputs": { "name": "my-style", "prompt": "<full Style Prompt>" },
  "outputs": { "styles_jsonl_line": 14 }
}
```

### `imagine.library.list` (Observation)

```json
{
  "inputs": {},
  "outputs": { "default_count": 6, "custom_count": 3, "names": ["SOMA", "NOIR", "..."] }
}
```

## Conventions

- Write atomically: write to `{run_id}.json.tmp`, then rename.
- Immutable after write. Never edit an existing journal.
- One journal per run, regardless of success or failure. On error, set `status: "error"` and populate `error` with a short message.
