# AI Newspaper Rendering Service v1.0

## 中文版

### 这是什么？

AI 报纸渲染服务是一个将新闻内容自动排版成**仿实体报纸风格**的工具。

想象一下：你提供新闻标题和内容，它返回一个精心排版的 HTML 页面——就像传统报纸那样，有大标题、多栏文字、配图，充满纸媒的质感。

### 它能做什么？

**1. 报纸风格排版**
- 自动生成报头（大标题 + 副标题 + 日期）
- 4 栏布局，栏与栏之间有分隔线
- 头条新闻跨栏显示，突出重要内容
- 使用宋体、楷体等传统报纸字体

**2. AI 配图生成**
- 为新闻自动生成配图
- 只需提供英文描述（如："A futuristic AI robot scientist"）
- 图片自动嵌入到合适位置
- 生成失败时自动使用占位图

**3. 响应式适配**
- 大屏幕显示 4 栏
- 平板显示 3 栏
- 小屏手机显示 1 栏
- 无需额外配置

### 使用场景

- 📰 **新闻汇总** - 将每日资讯排版成报纸
- 📋 **周报/月报** - 工作汇报的精美呈现
- 🎁 **创意礼物** - 把故事变成报纸纪念版
- 📢 **公告发布** - 正式公告的创意展示

### 快速开始

```bash
npm install
node server.js
```

服务启动后，发送 POST 请求到 `http://localhost:3000/render`

### 输入示例

```json
{
  "title": "科技日报",
  "subtitle": "聚焦前沿科技",
  "articles": [
    {
      "headline": "AI 大模型迎来突破",
      "body": "今日发布最新 AI 模型...\n\n研究团队表示...",
      "imagePrompt": "A futuristic AI robot scientist, digital art"
    },
    {
      "headline": "量子计算进展",
      "body": "科学家实现新突破..."
    }
  ]
}
```

### 输出结果

返回一个 URL，访问后即可查看渲染好的报纸页面：

```json
{
  "url": "http://localhost:3000/output/abc123.html"
}
```

---

## English Version

### What is this?

AI Newspaper Rendering Service is a tool that automatically formats news content into a **traditional newspaper-style** layout.

Think of it this way: you provide headlines and content, and it returns a beautifully typeset HTML page—just like a real newspaper, with large headlines, multi-column text, images, and that classic print media feel.

### What does it do?

**1. Newspaper-style Layout**
- Auto-generates masthead (title + subtitle + date)
- 4-column layout with separator lines
- Lead articles span across all columns
- Uses traditional Chinese serif fonts

**2. AI Image Generation**
- Automatically generates images for news articles
- Just provide an English description (e.g., "A futuristic AI robot scientist")
- Images are embedded in appropriate positions
- Falls back to placeholders if generation fails

**3. Responsive Design**
- 4 columns on large screens
- 3 columns on tablets
- 1 column on mobile phones
- No extra configuration needed

### Use Cases

- 📰 **News Digest** - Format daily news into newspaper style
- 📋 **Weekly/Monthly Reports** - Beautiful presentation for work reports
- 🎁 **Creative Gifts** - Turn stories into commemorative newspapers
- 📢 **Announcements** - Creative display for formal notices

### Quick Start

```bash
npm install
node server.js
```

After startup, send POST requests to `http://localhost:3000/render`

### Input Example

```json
{
  "title": "Tech Daily",
  "subtitle": "Frontier Technology News",
  "articles": [
    {
      "headline": "AI Model Breakthrough",
      "body": "New AI model released today...\n\nResearch team states...",
      "imagePrompt": "A futuristic AI robot scientist, digital art"
    },
    {
      "headline": "Quantum Computing Progress",
      "body": "Scientists achieve new breakthrough..."
    }
  ]
}
```

### Output

Returns a URL to view the rendered newspaper page:

```json
{
  "url": "http://localhost:3000/output/abc123.html"
}
```

---

**Version / 版本**: v1.0 - 2026 年 3 月