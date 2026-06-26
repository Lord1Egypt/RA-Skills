# PDF QR Code Extractor

从 PDF 文件中提取二维码的工具。

## 安装依赖

```bash
pip install fitz PyMuPDF opencv-python numpy pyzbar --break-system-packages
```

## 使用方式

```bash
python scripts/extract_qr.py <PDF文件路径> [输出目录]
```

## 示例

```bash
# 默认输出到 ./qr_output
python scripts/extract_qr.py D:/pdftest/text.pdf

# 指定输出目录
python scripts/extract_qr.py D:/pdftest/text.pdf ./my_qr
```

## 改进说明

- 二维码周围留 10 像素白边，提高扫码成功率
- 自动创建输出目录
- PDF页面图片保存在子目录中，二维码直接保存在顶层
