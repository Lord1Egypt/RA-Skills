# HTML 模式处理流程

本文档描述从 arXiv HTML 页面（或其他 HTML 形式论文）提取内容的完整流程。
完成 H1–H3 后，返回 [SKILL.md](../SKILL.md) 执行 **Step 2**（生成报告）和 **Step 3**（校验）。

## 进度清单

```
Task Progress (HTML Mode):
- [ ] Step H1: 下载 HTML 文件
- [ ] Step H2: 提取正文文本 & 规划图表清单
- [ ] Step H3: 下载图表图片并校验
- [ ] 返回 SKILL.md Step 2: 生成报告
- [ ] 返回 SKILL.md Step 3: 校验文件
```

---

### Step H1: 下载 HTML 文件

确定 HTML URL（来自路由决策），下载到工作目录：

```bash
curl -sL "{HTML_URL}" -o {workspace}/paper.html
```

验证下载成功（文件应大于 10KB，且包含 `<html` 标签）：

```bash
wc -c {workspace}/paper.html
grep -c "<html" {workspace}/paper.html
```

---

### Step H2: 提取正文文本 & 规划图表清单

**任务 A — 提取纯文本（含公式与表格结构）**：

使用 `scripts/extract_html_text.py` 提取干净的正文文本，保留数学公式和表格基本结构：

```bash
{PYTHON} scripts/extract_html_text.py {workspace}/paper.html {workspace}/paper_text.txt
```

脚本将 `<math>` 标签转为 LaTeX 格式（`$...$` / `$$...$$`），表格转为管道分隔行，输出到 `paper_text.txt`。

**任务 B — 提取图表 URL 列表**：

使用 `scripts/extract_figure_urls.py` 扫描 HTML 中所有 `<figure>` 块，提取可下载图片 URL 并识别内联 SVG：

```bash
{PYTHON} scripts/extract_figure_urls.py {workspace}/paper.html "{HTML_URL}"
```

脚本输出两类结果：
- **Downloadable figures**：带有 `<img>` 标签的图片，输出完整 URL
- **Inline SVG figures**：无外部图片文件，需用 cairosvg 转为 PNG（见 Step H3 末尾说明）

**任务 C — 阅读正文**：

使用 Read 工具阅读 `{workspace}/paper_text.txt`，理解论文全文内容。超长文本（>50,000 字符）使用 `offset` 和 `limit` 参数分批阅读。

在阅读过程中，从上方图表 URL 列表中挑选需纳入报告的**关键图表**（选取原则见 [SKILL.md](../SKILL.md) Step 2「图表选取原则」）。

记录下载计划：

```
图表下载计划：
1. Figure 1 - 系统架构图 → {URL1} → fig1_architecture.png
2. Figure 2 - 数据集构造 → {URL2} → fig2_dataset.png
3. Figure 4 - 方法框架 → {URL3} → fig4_framework.png
4. Table 3 - 实验结果 → {URL4} → table3_results.png
...
```

---

### Step H3: 下载图表图片并校验

根据 Step H2 的下载计划，逐一下载图片到 `{workspace}/figures/`：

```bash
mkdir -p {workspace}/figures
curl -sL "{FIGURE_URL}" -o {workspace}/figures/{FIGURE_NAME}
```

下载完成后，使用 Read 工具逐一查看每张图片，确认：
- 图片内容与预期图表一致（非空白、非破损）
- 图表标题或标注清晰可见
- 若图片无法正常显示或内容不对，记录问题并跳过该图（不强制使用）

**下载失败排查**：如果 curl 返回 HTML 错误页或 0 字节文件，检查 URL 是否正确。常见问题：
- arXiv 图片路径可能是 `x1.png`, `x2.png` 等简短名称
- 确认 `urljoin` 结果是否合理，必要时手动构造 URL

**内联 SVG 图表处理**：

部分 arXiv HTML 论文（尤其是 TikZ 绘制的图）不使用外部图片文件，而是将 SVG 直接内嵌在 `<figure>` 标签中。此时 Step H2 的图表 URL 列表中**不会出现**对应图片。

识别方式：`<figure>` 内包含 `<svg>` 标签而非 `<img>` 标签。

处理方法——**直接将 SVG 转为 PNG**（依赖 `cairosvg`，首次使用时安装：`pip install cairosvg`）：

```python
import re, cairosvg

# 从 HTML 中提取目标 <figure> 内的 <svg>...</svg> 完整内容
svg_match = re.search(r'(<svg[^>]*>.*?</svg>)', figure_block, re.DOTALL)
svg_string = svg_match.group(1)

# 渲染为 2x 分辨率 PNG
cairosvg.svg2png(bytestring=svg_string.encode('utf-8'),
                 write_to='{workspace}/figures/{name}.png',
                 scale=2)
```

转换后用 Read 工具查看图片，确认渲染正确。

> 仅对内联 SVG 图表执行此转换，能正常下载的 `<img>` 图片不受影响。

---

完成以上 H1–H3 后，返回 [SKILL.md](../SKILL.md) 执行 **Step 2** 生成报告。
