# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.9.5] - 2026-04-05

### Changed

- **init 流程简化**：移除 openclaw 配置文件查找逻辑，改为直接向用户获取 API Key
- 版本号统一为 `0.9.5`（SKILL.md 与 CHANGELOG.md 同步）

### Removed

- **移除 `image-01-live` 模型**：MiniMax 已停止支持 `image-01-live`，所有风格 `image-01` 均已支持
- 移除模型自动判断逻辑（`detect_model` 函数、`LIVE_STYLE_KEYWORDS`、`REALISTIC_KEYWORDS`）
- 移除 `--model` 的 `auto` / `image-01-live` 选项，固定使用 `image-01`
- 移除 `--region` 参数及 `REGION` 配置常量
- SKILL.md 移除「模型自动判断逻辑」整个章节
---

## [0.9.0] - 2026-03-26

### Added

- **模型自动判断逻辑**
  - CN 区：根据 prompt 关键词自动选择 `image-01`（写实）或 `image-01-live`（艺术风格）
  - Global 区：只用 `image-01`
  - 新增参数：`--model`、`--region`、`--api-key`、`--base-url`
  - 艺术风格关键词：手绘、卡通、漫画、动漫、油画、蜡笔、素描、水彩、国画、插画、原画 等
  - 写实关键词：写实、真实、逼真、照片、摄影、realistic、photorealistic 等
- **参考图 URL 处理优化**
  - `http://` 或 `https://` 开头 → 直接作为公网 URL 传给模型，无需下载转换
  - 本地路径 → 仍然转为 base64 Data URL
- **Prompt 长度校验**：超过 1500 字符会报错退出
- **prompt_optimizer 智能自动判断**
  - 短描述（< 80字符）→ 自动开启优化
  - 长描述（≥ 80字符）→ 自动关闭优化
  - 用户可手动覆盖：`--prompt-optimizer` 或 `--no-prompt-optimizer`
- **aigc_watermark 水印自动开启**：检测到水印相关关键词自动开启
- **输出目录改为共享目录**：`~/.openclaw/media/minimax/`
