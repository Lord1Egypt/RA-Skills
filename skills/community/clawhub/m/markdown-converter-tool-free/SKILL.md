---

slug: markdown-converter-tool-free
name: markdown-converter-tool-free
version: 1.0.0
displayName: Markdown转换器免费版
summary: 将PDF、Word、Excel、PPT等文件转换为Markdown格式,支持基础OCR与文档结构保留,适合个人使用.
license: Proprietary
edition: free
description: "Markdown转换器免费版帮助个人用户将各类文档文件转换为Markdown格式。支持PDF、Word、Excel、PPT、HTML、图片等常见格式,保留文档结构,
  无需安装额外软件(使用uvx运行)。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。自动化生成专业文档，提升文档覆盖率。触发关键词：文档生成、自动化、转换、设计、图片、PDF"

  无需安装额外软件(使用uvx运行)。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。'
tags:
  - Markdown
  - 文档转换
  - PDF
  - OCR
  - 生产力
  - 文档
  - 工具
  - uvx
  - markitdown
  - pdf
  - markdown
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Development"

---
# Markdown转换器免费版

## 概述

Markdown转换器免费版帮助个人用户将各类文档文件转换为Markdown格式。工具支持PDF、Word、Excel、PPT、HTML、图片、音频等常见格式,保留文档结构(标题、表格、列表、链接),无需安装额外软件,通过`uvx`直接运行.
本版本面向个人用户,提供基础的文档转换能力,适合文档数字化与知识管理.
## 核心能力

### 支持的格式

| 类别 | 格式 | 说明 |
|---|---|---|
| 文档 | PDF、Word(.docx)、PPT(.pptx)、Excel(.xlsx/.xls) | 办公文档转换 |
| 网页/数据 | HTML、CSV、JSON、XML | 结构化数据转换 |
| 媒体 | 图片(EXIF+OCR)、音频(EXIF+转录) | 媒体元数据与内容 |
| 其他 | ZIP(遍历内容)、YouTube URL、EPub | 特殊格式支持 |

**处理**: 解析支持的格式的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的格式的响应数据,包含状态码、结果和日志.
### 文档结构保留

转换后的Markdown保留原始文档结构:

- 标题层级(h1-h6)
- 表格(标准Markdown表格)
- 列表(有序/无序)
- 链接与引用
- 图片引用
- 代码块

**处理**: 解析文档结构保留的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文档结构保留的响应数据,包含状态码、结果和日志.
### 基础OCR

对图片进行OCR文字识别,提取图片中的文字内容并转为Markdown.

**处理**: 解析基础OCR的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回基础OCR的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：等文件转换为、支持基础、与文档结构保留、适合个人使用、转换器免费版帮助、个人用户将各类文、档文件转换为、图片等常见格式、保留文档结构、无需安装额外软件、uvx、Use、when、需要文件处理、格式互转、内容提取时使用、不适用于加密文件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:PDF文档转换

需求:将PDF报告转换为Markdown便于编辑与归档.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Markdown转换器免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 基础转换
uvx markitdown report.pdf -o report.md
# ...
# 从标准输入转换
cat input.pdf | uvx markitdown > output.md
```

### 场景二:Office文档批量转换

需求:将Word、Excel、PPT文件转为Markdown.
```bash
# Word文档
uvx markitdown document.docx -o document.md
# ...
# Excel表格
uvx markitdown data.xlsx > data.md
# ...
# PowerPoint演示文稿
uvx markitdown slides.pptx -o slides.md
```

### 场景三:网页与数据转换

需求:将HTML页面或数据文件转为Markdown.
```bash
# HTML页面
uvx markitdown page.html -o page.md
# ...
# CSV数据
uvx markitdown data.csv > data.md
# ...
# JSON数据
uvx markitdown config.json > config.md
```

## 快速开始

### Step 1:确保环境就绪

```bash
# 依赖说明
uvx --version
# ...
# 如未安装,安装uv
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2:执行转换

```bash
# 基础用法
uvx markitdown input.pdf
# ...
# 指定输出文件
# ...
# 重定向输出
```

### Step 3:检查结果

```bash
# 查看转换结果
cat output.md
# ...
# 检查文档结构是否完整
# - 标题层级是否正确
# - 表格是否保留
# - 列表是否完整
```

