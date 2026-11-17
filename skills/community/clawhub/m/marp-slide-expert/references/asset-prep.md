# Image Asset Preparation

When converting a deck with external image URLs (courseware screenshots, blog diagrams, scraped visuals), download and prep them before generating slides.

## Naming convention

Always rename downloaded images with a **chapter / section prefix** so the paths stay stable and meaningful:

```text
L1_1.1-01_section-overview.png    ← lesson 1, section 1.1, item 01
L3_3.6-30_workbench-walkthrough.png ← lesson 3, section 3.6, item 30
```

Format: `L<lesson>_<section>_<sequence>_<descriptive name>.<ext>`

This avoids:
- URL-encoded filenames that read poorly, and non-Latin names that render inconsistently across machines.
- Collisions when the same section number appears in multiple lessons.
- Path-unsafe characters like `/` in section names.

## Download

Use parallel downloads with `xargs -P` or `curl &` in a shell loop. Typical pattern:

```bash
# Split URL list into chunks to avoid "command line too long"
split -l 20 urls.txt chunk_
ls chunk_* | xargs -P 8 -I {} sh -c '
  while IFS="|" read -r url name; do
    [ -f "assests/$name" ] || curl -sS -o "assests/$name" "$url"
  done < {}
'
```

For URLs with non-ASCII characters, use Python + `unquote()` from `urllib.parse` to normalize filenames.

## Compression

Target ≤ 100 KB per image. Pillow works on macOS without extra deps:

```python
from pathlib import Path
from PIL import Image

def compress(path: Path, max_kb: int = 100):
    img = Image.open(path)
    if img.mode == 'RGBA':
        # Convert RGBA to RGB on white for diagrams
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # First: PNG optimize
    img.save(path, 'PNG', optimize=True)
    if path.stat().st_size / 1024 > max_kb:
        # Resize down
        w, h = img.size
        for scale in [0.85, 0.7, 0.55]:
            new_w, new_h = int(w * scale), int(h * scale)
            img2 = img.resize((new_w, new_h), Image.LANCZOS)
            img2.save(path, 'PNG', optimize=True)
            if path.stat().st_size / 1024 <= max_kb:
                break
        # If still too big, convert to JPEG with new extension
        if path.stat().st_size / 1024 > max_kb:
            new_path = path.with_suffix('.jpg')
            img.save(new_path, 'JPEG', quality=82, optimize=True, progressive=True)
            if new_path.stat().st_size / 1024 <= max_kb:
                path.unlink()  # remove original PNG
                return new_path.name
    return path.name
```

Key points:
- **Line art / simple diagrams** → keep as PNG (lossless).
- **Photographs / complex multi-color diagrams** → convert to JPEG q=82, rename to `.jpg`.
- **RGBA / transparency** → either flatten on white (for diagrams) or keep as PNG with `optimize=True`.

## Path resolution from marp

Marp resolves relative image paths from the **markdown file's directory**, not from the current working directory. This bites when:

- The .md file is at `path/to/deck.marp.md`
- The image path in markdown is `images/foo.png`
- Marp looks at `path/to/images/foo.png`

If your assets live elsewhere, either:

1. Move the .md file to a location where the relative path resolves, OR
2. Use paths relative to the .md file's directory, OR
3. Use absolute paths (works but not portable).

A common pattern: keep `.marp.md` files and `assests/` side-by-side, and reference with `![bg](<assests/L1_xxx.png>)`.

For images that need to render in PDF when invoked from a parent directory, wrap paths in `<...>` brackets:

```markdown
![bg left contain opacity:.9](<course/Harness Engineering/assests/L1_xxx.png>)
```

The brackets tell marp the entire content (including spaces) is one URL.
