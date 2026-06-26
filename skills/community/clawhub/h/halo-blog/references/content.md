# Halo CLI 内容管理 — 文章与独立页面

> 对应命令：`halo post` 和 `halo single-page`

## 文章发布格式规范

发布文章前请先阅读 [publishing.md](publishing.md)，了解 Markdown → HTML 的默认流程、front matter 规范、可见性检查和验证方法。

---

## 文章（Post）

### 列表与查看

```bash
halo post list
halo post list --keyword halo --publish-phase PUBLISHED
halo post get my-post --json
halo post open my-post              # 在浏览器打开已发布文章
```

### 创建与更新

**推荐：从 Markdown 文件导入（格式最可靠）**

```bash
halo post import-markdown --file ./article.md --force
```

Markdown 文件可包含 YAML front matter：

```markdown
---
title: "文章标题"
slug: "post-slug"
---

# 正文内容

正文支持 Markdown。
```

**直接命令行创建（仅适合简短内容）**

```bash
halo post create --title "Hello Halo" --content "短内容" --publish true
```

注意：在 shell 中 `--content` 里的 `\n` 会被当成字面量，不会变成真正的换行符。长内容或需要格式时，**务必使用 `import-markdown`**。

```bash
halo post update my-post --title "Updated title"
halo post update my-post --content "Updated content" --publish true
halo post update my-post --new-name my-post-renamed
```

### 分类与标签

```bash
halo post category list
halo post category create --display-name "Technology" --slug "tech"
halo post category update category-abc123 --display-name "Tech News"
halo post category delete category-abc123 --force

halo post tag list
halo post tag create --display-name "Halo" --slug "halo" --color "#1890ff"
halo post tag update tag-abc123 --display-name "Halo CMS"
halo post tag delete tag-abc123 --force
```

创建/更新文章时可直接指定分类和标签（逗号分隔）：

```bash
halo post create \
  --title "Release Notes" \
  --content "..." \
  --categories News,CLI \
  --tags Halo,Release
```

### 导入导出

**JSON：**

```bash
halo post export-json my-post --output ./post.json
halo post import-json --file ./post.json --force
halo post import-json --raw '{"post":...,"content":...}'
```

**Markdown：**

```bash
halo post export-markdown my-post --output ./post.md
halo post import-markdown --file ./post.md --force
```

### 删除

```bash
halo post delete my-post --force
```

## 独立页面（Single Page）

命令结构与文章类似，但命令名为 `single-page`：

```bash
halo single-page list
halo single-page get about --json
halo single-page create --title "About" --content "# About" --publish true
halo single-page update about --title "About Halo"
halo single-page update about --new-name about-page
halo single-page export-json about --output ./about.json
halo single-page import-json --file ./about.json --force
halo single-page delete about --force
```

注意：独立页面**不支持** `--pinned` 选项，也没有 category/tag 子命令。

## 常用字段说明

| 选项 | 说明 |
|------|------|
| `--title` | 标题 |
| `--content` | 内容（默认按 Markdown 解析） |
| `--raw-type` | `markdown`（默认）或 `html` |
| `--slug` | 别名/URL 片段 |
| `--excerpt` | 摘要 |
| `--cover <url>` | 封面图 |
| `--template <name>` | 模板 |
| `--visible` | `PUBLIC` / `INTERNAL` / `PRIVATE` |
| `--publish true\|false` | 是否发布 |
| `--pinned true\|false` | 是否置顶（仅文章） |
| `--allow-comment true\|false` | 是否允许评论 |
| `--priority <number>` | 优先级 |
| `--categories <items>` | 逗号分隔的分类名 |
| `--tags <items>` | 逗号分隔的标签名 |
