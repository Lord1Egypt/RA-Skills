# AI Newspaper Renderer - Agent 调用指南

## 服务概述

这是一个 AI 报纸渲染服务，接收结构化的新闻内容 JSON，返回报纸风格的 HTML 页面 URL。

**新增功能**：支持 ComfyUI 图片生成，可将文章中的 `imagePrompt` 转换为真实图片并嵌入报纸。

---

## API 端点

```
POST http://localhost:3000/render
```

---

## 请求参数结构

### 完整 JSON Schema

```json
{
  "type": "object",
  "required": ["title", "articles"],
  "properties": {
    "title": {
      "type": "string",
      "description": "报纸标题，显示在报头位置，跨栏展示",
      "maxLength": 50
    },
    "subtitle": {
      "type": "string",
      "description": "报纸副标题（可选），显示在标题下方",
      "maxLength": 100
    },
    "articles": {
      "type": "array",
      "description": "文章列表，至少包含一篇文章",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["headline", "body"],
        "properties": {
          "headline": {
            "type": "string",
            "description": "文章标题",
            "maxLength": 100
          },
          "body": {
            "type": "string",
            "description": "文章正文，使用双换行符 \\n\\n 分隔段落",
            "minLength": 1
          },
          "imagePrompt": {
            "type": "string",
            "description": "AI 绘画提示词（可选，最多 1 个），用于 ComfyUI 生成图片",
            "maxLength": 500
          }
        }
      }
    },
    "comfyOptions": {
      "type": "object",
      "description": "ComfyUI 图片生成配置（可选）",
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "是否启用 ComfyUI，默认 true"
        },
        "timeout": {
          "type": "number",
          "description": "超时时间（毫秒），默认 120000"
        },
        "interval": {
          "type": "number",
          "description": "轮询间隔（毫秒），默认 2000"
        },
        "width": {
          "type": "number",
          "description": "图片宽度（像素），默认 1024"
        },
        "height": {
          "type": "number",
          "description": "图片高度（像素），默认 1024"
        }
      }
    }
  }
}
```

---

## 响应结构

### 成功响应 (200)

```json
{
  "success": true,
  "id": "abc123xyz",
  "url": "http://localhost:3000/output/abc123xyz.html",
  "imageStatus": {
    "generated": true,
    "prompt": "a cute hedgehog wearing a hat",
    "imageUrl": "http://127.0.0.1:8000/view?filename=...",
    "articleIndex": 0,
    "error": null
  }
}
```

### 错误响应 (400)

```json
{
  "success": false,
  "errors": [
    "缺少必需的 title 字段",
    "最多只能有 1 个 article 包含 imagePrompt（单图限制）"
  ]
}
```

---

## Agent 规划指南

### 第一步：内容收集与结构化

当用户要求生成报纸时，Agent 应该：

1. **确定报纸主题** - 从用户需求中提取或询问
2. **收集文章内容** - 可以是用户提供的或 AI 生成的资讯
3. **判断是否需要配图** - 如果有图片需求，生成 1 个英文提示词

### 第二步：图片提示词编写指南

**重要限制**：每次请求最多只能有 1 个 `imagePrompt`！

#### 好的提示词特征：
- 使用英文描述
- 具体、详细
- 包含主体、动作、环境、风格等元素

#### 示例：

```
✅ 好的示例：
"A futuristic AI laboratory with robots working on computers, 
 blue and white color scheme, highly detailed, digital art style"

❌ 坏的示例：
"一个机器人"  // 太简单
"很多图片，这个那个"  // 不具体
```

### 第三步：内容组织策略

```
推荐的文章结构：

文章 1（头条）：
  - 最重要/最吸引人的新闻
  - 正文较长（300-800 字）
  - 如果有 imagePrompt，放在这里

文章 2-N（普通文章）：
  - 次要新闻或相关报道
  - 正文适中（100-500 字）
  - 不需要 imagePrompt
```

### 第四步：正文格式化

**重要：** 正文内容应该：
- 使用 `\n\n`（双换行）分隔段落
- 每段保持适当长度（50-200 字）
- 避免过长的单一段落

### 第五步：调用 API

```javascript
const response = await fetch('http://localhost:3000/render', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: "科技日报",
        subtitle: "前沿科技资讯",
        articles: [
            {
                headline: "AI 绘画新突破",
                body: "今日发布的最新 AI 绘画模型...\n\n该模型能够...",
                imagePrompt: "A futuristic AI art studio with robots painting, digital art, vibrant colors"
            },
            {
                headline: "量子计算进展",
                body: "科学家实现新突破..."
                // 没有 imagePrompt
            }
        ],
        comfyOptions: {
            enabled: true,
            timeout: 120000,
            interval: 2000,
            width: 1024,
            height: 512
        }
    })
});

const result = await response.json();
// result.url 为报纸页面地址
// result.imageStatus 包含图片生成状态
```

