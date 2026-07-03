---
name: mli-paper-reading
description: "Academic paper reading and literature research skill for paper-reading, 论文阅读, 论文精读, 文献阅读, literature review, arXiv, DOI, PDF, paper title, or paper list tasks. Use to triage papers, apply Li Mu inspired three-pass reading, do section-by-section deep reading, critique methods and experiments, compare papers, plan reproduction, find research ideas, or build a literature map."
allowed-tools: Bash, Write, Read, WebFetch
slug: mli-paper-reading-penghel
displayName: 李沐论文精读 Skill
version: 1.2.0
summary: 基于李沐论文精读系列的三遍读法 Skill。先筛选（五个 C），再系统精读，最后拆论证链、审实验、评复现风险。支持 arXiv 链接、PDF 文件、DOI 和论文标题，自动从 PDF 提取原文插图，生成含 MathJax 公式渲染的本地 HTML 阅读笔记，在浏览器中图文并茂地展示。
license: MIT
---

# 李沐论文精读 Skill

## 快速开始

### 一句话安装依赖（仅首次）

```bash
python3 -m pip install pymupdf --user
```

其他所有依赖（Python 3.7+、http.server、lsof、curl、open）在 macOS 上均为系统内置，Linux 用户见下方依赖表。

### 调用方式

```
# Claude Code
/mli-paper-reading 帮我精读这篇论文: https://arxiv.org/abs/1706.03762

# Codex
$mli-paper-reading 帮我精读这篇论文: https://arxiv.org/abs/1706.03762
```

支持输入格式：arXiv 链接、直接 PDF 链接、本地 PDF 路径、DOI、论文标题。

### 完整使用示例

**示例 1：精读 arXiv 论文**
```
/mli-paper-reading 帮我精读 Attention Is All You Need: https://arxiv.org/abs/1706.03762
```
→ 自动下载 PDF，提取 Figure 1–5，生成 HTML 笔记，浏览器打开 `http://localhost:7410/attention-is-all-you-need.html`

**示例 2：精读本地 PDF**
```
/mli-paper-reading 精读这篇论文: ~/Downloads/dspark.pdf
```
→ 从本地 PDF 提取图片，生成笔记

**示例 3：只有标题，无 PDF**
```
/mli-paper-reading 帮我了解一下 LoRA 这篇论文
```
→ 通过 WebFetch 获取摘要和正文，用 Mermaid 架构图替代原图，生成笔记

**示例 4：比较多篇论文**
```
/mli-paper-reading 比较 BERT、GPT-2、T5 的架构设计和预训练策略
```
→ 输出对比表，每篇独立 Paper Card，共用一个 HTML 笔记

**示例 5：为复现做准备**
```
/mli-paper-reading 我要复现 DSpark，帮我整理复现清单和风险点
```
→ 深度 Pass 3，输出复现 Recipe、假设列表、缺失细节标注

---

## 概述

这个 Skill 将论文变成可直接使用的研究理解：判断是否值得读、选择合适深度阅读、重建论证、审查证据，最终生成支持实现、评审、找方向的结构化笔记。

方法论来自李沐论文精读系列（快速筛选 + 三遍阅读 + 逐段精读）。详细检查清单和输出模板见 `references/li-mu-method.md`——在发起深度精读、对比、复现计划、文献综述或找研究方向前，必须先读该文件。

---

## 触发方式

显式触发最可靠：

- Claude Code: `/mli-paper-reading 帮我精读这篇论文: <arXiv/PDF/DOI/title>`
- Codex: `$mli-paper-reading 帮我精读这篇论文: <arXiv/PDF/DOI/title>`
- 路径兜底: `Use the skill at ./mli-paper-reading to read <paper>.`

自动触发依赖 frontmatter `description` 中的关键词：paper、PDF、arXiv、DOI、论文阅读、论文精读、literature review、reproduction、comparison、literature map。

---

## 工作流

