---
name: google-docs-to-feishu
description: |
  将 Google Docs 文档内容同步/复制到飞书文档。支持手动触发全自动转换。
  当用户提到 Google Docs 转飞书、Google 文档同步、复制文档到飞书时激活。
---

# Google Docs → 飞书文档 同步工具

## 功能概述

- Google Docs 文档 → 飞书文档全自动转换
- 支持标题、段落、列表、表格、图片
- 手动触发，无需定时

## 凭证配置

首次使用需要配置 Google OAuth，步骤如下：

### 1. 创建 Google Cloud 项目

访问 https://console.cloud.google.com，创建项目后：

1. 启用 **Google Docs API**
2. 创建 **OAuth 2.0 Client ID**（桌面应用类型）
3. 下载 JSON 文件，保存为 `~/.config/google-docs-to-feishu/credentials.json`

### 2. 授权

首次运行会自动打开浏览器进行授权，或手动访问授权 URL 完成授权。

### 3. 凭证存放位置

```
~/.config/google-docs-to-feishu/
├── credentials.json    # OAuth 客户端信息
├── token.json          # 访问令牌（自动生成）
```

## 使用方法

### 同步 Google Docs 到飞书

提供 Google Docs 链接和飞书文件夹 token：

```json
{
  "action": "sync",
  "google_doc_url": "https://docs.google.com/document/d/XXXXXXXXXXXXXXXXXXXXXXXX/edit",
  "feishu_folder_token": "fldcnXXXXXXXXXXXXXX"
}
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `google_doc_url` | ✅ | Google Docs 链接 |
| `feishu_folder_token` | ❌ | 飞书文件夹 token，不填则创建在根目录 |
| `feishu_owner_open_id` | ❌ | 飞书用户 open_id，用于授予文档访问权限 |

### 返回

- 飞书文档链接
- 文档标题
- 同步状态

### 完整流程说明

1. **读取 Google Docs** — 通过 Google Docs API 获取文档 blocks 结构
2. **格式转换** — 将 Google Docs block 转换为 Markdown
3. **创建飞书文档** — 在指定文件夹创建文档
4. **写入内容** — 通过 feishu-doc 写入 Markdown 内容

## 权限要求

### Google 侧
- Google Docs API
- OAuth 2.0 授权（read only）

### 飞书侧
- feishu-doc skill（已配置）

## 注意事项

- 表格图片等复杂格式可能存在少量格式差异
- 首次授权需要人工操作，后续可自动续期
