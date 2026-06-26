---
name: manual-to-solution
description: |
  将软件/系统操作手册转换为专业的系统解决方案建议书。适用场景：
  (1) 用户上传了一份操作手册/用户手册，要求转写为解决方案/方案建议书/投标方案
  (2) 需要从"功能描述"升维为"业务价值+技术架构+实施规划+ROI分析"的完整方案
  (3) 制作包含架构图、流程图、路线图等专业配图的方案文档
  触发关键词：操作手册转解决方案、手册升级、方案建议书、解决方案文档、转写方案

  Convert software/system operation manuals into professional solution proposals.
  Use cases:
  (1) User uploads an operation/user manual and needs it rewritten as a solution proposal or bid document
  (2) Elevating "feature descriptions" into a full proposal with business value, technical architecture, implementation planning, and ROI analysis
  (3) Producing proposal documents with professional diagrams (architecture, flowcharts, roadmaps, etc.)
  Trigger keywords: manual to solution, upgrade manual, solution proposal, solution document, rewrite proposal
---

# 操作手册→解决方案建议书 转换技能

将操作手册从"如何使用"升级为"为何使用、如何成功"的系统解决方案。

# Manual → Solution Proposal Conversion Skill

Transform operation manuals from "how to use" into "why use it and how to succeed" — a complete system solution proposal.

## 工作流程 / Workflow

### Step 1: 解析操作手册 / Parse the Manual

读取用户上传的操作手册（DOCX/PDF/Markdown），提取：

Read the user-uploaded operation manual (DOCX/PDF/Markdown) and extract:

- **系统名称与定位 / System name & positioning**
- **功能模块清单 / Feature module inventory**（一级+二级+功能要点 / L1 + L2 + key points）
- **用户角色 / User roles**
- **核心业务流程 / Core business processes**（审批链、状态机等 / approval chains, state machines, etc.）
- **技术特征 / Technical characteristics**（GIS、物联网、消息推送等 / GIS, IoT, push notifications, etc.）

### Step 2: 差距分析 / Gap Analysis

对照功能清单，识别：

Cross-reference the feature list and identify:

- ✅ 已覆盖的能力 / Capabilities already covered
- ⚠️ 需补充/扩展的能力 / Capabilities to supplement or extend（移动端、集成接口、智能推荐等 / mobile, integration APIs, smart recommendations, etc.）

### Step 3: 按七层框架生成方案 / Generate Proposal with the 7-Layer Framework

读取 `references/methodology.md` 获取完整方法论，按以下七层逐层展开：

Read `references/methodology.md` for the full methodology, then expand layer by layer:

```
操作手册 (What)                          Operation Manual (What)
  ↓
业务价值重构 (Why)                        Business Value Reframing (Why)
  ↓                                       → pain point mapping, quantified goals, scenario storylines
解决方案全景设计 (How↑)                    Solution Blueprint (How↑)
  ↓                                       → technical architecture, integration design
实施与运营规划 (How↓)                      Implementation & Operations Plan (How↓)
  ↓                                       → phased roadmap, WBS, risk management
保障体系构建 (With)                        Assurance Framework (With)
  ↓                                       → security & compliance, training & knowledge transfer
商业价值呈现 (For)                         Business Value Presentation (For)
  ↓                                       → TCO / ROI analysis
系统解决方案文档（交付物）                  System Solution Document (Deliverable)
```

### Step 4: 生成配图 / Generate Diagrams

运行 `scripts/generate_diagrams.py` 生成6类标准配图：

Run `scripts/generate_diagrams.py` to produce 6 standard diagram types:

```bash
python3 <skill_dir>/scripts/generate_diagrams.py <output_dir> [--font <font_name>]
```

生成的配图（PNG格式）/ Generated diagrams (PNG):

