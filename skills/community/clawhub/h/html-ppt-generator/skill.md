---
name: html-report-generator
description: 会自己设计PPT的智能报告技能，内置47套PPT模板（商务、科技、创意、学术、政府、金融等全场景覆盖），根据主题风格自由选配模板并自主设计，将任意输入拆解为5-15页精美HTML报告，每页严格1017×720px对齐PPT画布。当用户说"生成报告"、"分析内容做成页面"、"做成HTML"、"内容可视化"时立即使用，无需确认直接生成。
---

# HTML 报告生成器 · 主索引

按需读取，不要预加载所有文件。

---

## ⚡ 四条不可逾越的铁律

> 违反任意一条 → 该页推翻重做，无例外。

**铁律 1：画布锁死 1017×720px**
```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width:1017px; height:720px; min-width:1017px; max-width:1017px;
             min-height:720px; max-height:720px; overflow:hidden; }
```

**铁律 2：四区高度精确求和 720px**
```
Header  72px | Content 580px（仅左右 padding，上下禁止）| Summary 48px | Footer 20px
```

**铁律 3：不得 LibreOffice 渲染，必须 Chrome/Puppeteer 截图**

**铁律 4：每页 HTML 文件体积 ≥ 18KB**
内容页必须包含足量 CSS + 结构化卡片 + SVG 图表，封面/目录/结尾等特殊页 ≥ 8KB。
体积不足 = 内容偷懒，必须补充卡片正文、数据组件或 SVG 细节。

---

## 📂 文件索引（按需读取）

| 文件 | 职责 | 何时读 |
|------|------|--------|
| `references/01-canvas.md` | 画布、四区 CSS 骨架、溢出规则、高度铁律 4/5/6 | 每页生成前 |
| `references/02-design-system.md` | Tc 自创流程（Step 0→D）、风格文件索引、禁止清单 | 规划阶段第零步 |
| `references/03-layout.md` | Lc 自创流程、14 种布局基因库、高度计算规则 | 每页选布局时 |
| `references/05-content.md` | 反偷懒约束、三层内容结构、SVG 颜色规则、图表索引 | 写内容时 |
| `references/06-workflow.md` | S0 内容拆解、规划三元组、质量核查清单 | 开始+结束时 |
| `references/07-special-pages.md` | 封面/目录/章节/结尾页设计原则 + 变量映射（无 HTML 模板） | 生成特殊页时 |
| `references/09-components.md` | 页眉/摘要栏/卡片/徽章/数字排版规范 + Tc 变量映射（无 HTML 模板） | 每页组件选用时 |
| `references/10-diagram-types.md` | 业务图谱 5 族 44 种索引 + 网络查询流程 | 规划+写内容时 |

> 图表选型速查 → 见 `05-content.md`（统计图）· `10-diagram-types.md`（业务图谱）

---

## 🚀 完整生成流程

```
阶段零：读 06-workflow.md → 执行 S0-1~S0-4.5
  S0-1   联网查数据（核实，不估算）
  S0-2   主题定性（3 句话）
  S0-3   逐页内容指令（意图·气质·数据·原料）
  S0-3.5 逐页内容扩写（论点句·正文·数据组件·摘要栏）← 丰满度在这里
  S0-4   视觉规格声明（记忆点·背景三件套·禁止行为）
  S0-4.5 主题专属卡片语言设计（形状·线条·变体分工·装饰元素）← 新增强制步骤
  若用户已提供结构化 MD → S0-1/S0-2 可跳过，S0-3.5 仍须执行

阶段一（规划）：
  读 02-design-system.md → Step 0 自创 Tc 专属模板
    ★ Step B：尝试读取 design-system/[风格名].md
         文件存在 → 提取变量和卡片规格
         文件不存在 → 立即用 Write 工具新建该 .md 文件，再继续
  读 03-layout.md        → 了解 Lc 布局机制
  读 06-workflow.md      → 输出页码三元组规划表
  读 07-special-pages.md → 确认封面/结尾页需求
  读 10-diagram-types.md → 规划业务图谱

阶段二（逐页生成）：
  每页：01-canvas → Tc CSS（颜色/字体均来自 design-system）→ 03-layout（Lc）
       → 05-content → 09-components → 按需 svg-extended/ 或 diagram-types/
  ★ 卡片 CSS 必须应用 S0-4.5 定义的形状语言（切角/线条/装饰），禁止套用通用圆角壳

阶段三（验证）：
  读 06-workflow.md Phase 4 质检清单
```

---

## 📋 报告结构

```
P00 封面（可选）→ 07-special-pages.md 封面设计原则
P0N 目录（可选）→ 07-special-pages.md 目录设计原则
    章节分隔（可选）→ 07-special-pages.md 章节分隔原则
P01+ 内容页 × N（主流程）
PN  结尾页 → 07-special-pages.md 结尾页原则
```
