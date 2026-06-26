# OpenCC Conversion Modes - Complete Reference

## Overview

OpenCC supports 14 distinct conversion modes, organized by source/target language and regional variant. Each mode is a `.json` configuration file that defines character mappings and phrase-level conversion rules.

## All Conversion Modes

### Basic Conversions

#### `s2t.json` - Simplified to Traditional
- **Source**: Simplified Chinese (Mainland style)
- **Target**: Traditional Chinese (OpenCC Standard)
- **Use**: Generic simplified-to-traditional conversion
- **Example**: 软件 → 軟件

#### `t2s.json` - Traditional to Simplified
- **Source**: Traditional Chinese
- **Target**: Simplified Chinese
- **Use**: Converting traditional back to simplified
- **Example**: 軟件 → 软件

### Regional Variants (Taiwan - 正體)

Taiwan uses a specific standard called "正體" (correct form) which differs from both generic Traditional Chinese and Mainland Simplified.

#### `s2tw.json` - Simplified to Taiwan Standard
- **Source**: Simplified Chinese
- **Target**: Taiwan Standard (正體)
- **Use**: Convert for Taiwan audiences
- **Key differences from s2t**: Focuses on Taiwan standard terminology
- **Example**: 软件 → 軟體 (note: 體 not 件)

#### `s2twp.json` - Simplified to Taiwan Standard + Idioms
- **Source**: Simplified Chinese
- **Target**: Taiwan Standard with common phrase conversion
- **Use**: Most comprehensive Taiwan conversion (includes idiomatic terms)
- **Features**: Phrase-level conversion for common expressions
- **Example**: 鼠标 → 滑鼠, 软件 → 軟體

#### `tw2s.json` - Taiwan Standard to Simplified
- **Source**: Taiwan Standard (正體)
- **Target**: Simplified Chinese
- **Use**: Convert Taiwan content back to Mainland standard
- **Example**: 軟體 → 软件

#### `tw2sp.json` - Taiwan to Simplified + Idioms
- **Source**: Taiwan Standard
- **Target**: Simplified with Mainland idiomatic phrases
- **Use**: Convert Taiwan content with Mainland-specific terminology
- **Example**: 滑鼠 → 鼠标

#### `t2tw.json` - Traditional to Taiwan Standard
- **Source**: Generic Traditional Chinese
- **Target**: Taiwan Standard
- **Use**: Normalize traditional text to Taiwan standard
- **Example**: Useful when converting Hong Kong text to Taiwan standard

### Hong Kong Variants

Hong Kong uses a distinct written standard that differs from Taiwan.

#### `s2hk.json` - Simplified to Hong Kong Variant
- **Source**: Simplified Chinese
- **Target**: Hong Kong variant (繁體)
- **Use**: Convert for Hong Kong audiences
- **Key features**: Hong Kong-specific characters and conventions
- **Example**: 软件 → 軟件

#### `hk2s.json` - Hong Kong to Simplified
- **Source**: Hong Kong variant
- **Target**: Simplified Chinese
- **Use**: Convert Hong Kong content back to simplified
- **Example**: 軟件 → 软件

#### `t2hk.json` - Traditional to Hong Kong
- **Source**: Generic Traditional Chinese
- **Target**: Hong Kong variant
- **Use**: Normalize traditional text to Hong Kong standard
- **Example**: Converts generic traditional to Hong Kong conventions

#### `hk2t.json` - Hong Kong to Traditional
- **Source**: Hong Kong variant
- **Target**: Generic Traditional Chinese (OpenCC Standard)
- **Use**: Convert Hong Kong text to standard traditional
- **Example**: Normalizes Hong Kong characters to OpenCC standard

### Japanese Kanji Conversion

#### `t2jp.json` - Traditional Chinese to Japanese Kanji (Shinjitai)
- **Source**: Traditional Chinese characters (Kyūjitai - old form)
- **Target**: Japanese Kanji (Shinjitai - new form)
- **Use**: Convert classical Chinese to modern Japanese writing
- **Note**: Japanese uses simplified forms (Shinjitai) different from Simplified Chinese
- **Example**: 無 → 无 (but specific to Japanese standard)

#### `jp2t.json` - Japanese Kanji to Traditional Chinese
- **Source**: Japanese Kanji (Shinjitai)
- **Target**: Traditional Chinese (Kyūjitai)
- **Use**: Convert modern Japanese text to traditional Chinese
- **Example**: Reverse of t2jp

## Choosing the Right Mode

### For Content Writers

