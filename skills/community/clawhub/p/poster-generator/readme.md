# OpenClaw Poster Generator

**AI-Powered Poster Generation Tool / AI 驱动的海报生成工具**

---

## 🎨 Overview / 概述

### English

OpenClaw Poster Generator is an AI-powered tool that helps you create professional marketing posters, social media graphics, event flyers, and promotional materials with simple commands. Whether you're a marketer, designer, or content creator, this tool streamlines your poster creation workflow.

### 中文

OpenClaw 海报生成器是一个 AI 驱动的工具，帮助您通过简单的命令创建专业的营销海报、社交媒体图片、活动传单和宣传物料。无论您是营销人员、设计师还是内容创作者，这个工具都能简化您的海报创建流程。

---

## ✨ Features / 核心功能

### English

- 🎨 **Template System** - Pre-designed templates for various use cases
- 📝 **Smart Text Rendering** - Automatic text sizing and positioning
- 🖼️ **Image Composition** - Combine multiple images and elements
- 🎨 **Color Schemes** - Built-in color palettes and custom options
- 📏 **Multiple Formats** - Export to PNG, JPG, PDF, SVG
- ⚡ **Batch Generation** - Create multiple posters at once
- 🤖 **AI Assistant** - Get design suggestions and improvements
- 🔧 **Customizable** - Full control over fonts, colors, layouts

### 中文

- 🎨 **模板系统** - 为各种使用场景预设计的模板
- 📝 **智能文字渲染** - 自动文字大小调整和定位
- 🖼️ **图像组合** - 组合多个图像和元素
- 🎨 **色彩方案** - 内置色彩调色板和自定义选项
- 📏 **多种格式** - 导出为 PNG、JPG、PDF、SVG
- ⚡ **批量生成** - 一次创建多张海报
- 🤖 **AI 助手** - 获取设计建议和改进
- 🔧 **可自定义** - 完全控制字体、颜色、布局

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

**English**:
```bash
# Install globally via npm
npm install -g openclaw-poster-generator

# Or use npx (no installation required)
npx openclaw-poster-generator create --template marketing
```

**中文**：
```bash
# 通过 npm 全局安装
npm install -g openclaw-poster-generator

# 或使用 npx（无需安装）
npx openclaw-poster-generator create --template marketing
```

### Basic Usage / 基本使用

**English**:
```bash
# Create a marketing poster
poster-gen create \
  --template marketing \
  --title "Summer Sale" \
  --subtitle "Up to 50% OFF" \
  --output poster.png

# Create an event poster
poster-gen create \
  --template event \
  --title "Tech Conference 2024" \
  --date "March 25-27" \
  --location "San Francisco" \
  --output event.png

# Batch generation
poster-gen batch \
  --config posters.json \
  --output-dir ./output
```

**中文**：
```bash
# 创建营销海报
poster-gen create \
  --template marketing \
  --title "夏季促销" \
  --subtitle "最高 5 折优惠" \
  --output poster.png

# 创建活动海报
poster-gen create \
  --template event \
  --title "2024 技术大会" \
  --date "3月25-27日" \
  --location "旧金山" \
  --output event.png

# 批量生成
poster-gen batch \
  --config posters.json \
  --output-dir ./output
```

---

## 📖 Documentation / 文档

### Available Templates / 可用模板

**English**:

| Template | Size | Use Case | Description |
|----------|------|----------|-------------|
| `marketing` | 1920x1080 | Product promotions | Bold, eye-catching design for sales |
| `event` | 1080x1920 | Conferences, events | Professional layout with date/location |
| `social` | 1080x1080 | Instagram, Facebook | Square format, social media optimized |
| `minimal` | 1200x630 | Corporate | Clean, modern professional style |
| `creative` | 1920x1080 | Art, design | Colorful, artistic layouts |

**中文**：

| 模板 | 尺寸 | 使用场景 | 描述 |
|------|------|----------|------|
| `marketing` | 1920x1080 | 产品促销 | 大胆醒目的销售设计 |
| `event` | 1080x1920 | 会议、活动 | 专业布局，含日期/地点 |
| `social` | 1080x1080 | Instagram、Facebook | 方形格式，社交媒体优化 |
| `minimal` | 1200x630 | 企业 | 简洁现代的专业风格 |
| `creative` | 1920x1080 | 艺术、设计 | 多彩艺术布局 |

### Command Line Options / 命令行选项

**English**:

