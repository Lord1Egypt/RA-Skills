# 长文配图助手 (Long Article Illustration)

为长篇文章自动生成 AI 配图的 Skill 配置文件。

## ✨ 功能特性

- **智能段落划分**：自动识别文章结构，按语义边界划分配图段落
- **提示词生成**：为每个段落生成高质量的图像生成提示词
- **多风格支持**：扁平插画、水彩、卡通、国风水墨、科技感、极简线条
- **人物一致性**：通过角色锚定描述保持同一人物外观一致
- **避免图片文字**：自动添加参数避免生成的图片出现乱码文字

## 📁 文件结构

```
├── SKILL.md                    # 主配置文件，定义完整工作流程
├── references/
│   ├── style-presets.md        # 6种图片风格预设及提示词模板
│   ├── paragraph-rules.md      # 段落划分详细规则
│   └── troubleshooting.md      # 常见问题处理方案
└── preview/                    # 效果预览案例
    ├── 校园主题文章_配图效果.pdf
    ├── 职场主题文章_配图效果.pdf
    └── 案例*.png
```

## 🚀 使用方法

1. 将 `SKILL.md` 及 `references/` 文件夹导入支持 Skill 的 AI 助手
2. 向 AI 提供需要配图的长文章
3. 可选参数：
   - **图片风格**：默认扁平插画
   - **图片比例**：默认 16:9
   - **配图密度**：默认每 2-3 段一图

## 🎨 支持风格

| 风格 | 适用场景 |
|------|----------|
| 扁平插画 | 科技、商业、教程 |
| 水彩风格 | 情感、文艺、生活 |
| 卡通风格 | 轻松、幽默、儿童 |
| 国风水墨 | 传统文化、古典 |
| 科技感 | AI、数据、未来 |
| 极简线条 | 高端、简约、商务 |

## 📐 支持比例

| 用途 | 比例 |
|------|------|
| 公众号封面 | 2.35:1 |
| 公众号内文 | 16:9 |
| 小红书配图 | 3:4 |
| 正方形 | 1:1 |

## 📸 效果预览

| | |
|:---:|:---:|
| ![案例1](preview/案例1.png) | ![案例2](preview/案例2.png) |
| ![案例3](preview/案例3.png) | ![案例4](preview/案例4.png) |

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE) 开源。


# Long Article Illustration Assistant

An AI Skill configuration for automatically generating illustrations for long-form articles.

## ✨ Features

- **Smart Paragraph Segmentation**: Automatically identifies article structure and divides content by semantic boundaries
- **Prompt Generation**: Creates high-quality image generation prompts for each paragraph
- **Multiple Styles**: Flat illustration, watercolor, cartoon, Chinese ink, tech, minimalist
- **Character Consistency**: Maintains consistent character appearance through anchor descriptions
- **Text-Free Images**: Automatically adds parameters to prevent garbled text in generated images

## 📁 File Structure

```
├── SKILL.md                    # Main config file defining the complete workflow
├── references/
│   ├── style-presets.md        # 6 style presets and prompt templates
│   ├── paragraph-rules.md      # Detailed paragraph segmentation rules
│   └── troubleshooting.md      # Common issue solutions
└── preview/                    # Preview examples
    ├── 校园主题文章_配图效果.pdf   # Campus theme article demo
    ├── 职场主题文章_配图效果.pdf   # Workplace theme article demo
    └── 案例*.png                 # Sample images
```

## 🚀 Usage

1. Import `SKILL.md` and the `references/` folder into an AI assistant that supports Skills
2. Provide the AI with your long-form article
3. Optional parameters:
   - **Image Style**: Default is flat illustration
   - **Aspect Ratio**: Default is 16:9
   - **Illustration Density**: Default is one image per 2-3 paragraphs

## 🎨 Supported Styles

| Style | Best For |
|-------|----------|
| Flat Illustration | Tech, business, tutorials |
| Watercolor | Emotional, literary, lifestyle |
| Cartoon | Casual, humor, children's content |
| Chinese Ink | Traditional culture, classical |
| Tech/Futuristic | AI, data, future topics |
| Minimalist | Premium, simple, business |

## 📐 Supported Aspect Ratios

| Usage | Ratio |
|-------|-------|
| WeChat Article Cover | 2.35:1 |
| WeChat Article Content | 16:9 |
| Xiaohongshu (RED) | 3:4 |
| Square | 1:1 |

## 📸 Preview

| | |
|:---:|:---:|
| ![案例1](preview/案例1.png) | ![案例2](preview/案例2.png) |
| ![案例3](preview/案例3.png) | ![案例4](preview/案例4.png) |

## 📄 License

This project is open source under the [MIT License](LICENSE).
