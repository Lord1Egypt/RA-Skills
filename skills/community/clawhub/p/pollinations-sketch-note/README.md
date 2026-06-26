# Pollinations Sketch Note 🎨

**AI 手绘知识卡片生成器 | AI-Powered Sketch Note Generator**

自动生成手绘风格知识卡片，支持自动搜索、智能总结、3 种艺术风格。

---

## 📖 简介 / Introduction

### 🇨🇳 中文

Pollinations Sketch Note 是一个为 OpenClaw 设计的 AI 图片生成技能。它能自动搜索主题信息，智能总结内容，并生成精美的手绘风格知识卡片。

**它能做什么：**
- 🔍 自动从维基百科、百度百科搜索主题信息
- 📝 AI 智能总结成 180-200 字
- 🎨 3 种手绘风格随机轮换（极简/可爱/赛博朋克）
- 📐 输出 804×440 标准尺寸图片
- ✍️ 自动添加署名和时间

**适合谁用：**
- 学生：制作学习笔记卡片
- 老师：快速生成教学材料
- 内容创作者：社交媒体知识分享
- 企业培训：标准化培训材料

### 🇺🇸 English

Pollinations Sketch Note is an AI image generation skill for OpenClaw. It automatically searches for topic information, summarizes content, and generates beautiful hand-drawn style knowledge cards.

**What it does:**
- 🔍 Auto-search from Wikipedia and Baidu Baike
- 📝 AI summarizes to 180-200 characters
- 🎨 3 hand-drawn styles (Minimalist/Cute/Cyberpunk)
- 📐 Outputs 804×440 standard size images
- ✍️ Auto signature and timestamp

**Who it's for:**
- Students: Create learning note cards
- Educators: Quick teaching materials
- Content creators: Social media knowledge sharing
- Corporate training: Standardized training materials

---

## 🚀 快速开始 / Quick Start

### 1️⃣ 安装依赖 / Install Dependencies

```bash
pip3 install requests pillow
```

### 2️⃣ 配置环境变量 / Configure Environment Variables

```bash
# macOS/Linux: 编辑 ~/.zshrc 或 ~/.bashrc
export POLLINATIONS_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# Windows PowerShell:
$env:POLLINATIONS_API_KEY="your-key"
$env:TAVILY_API_KEY="your-key"
```

### 3️⃣ 生成卡片 / Generate Card

```bash
# 自动生成（搜索 + 总结）
python3 generate.py --theme "人工智能"

# 自定义文字
python3 generate.py --theme "AI" --detail "自定义介绍内容..."
```

### 4️⃣ 在 OpenClaw 中使用 / Use in OpenClaw

对话中说：
- "生成关于 XXX 的图片"
- "画一个 XXX 的知识卡片"

---

## 📦 Package Info

| Item | Value |
|------|-------|
| **Version** | 0.0.1 |
| **Author** | 锦鲤 |
| **License** | MIT |
| **Python** | 3.10+ |
| **Platforms** | macOS, Linux, Windows |

---

## 📚 完整文档 / Documentation

详细使用指南请查看：[INTRO.md](INTRO.md)

- 完整功能介绍
- 详细配置步骤
- 高级用法示例
- 常见问题解答

---

## 🔗 Links

- **GitHub**: https://github.com/openclaw/skills
- **OpenClaw**: https://openclaw.ai
- **Issues**: https://github.com/openclaw/skills/issues

---

**License**: MIT | **Author**: 锦鲤
