---
name: organise-photos
description: Organize a photo folder by cleaning non-photo files, removing bad exposures, detecting blur and burst shots, and classifying photos into numbered subfolders using AI vision analysis.
---

# Photo Folder Organizer

Intelligently organize a photo folder: clean non-photo files, remove bad exposures locally, detect blur/burst via Python, analyze content with AI vision, and sort into categorized subfolders.

## Usage

User wants to organize a photo folder: $ARGUMENTS

If the user has not provided a folder path, ask them to provide one.

**Language note**: Detect the language the user is writing in and respond in that language throughout the entire session. Category folder names should also be in the user's language.

---

## Step 1: Scan the Folder

Scan the folder for all files (non-recursive at root level):

```bash
# List all files with sizes
ls -la "$FOLDER"

# Find photo files (common extensions)
find "$FOLDER" -maxdepth 1 -type f \( \
  -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
  -o -iname "*.heic" -o -iname "*.heif" \
  -o -iname "*.raw" -o -iname "*.cr2" -o -iname "*.cr3" \
  -o -iname "*.nef" -o -iname "*.arw" -o -iname "*.dng" \
  -o -iname "*.tiff" -o -iname "*.tif" -o -iname "*.bmp" \
  -o -iname "*.webp" -o -iname "*.gif" \
\)

# Find non-photo files
find "$FOLDER" -maxdepth 1 -type f ! \( \
  -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
  -o -iname "*.heic" -o -iname "*.heif" \
  -o -iname "*.raw" -o -iname "*.cr2" -o -iname "*.cr3" \
  -o -iname "*.nef" -o -iname "*.arw" -o -iname "*.dng" \
  -o -iname "*.tiff" -o -iname "*.tif" -o -iname "*.bmp" \
  -o -iname "*.webp" -o -iname "*.gif" \
\)
```

Report to user:
- Total files found
- Number of photo files
- Number of non-photo files (list them)

---

## Step 2: Handle Non-Photo Files

**Use AskUserQuestion** (only if non-photo files exist):

Question: "Found N non-photo file(s). How would you like to handle them?"
Options:
- "Move to _misc subfolder (Recommended)"
- "Delete all non-photo files"
- "Leave them as-is"

```bash
mkdir -p "$FOLDER/_misc"
mv [non-photo files] "$FOLDER/_misc/"
```

---

## Step 3: Remove Bad Exposure Photos (Local Python)

**Use AskUserQuestion**:

Question: "Would you like to remove photos with severely bad exposure (near-black or near-white)?"
Options:
- "Yes, use default thresholds (brightness mean < 5% or > 95%) (Recommended)"
- "Yes, let me specify custom thresholds"
- "No, keep all photos"

Run a Python script to detect and report bad exposures **without deleting yet**:

```python
#!/usr/bin/env python3
"""Detect near-black or near-white photos using Pillow."""
import sys
import os
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    os.system("pip install Pillow numpy -q")
    from PIL import Image
    import numpy as np

FOLDER = sys.argv[1]
LOW_THRESH = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05   # < 5% = near-black
HIGH_THRESH = float(sys.argv[3]) if len(sys.argv) > 3 else 0.95  # > 95% = near-white

PHOTO_EXTS = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp',
              '.tiff', '.tif', '.webp', '.gif'}

bad = []
for f in sorted(Path(FOLDER).iterdir()):
    if f.suffix.lower() not in PHOTO_EXTS:
        continue
    try:
        with Image.open(f) as img:
            # Convert to grayscale for brightness analysis
            gray = img.convert('L')
            arr = np.array(gray, dtype=np.float32) / 255.0
            mean = float(arr.mean())
            if mean < LOW_THRESH or mean > HIGH_THRESH:
                label = "near-black" if mean < LOW_THRESH else "near-white"
                bad.append((f.name, mean, label))
    except Exception as e:
        print(f"Skipping {f.name}: {e}", file=sys.stderr)

if not bad:
    print("No severely bad exposure photos found.")
else:
    print(f"Found {len(bad)} problematic photo(s):")
    for name, mean, label in bad:
        print(f"  {label}  brightness={mean:.3f}  {name}")
```

Run: `python3 /tmp/detect_bad_exposure.py "$FOLDER" 0.05 0.95`

Show the list to user, then **confirm before deleting**:

```bash
rm "$BAD_PHOTO"
# or
mkdir -p "$FOLDER/_rejected_exposure"
mv "$BAD_PHOTO" "$FOLDER/_rejected_exposure/"
```

---

## Step 4: Detect Blur and Burst Shots (Local Python)

Run a comprehensive Python analysis script on all remaining photos. This step:
1. Scores each photo's sharpness (Laplacian variance)
2. Detects burst groups (photos taken within 3 seconds of each other OR with near-identical perceptual hash)

