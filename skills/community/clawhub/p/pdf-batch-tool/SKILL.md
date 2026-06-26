# PDF Toolkit - PDF 处理工具

## 功能描述
PDF 文件批量处理工具，支持合并、拆分、转图片、提取文字等操作。

## 使用场景
- 多个 PDF 合并为一个文件
- 大 PDF 拆分为多个小文件
- PDF 转图片 (PNG/JPG)
- 提取 PDF 文字内容
- PDF 加水印
- PDF 压缩

## 命令

### 合并 PDF
```
合并 PDF 文件列表=file1.pdf,file2.pdf,file3.pdf 输出=merged.pdf
```

### 拆分 PDF
```
拆分 PDF 文件=source.pdf 页码范围=1-10,15-20 输出=output.pdf
```

### PDF 转图片
```
PDF 转图片 文件=input.pdf 格式=PNG 输出目录=./images
```

### 提取文字
```
提取 PDF 文字 文件=input.pdf 输出=output.txt
```

### 添加水印
```
PDF 加水印 文件=input.pdf 水印文字=CONFIDENTIAL 输出=watermarked.pdf
```

### PDF 压缩
```
压缩 PDF 文件=input.pdf 质量=中 输出=compressed.pdf
```

## 输出格式
- PDF (.pdf)
- PNG (.png)
- JPG (.jpg)
- TXT (.txt)

## 特性
- 批量处理支持
- 保持原有质量
- 快速处理引擎
- 中文支持良好
