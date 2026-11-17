# ppshu —— 用单文件 HTML 画图表达与交互

一个 WorkBuddy / OpenClaw 兼容技能：把任何想表达的东西做成**一张自包含 HTML 图**，
集中存到当前项目的 `.ppshu/` 文件夹，按 `001-描述.html` 序号管理，并可直接交互。

## 它能做什么

- 流程图 / 架构图 / 状态机（带判断/分叉/回环的流程图用 Mermaid 自动布局，其余内联 SVG）
- 折线 / 柱状 / 饼图（内联 Canvas 或 SVG）
- 可点击、可填表单的交互式 UI 原型
- **代码 / 文本对比审查报告**（`scripts/diff_report.py`：双栏 diff、差异块导航、SHA-256 可验证、成果三栏）
- 任何「想看而不是读」的可视化需求

## 安装（两种方式）

**方式一：本地导入（推荐先这样测）**
1. 拿到 `ppshu.zip`。
2. WorkBuddy 客户端：右上角头像 → `Claw设置` → `技能管理` → `+导入技能` → 选 ZIP。
3. 系统校验后确认导入，列表里启用 `ppshu` 即可。

**方式二：直接丢进技能目录（原生格式也兼容）**
把解压后的 `ppshu/` 文件夹放到：
- 用户级（跨项目）：`~/.workbuddy/skills/ppshu/`
- 项目级（团队共享）：`<项目>/.workbuddy/skills/ppshu/`
重新打开 WorkBuddy 即生效。

## 怎么用

对话里直接说，例如：
- 「画个登录流程图」
- 「用图对比单体架构和微服务」
- 「做个能填表单、能点的原型」

技能会自动：生成单文件 HTML → 用 `scripts/save_html.py` 存到
当前项目的 `.ppshu/NNN-描述.html` → 给你预览。你用浏览器打开那个 html
就能离线交互（无外链依赖）。带判断/分叉的流程图由 Mermaid 渲染，
其库（`mermaid.min.js`）已随技能打包、`save_html.py` 会自动复制到作品目录，
**同样完全离线、国内也不被墙**。要对比两份文件时，用 `scripts/diff_report.py`
生成 diff 审查报告页，同样存进 `.ppshu/`。

## 作品存哪、怎么找

默认全部在**当前项目的 `.ppshu/` 文件夹**（一眼可见，不用翻隐藏目录）。
该目录自动生成 `index.html` 画廊，列出所有作品，点开即可回看。
想清掉全部作品：直接删除这个 `.ppshu/` 文件夹即可。
想换位置：设环境变量 `PPSHU_DIR` 或给 `save_html.py` 传 `--dir`。

## 目录结构

```
ppshu/
├── manifest.json            # OpenClaw 导入元数据
├── prompt.md                # 技能正文（指令）
├── SKILL.md                 # 原生 WorkBuddy 格式（同内容）
├── README.md                # 本说明
├── scripts/
│   ├── save_html.py         # 自动编号 + 落盘 + 生成画廊（流程图自动复制 mermaid 库）
│   └── diff_report.py       # 代码/文本对比审查报告生成器（双栏 diff + SHA-256 可验证）
├── assets/
│   └── mermaid.min.js       # 随包发布的 Mermaid 库（约 3.3MB），流程图离线渲染用
└── references/
    ├── html_cookbook.md             # 单文件 HTML 画图规范
    └── mermaid_flowchart_template.html  # 决策/分支流程图模板（本地引用 mermaid.min.js）
```

## 许可证

MIT —— 随便改、随便发。