```python
#!/usr/bin/env python3
"""Analyze photos for blur and burst grouping."""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

try:
    import cv2
    import numpy as np
    from PIL import Image
    from PIL.ExifTags import TAGS
    import imagehash
except ImportError:
    os.system("pip install opencv-python-headless Pillow imagehash numpy -q")
    import cv2
    import numpy as np
    from PIL import Image
    from PIL.ExifTags import TAGS
    import imagehash

FOLDER = sys.argv[1]
BLUR_THRESHOLD = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0  # Laplacian variance below this = blurry
BURST_SECONDS = int(sys.argv[3]) if len(sys.argv) > 3 else 3         # seconds between shots = same burst
PHASH_DIST = int(sys.argv[4]) if len(sys.argv) > 4 else 8            # perceptual hash distance threshold

PHOTO_EXTS = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.bmp',
              '.tiff', '.tif', '.webp'}

def get_exif_datetime(img_path):
    """Extract DateTimeOriginal from EXIF."""
    try:
        with Image.open(img_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    # Fall back to file modification time
    return datetime.fromtimestamp(Path(img_path).stat().st_mtime)

def laplacian_sharpness(img_path):
    """Compute Laplacian variance as sharpness score. Higher = sharper."""
    img = cv2.imread(str(img_path))
    if img is None:
        return 0.0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

# Collect all photos
photos = []
for f in sorted(Path(FOLDER).iterdir()):
    if f.suffix.lower() not in PHOTO_EXTS or f.name.startswith('.'):
        continue
    photos.append(f)

print(f"Analyzing {len(photos)} photos...", flush=True)

results = []
for i, f in enumerate(photos):
    print(f"  [{i+1}/{len(photos)}] {f.name}", flush=True)
    dt = get_exif_datetime(f)
    sharp = laplacian_sharpness(f)
    try:
        ph = imagehash.phash(Image.open(f))
    except Exception:
        ph = None
    results.append({
        "file": f.name,
        "path": str(f),
        "datetime": dt.isoformat(),
        "sharpness": sharp,
        "blurry": sharp < BLUR_THRESHOLD,
        "phash": str(ph) if ph else None,
    })

# Detect burst groups: same timestamp (within N seconds) OR similar phash
groups = []
used = set()
for i, r in enumerate(results):
    if i in used:
        continue
    group = [i]
    used.add(i)
    t1 = datetime.fromisoformat(r["datetime"])
    for j, r2 in enumerate(results):
        if j <= i or j in used:
            continue
        t2 = datetime.fromisoformat(r2["datetime"])
        time_close = abs((t2 - t1).total_seconds()) <= BURST_SECONDS
        hash_close = (r["phash"] and r2["phash"] and
                      imagehash.hex_to_hash(r["phash"]) - imagehash.hex_to_hash(r2["phash"]) <= PHASH_DIST)
        if time_close or hash_close:
            group.append(j)
            used.add(j)
    if len(group) > 1:
        groups.append(group)

# Mark burst membership
for g_idx, group in enumerate(groups):
    # Find sharpest in group
    best_idx = max(group, key=lambda i: results[i]["sharpness"])
    for idx in group:
        results[idx]["burst_group"] = g_idx + 1
        results[idx]["burst_best"] = (idx == best_idx)
        results[idx]["burst_size"] = len(group)

# Output JSON for further processing
output = {
    "photos": results,
    "burst_groups": len(groups),
    "blurry_count": sum(1 for r in results if r.get("blurry")),
    "blur_threshold": BLUR_THRESHOLD,
}
with open("/tmp/photo_analysis.json", "w") as fout:
    json.dump(output, fout, indent=2, ensure_ascii=False)

# Print summary
blurry = [r for r in results if r.get("blurry")]
burst_photos = [r for r in results if "burst_group" in r]
print(f"\n=== Analysis Complete ===")
print(f"Blurry photos (sharpness < {BLUR_THRESHOLD}): {len(blurry)}")
print(f"Burst groups: {len(groups)} group(s) ({len(burst_photos)} photos total)")
if blurry:
    print("\nBlurry photo list:")
    for r in blurry:
        print(f"  sharpness={r['sharpness']:.1f}  {r['file']}")
if groups:
    print(f"\nBurst group details:")
    for g_idx, group in enumerate(groups):
        print(f"  Group {g_idx+1} ({len(group)} photos):")
        for idx in group:
            r = results[idx]
            best_mark = "★ sharpest" if r.get("burst_best") else ""
            print(f"    {r['file']}  sharpness={r['sharpness']:.1f} {best_mark}")
print("\nFull analysis saved to /tmp/photo_analysis.json")
```

Run: `python3 /tmp/analyze_photos.py "$FOLDER" 80 3 8`

---

## Step 5: Handle Blurry Photos

If any blurry photos were found:

**Use AskUserQuestion**:

Question: "Found N blurry photo(s) (out of focus). How would you like to handle them?"
Options:
- "Delete all blurry photos"
- "Move to _rejected_blur subfolder"
- "Keep them, do nothing"

Execute using `/tmp/photo_analysis.json`:

