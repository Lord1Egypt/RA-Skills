# Image to PDF Merger Skill

将多张图片合并成一个 PDF 文档，适合处理会计凭证、扫描文件等。支持自动旋转调整方向。

## 依赖

```bash
# Python
pip3 install Pillow pypdf openpyxl

# 系统工具
brew install poppler tesseract tesseract-lang
```

## 触发条件

- 用户说"合并 PDF"、"把图片合成 PDF"、"生成 PDF"
- 用户发送多张图片并要求合并
- 用户发送 PDF 并要求添加摘要
- 用户发送扫描版 PDF 并要求"提取文字"、"总结"

## 使用方法

### 1. 收集图片/PDF

让用户一次性发送所有需要处理的 PDF，不要分开多次发。

### 2. 执行合并（图片转 PDF）

适用于图片文件（.jpg）：

```python
import os
from pypdf import PdfWriter
from PIL import Image

# 获取所有新上传的图片
images = sorted(glob.glob(f"{inbound_dir}*.jpg"), key=os.path.getmtime, reverse=True)[:20]

merger = PdfWriter()
for img_path in images:
    img = Image.open(img_path)
    # 自动旋转：横版图片旋转90度
    width, height = img.size
    if width > height:
        img = img.rotate(90, expand=True)
    pdf_path = img_path.replace('.jpg', '.pdf')
    img.save(pdf_path, 'PDF', resolution=100.0)
    merger.append(pdf_path)

output_path = f"{output_dir}{凭证号}.pdf"
merger.write(output_path)
```

### 3. PDF 重命名（带完整摘要 + 船名归属）

根据 Excel 清单自动重命名 PDF：

**Excel 结构：**
- F列 = Index（凭证序号）
- H列 = 摘要（Description）
- M列 = 船名/归属

**关键：使用字母索引法，避免列号混淆！**

```python
import openpyxl
import re
import shutil
import os

# Excel 路径
excel_path = "~/.openclaw/media/inbound/Vouching_list---*.xlsx"

# 加载 Excel（使用字母索引）
wb = openpyxl.load_workbook(excel_path)
ws = wb.active

# 需要处理的文件列表 (序号, 原始文件名)
files = [
    (1, "1._1月79号---xxx.pdf"),
    (2, "2_1月109号---xxx.pdf"),
    # ...
]

for idx, filename in files:
    # Index N -> Excel Row N+1（因为 Row 1 是表头）
    excel_row = idx + 1
    
    # 使用字母索引直接访问列
    desc = ws[f'H{excel_row}'].value    # H列 = 摘要
    ship = ws[f'M{excel_row}'].value    # M列 = 船名归属
    
    # 从文件名提取凭证号（如 "1月79号"）
    date_match = re.search(r'(\d+月\d+号)', filename)
    date_part = date_match.group(1) if date_match else ""
    
    # 命名格式：序号_凭证号-【船名】摘要.pdf
    # 例如：01_1月79号-【祥瀚8】V2501运费收入.pdf
    new_name = f"{idx:02d}_{date_part}-【{ship}】{desc}.pdf"
    
    # 复制并重命名
    src = os.path.join(inbound_dir, filename)
    dst = os.path.join(output_dir, new_name)
    shutil.copy(src, dst)
```

**文件名格式规范：**
```
序号_凭证号-【船名/公司】摘要.pdf

示例：
01_1月79号-【祥瀚8】V2501运费收入.pdf
02_1月109号-【River】坞修2411001.pdf
03_1月135号-【Alice】2503航次收入.pdf
04_1月169号-【Anna】DBS融资款付船款.pdf
```

### 4. 发送到 Telegram

```python
message(
    action="send",
    filePath=output_path,
    message=f"{序号}. {凭证号} - 【{船名}】{摘要}",
    target="用户ID"
)
```

## 关键要点

