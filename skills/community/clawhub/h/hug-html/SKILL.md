---
name: hug-html
tags: ['html', 'grid', 'template', 'visual-editor', 'module-library', 'style-presets', 'layout', 'chinese-error-handling']
version: 3.2.0
author: Ldxs
license: MIT
description: 8种原子组件自由组合 + 3级约束, cell merging, two-level module system (base + composite), 7+ built-in templates, grid-aware visual editor, style presets, post-generation audit, user template save-as, Chinese error handling
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/hug-html/data/
external_data_dir: true
trigger: 生成 HTML 模板/编辑 HTML/HTML 模块/网格布局/单元格合并/可视化编辑/输出自包含 HTML
trigger_negative: 仅询问概念/无文件生成需求/要求使用其他工具
meta_field_sync: true
create_permissions_md: true
license_compliance: true
---
# hug-html

> → 详见核心能力的渐进式文件索引
> → 详见核心能力的渐进式文件索引
> → 详见核心能力的渐进式文件索引

## 限制

- **本技能的能力边界分为支持场景、不支持场景和边界情况三类。**
- **生成推广卡片** — 应用推广、活动宣传、产品介绍的毛玻璃卡片。触发词："生成一个APP推广HTML卡片"
- **生成信息面板** — 带表格、参数、二维码的信息展示面板。触发词："做一个带二维码和参数描述的HTML"
- **生成可视化编辑模板** — 带 Ctrl+E 可编辑的 HTML。触发词："生成一个可视化编辑的HTML模板"
- **生成日历/周历仪表板** — 假日管理、年份控制、工日统计的交互仪表板。触发词："生成一个周历交互HTML"
- **生成双端对比卡片** — 左应用右元服务/双实体的对比展示。触发词："生成一个双端推广卡片"
- **内容填充** — 自动/手动填充 data-field 标记的文字和图片。触发词："给这个HTML模板填充示例内容"
- **方案模板固化** — 将当前设计保存为可复用的用户模板。触发词："把这个模板保存为 my-card"
- **自由创作 HTML** — AI 参考模块库直接编写自包含 HTML。触发词："帮我写一个毛玻璃风格的首页"

**不支持的场景：**
- **复杂前端应用** — 不支持路由/状态管理/API调用（替代：手写 React/Vue）
- **多页面 HTML 站点** — 不处理页面间导航（替代：静态站点生成器）
- **PDF / 图片输出** — 不直接生成图片或 PDF（替代：浏览器打印或截图）
- **外部 CSS/JS 框架集成** — 强调零外部依赖（替代：手动引入 CDN）
- **非网格布局的自由排版** — 基于 CSS Grid（替代：自由生成模式）
- **后端交互** — 纯前端 HTML，无后端能力。影响：数据持久化需额外方案。替代：搭配 Flask/Node.js

**边界情况：**
- **网格越界** — row/col + rowspan/colspan 不能超过网格总行列数。影响：CSS Grid 异常渲染
- **毛玻璃裁剪** — backdrop-filter 需要 overflow:hidden 容器
- **JSON 模板路径** — --spec 支持绝对/相对路径和内置名，不存在有中文错误提示
- **文件编码** — 必须 UTF-8，其他编码可能乱码
- **编辑模式兼容性** — Ctrl+E 需要 Chrome/Edge/Firefox，不支持 IE

## 触发条件

**正向触发：**
- "生成 HTML 模板" / "HTML template" / "hug html"
- "编辑 HTML" / "可视化编辑 HTML" / "visual edit HTML"
- "HTML 模块" / "HTML module library"
- "网格布局" / "grid layout" / "N×M 网格"
- "单元格合并" / "rowspan" / "colspan"
- 输出格式：自包含 HTML 文件（毛玻璃卡片风格）
- "我需要一个APP推广卡片，要有个二维码—可以用，支持"
- "帮我做一个带表格和参数配置的HTML面板—支持，用 data-table + param-panel 模块"
- "生成一个双端对比的推广页面—支持，用 header-dual + qr-dual"
- "这个模板我想保存下来以后用—支持，用 --save-as 固化"
- "给我生成的HTML加一个可视化编辑界面—支持，用 visual_editor.py"

