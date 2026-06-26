---
name: pdf-split
version: 1.0.1
description: 拆分 PDF 文件，支持单页拆分、页码范围和批量处理
metadata:
  openclaw:
    emoji: ✂️
    requires:
      bins:
        - node
    install:
      - kind: npm
        package: pdf-lib
---

# PDF Split Skill

拆分 PDF 文件为单个页面或多个部分，支持批量处理，本地处理。

## 使用方法

### 拆分为单页

```bash
node index.js split input.pdf --mode single -o output/
```

### 按页码范围拆分

```bash
node index.js split input.pdf --mode range --pages "1-3,5-7" -o output/
```

### 批量拆分

```bash
for f in *.pdf; do node index.js split "$f" --mode single -o "output/$f/"; done
```

## 功能特点

- ✅ 本地处理，文件不上传
- ✅ 支持拆分为单页
- ✅ 支持按页码范围拆分
- ✅ 支持批量处理
- ✅ 自定义输出目录
- ✅ 隐私安全

## 示例

### 拆分为单页

```bash
# 拆分 PDF 为单页
node index.js split document.pdf --mode single -o pages/

# 指定输出前缀
node index.js split document.pdf --mode single -o pages/ --prefix "page_"
```

### 按页码范围拆分

```bash
# 提取第 1-3 页
node index.js split document.pdf --mode range --pages "1-3" -o output/

# 提取第 1,3,5 页
node index.js split document.pdf --mode range --pages "1,3,5" -o output/

# 提取第 1-3 页和 5-7 页
node index.js split document.pdf --mode range --pages "1-3,5-7" -o output/
```

### 批量处理

```bash
# 拆分当前目录所有 PDF
for f in *.pdf; do
  node index.js split "$f" --mode single -o "output/$f/"
done
```

## 许可证

MIT

## 作者

fly3094