```bash
poster-gen create [options]

Options:
  --template <name>      Template name (marketing, event, social, etc.)
  --title <text>         Main title text
  --subtitle <text>      Subtitle text
  --description <text>   Description text
  --date <text>          Event date (for event template)
  --location <text>      Event location (for event template)
  --colors <colors>      Custom colors (comma-separated hex codes)
  --background <path>    Background image path
  --logo <path>          Logo image path
  --font-title <font>    Title font name
  --font-body <font>     Body font name
  --width <pixels>       Custom width
  --height <pixels>      Custom height
  --format <type>        Output format (png, jpg, pdf, svg)
  --quality <number>     Output quality (1-100)
  --dpi <number>         DPI for print (default: 72)
  --output <path>        Output file path
```

**中文**：

```bash
poster-gen create [选项]

选项：
  --template <名称>      模板名称（marketing、event、social 等）
  --title <文本>         主标题文本
  --subtitle <文本>      副标题文本
  --description <文本>   描述文本
  --date <文本>          活动日期（用于 event 模板）
  --location <文本>      活动地点（用于 event 模板）
  --colors <颜色>        自定义颜色（逗号分隔的十六进制代码）
  --background <路径>    背景图片路径
  --logo <路径>          Logo 图片路径
  --font-title <字体>    标题字体名称
  --font-body <字体>     正文字体名称
  --width <像素>         自定义宽度
  --height <像素>        自定义高度
  --format <类型>        输出格式（png、jpg、pdf、svg）
  --quality <数字>       输出质量（1-100）
  --dpi <数字>           打印 DPI（默认：72）
  --output <路径>        输出文件路径
```

---

## 💡 Use Cases / 使用场景

### English

**1. Marketing Campaign**
Create consistent branded posters for product launches, sales, and promotions.

**2. Social Media Content**
Generate optimized graphics for Instagram, Facebook, Twitter posts.

**3. Event Promotion**
Design professional flyers for conferences, workshops, meetups.

**4. E-commerce**
Create product announcement posters for online stores.

**5. Real Estate**
Generate property listing posters with photos and details.

### 中文

**1. 营销活动**
为产品发布、销售和促销创建一致品牌的海报。

**2. 社交媒体内容**
为 Instagram、Facebook、Twitter 帖子生成优化的图片。

**3. 活动推广**
为会议、研讨会、聚会设计专业传单。

**4. 电子商务**
为在线商店创建产品公告海报。

**5. 房地产**
生成带有照片和详细信息的房产列表海报。

---

## 🎯 Examples / 示例

### Example 1: Marketing Poster / 营销海报

**English**:
```bash
poster-gen create \
  --template marketing \
  --title "Black Friday Sale" \
  --subtitle "Everything 50% OFF" \
  --description "This Weekend Only" \
  --colors "#000000,#FF0000,#FFFFFF" \
  --output black-friday.png
```

**中文**：
```bash
poster-gen create \
  --template marketing \
  --title "黑色星期五特卖" \
  --subtitle "全场 5 折" \
  --description "仅限本周末" \
  --colors "#000000,#FF0000,#FFFFFF" \
  --output black-friday.png
```

### Example 2: Event Poster / 活动海报

**English**:
```bash
poster-gen create \
  --template event \
  --title "AI Summit 2024" \
  --date "March 25-27, 2024" \
  --location "San Francisco, CA" \
  --background ./images/tech-bg.jpg \
  --logo ./images/logo.png \
  --output ai-summit.png
```

**中文**：
```bash
poster-gen create \
  --template event \
  --title "2024 AI 峰会" \
  --date "2024年3月25-27日" \
  --location "旧金山，加州" \
  --background ./images/tech-bg.jpg \
  --logo ./images/logo.png \
  --output ai-summit.png
```

### Example 3: Batch Generation / 批量生成

**posters.json**:
```json
{
  "posters": [
    {
      "template": "social",
      "title": "Monday Motivation",
      "colors": ["#FF6B6B", "#4ECDC4"],
      "output": "monday.png"
    },
    {
      "template": "social",
      "title": "Tuesday Tips",
      "colors": ["#95E1D3", "#F38181"],
      "output": "tuesday.png"
    }
  ]
}
```

**English**:
```bash
poster-gen batch --config posters.json
```

**中文**：
```bash
poster-gen batch --config posters.json
```

---

## 🛠️ Advanced Usage / 高级用法

### Custom Templates / 自定义模板

**English**:
Create your own templates in `templates/` directory:

```javascript
// templates/my-template.js
module.exports = {
  name: 'my-template',
  width: 1920,
  height: 1080,
  layers: [
    {
      type: 'background',
      color: '#FF6B6B'
    },
    {
      type: 'text',
      content: '{{title}}',
      fontSize: 72,
      position: { x: 'center', y: 200 }
    }
  ]
};
```

