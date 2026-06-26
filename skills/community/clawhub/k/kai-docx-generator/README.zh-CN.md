# kai-docx-generator

> 从 Markdown 生成专业的 .docx 文档——8 种风格预设，适用于合同、报告、红头文件等。或用 `{{placeholder}}` 变量填充现有 .docx 模板。

一个 Claude Code 技能，将 Markdown 转换为带样式格式的 Word 文档，或通过 XML 级扫描将数据填充到 .docx 模板中。

[English](README.md) | 简体中文

---

## 功能特性

### Markdown → .docx

| 功能 | 输入 | 输出 |
|------|------|------|
| 标题 | `#`, `##`, `###` | 1–3 级样式化标题 |
| 表格 | GFM 表格 | 100% 宽度，斑马纹，蓝色表头 |
| 列表 | `- item`, `1. item` | List Bullet / List Number 样式 |
| 代码块 | `` ```python `` | 等宽字体，灰色背景，语言标签 |
| 引用框 | `> text` | 彩色信息框（info/warning/success） |
| 图片 | `![alt](path)` | 嵌入图片，可选居中标题 |
| 分页符 | `<!-- pagebreak -->` | Word 分页 |
| 目录 | YAML front matter | 自动生成目录 |

### 风格预设

| 风格 | 适用场景 | 特点 |
|------|----------|------|
| `standard`（默认） | 通用文档 | 蓝色标题，11pt，1.15 倍行距 |
| `contract` | 合同/协议 | 正式，12pt，紧凑行距 |
| `report` | 商业报告 | 蓝色标题，10.5pt，专业 |
| `meeting` | 会议纪要 | 紧凑，10.5pt，偏行动项 |
| `business_letter` | 商务信函 | 传统信函格式 |
| `tech_spec` | 技术规格书 | 等宽字体，暗色友好 |
| `dispatch` | 红头文件 | 红色一级标题，28pt 固定行距 |
| `notice` | 通知公告 | 加粗，14pt，权威感 |

---

## 设计理念

### 1. 内容与样式分离

Markdown 内容从不直接引用颜色、字体或字号。它只声明结构（`# 标题`、`> 引用`），风格预设决定外观。同一个 Markdown 文件，`--style report` 和 `--style contract` 会生成完全不同的文档。

### 2. 风格驱动架构

每个风格预设配置：标题颜色/大小、段落间距、行距、字号。所有预设共用同一套渲染引擎——无重复代码。

### 3. CJK 字体处理

通过在每个 run 上设置 `w:eastAsia` XML 属性，确保中文/日文/韩文字符正确渲染。默认字体：Microsoft YaHei（Windows）/ PingFang SC（macOS 回退）。

### 4. 安全优先

| 威胁 | 防护 |
|------|------|
| 图片路径穿越 | 拒绝 `..` 和绝对路径 |
| 模板 XML 注入 | 转义 `&`、`<`、`>` |
| 输入耗尽 | 200KB Markdown，20 张图片，50×20 表格 |

---

## 安装

### Claude Code

告诉 Claude："安装 kai-docx-generator"

或手动：
```bash
pip install kai-docx-generator
```

### OpenClaw

```bash
# 通过 ClawHub 安装（推荐）
clawhub install kai-docx-generator

# 或手动克隆
git clone https://github.com/kaisersong/kai-docx-generator ~/.openclaw/skills/kai-docx-generator
```

> ClawHub 页面：https://clawhub.ai/kaisersong/kai-docx-generator

OpenClaw 首次使用时会自动安装所有依赖。

---

## 使用方式

### 基本命令

```bash
# 基础：Markdown → .docx
kai-docx-generate input.md output.docx

# 指定风格预设
kai-docx-generate --style report input.md output.docx

# 用 JSON 数据填充 .docx 模板
kai-docx-fill --data data.json --output output.docx template.docx

# 用 YAML front matter 填充
kai-docx-fill --data frontmatter.md --output output.docx template.docx

# 验证 .docx 结构
kai-docx-validate file.docx
```

### 典型工作流

**生成商业报告：**