1. **一次性收集** - 让用户一次发完所有文件
2. **使用字母索引** - 用 `ws[f'H{row}']` 而非 `row[7]`
3. **正确映射** - Index N → Excel Row N+1
4. **完整命名** - 序号_凭证号-【船名】摘要
5. **自动发送** - 处理完成后自动推送给用户

## 错误处理

- 如果 Excel 找不到对应 Index，跳过或用原文件名
- 如果 PDF 是图片合并的（无文字层），使用 OCR 功能提取文字
- 文件名中的特殊字符（如 `/`）需要清理

---

## 功能三：扫描版 PDF OCR 文字提取

当用户发送扫描版 PDF（无文字层）时，使用 tesseract 提取文字：

### 步骤 1：PDF 转图片

```bash
# 安装依赖
brew install poppler tesseract tesseract-lang

# PDF 转图片（300 DPI）
pdftocairo -png -r 300 input.pdf page
```

### 步骤 2：OCR 识别

```bash
# 识别中文+英文
tesseract page-01.png stdout -l chi_sim+eng > output.txt

# 批量识别
for p in page-*.png; do
  tesseract "$p" stdout -l chi_sim+eng >> combined.txt
done
```

### 步骤 3：提取关键信息

```python
import re

# 读取 OCR 结果
with open('combined.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# 提取关键信息（根据文档类型调整）
patterns = {
    '贷款人': r'([A-Z]+ BANK LTD\.?.*?)\n',
    '借款人': r'([A-Z]+ SHIPPING LIMITED.*?)\n',
    '贷款金额': r'USD([\d,]+)',
    '利率': r'([\d.]+)%',
    '期限': r'(\d+)\s*years?',
}

results = {}
for key, pattern in patterns.items():
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        results[key] = match.group(1) if match.lastindex else match.group(0)

print(results)
```

### 完整流程脚本

```bash
#!/bin/bash
# pdf-ocr.sh - 从扫描版 PDF 提取文字

PDF_PATH="$1"
OUTPUT_DIR="/tmp/pdf_ocr_$(date +%s)"

mkdir -p "$OUTPUT_DIR"

# 1. PDF 转图片
echo "Converting PDF to images..."
pdftocairo -png -r 300 "$PDF_PATH" "$OUTPUT_DIR/page"

# 2. OCR 识别
echo "Running OCR..."
> "$OUTPUT_DIR/combined.txt"
for img in "$OUTPUT_DIR"/page-*.png; do
    echo "Processing: $img"
    tesseract "$img" stdout -l chi_sim+eng 2>/dev/null >> "$OUTPUT_DIR/combined.txt"
done

# 3. 提取关键信息
echo "Extracting key information..."
python3 << 'EOF'
import re

with open('$OUTPUT_DIR/combined.txt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

patterns = {
    'lender': r'([A-Z]+ BANK LTD\.?.*?)\n',
    'borrower': r'([A-Z]+ SHIPPING LIMITED.*?)\n',
    'amount': r'USD([\d,]+)',
    'date': r'(\d{1,2}\s+\w+\s+\d{4})',
}

for key, pattern in patterns.items():
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        print(f"{key}: {match.group(1)}")
EOF

echo "Output saved to: $OUTPUT_DIR/combined.txt"
```

## 改进：处理延时

为避免图片传输不完整，添加等待机制：

```python
import time

# 等待所有图片传输完成
time.sleep(5)  # 等待5秒

# 获取最新上传的图片（按修改时间排序）
# 这样可以确保所有已传输的图片都被处理
```

### 为什么需要延时

- 用户一次性发送多张图片
- Telegram/网络传输需要时间
- 如果立刻处理，后传输的图片可能还没到

### 延时建议

- 5秒：适合少量图片（1-10张）
- 10秒：适合大量图片（10张以上）

### 替代方案

如果不想用固定延时，也可以：
1. 等待用户确认"还有吗？"
2. 用心跳时检查inbound目录是否有新文件
