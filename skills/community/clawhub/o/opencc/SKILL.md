---
name: opencc
description: Chinese character conversion between Simplified/Traditional and regional variants. Use when Pi needs to convert Chinese text with precision and awareness of regional differences (Mainland China, Taiwan, Hong Kong, Japanese Kanji). Supports phrase-level conversion, character variants, and regional idioms. Helps generate more accurate Chinese in multilingual contexts.
---

# OpenCC Skill for OpenClaw

Convert Chinese text with precision using OpenCC (Open Chinese Convert).

## Quick Start

### Basic Conversions

```python
import opencc

# Simplified → Traditional
converter = opencc.OpenCC('s2t.json')
result = converter.convert('汉字')  # → 漢字

# Traditional → Simplified  
converter = opencc.OpenCC('t2s.json')
result = converter.convert('漢字')  # → 汉字

# Simplified → Taiwan Standard (正體)
converter = opencc.OpenCC('s2tw.json')
result = converter.convert('软件')  # → 軟體

# Simplified → Hong Kong variant (繁體)
converter = opencc.OpenCC('s2hk.json')
result = converter.convert('软件')  # → 軟件
```

## Conversion Modes

| Config | Source | Target | Use Case |
|--------|--------|--------|----------|
| `s2t.json` | Simplified | Traditional (OpenCC) | Generic traditional conversion |
| `t2s.json` | Traditional | Simplified | Generic simplified conversion |
| `s2tw.json` | Simplified | Taiwan Standard (正體) | Taiwan-specific terminology |
| `tw2s.json` | Taiwan Standard | Simplified | Taiwan to Mainland |
| `s2hk.json` | Simplified | Hong Kong (繁體) | Hong Kong variant |
| `hk2s.json` | Hong Kong | Simplified | Hong Kong to Mainland |
| `s2twp.json` | Simplified | Taiwan + idioms | Taiwan terminology + common phrases |
| `tw2sp.json` | Taiwan | Simplified + idioms | Taiwan to Mainland with idioms |
| `t2tw.json` | Traditional | Taiwan Standard | Standardize to Taiwan |
| `t2hk.json` | Traditional | Hong Kong | Standardize to Hong Kong |
| `hk2t.json` | Hong Kong | Traditional | Hong Kong to OpenCC standard |
| `t2jp.json` | Traditional | Japanese Kanji (Shinjitai) | Convert to modern Japanese |
| `jp2t.json` | Japanese | Traditional Chinese | Japanese to traditional Chinese |
| `tw2t.json` | Taiwan Standard | Traditional | Taiwan to OpenCC standard |

## Use Cases

### When to Use OpenCC

1. **Blog writing with regional awareness** — Ensure blog uses consistent Taiwan/Mainland terminology
2. **Content localization** — Convert content for different Chinese-speaking regions
3. **Character normalization** — Standardize variant characters (e.g., 裏 vs 裡)
4. **Multi-script content** — Convert between Chinese and Japanese Kanji as needed

### Region-Specific Guidance

- **Mainland China**: Use `s2t` for traditional, `t2s` for simplified
- **Taiwan (正體)**: Use `s2tw` for precise Taiwan terminology, `s2twp` for common phrases
- **Hong Kong**: Use `s2hk` for Hong Kong variant
- **Japan**: Use `t2jp` for modern Japanese Kanji

## CLI Usage

Use the included `convert.py` script:

```bash
# Command line conversion
python scripts/convert.py --source s2t "汉字转换"

# With stdin
echo "汉字转换" | python scripts/convert.py --source s2t

# Save to file
python scripts/convert.py --source s2t --input input.txt --output output.txt
```

## Installation

```bash
# Using uv (recommended)
uv add opencc

# Or with pip
pip install opencc
```

## API Reference

See [references/opencc_guide.md](references/opencc_guide.md) for:
- Detailed conversion mode descriptions
- Common conversion patterns
- Performance considerations
- Troubleshooting

## Characteristics

- **Character-level conversion**: Precise character-by-character transformation
- **Phrase-level conversion**: Smart phrase detection for accurate multi-character terms
- **Variant handling**: Distinguishes between character variants (e.g., 裏/裡)
- **Regional awareness**: Customized rules for Mainland, Taiwan, Hong Kong, Japan
- **No linguistic translation**: Converts writing system only, not meaning

## Limitations

- **Not a translator**: Converts writing systems, not languages. Cannot convert between Cantonese/Mandarin or other dialects.
- **Phrase-based**: Some contexts may require manual review (e.g., proper nouns, technical terms)
- **Regional boundaries**: Different regions have different standards; always verify output matches your target

## Files

- `scripts/convert.py` — Python CLI wrapper
- `references/opencc_guide.md` — Detailed mode reference
- `pyproject.toml` — Python project configuration with uv
