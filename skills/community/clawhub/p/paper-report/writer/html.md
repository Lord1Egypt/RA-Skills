# 输出格式：HTML

自包含 HTML 报告（图片以 base64 形式内嵌），打开即可阅读，便于分享。

---

## 1. 适用场景

- 用户明确要求"生成 HTML 报告"。
- 用户未指定输出格式时的**默认选择**。
- 报告需要直接发送 / 分享 / 在线浏览，不希望出现"图片丢失"问题。
- 论文公式较多，需要更佳的数学公式排版（MathJax 渲染）。

## 2. 图片处理

将 `{workspace}/figures/` 下的所有目标图片转为 base64 data URI 内嵌：

```python
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    return f"data:{mime};base64,{data}"
```

在 HTML 中使用：

```html
<figure>
  <img src="{base64_data}" alt="Figure 1：架构图" style="max-width:100%;">
  <figcaption>图 1：架构图（原文 Figure 1）</figcaption>
</figure>
```

> 单张图片体积过大（>2 MB）时建议先用 PIL 缩放（如 LANCZOS 重采样到 1400 px 宽），避免最终 HTML 过大。

## 3. 数学公式

使用 LaTeX 语法书写公式：

- 行内公式：`$x = y + z$`
- 独立公式：`$$\mathcal{L} = \sum_i \log p_\theta(x_i)$$`

模板已内置 MathJax 3 配置和 `tex-svg.js` 脚本引用，无需额外引入。

**反斜杠陷阱**：在 Python 中拼接含 LaTeX 的字符串时，应使用**原始字符串**或**单反斜杠**，确保最终 HTML 中 LaTeX 命令前是单个 `\`：

```python
# ✅ 正确
formula = r"$\mathcal{L} = \sum_i \log p_\theta$"
# ❌ 错误：写成 \\mathcal 会渲染失败
formula = "$\\\\mathcal{L} = \\\\sum_i$"
```

## 4. 表格处理

直接使用 HTML `<table>` 标签，模板 CSS 已为表格定义样式（边框、表头加粗、行斑马纹）：

```html
<table>
  <thead>
    <tr><th>模型</th><th>BLEU</th><th>ROUGE-L</th></tr>
  </thead>
  <tbody>
    <tr><td>Baseline</td><td>32.1</td><td>54.2</td></tr>
    <tr><td><strong>Ours</strong></td><td><strong>35.8</strong></td><td><strong>57.6</strong></td></tr>
  </tbody>
</table>
```

加粗使用 `<strong>` 标记最佳值，便于读者快速定位重点。

## 5. 模板路径

[html-template.html](html-template.html)

模板包含完整 `<head>`（CSS 变量、MathJax 配置）、占位符（如 `{{PAPER_TITLE_CN}}`、`{{FIG1_BASE64}}`、`{{FIG1_CAPTION}}` 等）和章节骨架。生成时用字符串替换占位符。

## 6. 输出文件命名

保存到 `{workspace}/outputs/`：

- `report_{简短标题}.html` —— 单一自包含 HTML 文件

简短标题从论文标题中提取核心关键词（去除特殊字符，空格替换为 `-` 或 `_`）。

## 7. 写作风格细节

- 段落使用 `<p>` 包裹，章节使用 `<h2>` / `<h3>`。
- 重点结论可用 `<div class="highlight">...</div>`（模板预定义高亮卡片样式）。
- 引用原文术语时优先 `<em>` 或 `<code>` 而非反引号。
- 图表说明放在 `<figcaption>` 中，与图紧邻；正文用"如图 1 所示"引用。

## 8. 校验清单

使用 Read 工具查看生成的 HTML，逐项确认：

**通用检查**：

- 各章节标题完整、层级清晰
- 每个章节有实质内容，不存在空段落或占位符（无 `{{...}}` 残留）
- 不包含"报告生成日期"或"AI 辅助生成"相关文字

**HTML 专项检查**：

- HTML 基本结构完整：`<!DOCTYPE html>`、`<html>`、`<head>`、`<body>`、`</html>` 齐全
- `<head>` 中包含 MathJax 配置和 `tex-svg.js` 脚本引用
- 所有 `<img>` 的 `src` 为有效 base64 data URI（以 `data:image/png;base64,` 或 `data:image/jpeg;base64,` 开头）
- 不存在外部图片链接（`http://...png`）或本地文件路径引用
- 每张图片有描述性 `alt` 属性和 `<figcaption>`
- CSS 样式内嵌在 `<style>` 标签中，无外部样式表依赖
- **反斜杠检查**——确认 LaTeX 命令前是单个 `\`：

  ```bash
  grep -c '\\\\math' {workspace}/outputs/report_{简短标题}.html
  # 结果应为 0
  ```

## 9. 已知陷阱

- **公式中禁用 HTML 特殊字符**：`<`、`>`、`&` 同时对 HTML 解析器和 MathJax 有特殊含义，直接使用或转义为 `&lt;`/`&gt;` 都可能导致公式渲染失败。必须用 LaTeX 命令替代：`<` → `\lt`，`>` → `\gt`，尖括号标记如 `<token>` → `\langle\texttt{token}\rangle`。
- **MathJax 误报**：校验"无外部 src"时，注意 `<script src="https://...mathjax...">` 是允许的，只需确认 `<img>` 标签全部使用 base64。
- **HTML 体积**：高分辨率图过多时文件可能超过 5 MB，建议先在 figures 目录预压缩或限制 max-width。
- **占位符冲突**：模板中 `{{PLACEHOLDER}}` 与 LaTeX 的 `{...}` 形式相似，替换时使用精确字符串匹配，避免误伤。
- **base64 中转义字符**：base64 字符集不含 `\`，无需对其转义；但拼接到字符串时仍要确保 Python 字面量的反斜杠正确。
