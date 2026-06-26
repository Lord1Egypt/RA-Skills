# pandoc-docx

> 🔄 通过 pandoc 实现 Word (.docx) 与 Markdown 双向转换

---

## 📖 概述

基于 pandoc 的文档格式转换工具，支持 Word (.docx) 与 Markdown 之间的双向转换。

**核心能力：**
- ✅ 读取 Word (.docx) → Markdown
- ✅ 写入 Word (.docx) ← Markdown
- ✅ 格式转换 (.docx ↔ .md ↔ .pdf ↔ .txt ↔ .html)
- ✅ 批量处理
- ✅ 图片提取
- ✅ 格式保留（标题、粗体、列表、表格、代码）

**依赖：** pandoc (必需), libreoffice (可选，用于 .doc 支持)

---

## 🎯 触发条件

用户提到以下关键词时触发：

| 关键词 | 示例 |
|--------|------|
| "读取 Word" | "读取这个 report.docx" |
| "转为 Word" | "把这个 md 转为 word" |
| "docx 转 md" | "docx 转 md" |
| "创建 Word" | "创建一个 Word 文档" |
| "修改 docx" | "修改这个合同.docx" |
| "pandoc" | "用 pandoc 转换" |
| 文件路径包含 .docx | "处理 ~/documents/report.docx" |

---

## 🛠️ 支持格式

### 输入格式

| 格式 | 读取 | 写入 | 说明 |
|------|------|------|------|
| .docx | ✅ | ✅ | Word 2007+（主要支持） |
| .doc | ⚠️ | ⚠️ | 需要 libreoffice |
| .md | ✅ | ✅ | Markdown |
| .txt | ✅ | ✅ | 纯文本 |
| .pdf | ⚠️ | ❌ | 仅读取（需 pdftotext） |
| .html | ✅ | ✅ | HTML |

### 输出格式

| 格式 | 支持 | 说明 |
|------|------|------|
| .docx | ✅ | Word 文档 |
| .md | ✅ | Markdown |
| .pdf | ✅ | PDF（需 texlive） |
| .txt | ✅ | 纯文本 |
| .html | ✅ | HTML |
| .epub | ✅ | 电子书 |

---

## 🔄 核心流程

### 1. 读取 Word 文档

```
用户请求：读取 ~/report.docx
     ↓
检查文件格式 (.docx)
     ↓
调用 scripts/doc-read.sh
     ↓
pandoc report.docx -t markdown
     ↓
返回 Markdown 内容
     ↓
AI 分析/总结/处理
```

### 2. 写入 Word 文档

```
用户请求：创建 Word 文档
     ↓
AI 生成 Markdown 内容
     ↓
调用 scripts/doc-write.sh
     ↓
pandoc input.md -o output.docx
     ↓
返回 Word 文件路径
     ↓
确认完成
```

### 3. 格式转换

```
用户请求：docx 转 md
     ↓
检查源文件和目标格式
     ↓
调用 scripts/doc-convert.sh
     ↓
pandoc input.docx -o output.md
     ↓
返回转换结果
```

---

## 📝 使用方式

### 基础命令

```bash
# 读取文档
./scripts/doc-read.sh <文件路径> [格式]

# 写入文档
./scripts/doc-write.sh <输出文件> <输入文件|-> [格式]

# 格式转换
./scripts/doc-convert.sh <输入文件> -o <输出文件>

# 编辑文档
./scripts/doc-edit.sh <文件> <操作> [内容]
```

### 使用示例

```bash
# 读取 Word
./scripts/doc-read.sh ~/report.docx

# 创建 Word
echo "# 标题" | ./scripts/doc-write.sh ~/output.docx -

# 格式转换
./scripts/doc-convert.sh ~/input.docx -o ~/output.md

# 提取图片
./scripts/doc-convert.sh ~/input.docx -o ~/output.md --extract-media=./images

# 批量转换
for f in *.docx; do ./scripts/doc-convert.sh "$f" -o "${f%.docx}.md"; done

# 检查依赖
./scripts/check-deps.sh
```

---

## ⚠️ 依赖检查

### 必需依赖

| 工具 | 检查命令 | 安装命令 (Linux) | 安装命令 (macOS) |
|------|---------|-----------------|-----------------|
| pandoc | `pandoc --version` | `sudo apt install pandoc` | `brew install pandoc` |

### 可选依赖

