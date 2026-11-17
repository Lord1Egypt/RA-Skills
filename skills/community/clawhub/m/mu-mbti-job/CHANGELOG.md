# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2025-08-27

### What's New

- ✨ Three depth levels: Quick (70) / Standard (93) / Pro (144) questions from a single bilingual superset
- ✨ Bilingual PDF reports (Chinese & English) for both personal and team modes
- ✨ Team analysis report: 16-type distribution, dimension heatmap, complementary pairs, collaboration advice
- ✨ Three interaction modes: Card mode, Conversational, Web mode (quiz.html with autosave & one-click copy-back)
- ✨ Triple-tier PDF engine fallback: weasyprint → Chrome/Edge headless → reportlab
- ✨ Clarity index and Top-3 similar types based on Manhattan distance

### Technical Highlights

- Pure Python standard library core, zero dependencies for scoring and quiz generation
- Offline-first: answers never leave the device
- Form M structure for the 93-question standard version
- Automatic progress restoration in web quiz mode

### Full Changelog

https://github.com/muippt/mu-mbti-job/commits/v1.1.1
