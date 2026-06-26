---
name: image-highlight-cropper
description: >
  Use this skill whenever a user uploads a large image and wants to see interesting details, highlights, or close-ups cropped out of it. Trigger when users say things like "zeig mir die Details", "crop die highlights", "was sind die interessanten Stellen", "schneide Details aus", "highlight the details", "show me close-ups", or any variation of wanting to extract notable sections from an image. Especially useful for paintings, artworks, technical drawings, and detailed photographs. Always use this skill when the user uploads an image and asks about details, interesting areas, or wants crops/cutouts.
---

# Image Highlight Cropper

Extract the 5 most visually interesting detail regions from a large image, crop them as squares, display them in the chat (2 per row), and save them as downloadable files.

## Workflow

### Step 1 – Analyse the image

Look carefully at the uploaded image. Identify the **5 most interesting regions** based on:
- Visual richness: texture, fine detail, intricate patterns
- Artistic significance: focal points, expressive faces, key objects
- Contrast and color drama
- Unique or surprising elements the viewer might miss at first glance

**⚠️ Signature rule:** If a painter's signature is visible anywhere in the image, it **must always be one of the 5 highlights**. Center the crop precisely on the signature so it is fully visible and not cut off.

**⚠️ Strict 1:1 square-fit rule:** Every highlight must be a subject that naturally fills a square frame. Before selecting a region, ask: *"Does this subject fit well into a square?"*
- ✅ Good: a face, a bouquet of flowers, a single tree, a lamp post with surroundings, a signature, a wheel, a window, a doorway, a small group of figures
- ❌ Bad: a wide panoramic skyline, a long horizontal street scene, a tall thin tower spanning the full image height — these are inherently non-square and will look like an awkward strip crop
- If a subject is too wide or too tall to feel natural in a 1:1 frame, **skip it and choose something else** that genuinely fits a square
- The goal: each crop looks intentional and well-composed, as if it were a standalone photograph

For each region, record:
- A short **label** (e.g. "Gesicht links", "Goldornament", "Signatur")
- **Center point (cx, cy)** of the subject and a **half-size** (half the desired square side length)
- A one-sentence **explanation** of why this area is interesting

### Step 2 – Crop with Python (Pillow)

Use the `bash_tool` + Python to:
1. Load the image from `/mnt/user-data/uploads/<filename>`
2. For each region: use the `save_crop` helper below — it handles edge cases automatically
3. Save each crop to `/mnt/user-data/outputs/highlight_1.jpg` … `highlight_5.jpg`

**Choosing the half-size:** Claude decides per region:
- Tiny ornament or signature → half = 100–200 px
- Face or small group → half = 200–350 px
- Large scene or texture area → half = 350–600 px
- Rule of thumb: the crop should feel like a natural close-up. Always use center-based coordinates.

**Edge case — subject at image border:** If the desired crop extends beyond the image boundary, `save_crop` takes whatever image content is available and places it centered on a **white square canvas** (side = longest available side). This keeps the result square and clean with no distortion.

```python
from PIL import Image
import os

img = Image.open("/mnt/user-data/uploads/IMAGE_FILENAME")
w, h = img.size

def save_crop(img, w, h, cx, cy, half, path):
    x1 = max(0, cx - half)
    x2 = min(w, cx + half)
    y1 = max(0, cy - half)
    y2 = min(h, cy + half)
    rect_w = x2 - x1
    rect_h = y2 - y1

    crop = img.crop((x1, y1, x2, y2))

    if rect_w == rect_h:
        # Already square — save directly
        crop.save(path, quality=92)
    else:
        # Place on white square canvas, centered horizontally and vertically
        canvas_size = max(rect_w, rect_h)
        canvas = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
        paste_x = (canvas_size - rect_w) // 2
        paste_y = (canvas_size - rect_h) // 2
        canvas.paste(crop, (paste_x, paste_y))
        canvas.save(path, quality=92)

# Define crops by CENTER point (cx, cy) and half-size
crops = [
    # (label, cx, cy, half)
    ("highlight_1", cx1, cy1, half1),
    ("highlight_2", cx2, cy2, half2),
    ("highlight_3", cx3, cy3, half3),
    ("highlight_4", cx4, cy4, half4),
    ("highlight_5", cx5, cy5, half5),
]

os.makedirs("/mnt/user-data/outputs", exist_ok=True)

for label, cx, cy, half in crops:
    save_crop(img, w, h, cx, cy, half, f"/mnt/user-data/outputs/{label}.jpg")

print("Done")
```

### Step 3 – Display in chat

After saving, use `present_files` to make all 5 crops downloadable.

Then write a short markdown summary:

```
## 🎨 5 Highlights aus dem Bild

**1. [Label]** – [Erklärung warum interessant]
**2. [Label]** – ...
...
```

Show the crops 2 per row by presenting them via `present_files` and listing them clearly with their labels. Users can download each file individually.

### Step 4 – Invite feedback

Ask the user: "Soll ich andere Bereiche auswählen, oder die Größe der Crops anpassen?"

---

## Tips for choosing good crops

- **Avoid overlap** between the 5 regions as much as possible
- **Spread across the image** — don't cluster all crops in one corner
- For **paintings**: prioritize faces, hands, symbolic objects, and texture-rich backgrounds
- For **technical drawings**: prioritize labels, detail views, and complex intersections
- half-size should be roughly **10–20% of the shorter image dimension** so crops feel like genuine close-ups, not tiny stamps

---

## Error handling

- If the image cannot be opened, tell the user and ask them to re-upload
- If Pillow is not installed: `pip install Pillow --break-system-packages`