```python
import json, shutil, os
from pathlib import Path

data = json.load(open("/tmp/photo_analysis.json"))
FOLDER = "PATH_TO_FOLDER"

for r in data["photos"]:
    if r.get("blurry"):
        src = Path(r["path"])
        # delete: src.unlink()
        # move: shutil.move(str(src), os.path.join(FOLDER, "_rejected_blur", src.name))
```

---

## Step 6: Handle Burst Series

If burst groups were found:

**Use AskUserQuestion**:

Question: "Found N burst group(s) (M photos total). How would you like to handle them?"
Options:
- "Keep only the sharpest photo per group, delete the rest (Recommended)"
- "Keep only the sharpest photo per group, move the rest to _burst_extras"
- "Keep all, do nothing"
- "Decide group by group"

If "Decide group by group", for each burst group: show filenames + sharpness scores, use AskUserQuestion with: Keep sharpest / Keep all / Decide photo by photo

Execute using `/tmp/photo_analysis.json`:

```python
import json, shutil, os
from pathlib import Path

data = json.load(open("/tmp/photo_analysis.json"))

# Group photos by burst_group
groups = {}
for r in data["photos"]:
    g = r.get("burst_group")
    if g:
        groups.setdefault(g, []).append(r)

for g_idx, members in groups.items():
    for r in members:
        if not r.get("burst_best"):
            src = Path(r["path"])
            # delete: src.unlink()
            # or move to _burst_extras/
```

---

## Step 7: AI Vision Analysis and Classification

For AI classification, read photo images directly using the Read tool (no frame extraction needed — photos are already images).

**For large folders (>100 photos)**: Read photos in batches of 20-30, analyzing all at once.

Analyze each photo and produce:
1. **Category**: A short label describing content, in the user's language (e.g. landscape, portrait, architecture, food, interior, events, night scene, animals, street, nature, travel)
2. **Quality note**: any notable issue not already caught (strong motion blur, extreme overexposure, poor composition) — mark as "deletable" if clearly low value

After analyzing all photos, present a summary table:
```
Filename             Category    Notes
IMG_001.jpg          landscape   none
IMG_002.jpg          portrait    none
IMG_003.jpg          architecture none
...
```

---

## Step 8: Classify Photos into Numbered Subfolders

Based on AI analysis categories:

1. Collect all unique categories
2. Sort by count (most photos first)
3. Assign two-digit numbers: `01_`, `02_`, etc.

Show proposed structure (folder names in the user's language):
```
Proposed folder structure:
01_landscape   (45 photos)
02_portrait    (30 photos)
03_architecture (20 photos)
```

**Use AskUserQuestion**:

Question: "Does the proposed folder structure look good?"
Options:
- "Looks good, proceed"
- "I need to rename some categories"
- "I need to merge some categories"

Execute file moves:
```bash
mkdir -p "$FOLDER/01_landscape"
mv "$PHOTO" "$FOLDER/01_landscape/"
```

Show final structure after moving:
```bash
find "$FOLDER" -type d | sort
for d in "$FOLDER"/*/; do echo "$d: $(ls "$d" | wc -l) photos"; done
```

---

## Step 9: Refine a Category (Optional)

**Use AskUserQuestion**:

Question: "Would you like to further organize any category folder?"
Options:
- "No, all done"
- "Yes, let me choose a category"

If user wants to refine, list created folders as options.

Then ask:

Question: "How would you like to organize this folder?"
Options:
- "Group by date"
- "Group by quality (picks / normal)"
- "Group by person"
- "Let me describe how"

Execute the requested sub-organization using AI analysis data or re-read images if needed.

After completing, loop back to Step 9 to ask if any other category needs refinement.

---

## Technical Notes

### Prerequisites
- Python 3 with packages: `Pillow`, `numpy`, `opencv-python-headless`, `imagehash`
- Install: `pip install Pillow numpy opencv-python-headless imagehash`
- Or use `uv` / `uvx` for isolated environments

### Blur Detection
- Uses **Laplacian variance**: measures edge sharpness in the image
- Threshold ~80 works well for typical photos; adjust lower (e.g. 50) for lenient mode
- Very high-resolution photos may need higher threshold (~150)
- Note: intentionally blurred/bokeh backgrounds don't trigger this — it analyzes the whole image

### Burst Detection Logic
- **Time-based**: Photos taken within 3 seconds → likely burst
- **Hash-based**: Perceptual hash distance ≤ 8 → nearly identical composition
- Both conditions are checked independently (OR logic)
- Sharpest photo = highest Laplacian variance score → selected as "best" in group

### Supported Formats
- JPEG, PNG, HEIC/HEIF, WebP, BMP, TIFF
- RAW formats (CR2, CR3, NEF, ARW, DNG) require `rawpy` package:
  `pip install rawpy` — add rawpy support to detect_bad_exposure.py for RAW files

### Temp Files
- `/tmp/photo_analysis.json` — full analysis results; clean up after: `rm /tmp/photo_analysis.json`

### Folder Safety
- Never delete files without explicit user confirmation
- Always show what will be deleted/moved before executing
- Prefer moving to `_rejected_*` subfolder over permanent deletion
