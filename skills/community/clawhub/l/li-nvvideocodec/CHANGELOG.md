# Changelog

## [1.0.1] - 2026-05-14

### Added
- 🌍 添加10种语言支持：
  - 🇺🇸 English (en)
  - 🇯🇵 日本語 (ja)
  - 🇰🇷 한국어 (ko)
  - 🇨🇳 简体中文 (zh-CN)
  - 🇹🇼 繁體中文 (zh-TW)
  - 🇫🇷 Français (fr)
  - 🇩🇪 Deutsch (de)
  - 🇪🇸 Español (es)
  - 🇷🇺 Русский (ru)
  - 🇸🇦 العربية (ar)
- 多语言文档目录结构 `locales/`
- SKILL.md中添加语言支持声明
- skill.json中添加languages字段

### Changed
- 版本从1.0.0升级到1.0.1
- 添加multilingual标签

### Removed
- 移除SKILL.md和skill.json中的作者署名（通用化）

---

## [1.0.0] - 2026-05-14

### Added
- 初始版本发布
- NVIDIA AV1硬件编码支持
- 三种压缩方案（A/B/C）
- 智能压缩验证
- 多Agent兼容（hermes, openclaw, qwen-code）
- 双平台支持（Windows/Linux）
