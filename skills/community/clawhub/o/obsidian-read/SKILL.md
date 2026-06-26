---
name: obsidian-read
description: |
  读取 Obsidian Publish 发布的文档链接。当用户发送 publish.obsidian.md 链接，或需要读取 Obsidian 笔记文章时使用。
  适用于从 Obsidian Publish 平台获取完整文章内容、笔记、Essay 等场景。
  优先使用 web_fetch，失败时使用 browser 工具方案。
---

# Obsidian Read

读取 Obsidian Publish 发布的文档内容。

## 工作流

### 步骤 1：优先尝试 web_fetch

```python
web_fetch(url="链接", maxChars=15000)
```

如果成功返回完整内容，直接使用。

### 步骤 2：使用 browser 方案（当 web_fetch 失败时）

当 web_fetch 返回内容不完整、404 或解析错误时，使用以下流程：

**2.1 打开链接获取 targetId**

```python
browser(action="open", url="https://publish.obsidian.md/a/essay/xxx")
```

返回结果包含 `targetId`，例如：`"579ECBB9218EE0FA843D5CACD2BD99F0"`

**2.2 读取页面内容**

```python
browser(action="snapshot", targetId="上一步获取的targetId")
```

**2.3 提取文本**

从 snapshot 结果中提取 `paragraph`、`heading` 等文本元素，返回给用户。

## 注意事项

- **必须用 open 获取 targetId**：直接使用 snapshot 而不传 targetId 会导致失败
- **静态内容优先**：Obsidian Publish 是静态站点，snapshot 通常能完整抓取
- **不需要截图**：snapshot 是获取可访问性树（文本内容），不是截图

## 示例

用户发送：`https://publish.obsidian.md/a/essay/202603181132`

1. 先尝试 `web_fetch` → 失败/不完整
2. `browser.open` → 获取 targetId
3. `browser.snapshot` → 读取完整文章
4. 总结文章内容返回给用户
