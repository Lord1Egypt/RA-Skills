---
name: markdown-sync-pro
description: Markdown 一键同步到 Notion、GitHub Wiki、Medium 等平台
author: openclaw
version: 1.0.0
commands:
  /publish: 将 Markdown 文件发布到指定平台
---

# Markdown Sync Pro — 多平台内容同步工具

一键将 Markdown 内容同步发布到多个平台。

## 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| GitHub Wiki | ✅ | 发布到仓库 Wiki |
| Notion | 📝 | 创建 Notion 页面 |
| Medium | 📝 | 发布文章（需要 API Token） |
| 本地 HTML | ✅ | 导出为 HTML 文件 |

## 使用方法

### 基本用法

```bash
/publish article.md --to github --repo owner/repo
```

### 发布到多个平台

```bash
/publish article.md --to github,notion,medium
```

### 预览转换结果

```bash
/publish article.md --dry-run
```

## 平台配置

### GitHub Wiki

```bash
export GITHUB_TOKEN=your_github_token
/publish article.md --to github --repo username/repo
```

### Notion

```bash
export NOTION_TOKEN=secret_xxx
export NOTION_PARENT_PAGE=page_id
/publish article.md --to notion
```

### Medium

```bash
export MEDIUM_TOKEN=your_medium_token
/publish article.md --to medium
```

## Markdown 转换支持

- ✅ 标准 Markdown 语法
- ✅ 代码块高亮
- ✅ 表格
- ✅ 图片（自动上传图床）
- ✅ Frontmatter 元数据

## 示例

```bash
# 发布到 GitHub Wiki
/publish docs/guide.md --to github --repo myorg/project

# 发布到 Notion 并设置标题
/publish blog/post.md --to notion --title "我的文章"

# 导出为 HTML
/publish article.md --to html --output ./dist/
```
