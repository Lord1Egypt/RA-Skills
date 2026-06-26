---
name: html-visual-editor
version: "1.8.4"
description: "把任意静态 HTML 转成可视化编辑版：注入可拖动工具栏、颜色/字号/布局/风格面板、就地文字编辑、撤销保存导出干净版、元素与面板双向跳转、中英文 i18n、6 套场景风格 Prompt 一键复制给 AI 重塑样式。颜色面板数据驱动：扫 DOM 文字字符数 top 5 + 背景元素数 top 4 + 边框元素数 top 3，跨主题通用。适用于用户说可编辑版HTML、html可视化编辑、让html可编辑、样式面板、改html不写代码、所见即所得、点击直接编辑、把报告/页面/演示稿变成可调样式、给 AI 复制风格提示词。"
agent_created: true
---

# html-visual-editor

把任意静态 HTML 升级成「可视化编辑版」：文字可直接点开编辑，右侧面板可调颜色、字号、布局和主题预设，改完可导出新的 HTML。

## 一行使用

```bash
python <skill-dir>/scripts/adapt.py <your-report.html>
# 输出：<your-report>-editable.html
```

指定输出路径：

```bash
python <skill-dir>/scripts/adapt.py <your-report.html> -o <your-report>-editable.html --force
```

依赖只有一个：

```bash
pip install beautifulsoup4
```

## 生成后的能力

打开生成的 `*-editable.html`，页面会多出工具栏和右侧样式面板：

- **可拖动工具栏**：默认右上角，可拖动到任意位置，位置写入 `localStorage.hve_toolbar_pos`，刷新仍在。
- **文字编辑**：点击页面文字直接改；支持撤销、保存到浏览器、导出干净版。
- **颜色面板（v1.8 数据驱动）**：扫 DOM 所有文字节点的 computed color，按字符数加权聚合，输出 top 5 文字色 / top 4 背景色 / top 3 边框色；跨主题通用（蓝/红/绿主题都自动适配）。同色多变量自动联动。命名按使用频次：「主要 Primary / 次要 Secondary / 强调 Highlight / 装饰 Accent / 偶用 Subtle」。
- **字号面板（v1.7 收敛）**：≤10 个 slider，分 3 组（标题层级 / 正文层级 / 辅助）；自动合并 strong/upcoming/event/data 等同族选择器，避免堆砌。
- **布局面板**：7 个 slider，分 3 组——页面宽度 / 页面左右内距 / 段落最大宽 / 行高、章节间距、卡片间距 / 卡片内边距。命名清晰双语。
- **风格 Prompt（v1.5+）**：6 张场景风格卡片，点击不再改 CSS，而是**把风格描述 + 色板 + 硬约束的完整 prompt 复制到剪贴板**，让用户粘贴给任意 AI（Claude/ChatGPT/CodeBuddy）让 AI 重塑 CSS。6 套场景：云原生企业（产品汇报）、瑞士网格（咨询报告）、杂志编辑（品牌长文）、阳光手账（NGO/社区）、终端骇客（技术）、Y2K 可爱数字（创意）。
- **i18n（v1.8.3 双显）**：工具栏右上角「中 / EN」双显，激活态高亮、未激活半透明；首次加载根据 `navigator.language` 自动识别，写入 `localStorage.hve_lang`。
- **Pinned 弹窗 + 一键提取（v1.8.2+）**：hover 页面元素显示提示；按 P 固定后弹窗每行带色块/数值；自动检测元素颜色是否未提取为变量，按 A/B 类分流：
  - **A 类**（inline 写死）→ 橙色按钮「+ 一键提取为变量」→ 智能命名（基于色相 `--text-purple` 等）+ prompt 改名 + 直改 inline 为 `var()`，画面联动
  - **B/C/D 类**（CSS 规则 / 继承 / 复杂表达式）→ 蓝色按钮「📋 复制提示让 AI 改」→ 复制语义化 prompt 到剪贴板
- **导出干净版（v1.7+ ε 方案）**：toolbar 顶部「导出干净版 Export Clean」按钮——去掉编辑器、保留 data-editable（方便日后再次 adapt），同时把 inline 的 `var(--xxx)` 还原成 hex（剪贴到 Notion / 邮件 / 微信也不丢色），vars-style 块保留供完整网页渲染。
- **双向跳转**：hover 页面元素会提示可调项；点击提示会自动切到对应 tab 并高亮面板控件。

