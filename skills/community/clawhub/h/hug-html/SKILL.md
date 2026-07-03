---
name: hug-html
tags: ['html', 'grid', 'template', 'visual-editor', 'module-library', 'style-presets', 'layout', 'chinese-error-handling']
version: 3.0.4
author: Ldxs
license: MIT
description: 8种原子组件自由组合 + 3级约束, cell merging, two-level module system (base + composite), 7+ built-in templates, grid-aware visual editor, style presets, post-generation audit, user template save-as, Chinese error handling
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/hug-html/data/
external_data_dir: true
trigger: 生成 HTML 模板/编辑 HTML/HTML 模块/网格布局/单元格合并/可视化编辑/输出自包含 HTML
trigger_negative: 只是简单文本编辑/不涉及 HTML 生成/使用其他框架
meta_field_sync: true
---
# hug-html

> → 详见 `references/antipatterns.md`
> → 详见 `references/faq.md`
> → 详见 `references/architecture.md`

## 触发场景

当用户提到以下内容时触发本技能：

- "生成 HTML 模板" / "HTML template" / "hug html"
- "编辑 HTML" / "可视化编辑 HTML" / "visual edit HTML"
- "HTML 模块" / "HTML module library"
- "网格布局" / "grid layout" / "N×M 网格"
- "单元格合并" / "rowspan" / "colspan"
- 输出格式：自包含 HTML 文件（毛玻璃卡片风格）

**复杂需求触发示例**（以下场景同样支持）：
- "我需要一个APP推广卡片，要有个二维码—可以用，支持"
- "帮我做一个带表格和参数配置的HTML面板—支持，用 data-table + param-panel 模块"
- "生成一个双端对比的推广页面—支持，用 header-dual + qr-dual"
- "这个模板我想保存下来以后用—支持，用 --save-as 固化"
- "给我生成的HTML加一个可视化编辑界面—支持，用 visual_editor.py"

**不触发**：
- 用户仅询问 HTML 语法概念，无文件生成需求
- 用户明确请求其他特定技能

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 能力 | 说明 |
|---|------|------|
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
| 13 | **向后兼容** | 旧格式 `"module": "composite:xxx"` 仍然支持 |
| 14 | **中文错误处理** | 所有脚本内置中文错误提示、参数校验前置、安全文件操作、调试模式 |

### 渐进式文件索引

| 文件名 | 位置 | 说明 |
|--------|------|------|
| `references/antipatterns.md` | 反模式 | 常见错误做法及正确做法 |
| `references/architecture.md` | 架构设计 | 四层架构体系详解 |
| `references/call-chains.md` | 调用链 | skill-sub 调用链定义 |
| `references/changelog.md` | 更新日志 | 版本历史变更记录 |
| `references/examples.md` | 示例 | 使用示例 |
| `references/faq.md` | FAQ | 常见问题解答 |
| `references/guide.md` | 使用指南 | 完整使用教程 |
| `references/module-library.md` | 模块库 | 组件系统 + 约束系统 |
| `references/permissions.md` | 权限说明 | 权限扫描报告和风险说明 |
| `references/style-presets.md` | 样式预设 | 样式预设系统说明 |

## 限制

> **明确这个技能能做什么、不能做什么，避免使用时"不知道支不支持"。**

### ✅ 支持的场景

| 场景 | 说明 | 示例触发词 |
|------|------|-----------|
| 生成推广卡片 | 应用推广、活动宣传、产品介绍的毛玻璃卡片 | "生成一个APP推广HTML卡片" |
| 生成信息面板 | 带表格、参数、二维码的信息展示面板 | "做一个带二维码和参数描述的HTML" |
| 生成可视化编辑模板 | 带 Ctrl+E 可编辑的 HTML | "生成一个可视化编辑的HTML模板" |
| 生成日历/周历仪表板 | 假日管理、年份控制、工日统计的交互仪表板 | "生成一个周历交互HTML" |
| 生成双端对比卡片 | 左应用右元服务/双实体的对比展示 | "生成一个双端推广卡片" |
| 内容填充 | 自动/手动填充 data-field 标记的文字和图片 | "给这个HTML模板填充示例内容" |
| 方案模板固化 | 将当前设计保存为可复用的用户模板 | "把这个模板保存为 my-card" |
| 自由创作 HTML | AI 参考模块库直接编写自包含 HTML | "帮我写一个毛玻璃风格的首页" |

### ❌ 不支持 / 不适合的场景

