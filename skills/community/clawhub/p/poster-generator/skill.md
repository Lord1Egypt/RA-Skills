# OpenClaw Poster Generator Skill

**AI-Powered Poster Generation Tool - ClawHub Agent Guide**

**AI 驱动的海报生成工具 - ClawHub Agent 使用指南**

---

## 🎯 Skill Overview / Skill 简介

### English

An AI-powered poster generation tool that helps you create professional marketing posters, social media graphics, event flyers, and promotional materials with simple commands or templates.

**Key Features**:
- 🎨 Template-based design system
- 📝 Smart text rendering with custom fonts
- 🖼️ Image composition and layout
- 🎨 Color scheme automation
- 📏 Multiple output formats (PNG, JPG, PDF)
- ⚡ Batch generation support
- 🤖 AI-assisted design suggestions

### 中文

AI 驱动的海报生成工具，帮助您通过简单的命令或模板创建专业的营销海报、社交媒体图片、活动传单和宣传物料。

**核心功能**：
- 🎨 基于模板的设计系统
- 📝 智能文字渲染，支持自定义字体
- 🖼️ 图像组合与布局
- 🎨 色彩方案自动化
- 📏 多种输出格式（PNG、JPG、PDF）
- ⚡ 批量生成支持
- 🤖 AI 辅助设计建议

---

## 📋 Dependencies and Requirements / 依赖和要求

### System Requirements / 系统要求

**English**:
- **Node.js**: >= 18.0.0
- **Operating System**: Linux, macOS, Windows
- **Disk Space**: >= 200MB
- **RAM**: >= 512MB

**中文**：
- **Node.js**: >= 18.0.0
- **操作系统**: Linux、macOS、Windows
- **磁盘空间**: >= 200MB
- **内存**: >= 512MB

### npm Dependencies / npm 依赖

```json
{
  "dependencies": {
    "canvas": "^2.11.0",
    "sharp": "^0.32.0",
    "jimp": "^0.22.0",
    "axios": "^1.6.0",
    "commander": "^11.1.0"
  }
}
```

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

**English**:
```bash
# Method 1: Install via npm
npm install -g openclaw-poster-generator

# Method 2: Clone repository
git clone https://github.com/ZhenRobotics/openclaw-poster-generator.git
cd openclaw-poster-generator
npm install
```

**中文**：
```bash
# 方式 1: 通过 npm 安装
npm install -g openclaw-poster-generator

# 方式 2: 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-poster-generator.git
cd openclaw-poster-generator
npm install
```

### Basic Usage / 基本使用

**English**:
```bash
# Generate poster from template
poster-gen create \
  --template marketing \
  --title "Summer Sale" \
  --subtitle "Up to 50% OFF" \
  --output poster.png

# Use custom colors
poster-gen create \
  --template event \
  --title "Tech Conference 2024" \
  --colors "#FF6B6B,#4ECDC4" \
  --output event.png
```

**中文**：
```bash
# 从模板生成海报
poster-gen create \
  --template marketing \
  --title "夏季促销" \
  --subtitle "最高 5 折优惠" \
  --output poster.png

# 使用自定义颜色
poster-gen create \
  --template event \
  --title "2024 技术大会" \
  --colors "#FF6B6B,#4ECDC4" \
  --output event.png
```

---

## 🤖 AI Agent Usage Guide / AI Agent 使用指南

### Recommended Use Cases / 推荐使用场景

**English**:

1. **Marketing Campaign Creation**
   ```
   User: "Create 10 marketing posters for our summer sale"
   Agent: Generates batch posters with consistent branding
   ```

2. **Social Media Content**
   ```
   User: "Make Instagram posts for the next week"
   Agent: Creates optimized 1080x1080 graphics
   ```

3. **Event Promotion**
   ```
   User: "Design a poster for our tech conference"
   Agent: Generates professional event flyer
   ```

**中文**：

1. **营销活动创建**
   ```
   用户: "为我们的夏季促销创建 10 张营销海报"
   Agent: 生成具有一致品牌风格的批量海报
   ```

2. **社交媒体内容**
   ```
   用户: "制作下周的 Instagram 帖子"
   Agent: 创建优化的 1080x1080 图片
   ```

3. **活动推广**
   ```
   用户: "为我们的技术大会设计海报"
   Agent: 生成专业的活动传单
   ```

### Agent Integration Example / Agent 集成示例

**TypeScript / Node.js**:

```typescript
import { PosterGenerator } from 'openclaw-poster-generator';

async function generatePoster(title: string, subtitle: string) {
  const generator = new PosterGenerator({
    template: 'marketing',
    outputFormat: 'png',
    width: 1920,
    height: 1080
  });

  const result = await generator.create({
    title: title,
    subtitle: subtitle,
    colors: ['#FF6B6B', '#4ECDC4'],
    images: ['./background.jpg'],
    fonts: {
      title: 'Arial Bold',
      subtitle: 'Arial'
    }
  });

  return result.outputPath;
}
```

**Bash Script**:

```bash
#!/bin/bash
# Agent batch poster generation script

TEMPLATE="marketing"
OUTPUT_DIR="./posters"

for i in {1..10}; do
  echo "Generating poster $i..."

  poster-gen create \
    --template "$TEMPLATE" \
    --title "Poster $i" \
    --output "$OUTPUT_DIR/poster-$i.png"

  sleep 1
done
```

