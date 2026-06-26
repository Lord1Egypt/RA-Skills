---
name: md2wechat-skill
version: 1.0.2
description: 将 Markdown 文件转换为微信公众号兼容的内联样式 HTML，并一键发送到微信草稿箱。支持 Front Matter 元数据、表格、代码块、列表、图片自动上传等完整排版能力。
metadata:
  openclaw:
    primaryEnv: WECHAT_APPID
    requires:
      bins:
        - python3
      env:
        - WECHAT_APPID
        - WECHAT_SECRET
    permissions:
      declared_purpose: "将 Markdown 转换为微信兼容 HTML，可选上传到微信公众号草稿箱。写操作包括：保存本地预览 HTML、生成临时封面图到系统 temp 目录"
      network: true
      filesystem: read-write
---

# md2wechat-skill — Markdown 转微信草稿箱

将 Markdown 文件经过排版引擎转换为微信图文编辑器兼容的内联样式 HTML，并通过微信公众号 API 发送到草稿箱。

## 核心能力

- **Markdown → 微信 HTML**：完整解析标准 Markdown 语法（标题、列表、表格、代码块、引用等），自动转换为微信兼容的内联样式
- **Front Matter 元数据**：支持 YAML Front Matter 定义标题、作者、摘要、发布模式等
- **图片自动处理**：正文内嵌的本地图片自动上传到微信 CDN 并替换为永久链接
- **封面图上传**：支持指定封面图上传为微信永久素材
- **代码块深色主题**：代码块自动适配深色背景样式
- **超长内容截断**：超过微信 2MB 限制的内容自动安全截断

## 前置条件

### 依赖安装

```bash
pip install wechatpy markdown beautifulsoup4 requests python-dotenv pillow
```

### 微信公众号配置（仅草稿箱发布需要）

需要设置以下环境变量（可通过 .env 文件或系统环境变量）：

```
WECHAT_APPID=你的公众号AppID
WECHAT_SECRET=你的公众号AppSecret
```

获取方式：登录 [微信公众平台](https://mp.weixin.qq.com/) →「开发」→「基本配置」→ 获取 AppID 和 AppSecret。

配置模板见 `{baseDir}/resources/env_template.txt`。

> **提示**：如果仅需要将 Markdown 转换为微信兼容 HTML（`--convert-only` 模式），则不需要配置微信密钥。

## 使用方式

### 模式一：仅转换 HTML（无需微信密钥）

将 Markdown 文件转换为微信兼容的内联样式 HTML，输出到本地文件：

```bash
python {baseDir}/scripts/md2wechat.py <markdown文件路径> --convert-only --output <输出HTML路径>
```

示例：

```bash
python {baseDir}/scripts/md2wechat.py ./article.md --convert-only --output ./preview.html
```

### 模式二：转换并上传到微信草稿箱

```bash
python {baseDir}/scripts/md2wechat.py <markdown文件路径> --draft --env-file <.env路径>
```

支持的可选参数：
- `--title "自定义标题"`：覆盖自动提取的标题
- `--author "作者名"`：指定作者
- `--cover ./cover.png`：指定封面图
- `--output ./preview_dir/`：同时保存本地预览 HTML
- `--env-file .env`：指定环境变量配置文件

完整示例：

```bash
python {baseDir}/scripts/md2wechat.py ./my_article.md --draft \
    --title "我的文章标题" \
    --cover ./images/cover.png \
    --env-file ./.env \
    --output ./preview/
```

### 查看帮助

```bash
python {baseDir}/scripts/md2wechat.py --help
```

## Markdown 文件格式

### 基本格式

标准的 GitHub Flavored Markdown 语法均受支持：

```markdown
# 文章标题

正文段落...

## 二级标题

- 无序列表项
- 列表项

1. 有序列表项
2. 列表项

> 引用文本

**加粗** 和 *斜体*

| 表头1 | 表头2 |
|-------|-------|
| 单元格 | 单元格 |
```

### Front Matter 元数据（可选）

在文件最顶部添加 YAML 格式的元数据块：

```markdown
---
title: 自定义标题
author: 作者名
summary: 文章摘要描述
publish_mode: draft
---

正文内容...
```

支持的字段：`title`、`author`、`summary`、`cover`、`publish_at`、`publish_mode`、`account_id`

### 图片引用

使用相对路径引用图片，上传草稿时会自动处理：

```markdown
![图片描述](images/photo.png)
```

## 示例文件

示例 Markdown 文章：`{baseDir}/examples/sample_article.md`

## 脚本文件说明

| 文件 | 说明 |
|------|------|
| `scripts/md2wechat.py` | 主入口脚本（CLI） |
| `scripts/md_converter.py` | Markdown → 微信 HTML 转换引擎 |
| `scripts/html_formatter.py` | HTML 内联样式适配器 |
| `scripts/wechat_client.py` | 微信公众号 API 客户端 |

## Rules

1. 在执行 `--draft` 模式前，必须确认用户已正确配置 `WECHAT_APPID` 和 `WECHAT_SECRET`
2. 如果用户只需要转换 HTML 而不需要上传，应使用 `--convert-only` 模式
3. 所有脚本的工作目录应在 `{baseDir}/scripts/` 下执行，以确保模块导入正确
4. 转换生成的 HTML 使用内联样式，不依赖外部 CSS 文件，确保微信兼容性
