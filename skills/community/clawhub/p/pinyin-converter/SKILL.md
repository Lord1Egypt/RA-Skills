---
name: Pinyin Converter
description: "Convert Chinese text to Pinyin (拼音). 中文转拼音工具，支持声调标记、去声调、首字母大写。适合语言学习、输入法开发、中文处理。Chinese to Pinyin converter with tone marks."
tags: pinyin, chinese, converter, tone, language, 拼音, mandarin, utility, tool
---

# Pinyin Converter 🔤

中文转拼音工具。

## Features | 功能

- **标准拼音**：带声调标记
- **无声音调**：纯字母拼音
- **首字母**：仅保留首字母缩写

## Usage | 使用

```bash
# 标准拼音（带声调）
python3 scripts/pinyin.py "你好世界"
# nǐ hǎo shì jiè

# 无声音调
python3 scripts/pinyin.py "你好世界" --no-tone
# ni hao shi jie

# 首字母
python3 scripts/pinyin.py "你好世界" --initial
# NHSJ
```

---

*免责声明：本工具仅供学习参考，不构成任何投资或商业建议。*
