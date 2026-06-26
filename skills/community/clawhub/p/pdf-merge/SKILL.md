---
name: pdf-merge
version: 1.0.1
description: 合并多个 PDF 文件，支持压缩和元数据编辑（本地处理，隐私安全）
metadata:
  openclaw:
    emoji: 📄
    requires:
      bins:
        - node
    install:
      - kind: npm
        package: pdf-lib
---

# PDF Merge Skill

合并多个 PDF 文件为一个，支持压缩和元数据编辑，完全本地处理，隐私安全。

## 使用方法

### 基本合并

```bash
node index.js merge file1.pdf file2.pdf file3.pdf -o merged.pdf
```

### 带压缩

```bash
node index.js merge file1.pdf file2.pdf -o compressed.pdf --compress
```

### 添加元数据

```bash
node index.js merge file1.pdf -o output.pdf --title "文档标题" --author "作者名"
```

## 功能特点

- ✅ 本地处理，文件不上传
- ✅ 支持合并多个 PDF
- ✅ 支持 PDF 压缩
- ✅ 支持元数据编辑
- ✅ 保持原始质量
- ✅ 隐私安全

## 示例

### 合并文档

```bash
# 合并两个 PDF
node index.js merge doc1.pdf doc2.pdf -o merged.pdf

# 合并多个 PDF
node index.js merge *.pdf -o all.pdf
```

### 压缩 PDF

```bash
# 压缩单个 PDF
node index.js merge large.pdf -o small.pdf --compress

# 合并并压缩
node index.js merge doc1.pdf doc2.pdf -o output.pdf --compress
```

### 添加元数据

```bash
# 添加标题和作者
node index.js merge doc.pdf -o output.pdf --title "项目报告" --author "张三"

# 添加完整元数据
node index.js merge doc.pdf -o output.pdf --title "标题" --author "作者" --subject "主题" --keywords "关键词"
```

## 许可证

MIT

## 作者

fly3094