1. **明确阅读目标。** 判断用户需要快速决策、学习笔记、严格评审、复现计划、论文对比还是文献地图。若只给了标题或链接，先获取论文元数据和正文再分析。

2. **先筛选再深读。** 读标题、摘要、引言、节标题、结论、图表、参考文献。产出 Paper Card：问题、背景、贡献声明、证据类型、venue/年份、是否继续。

3. **三遍读法。** Pass 1 建立整体图像和读/跳决策。Pass 2 梳理内容、图表、方法、实验和核心证据，不陷入证明细节。Pass 3 虚拟复现：重建假设、方法步骤、公式/伪代码、实验设计、局限性、可能缺失的细节。

4. **把论文读成论证链。** 追踪「问题→主张→理由→证据→局限」链条。不只是逐节总结。对每个主要主张，问：哪个结果支撑它？基线公平吗？隐含了什么假设？什么会改变你的判断？

5. **建立论文上下文。** 用相关工作、共同引用、重复作者名、顶会、后续论文定位研究谱系。综述任务时，按问题、方法族、数据集、主张、失败模式聚类。

6. **生成 HTML 笔记并在浏览器打开。** 分析完成后，生成自包含 HTML 阅读笔记，本地起服务打开。见下方 HTML Output 节。

---

## 阅读规则

- 先宽后深。除非用户明确要求逐段阅读，不要从头逐段复述。
- 以图表、数据、消融实验、误差分析为证据优先，文字主张只是主张不是证明。
- 挑战实验设计细节：数据泄露、不公平基线、指标错位、规模效应、计算预算、超参搜索、省略的负面结果。
- 把陌生符号和术语翻译成平白语言，但实现所需的原始符号要保留。
- 论文无法访问或关键细节缺失时，明确说明缺失内容，在最有依据的前提下继续分析。

---

## 依赖

### 一键自检

```bash
python3 - <<'EOF'
import sys
print("Python:", sys.version.split()[0])

missing = []

try:
    import fitz
    print("pymupdf:", fitz.__version__)
except ImportError:
    missing.append("pymupdf")
    print("pymupdf: MISSING")

import http.server, urllib.request, base64, json, os, subprocess
print("stdlib (http.server, base64, json, subprocess): ok")

r = subprocess.run(["lsof", "-h"], capture_output=True)
print("lsof:", "ok" if r.returncode in (0,1) else "MISSING")

r = subprocess.run(["curl", "--version"], capture_output=True)
print("curl:", "ok" if r.returncode == 0 else "MISSING")

import platform
if platform.system() == "Darwin":
    print("browser opener: open (macOS built-in)")
else:
    r = subprocess.run(["which", "xdg-open"], capture_output=True)
    print("browser opener: xdg-open", "ok" if r.returncode == 0 else "MISSING — install xdg-utils")

if missing:
    print("\n缺少以下包，请安装：")
    for pkg in missing:
        print(f"  python3 -m pip install {pkg} --user")
else:
    print("\n所有依赖已满足。")
EOF
```

### 依赖明细

| 依赖 | 用途 | 安装 | 备注 |
|---|---|---|---|
| **Python 3.7+** | 所有步骤 | macOS 内置；Linux: `sudo apt install python3` | `http.server --directory` 需 3.7+ |
| **pymupdf** (`import fitz`) | 图片提取（Step 2） | `python3 -m pip install pymupdf --user` | **唯一需要手动安装的包**，版本 ≥ 1.18 |
| **http.server** | 本地服务（Step 3） | Python 内置，无需安装 | 服务 `~/paper-notes/` |
| **lsof** | 端口检测（Step 3） | macOS 内置；Linux: `sudo apt install lsof` | 不可用时直接用 7410 端口 |
| **curl** | 服务健康检查（Step 3） | macOS 内置；Linux: `sudo apt install curl` | 不可用时改 `sleep 1` |
| **open** / **xdg-open** | 打开浏览器（Step 4） | macOS 内置；Linux: `sudo apt install xdg-utils` | 不可用时打印 URL 请用户手动打开 |
| **MathJax 3** | HTML 公式渲染 | 浏览器打开时从 cdn.jsdelivr.net 加载 | 离线时公式显示为原始 LaTeX |
| **Mermaid** | HTML 架构图 | 浏览器打开时从 cdn.jsdelivr.net 加载 | 无 PDF 时作为图的替代；离线时不渲染 |

