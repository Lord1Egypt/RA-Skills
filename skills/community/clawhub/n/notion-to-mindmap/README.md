# Notion Mind Map — Reference

## Notion 链接格式

每个页面的链接由工作空间 URL + 32 位页面 UUID 组成：

```
https://www.notion.so/<workspace>/<page-id-32chars>
```

示例：`https://www.notion.so/workspace/abc123def456789...`

UUID 从 HTML 中的 `<ul id="id::xxxx-xxxx-xxxx">` 属性提取，去掉连字符。

## 层级定义

| Level | 定义 | 默认展开 |
|-------|------|----------|
| 0 | 根节点（工作空间名称） | 是 |
| 1 | 一级页面（Notion 导出的顶层页面） | 是 |
| 2+ | 逐级展开 | 默认折叠 |

## 页面标题清理规则

原始 HTML 中的 `<a>` 标签文本可能包含：
- `.html` / `.csv` 文件后缀
- `(Inline database)` 标注
- 末尾的 32 位 UUID

这些都会被 `build_mindmap.py` 的 `clean_title()` 函数自动清理。

## CSV 数据库条目处理

Notion 导出的 HTML 中，每个数据库页面会生成两个条目：
- `<ul id="...csv">` — CSV 文件条目（被跳过）
- `<ul id="...">` — 真实页面（被解析）

## 交互功能详解

### 鼠标交互

- **空白拖拽**：平移画布
- **滚轮**：以鼠标位置为中心缩放，每级 5%
- **左键单击**：展开/折叠（节点屏幕位置保持不变）
- **Ctrl+左键单击**：直接在浏览器打开 Notion 页面
- **右键**：弹出菜单（复制链接 / 聚焦）

### 搜索

- `Ctrl+F` 聚焦搜索框
- 实时高亮匹配页面（当前结果金色，其他结果橙色）
- `Enter` 跳转到下一个匹配
- `Esc` 清除搜索
- **智能展开**：只展开包含搜索结果的路径，不展开无关分支

### 工具栏

| 按钮 | 效果 |
|------|------|
| 重置 | 展开到第 2 级，缩放 100%，根节点居中 |
| 适应屏幕 | 自动计算所有可见节点边界，缩放至屏幕内 |
| 展开全部 | 展开所有层级 |
| 折叠全部 | 仅显示到第 1 级 |

### 提示信息

- **鼠标悬停父节点**：显示子页面数量（tooltip）
- **右下角**：当前缩放比例

## 视觉风格

- **暗色主题**：深蓝色背景（#1a1a2e）
- **分支颜色继承**：每个第 1 级分支有独立颜色，子级颜色逐级淡化
- **连接线**：贝塞尔曲线，粗细随层级递减
- **叶子节点**：无边框，仅底部细线
- **非叶子节点**：圆角矩形带半透明填充

## 依赖

```bash
pip install beautifulsoup4
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `build_mindmap.py` | 解析 HTML → 生成 `mindmap_data.json` |
| `generate_html.py` | 读取 JSON → 生成自包含 `mindmap.html` |

## 自定义

如需修改 Notion 链接基础地址：

```bash
python build_mindmap.py index.html https://www.notion.so/yourworkspace/
```

如需修改分支颜色，编辑 `generate_html.py` 中的 `BRANCH_COLORS` 数组。