**中文**：
在 `templates/` 目录中创建自己的模板：

```javascript
// templates/my-template.js
module.exports = {
  name: 'my-template',
  width: 1920,
  height: 1080,
  layers: [
    {
      type: 'background',
      color: '#FF6B6B'
    },
    {
      type: 'text',
      content: '{{title}}',
      fontSize: 72,
      position: { x: 'center', y: 200 }
    }
  ]
};
```

### Programmatic API / 编程 API

**English**:
```javascript
const { PosterGenerator } = require('openclaw-poster-generator');

const generator = new PosterGenerator();

await generator.create({
  template: 'marketing',
  data: {
    title: 'Custom Poster',
    subtitle: 'Made with API'
  },
  output: 'output.png'
});
```

**中文**：
```javascript
const { PosterGenerator } = require('openclaw-poster-generator');

const generator = new PosterGenerator();

await generator.create({
  template: 'marketing',
  data: {
    title: '自定义海报',
    subtitle: '使用 API 制作'
  },
  output: 'output.png'
});
```

---

## 🔧 Configuration / 配置

### Config File / 配置文件

**English**:
Create `.postergenrc.json` in your project:

```json
{
  "defaultTemplate": "marketing",
  "defaultFormat": "png",
  "defaultQuality": 90,
  "outputDir": "./output",
  "fonts": {
    "title": "Arial Bold",
    "body": "Arial"
  },
  "colors": {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4"
  }
}
```

**中文**：
在项目中创建 `.postergenrc.json`：

```json
{
  "defaultTemplate": "marketing",
  "defaultFormat": "png",
  "defaultQuality": 90,
  "outputDir": "./output",
  "fonts": {
    "title": "Arial Bold",
    "body": "Arial"
  },
  "colors": {
    "primary": "#FF6B6B",
    "secondary": "#4ECDC4"
  }
}
```

---

## 🐛 Troubleshooting / 故障排查

### Common Issues / 常见问题

**English**:

**Q: Font not found**
```bash
sudo apt-get install fonts-liberation
```

**Q: Low quality output**
```bash
poster-gen create --dpi 300 --quality 100
```

**Q: Memory issues**
```bash
NODE_OPTIONS="--max-old-space-size=4096" poster-gen create
```

**中文**：

**问：字体未找到**
```bash
sudo apt-get install fonts-liberation
```

**问：输出质量低**
```bash
poster-gen create --dpi 300 --quality 100
```

**问：内存问题**
```bash
NODE_OPTIONS="--max-old-space-size=4096" poster-gen create
```

---

## 📄 License / 许可证

MIT License

---

## 🔗 Links / 链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-poster-generator
- **npm**: https://www.npmjs.com/package/openclaw-poster-generator
- **Issues**: https://github.com/ZhenRobotics/openclaw-poster-generator/issues
- **Documentation**: https://github.com/ZhenRobotics/openclaw-poster-generator/wiki

---

## 🤝 Official Support Partner / 官方技术支持合作伙伴

### English

For technical support, custom development, and consulting services, please contact our official maintenance partner:

**Official Maintenance Partner**:
- **Name**: 黄纪恩学长 (Huang Jien)
- **Xianyu ID**: 专注人工智能的黄纪恩学长
- **Specialization**: Artificial Intelligence & Technical Support
- **Services Offered**:
  - ✅ Technical consultation and troubleshooting
  - ✅ Custom poster template development
  - ✅ API integration support
  - ✅ Training and onboarding for teams
  - ✅ Performance optimization
  - ✅ Feature customization

### 中文

如需技术支持、定制开发和咨询服务，请联系我们的官方维护合作伙伴：

**官方维护合作伙伴**：
- **姓名**: 黄纪恩学长
- **闲鱼 ID**: 专注人工智能的黄纪恩学长
- **专长**: 人工智能与技术支持
- **提供服务**：
  - ✅ 技术咨询与故障排查
  - ✅ 定制海报模板开发
  - ✅ API 集成支持
  - ✅ 团队培训与入门指导
  - ✅ 性能优化
  - ✅ 功能定制

### How to Contact / 如何联系

**English**:
1. Open Xianyu App (闲鱼 APP)
2. Search for "专注人工智能的黄纪恩学长"
3. Send your technical requirements or questions
4. Our partner will respond within 24 hours

**中文**：
1. 打开闲鱼 APP
2. 搜索「专注人工智能的黄纪恩学长」
3. 发送您的技术需求或问题
4. 合作伙伴将在 24 小时内回复

---

**Create stunning posters with AI! / 用 AI 创建精美海报！** ✨🎨