HTML 文件本身完全自包含（图片 base64 内嵌），生成和启动服务均不需要联网。

---

## HTML 笔记生成

分析完成后，**必须**生成本地 HTML 阅读笔记并打开浏览器。深度精读不得跳过此步骤。

### Step 1：确定输出路径

```bash
mkdir -p ~/paper-notes
SLUG=$(echo "<paper-title>" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | cut -c1-60)
OUTPUT="$HOME/paper-notes/${SLUG}.html"
echo "Output: $OUTPUT"
```

### Step 2：提取论文原图

从 PDF 提取图片并 base64 编码，内嵌进 HTML。需要 `pymupdf`（见依赖节）。若输入只有 URL 或标题（无本地 PDF），跳至 Step 2b，仅用 Mermaid 图。

```python
# 运行方式: python3 extract_figs.py <pdf_path>
import fitz, base64, json, sys, os

pdf_path = sys.argv[1]
doc = fitz.open(pdf_path)
figures = []

# Pass 1: 取 PDF 内嵌的栅格图（已光栅化的图）
for pg_num in range(len(doc)):
    page = doc[pg_num]
    text_lines = [l.strip() for l in page.get_text().split('\n')]
    captions = [l for l in text_lines if l.lower().startswith('figure')]
    for img_idx, img_info in enumerate(page.get_images(full=True)):
        xref = img_info[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.width < 120 or pix.height < 120:  # 跳过装饰性小图
            pix = None; continue
        if pix.n > 4:                             # CMYK → RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        b64 = base64.b64encode(pix.tobytes("png")).decode()
        cap = captions[img_idx] if img_idx < len(captions) else f"Figure (page {pg_num+1})"
        figures.append({"label": f"fig_p{pg_num+1}_{img_idx}", "page": pg_num+1,
                        "caption": cap, "b64": b64, "w": pix.width, "h": pix.height})
        pix = None

# Pass 2: 矢量绘制的图所在页，整页 2× 渲染并精确裁剪图区
raster_pages = {f["page"]-1 for f in figures}
for pg_num in range(len(doc)):
    if pg_num in raster_pages:
        continue
    page = doc[pg_num]
    text = page.get_text()
    if not any(kw in text.lower() for kw in ['figure ', 'fig.']):
        continue
    # 用 drawing bbox 精确裁剪图区（含 caption padding）
    paths = page.get_drawings()
    img_blocks = [b for b in page.get_text("dict")["blocks"] if b.get("type") == 1]
    fig_rects = [fitz.Rect(p["rect"]) for p in paths if p["rect"][2]-p["rect"][0] > 20]
    for ib in img_blocks:
        fig_rects.append(fitz.Rect(ib["bbox"]))
    if fig_rects:
        union = fig_rects[0]
        for r in fig_rects[1:]: union = union | r
        pad = 10
        pw, ph = page.mediabox.width, page.mediabox.height
        clip = fitz.Rect(max(0,union.x0-pad), max(0,union.y0-pad),
                         min(pw,union.x1+pad), min(ph,union.y1+pad))
        # 向下扩展到 caption 文字
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0: continue
            bt = " ".join(s["text"] for ln in b["lines"] for s in ln["spans"])
            if "figure" in bt.lower() and fitz.Rect(b["bbox"]).y0 < clip.y1 + 60:
                clip = clip | fitz.Rect(b["bbox"])
    else:
        clip = fitz.Rect(0, 0, page.mediabox.width, page.mediabox.height * 0.65)
    captions = [l.strip() for l in text.split('\n') if l.strip().lower().startswith('figure')]
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
    b64 = base64.b64encode(pix.tobytes("png")).decode()
    cap = captions[0] if captions else f"Figure (page {pg_num+1})"
    figures.append({"label": f"fig_p{pg_num+1}_render", "page": pg_num+1,
                    "caption": cap, "b64": b64, "w": pix.width, "h": pix.height,
                    "full_page": True})
    pix = None

doc.close()
print(json.dumps(figures))  # 被 HTML 生成步骤消费
```