```bash
# 1. 编写 report.md（含 YAML front matter）
# 2. 用 report 风格转换
kai-docx-generate --style report report.md report.docx
# → report.docx（蓝色标题，专业间距）
```

**填充合同模板：**

```bash
# 1. 准备 template.docx，含 {{甲方}}、{{金额}}、{{日期}}
# 2. 用 JSON 数据填充
kai-docx-fill --data contract-data.json --output signed.docx template.docx
# → signed.docx（所有占位符已替换）
```

**带目录、页眉页脚生成：**

```markdown
---
title: Q4 技术报告
author: 工程团队
date: 2026-04-10
header:
  text: 机密文件
  alignment: center
footer:
  page_number: true
toc:
  max_level: 3
---

# 执行摘要
...
```

```bash
kai-docx-generate --style tech_spec report.md report.docx
# → report.docx（含目录、页码、"机密文件"页眉）
```

---

## 功能特性

### Markdown 支持

| 元素 | 语法 | 渲染效果 |
|------|------|----------|
| 标题（H1–H3） | `#`, `##`, `###` | 预设样式，CJK 字体 |
| 段落 | 文字块 | 标准间距，富文本 runs |
| 加粗 / 斜体 | `**bold**`, `*italic*` | 逐 run 格式化 |
| 无序列表 | `- item` | List Bullet 样式 |
| 有序列表 | `1. item` | List Number 样式 |
| 表格 | GFM 管道表格 | 100% 宽度，斑马纹，蓝色表头 |
| 代码块 | 三反引号 | 等宽字体，灰色背景，语言标签 |
| 引用 | `> text` | 彩色引用框 |
| 图片 | `![说明](路径)` | 嵌入图片，居中标题 |
| 分页符 | `<!-- pagebreak -->` | Word 分页 |
| 分割线 | `---` | 底部边框线 |
| YAML front matter | `---\n...\n---` | 元数据、页眉、页脚、目录 |

### 模板填充

- 扫描文档正文、页眉、页脚、批注、脚注中的 `w:t` XML 节点
- 将 `{{占位符}}` 替换为提供的数据
- 数据清洗：去除控制字符、转义 XML、单值截断至 5000 字符
- 多调用安全：每次 `fill()` 调用前重置为原始模板状态

### 输入限制

| 资源 | 限制 | 超限行为 |
|------|------|----------|
| Markdown 大小 | 200 KB | 截断至 200 KB |
| 图片数量 | 20 | 丢弃超出部分 |
| 表格行数 | 50 | 截断至 50 行 |
| 表格列数 | 20 | 截断至 20 列 |
| 模板字段值 | 5000 字符 | 单值截断 |

---

## 依赖要求

| 依赖 | 用途 | 自动安装 |
|------|------|----------|
| Python >= 3.10 | 运行环境 | ❌ |
| `python-docx` >= 1.1.0 | Word 文档组装 | ✅ |
| `markdown-it-py` >= 3.0.0 | Markdown 解析（类 GFM） | ✅ |
| `lxml` >= 4.9.0 | XML 处理 | ✅ |
| `Pillow` >= 10.0.0 | 图片验证 | ✅ |
| `pyyaml` >= 6.0 | YAML front matter 解析 | ✅ |

---

## 兼容性

| 平台 | 版本 | 安装路径 |
|------|------|----------|
| Claude Code | 任意 | `~/.claude/skills/kai-docx-generator/` |
| OpenClaw | ≥ 0.9 | `~/.openclaw/skills/kai-docx-generator/` |

**适配的技能：**

| 技能 | 输出类型 | 消费方式 |
|------|---------|----------|
| kai-report-creator | Markdown 报告 | → 通过 kai-docx-generate 转 .docx |
| 任意 Markdown 源 | .md 文件 | → 生成带样式 .docx |
| 现有 .docx 模板 | `{{占位符}}` 模式 | → 通过 kai-docx-fill 填充 |

---

## 版本日志

**v0.1.0** — 初始发布：Markdown → .docx，8 种风格预设，XML 扫描模板填充，目录插入，输入限制，安全保护。