**否定条件：**
- 不触发：用户仅询问 HTML 语法概念，无文件生成需求
- 不触发：用户明确请求其他特定技能

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 能力 | 说明 |
| --- |------| ------ |
| 1 | **骨架结构** | N×M 网格、行列数、单元格合并（rowspan/colspan）、gap 间距 |
| 2 | **骨架约束** | 3级约束（fill/fit/clip），递归传递到组件级别 |
| 3 | **组件体系** | 8种原子组件（text/image/icon/qrcode/table/divider/spacer/group），自由组合 |
| 4 | **组合逻辑** | 方向(row/column)、比例(ratios)、对齐(align)、8方向位置 |
| 5 | **方案模板库** | 内置 7+ 预置{骨架+组件+样式}组合 + **用户可自定义固化** |
| 6 | **样式预设** | 5 种内置风格：商务/科研/喜庆/丧事/技术，一键切换配色字体 |
| 7 | **基础编辑** | 每个文字元素独立控制：字体家族(8种)/字重(100-900)/字号(9-48px)/字色/透明度 |
| 8 | **图片编辑** | 点击输入URL + 拖放文件替换，所有图片组件均支持 |
| 9 | **生成后审计** | 自动检查 HTML 结构完整性、标签平衡、图片属性、网格越界、渲染风险 |
| 10 | **统一接口** | `--export-interfaces` 导出完整接口定义 JSON，大模型可直接理解 |
| 11 | **方案模板固化** | `--save-as <名>` 将任意生成固化为用户模板，后续按名引用 |
| 12 | **自由生成模式** | AI 参考组件库，理解需求确定骨架→组合组件→约束→生成→审计 |
| 13 | **参数约束** | 行列数 1-10, span≥1, gap 4-24px, 字号 9-48px, 字重 100-900 |
| 14 | **向后兼容** | 旧格式 `"module": "composite:xxx"` 仍然支持 |
| 14 | **中文错误处理** | 所有脚本内置中文错误提示、参数校验前置、安全文件操作、调试模式 |

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
|--------|------|----------|----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/architecture.md` | 架构设计 | skill-standardization 整体架构。包含：模块关系、数据流、核心设计决策。 | 无 |
| `references/call-chains.md` | 参考文档 | 本文件定义 `hug-html` 技能的调用链，供 `skill-sub` 读取和执行。 | 无 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、变更类型、修复项、升级说明。 | R-24 |
| `references/examples.md` | 使用示例 | 各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。 | R-25 C-17 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | 三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。 | 无 |
| `references/module-library.md` | 参考文档 | ``` | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/style-presets.md` | 参考文档 | `hug-html` 支持 5 种常见风格的样式预设，通过 `content_filler.py --preset` 应用。 | 无 |
## 快速开始

**场景：生成推广卡片**
用户需求：帮我做一个APP推广卡片，要有二维码，输出HTML文件
系统执行：
```bash
python scripts/template_generator.py --type promo -o "data/output/card.html"
```
系统输出：data/output/card.html — 毛玻璃风格推广卡片，含二维码、产品名、宣传语

**场景：可视化编辑**
用户需求：给这个卡片加一个在线编辑功能，输出可编辑HTML
系统执行：
```bash
python scripts/visual_editor.py --template data/output/card.html -o data/output/editor.html
```
系统输出：data/output/editor.html — 带Ctrl+E编辑界面，双击文字可修改

**场景：生成周历仪表板**
用户需求：做一个带假日管理的周历交互HTML，输出仪表板
系统执行：
```bash
python scripts/template_generator.py --type calendar-dashboard -o "data/output/calendar.html"
```
系统输出：data/output/calendar.html — 交互式周历，支持年份切换和工日统计
## 工作流程

本技能的执行流程包含以下编号列表（按顺序执行）：

- **① 解析需求** — 输入 用户需求描述 → 输出 需求规格
- **② 选择/创建 Grid Spec** — 输入 需求规格 → 输出 grid_spec.json
- **③ 引用模块** — 输入 grid_spec.json, modules/ → 输出 module_config.json
- **④ 生成 HTML** — 输入 grid_spec.json, module_config.json → 输出 *.html
- **⑤ 生成编辑界面（可选）** — 输入 *.html → 输出 editor.html
- **⑥ 内容填充（可选）** — 输入 editor.html → 输出 filled.html
- **⑦ 方案模板固化（可选）** — 输入 filled.html → 输出 interfaces.json
- **⑧ 输出结果** — 输入 最终 HTML → 输出 预览
## 权限说明

| 工具 | 访问级别 | 用途 |
| ------ |----------| ------ |
| Read | 只读 | 读取 Grid Spec、模块库、样式预设 |
| Write | 写入 | 将输出 HTML 写入 `data/output/` |
| Bash | 受限 | 运行内部处理脚本（限制在 `scripts/` 目录内） |

- **不会**访问系统敏感路径或凭证文件
- **不会**向外部网络发送数据
- **不会**执行用户 Shell 配置文件
- **不会**修改系统注册表或环境变量
- **不会**执行用户 Shell 配置文件

