# latex-modular 使用指南

## 触发词

- `把这段 LaTeX 做成模块化模板`
- `生成一个 LaTeX 文档，用模块化方式`
- `重构这个 LaTeX 代码进模块化体系`
- `提取 LaTeX 的组件，做成可复用模块`
- `用 latex-modular 生成一个...文档`
- `验证这段 LaTeX 能不能编译通过`
- `latex-modular` / `latex 模块化`

## 工作流程

### 模式 1: extract（提取组件）

从已有 LaTeX 源文件提取可复用组件到 `scripts/components/` 目录：

```bash
python scripts/extract.py <source.tex> --output-dir scripts/components/
```

**提取的组件分类**：

| 分类 | 目录 | 内容 |
|------|------|------|
| 文档类配置 | `scripts/components/preamble/class-settings.txt` | `\documentclass` 及选项 |
| 宏包引入 | `scripts/components/preamble/packages.txt` | 所有 `\usepackage` 行 |
| 颜色定义 | `preamble/colors.tex` | `xcolor`、`\definecolor` |
| 字体配置 | `preamble/fonts.tex` | `fontspec`、`\setmainfont`、`ctex` |
| 页面配置 | `preamble/geometry.tex` | `geometry` 宏包配置 |
| 作图支持 | `preamble/pgfplots.tex` | `pgfplots`、`tikz`、`siunitx` |
| 自定义环境 | `environments/*.tex` | `mylist`、`mycolumns` 等 |
| 自定义命令 | `commands/*.tex` | `\timu`、`\seeref` 等 |
| 章节样式 | `scripts/components/styles/section-style.txt` | `ctexset` 配置 |
| 目录样式 | `scripts/components/styles/toc-style.txt` | `tocloft` 相关配置 |
| 页眉页脚 | `scripts/components/styles/header-footer.txt` | `fancyhdr` 配置 |
| 表格样式 | `tables/*.tex` | `tabularx`、`booktabs` 等 |
| 图片插入 | `graphics/*.tex` | `graphicx`、`eso-pic` |

### 模式 2: compose（组合生成）

通过 Python 脚本按模块组合生成完整 LaTeX 文档：

```bash
python scripts/compose.py \
  --manifest scripts/components/manifest.json \
  --output output.tex \
  --body-file body.tex \
  --engine lualatex \
  --validate
```

组合顺序（自动处理依赖）：

1. 文档类声明（`scripts/components/preamble/class-settings.txt`）
2. 宏包引入（自动去重 + 按正确顺序排序）
3. 颜色/字体/页面配置
4. 自定义环境和命令
5. 章节/目录/页眉页脚样式
6. 文档正文（`\begin{document}` ... `\end{document}`）

### 模式 3: refactor（重构）

将原始 LaTeX 代码重构进模块化体系：

```bash
python scripts/refactor.py input.tex \
  --output-dir scripts/components/ \
  --output-doc output_modular.tex \
  --engine lualatex
```

重构过程：

1. 读取原始 .tex 文件
2. 分割为导言区和正文区
3. 按分类规则提取各组件到 `scripts/components/` 对应目录
4. 生成 `manifest.json` 组件索引
5. 生成模块化主文档（使用 `\input{}` 引入组件）
6. 编译验证（可选）

### 模式 4: validate（编译验证）

使用 lualatex 编译验证 .tex 文件：

```bash
python scripts/validate.py document.tex --engine lualatex --fix
```

验证内容：

- 编译是否成功生成 PDF
- 解析错误（Undefined control sequence、Missing $ inserted 等）
- 解析警告（Overfull `\hbox`、未定义引用等）
- 自动修复常见错误（可选 `--fix`）

### 模式 5: template（模板生成）

根据文档类型自动生成完整模板：

```bash
# 生成中文论文模板
python scripts/template.py --type article --title "论文标题" --author "作者" --output thesis.tex

# 生成技术报告模板（含目录）
python scripts/template.py --type report --title "项目报告" --author "作者" --output report.tex

# 只输出骨架，不生成示例正文
python scripts/template.py --type article --output skeleton.tex --no-sample

# 生成并编译验证
python scripts/template.py --type article --validate --engine lualatex
```

**参数说明**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--type` | article | 文档类型：article(论文) / report(报告) |
| `--title` | 文档标题 | 文档标题（中文/英文） |
| `--author` | 作者姓名 | 作者署名 |
| `--lang` | chinese | 语言：chinese / english |
| `--output` / `-o` | template_output.tex | 输出的 .tex 文件路径 |
| `--engine` | lualatex | LaTeX 引擎：lualatex / xelatex |
| `--output-mode` | tex | 输出模式：tex(保留已验证代码) / pdf(保留 .tex+.pdf) |
| `--skip-validation` | (默认验证) | 跳过编译验证（快速迭代用） |
| `--no-sample` | (生成示例) | 只输出骨架，不生成示例正文 |

**生成内容**：

- **article**（论文）：标题、摘要、关键词、引言、方法、实验、结论、参考文献样式
- **report**（报告）：标题、目录、项目概述、技术方案、实施计划、风险评估、总结

所有生成的模板都会自动展示各组件用法（mylist 列表、timu 命令、seeref 引用等）。

### 模板库管理

模板定义存储在 `scripts/templates/<name>.json`，内置 article/report 两种，支持用户自定义。

**模板库操作：**
```bash
python scripts/template.py --list-templates        # 列出所有模板
python scripts/template.py --show-template report  # 查看模板详情
python scripts/template.py --search 论文           # 搜索模板
```

**自定义模板：**
```bash
# 基于现有模板保存
python scripts/template.py --template article --save-as my-template --save-description '我的模板'

