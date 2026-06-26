# LocaleFlow — i18n for OpenClaw

> The first i18n post-processing layer for OpenClaw that fixes diacritics, removes stray characters, and makes your AI truly multilingual.

**Website:** https://bloommediacorporation-lab.github.io/openclaw-i18n-skill/

## What is LocaleFlow?

LocaleFlow is a two-layer internationalization system for OpenClaw:

1. **SKILL.md** — Configures your agent to think in the correct language. Auto-detection, locale-aware formatting, and cultural communication norms.
2. **Post-Processor** — Python engine that mechanically cleans every response before it reaches the user. Fixes diacritics, removes artifacts, normalizes whitespace.

## Supported Languages

| Language | Code | Status |
|----------|------|--------|
| Romanian | `ro` | Stable |
| German | `de` | Stable |
| French | `fr` | Coming v1.1 |
| Spanish | `es` | Coming v1.1 |

## Installation

### Option 1: ClawHub (recommended)
```bash
clawhub install bloommediacorporation-lab/openclaw-i18n-skill
```

### Option 2: Manual Install
```bash
git clone https://github.com/bloommediacorporation-lab/openclaw-i18n-skill.git
cd openclaw-i18n-skill/processor
pip install -r requirements.txt
```

## Usage

### Set Language
Say to your agent:
- `"Set language to Romanian"` or `"Setează limba la română"`
- `"Set language to German"` or `"Stelle Sprache auf Deutsch"`

### Reset to Auto-Detect
Say: `"Reset language to auto-detect"`

### Post-Processor (standalone)
```python
from i18n_processor import process

# Process raw model output before sending to user
cleaned = process("vreau sa ajut", language="ro")
# Output: "vreau să ajut" (diacritics fixed)
```

## Features

- **Diacritics fixing**: Romanian (ăâîșț) and German (üöäß) corrected automatically
- **Stray character removal**: Removes CJK/Cyrillic artifacts glued to Latin text
- **Whitespace normalization**: Fixes double spaces, trailing/leading spaces
- **Locale formatting**: Dates, currency, phone numbers in local formats
- **Auto-detection**: Detects language from context with 80% confidence threshold

## Testing

```bash
cd processor
python3 tests/test_processor.py
```

All 26 tests pass.

## Contributing

Contributions welcome! Please read the docs and follow the same patterns for new languages.

## License

© 2026 Bloom Media. All rights reserved.

## Authors

Built by [Bloom Media](https://bloommedia.ro)