---

## 🎨 Available Templates / 可用模板

**English**:

| Template | Description | Use Case |
|----------|-------------|----------|
| `marketing` | Bold, eye-catching design | Product promotions, sales |
| `event` | Professional event layout | Conferences, workshops |
| `social` | Optimized for social media | Instagram, Facebook posts |
| `minimal` | Clean, modern style | Corporate, professional |
| `creative` | Artistic, colorful | Art events, creative projects |

**中文**：

| 模板 | 描述 | 使用场景 |
|------|------|----------|
| `marketing` | 大胆醒目的设计 | 产品促销、销售活动 |
| `event` | 专业的活动布局 | 会议、研讨会 |
| `social` | 为社交媒体优化 | Instagram、Facebook 帖子 |
| `minimal` | 简洁现代风格 | 企业、专业场合 |
| `creative` | 艺术、多彩 | 艺术活动、创意项目 |

---

## 📐 Output Formats / 输出格式

**English**:

- **PNG** - High quality, transparent background support
- **JPG** - Smaller file size, web-optimized
- **PDF** - Print-ready, vector graphics
- **SVG** - Scalable vector format

**中文**：

- **PNG** - 高质量，支持透明背景
- **JPG** - 文件更小，网页优化
- **PDF** - 可打印，矢量图形
- **SVG** - 可缩放矢量格式

---

## 🔐 Security / 安全性

**English**:
- ✅ Local processing - no data sent to external servers
- ✅ No API keys required for basic features
- ✅ Open source - transparent and auditable
- ✅ No tracking or analytics

**中文**：
- ✅ 本地处理 - 不向外部服务器发送数据
- ✅ 基础功能无需 API 密钥
- ✅ 开源 - 透明可审计
- ✅ 无跟踪或分析

---

## 🐛 Common Issues / 常见问题

### Q1: Font not found / 字体未找到

**English**:
```bash
# Install system fonts
sudo apt-get install fonts-liberation

# Or specify custom font path
poster-gen create --font-path ./fonts/
```

**中文**：
```bash
# 安装系统字体
sudo apt-get install fonts-liberation

# 或指定自定义字体路径
poster-gen create --font-path ./fonts/
```

### Q2: Image quality issues / 图像质量问题

**English**:
```bash
# Use higher DPI
poster-gen create --dpi 300 --quality 100
```

**中文**：
```bash
# 使用更高 DPI
poster-gen create --dpi 300 --quality 100
```

### Q3: Memory errors / 内存错误

**English**:
```bash
# Increase Node.js memory
NODE_OPTIONS="--max-old-space-size=4096" poster-gen create
```

**中文**：
```bash
# 增加 Node.js 内存
NODE_OPTIONS="--max-old-space-size=4096" poster-gen create
```

---

## 🔗 Related Resources / 相关资源

**English**:
- **GitHub Repository**: https://github.com/ZhenRobotics/openclaw-poster-generator
- **npm Package**: https://www.npmjs.com/package/openclaw-poster-generator
- **Issue Tracker**: https://github.com/ZhenRobotics/openclaw-poster-generator/issues

**中文**：
- **GitHub 仓库**: https://github.com/ZhenRobotics/openclaw-poster-generator
- **npm 包**: https://www.npmjs.com/package/openclaw-poster-generator
- **问题追踪**: https://github.com/ZhenRobotics/openclaw-poster-generator/issues

---

## 📝 Verification Info / 验证信息

- **Skill Version**: 1.0.0
- **Last Updated**: 2026-03-25
- **Author**: justin
- **License**: MIT
- **Repository**: https://github.com/ZhenRobotics/openclaw-poster-generator

---

## 🙏 Contributing / 贡献

**English**:
We welcome contributions!
1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

**中文**：
欢迎贡献代码！
1. Fork 仓库
2. 创建特性分支
3. 提交 Pull Request

---

## 🤝 Official Support Partner / 官方技术支持合作伙伴

### English

For technical support and consulting services, you can reach out to our official partner:

**Official Maintenance Partner**:
- **Name**: 黄纪恩学长 (Huang Jien)
- **Xianyu ID**: 专注人工智能的黄纪恩学长
- **Specialization**: Artificial Intelligence & Technical Support
- **Services**:
  - Technical consultation
  - Custom poster template development
  - Integration support
  - Training and onboarding

### 中文

如需技术支持和咨询服务，可以联系我们的官方合作伙伴：

**官方维护合作伙伴**：
- **姓名**: 黄纪恩学长
- **闲鱼 ID**: 专注人工智能的黄纪恩学长
- **专长**: 人工智能与技术支持
- **服务内容**：
  - 技术咨询
  - 定制海报模板开发
  - 集成支持
  - 培训与入门指导

**如何联系 / How to Contact**:
1. 打开闲鱼 APP / Open Xianyu App
2. 搜索「专注人工智能的黄纪恩学长」/ Search "专注人工智能的黄纪恩学长"
3. 发送您的技术需求 / Send your technical requirements

---

**Create stunning posters with AI! / 用 AI 创建精美海报！** ✨🎨