# 使用自定义模板生成
python scripts/template.py --template my-template --title '标题'
```

**注入自定义正文内容：**
```bash
python scripts/template.py --template article --content '\\section{引言}自定义内容'
```

**模板参数表（--template 代替 --type）：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--template` | -- | 按名称加载模板（scripts/templates/ 下） |
| `--type` | article | （兼容旧版）自动映射到同名模板 |
| `--content` | -- | 注入自定义正文内容（LaTeX 代码） |
| `--save-as` | -- | 将当前配置保存为新模板 |
| `--save-description` | -- | 保存模板时的描述 |
| `--list-templates` | -- | 列出所有可用模板 |
| `--show-template` | -- | 显示指定模板的详情 |
| `--search` | -- | 在模板库中搜索 |

## 组件库管理

使用 `scripts/component_manager.py` 管理组件库：

```bash
# 列出所有组件
python scripts/component_manager.py list --dir scripts/components/

# 添加组件
python scripts/component_manager.py add new_component.tex \
  --dir scripts/components/ \
  --category preamble \
  --name my-package \
  --desc "我的宏包配置"

# 删除组件
python scripts/component_manager.py remove preamble/my-package \
  --dir scripts/components/

# 显示组件内容
python scripts/component_manager.py show preamble/packages \
  --dir scripts/components/

# 验证所有组件
python scripts/component_manager.py validate --dir scripts/components/
```

## 输出格式

### 成功的 compose/refactor 输出

```
[compose] 加载 manifest: 12 个组件
[compose] 已生成: output.tex
[compose] 开始编译验证 (lualatex)...
[compose] ✓ 编译成功: output.pdf
```

### validate 验证报告

```
============================================================
  LaTeX 编译验证报告
============================================================
  文件: output.tex
  引擎: lualatex
  状态: ✓ 成功
  PDF:  output.pdf
------------------------------------------------------------
   ⚠️  警告 (2 条):
  [1] 引用未定义
       行号: 45
  [2] 行溢出（hbox 过宽）
============================================================
```

## 常见错误及修复

| 错误 | 原因 | 修复 |
|------|------|------|
| `Undefined control sequence` | 宏包未引入或命令拼写错误 | 检查 `\usepackage`，运行 `--fix` |
| `Missing $ inserted` | 数学公式未用 `$...$` 包裹 | 检查数学符号 |
| `Extra }` / `Missing }` | `{}` 不匹配 | 检查 `\begin{}` 和 `\end{}` 配对 |
| `Environment xxx undefined` | 环境未定义 | 添加对应 `\usepackage` |
| `File 'xxx' not found` | 图片/文件未找到 | 检查路径，使用绝对路径 |
| `Undefined color` | 颜色未定义 | 添加 `\usepackage{xcolor}` |
| `Font xxx not found` | 字体未安装 | 改用系统已有字体 |
| `Unicode character not set up` | 编码问题 | 使用 `\usepackage[UTF8]{ctex}` |

## 依赖

- Python 3.11+（推荐 3.13.12 managed）
- lualatex（系统已安装: `/c/Program Files/MiKTeX/miktex/bin/x64/lualatex`）
- 或 xelatex（可切换引擎）

## 文件路径

所有脚本使用 managed Python（版本由 WorkBuddy 运行时自动管理）执行：

```
<python> scripts/compose.py ...
```


## 快速用例

### 用例 1: 新建文档

用 article 模板生成一篇论文，自动编译为 PDF：



用 report 模板生成技术报告，只输出 .tex 不编译：



### 用例 2: 改造旧文章

将一篇 pdfLaTeX 老文章转换为 LuaLaTeX，直接输出（不入库）：

This is LuaHBTeX, Version 1.17.1 (MiKTeX 24.1)
 restricted system commands enabled.
! I can't find file `old_paper_lualatex.tex'.
<*> old_paper_lualatex.tex
                       
(Press Enter to retry, or Control-Z to exit)
Please type another input file name: 
! Emergency stop.
<*> 
 
 270 words of node memory still in use:
   1 hlist, 39 glue_spec nodes
   avail lists: 2:12,3:3,4:1,5:1
!  ==> Fatal error occurred, no output PDF file produced!
Transcript written on texput.log.

转换后同时入库和输出：



LuaLaTeX 文章直接入库（跳过 convert）：



### 用例 3: 增量编辑

写到一半的文章，加一个表格：

This is LuaHBTeX, Version 1.17.1 (MiKTeX 24.1)
 restricted system commands enabled.
! I can't find file `draft.tex'.
<*> draft.tex
          
(Press Enter to retry, or Control-Z to exit)
Please type another input file name: 
! Emergency stop.
<*> 
 
 270 words of node memory still in use:
   1 hlist, 39 glue_spec nodes
   avail lists: 2:12,3:3,4:1,5:1
!  ==> Fatal error occurred, no output PDF file produced!
Transcript written on texput.log.

给 pdfLaTeX 文档加图片（自动转换语法）：

This is pdfTeX, Version 3.141592653-2.6-1.40.25 (MiKTeX 24.1) (preloaded format=pdflatex.fmt)
 restricted \write18 enabled.
entering extended mode
! I can't find file `old_doc.tex'.
<*> old_doc.tex
               
(Press Enter to retry, or Control-C to exit)
Please type another input file name: 
! Emergency stop.
<*> 
    
!  ==> Fatal error occurred, no output PDF file produced!
Transcript written on texput.log.

### 用例 4: 组件复用

拆解已有文章 → 存入组件库：



用组件库组合生成新文档：



保存当前组件组合为模板，下次直接复用：



### 用例 5: 语义路由

测试路由是否能识别你的需求：



### 用例 6: 写入守卫

扫描所有脚本的违规直接写入：



检查单个文件是否有违规写入：


