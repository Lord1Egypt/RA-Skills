---
name: long-image-generator
description: |
  Generative AI 长图（竖版图片）制作技能。使用 canvas 将文本、LaTeX 公式、图表等内容渲染为长条形图片（1080x+ 像素），适用于课程笔记、知识卡片、学习指南、读书笔记、思维导图等场景。
  触发时机：(1) 用户要求"生成一张长图"或"做个长图" (2) 用户提到"竖图"、"海报"、"知识卡片" (3) 需要将文档/笔记转换为图片时
---

# Long Image Generator

通用长图（竖版图片）生成技能，可将文本、公式、图表等内容渲染为精美的长条图片。

## 支持的内容类型

| 类型 | 说明 | 示例 |
|------|------|------|
| 纯文本 | 标题、段落、列表 | 读书笔记、知识点总结 |
| LaTeX 公式 | 数学公式渲染 | $\int_a^b f(x)dx$ |
| 代码块 | 语法高亮代码 | Python、JavaScript |
| 表格 | 行列数据 | 课表、价格表 |
| 分割线 | 内容分区 | PART 分隔 |

## 输出规格

- 默认宽度：1080px
- 最小高度：500px
- 最大高度：无限制（自动扩展）
- 背景色：#FFFFFF (可定制)
- 文字色：#1D3557 (深海蓝)
- 标题色：#E85D4E (龙虾红)
- 强调色：#F4A261 (暖橙)

## 生成流程

### 1. 内容规划

将用户需求拆分为若干 PART（模块），每个 PART 高度建议 600-1200px：

```
PART 1: 封面/标题区 (~400px)
PART 2: 核心内容区 (~800px)
PART 3: 示例/练习区 (~600px)
PART 4: 总结/复习区 (~300px)
```

### 2. Canvas 渲染

使用 OpenClaw 的 canvas 工具渲染 HTML 为图片：

```javascript
// 基础模板结构
const template = `
<!DOCTYPE html>
<html>
<head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&family=JetBrains+Mono&display=swap');
    body { font-family: 'Noto Sans SC', sans-serif; margin: 0; padding: 0; }
    .part { padding: 40px; margin-bottom: 20px; }
    .title { color: #E85D4E; font-size: 48px; font-weight: 700; }
    .content { color: #1D3557; font-size: 28px; line-height: 1.8; }
    .formula { font-size: 32px; }
  </style>
</head>
<body>
  ${content}
</body>
</html>
`;

canvas.action = 'present';
canvas.javaScript = template;
canvas.width = 1080;
canvas.height = totalHeight;
```

### 3. LaTeX 公式渲染

在 HTML 中直接使用 LaTeX：

```html
<!-- 使用 KaTeX -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>

<!-- 公式示例 -->
<div class="formula">$$\\int_a^b f(x)dx = F(b) - F(a)$$</div>
```

### 4. 代码高亮

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-@11.9.0/build/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-@11.9.0/build/highlight.min.js"></script>
<pre><code class="language-python">def f(x):
    return x**2</code></pre>
```

## 输出流程

### 1. 生成 Canvas

调用 canvas 工具生成 HTML 渲染：

```json
{
  "action": "present",
  "javaScript": "HTML模板",
  "width": 1080,
  "height": auto,
  "outputFormat": "png"
}
```

### 2. 下载图片

Canvas 输出会自动返回图片路径，通常位于：
`/root/.openclaw/media/outbound/longimage_*.png`

### 3. 提供下载

使用 lightclaw_upload_file 上传并提供下载链接，或用 litterbox 临时链接。

## 常用模板

### 模板 A: 课程笔记长图

```html
<div style="width:1080px; background:#FFFFFF;">
  <!-- 封面区 -->
  <div style="padding:60px; text-align:center; background:linear-gradient(135deg, #2E5C8A 0%, #1D3557 100%);">
    <h1 style="color:#FFFFFF; font-size:56px; margin:0;">${标题}</h1>
    <p style="color:#A8DADC; font-size:28px; margin-top:20px;">${副标题}</p>
  </div>
  
  <!-- 内容区 -->
  <div style="padding:40px 60px;">
    <h2 style="color:#E85D4E; font-size:40px; border-left:8px solid #E85D4E; padding-left:20px;">${章节标题}</h2>
    <div style="color:#1D3557; font-size:28px; line-height:2.0; margin-top:30px;">
      ${正文内容}
    </div>
    <!-- 公式区 -->
    <div style="background:#F1FAEE; padding:30px; border-radius:12px; margin:30px 0;">
      $${LaTeX公式}$
    </div>
  </div>
  
  <!-- 底部信息 -->
  <div style="padding:40px 60px; background:#A8DADC; text-align:center;">
    <span style="color:#1D3557; font-size:24px;">🦞 定积出品</span>
  </div>
</div>
```

### 模板 B: 知识卡片

```html
<div style="width:1080px; min-height:600px; background:#FFFFFF;">
  <div style="padding:50px;">
    <h1 style="color:#E85D4E; font-size:48px;">${核心概念}</h1>
    <div style="color:#1D3557; font-size:28px; line-height:2.0 margin-top:30px;">
      ${解释}
    </div>
    <div style="background:#F4A261; color:#1D3557; padding:30px; border-radius:12px; margin-top:40px;">
      <strong>💡 关键点：</strong>${要点}
    </div>
  </div>
</div>
```

### 模板 C: 代码教程

```html
<div style="width:1080px; background:#1D3557;">
  <div style="padding:40px;">
    <h1 style="color:#FFFFFF; font-size:48px;">${标题}</h1>
    <pre style="background:#2E5C8A; padding:30px; border-radius:12px; overflow-x:auto;">
<code class="language-${语言}" style="color:#F1FAEE; font-size:24px; font-family:'JetBrains Mono', monospace;">
${代码内容}
</code>
    </pre>
  </div>
</div>
```

## 注意事项

1. **高度控制**：单张长图建议不超过 15000px，否则可能导致渲染失败
2. **分块渲染**：超长内容建议分多个 PART 分别渲染后拼接
3. **字体加载**：使用 Google Fonts 需确保网络访问
4. **LaTeX**：复杂公式建议预渲染检查效果
5. **中文排版**：推荐霞鹜文楷 / 思源黑体

## 跨界应用示例

本技能可应用于多个领域：

### 教育领域
- 课程思维导图
- 考试重点笔记
- 知识点速查表

### 读书笔记
- 书籍核心观点总结
- 读书心得整理

### 产品运营
- 功能说明图
- 用户指南
- 活动海报

### 技术文档
- API 说明图
- 架构图解

### 营销素材
- 产品卖点图
- 品牌故事长图