1. **技术架构图** / **Technical Architecture Diagram** — 六层/多层架构全景 / multi-layer architecture overview
2. **业务流程图** / **Business Process Diagram** — 核心审批/业务流程 / key approval/business flows
3. **实施路线图** / **Implementation Roadmap** — 分阶段时间线 / phased timeline
4. **投资回报图** / **ROI Chart** — 成本构成饼图 + 收益柱图 / cost breakdown pie + benefit bar chart
5. **价值映射图** / **Value Mapping** — 痛点→功能→价值对应关系 / pain point → feature → value mapping
6. **安全架构图** / **Security Architecture** — 安全体系五大支柱 / five pillars of security framework

**注意 / Note**：脚本需要 `matplotlib`。首次运行前执行：

The script requires `matplotlib`. Run before first use:

```bash
pip install matplotlib --break-system-packages -q
```

字体要求 / Fonts: 确保系统有中文字体（Noto Sans CJK SC / WenQuanYi / SimHei）。

Ensure Chinese fonts are available (Noto Sans CJK SC / WenQuanYi / SimHei).

用 `fc-list :lang=zh` 检查。如无中文字体，脚本将使用英文fallback。

Check with `fc-list :lang=zh`. If no Chinese fonts are found, the script falls back to English.

### Step 5: 构建DOCX文档 / Build DOCX Document

读取 `references/doc_structure.md` 获取标准文档结构模板。

Read `references/doc_structure.md` for the standard document structure template.

运行 `scripts/build_docx.py` 将方案内容和配图合并为DOCX：

Run `scripts/build_docx.py` to merge the proposal content and diagrams into a DOCX:

```bash
python3 <skill_dir>/scripts/build_docx.py <markdown_file> <images_dir> <output.docx> [--title <title>]
```

**注意 / Note**：脚本需要 `python-docx`。首次运行前执行：

The script requires `python-docx`. Run before first use:

```bash
pip install python-docx --break-system-packages -q
```

## 输出物 / Outputs

1. **Markdown版方案** / **Markdown version** — 便于编辑和版本控制 / easy to edit and version-control
2. **Word版方案** / **Word version** — 带配图的正式交付物（.docx）/ formal deliverable with diagrams (.docx)
3. **配图源文件** / **Diagram source files** — imgs/ 目录下的PNG图片 / PNG images in the imgs/ directory

## 自定义指南 / Customization Guide

### 不同行业的调整 / Industry-Specific Adjustments

方案框架通用，但需根据行业调整侧重点：

The framework is universal, but emphasis should shift by industry:

| 行业 / Industry | 侧重点 / Focus | 合规要求 / Compliance |
|------|-------|---------|
| 政府/事业单位 / Government | 合规审计、巡视迎检、标识化管理 / compliance audit, inspection readiness, asset labeling | 等保2.0、公务用车管理办法 / MLPS 2.0, govt vehicle regulations |
| 金融 / Finance | 数据安全、审计追溯 / data security, audit trail | 等保三级、银保监要求 / MLPS Level 3, CBIRC requirements |
| 制造业 / Manufacturing | 生产效率、设备利用率 / production efficiency, equipment utilization | ISO体系 / ISO standards |
| 医疗 / Healthcare | 患者安全、数据隐私 / patient safety, data privacy | HIPAA、等保 / HIPAA, MLPS |

### 配图自定义 / Diagram Customization

`generate_diagrams.py` 使用 matplotlib 生成，可通过修改脚本中的参数调整：

`generate_diagrams.py` uses matplotlib. Adjust by modifying parameters in the script:

- 颜色方案（修改 `colors` 字典）/ Color scheme (modify the `colors` dict)
- 图表尺寸（修改 `figsize`）/ Chart dimensions (modify `figsize`)
- 额外图表类型（添加新函数并在 `__main__` 中调用）/ Additional chart types (add new functions and call them in `__main__`)

### DOCX样式自定义 / DOCX Style Customization

`build_docx.py` 中可调整：

Adjustable in `build_docx.py`:

- 页面边距 / Page margins（`section.top_margin` 等）
- 字体 / Fonts（`set_run_font` 的 `name` 参数）
- 行距 / Line spacing（`line_spacing`）
- 表格样式 / Table styles（`table.style`）
