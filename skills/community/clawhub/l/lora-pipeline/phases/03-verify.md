# Phase 4 — Verify & Clean Dataset

## Input Contract

- `datasets/face_references/<lora_name>/` exists with approved reference photos
- `datasets/<lora_name>_raw/` exists with raw scraped images from Phase 3

## Output Contract

- `datasets/<lora_name>/` contains only verified, cropped, deduplicated images
- Each image is PNG with no black borders
- No duplicate poses (max 2 per angle)
- ≥30% clothed/natural skin shots in final set

## Completion Signal

```
sessions_send(parent_session_id, "✅ Phase 4 complete: <N> images passed verification for <lora_name>. <M> rejected. Dataset at datasets/<lora_name>/. Ready for Phase 5 (caption).")
```

Fallback: write to `~/.openclaw/workspace/lora_status_phase4.txt`

## Model Recommendation

`openrouter/google/gemini-2.0-flash-lite-001` (Worker) — pure bash + Python scripts, no browser needed

---

## Phase 4 — 確認照片正確 (Verify & Clean Dataset)

Four-step quality gate on the raw scraped photos. Run in this order:

### Step 4a — Grid / Collage Splitting + Autocrop + PNG Convert

Detect collages, autocrop black borders, convert all to PNG in one pass.

```python
import cv2, os, shutil
import numpy as np
from PIL import Image

RAW = 'datasets/<lora_name>_raw/'
OUT = 'datasets/<lora_name>/'
os.makedirs(OUT, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
files = sorted([f for f in os.listdir(RAW) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))])

for fname in files:
    src = os.path.join(RAW, fname)
    stem = os.path.splitext(fname)[0]
    try:
        img = Image.open(src).convert('RGB')
    except Exception as e:
        print(f'  ⚠️  skip {fname}: {e}')
        continue

    # autocrop black borders
    bbox = img.convert('L').point(lambda p: 255 if p > 15 else 0).getbbox()
    if bbox:
        img = img.crop(bbox)

    # collage detection: ≥2 faces spanning >50% width → split
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY), 1.1, 4)
    if len(faces) >= 2:
        xs = [x for (x, y, w, h) in faces]
        if (max(xs) - min(xs)) / img.width > 0.5:
            w, h = img.size
            for box, suf in [((0, 0, w//2, h), '_a'), ((w//2, 0, w, h), '_b')]:
                part = img.crop(box)
                if part.width >= 256 and part.height >= 256:
                    part.save(os.path.join(OUT, f'{stem}{suf}.png'))
            continue

    img.save(os.path.join(OUT, f'{stem}.png'))
```

**Naming for splits:** `filename_a`, `filename_b` (left→right).

### Step 4b — Manual Blacklist (Pre-Verification)

Before running face verify, check if a blacklist file exists and pre-exclude known wrong images.

```python
import json, os, shutil

BLACKLIST_FILE = 'datasets/<lora_name>_blacklist.json'
OUT = 'datasets/<lora_name>/'
REJECT = 'datasets/<lora_name>_rejected/'
os.makedirs(REJECT, exist_ok=True)

if os.path.exists(BLACKLIST_FILE):
    blacklist = json.load(open(BLACKLIST_FILE))
    for fname in blacklist:
        src = os.path.join(OUT, fname)
        if os.path.exists(src):
            shutil.move(src, os.path.join(REJECT, fname))
            print(f'  🚫 blacklisted: {fname}')
```

**Blacklist format** (`datasets/<lora_name>_blacklist.json`):
```json
["image_029_a.png", "image_029_b.png"]
```

When to use: images that consistently pass face verify despite being clearly wrong (model blind spot).

### Step 4c — Face Verification (Local — Privacy Critical)

**NEVER send images to any cloud API. All deepface processing must be local.**

**Model:** `Facenet512` + `retinaface` detector (more accurate than Facenet + opencv)
**Threshold:** `0.3` (Facenet512 scale — lower = stricter)
**Fallback:** if retinaface fails to detect a face, retry with `enforce_detection=False`

```python
import os, shutil
from deepface import DeepFace

reference_dir = 'datasets/face_references/<lora_name>/'
target_dir = 'datasets/<lora_name>/'
reject_dir = 'datasets/<lora_name>_rejected/'
THRESHOLD = 0.3

os.makedirs(reject_dir, exist_ok=True)
refs = [os.path.join(reference_dir, f) for f in os.listdir(reference_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.endswith('.md')]

for img_file in sorted(os.listdir(target_dir)):
    if not img_file.endswith('.png'):
        continue
    img_path = os.path.join(target_dir, img_file)
    best = 999
    for ref_path in refs:
        try:
            r = DeepFace.verify(img_path, ref_path,
                                model_name='Facenet512',
                                detector_backend='retinaface',
                                enforce_detection=True)
            best = min(best, r['distance'])
        except Exception:
            try:  # fallback: no face detected → compare whole image
                r = DeepFace.verify(img_path, ref_path,
                                    model_name='Facenet512',
                                    detector_backend='retinaface',
                                    enforce_detection=False)
                best = min(best, r['distance'])
            except Exception:
                pass

    if best <= THRESHOLD:
        print(f'  ✅ {img_file} (dist={best:.3f})')
    else:
        shutil.move(img_path, os.path.join(reject_dir, img_file))
        print(f'  ❌ {img_file} (dist={best:.3f})')
```

**Result categories:**
- `dist ≤ 0.3` → ✅ pass
- `dist 0.3–0.5` → borderline — human review recommended
- `dist > 0.5` → ❌ reject (likely different person)

> **Note:** Special makeup, costumes, or unusual angles can push distance above threshold for the correct person. Always do a human spot-check on borderline rejects before discarding.

### Step 4d — Duplicate Pose Detection

Prevent overfitting from too many similar poses.

```python
import os, imagehash
from PIL import Image

target_dir = 'datasets/<lora_name>/'
files = sorted([os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.endswith('.png')])

hashes = {}
for f in files:
    try:
        hashes[f] = imagehash.phash(Image.open(f))
    except:
        pass

removed, checked = [], set()
for f1 in hashes:
    if f1 in checked:
        continue
    group = [f1]
    for f2 in hashes:
        if f2 != f1 and f2 not in checked and hashes[f1] - hashes[f2] < 8:
            group.append(f2)
    if len(group) > 1:
        group.sort(key=lambda x: os.path.getsize(x), reverse=True)
        for dup in group[1:]:
            os.remove(dup)
            removed.append(os.path.basename(dup))
            print(f'  🗑️  {os.path.basename(dup)} (dup of {os.path.basename(group[0])})')
    checked.update(group)
```

**Guideline:** Max 2 images with the same pose/angle. Final dataset diversity:
- Different poses (front, back, side, 3/4)
- Different scenarios (stage, training, lifestyle, clothed)
- Clothed / natural skin ≥30% of dataset

---

## Quality Standards

- **Format:** PNG (convert during Step 4a)
- **No black borders:** Autocrop in Step 4a
- **Min size after crop:** 256×256 (discard smaller splits)

**Final dataset path:** `datasets/<lora_name>/`

---

## Error Escalation

- If fewer than 15 images pass verification → report to parent session before proceeding
- If many correct images are rejected (borderline dist 0.3–0.5) → add to manual rescue list and re-run, or lower threshold to 0.35
- Do NOT send images to cloud APIs
- Do NOT upgrade model tier — report to parent