## 工作原理

```text
HTML
  ↓ parse_css.py        →  抽取 CSS 变量、font-size、background、color、选择器规则
  ↓ scan_dom.py         →  扫描 DOM；v1.8 数据驱动统计 color/bg/border 使用频次（top-N）
  ↓ generate_panel.py   →  生成颜色（top-N）/字号（≤10 收敛）/布局（7 项）面板 + 6 张 Style Prompt 卡片 + window.X 常量
  ↓ inject.py           →  注入可拖动 toolbar、panel、editor-core.css/js、i18n 字典，标记 data-editable
  ↓ verify.py           →  运行 sanity checks；失败则不产出坏件
```

## LLM 增强（可选）

不配置 API key 也能跑，启发式命名会兜底。若环境变量可用，会使用 LLM 给 CSS 变量生成更语义化的 label，例如「主色调 Accent」而不是「蓝色 Blue」。

支持的环境变量：

- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

## 兼容性

- **Level A，全自动**：HTML 内有 `<style>`，且 `:root` 里有 5 个以上 CSS 变量；效果最好。
- **Level B，降级可用**：CSS 变量少、外链 CSS、Tailwind/utility class 较多；文字编辑、字号/布局面板和数据驱动颜色 top-N 仍可用。inline 写死的色可通过 pinned 弹窗「+ 一键提取为变量」补救（A 类）。
- **Level C，部分受限**：几乎全是 inline style、canvas/iframe 主导。文字编辑可用；颜色面板靠 DOM 扫描仍能列出 top-N；建议先用 Style Prompt 让 AI 把 inline 重构为 CSS 变量后再二次 adapt。

## 安装位置

把整个 `html-visual-editor/` 目录放到对应工具可读取的位置：

- WorkBuddy / CodeBuddy：`~/.workbuddy/skills/html-visual-editor/`
- Claude Code：`~/.claude/skills/html-visual-editor/` 或项目级 skills 目录
- Cursor：放到任意项目目录，并在规则或说明中引用 `scripts/adapt.py`
- 手动使用：直接运行 `python /path/to/html-visual-editor/scripts/adapt.py <html>`

## 快速 demo

```bash
python <skill-dir>/scripts/adapt.py <skill-dir>/examples/demo-report.html --force --verbose
open <skill-dir>/examples/demo-report-editable.html
```

## 质量守门

`adapt.py` 会自动运行 sanity checks，重点覆盖：

- panel label 与 `PAGE_ELEMENT_TO_PANEL` row 字符级一致
- `PRESETS` 为 flat 格式，仅保留 `original`（v1.5+ 风格切换改为复制 prompt，不再 apply CSS）
- `HVE_STYLE_PRESETS` 包含 6 套场景风格 + palette + vibe 双语
- 字号 slider 数量 ≥ 4（v1.7 收敛策略：少而精，不再要求覆盖所有 font-size 规则）
- 字号 slider 优先用组合选择器；少数语义化裸 tag（th/td/p/h1/h2 等）允许直命中
- `data-editable` 覆盖率达标
- 无 `applyFallbackSize` / `applyFallbackLayout` 等绕开核心引擎的 shim
- 打包后无个人绝对路径依赖
- panel-actions 至少 1 个 action-btn

若检查失败，修源 HTML 或脚本，不要绕过检查。

## 文件结构

```text
html-visual-editor/
├── SKILL.md
├── README.md
├── LICENSE
├── assets/
│   ├── editor-core.css
│   ├── editor-core.js
│   └── panel.template.html
├── presets/
│   ├── builtin.json
│   └── llm_label_prompt.txt
├── scripts/
│   ├── adapt.py
│   ├── parse_css.py
│   ├── scan_dom.py
│   ├── generate_panel.py
│   ├── inject.py
│   ├── verify.py
│   └── utils/diagnose_css.py
└── examples/
    └── demo-report.html
```

## 实操原则

- 优先运行 `adapt.py`，不要手写 panel。
- 不修改 `assets/editor-core.js`，所有适配逻辑放在 scripts 和 window.X 常量里。
- 生成结果要先人工抽查：文字是否都可编辑、字号 tab 是否覆盖不同文字层级、预设是否明显生效。
