---
name: md-to-pdf
description: 将 Markdown 文件转换为带封面页的专业 PDF。使用 Pandoc + Chrome Headless 方案，支持中文、表格、emoji、代码高亮、目录。默认自动生成封面（标题+日期），除非指定 --no-cover。
---

# MD to PDF v4.0

将 Markdown 转换为带封面页的高质量 PDF。

## 核心流程

```
MD 文件 → [提取标题] → 生成封面 HTML
                      → Pandoc 生成正文 HTML
                      → 本地 HTTP 服务 (127.0.0.1:PORT)
                      → Playwright CDP (chrome port 9222)
                      → page.pdf() 导出封面/正文 PDF
                      → PyPDF2 合并 → 最终 PDF
```

## 使用方法

```bash
# 带封面 + 目录（默认）
python "C:\Users\ThinkPad\.openclaw\workspace\skills\md-to-pdf\md_to_pdf_v4.py" input.md output.pdf --toc

# 不要封面页
python "C:\Users\ThinkPad\.openclaw\workspace\skills\md-to-pdf\md_to_pdf_v4.py" input.md output.pdf --toc --no-cover

# 自定义 CSS
python "C:\Users\ThinkPad\.openclaw\workspace\skills\md-to-pdf\md_to_pdf_v4.py" input.md output.pdf --toc --css custom.css
```

## 封面页

默认自动生成：
- **标题**：从 MD 文件第一个 `# 标题` 提取
- **日期**：当前日期（如 `2026年05月16日`）
- **样式**：居中大标题 + 底部日期横线，A4 白底

## 依赖

| 工具 | 说明 |
|------|------|
| Pandoc | 3.6.4 (`D:\mycode\pandoc\pandoc.exe`) |
| Chrome | 需开启 `--remote-debugging-port=9222` |
| Python | `PyPDF2`、`playwright` |

## 故障排除

### Chrome 147+ `--print-to-pdf` 失效（已修复）

Chrome v147+ 命令行 `--headless --print-to-pdf` 在 Windows 上已失效。

**修复**：改用 **Playwright CDP `page.pdf()`** + 本地 HTTP 服务（`http.server`）提供 HTML 文件。

### 列表符号不显示（已修复）

Chrome Headless 默认不渲染列表符号。

**修复**：CSS 显式声明 `list-style-type`（已内置）。

## 发送 PDF（QQ Bot）

**必须用 `Copy-Item` 复制到媒体目录，再用 `message` 工具发送：**

```powershell
Copy-Item $pdfPath "C:\Users\ThinkPad\.openclaw\media\qqbot\文件名.pdf" -Force
```

```
message(action="send", channel="qqbot", filePath="C:\Users\ThinkPad\.openclaw\media\qqbot\文件名.pdf", target="...")
```

⚠️ 旧版 `<qqmedia>` 标签已废弃。

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v4.0 | 2026-05-16 | 彻底删除 Pandoc 内置样式，只注入 BUILTIN_CSS；修复封面页 HTTP 服务目录 404 |
| v2.2 | 2026-05-14 | 增强 CSS（`!important`），修复列表/表格渲染 |
| v2.1 | 2026-05-10 | Playwright CDP 替代 Chrome Headless，修复 Chrome 147+ 失效问题 |
