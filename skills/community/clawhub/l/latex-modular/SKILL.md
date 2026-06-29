---
name: latex-modular
data_dir: ../.standardization/latex-modular/data
version: 1.3.0
author: wUwproject
license: MIT
description: LaTeX 模块化组合技能。提取 LaTeX 文档头/组件（表格、图片、列表、章节样式）作为可组合模块，通过 Python 脚本稳定组合生成不报错的 lualatex 文档，支持从原始 LaTeX 代码重构进模块化体系。
tags: ['latex', 'modular', 'template', 'luatex', 'xelatex', 'document-generation', 'refactor']
trigger: ['latex-modular', 'latex 模块化', '模块化模板', 'LaTeX 文档 模块化']
trigger_negative: false
external_data_dir: false
sensitive_access: false
critical_write: false
permission_weight: LOW
h1_position: true
meta_field_sync: true
data_dir_compliance: true
---
# latex-modular

## 触发场景

### 文件更新约束

> **本技能的 `.md` 文件禁止使用 Write/Edit 工具更新。**
> 必须用 `scripts/` 下的 Python 脚本原子写入（`tmp + os.replace()`）。

| 文件 | 更新方式 | 脚本 |
|------|----------|--------|
| `SKILL.md` frontmatter | Python 原子写入 | `scripts/update_frontmatter.py` |
| `SKILL.md` 正文 | Python 直接重建 | `scripts/safe_write.py` 的 `safe_write()` |
| `scripts/components/*.txt` | Python 写入 | `scripts/component_manager.py` |
| `references/*.md` | `scripts/safe_write.py` | 随技能自带 |

- [把这段 LaTeX 做成模块化模板]
- [生成一个 LaTeX 文档，用模块化方式]
- [重构这个 LaTeX 代码进模块化体系]
- [提取 LaTeX 的组件，做成可复用模块]
- [用 latex-modular 生成一个...文档]
- [验证这段 LaTeX 能不能编译通过]

**不触发**：
- 用户只是问 [LaTeX 怎么写]——这是闲聊
- 用户要求直接编辑 .tex 文件而不使用模块化方式

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

- **extract 模式** — 从已有 LaTeX 代码中提取文档头、宏包、自定义命令、环境、样式，保存为可复用组件
- **compose 模式** — 通过 Python 脚本按模块组合生成完整 LaTeX 文档，确保编译无错误
- **refactor 模式** — 将原始 LaTeX 代码重构进模块化体系，保留原文语义，按模块拆分存储
- **validate 模式** — 使用 lualatex 编译验证生成的 .tex 文件，报告错误并返回修复建议
- **template 模式** — 模板库+自定义保存+内容注入。支持 `--template` 按名加载、`--save-as` 保存自定义模板、`--content` 注入正文、`--list-templates` 等，内置 article/report 两种预设模板（`scripts/template.py` + `scripts/templates/`）
- **inject 模式** — 向现有 .tex 增量插入组件，不破坏已有内容。自动将导言区内容追加到目标导言区，正文插入到指定位置。支持 LuaLaTeX/XeLaTeX 直接注入和 pdfLaTeX 语法动态转换（`scripts/component_inject.py`）
- **convert 模式** — 将完整的 pdfLaTeX 文档转换为 LuaLaTeX 兼容语法。原文件不动，输出新文件 + 转换报告（`scripts/convert.py`）

### 渐进式文件索引

| 文件 | 位置 | 说明 |
|------|------|------|
| `references/guide.md` | 使用指南 | 完整使用指南（触发词、工作流程、输出格式） |
| `references/architecture.md` | 架构说明 | 内部架构（组件分类、组合引擎、验证器） |
| `references/antipatterns.md` | 反模式 | 常见 LaTeX 错误 + 正确做法 |
| `references/faq.md` | FAQ | 常见问题解答（宏包冲突、字体问题、编译错误） |
| `references/changelog.md` | 更新日志 | 版本更新记录 |
| `references/component-spec.md` | 组件规范 | 命名、参数、依赖声明 |

### 脚本工具

| 脚本 | 功能 |
|------|------|
| `scripts/compose.py` | 模块组合引擎，按依赖顺序组合组件 |
| `scripts/extract.py` | 从 LaTeX 源文件提取组件 |
| `scripts/validate.py` | 编译验证，调用 lualatex 并检查输出 |
| `scripts/refactor.py` | 重构引擎，将原始 LaTeX 转为模块化结构 |
| `scripts/template.py` | 模板库管理 |
| `scripts/component_manager.py` | 组件库管理（增删改查） |
| `scripts/component_inject.py` | 增量注入：向现有 .tex 插入组件 |
| `scripts/convert.py` | 引擎转换：pdfLaTeX → LuaLaTeX |
| `scripts/workflow_router.py` | 语义路由：分析用户输入 → 匹配流程线 |
| `scripts/write_guard.py` | 写入守卫：扫描直接 open()/os.remove() 调用，强制使用 safe_write |
| `scripts/safe_write.py` | 原子写入工具 + safe_delete() 安全删除 |
| `scripts/workflow_state.py` | 流程守卫：步骤依赖检查 + 状态持久化 |
| `scripts/update_frontmatter.py` | 更新 SKILL.md frontmatter |

### 依赖

