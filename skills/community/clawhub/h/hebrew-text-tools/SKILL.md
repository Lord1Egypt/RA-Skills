---
name: hebrew-text-tools
slug: jewish-hebrew-tools
version: 1.0.0
description: |
  Hebrew text processing utilities: transliteration, gematria calculation,
  nikud removal, letter identification, and Hebrew number formatting.
  Pure Python, no dependencies. Works offline.
  Use when: user needs to transliterate Hebrew, calculate gematria,
  remove vowel points, or work with Hebrew letters.
triggers:
  - transliterate hebrew
  - gematria
  - hebrew letters
  - remove nikud
  - hebrew text
  - hebrew number
metadata:
  openclaw:
    emoji: א
---

# Hebrew Text Tools

Pure Python utilities for Hebrew text processing. No dependencies, works offline.

## Quick Start

```bash
# Transliterate Hebrew to Latin
hebrew-tools "שלום עולם"
# Output: shalom olam

# Calculate gematria
hebrew-tools -g "בראשית"
# Output: 913

# Remove nikud (vowel points)
echo "שָׁלוֹם" | hebrew-tools -n
# Output: שלום

# List letter names
hebrew-tools -l "אבג"
# Output: Alef, Bet, Gimel

# Format number as Hebrew letters
hebrew-tools -N 613
# Output: תרי"ג
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `hebrew-tools <text>` | All transformations | `hebrew-tools "שלום"` |
| `hebrew-tools -t <text>` | Transliterate only | `hebrew-tools -t "תורה"` → "torah" |
| `hebrew-tools -g <text>` | Gematria only | `hebrew-tools -g "חי"` → 18 |
| `hebrew-tools -n <text>` | Remove nikud | `hebrew-tools -n "בְּרֵאשִׁית"` → "בראשית" |
| `hebrew-tools -l <text>` | Letter names | `hebrew-tools -l "אב"` → [Alef, Bet] |
| `hebrew-tools -r <text>` | Reverse RTL | `hebrew-tools -r "שלום"` → "מולש" |
| `hebrew-tools -N <num>` | Number to letters | `hebrew-tools -N 26` → "כו" |

## Output Format (Default)

```
original: שלום
has_hebrew: True
transliteration: shalom
no_nikud: שלום
gematria: 376
letter_names: [Shin, Lamed, Vav, Mem]
```

## Features

### Transliteration
- Ashkenazi-style pronunciation
- Handles all Hebrew letters including sofit (final forms)
- Shin/Sin distinction (dot right/left)
- Dagesh handling

### Gematria
- Standard Mispar Hechrachi values
- Supports all Hebrew letters including sofit forms
- Works with or without nikud

### Nikud Removal
- Removes all Hebrew vowel points and cantillation marks
- Preserves base letters
- Handles composite characters

### Letter Names
- Returns English names for each Hebrew letter
- Sofit forms identified (e.g., "Mem Sofit")
- Non-Hebrew characters preserved

### Hebrew Number Formatting
- Converts integers to Hebrew letters (Gematria style)
- Standard abbreviations (e.g., תרי"ג for 613)
- Range: 1–999

## Python API

```python
from scripts.hebrew_tools import transliterate, gematria, remove_nikud

# Transliterate
print(transliterate("תורה"))  # "torah"

# Gematria
print(gematria("חי"))  # 18

# Remove nikud
clean = remove_nikud("בְּרֵאשִׁית")
print(clean)  # "בראשית"
```

## Limitations

- Transliteration is Ashkenazi-style; Sephardi variants not yet supported
- Hebrew number formatting only supports 1–999
- RTL reversal is basic (word-level, not character-level for mixed text)
