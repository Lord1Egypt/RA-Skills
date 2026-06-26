# PDF QR Code Extractor

从 PDF 文件中提取每一页的图片，并检测、裁剪保存其中的二维码。

## 功能

- 将 PDF 每一页转换为图片
- 使用 OpenCV + pyzbar 检测并裁剪二维码区域
- 二维码周围留有 10 像素白边（padding），便于扫码识别
- 保存到指定目录

## 使用方法

```
请帮我提取 PDF 中的二维码：[PDF文件路径]
```

例如：
```
请帮我提取 PDF 中的二维码：D:/pdftest/text.pdf
```

或者指定输出目录：
```
请帮我提取 PDF 中的二维码：D:/pdftest/text.pdf，输出到 ./my_qr
```

## 依赖安装

需要先安装依赖：
```
pip install fitz PyMuPDF opencv-python numpy pyzbar --break-system-packages
```

## 输出结构

```
输出目录/
├── qr_page_1_1.png      # 二维码图片
├── qr_page_2_1.png
├── text.pdf_pages/       # PDF页面图片（中间文件）
│   ├── page_1.png
│   └── page_2.png
```

## 适用场景

客户提供的 PDF 文件中包含生成的二维码，需要批量提取保存。
