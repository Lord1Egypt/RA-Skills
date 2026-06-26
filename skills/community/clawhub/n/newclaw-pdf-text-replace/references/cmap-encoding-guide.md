# PDF Font CMap Encoding Guide

## Why PDF Text Replacement Is Hard

PDFs don't store text as readable strings. Instead, they use a multi-layer encoding:

```
Visible Text: "2025"
    ↓ (font CMap)
Byte Codes: 0x22 0x25 0x22 0x24
    ↓ (glyph table)
Font Glyphs: [outline data for each shape]
    ↓ (renderer)
Pixels on screen
```

Each PDF embeds **font subsets** — minimal fonts containing only the characters used in the document. A font subset for a certificate might only have: digits 0-9, a few CJK characters, and punctuation.

## Understanding ToUnicode CMap

Every embedded font has a `ToUnicode` CMap that maps byte codes back to Unicode (for text extraction/search). Format:

```
beginbfrange
<22><22><0032>   ← byte 0x22 → Unicode U+0032 = '2'
<23><23><002E>   ← byte 0x23 → Unicode U+002E = '.'
<24><24><0035>   ← byte 0x24 → Unicode U+0035 = '5'
<25><25><0030>   ← byte 0x25 → Unicode U+0030 = '0'
endbfrange
```

So the string "2025" is encoded as bytes `0x22, 0x25, 0x22, 0x24`.

## Content Stream Text Operations

PDF content streams use PostScript-like operators:

```
q 1 0 0 1 188.673 236.763 cm    % Set coordinate transform (translate)
BT                                % Begin text
  0.0003 Tc                      % Character spacing
  18 0 0 18 90 0 Tm              % Text matrix: 18pt font, at x=90 y=0
  /TT4 1 Tf                      % Select font TT4
  ("%"$) Tj                      % Draw string (encoded bytes)
ET                                % End text
Q                                 % Restore graphics state
```

## Position Calculation

To place a replacement character at the correct position:

```python
# Character advance = glyph_width / unitsPerEm * fontSize + charSpacing
advance = 1213 / 2048 * 18 + 0.0003  # ≈ 10.66 points

# Position after N characters
x_position = tm_x + N * advance
```

## Why fontTools Re-embedding Fails

When you modify an embedded font subset with fontTools and re-embed:
1. Table checksums change
2. `loca` table offsets shift
3. Some PDF viewers cache font data by object ID
4. The `hmtx`, `maxp`, `glyf` tables must be perfectly synchronized

Result: garbled or invisible text in most viewers. The safe approach is to add a **new** font resource.

## The New Font Overlay Technique

Instead of modifying the existing font:
1. Create a minimal subset of a system font with only the needed characters
2. Add it as a separate font resource (`/TT9`)
3. Split the original text operation at the replacement point
4. Draw the replacement character(s) using the new font at the calculated position

This preserves the original font completely and works reliably across all PDF viewers.
