# AI Newspaper Renderer Skill

## 工具描述

AI 报纸渲染服务 - 将结构化新闻内容渲染成仿实体报纸风格的 HTML 页面。支持 ComfyUI AI 图片生成。

**服务地址**: `http://localhost:3000`

## API 端点

### POST /render

渲染报纸 HTML。

**请求格式**:
```
POST http://localhost:3000/render
Content-Type: application/json
```

**请求参数**:
```json
{
  "title": "string (必需) - 报纸标题",
  "subtitle": "string (可选) - 副标题",
  "articles": [
    {
      "headline": "string (必需) - 文章标题",
      "body": "string (必需) - 文章正文，用\\n\\n分隔段落",
      "imagePrompt": "string (可选) - AI 绘画提示词，最多 1 个"
    }
  ],
  "comfyOptions": {
    "enabled": "boolean (可选，默认 true)",
    "timeout": "number (可选，默认 120000ms)",
    "interval": "number (可选，默认 2000ms)",
    "width": "number (可选，默认 1024)",
    "height": "number (可选，默认 1024)"
  }
}
```

**成功响应**:
```json
{
  "success": true,
  "id": "生成的唯一 ID",
  "url": "http://localhost:3000/output/{id}.html",
  "imageStatus": {
    "generated": "是否生成图片",
    "prompt": "使用的提示词",
    "imageUrl": "ComfyUI 图片地址",
    "articleIndex": "图片所在文章索引",
    "error": "错误信息（如有）"
  }
}
```

**错误响应**:
```json
{
  "success": false,
  "errors": ["错误列表"]
}
```

## 使用规则

### 输入验证
- `title`: 必需，非空字符串
- `articles`: 必需，至少包含 1 篇文章
- 每篇文章必须有 `headline` 和 `body`
- `imagePrompt`: 最多只能有 1 个（单图限制）

### 内容组织策略

**头条文章**（articles[0]）:
- 跨栏显示，最重要内容
- 建议放置 imagePrompt（如有）
- 正文建议 300-800 字

**普通文章**:
- 次要新闻
- 正文建议 100-500 字
- 不需要 imagePrompt

### 正文格式
- 使用 `\n\n` 分隔段落
- 每段 50-200 字为宜
- 首段不缩进，后续段落缩进

### 图片提示词指南
- 使用英文描述
- 具体详细，包含主体 + 环境 + 风格
- 示例：`"A futuristic AI robot scientist in high-tech laboratory, holographic displays, blue lighting, digital art"`

## 调用示例

```javascript
const response = await fetch('http://localhost:3000/render', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        title: "科技日报",
        subtitle: "前沿科技资讯",
        articles: [
            {
                headline: "AI 大模型迎来重大突破",
                body: "今日发布最新 AI 模型...\n\n研究团队表示...",
                imagePrompt: "A futuristic AI robot scientist, digital art"
            },
            {
                headline: "量子计算进展",
                body: "科学家实现新突破..."
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

## ComfyUI 集成

### 服务地址
- ComfyUI 服务地址：`http://127.0.0.1:8000`
- 提交任务：`{COMFY_BASE_URL}/prompt`
- 查看图片：`{COMFY_VIEW_URL}/view`

### 环境变量配置
```bash
# 可选：自定义 ComfyUI 地址
export COMFY_BASE_URL="http://127.0.0.1:8000"
export COMFY_VIEW_URL="http://127.0.0.1:8000"
```

### 图片生成流程
1. 检测 `imagePrompt` 字段
2. 提交任务到 ComfyUI
3. 轮询 `/history/{prompt_id}` 直到完成
4. 提取图片 URL 嵌入 HTML

### 降级策略
- ComfyUI 不可用时，使用占位图继续渲染
- 生成超时/失败时，不中断渲染流程

## 输出布局

- **4 栏布局**（大屏幕）
- **3 栏布局**（中等屏幕）
- **2 栏布局**（小屏幕）
- **1 栏布局**（手机）

### 样式特点
- 仿实体报纸风格
- 宋体/楷体/黑体中文字体
- 栏线分隔
- 头条图文并排
- 普通文章图片环绕

## 健康检查

```
GET http://localhost:3000/health
```

响应：`{ "status": "ok", "timestamp": "..." }`

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 缺少 title | 未提供标题 | 从内容提取或询问用户 |
| articles 为空 | 没有文章 | 确保至少 1 篇 |
| 多个 imagePrompt | 违反单图限制 | 只保留 1 个 |
| ComfyUI 超时 | 生成时间长 | 增加 comfyOptions.timeout |
| ComfyUI 不可用 | 服务未启动 | 检查 ComfyUI 或使用占位图 |

### 安全提示
- 日志仅记录标题和文章数量，不记录完整内容
- 避免在 body 中传递敏感信息
- 渲染的 HTML 会引用 ComfyUI 返回的图片 URL

## AI 规划流程

1. **分析需求** → 确定报纸主题
2. **收集内容** → 生成或整理文章
3. **判断配图** → 生成 1 个英文 imagePrompt
4. **组织内容** → 头条放最重要内容 + 图片
5. **调用 API** → POST /render
6. **返回结果** → 提供 URL 和图片状态