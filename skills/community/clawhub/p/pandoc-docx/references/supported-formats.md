# 支持的文档格式

## 输入格式

| 格式 | 扩展名 | 读取 | 写入 | 说明 |
|------|--------|------|------|------|
| **Word 2007+** | .docx | ✅ | ✅ | 主要支持格式 |
| **Word 97-2003** | .doc | ⚠️ | ⚠️ | 需要 libreoffice |
| **Markdown** | .md, .markdown | ✅ | ✅ | 原生支持 |
| **纯文本** | .txt | ✅ | ✅ | 原生支持 |
| **PDF** | .pdf | ⚠️ | ❌ | 仅读取，需 pdftotext |
| **HTML** | .html, .htm | ✅ | ✅ | 网页格式 |
| **EPUB** | .epub | ✅ | ✅ | 电子书格式 |
| **LaTeX** | .tex | ✅ | ✅ | 学术文档 |
| **reStructuredText** | .rst | ✅ | ✅ | Python 文档 |
| **Org-mode** | .org | ✅ | ✅ | Emacs 格式 |
| **MediaWiki** | .wiki | ✅ | ✅ | Wiki 格式 |
| **JSON** | .json | ✅ | ✅ | 数据结构 |

## 输出格式

| 格式 | 扩展名 | 支持 | 说明 |
|------|--------|------|------|
| **Word 2007+** | .docx | ✅ | 主要输出格式 |
| **Word 97-2003** | .doc | ⚠️ | 需要 libreoffice |
| **Markdown** | .md, .markdown | ✅ | 推荐输出格式 |
| **纯文本** | .txt | ✅ | 无格式文本 |
| **PDF** | .pdf | ✅ | 需 texlive |
| **HTML** | .html | ✅ | 网页格式 |
| **EPUB** | .epub | ✅ | 电子书 |
| **LaTeX** | .tex | ✅ | 学术排版 |
| **PowerPoint** | .pptx | ✅ | 演示文稿 |
| **DOCX 模板** | .dotx | ✅ | Word 模板 |

## 格式转换矩阵

```
          输出
输入      docx  md  pdf  txt  html  epub
docx      -     ✅   ✅   ✅   ✅    ✅
md        ✅    -    ✅   ✅   ✅    ✅
pdf       ❌    ❌   -    ✅   ❌    ❌
txt       ✅    ✅   ✅   -    ✅    ✅
html      ✅    ✅   ✅   ✅   -     ✅
epub      ✅    ✅   ✅   ✅   ✅    -
```

## 特殊说明

### .docx（Word 2007+）

**优势：**
- 完整格式支持
- 广泛兼容
- 可编辑性强

**限制：**
- 二进制格式（实际是 ZIP+XML）
- 需要 pandoc

### .doc（Word 97-2003）

**说明：**
- 旧格式，不推荐使用
- 需要 libreoffice 转换
- 可能丢失部分格式

**建议：**
- 优先使用 .docx
- 旧文档建议转换为 .docx

### Markdown

**优势：**
- 纯文本，易读易写
- 版本控制友好
- 转换质量高

**限制：**
- 不支持复杂样式
- 不支持页眉页脚

### PDF

**读取：**
- 需要 pdftotext (poppler-utils)
- 仅提取文本，格式丢失

**写入：**
- 需要 texlive
- 质量高，适合打印

## 最佳实践

1. **优先使用 .docx**
   - 最好的格式支持
   - 最少的兼容问题

2. **Markdown 作为中介**
   - 编辑和版本控制
   - 转换为其他格式

3. **避免循环转换**
   - .md → .docx → .md 可能丢失格式
   - 保留原始格式备份

4. **图片单独处理**
   - 使用 --extract-media
   - 图片保存在独立目录

## 相关资源

- [pandoc 官方文档](https://pandoc.org/)
- [pandoc 用户指南](https://pandoc.org/MANUAL.html)
- [LibreOffice 文档](https://www.libreoffice.org/)