| 工具 | 用途 | 安装命令 (Linux) | 安装命令 (macOS) |
|------|------|-----------------|-----------------|
| libreoffice | .doc 支持 | `sudo apt install libreoffice` | `brew install --cask libreoffice` |
| pdftotext | PDF 读取 | `sudo apt install poppler-utils` | `brew install poppler` |
| texlive | PDF 生成 | `sudo apt install texlive` | `brew install --cask mactex` |

---

## 📋 模板文件

### 文档摘要模板

```markdown
# 📄 文档摘要

**文件**: {filename}
**格式**: {format}
**大小**: {size}
**创建时间**: {created}
**修改时间**: {modified}

---

## 内容概览

- **标题数**: {heading_count}
- **段落数**: {paragraph_count}
- **表格数**: {table_count}
- **图片数**: {image_count}

---

## 核心内容

{content_summary}

---

**生成时间**: {timestamp}
```

---

## 🎯 典型场景

### 场景 1：读取并分析 Word 报告

```
用户：帮我分析这个季度报告 report.docx
     ↓
1. doc-read.sh report.docx
2. AI 分析内容
3. 生成摘要和洞察
```

### 场景 2：创建 Word 文档

```
用户：创建一个项目计划文档
     ↓
1. AI 生成 Markdown 内容
2. doc-write.sh plan.docx
3. 返回文件路径
```

### 场景 3：修改现有 Word

```
用户：把这个合同的甲方改为 ABC 公司
     ↓
1. doc-read.sh contract.docx
2. AI 修改内容
3. doc-write.sh contract-updated.docx
```

### 场景 4：批量转换

```
用户：把所有 Word 文档转为 Markdown
     ↓
1. 批量调用 doc-convert.sh
2. 返回转换结果列表
```

---

## ⚠️ 注意事项

### 格式保留

| 内容 | 保留度 | 说明 |
|------|--------|------|
| 标题层级 | ✅ 100% | H1-H6 完美转换 |
| 粗体/斜体 | ✅ 100% | **粗体** *斜体* |
| 列表 | ✅ 100% | 有序/无序列表 |
| 表格 | ✅ 95% | 简单表格完美，复杂表格可能简化 |
| 代码块 | ✅ 90% | 保留语言和格式 |
| 图片 | ✅ 100% | 需使用 --extract-media |
| 超链接 | ✅ 100% | 完美转换 |

### 可能丢失的内容

| 内容 | 说明 |
|------|------|
| 复杂样式 | 字体颜色、背景色等 |
| 页眉页脚 | Markdown 不支持 |
| 分页符 | Markdown 不支持 |
| 批注/修订 | 不转换 |
| 宏 | 不转换 |
| 合并单元格 | 可能简化为普通表格 |

### 最佳实践

1. **优先使用 .docx 格式**
   - .doc 需要 libreoffice，转换质量略低

2. **图片单独提取**
   ```bash
   pandoc input.docx -o output.md --extract-media=./images
   ```

3. **保留原始格式**
   ```bash
   pandoc input.docx -o output.md --wrap=preserve
   ```

4. **使用参考文档（保持样式）**
   ```bash
   pandoc input.md -o output.docx --reference-doc=template.docx
   ```

---

## 🔧 脚本说明

| 脚本 | 用途 | 参数 |
|------|------|------|
| `doc-read.sh` | 读取文档 | `<文件> [格式]` |
| `doc-write.sh` | 写入文档 | `<输出> <输入|-> [格式]` |
| `doc-convert.sh` | 格式转换 | `<输入> -o <输出> [选项]` |
| `doc-edit.sh` | 编辑文档 | `<文件> <操作> [内容]` |
| `check-deps.sh` | 检查依赖 | 无 |

---

## 📚 相关文档

- [supported-formats.md](./references/supported-formats.md) - 完整格式支持列表
- [pandoc-options.md](./references/pandoc-options.md) - pandoc 参数详解

---

## 🚀 快速开始

```bash
# 1. 检查依赖
./scripts/check-deps.sh

# 2. 读取 Word
./scripts/doc-read.sh ~/document.docx

# 3. 创建 Word
echo "# 标题" | ./scripts/doc-write.sh ~/output.docx -

# 4. 格式转换
./scripts/doc-convert.sh ~/input.docx -o ~/output.md
```

---

**版本**: 1.0.0  
**创建**: 2026-03-21  
**依赖**: pandoc >= 2.0  
**作者**: Cyber 🌟  
**许可**: MIT
