# OpenCC Skill for OpenClaw

Convert Chinese text between Simplified/Traditional and regional variants using OpenCC.

> **What is OpenCC?** Open Chinese Convert (開放中文轉換) is a comprehensive library for converting between Traditional Chinese, Simplified Chinese, and Japanese Kanji, with support for regional variants (Mainland, Taiwan, Hong Kong).

## Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/kai-tw/openclaw-opencc-skill.git
cd openclaw-opencc-skill

# Install dependencies with uv
uv sync

# Verify installation
uv run python scripts/convert.py --source s2t "汉字"
# Output: 漢字
```

### Basic Usage

**Command line:**

```bash
# Simplified to Traditional
uv run python scripts/convert.py --source s2t "汉字"

# Simplified to Taiwan Standard (with idioms)
uv run python scripts/convert.py --source s2twp "鼠标和软件"
# Output: 滑鼠和軟體

# From stdin
echo "简体中文" | uv run python scripts/convert.py --source s2tw
```

**Python code:**

```python
import opencc

# Create converter
converter = opencc.OpenCC('s2tw.json')

# Convert text
result = converter.convert('软件')  # → 軟體
print(result)
```

## Conversion Modes

### Basic (Universal Traditional/Simplified)

- `s2t.json` — Simplified → Traditional
- `t2s.json` — Traditional → Simplified

### Taiwan Standard (正體)

- `s2tw.json` — Simplified → Taiwan
- `s2twp.json` — Simplified → Taiwan + Mainland idioms
- `tw2s.json` — Taiwan → Simplified
- `t2tw.json` — Traditional → Taiwan

### Hong Kong Variant

- `s2hk.json` — Simplified → Hong Kong
- `hk2s.json` — Hong Kong → Simplified
- `t2hk.json` — Traditional → Hong Kong
- `hk2t.json` — Hong Kong → Traditional

### Japanese Kanji

- `t2jp.json` — Traditional → Japanese Kanji
- `jp2t.json` — Japanese → Traditional

## Use Cases

### Blog Localization (Taiwan)

```python
import opencc

content = "本文介绍如何使用鼠标安装软件"
converter = opencc.OpenCC('s2twp.json')  # Use phrase-aware mode
result = converter.convert(content)
# Output: 本文介紹如何使用滑鼠安裝軟體
```

### Multi-Region Content

```python
# Convert for different regions
text = "软件和硬件"

for mode, region in [('s2tw', 'Taiwan'), ('s2hk', 'Hong Kong'), ('s2t', 'Traditional')]:
    converter = opencc.OpenCC(f'{mode}.json')
    print(f"{region}: {converter.convert(text)}")
```

### Normalize Variant Characters

```python
# Handle variant forms (e.g., 裏 vs 裡)
converter = opencc.OpenCC('s2tw.json')
standard = converter.convert("里面")  # → 裡面
```

## Testing

```bash
# Run tests with uv
uv run pytest test_convert.py -v

# Or directly
uv run python test_convert.py
```

## Key Features

✅ **14 conversion modes** for comprehensive Chinese text handling  
✅ **Phrase-level conversion** for accurate idiom handling  
✅ **Regional awareness** — Taiwan (正體), Hong Kong, Mainland, Japan  
✅ **Character variants** — Distinguishes 裏/裡, and more  
✅ **Fast** — ~1ms per string after initialization  
✅ **Reliable** — Used in major Chinese input methods (iBus, Fcitx, RIME)  

## CLI Tool

The included `scripts/convert.py` provides a command-line interface:

```bash
usage: convert.py [-h] -s SOURCE [-i INPUT] [-o OUTPUT] [text]

Convert Chinese text using OpenCC

positional arguments:
  text                  Text to convert (or read from stdin)

options:
  -s, --source SOURCE   Conversion mode (e.g., s2t, t2s, s2tw)
  -i, --input INPUT     Input file path
  -o, --output OUTPUT   Output file path (default: stdout)

Examples:
  python scripts/convert.py --source s2t "汉字转换"
  echo "简体中文" | python scripts/convert.py --source s2tw
  python scripts/convert.py --source s2t --input input.txt --output output.txt
```

## Configuration

Default project structure:
```
openclaw-opencc-skill/
├── SKILL.md                    # Skill definition for OpenClaw
├── scripts/convert.py          # CLI converter tool
├── references/opencc_guide.md  # Detailed mode reference
├── test_convert.py             # Test suite
├── pyproject.toml              # uv project config
└── README.md
```

## For OpenClaw Usage

This skill integrates with OpenClaw to help Pi generate more precise Chinese:

1. **Install the skill**: Copy to your OpenClaw skills directory or use clawhub
2. **Trigger automatically**: OpenClaw recognizes Chinese conversion requests
3. **Use in workflows**: Convert blog content, localize documentation, standardize regional variants

See `SKILL.md` for OpenClaw integration details.

## Performance

- **Initialization**: ~20-25ms (first time, loads dictionary)
- **Conversion**: ~1-10ms per string (depends on length)
- **Memory**: ~50MB (dictionary loaded once)

For batch processing, reuse converter instances:

```python
converter = opencc.OpenCC('s2tw.json')
for text in large_batch:
    result = converter.convert(text)  # Fast (reuses loaded dict)
```

## Limitations

- **Not a translator**: Converts writing systems only, not languages
- **Phrase context**: Some idioms may require manual review
- **Proper nouns**: Names may convert unexpectedly; verify output

## References

- **OpenCC GitHub**: https://github.com/BYVoid/OpenCC
- **OpenCC Docs**: https://byvoid.github.io/OpenCC/
- **Detailed Guide**: See `references/opencc_guide.md` in this repo

## License

Apache License 2.0 — Same as OpenCC

## Contributing

Contributions welcome! File issues or PRs for:
- New conversion modes or features
- Performance improvements
- Better documentation
- Bug fixes

---

Built with ❤️ for OpenClaw and precise Chinese text processing.
