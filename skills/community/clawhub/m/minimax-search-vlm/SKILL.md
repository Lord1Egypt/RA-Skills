---
name: minimax-mcp
description: "使用 MiniMax Coding Plan API 进行网络搜索和图片理解。使用场景：(1) 用户需要搜索实时信息或新闻，(2) 需要分析图片内容，(3) 做研究或查找资料。无需 API key：用户需自行配置。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl"] },
        "install": [
          {
            "id": "config",
            "kind": "manual",
            "label": "配置 MiniMax API Key",
            "steps": [
              "创建配置文件: echo 'MINIMAX_API_KEY=你的API密钥' > ~/.openclaw/config/minimax-api.env",
              "设置权限: chmod 600 ~/.openclaw/config/minimax-api.env"
            ]
          }
        ]
      }
  }
---

# MiniMax MCP Skill

使用 MiniMax Coding Plan API 进行网络搜索和图片理解。

## 何时使用

✅ **使用这个 skill 当：**

- 用户需要搜索实时信息（新闻、科技动态等）
- 需要分析图片内容（描述图片、提取信息）
- 做研究、查找资料
- 用户问"今天有什么科技新闻"

❌ **不要使用这个 skill 当：**

- 本地文件操作 → 使用 `exec` 或 `read` 工具
- 简单的计算或文本处理 → 直接处理
- 需要登录认证的搜索 → 使用其他方式

## 配置步骤（用户需先完成）

首次使用需要配置 API Key，只需执行一次：

```bash
# 创建配置目录（如不存在）
mkdir -p ~/.openclaw/config

# 添加 API Key（替换为你自己的 key）
echo 'MINIMAX_API_KEY=你的API密钥' > ~/.openclaw/config/minimax-api.env

# 设置安全权限
chmod 600 ~/.openclaw/config/minimax-api.env
```

> API Key 需要从 MiniMax 开发者平台获取：https://platform.minimaxi.com

## 功能

### 1. 网络搜索

搜索网络获取实时信息。

```bash
# 加载 API Key
source ~/.openclaw/config/minimax-api.env

# 搜索示例
curl -s "https://api.minimaxi.com/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"今天科技新闻"}'
```

### 2. 图片理解

分析图片内容，支持本地文件或网络图片。

```bash
# 加载 API Key
source ~/.openclaw/config/minimax-api.env

# 分析本地图片
IMG_PATH="/path/to/image.jpg"
curl -s "https://api.minimaxi.com/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"描述这张图片\",\"image_url\":\"data:image/jpeg;base64,$(base64 -w0 $IMG_PATH)\"}"
```

**支持格式**: JPEG, PNG, GIF, WebP（最大 20MB）

## 快速命令

### 搜索并美化输出

```bash
source ~/.openclaw/config/minimax-api.env
curl -s "https://api.minimaxi.com/v1/coding_plan/search" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"关键词"}' | python3 -c "
import json,sys
data = json.load(sys.stdin)
for r in data.get('organic',[])[:5]:
    print(f'• {r[\"title\"]}')
    print(f'  {r[\"link\"]}\n')
"
```

### 下载网络图片后分析

```bash
source ~/.openclaw/config/minimax-api.env
curl -s "https://example.com/image.jpg" -o /tmp/tmp_img.jpg
curl -s "https://api.minimaxi.com/v1/coding_plan/vlm" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"描述这张图片\",\"image_url\":\"data:image/jpeg;base64,$(base64 -w0 /tmp/tmp_img.jpg)\"}"
```

## 注意事项

- API Key 保存在用户本地配置文件中，不会随 skill 发布
- 请勿在命令输出或日志中暴露 API Key
- 搜索 API 有频率限制，避免短时间内大量请求
