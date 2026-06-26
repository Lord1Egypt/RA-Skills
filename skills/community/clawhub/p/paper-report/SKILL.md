---
name: paper-report
description: Convert academic papers into structured Chinese reading reports with original figures. Supports arXiv HTML and local PDF inputs. For arXiv links, HTML mode is preferred for textual accuracy. Use when the user asks to summarize, read, analyze, or create a reading report for an academic paper (PDF file or arXiv link).
---

# Paper Reader

将学术论文转化为结构化的中文阅读报告。输入方式（`reader/`）与输出格式（`writer/`）独立解耦，详见末尾目录结构。

> **Python 约定**：`{PYTHON}` = macOS 用 `/Library/Developer/CommandLineTools/usr/bin/python3`，其他环境用 `python3`。

---

## Step 1: 路由决策

### 1.1 选择输出格式

- 用户明确指定 → 按用户要求。
- 用户未指定 → **默认 HTML**。

确定后**记住这个选择**，用于 Step 2 时分发到对应的 writer。

### 1.2 选择输入处理模式

两种模式完全独立，**不得混用**。规则：

**规则 1：用户提供本地 PDF 文件路径**
→ 使用 **PDF 模式**，跳转至 [reader/pdf.md](reader/pdf.md) 执行 P1–P5。

**规则 2：用户提供 arXiv 链接（不论 `/pdf/` 还是 `/html/` 形式）**
→ 优先尝试 HTML 模式。构造 HTML URL：将 `/pdf/` 替换为 `/html/`，并去掉末尾的 `.pdf`。
例：`https://arxiv.org/pdf/2605.12036` → `https://arxiv.org/html/2605.12036`

用 curl 检查页面是否存在：

```bash
curl -sI "https://arxiv.org/html/{ARXIV_ID}" | head -1
```

- 返回 `HTTP/... 200` → **HTML 模式**，跳转至 [reader/html.md](reader/html.md) 执行 H1–H3。
- 返回非 200（如 404）→ 回退到 **PDF 模式**，跳转至 [reader/pdf.md](reader/pdf.md) 执行 P1–P5。

**规则 3：用户提供其他 HTML 页面链接**
→ **HTML 模式**，跳转至 [reader/html.md](reader/html.md) 执行 H1–H3。

> 完成对应模式的步骤后，回到本文档继续 **Step 2**。

---

## Step 2: 生成中文阅读报告

完成输入处理后，`{workspace}/figures/` 已包含所有目标图表。

### 2.1 报告结构（参考框架，可根据论文内容灵活调整）

```
1. 论文基本信息（标题、作者、机构、发表信息）
2. 研究背景与动机
3. 核心方法 / 技术方案（配架构图）
4. 实验设计
5. 实验结果与分析（配结果图表）
6. 主要贡献与创新点
7. 局限性与未来方向
8. 个人点评与总结
```

**灵活性**：根据论文内容可增加章节（如 Case Study、数据集详解）、合并章节（如实验设计与结果合一）、自由组织子结构。

**附录内容集成**：

- "方法实现细节/超参数/训练配置" → **融入对应主方法章节**
- "补充实验/额外消融" → 融入实验结果章节或独立小节
- "独立子课题/独立证明" → 可设独立附录章节

### 2.2 图表选取原则

根据报告内容需要选取，**不设数量硬上限**：

- 架构图/流程图：必选（帮助读者建立全局理解）
- 主实验结果表/图：必选
- 关键消融/对比图：报告中有讨论则选入
- Case Study 截图：有说明价值则选入

### 2.3 通用写作要求

- 全文中文，术语首次出现时附英文原文，如"注意力机制（Attention Mechanism）"
- 图表引用："如图 1 所示，..." / "表 1 汇总了..."
- 严格基于原文，不添加原文未涉及的推测或数据
- 每章应有实质内容，避免泛泛而谈
- **不**包含"报告生成日期"或"AI 生成"相关文字

### 2.4 按输出格式分发

根据 Step 1.1 的输出格式选择，跳转到对应的 writer 文档：

- **HTML 输出** → [writer/html.md](writer/html.md)
- **Markdown 输出** → [writer/markdown.md](writer/markdown.md)

每份 writer 文档包含完整的：图片处理 / 数学公式 / 表格 / 模板路径 / 文件命名 / 写作风格 / 校验清单 / 已知陷阱。

---

## Step 3: 校验

按所选 writer 文档的**第 8 节"校验清单"**逐项检查。

**通用必检项**（任何格式都适用）：

- 各章节标题完整、层级清晰
- 章节有实质内容，无空段落或 `{{...}}` 占位符残留
- 无"报告生成日期"或"AI 辅助生成"文字

**如果发现问题**：直接修复对应文件，修复后重新保存到同一路径。

---

## 特殊情况处理

**超长论文（>20 页 / >50,000 字符）**：分批处理，先通读整体结构，再聚焦核心章节（方法、实验、结论）。

**双栏排版论文（PDF 模式）**：单栏图宽约 30–280 或 300–565 pt，跨栏图宽约 30–565 pt，调整裁剪坐标。

**扫描版 PDF**：文字模糊时通过图片阅读，报告中注明来源质量受限。

**论文含附录**：参照 Step 2.1 中"附录内容集成"处理。

---

## 文件结构参考

```
paper-report/
├── SKILL.md                    # 本文件（路由 + 通用流程）
├── reader/
│   ├── html.md                 # 输入处理：HTML 模式（H1–H3）
│   └── pdf.md                  # 输入处理：PDF 模式（P1–P5）
├── writer/
│   ├── html.md                 # 输出格式：HTML（9 节）
│   ├── html-template.html      # HTML 报告模板（含 MathJax）
│   ├── markdown.md             # 输出格式：Markdown（9 节）
│   └── markdown-template.md    # Markdown 报告模板
└── scripts/
    ├── pdf_to_images.py
    ├── crop_figures.py
    ├── extract_arxiv_text.py
    └── extract_figure_urls.py
```

> 新增输入源：在 `reader/` 加 `{name}.md`。新增输出格式：在 `writer/` 加 `{name}.md` + `{name}-template.{ext}`。SKILL.md 主流程无需改动。
