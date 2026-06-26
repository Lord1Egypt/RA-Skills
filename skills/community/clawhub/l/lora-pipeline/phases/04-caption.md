# Phase 5 — WD14 Captioning

## Input Contract

- `datasets/<lora_name>/` exists with verified, cleaned images from Phase 4
- All images are PNG, ≥1024×1024, no black borders

## Output Contract

- Each image in `datasets/<lora_name>/` has a corresponding `.txt` file
- Every `.txt` starts with the trigger word (CamelCase `<LoraName>`)
- Split children (`_a`, `_b`, `_c`) have been re-tagged with fresh captions

## Completion Signal

```
sessions_send(parent_session_id, "✅ Phase 5 complete: <N> images captioned for <lora_name>. Trigger word '<TriggerWord>' prepended to all captions. Ready for Phase 6 (training).")
```

Fallback: write to `~/.openclaw/workspace/lora_status_phase5.txt`

## Model Recommendation

`openrouter/google/gemini-2.0-flash-lite-001` (Worker) — pure bash + Python script execution, no reasoning needed

---

## Phase 5 — 開始 Caption (WD14 Local Tagging)

Run Danbooru-style captioning locally to avoid cloud costs.

```bash
python3 skills/lora-pipeline/scripts/tag_batch.py ~/.openclaw/workspace/datasets/<lora_name>/
```

Output: one `.txt` per image with tags like `1boy, muscular, shirtless, facial hair, ...`

### Prepend Trigger Word to Every Caption

```python
import os

trigger = 'DerekLunsford'  # CamelCase — creates unique token, won't overlap model weights
dataset_dir = 'datasets/<lora_name>/'

for f in os.listdir(dataset_dir):
    if f.endswith('.txt'):
        fpath = os.path.join(dataset_dir, f)
        content = open(fpath).read().strip()
        if not content.startswith(trigger):
            open(fpath, 'w').write(f'{trigger}, {content}')
```

### Trigger Word Rules
- CamelCase (e.g., `DerekLunsford`, not `derek lunsford`)
- Always at the very beginning of the `.txt`
- Never duplicated within the same file

**After tagging, re-run tagger on any split children** (files ending in `_a`, `_b`, `_c`) as they may have inherited the parent caption.

---

## Training Dataset Package (for Phase 6 handoff)

**Dataset folder naming:** `{repeats}_{FullName} {class}`
```
50_DerekLunsford man/
├── image001.png
├── image001.txt    # DerekLunsford, 1boy, muscular, ...
└── ...
```

**ZIP and hand off:**
```bash
cd ~/.openclaw/workspace/datasets/
zip -r DerekLunsford_dataset.zip "50_DerekLunsford man/"
```

Then invoke Phase 6 (training) with the ZIP path.

---

## Error Escalation

- If `tag_batch.py` fails (model not found) → check `~/.openclaw/workspace/tools/wd14-tagger/models/` exists
- Do NOT use cloud captioning APIs
- Do NOT upgrade model tier — report to parent
