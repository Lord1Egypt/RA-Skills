# Arabic OCR Cleanup — Reusable Script

Use after `marker_single` output on Arabic/Persian scanned PDFs.
Saves a cleaned version with `-cleaned.md` suffix.

## Usage

```bash
python3 arabic-ocr-cleanup.py /path/to/marker-output.md
```

## Script

Save this as a standalone file (`~/.hermes/scripts/cleanup-arabic-ocr.py`) for reuse:

```python
#!/usr/bin/env python3
"""
Clean Marker-pdf Arabic OCR output:
  - Preserve page markers {N}---- and table separators |---|---|
  - Remove pure English garbage lines (repeated "ASS NO", "second second", etc.)
  - Truncate Arabic repetition tails (same word repeated 5+ times at end of line)
  - Remove pure-garbage lines (repeated Arabic word filling entire line)
"""
import re, sys

def cleanup(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    removed_count = 0
    truncated_count = 0

    for i, line in enumerate(lines):
        lineno = i + 1
        stripped = line.strip()
        if not stripped:
            new_lines.append(line)
            continue

        # --- PRESERVE structural markers ---
        # Page markers: {N}----------------
        if re.match(r'^\{?\d*\}?[-—]{10,}', stripped) and any(c.isdigit() for c in stripped[:10]):
            new_lines.append(line)
            continue
        # Table separators: |---|---|---|
        if re.match(r'^[\|\s\-]+$', stripped) and '|' in stripped:
            new_lines.append(line)
            continue

        arabic_chars = sum(1 for c in stripped if '\u0600' <= c <= '\u06FF')

        # --- REMOVE English-only garbage ---
        if arabic_chars == 0 and len(stripped) > 20:
            garbage_signals = ['ASS NO', 'SECOND SECOND', 'STATE OF THE STATE']
            if any(s in stripped.upper() for s in garbage_signals) \
               and sum(stripped.upper().count(w) for w in ['ASS', 'SECOND', 'STATE']) >= 5:
                removed_count += 1
                print(f"REMOVED L{lineno}: {stripped[:60]}...")
                continue

        # --- REMOVE line-wide Arabic repetition (same word 8+ times) ---
        words = [w for w in stripped.split() if len(w) >= 3 and re.match(r'[\w\u0600-\u06FF\u064B-\u0652]+', w)]
        word_counts = {}
        for w in words:
            word_counts[w] = word_counts.get(w, 0) + 1
        if any(c >= 8 for c in word_counts.values()) and arabic_chars > 0:
            removed_count += 1
            print(f"REMOVED L{lineno}: {stripped[:60]}...")
            continue

        # --- TRUNCATE repetition tails ---
        # Same word repeated 4+ times consecutively at end of line
        tail_patterns = [
            (r'((الله\s+الله\s+الله\s+الله[\s\S]*)$)', False),
            (r'((المسافرة\s+المسافرة[\s\S]*)$)', False),
            (r'((المالية\s+المالية[\s\S]*)$)', False),
            (r'((المامات\s+المامات[\s\S]*)$)', False),
            (r'((second\s+second[\s\S]*)$)', True),
            (r'((THE STATE[\s\S]*)$)', True),
        ]
        truncated = False
        for pattern, case_insensitive in tail_patterns:
            flags = re.IGNORECASE if case_insensitive else 0
            m = re.search(pattern, stripped, flags)
            if m and m.start(1) > 5:  # only if there's content before the garbage
                stripped = stripped[:m.start(1)].rstrip('و﴿﴾﴿• ﴾· ')
                truncated = True
                truncated_count += 1
                print(f"TRUNCATED L{lineno}")
                break

        new_lines.append(stripped + '\n')

    out_path = md_path.replace('.md', '-cleaned.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"\nDone: {len(lines)} → {len(new_lines)} lines, {removed_count} removed, {truncated_count} truncated")
    print(f"Output: {out_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <marker-pdf-output.md>")
        sys.exit(1)
    cleanup(sys.argv[1])
```

## Common Garbage Patterns

| Pattern | Source | Fix |
|---------|--------|-----|
| "المسافرة / الله / المالية" × 40 | OCR confuses end of a page with repeated header/footer text | Truncate |
| "ASS NO. 10. ASS NO. 10." × 20 | Table cell with "Assignment No." corrupted | Remove line |
| "second second second..." or "STATE OF THE STATE..." | Corrupted English table cell | Remove line |
| "اللَّهُ اللَّهُ..." with diacritics | Page footer/header bled into text | Truncate |
| Half-page of whitespace with one word | Table format exploded | Usually OK to leave |

## Quality Expectations

| Document Type | Expected Readable % | Issues |
|--------------|---------------------|--------|
| Standard Arabic text (14pt+) | 90-95% | Minor letter subs: ب↔ج, ت↔ث |
| Small font / footnotes | 60-75% | More noise, fine-print mangling |
| Tables with mixed text/numbers | 70-85% | Cell alignment issues, number confusion |
| Diagrams / figures with text | 40-60% | Minimal — use extracted JPEG instead |
