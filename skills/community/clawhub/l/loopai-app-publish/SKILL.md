---
name: loopai-app-publish
description: 用于将应用信息（名称、链接、截图、作者、社区等）提交到 App Hub 展示中心。支持创建新的 AI 应用、软件或工具的展示页面。也适用于生成和发布 Loop App、Loop 小程序、Loop 网站、Loop 应用等场景。提交前会自动通过 curl 验证 app_url 是否可访问，不可访问则拒绝提交并提示用户修正。
---

# LoopAI App Publish

## Overview

创建并发布应用到 App Hub 展示中心。通过调用 API 将应用信息提交到平台，包括应用名称、URL、描述、截图、作者信息、定价模式和关联社区等。

**重要：** 提交前脚本会自动使用 `curl` 验证 `app_url` 是否能正常访问（支持跟随重定向，超时10秒）。如果 URL 不可达，将拒绝提交并返回错误提示。

## When to Use This Skill

使用此技能当用户需要：
- 分享新开发的 AI 应用或工具
- 发布软件到应用展示中心
- 更新应用信息（截图、描述等）
- 在多社区场景下展示应用
- 生成或发布 Loop App
- 创建 Loop 小程序
- 搭建 Loop 网站
- 发布 Loop 应用

## Prerequisites

- 需要有效的 App Hub API 访问权限
- 应用信息必须完整（名称、URL、描述、作者）
- 截图 URL 必须有效且可公开访问
- 建议准备应用图标（可选但推荐）

## Core Capabilities

### 1. 创建应用展示

提交新应用到 App Hub：

```bash
python scripts/create_app.py --app-name "应用名称" --app-url "https://example.com" --description "应用描述" --author-name "作者名"
```

**必填参数：**
- `--app-name` - 应用正式名称
- `--app-url` - 应用访问网址
- `--description` - 功能详细描述
- `--author-name` - 作者姓名

**可选参数：**
- `--icon` - 应用图标 URL
- `--screenshot` - 截图 URL（可重复添加多个）
- `--author-avatar` - 作者头像链接
- `--author-url` - 作者个人主页
- `--price-mode` - 计费模式：0=免费，1=付费（默认 0）
- `--price` - 价格（默认 "0"）
- `--visibility` - 可见性：0=公开，1=私有（默认 0）
- `--community-name` - 社区名称（可重复添加多个）
- `--community-avatar` - 社区头像链接
- `--community-url` - 社区链接

**示例：**
```bash
# 基础提交
python scripts/create_app.py \
  --app-name "My AI Assistant" \
  --app-url "https://myai.example.com" \
  --description "一个智能 AI 助手，帮助用户处理日常任务" \
  --author-name "John Doe"

# 完整提交（含截图和多社区）
python scripts/create_app.py \
  --app-name "Smart ChatBot" \
  --app-url "https://smartchat.example.com" \
  --description "基于最新 LLM 的智能对话系统" \
  --author-name "Jane Smith" \
  --author-avatar "https://example.com/avatar.jpg" \
  --author-url "https://jane.example.com" \
  --icon "https://example.com/icon.png" \
  --screenshot "https://example.com/screenshot1.png" \
  --screenshot "https://example.com/screenshot2.png" \
  --price-mode 0 \
  --visibility 0 \
  --community-name "OpenAI Community" \
  --community-avatar "https://example.com/community-avatar.png" \
  --community-url "https://community.example.com"
```

### 2. 查看应用详情

获取指定 App Hub 应用的详细信息：

```bash
python scripts/create_app.py --get-detail --app-id "应用ID"
```

**参数：**
- `--app-id` - 应用唯一标识（从创建结果或列表中获取）