### 第六步：结果呈现

调用成功后，Agent 应该：

1. **返回完整 URL** - 用户可点击访问
2. **说明图片状态** - 告知是否成功生成图片
3. **提供后续选项** - 如需要修改可重新生成

---

## 完整调用示例

### 示例 1：带 AI 生成图片的日报

```json
{
  "title": "科技日报",
  "subtitle": "聚焦前沿科技动态",
  "articles": [
    {
      "headline": "AI 大模型迎来重大突破",
      "body": "今日，多家科技公司联合发布了新一代人工智能大模型。该模型在视觉理解、语言生成、逻辑推理等多个维度取得了突破性进展。\n\n研究团队表示，新模型采用了创新的架构设计，能够更高效地处理跨模态任务。在基准测试中，其表现超越了现有所有模型。\n\n业内专家认为，这一突破将加速 AI 技术在各行业的应用落地。",
      "imagePrompt": "A futuristic AI robot scientist working in a high-tech laboratory, holographic displays, blue and purple lighting, highly detailed digital art"
    },
    {
      "headline": "量子计算机商业化进程加速",
      "body": "多家初创公司宣布推出面向企业的量子计算云服务，标志着量子计算正从实验室走向商业应用。"
    },
    {
      "headline": "全球科技公司竞相布局元宇宙",
      "body": "随着 VR/AR 技术的成熟，科技巨头们纷纷加大在元宇宙领域的投入。"
    }
  ],
  "comfyOptions": {
    "enabled": true,
    "timeout": 120000,
    "interval": 2000
  }
}
```

---

## 注意事项

### 单图限制
1. **必须字段**：`title` 和 `articles` 数组必不可少
2. **文章数量**：至少 1 篇，建议 3-6 篇以获得最佳排版效果
3. **单图原则**：最多只能有 1 个 `imagePrompt`，否则返回错误
4. **头条优势**：第一篇文章会跨栏显示，建议将图片放在头条

### ComfyUI 依赖
- ComfyUI 服务地址：`http://127.0.0.1:8000`（提交任务和查看图片）
- 可通过环境变量自定义：
  - `COMFY_BASE_URL` - ComfyUI API 地址
  - `COMFY_VIEW_URL` - 图片查看地址
- 如果 ComfyUI 不可用，将使用占位图继续渲染

### 提示词编写
- 使用英文
- 描述具体场景
- 可包含风格关键词：`digital art`, `photorealistic`, `anime style` 等

---

## 错误处理

Agent 应该处理以下常见错误：

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 缺少 title | 未提供标题 | 从内容中提取或请用户提供 |
| articles 为空 | 没有文章内容 | 确保至少生成一篇文章 |
| 多个 imagePrompt | 违反单图限制 | 只保留最重要的 1 个 |
| ComfyUI 超时 | 生成时间过长 | 增加 timeout 或检查 ComfyUI 状态 |
| ComfyUI 不可用 | 服务未启动 | 使用占位图继续渲染 |

---

## 健康检查

调用主接口前可先检查服务状态：

```
GET http://localhost:3000/health
```

响应：
```json
{ "status": "ok", "timestamp": "2026-03-30T..." }
```

---

## 服务信息

- **服务端口**：3000（报纸渲染服务）
- **ComfyUI 端口**：8000（AI 图片生成）
- **输出目录**：`./output/`
- **文件格式**：HTML5
- **布局**：4 栏报纸风格（响应式）
- **字体**：宋体/楷体/黑体
- **环境变量**：
  - `COMFY_BASE_URL` - ComfyUI API 地址（默认 http://127.0.0.1:8000）
  - `COMFY_VIEW_URL` - 图片查看地址（默认 http://127.0.0.1:8000）

---

## Agent 快速参考

```
📋 输入检查清单：
□ title 存在且非空
□ articles 数组至少 1 篇
□ 每篇有 headline 和 body
□ imagePrompt 最多 1 个（如有）

🎨 图片提示词指南：
□ 使用英文
□ 描述具体
□ 包含主体 + 环境 + 风格
□ 放在最重要的文章上

📞 API 调用：
POST /render
Content-Type: application/json
Body: { title, articles, comfyOptions }

✅ 成功响应：
{ success: true, url, imageStatus }