| 场景 | 为什么不支持 | 替代方案 |
|------|-------------|---------|
| 复杂前端应用（SPA / 数据可视化大屏） | 本技能面向静态 HTML+CSS 卡片，不支持路由/状态管理/API调用 | 手写 React/Vue 项目 |
| 多页面 HTML 站点 | 本技能是单页面自包含 HTML 生成器，不处理页面间导航 | 手写或使用静态站点生成器 |
| PDF / 图片输出 | 本技能输出 HTML 文件，不直接生成图片或 PDF | 生成 HTML 后用浏览器打印或截图 |
| 外部 CSS/JS 框架集成 | 本技能强调零外部依赖的自包含 HTML | 手动引入 CDN 或在 `scripts` 字段写自定义 JS |
| 非网格布局的自由排版 | 本技能基于 CSS Grid 网格系统，不适合绝对定位的自由排版 | 使用自由生成模式直接手写 HTML |
| 后端交互 / 数据库读写 | 本技能是纯前端 HTML，无后端能力 | 搭配 Node.js / Flask 等后端框架 |

### ⚠️ 需要注意的边界情况

| 情况 | 说明 |
|------|------|
| 网格越界 | 单元格的 row/col 索引 + rowspan/colspan 不能超过网格总行列数，否则 CSS Grid 会异常渲染 |
| 毛玻璃裁剪 | `backdrop-filter` 需要容器有 `overflow:hidden`，否则内容可能被裁剪 |
| JSON 模板路径 | `--spec` 参数支持绝对路径、相对路径和内置模板名；文件不存在会输出中文错误提示 |
| 文件编码 | 所有输入输出文件必须为 UTF-8 编码；其他编码可能导致乱码 |
| 编辑模式兼容性 | Ctrl+E 编辑模式需要现代浏览器（Chrome/Edge/Firefox），不支持 IE |

## 快速开始

```bash
# 列出所有组件类型（v3 新！）
python scripts/module_assembler.py --list-components

# 导出完整的组件接口定义
python scripts/module_assembler.py --export-interfaces "data/output/interfaces.json"

# 生成组件系统演示HTML
python scripts/module_assembler.py --demo

# 查看所有模板（向后兼容）
python scripts/grid_builder.py --list-templates

# 从内置模板生成 HTML
python scripts/template_generator.py --type harmony-app -o "data/output/card.html"

# 使用自定义 Grid Spec（支持新旧两种格式）
python scripts/grid_builder.py --spec "data/templates/3x3-merge.json" -o "data/output/grid.html"

# 导出完整接口定义（供大模型参考）
python scripts/grid_builder.py --export-interfaces "data/output/interfaces.json"
```

## 工作流程

本技能支持两种生成模式，**每次生成完成后必须输出生成说明**（`print_generation_guide()` 自动输出）：

### 模式 A：结构化模式（推荐）
1. **解析需求** — 理解用户需要的布局（行列数、合并、内容类型）
2. **选择/创建 Grid Spec** — 选择内置模板或用 JSON 定义自定义网格
3. **引用模块** — 从模块库中选择 base/composite 模块放入格子
4. **生成 HTML** — 调用 `grid_builder.py` 生成，**自动执行审计**
5. **生成编辑界面**（可选）— 调用 `visual_editor.py`
6. **内容填充**（可选）— 调用 `content_filler.py`
7. **输出结果** — 用 `preview_url` 展示，`deliver_attachments` 交付

### 模式 B：自由生成模式（省 token）

> **🛑 [MANDATORY] 每次生成完成后，必须阅读 `print_generation_guide()` 输出的生成说明并向用户展示。**
1. **参考模块库** — 先执行 `python scripts/grid_builder.py --list-modules` 查看可用的 base/composite 模块
2. **参考模板范例** — 先执行 `python scripts/grid_builder.py --list-templates` 查看内置模板风格
3. **参考样式预设** — 先执行 `python scripts/grid_builder.py --list-presets` 查看可用风格
4. **AI 自由生成** — 基于上述参考，直接编写自包含 HTML（使用 data-field 标记可编辑区域）
5. **保存到文件** — 使用 Write 工具写入 `data/output/`
6. **审计 [MANDATORY]** — 调用 `python scripts/grid_builder.py --audit <文件>`，不可跳过
7. **输出结果** — 用 `preview_url` 展示

> 自由生成模式适用场景：简单卡片、快速原型、不需要网格拆分的页面。
> 结构化模式适用场景：复杂网格布局、需要批量生产、可复用模板。

## 权限说明

| 工具 | 访问级别 | 用途 |
|------|----------|------|
| Read | 只读 | 读取 Grid Spec、模块库、样式预设 |
| Write | 写入 | 将输出 HTML 写入 `data/output/` |
| Bash | 受限 | 运行内部处理脚本（限制在 `scripts/` 目录内） |

- **不会**访问系统敏感路径或凭证文件
- **不会**向外部网络发送数据
- **不会**执行用户 Shell 配置文件