**示例：**
```bash
python scripts/create_app.py --get-detail --app-id "797fe6a6-fc43-4001-92c6-6f06e12b5fd9"
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "app_id": "797fe6a6-fc43-4001-92c6-6f06e12b5fd9",
    "app_name": "Test AI Assistant",
    "app_url": "https://test-ai.example.com",
    "description": "一个测试用的 AI 助手应用",
    "icon": "https://example.com/icon.png",
    "screenshots": [...],
    "author": [...],
    "price_mode": 0,
    "price": "0",
    "visibility": 0,
    "communities": [...],
    "created_at": "2025-03-24T03:18:31Z"
  }
}
```

### 3. 更新应用信息

修改已创建应用的详细信息：

```bash
python scripts/create_app.py --update --app-id "应用ID" --app-name "新名称" --description "新描述" ...
```

**必填参数：**
- `--app-id` - 要更新的应用 ID

**可选参数（只提供需要修改的字段）：**
- `--app-name` - 新的应用名称
- `--app-url` - 新的应用 URL
- `--description` - 新的应用描述
- `--icon` - 新的应用图标
- `--screenshot` - 新的截图（会替换原有截图列表）
- `--author-name` - 作者名称（需要同时提供 --author-avatar 和 --author-url 才会更新）
- `--author-avatar` - 作者头像
- `--author-url` - 作者主页
- `--price-mode` - 计费模式
- `--price` - 价格
- `--visibility` - 可见性
- `--add-screenshot` - 添加截图（不覆盖）
- `--remove-screenshot` - 删除指定索引的截图（从0开始）
- `--community-name` - 社区名称（添加或更新，需配合其他参数）
- `--community-avatar` - 社区头像
- `--community-url` - 社区链接

**示例：**
```bash
# 仅更新名称和描述
python scripts/create_app.py \
  --update \
  --app-id "797fe6a6-fc43-4001-92c6-6f06e12b5fd9" \
  --app-name "Super AI Assistant" \
  --description "更强大的 AI 助手，支持多语言和多种任务"

# 添加截图（不覆盖）
python scripts/create_app.py \
  --update \
  --app-id "797fe6a6-fc43-4001-92c6-6f06e12b5fd9" \
  --add-screenshot "https://example.com/new-ss.png"

# 删除第一个截图（索引0）
python scripts/create_app.py \
  --update \
  --app-id "797fe6a6-fc43-4001-92c6-6f06e12b5fd9" \
  --remove-screenshot 0

# 完整更新作者信息
python scripts/create_app.py \
  --update \
  --app-id "797fe6a6-fc43-4001-92c6-6f06e12b5fd9" \
  --author-name "Jane Doe" \
  --author-avatar "https://example.com/new-avatar.jpg" \
  --author-url "https://jane.example.com"
```

### 4. 批量创建（JSON 输入）

支持通过 JSON 文件批量创建：

```bash
python scripts/create_app.py --json-file apps.json
```

JSON 文件格式：
```json
[
  {
    "app_name": "App 1",
    "app_url": "https://app1.example.com",
    "description": "描述...",
    "author": [
      {
        "name": "Author Name"
      }
    ],
    "icon": "https://example.com/icon.png",
    "screenshots": [
      "https://example.com/ss1.png"
    ],
    "price_mode": 0,
    "price": "0",
    "visibility": 0,
    "communities": []
  }
]
```

### 3. 验证应用信息

在提交前验证数据完整性：

```bash
python scripts/create_app.py --validate-only --app-name "Test" --app-url "https://test.com" --description "desc" --author-name "Author"
```

该命令只验证参数，不实际提交。

## Input Schema (参数定义)

