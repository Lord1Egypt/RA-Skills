---
name: obsidian-save-article
description: 将网页文章保存到本地 Obsidian Vault，支持图片抓取、Markdown 转换、YAML frontmatter 和用户笔记附加。
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# Obsidian Save Article

将网页文章保存到本地 Obsidian Vault，支持图片抓取。

## 触发方式

当用户发送：

- 一个网页链接
- 可选的 notes 或 comments
- 明确要求"保存到 Obsidian"或"收藏文章"

例如：

- `https://example.com/article 这篇文章不错`
- `帮我保存这个：https://xxx.com 内容：我的笔记`

---

## 首次使用：路径配置

### 第一次运行时的引导流程

首次使用该技能时，系统会自动检测是否已配置保存路径。如果没有配置，会引导用户完成设置：

```
🔷 欢迎使用 Obsidian 文章保存功能！

请选择您要保存到的 Obsidian Vault 类型：

1️⃣ 本地 Obsidian（本地磁盘）
2️⃣ iCloud Obsidian（云端同步）

请回复数字或选项名称。
```

#### 选项 1：本地 Obsidian

如果用户选择本地 Vault：

```
📂 请告诉我您的 Obsidian Vault 路径。

例如：~/Documents/Obsidian Vault

或者直接拖拽文件夹到聊天窗口，我会自动识别路径。
```

用户输入路径后，验证路径有效性：

```
✅ 找到 Vault：My Notes
   路径：/Users/liz/Documents/Obsidian Vault/My Notes

📁 请输入要保存文章的子文件夹名称（可选）。

例如：Articles、ReadLater、收藏夹
直接回车将保存到根目录。
```

#### 选项 2：iCloud Obsidian

如果用户选择 iCloud Vault：

```
☁️ iCloud Obsidian 路径查找指南：

1. 打开 Finder
2. 在左侧边栏找到 "iCloud"
3. 点击 "iCloud Drive"
4. 找到您的 Obsidian Vault 文件夹
5. 右键点击 → "复制路径"

请将路径粘贴到聊天中。
```

用户输入 iCloud 路径后，类似本地流程询问子文件夹。

### 路径配置存储

配置完成后，路径信息会保存在：
```
~/.obsidian-save-article-config.json
```

内容示例：
```json
{
  "type": "local",
  "vault_path": "/Users/liz/Documents/Obsidian Vault/My Notes",
  "subfolder": "Articles",
  "full_path": "/Users/liz/Documents/Obsidian Vault/My Notes/Articles",
  "configured": true,
  "configured_at": "2026-03-18T01:00:00Z"
}
```

### 重新配置路径

用户可以随时重新配置路径：
- 说"更改 Obsidian 保存路径"或"重新配置"
- 说"查看当前保存路径"查看配置

---

## 保存格式

### YAML Frontmatter

```yaml
---
title: "文章标题"
url: "原始链接"
created: "YYYY/MM/DD"
pagecomment: "用户添加的页面评论"
---
```

### 全文内容

**重要：图片必须放在 Full Article callout 内部，位于内容之前！**

```text
> [!note]- 📄 Full Article
> ![](images/img-xxxxxx.png)
> ![](images/img-yyyyyy.png)
> 文章第一段内容...
> 文章第二段内容...
```

**错误格式（图片在 callout 外部）：**
```text
> ![](images/img-xxxxxx.png)  ← 错误！在 callout 外面
> [!note]- 📄 Full Article
> 文章内容...
```

**正确格式（图片在 callout 内部）：**
```text
> [!note]- 📄 Full Article  ← callout 头部先
> ![](images/img-xxxxxx.png)  ← 图片在 callout 内部
> 文章第一段内容...
> 文章第二段内容...
```

### 用户 Notes

```text
> 用户笔记内容
^note-xxx
```

## 内容抓取方法

该技能支持两种内容抓取方法，系统会自动选择最合适的方式。

### 方法 1：Jina.ai Reader（首选）

- **原理**：使用 `https://r.jina.ai/<URL>` 抓取网页内容
- **优点**：快速、返回干净的 Markdown 格式
- **适用**：大多数网站、博客、新闻文章

### 方法 2：Browser 工具（Fallback）

当 Jina.ai 失败时，自动使用浏览器工具抓取内容。

**触发条件**：
- Jina.ai 返回错误
- Jina.ai 返回空内容或无效内容
- 连接超时
- 网站阻止 Jina.ai 访问（如微信公众号文章、付费内容）

**操作步骤**：
1. 使用 `browser` 工具打开目标 URL
2. 获取页面快照（snapshot）
3. 提取页面文本内容
4. 清理和格式化内容

#### Browser 工具调用示例

```python
# Step 1: 打开页面
browser(action="open", url="https://example.com/article")

# Step 2: 获取快照（使用 aria 模式获取结构化内容）
browser(action="snapshot", snapshotFormat="aria")

# Step 3: 提取文本内容并清理
```

#### 内容清理规则

