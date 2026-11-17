---
slug: "markdown-exporter-free"
name: "markdown-exporter-free"
version: "1.0.0"
displayName: "Markdown导出工具(免费版)"
summary: "Markdown转DOCX/PPTX/XLSX/PDF/HTML/IPYNB/CSV/JSON/XML多格式导出引擎。免费版,提供核心能力"
summary_zh: "Markdown转DOCX/PPTX/XLSX/PDF/HTML/IPYNB/CSV/JSON/XML多格式导出引擎。免费版,提供核心能力"
license: "MIT"
description: "|-. 适用于需要markdown exporter相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  Markdown文本多格式导出引擎（免费版），支持将Markdown转换为DOCX、PDF、HTML、
  XLSX、CSV、JSON等常用格式。核心能力：
  - 文档格式转换（md_to_docx/md_to_pdf/md_to_html）
  - 表格数据导出（md_to_xlsx/md_to_csv/md_to_json）
  - 演示文稿生成（md_to_pptx）
  - 代码块提取（md_to_codeblock，支持ZIP压缩）
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 文档处理
  - markdown
  - exporter
  - automation
  - productivity
  - 文档
  - 工具
  - path
  - markdown-exporter
  - input
category: "Development"
pricing_tier: free
---
# Markdown导出工具(免费版)

Markdown文本多格式导出引擎，支持将Markdown转换为DOCX、PDF、HTML、XLSX、CSV、JSON等格式.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Markdown导出工具(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API凭证 配置
本Skill无需额外API凭证（LLM能力由Agent平台内置提供）

### 可用性分类
- **分类**: MD+EXEC（）

## 核心能力

### 1. 文档格式转换
```bash
markdown-exporter md_to_docx /path/input.md /path/output.docx
markdown-exporter md_to_pdf /path/input.md /path/output.pdf
markdown-exporter md_to_html /path/input.md /path/output.html
markdown-exporter md_to_html_text /path/input.md
markdown-exporter md_to_md /path/input.md /path/output.md
```- 验证返回数据的完整性和格式正确性
- 参考`文档格式转换`的配置文档进行参数调优
### 2. 表格数据导出
将Markdown表格转换为结构化数据格式：
```bash
markdown-exporter md_to_xlsx /path/input.md /path/output.xlsx
markdown-exporter md_to_csv /path/input.md /path/output.csv
markdown-exporter md_to_json /path/input.md /path/output.json
markdown-exporter md_to_xml /path/input.md /path/output.xml
markdown-exporter md_to_latex /path/input.md /path/output.tex
```- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `表格数据导出` 选项
- 处理流程: 接收输入 -> 执行表格数据导出 -> 返回结果
- 输入: 用户提供表格数据导出所需的参数和指令

### 3. 演示文稿生成
```bash
markdown-exporter md_to_pptx /path/input.md /path/output.pptx
md /path/output.pptx --template /path/template.pptx
```
支持Pandoc风格的幻灯片语法：分栏布局（`::::: columns`）、演讲者备注（`::: notes`）、增量列表（`::: incremental`）、背景图片.
- 异常时参考错误处理章节进行恢复
- 关键参数: `演示文稿生成` 选项

### 4. 代码块提取
```bash
markdown-exporter md_to_codeblock /path/input.md /path/output_dir
md /path/output.zip --compress
```
从Markdown中提取所有代码块，按语言保存为独立文件（`.py`/`.js`/`.sh`等）。- 验证执行结果,确认输出符合预期格式
- 异常时参考错误处理章节进行恢复
- 关键参数: `代码块提取` 选项

#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---:|---:|---:|
| 技术文档导出 | Markdown文档 | `.docx` Word文档 |
| 数据表导出 | Markdown表格 | `.xlsx`/`.csv`/`.json` |
| 演示文稿制作 | Pandoc风格Markdown | `.pptx` PowerPoint |
| 代码提取 | 含代码块的Markdown | 独立代码文件或ZIP |

**不适用于**：加密文件破解、二进制文件转换、非Markdown格式间互转.
## 使用流程

1. 安装：`pip install md-exporter`
2. 准备Markdown输入文件（所有命令仅支持文件路径输入）
3. 选择目标格式对应的子命令
4. 执行转换：`markdown-exporter <subcommand> <input> <output> [options]`
5. 验证输出文件

## 示例

### 示例1：Markdown转Word
```bash
markdown-exporter md_to_docx /home/$USER/report.md /home/$USER/report.docx
```
输入 `report.md` 包含标题、段落、列表和表格，输出 `report.docx` 保留格式结构.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| `md_to_pptx` 输出幻灯片格式错乱 | Markdown未使用Pandoc幻灯片语法 | 确保每个 `##` 标题作为新幻灯片起始，分栏用 `::::: columns`，备注用 `::: notes` |
| `md_to_xlsx` 报 "no tables found" | 输入Markdown中无标准表格 | 确保表格使用 `| col |` 管道符格式，表头分隔行 `|---|---|` 必须存在 |
| `md_to_codeblock` 文件名冲突 | 多个代码块语言相同 | 输出文件自动编号：`block_1.py`、`block_2.py`，避免覆盖 |
| `md_to_pdf` 中文字体缺失 | PDF生成引擎未安装中文字体 | 安装中文字体包（如Noto Sans CJK），或使用 `md_to_html` 后通过浏览器打印为PDF |

## 常见问题

### Q1: 所有命令为什么只支持文件路径输入而不支持管道？
设计上要求所有输入为文件路径，确保大文件处理的稳定性和可重现性。如果需要处理管道输入的Markdown文本，先写入临时文件再调用命令：`echo "$markdown" > /tmp/input.md && markdown-exporter md_to_docx /tmp/input.md /tmp/output.docx`.
### Q2: `md_to_pptx` 支持哪些幻灯片布局？
支持Pandoc风格的幻灯片语法：标题+内容布局（`##` 标题后跟内容）、两栏布局（`::::: columns` + `::: column`）、比较布局（含图片的栏触发）、内容带说明（图片+caption）、增量列表（`::: incremental`）、空白布局（仅背景图+备注）。通过 `--template` 可使用自定义PPTX模板控制视觉风格.
### Q3: `md_to_codeblock` 如何处理代码块语言识别？
代码块的语言标注（如 ` ```python `）决定输出文件扩展名：`python`→`.py`，`javascript`→`.js`，`bash`→`.sh`，`sql`→`.sql`等。未标注语言的代码块默认输出为 `.txt`。使用 `--compress` 将所有代码块打包为ZIP，适合教程场景一次性分发所有示例代码.
## 已知限制

- 所有命令仅支持文件路径输入，不支持stdin管道
- 多表格/多代码块场景下输出文件自动编号
- PDF生成依赖系统字体配置，中文需额外安装字体

## 升级提示

本免费版提供基础功能。升级到完整版 markdown-exporter 获取全部能力和高级特性.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Markdown导出工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "markdown-exporter"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
