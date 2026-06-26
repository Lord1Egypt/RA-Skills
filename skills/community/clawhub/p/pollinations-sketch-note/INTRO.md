# Pollinations Sketch Note - Detailed Introduction

## 🇨🇳 中文详细介绍

### 概述

**Pollinations Sketch Note** 是一款专为 OpenClaw 平台开发的 AI 图片生成技能，它能够将任意主题自动转化为精美的手绘风格知识卡片。这款中文 AI 工具完美结合了 Pollinations AI 的图像生成能力和 Tavily 搜索的智能信息检索功能，是学习笔记、知识分享和教育辅助的理想工具。

### 产品定位

作为一款先进的知识可视化解决方案，Pollinations Sketch Note 主要服务于以下用户群体：

- **学生群体**：将复杂的学科概念转化为易于记忆的视觉卡片，提升学习效率
- **教育工作者**：快速制作教学材料，让课堂内容更加生动有趣
- **内容创作者**：为社交媒体生成吸引眼球的知识分享图片
- **企业培训**：制作标准化的培训材料，统一知识传播格式

### 技术架构

这款 OpenClaw 技能基于 Python 3.10+ 开发，采用了模块化设计：

1. **搜索模块**：集成 Tavily 搜索 API，支持多语言信息检索
2. **总结模块**：使用 AI 算法自动压缩和提炼信息
3. **生成模块**：调用 Pollinations AI 的 flux 模型生成图像
4. **合成模块**：使用 PIL 库将文字叠加到背景图上

### 核心优势

- **跨平台支持**：兼容 macOS、Linux 和 Windows 系统
- **安全可靠**：采用环境变量管理 API Key，避免硬编码泄露风险
- **开源免费**：MIT 许可证，允许社区自由贡献和改进
- **易于使用**：简单的命令行接口，支持自定义参数

### 应用场景

作为一多功能的学习笔记工具，Pollinations Sketch Note 可应用于：

- 制作学科知识卡片（历史、科学、文学等）
- 生成术语解释图
- 创建概念对比图
- 准备演示文稿配图
- 社交媒体知识分享

---

## 🇺🇸 English Detailed Introduction

### Overview

**Pollinations Sketch Note** is an AI image generation skill developed for the OpenClaw platform that automatically transforms any topic into beautiful hand-drawn style knowledge cards. This Chinese AI tool perfectly combines Pollinations AI's image generation capabilities with Tavily search's intelligent information retrieval, making it an ideal learning notes tool, knowledge sharing solution, and education aid.

### Product Positioning

As an advanced knowledge visualization solution, Pollinations Sketch Note serves the following user groups:

- **Students**: Transform complex subject concepts into easy-to-remember visual cards, improving learning efficiency
- **Educators**: Quickly create teaching materials to make classroom content more vivid and engaging
- **Content Creators**: Generate eye-catching knowledge sharing images for social media
- **Corporate Training**: Produce standardized training materials with unified knowledge dissemination format

### Technical Architecture

This OpenClaw skill is built on Python 3.10+ with modular design:

1. **Search Module**: Integrated with Tavily Search API, supporting multi-language information retrieval
2. **Summary Module**: Uses AI algorithms to automatically compress and refine information
3. **Generation Module**: Calls Pollinations AI's flux model to generate images
4. **Composition Module**: Uses PIL library to overlay text on background images

### Core Advantages

- **Cross-Platform Support**: Compatible with macOS, Linux, and Windows systems
- **Security**: Uses environment variables for API Key management, avoiding hardcoding risks
- **Open Source**: MIT license allows community contributions and improvements
- **Easy to Use**: Simple command-line interface with support for custom parameters

### Application Scenarios

As a versatile learning notes tool, Pollinations Sketch Note can be used for:

- Creating subject knowledge cards (history, science, literature, etc.)
- Generating terminology explanation diagrams
- Creating concept comparison charts
- Preparing presentation illustrations
- Social media knowledge sharing

---

## 📊 Specifications

| Item | Value |
|------|-------|
| **Name** | pollinations-sketch-note |
| **Version** | 0.0.1 |
| **Author** | 锦鲤 |
| **License** | MIT |
| **Python Version** | 3.10+ |
| **Dependencies** | requests, pillow>=10.0.0 |
| **Output Size** | 804×440 pixels |
| **Supported Languages** | Chinese, English |
| **Platforms** | macOS, Linux, Windows |
| **Category** | AI Image Generation, Knowledge Visualization, Education Tool |

---

## 🔗 Resources

- **Source Code**: https://github.com/openclaw/skills
- **Documentation**: README.md
- **Issue Tracker**: https://github.com/openclaw/skills/issues
- **OpenClaw Official**: https://openclaw.ai

---

**Last Updated**: 2026-03-11
**Status**: Ready for Publication