**Writing for Mainland China?**
- Use `t2s` if converting from traditional
- Or write directly in simplified from the start

**Writing for Taiwan?**
- Use `s2tw` or `s2twp` (s2twp includes idioms like 鼠标→滑鼠)
- **Recommended**: `s2twp` for most accurate Taiwan localization

**Writing for Hong Kong?**
- Use `s2hk`
- Hong Kong and Taiwan have different standards

**Writing for Japan?**
- Use `t2jp` for literary/classical content
- Most modern Japanese is written in Japanese script (hiragana/katakana), not kanji-only

### Common Workflows

#### Mainland → Taiwan
```python
converter = opencc.OpenCC('s2tw.json')  # or s2twp.json
result = converter.convert(mainland_text)
```

#### Taiwan → Mainland
```python
converter = opencc.OpenCC('tw2s.json')  # or tw2sp.json for idioms
result = converter.convert(taiwan_text)
```

#### Generic Traditional → Taiwan Standard
```python
converter = opencc.OpenCC('t2tw.json')
result = converter.convert(traditional_text)
```

#### Mainland → Hong Kong
```python
converter = opencc.OpenCC('s2hk.json')
result = converter.convert(mainland_text)
```

## Implementation Notes

### Character-Level vs Phrase-Level

OpenCC supports two conversion strategies:

1. **Character-level**: Converts each character individually
   - Fast, predictable
   - May miss phrase-specific terminology
   - Example: 软 → 軟 (individual character)

2. **Phrase-level**: Groups characters and converts multi-character terms
   - Accurate for idioms and common phrases
   - More complex lookup
   - Example: 鼠标 → 滑鼠 (phrase-level, not just character)

Modes with phrases enabled:
- `s2twp.json` (Taiwan phrases)
- `tw2sp.json` (Mainland phrases)

### Performance

- First initialization: ~20-25ms (loading dictionary)
- Subsequent conversions: ~1-10ms per string (depends on length)
- For batch processing: Reuse same converter instance

### Variant Characters

Some characters have multiple valid forms:
- 裏 vs 裡 (inside)
- 鼠标 vs 鼠標 (mouse)

OpenCC distinguishes these carefully based on context and region.

## Common Conversion Scenarios

### 1. Blog Post Localization (Taiwan)

```python
import opencc

# Original simplified content
content = "本文介绍如何使用鼠标安装软件"

# Convert to Taiwan standard
converter = opencc.OpenCC('s2twp.json')
taiwan_version = converter.convert(content)
# Result: 本文介紹如何使用滑鼠安裝軟體
```

### 2. Normalize Variant Characters

```python
# Both 裏 and 裡 mean "inside"
converter = opencc.OpenCC('s2tw.json')
standard = converter.convert("里面")  # 裡面 (standardized)
```

### 3. Cross-Regional Text Processing

```python
# Convert Hong Kong text to Taiwan standard (via traditional)
converter_hk2t = opencc.OpenCC('hk2t.json')
converter_t2tw = opencc.OpenCC('t2tw.json')

hongkong_text = "軟件"
traditional = converter_hk2t.convert(hongkong_text)
taiwan_text = converter_t2tw.convert(traditional)
```

## Regional Differences at a Glance

| Term | Simplified | Traditional | Taiwan | Hong Kong | Meaning |
|------|-----------|-------------|--------|-----------|---------|
| 软件 | 软件 | 軟件 | 軟體 | 軟件 | Software |
| 鼠标 | 鼠标 | 鼠標 | 滑鼠 | 鼠標 | Mouse (device) |
| 硬盘 | 硬盘 | 硬盤 | 硬碟 | 硬碟 | Hard disk |
| 裏面 | 里面 | 裡面 | 裡面 | 裡面 | Inside |
| 应用 | 应用 | 應用 | 應用 | 應用 | Application |

## Troubleshooting

### Mode Not Found

If you get an error like "s2tx.json not found":
- Check spelling: modes are exact (s2t, not s2T)
- Use only documented modes (see list above)

### Unexpected Conversions

- Some proper nouns or technical terms may convert unexpectedly
- Review output carefully for names and brand terms
- Consider leaving certain terms unconverted if needed

### Performance Issues

- For large documents (>1MB), convert in chunks
- Reuse converter instances across multiple strings
- Character-level modes (s2t, t2s) are faster than phrase-based (s2twp)

## References

- OpenCC GitHub: https://github.com/BYVoid/OpenCC
- Official Documentation: https://byvoid.github.io/OpenCC/
- Telegram Discussion: https://t.me/open_chinese_convert
