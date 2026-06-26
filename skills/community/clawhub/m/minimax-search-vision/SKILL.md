---
name: minimax-tools
description: MiniMax 网络搜索和图片理解工具。当用户需要搜索信息或理解图片内容时使用此技能。支持通过 MiniMax Token Plan MCP 进行网络搜索和图片分析。
homepage: https://platform.minimaxi.com
tags:
  - minimax
  - search
  - web-search
  - image-understanding
  - vision
  - mcp
version: 1.0.0
---

# MiniMax Tools 技能

MiniMax Token Plan 提供的网络搜索和图片理解工具封装。

## 触发条件

当用户请求以下操作时激活：
- "搜索..."
- "在网上查找..."
- "这张图片是什么"
- "分析这张图片"
- "解释这个图片"
- "MiniMax 搜索"
- "用 MiniMax 搜索"

## 工具说明

### web_search

网络搜索工具，根据查询词返回搜索结果。

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| query | string | ✓ | 搜索查询词 |

**输出格式：**
```json
{
  "results": [
    {"title": "标题", "url": "链接", "snippet": "摘要"},
    ...
  ],
  "related_searches": ["相关搜索词1", "相关搜索词2"]
}
```

### understand_image

图片理解工具，对图片进行分析和理解。

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| prompt | string | ✓ | 对图片的提问或分析要求 |
| image_url | string | ✓ | 图片地址（HTTP/HTTPS URL 或本地文件路径）|

**支持格式：** JPEG, PNG, GIF, WebP（最大 20MB）

## 安全规范

✅ **必须遵守：**
- API Key 从环境变量或凭据文件读取，绝不硬编码
- 凭据文件路径：`~/.openclaw/credentials/minimax_mcp.env`
- 输出时对 API Key 进行脱敏（如 `sk-cp-rOHr...****`）

❌ **禁止：**
- 在代码或输出中明文显示 API Key
- 将凭据信息写入日志

## 依赖

此技能依赖 `mcporter` 工具来调用 MiniMax Token Plan MCP 服务。

**mcporter 安装：**
```bash
npm install -g mcporter
```

**MiniMax MCP 配置：**
```bash
mcporter config add MiniMax \
    --command uvx \
    --args "minimax-coding-plan-mcp -y" \
    --env MINIMAX_API_KEY=$MINIMAX_API_KEY \
    --env MINIMAX_API_HOST=https://api.minimaxi.com \
    --scope home
```

## 错误处理

| 错误类型 | 说明 | 处理方式 |
|---------|------|---------|
| ConnectionError | MCP 服务离线 | 提示用户检查 mcporter 配置 |
| TimeoutError | 请求超时 | 建议重试或使用更小的图片 |
| ValueError | 参数无效 | 提示正确的参数格式 |

## 示例

**网络搜索：**
```
用户: 搜索 Python 教程
助手: 调用 web_search("Python 教程")
返回搜索结果列表
```

**图片理解：**
```
用户: 分析这张图片 https://example.com/diagram.png
助手: 调用 understand_image("描述这张图片的内容", "https://example.com/diagram.png")
返回图片分析结果
```

## 维护日志

- 2026-03-22 v1.0.0: 初始版本，支持 web_search 和 understand_image