- Python 3.11+（推荐 3.13.12 managed）
- **LuaLaTeX**（默认，推荐）：组件库基于 LuaLaTeX 语法
- **XeLaTeX**：可通过 `--engine xelatex` 切换，组件库完全兼容
- **pdfLaTeX**：inject 模式支持动态转换为 pdfLaTeX 语法；convert 模式支持从 pdfLaTeX 转换为 LuaLaTeX
- **首次编译**时 MiKTeX 会自动安装缺失宏包，可能需要等待
- 中文字体依赖：SimSun、SimHei、KaiTi、FangSong（Windows 系统自带）

### 大文件处理

长篇 .tex 文件处理策略：
- 使用 `--lines START-END` 参数限定处理行范围，避免加载全文
- 支持 `--encoding` 指定文件编码（默认 utf-8）
- inject 模式下通过正则锚点或行号定位插入点，避免全文扫描
- validate 模式下流式读取编译输出，不分页

### 四流程线 + 语义路由

本技能内置 4 条流程线 + 独立模式，通过语义路由器自动匹配用户意图。

#### 执行协议（强制）

```
用户输入
  │
  ▼
语义路由器 (scripts/workflow_router.py)
  ├── 路由分析 → 匹配流程线或独立模式
  ├── 验证钩子 → 检查路由与输入语义的一致性
  │   ├── 高置信度 + 无冲突 → 走匹配路线
  │   └── 低置信度 + 有冲突 → 降级为独立模式
  └── 文件大小钩子 → 检测源文件体积
      ├── >500KB → 建议 --lines 分块
      └── >2MB  → 强制 --lines，拒绝无参数执行
  │
  ├── workflow 模式 → 严格步骤守卫 (workflow_state.py)
  │   每步执行前检查前置步骤是否完成，跳过则报错
  │   状态持久化在 .standardization/latex-modular/data/workflow_state/ 目录
  │
  └── standalone 模式 → 独立操作，无步骤约束
       AI 自行决断，不设守卫
```

#### 流程线定义

| 流程线 | 步骤链 | 强制备份 | 强制验证 | 报告 |
|--------|--------|---------|---------|------|
| **Line 1 创建文档** | template → inject_params → compose → **validate** → **report** | ❌ | ✅ | ✅ |
| **Line 2 改造** | **backup** → convert → branch → **final_validate** → **report** | ✅ 第一步 | ✅ | ✅ |
| **Line 3 增量编辑** | **backup** → inject → **final_validate** → **report** | ✅ 第一步 | ✅ | ✅ |
| **Line 4 组件复用** | extract → compose → template → reuse → **final_validate** → **report** | ❌ | ✅ | ✅ |
| **独立模式** | execute → **final_validate** → **report** | ❌ | 推荐 | ✅ |

#### 文件大小钩子

| 大小 | 级别 | 行为 |
|------|------|------|
| <500KB | normal | 正常处理 |
| 500KB~2MB | large | 建议使用 `--lines` 限定范围 |
| >2MB | huge | **强制** `--lines`，拒绝无参数执行 |

#### 相关脚本

- `scripts/workflow_router.py` — 语义路由 + 验证钩子 + 文件大小钩子
- `scripts/workflow_state.py` — 流程守卫：步骤依赖检查 + 状态持久化
- `scripts/workflow_report.py` — 结构化报告生成（Markdown 表格）

## 工作流程

### extract 模式（提取组件）

1. 读取用户提供的 LaTeX 源文件
2. 解析文档结构：导言区（\\documentclass 到 \\begin{document}）、正文区
3. 提取组件并分类保存到 `scripts/components/`：
   - `preamble/*.tex` — 宏包引入、颜色定义、字体配置
   - `environments/*.tex` — 自定义环境（mylist、mycolumns 等）
   - `commands/*.tex` — 自定义命令（\\timu、\\seeref 等）
   - `styles/*.tex` — 章节样式、目录样式、页眉页脚
   - `tables/*.tex` — 表格样式模板
   - `graphics/*.tex` — 图片插入模板
4. 生成组件索引 `scripts/components/manifest.json`

### compose 模式（组合生成）

1. 读取 `scripts/components/manifest.json` 获取可用组件列表
2. 根据用户需求选择所需组件
3. 调用 `scripts/compose.py` 按正确顺序组合：
   - 第1层：文档类声明
   - 第2层：宏包引入（自动去重）
   - 第3层：自定义命令和环境
   - 第4层：样式配置
   - 第5层：文档正文（用户提供）
4. 输出完整 .tex 文件

### 组件库结构

```
scripts/components/
├── manifest.json          # 组件索引
├── preamble/              # 导言区组件
│   ├── class-settings.txt
│   └── packages.txt
├── environments/          # 自定义环境
│   ├── mylist.txt
│   ├── mycolumns.txt
│   └── abstract-env.txt
├── commands/              # 自定义命令
│   ├── title-commands.txt
│   └── background.txt
├── styles/                # 样式配置
│   ├── section-style.txt
│   ├── toc-style.txt
│   └── header-footer.txt
├── tables/                # 表格模板
│   └── table-style.txt
└── graphics/              # 图片模板
    └── figure-insert.txt
```

### refactor 模式（重构）

1. 读取原始 LaTeX 文件
2. 解析并提取各组件到 `scripts/components/` 对应目录
3. 生成模块化版本的主文档（使用 \\input{} 或 \\include{} 引入组件）
4. 验证重构后文档编译通过

### validate 模式（编译验证）

1. 调用 `scripts/validate.py`
2. 使用系统 lualatex 编译 .tex 文件
3. 捕获编译输出，解析错误和警告
4. 返回结构化报告：成功/失败、错误位置、修复建议
