---
name: pdf-watermark
description: "PDF 水印添加和移除功能，支持文本和图像水印"
auth: 午餐肉
---

# PDF 水印技能

## 功能
- 添加文本水印到 PDF
- 添加图像水印到 PDF  
- 移除 PDF 中的水印
- 批量处理 PDF 文件

## 使用方法

### 添加文本水印
```
说："给这个PDF添加水印 '机密文件'"
或："在PDF上添加水印，文字是公司名称，位置在右下角"
```

### 添加图像水印
```
说："给PDF添加logo水印"
或："用这个图片作为PDF水印"
```

### 移除水印
```
说："移除这个PDF的水印"
或："清除PDF中的所有水印"
```

## 技术依赖
- PyPDF2: PDF 操作
- reportlab: PDF 生成和水印绘制
- Python 3.8+

## 示例代码
```python
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_text_watermark(input_pdf, output_pdf, watermark_text):
    """添加文本水印到PDF"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # 创建水印
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 40)
        can.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.3)  # 灰色，半透明
        can.rotate(45)
        can.drawString(200, 100, watermark_text)
        can.save()
        
        # 合并水印
        packet.seek(0)
        watermark = PdfReader(packet)
        watermark_page = watermark.pages[0]
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)
```

## 文件格式支持
- 输入: PDF 文件
- 输出: 带水印的 PDF 文件
- 水印类型: 文本、图像 (PNG, JPG)

## 配置选项
- 水印文字、字体、大小、颜色、透明度
- 水印位置: 居中、四角、平铺
- 水印旋转角度
- 页面范围: 所有页、特定页