将脚本 JSON 输出中的 `b64` 值作为 `data:image/png;base64,<b64>` 图片源内嵌进 HTML。每张图的 HTML 结构：

```html
<figure style="text-align:center;margin:1.5rem 0;">
  <img src="data:image/png;base64,{b64}"
       style="display:block;max-width:100%;height:auto;margin:0 auto;
              border:1px solid #ddd;border-radius:4px;background:#fff;"
       alt="{caption}">
  <figcaption style="font-size:0.82rem;color:#666;font-style:italic;margin-top:0.4rem;">
    {caption}
  </figcaption>
</figure>
```

每张图放在**讨论它的段落之后**，不要集中放到末尾。无 PDF 时跳过此步骤，仅用 Mermaid 图。

### Step 2b：写 HTML 文件

写一个自包含 HTML 文件到 `$OUTPUT`。所有 CSS/JS 内联，仅允许加载以下两个可信 CDN 库：

- MathJax：`https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`
- Mermaid（无 PDF 时用）：`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`

#### HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{paper title}</title>
  <script>
    MathJax = { tex: { inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['$$','$$'],['\\[','\\]']] } };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>/* 见设计规范 */</style>
</head>
<body>
  <!-- 见内容规范 -->
  <script>mermaid.initialize({startOnLoad:true, theme:'neutral'});</script>
