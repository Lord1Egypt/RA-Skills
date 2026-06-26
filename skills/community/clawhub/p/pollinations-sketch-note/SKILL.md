# Pollinations Sketch Note Skill

**Name**: pollinations-sketch-note  
**Version**: 0.0.1  
**Author**: 锦鲤  
**License**: MIT

## Description

AI-powered sketch note generator that creates hand-drawn style knowledge cards with auto-search and summary.

AI 手绘知识卡片生成器，自动搜索主题并总结，生成手绘风格知识卡片。

## Features

- Auto-search from Wikipedia and Baidu Baike
- AI summary to 180-200 characters
- 3 artistic styles (Minimalist/Cute/Cyberpunk)
- Standard 804×440 output
- Auto signature and timestamp

## Requirements

- Python 3.10+
- requests
- pillow>=10.0.0
- Environment variables: POLLINATIONS_API_KEY, TAVILY_API_KEY

## Usage

```bash
python3 generate.py --theme "主题名"
```

## Documentation

See README.md and INTRO.md for full usage guide.