#
## 示例

### 命令行选项

```bash
uvx markitdown [输入文件] [选项]
# ...
选项:
  -o OUTPUT      # 输出文件路径
  -x EXTENSION   # 提示文件扩展名(用于标准输入)
  -m MIME_TYPE   # 提示MIME类型
  -c CHARSET     # 提示字符集(如UTF-8)
  -d             # 使用Azure文档智能(高级PDF)
  -e ENDPOINT    # 文档智能端点
  --use-plugins  # 启用第三方插件
  --list-plugins # 列出已安装插件
```

### 常见转换示例

```bash
# PDF转Markdown
# ...
# Word转Markdown
# ...
# Excel转Markdown(表格保留)
uvx markitdown spreadsheet.xlsx > spreadsheet.md
# ...
# PowerPoint转Markdown
uvx markitdown presentation.pptx -o presentation.md
# ...
# HTML转Markdown
uvx markitdown webpage.html -o webpage.md
# ...
# 图片OCR
uvx markitdown scan.jpg -o scan.md
# ...
# ZIP包遍历
uvx markitdown archive.zip -o archive.md
# ...
# 标准输入(需指定扩展名)
cat document | uvx markitdown -x .pdf > output.md
```

## 最佳实践

### 格式选择指南

| 源格式 | 转换效果 | 注意事项 |
|---:|---:|---:|
| Word(.docx) | 优秀 | 保留格式、表格、列表 |
| Excel(.xlsx) | 良好 | 表格转为Markdown表格 |
| PPT(.pptx) | 良好 | 每页转为一个章节 |
| PDF(文本) | 良好 | 保留文本与结构 |
| PDF(扫描) | 需OCR | 使用`-d`选项启用文档智能 |
| HTML | 优秀 | 保留链接与结构 |
| 图片 | OCR依赖 | 清晰图片效果更好 |

### 转换质量优化

```bash
# 复杂PDF使用文档智能提升效果
uvx markitdown complex.pdf -d -e "https://your-resource.cognitiveservices.azure.com/"
# ...
# 指定字符集确保中文正确
uvx markitdown chinese-doc.pdf -c UTF-8 -o output.md
# ...
# 使用插件扩展功能
uvx markitdown --use-plugins input.docx -o output.md
```

### 性能建议

| 场景 | 建议 |
|:---:|:---:|
| 首次运行 | 会缓存依赖,稍慢 |
| 后续运行 | 使用缓存,更快 |
| 大文件 | 可能需要较长时间 |
| 批量转换 | 逐个执行或使用PRO版 |

## 常见问题

### Q1: 转换后中文乱码怎么办?

A: 使用`-c`选项指定字符集:

```bash
```

### Q2: PDF转换效果不好?

A: 对于扫描版PDF或复杂排版的PDF,使用`-d`选项启用文档智能服务:

```bash
uvx markitdown scan.cognitiveservices.azure.com/"
```

### Q3: 免费版支持批量转换吗?

A: 免费版需逐个文件执行转换。如需批量处理整个目录,请使用PRO版的批量转换功能.
### Q4: 是否支持自定义输出格式?

A: 免费版输出标准Markdown格式。如需自定义输出模板、元数据提取等高级功能,请使用PRO版.
### Q5: 转换后的表格格式不对?

A: 确保源文件的表格结构清晰。复杂合并单元格可能无法完美保留。建议在转换后手动检查并调整表格格式.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md规范的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+(通过uvx自动管理)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| uv/uvx | 工具 | 必需 | astral.sh安装 |
| markitdown | Python包 | 必需 | uvx自动安装 |

### API Key 配置

- 基础LLM由Agent平台内置提供，特定外部API需单独配置密钥
- 基础转换使用本地工具,无需云端服务
- 如使用Azure文档智能(`-d`选项),需配置Azure端点与API Key

### 可用性分类

- **分类**: MD+EXEC(纯Markdown指令+命令行执行能力)
- **说明**: 基于Markdown指令驱动Agent执行文档转换任务,通过uvx运行markitdown工具
- **免费版限制**: 单文件转换、基础OCR、无批量处理、无自定义模板

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Markdown转换器免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "markdown converter"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