```json
{
  "type": "object",
  "properties": {
    "app_name": {
      "type": "string",
      "description": "应用的正式名称"
    },
    "app_url": {
      "type": "string",
      "description": "应用的访问网址 (URL)"
    },
    "icon": {
      "type": "string",
      "description": "应用图标的图片链接"
    },
    "description": {
      "type": "string",
      "description": "应用的功能详细描述"
    },
    "screenshots": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "应用界面的截图 URL 数组"
    },
    "author": {
      "type": "array",
      "description": "作者信息列表",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "作者姓名"
          },
          "avatar": {
            "type": "string",
            "description": "作者头像链接"
          },
          "url": {
            "type": "string",
            "description": "作者个人主页或社交链接"
          }
        },
        "required": ["name"]
      }
    },
    "price_mode": {
      "type": "integer",
      "description": "计费模式：0 代表免费, 1 代表付费",
      "default": 0
    },
    "price": {
      "type": "string",
      "description": "价格数值字符串，免费填 '0'",
      "default": "0"
    },
    "visibility": {
      "type": "integer",
      "description": "可见性设置：0 代表公开, 1 代表私有",
      "default": 0
    },
    "communities": {
      "type": "array",
      "description": "关联的社区或公司信息",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "avatar": {
            "type": "string"
          },
          "url": {
            "type": "string"
          }
        }
      }
    }
  },
  "required": ["app_name", "app_url", "description", "author"]
}
```

## Implementation

脚本位置：`scripts/create_app.py`

**主要功能：**
1. 解析命令行参数或 JSON 输入
2. 验证必填字段
3. 构造符合 Schema 的请求体
4. 支持三种 API 操作：
   - `POST /api/app_hub/create` - 创建新应用
   - `GET /api/app_hub/detail/:id` - 查询应用详情
   - `POST /api/app_hub/update` - 更新应用信息
5. 处理响应并输出结果

### API 端点详情

#### 1. 创建应用
- **URL**: `POST /api/app_hub/create`
- **Content-Type**: `application/json`
- **Headers**: `Token: <token>`

#### 2. 查询详情
- **URL**: `GET /api/app_hub/detail/:id`
- **Headers**: `Token: <token>`
- **Response**: 完整的应用信息 JSON

#### 3. 更新应用
- **URL**: `POST /api/app_hub/update`
- **Headers**: `Token: <token>`
- **Body**: 包含 `app_id` 和需要更新的字段（部分更新）

**成功响应示例：**
```json
{
  "code": 0,
  "msg": "",
  "data": {
    "app_id": "app_123456",
    "app_key": "key_xxx"
  },
  "time": 1774320855
}
```

**查询详情响应示例：**
```json
{
  "code": 0,
  "data": {
    "app_id": "app_123456",
    "app_name": "My App",
    "app_url": "https://example.com",
    "description": "...",
    ...
  }
}
```

**错误处理：**
- 参数缺失 → 显示错误信息
- API 调用失败 → 显示错误详情
- 网络异常 → 提示重试
- 权限不足 → 检查 token 和 app_id 归属

---

## Full Command Reference

### 创建应用

## Best Practices

1. **信息完整** - 尽可能提供完整信息（截图、图标、作者主页）
2. **截图质量** - 使用清晰、高分辨率的截图
3. **描述清晰** - 描述应准确反映应用功能
4. **价格准确** - 免费应用填 0，付费应用填具体金额
5. **验证前置** - 提交前先运行 `--validate-only` 检查
6. **社区关联** - 如果应用属于某个社区，务必关联

## Troubleshooting

**常见问题：**

- **"Missing required field"** - 检查必填参数是否齐全
- **"Invalid URL"** - 确保 URL 格式正确（包含 http:// 或 https://）
- **"API Error 403"** - API 密钥无效或权限不足
- **"Screenshot URL unreachable"** - 截图 URL 必须公开可访问
- **"Duplicate app"** - 相同 app_url 可能已存在

**调试模式：**
添加 `--verbose` 查看详细日志：
```bash
python scripts/create_app.py ... --verbose
```

## Resources

- **API 文档**: `/api/app_hub/create`
- **输入 Schema**: 见上方 JSON Schema
- **脚本**: `scripts/create_app.py`
- **示例**: `examples/` 目录（如果存在）

## Notes

- 应用创建后可能需要审核才能公开显示
- 可随时通过 App Hub 管理界面编辑应用信息
- 删除应用需通过管理接口或联系管理员