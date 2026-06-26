---
name: lora-pipeline
description: End-to-end LoRA training pipeline: reference photo collection → face verification → dataset scraping → quality check → WD14 captioning → RunPod training. Use this skill whenever a user asks to build a training dataset, collect photos for a LoRA, or train a LoRA model.
---

# LoRA Pipeline

Orchestrates the full LoRA dataset-to-model pipeline. Each phase is self-contained and can be delegated to a sub-agent independently.

---

## Pipeline Overview

```
Phase 1: 蒐集範例照片   → collect 3–6 reference face photos
Phase 2: 確認人臉正確   → user confirms refs; deepface cross-check
Phase 3: 蒐集 datasets  → scrape web sources guided by face features
Phase 4: 確認照片正確   → face verify + dedup + quality filter + crop
Phase 5: 開始 caption   → WD14 local tagging + trigger word
Phase 6: LoRA training  → RunPod Kohya training → retrieve outputs
```

---

## Phase Index

| Phase | File | Can Sub-Agent | Model | Est. Time |
|-------|------|:---:|---|---|
| 01 — Reference Collection | `phases/01-reference.md` | ✅ | Haiku (Worker) | 5–10 min |
| 02 — Scraping | `phases/02-scraping.md` | ✅ | Haiku (Worker) | 10–30 min |
| 03 — Verify & Clean | `phases/03-verify.md` | ✅ | Haiku (Worker) | 2–5 min |
| 04 — Caption | `phases/04-caption.md` | ✅ | Haiku (Worker) | 1–3 min |
| 05 — Training | `phases/05-training.md` | ✅ | Haiku (Worker) + Sentry | 15–30 min |

**To load a specific phase:** read `skills/lora-pipeline/phases/<phase-file>` — each file is independently readable.

---

## Directory Structure

```
~/.openclaw/workspace/
└── datasets/
    ├── face_references/
    │   └── <lora_name>/          # Phase 1–2: Gold standard refs (3–6 photos)
    │       ├── ref_01.jpg
    │       └── ...
    ├── <lora_name>_raw/          # Phase 3: Raw scraped images (pre-verification)
    │   └── ...
    └── <lora_name>/              # Phase 4–5: Verified + captioned training set
        ├── image001.png
        ├── image001.txt
        └── ...
```

---

## Privacy Rules (CRITICAL — All Phases)

- **NO DATA INSPECTION**: Do NOT `cat`, `read`, or analyze image file contents or `.txt` caption files.
- **NO CLOUD UPLOAD**: All face verification (DeepFace) must run **locally**. Never send images to cloud APIs.
- **NO DATA LEAKAGE**: Do not describe dataset details (person names, attributes) to the LLM unnecessarily.
- Treat datasets as opaque binary blobs except when running local scripts.

---

## Quality Standards (SDXL)

- **Resolution:** 1024×1024 minimum after crop
- **Format:** Convert all to PNG before training
- **No black borders:** Run autocrop before final save
- **Dataset diversity:** ≥30% clothed/natural skin shots

---

## Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `tag_batch.py` | `skills/lora-pipeline/scripts/tag_batch.py` | Local WD14 ONNX tagger for a directory |
| `smart_crop.py` | `skills/lora-pipeline/scripts/smart_crop.py` | Interactive or automated single-subject cropping |
| `batch_lora_train.py` | `skills/lora-pipeline/scripts/batch_lora_train.py` | Kohya batch training runner for RunPod |

---

## Sub-Agent Protocol

Each phase file contains:
1. **Input Contract** — what must already exist before this phase starts
2. **Output Contract** — what this phase produces
3. **Completion Signal** — how to report back (`sessions_send` + status file fallback)
4. **Error Escalation** — sub-agent reports to parent, never self-escalates model tier
