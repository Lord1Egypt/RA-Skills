---
name: markdown-to-feishu-post
description: 将标准 Markdown 文本转换为飞书富文本消息（Post）的 JSON 结构。支持多级标题、粗体、斜体、下划线、删除线、链接、@用户、图片、有序/无序列表、代码块、引用和分割线。当用户需要发送飞书富文本消息、将 Markdown 转换为飞书格式、构建飞书机器人消息内容时使用。
---

# Markdown 转飞书富文本消息

将标准 Markdown 转换为飞书 Post 消息的 JSON 结构。

## 使用方法

```bash
# 直接输入 Markdown 文本
python3 scripts/markdown_to_feishu_post.py "markdown内容"

# 从文件读取
python3 scripts/markdown_to_feishu_post.py --file input.md

# 紧凑输出（单行 JSON）
python3 scripts/markdown_to_feishu_post.py --compact "markdown内容"
```

## 支持的 Markdown 语法

| 语法 | 飞书标签/样式 |
|------|---------------|
| `# 标题` | `title` 字段（一级标题） |
| `## ### 标题` | 加粗文本 |
| `**粗体**` | `style: ["bold"]` |
| `*斜体*` | `style: ["italic"]` |
| `~下划线~` | `style: ["underline"]` |
| `~~删除线~~` | `style: ["lineThrough"]` |
| `[链接](url)` | `{"tag": "a", "href": "url", "text": "链接"}` |
| `<at user_id="ou_xxx">@名字</at>` | `{"tag": "at", "user_id": "ou_xxx"}` |
| `![alt](image_key)` | `{"tag": "img", "image_key": "..."}` |
| `1. 有序列表` | 带数字前缀的文本 |
| `- 无序列表` | 带 `•` 前缀的文本 |
| ` ```语言\ncode\n``` ` | `{"tag": "code_block", "language": "...", "text": "..."}` |
| `> 引用` | 普通文本段落 |
| `---` | `{"tag": "hr"}` |

## 输出结构

```json
{
  "zh_cn": {
    "title": "一级标题",
    "content": [
      [{"tag": "text", "text": "段落内容"}],
      [{"tag": "hr"}]
    ]
  }
}
```

## 注意事项

1. **一级标题**：第一个 `#` 标题会作为消息标题（`title` 字段）
2. **图片**：飞书使用 `image_key` 而非 URL，需要先上传图片获取 key
3. **@用户**：`user_id` 可为 `open_id`、`user_id`、`union_id` 或 `all`（@所有人）
4. **代码块**：支持 PYTHON、GO、JAVA、JAVASCRIPT 等语言标识
5. **多语言**：默认输出 `zh_cn`，可手动添加 `en_us` 等其他语言版本