从浏览器获取内容后，需要进行清理：
- 移除导航栏、页脚、广告等无关内容
- 保留文章标题和正文
- 转换 HTML 标签为 Markdown 格式
- 处理特殊字符和编码问题

---

## 工作流程

### 带路径配置的工作流程

1. **检查配置**：读取 `~/.obsidian-save-article-config.json`
   - 如果未配置 → 触发首次配置流程（见上文）
   - 如果已配置 → 继续第 2 步

2. **解析输入**：提取 URL 和用户 notes

3. **抓取内容**：
   - **Step 1**：优先使用 Jina.ai Reader (`https://r.jina.ai/<URL>`)
   - **Step 2 (Fallback)**：如果 Jina.ai 失败，使用 browser 工具：
     - 执行 `browser action=open url="<URL>"` 打开页面
     - 执行 `browser action=snapshot` 获取页面内容
     - 提取文本并清理格式
   - **Step 3**：继续图片提取和保存流程

4. **提取图片**：从 HTML 中提取正文图片

5. **下载图片**：调用 `download_images.py` 保存到配置的 Vault 的 `images/` 目录

6. **转换 Markdown**：将图片路径转为本地相对路径

7. **构建文件**：
   - Frontmatter（标题、URL、日期、评论）
   - Full Article callout（图片在前，内容在后）
   - 用户 notes

8. **保存文件**：写入配置的 Vault 路径

### 路径配置检测逻辑

```python
import os
import json

CONFIG_PATH = os.path.expanduser("~/.obsidian-save-article-config.json")

def load_config():
    """加载配置文件，如果不存在返回 None"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    """保存配置到文件"""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def get_save_path():
    """获取当前配置的保存路径"""
    config = load_config()
    if config and config.get("configured"):
        return config.get("full_path")
    return None
```

---

## 图片下载脚本

### 调用方式

```bash
python ~/.openclaw/workspace/skills/obsidian-save-article/scripts/download_images.py "<URL>" "<Vault子目录路径>"
```

**参数说明：**
- `<URL>`：要抓取的网页 URL
- `<Vault子目录路径>`：Obsidian Vault 的路径（脚本会自动在此创建 `images/` 子目录）

**示例：**
```bash
# 保存到本地 Vault 的 Articles 文件夹
python ~/.openclaw/workspace/skills/obsidian-save-article/scripts/download_images.py \
  "https://example.com/article" \
  "~/Documents/Obsidian Vault/My Notes/Articles"

# 保存到 iCloud Vault 的 ReadLater 文件夹
python ~/.openclaw/workspace/skills/obsidian-save-article/scripts/download_images.py \
  "https://example.com/article" \
  "~/Library/Mobile Documents/iCloud~com~obsidian~md/Documents/我的 Vault/ReadLater"
```

### 返回结果

脚本返回 JSON：

```json
{
  "html": "原始 HTML",
  "images": [["original_url", "local_filename"]],
  "markdown": "转换后的 Markdown"
}
```

---

## 图片处理规则

- 支持格式：`jpg`、`jpeg`、`png`、`gif`、`webp`、`svg`、`bmp`
- 跳过 `data:`、`javascript:`、base64 小图
- 使用 URL 的 MD5 前 12 位作为本地文件名
- Markdown 中使用相对路径 `images/img-xxxx.png`

---

## 常见问题

### Q: 如何查看当前保存路径？
A: 说"查看保存路径"或"我的 Obsidian 配置"

### Q: 如何更改保存位置？
A: 说"更改保存路径"或"重新配置"来重新设置

### Q: iCloud 路径找不到怎么办？
A: 
1. 确保 macOS 已登录 iCloud
2. 打开 Finder → iCloud Drive
3. 找到 Obsidian 文件夹，右键"复制路径"

### Q: 图片下载失败怎么办？
A: 文章仍会保存，只是图片位置会保留原始 URL。不影响主要功能。

### Q: 什么情况下会使用浏览器抓取？
A: 系统会自动判断。当 Jina.ai 无法使用时，会自动切换到浏览器方式：
- 微信公众号文章
- 需要登录的内容
- 阻止爬虫的网站
- 返回空内容的页面

### Q: 两种抓取方式有什么区别？
A: 
| 特性 | Jina.ai Reader | Browser 工具 |
|------|----------------|--------------|
| 速度 | 快 | 较慢 |
| 格式 | 干净 Markdown | 需要清理 |
| 适用 | 大多数网站 | 复杂页面 |
| 登录 | 不支持 | 可支持 |

---

## 注意事项

- Jina.ai Reader URL 格式：`https://r.jina.ai/<原始URL>`
- X 链接使用：`https://r.jina.ai/https://x.com/...`
- 当 Jina.ai 失败时，自动使用 browser 工具作为后备方案
- 微信公众号文章通常需要使用 browser 工具抓取
- 图片下载失败不应阻断文章保存
- 文件名中的特殊字符 `<>:\"|?*` 需要替换
- 页面正文超过 50000 字符时应截断
