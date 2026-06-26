# kai-business-blueprint

> 售前需求、会议纪要、RFP 材料 → 可编辑的业务能力蓝图、泳道流程图、应用架构图。一份 canonical JSON IR，多个下游导出格式（SVG / draw.io / Excalidraw / Mermaid）。

适用于 [Claude Code](https://claude.ai/claude-code) 和 [OpenClaw](https://openclaw.ai) 的业务蓝图生成技能，将原始售前输入转化为结构化业务能力架构。

[English](README.md) | 简体中文

---

## 效果展示

零售行业蓝图，导出为 SVG 架构：

![retail-blueprint](demos/screenshots/retail-arch.svg)

该 SVG 由 `business-blueprint --export demos/retail.blueprint.json` 生成，源 JSON 在 `demos/retail.blueprint.json`，交互式查看器在 `demos/solution.viewer.html`。

---

## 设计理念：IR 优先管道

### 一、JSON 作为标准中间表示

所有工作流最终都收敛到 `solution.blueprint.json`——唯一的事实来源。所有其他产物（查看器、SVG、draw.io）都是从这个 JSON 确定性投影出来的。

```
原始文本 ──(--plan)──→ JSON ──(--generate)──→ 查看器 HTML
                          │
                          ├──(--export)──→ SVG / draw.io / Excalidraw / Mermaid
                          │
                          └──(--edit)────→ JSON（补丁日志）+ 查看器刷新
```

IR 文件的特点：
- **可版本管理**——标准 JSON，diff 有意义
- **AI 可读**——下游技能直接解析 `entities`、`relations`、`flowSteps`，不需要 HTML 解析
- **人类可编辑**——名称、标签等轻量字段可以直接修改，不会破坏结构

### 二、渐进式披露

技能文件（`SKILL.md`）是一个路由层——它告诉 Claude 在哪个命令下应该读哪个文件。重型资产（行业包、查看器 HTML 模板、导出引擎）只有在需要时才加载。

```
--plan        → 只需模型 + 生成规则；不加载 CSS 或导出引擎
--generate    → 一个 viewer.html 模板 + 一个行业包
--export      → 仅加载请求的导出引擎；其他格式保留在磁盘
--validate    → 仅加载 schema + 规则；不加载渲染代码
```

### 三、硅碳协作

**输入端：** 人类书写自然语言（需求、会议纪要、RFP），AI 解析为结构化实体（应用系统、业务能力、流程步骤、角色）和关系。

**输出端：** 查看器是纯静态 HTML——无需构建步骤、无 JS 框架、支持离线。每个节点都可以原地编辑，编辑操作记录为 JSON patch 日志（`solution.patch.jsonl`），确保完全可追溯。

---

## 安装

### Claude Code

```bash
git clone https://github.com/kaisersong/kai-business-blueprint ~/.claude/skills/kai-business-blueprint
```

然后：`cd kai-business-blueprint && pip install -e .`

### OpenClaw

```bash
git clone https://github.com/kaisersong/kai-business-blueprint ~/.openclaw/skills/kai-business-blueprint
cd kai-business-blueprint && pip install -e .
```

---

## 使用方式

### 命令行参数

| 参数 | 说明 |
|------|------|
| `--plan "文本"` | 将原始文本解析为标准蓝图 JSON |
| `--project <blueprint.json>` | 派生 canonical `solution.projection.json`，供下游技能消费 |
| `--generate <输出>` | 生成 JSON + 静态 HTML 查看器包 |
| `--edit <blueprint.json>` | 刷新现有蓝图的查看器（保留人工编辑） |
| `--export <blueprint.json>` | 导出 SVG、draw.io、Excalidraw、Mermaid 图表 |
| `--export-auto <blueprint.json>` | 使用内容路由 + 自由流式布局导出 SVG |
| `--validate <blueprint.json>` | 验证蓝图结构，输出错误/警告 |
| `--refine <blueprint.json>` | 基于自然语言反馈优化已有蓝图，配合 `--feedback "..."`。LLM 输出结构化 diff，自动应用产生新版本 |
| `--from <文件>` | 从指定文件读取源材料 |
| `--industry <包名>` | 指定行业模板包（`common`、`finance`、`manufacturing`、`retail`、**`cross-border-ecommerce`**） |

### Domain-Knowledge 蓝图（v0.14 新增）

除了原有的架构视角蓝图（capabilities / actors / flowSteps / systems），skill 新增 **domain-knowledge 蓝图**用于客户 know-how pitch：痛点、策略、规则、指标、最佳实践、常见误区六类实体，通过 `solves` / `measures` / `enforces` / `requires` / `prevents` / `causes` 等关系串联。

通过 `meta.blueprintType: "domain-knowledge"` 选定（用 `cross-border-ecommerce` 这类 know-how 行业模板时自动设定，或由 AI 意图抽取得出）。pipeline 内置三个质量驱动机制：

- **澄清回合**：domain-knowledge 蓝图必须包含 ≥3 条 `clarifyRequests`，每条都要指向具体实体；validator 在第一轮强制 AI 暴露不确定点。
- **实体自检**：每个 knowledge 实体可附 `_selfCheck` 字段（`passed` / `questions` 数组），`questions` 非空的实体在 SVG 中渲染为琥珀色边框 + `?` 标记，让 reviewer 一眼看出哪些点还需要确认。
- **修订命令**：`--refine blueprint.json --feedback "..."` 让 LLM 输出 `add` / `modify` / `delete` diff，应用后产生新版本。diff 结构类似 JSON Patch，可在应用前按操作筛选。

知识图渲染采用三段式布局：顶部规则 band、中部「痛点 → 策略 → 指标」三联画（按 `solves` / `measures` 关系行对齐，让主线接近水平）、底部「最佳实践 + 常见误区」胶囊。跨区域连接使用三阶贝塞尔曲线；关系按三档透明度分级，确保 30+ 关系密度下主线（solves / measures）依然清晰可读。

### 导出质量契约

- 导出路由现在是显式决策：只有当蓝图结构明确匹配某个专用视图时才会切过去，否则默认停在 `freeflow`。
- SVG 输出在落盘前会做结构完整性检查，先覆盖缺失 defs 引用和基础画布越界。
- 导出阈值和缺陷分类放在 [`evals/`](evals) 下，用 machine-readable 资产支撑 route 和 integrity 行为，而不是只靠文字说明。
- Windows / 终端支持是收敛范围的：推荐统一走 `python -m business_blueprint.cli`，遇到编码敏感场景时显式设置 `PYTHONIOENCODING=utf-8`。

### 典型工作流

**从原始文本开始：**
```bash
# 第一步：解析为标准 JSON
business-blueprint --plan "ERP 支持 POS 系统..." --from meeting-notes.md --industry retail

# 第二步：生成查看器
business-blueprint --generate solution.blueprint.json

# 第三步：导出图表
business-blueprint --export solution.blueprint.json
```

**编辑现有蓝图：**
```bash
# 手动编辑 JSON 或让 AI 编辑
# 然后刷新查看器（通过 editor.fieldLocks 保留人工编辑的字段）
business-blueprint --edit solution.blueprint.json
```

**导出前验证：**
```bash
business-blueprint --validate solution.blueprint.json
# 修复错误后：
business-blueprint --export solution.blueprint.json
```

**准备下游 machine handoff：**
```bash
business-blueprint --project solution.blueprint.json
```

---

## 输出产物

| 文件 | 角色 |
|------|------|
| `solution.blueprint.json` | 标准 IR——唯一事实来源 |
| `solution.projection.json` | 规范化的下游机器投影 |
| `solution.viewer.html` | 静态查看器 + 轻量编辑器 |
| `solution.exports/` | SVG、draw.io、Excalidraw、Mermaid 导出 |
| `solution.patch.jsonl` | 编辑追溯日志（JSON patches） |
| `solution.handoff.json` | viewer 修订版本清单 |

### SVG 架构导出

SVG 导出渲染三层架构图：

- **应用系统**（顶部）——ERP、CRM、POS 等
- **业务能力**（中间）——门店运营、会员管理、订单管理
- **流程步骤**（底部）——带能力关联的泳道流程图
- **角色**（右侧列）——与对应系统对齐的人员角色
- **语义箭头**——4 种类型，各有独立颜色/标记：`支撑`（绿色实线）、`依赖`（灰色虚线）、`数据流`（蓝色实线）、`负责`（黄色点线）
- **语义节点形状**——菱形用于流程步骤、左侧色条用于系统、圆角矩形用于能力、药丸形用于角色
- **行业主题**——零售（橙色）、金融（蓝色）、制造（灰色）叠加色

层高度通过两遍布局动态计算：第一遍放置所有节点，第二遍计算精确的内容高度，确保角色、多行流程、堆叠的能力永远不会溢出。

---

## 项目结构

```
kai-business-blueprint/
├── SKILL.md                      # 技能定义（路由层）
├── business_blueprint/           # Python 引擎（零外部依赖）
│   ├── cli.py                    # 命令行入口
│   ├── generate.py               # 从文本生成蓝图
│   ├── model.py                  # 数据模型与顶层结构
│   ├── projection.py             # 下游 projection 构建器
│   ├── validate.py               # 机器可读验证
│   ├── clarify.py                # 澄清请求构建器
│   ├── normalize.py              # 实体解析与同义词合并
│   ├── viewer.py                 # HTML 查看器写入器
│   ├── export_theme.py           # 共享导出主题 token 与语义颜色
│   ├── export_text.py            # 共享 SVG 文本测宽与换行 helper
│   ├── export_routes.py          # 显式导出路由决策
│   ├── export_integrity.py       # 导出结构完整性检查与 diagnostics
│   ├── export_svg.py             # SVG 导出器（两遍布局、内容路由、自由流式布局）
│   ├── export_drawio.py          # draw.io 导出器
│   ├── export_excalidraw.py      # Excalidraw 导出器
│   ├── export_mermaid.py         # Mermaid 导出器
│   ├── templates/                # 行业包（通用、零售、金融、制造）
│   ├── assets/                   # viewer.html 模板
│   └── specs/                    # 蓝图 schema 定义
├── references/                   # Schema、编写规则、行业包
├── tests/                        # 测试套件
├── demos/                        # 演示蓝图与导出
└── examples/                     # 示例蓝图 JSON
```

---

## 架构规则

引擎强制执行以下结构规则：

| 规则 | 说明 |
|------|------|
| **每个能力必须关联到系统** | 不允许孤立的能力 |
| **每个流程步骤必须关联到能力** | 不允许悬空的流程 |
| **角色 → 系统** | 角色必须引用有效的系统 ID |
| **无循环关系** | 系统 → 能力 → 流程 必须是有向无环图 |

运行 `--validate` 检查所有规则。警告表示潜在问题（如某个系统没有任何能力），错误会阻止导出。

---

## 面向 AI 智能体

其他技能应通过提示词编排来消费蓝图产物，而不是通过 viewer handoff manifest：

```
# 1. 先准备 machine artifacts
business-blueprint --plan solution.blueprint.json --from "..."
business-blueprint --project solution.blueprint.json

# 2. 再用提示词驱动 report-creator
"Use solution.blueprint.json and solution.projection.json to generate a report IR first. Do not render HTML yet."

# 3. 再用提示词驱动 slide-creator
"Use solution.blueprint.json and solution.projection.json to generate PLANNING.md first. Do not generate HTML yet."
```

可直接复用的提示词模板见 [references/prompt-orchestration-templates.md](references/prompt-orchestration-templates.md)。

`solution.handoff.json` 只用于 viewer manifest，不要把它当作 report / slide 的输入。

**提取结构化数据：**
```python
import json

with open("solution.blueprint.json") as f:
    bp = json.load(f)

# 系统
for sys in bp["library"].get("systems", []):
    print(f"系统: {sys['name']}")

# 能力
for cap in bp["library"].get("capabilities", []):
    print(f"能力: {cap['name']}")

# 关系
for rel in bp["relations"]:
    print(f"{rel['from']} --{rel['type']}--> {rel['to']}")
```

---

## 依赖要求

| 要求 | 版本 | 说明 |
|------|------|------|
| **Python** | >= 3.12 | 零外部依赖 |

---

## 兼容性

| 平台 | 版本 | 安装路径 |
|------|------|----------|
| Claude Code | 任意 | `~/.claude/skills/kai-business-blueprint/` |
| OpenClaw | >= 0.9 | `~/.openclaw/skills/kai-business-blueprint/` |

---

## 版本日志

**v0.14.0** — Domain-knowledge 蓝图：在原有架构蓝图（capabilities / actors / flowSteps / systems）之外，新增 know-how pitch 蓝图类型——痛点、策略、规则、指标、最佳实践、常见误区六类实体。pipeline 内置三大质量机制：**澄清回合**（validator 强制 ≥3 条指向具体实体的 clarifyRequests）、**实体自检**（每个实体可声明自身不确定项，渲染为琥珀色 `?` 标记）、**`--refine` 命令**（LLM 输出结构化 diff 自动应用产生新版本）。新增 `cross-border-ecommerce` 行业模板（深度验证），retail / finance / manufacturing 模板补充 `knowledgeHints`（标记 `template-only-not-domain-validated`，AI 使用时必须向用户披露此限制）。知识图渲染采用三段式布局（规则 band / 痛点-策略-指标三联画 / 实践-误区胶囊），按 `solves` / `measures` 行对齐，跨区使用三阶贝塞尔曲线，关系分三档透明度避免视觉过载。Free-flow 渲染器同步切换为贝塞尔曲线。新增 67 条单元测试（共 85 条），锁定 v2 行为。

**v0.13.0** — 意图解析与标签遮挡修复：将 `IntentResolver` + `RuleEngine` 集成到 SVG 导出 pipeline，使 layer 分配数据驱动；修复自由流式布局下标签与节点的视觉遮挡。

**v0.10.0** — 质量加固发布：新增显式导出路由决策与 SVG 完整性检查，并在 fallback 失败时返回结构化 diagnostics；补齐 `evals/` 下的 machine-readable 评测资产（阈值、缺陷分类、路由 fixture、评分 schema）；增强 CLI 对带空格路径、CRLF 输入和 UTF-8 校验输出的跨平台兼容；将共享导出文本/主题 helper 从 `export_svg.py` 中拆出；并修正演进时间线在暗黑主题下的卡片底色与多胶囊换行溢出问题。

**v0.9.0** — Canonical projection 发布：新增 `--project` 生成 `solution.projection.json`；补齐面向 report/slide 下游 skill 的 prompt-native 编排模板；明确非标准图形默认回退 `freeflow`；并完成一整轮 SVG 导出质量升级，覆盖海报图、泳道图、层次图、演进图，包括暗黑主题修复、标签避让、按宽度换行、卡片居中和新增回归测试。

**v0.8.0** — 技能重命名：从 `business-blueprint-skill` 更名为 `kai-business-blueprint`；更新所有 GitHub 链接、安装路径与文档引用。

**v0.7.0** — 视觉增强：4 种语义箭头类型（支撑/依赖/数据流/负责），各有独立颜色、虚线样式和 SVG 标记；语义节点形状（菱形用于流程步骤、左侧色条用于系统、圆角矩形用于能力、药丸形用于角色）；3 个行业主题叠加色（零售=#F97316、金融=#3B82F6、制造=#6B7280）；HTML 模板驱动查看器生成（替代 244 行 f-string 拼接）；架构布局修复——每个唯一能力独占一列；自由流式布局现在从 `blueprint.relations` 渲染完整关系箭头；同列箭头使用直接垂直路径；区域框覆盖所有系统节点；46 条新增测试。

**v0.5.0** — 内容路由与自由流式布局引擎：`_content_router()` 根据蓝图内容自动选择视图（架构图、能力地图、泳道图、流程链）；`_layout_free_flow()` 按域分组、自动换行计算节点位置；`export_svg_auto()` 组合路由+布局；新增 CLI `--export-auto` 参数；HTML 查看器现在动态显示可用视图的标签页。

**v0.4.0** — HTML 查看器与布局修复：自包含 HTML 查看器，内嵌三个 SVG 视图（架构图、能力地图、泳道图），标签页导航，汇总卡片，暗色主题支持网格背景。

**v0.3.1** — CLI 修复：`--from` 参数长中文文本不再触发 `File name too long`，`--plan` 支持 stdin 管道输入。

**v0.2.0** — SVG 布局引擎：两遍动态层高、角色溢出修复、标题层间距、标题遮挡修复、图例截断修复。

**v0.1.0** — 初始发布：plan/generate/edit/export/validate 管道；HTML 查看器支持原地编辑；SVG/draw.io/Excalidraw/Mermaid 导出；行业模板包（通用、零售、金融、制造）。
