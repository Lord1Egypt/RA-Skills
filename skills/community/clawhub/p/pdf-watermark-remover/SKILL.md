---
name: pdf-watermark-remover
description: >
  Remove image-based watermarks from PDF files (e.g. "Made with Gamma", Canva, Notion watermarks).
  This skill should be used when the user wants to remove watermarks from a PDF, delete PDF watermarks,
  clean up PDF watermark text or images, or says "去水印", "remove watermark", "去掉水印",
  "去PDF水印", "delete watermark", "消除水印", "水印去除". Works by deleting drawing instructions
  from content streams and removing XObject references — no color overlay, no image replacement,
  clean removal with no visual artifacts.
---

# PDF Watermark Remover

Remove image-based watermarks from PDF files by surgically deleting the drawing instructions from
content streams and removing XObject resource references. This produces clean results with no
visible artifacts (no white/black rectangles, no color mismatches).

## When to Use

- User wants to remove a watermark from a PDF
- User says "去水印", "remove watermark", "去掉水印", "去PDF水印"
- PDF has a "Made with Gamma", Canva, or similar branded watermark
- PDF has an image-based watermark in a corner or specific position

## How It Works

The removal process targets the **root cause** — the PDF content stream instructions that draw the
watermark image — rather than covering or replacing the image:

1. **Detect**: Scan each page for images matching watermark characteristics (position + size)
2. **Map**: Build XObject name-to-xref mapping from the page's resource dictionary
3. **Remove from content stream**: Delete the `q...cm.../Name Do...Q` drawing instruction
4. **Remove from resources**: Delete the watermark entry from the XObject dictionary
5. **Save** with garbage collection to clean up orphaned objects

This approach leaves **zero visual artifacts** because the watermark simply never gets drawn.

## Workflow

### Step 1: Analyze the Watermark

Before running the script, determine the watermark's characteristics:

1. Open the PDF and identify the watermark visually
2. Note its **position** (typically bottom-right corner) and **approximate size**
3. If it's a link (clickable), note the **domain** (e.g. `gamma.app`)

### Step 2: Run the Removal Script

Execute `scripts/remove_watermark.py`:

```bash
python scripts/remove_watermark.py <input.pdf> <output.pdf> [options]
```

**Common options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--x-threshold` | 700 | X position threshold — images with x0 > this value are candidates |
| `--min-w` / `--max-w` | 100 / 200 | Width range for watermark detection |
| `--min-h` / `--max-h` | 20 / 50 | Height range for watermark detection |
| `--remove-links` | off | Also remove link annotations |
| `--link-domain` | all | Only remove links containing this domain |

**Gamma watermark example:**
```bash
python scripts/remove_watermark.py input.pdf output.pdf --remove-links --link-domain gamma.app
```

**Custom position watermark (e.g. top-left):**
```bash
python scripts/remove_watermark.py input.pdf output.pdf --x-threshold 0 --min-w 50 --max-w 300 --min-h 10 --max-h 80
```

### Step 3: Verify

Open the output PDF and check:
- Watermark is completely gone (no visual remnants)
- No color patches, rectangles, or artifacts in the watermark area
- Page content is otherwise intact

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Watermark still visible | Position/size doesn't match detection thresholds | Adjust `--x-threshold`, `--min-w/max-w`, `--min-h/max-h` |
- Watermark still visible after adjustment | Watermark may be text-based, not image-based | This skill only handles image watermarks; for text watermarks, use redaction or content stream editing |
| Other images accidentally removed | Detection thresholds too broad | Narrow the width/height/position ranges |
| Black/white rectangle appears | Old approach used image replacement instead of content stream deletion | This skill uses content stream deletion — this should not happen |

## Key Technical Insight

**Why not overlay/replace?** Three approaches that DON'T work well:
1. **White rectangle overlay** — Visible on non-white backgrounds, misses rounded corners
2. **Image data replacement with 1x1 pixel** — PDF renders the 1x1 pixel scaled up as a colored rectangle (black for transparent, white for white pixel)
3. **`delete_image` API** — Only clears image data, doesn't remove the XObject reference or content stream Do instruction; renders as blank/colored rectangle

**The correct approach** (used by this skill): Delete the `Do` instruction from the content stream
and the `/Name xref R` entry from the XObject dictionary. The watermark image data becomes an
orphaned object that gets garbage-collected on save.

## Requirements

- Python 3.8+
- pymupdf (`pip install pymupdf`)
