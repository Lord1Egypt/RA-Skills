---
name: notion-to-mindmap
description: 将 Notion 导出的 HTML 文件转换为可交互的思维导图 HTML。支持右键跳转到 Notion 页面链接、搜索、缩放、展开/折叠等功能。当用户提供 Notion HTML 导出文件、提到"思维导图"、"mindmap"、或希望可视化 Notion 页面结构时使用。
---

# Notion to Mind Map

将用户的 Notion HTML 导出转换为可交互的思维导图。

## 核心交互功能

| 操作 | 效果 |
|------|------|
| 空白处拖拽 | 平移画布 |
| 鼠标滚轮 | 缩放（每级 5%，右下角显示比例） |
| 左键单击节点 | 展开/折叠（位置保持不变） |
| Ctrl+左键 | 直接在浏览器打开 Notion 页面 |
| 右键节点 | 复制链接 / 聚焦此页面 |
| Ctrl+F | 聚焦搜索框，实时高亮跳转 |

## 顶部工具栏

- **重置**：展开到第 2 级，100% 缩放
- **适应屏幕**：自动缩放显示全部展开节点
- **展开全部** / **折叠全部**
- **统计**：显示页面总数和最大层级

## 使用方式

用户只需要发送 Notion 导出的 `index.html` 文件给我，我会自动完成所有转换工作，输出可直接打开的 `mindmap.html`。

### 工作流程

1. 用户发送 Notion 导出的 `index.html`
2. 我运行 `build_mindmap.py` 解析 HTML → 生成 `mindmap_data.json`
3. 我运行 `generate_html.py` 生成 `mindmap.html`
4. 我将 `mindmap.html` 返回给用户

### 依赖要求

需要 BeautifulSoup4：
```bash
pip install beautifulsoup4
```

## Notion 链接说明

生成的 Notion 链接格式为：`https://www.notion.so/<workspace>/<page-id>`

如果用户需要自定义工作空间前缀（默认从 HTML 中解析），可以修改 `build_mindmap.py` 中的 `NOTION_BASE` 常量。

## 数据结构说明

页面层级对应：
- Level 0：根节点（工作空间名称）
- Level 1：一级页面（Notion 导出的顶层页面）
- Level 2+：逐级展开

脚本会自动跳过 CSV 数据库条目，并从 `<ul id>` 中提取真实的 32 位页面 UUID。

## 详细参考

- [README.md](README.md) — 完整的 Notion 链接格式、层级定义、交互细节