</body>
</html>
```

#### 样式规范

```css
body { max-width: 860px; margin: 0 auto; padding: 2rem; font-family: 'Georgia', serif; color: #222; line-height: 1.75; background: #fafaf8; }
h1 { font-size: 1.6rem; border-bottom: 2px solid #333; padding-bottom: 0.4rem; margin-top: 2rem; }
h2 { font-size: 1.2rem; color: #444; margin-top: 1.8rem; }
h3 { font-size: 1rem; color: #555; }
.paper-card { background: #f0ede6; border-left: 4px solid #8b7355; padding: 1rem 1.2rem; border-radius: 4px; margin: 1.2rem 0; }
.paper-card p { margin: 0.3rem 0; }
.claim-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.claim-table th { background: #e8e4db; text-align: left; padding: 0.5rem 0.7rem; }
.claim-table td { border-top: 1px solid #ddd; padding: 0.5rem 0.7rem; vertical-align: top; }
.badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.78rem; font-family: monospace; }
.badge-strong { background: #d4edda; color: #155724; }
.badge-weak   { background: #fff3cd; color: #856404; }
.badge-unsup  { background: #f8d7da; color: #721c24; }
.mermaid { margin: 1.2rem 0; }
blockquote { border-left: 3px solid #bbb; margin: 1rem 0; padding: 0.5rem 1rem; color: #555; font-style: italic; }
code { background: #f0ede6; padding: 0.1rem 0.3rem; border-radius: 2px; font-size: 0.88em; }
pre { background: #f0ede6; padding: 1rem; border-radius: 4px; overflow-x: auto; }
.tag { display: inline-block; background: #e8e4db; padding: 0.1rem 0.5rem; border-radius: 10px; font-size: 0.8rem; margin: 0.1rem; }
nav { position: sticky; top: 0; background: #fafaf8ee; border-bottom: 1px solid #ddd; padding: 0.5rem 0; margin-bottom: 1.5rem; font-size: 0.85rem; }
nav a { margin-right: 1rem; color: #5a4a3a; text-decoration: none; }
nav a:hover { text-decoration: underline; }
```

#### 内容规范

按**用户语言**（从调用 prompt 判断）生成所有章节：

1. **粘性导航栏** — 各节锚点链接。
2. **Paper Card** (`<div class="paper-card">`) — 标题、作者、venue/年份、来源链接、领域/任务、一句话论文、标签、阅读决策（精读/略读/跳过，附一行理由）。
3. **整体认知** — 问题、先前局限、核心思想、主要贡献、主要证据，3–5 短段散文。
4. **方法** — 优先放论文 Figure 1（架构图）的 `<img>` 标签（来自 Step 2 的 base64）。无 PDF 时用 Mermaid 流程图替代。行内 LaTeX 用 `$...$`，显示公式用 `$$...$$`。其他方法图紧跟讨论它的段落之后。
5. **证据账本** — HTML 表格，列：主张 / 证据 / 强度（strong/weak/unsupported badge）/ 注意事项 / 待验证。
6. **批判评价** — 优缺点、隐含假设、复现风险、缺失对照，双列表格或列表。
7. **研究用途** — 可复用的设计、应规避的设计、后续论文（附 arXiv 链接）、可能的研究方向。
8. **附录图** — 论文附录或后续页的额外图（如注意力可视化、消融图），`full_page: true` 的整页渲染放这里，不要混入正文节。
9. **页脚** — "Generated by mli-paper-reading skill · {date}" 小灰字。

保持分析性语气，不要填充废话。推断内容明确标注「（推断）」或「(inferred)」。

#### HTML 生成安全规则

1. **LaTeX 数学中的 `<` 和 `>` 必须转义为 `&lt;` 和 `&gt;`。** 浏览器在 MathJax 运行之前解析 HTML，`$...$` 或 `$$...$$` 中的裸 `<` 会被当作标签开口截断公式。正确写法：`$x_{\&lt;k}$`。
2. **中文及所有非 ASCII 字符直接写 UTF-8，不用 HTML 数字实体。** `&#27599;`（每）这类实体在字符串拼接时容易被截断，产生乱码。文件以 `charset=UTF-8` 服务，直接写汉字永远安全。

### Step 3：找空闲端口并起服务

```bash
PORT=7410
while lsof -i :$PORT >/dev/null 2>&1; do PORT=$((PORT+1)); done

python3 -m http.server $PORT --directory "$HOME/paper-notes" \
  --bind 127.0.0.1 >/tmp/paper-notes-server.log 2>&1 &
echo $! > /tmp/paper-notes-server.pid

for i in $(seq 1 10); do
  curl -s "http://localhost:$PORT/" >/dev/null 2>&1 && break
  sleep 0.5
done

echo "Serving at http://localhost:$PORT"
echo "Note: http://localhost:$PORT/${SLUG}.html"
```

### Step 4：打开浏览器

```bash
open "http://localhost:$PORT/${SLUG}.html"   # macOS
# Linux: xdg-open "http://localhost:$PORT/${SLUG}.html"
```

### Step 5：向用户报告并发起追问

浏览器打开后，**先报告结果**，再展示追问菜单，引导用户进一步深挖：

```
✅ 笔记已生成并在浏览器中打开
   地址：http://localhost:{PORT}/{slug}.html
   文件：~/paper-notes/{slug}.html
   停止服务：kill $(cat /tmp/paper-notes-server.pid)

────────────────────────────────
📖 想继续深挖？选一个方向：

  1. 🔬 方法深挖 — 逐公式拆解，写伪代码/推导步骤
  2. 🧪 实验审查 — 逐个质疑实验设计，找潜在缺陷
  3. 🔁 复现清单 — 输出可执行的复现 Recipe + 风险点
  4. ⚖️  对比分析 — 与指定论文做维度对比表
  5. 🗺️  文献地图 — 找前驱/后续论文，梳理研究谱系
  6. 💡 研究方向 — 在此基础上提出可做的 idea
  7. ❓ 自由提问 — 直接输入你的问题

回复数字或直接描述你的需求。
────────────────────────────────
```

用户选择后，针对性深化分析，并将新内容追加到同一 HTML 文件（不重新生成整个文件，只追加对应节）。
