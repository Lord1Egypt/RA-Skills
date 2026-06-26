---
name: newton-quotation-pdf-extraction
description: 从PDF报价单中提取产品信息（型号、数量、价格、币种、图片）。当用户需要从PDF报价单或产品目录中提取结构化产品数据时使用，特别适用于电商产品列表或价格表。
---

# 报价单PDF信息提取技能 (Quotation PDF Extraction)

从PDF产品目录中提取结构化产品信息，包括产品型号、起批量、价格、币种和产品图片。

## 核心原则

### 1. 先理解PDF结构，再设计方案（关键！）

**必须执行的预分析步骤：**

在编写提取代码前，必须先分析PDF的文本结构，理解以下关键信息：

1. **每行产品数量**：一行包含1个还是多个产品？
   - 常见模式：每行1个产品、每行3个产品、每行4个产品
   - 检查方法：查看包含型号和数量的行，统计 `(型号 数量)` 模式出现次数

2. **数据组织方式**：
   - 型号和数量是否在同一行？
   - 价格在同一行还是下一行？
   - 是否存在干扰文本（如装饰字符、页眉页脚）？

3. **结构分析代码模板：**

```python
import pdfplumber
import re

def analyze_pdf_structure(pdf_path):
    """分析PDF文本结构，理解产品组织方式"""
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(min(5, len(pdf.pages))):  # 分析前5页
            page = pdf.pages[page_num]
            text = page.extract_text()
            lines = text.strip().split('\n') if text else []
            
            print(f'\n===== 第{page_num+1}页 - {len(lines)}行 =====')
            
            for i, line in enumerate(lines):
                # 高亮包含型号和数量的行
                if re.search(r'[A-Za-z0-9\-]+\s*\(\d+\s*Peças?\)', line):
                    # 统计这一行有多少个产品
                    products_in_line = len(re.findall(r'[A-Za-z0-9\-]+\s*\(\d+\s*Peças?\)', line))
                    print(f'  [{i}] >>> {line} ({products_in_line}个产品)')
                elif i < 30:
                    print(f'  [{i}] {line}')

# 使用
analyze_pdf_structure("/path/to/catalog.pdf")
```

**分析示例输出：**
```
===== 第2页 - 52行 =====
  [0] Catálogo Caixa Master
  [16] >>> JF-181 (144 Peças) JF-43 (144 Peças) JF-44 (144 Peças) (3个产品)
  [17] >>> R$12,00 R$11,00 R$11,00
  ...
  [33] >>> MY-46 (144 Peças) MY-48 (144 Peças) MY-62 (144 Peças) (3个产品)
  [34] >>> R$9,00 R$12,50 R$12,00
```

**结论**：每行包含3个产品，型号数量在一行，价格在下一行。

### 2. 数据必须来自PDF提取
- **禁止硬编码**：所有产品数据必须从PDF动态提取
- **禁止猜测**：币种必须询问用户，不能假设

## 提取流程

### Phase 1: PDF结构分析

```python
import fitz
import pdfplumber

def analyze_pdf_structure(pdf_path):
    """分析PDF结构，理解产品组织方式"""
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 分析图片分布
        image_list = page.get_images(full=True)
        print(f"第{page_num+1}页: {len(image_list)}张图片")
        
        for img in image_list:
            xref = img[0]
            rects = page.get_image_rects(xref)
            if rects:
                x0, y0, x1, y1 = rects[0]
                print(f"  xref{xref}: x={x0:.0f}-{x1:.0f}, y={y0:.0f}-{y1:.0f}")
    
    doc.close()
```

### Phase 2: 提取产品信息

**关键：正确处理每行多个产品的情况**

```python
def extract_products_from_pdf(pdf_path):
    """提取产品信息（型号、起批量、价格、X坐标）
    
    支持每行多个产品的格式，如：
    "JF-181 (144 Peças) JF-43 (144 Peças) JF-44 (144 Peças)"
    "R$12,00 R$11,00 R$11,00"
    """
    products = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.strip().split('\n')
            words = page.extract_words()
            
            i = 0
            row_idx = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # 跳过表头和无关行
                if any(h in line for h in ['Catálogo', 'Caixa Master', 'Flashing', 'Page', 'Av. Vautier']):
                    i += 1
                    continue
                
                # 跳过单字母行（装饰字符）
                if len(line) <= 3 and not any(c.isdigit() for c in line):
                    i += 1
                    continue
                
                # 关键：使用正则匹配所有 (型号 数量) 组合
                # 如：JF-181 (144 Peças) JF-43 (144 Peças) JF-44 (144 Peças)
                model_qty_pattern = r'([A-Za-z0-9\-/]+)\s*\((\d+)\s*Peças?\)'
                model_qty_matches = list(re.finditer(model_qty_pattern, line))
                
                if model_qty_matches:
                    # 获取下一行的价格信息
                    prices = []
                    if i + 1 < len(lines):
                        price_line = lines[i + 1].strip()
                        # 匹配所有价格 R$xx,xx 后面跟各种单位（Un、Par、Kit、Cx、Jogo等）
                        price_matches = re.findall(r'R\$([\d,.]+)', price_line)
                        prices = price_matches
                    
                    # 为每个型号创建产品记录
                    for idx, match in enumerate(model_qty_matches):
                        model = match.group(1)
                        qty = match.group(2)
                        
                        # 获取该型号在PDF中的X坐标（用于图片匹配）
                        x_center = None
                        y_coord = None
                        
                        # 使用word位置信息来定位
                        for word in words:
                            if word['text'] == model or word['text'].startswith(model):
                                x_center = (word['x0'] + word['x1']) / 2
                                y_coord = word['top']
                                break
                        
                        # 获取对应价格
                        price = prices[idx] if idx < len(prices) else ""
                        
                        products.append({
                            '页码': page_num + 1,
                            '排号': row_idx,
                            '型号': model,
                            '产品名称': '',
                            '起批量': qty,
                            '价格': price,
                            'x_center': x_center,
                            'y_coord': y_coord
                        })
                    
                    row_idx += 1
                    i += 2  # 跳过当前行和价格行
                else:
                    i += 1
    
    return products
```

**重要：价格单位变体覆盖**

不同PDF可能使用不同的价格单位后缀，常见的有：
- `Un`（个/件）
- `Par`（对/双）
- `Kit`（套件）
- `Cx`（箱）
- `Jogo`（套）
- `Pares` / `Par`（双）

**正确的价格正则表达式：**
```python
# 匹配 R$XX,XX 后面跟各种单位
pattern = r'CX-(\d+)Pcs\s+R\$[：:]\s*([\d,]+)(?:Un|Par|Kit|Cx|Jogo|Pares?)'

# 如果单位格式不固定，可以先匹配价格数字，再单独处理单位
price_pattern = r'R\$([\d,]+)'  # 只匹配价格数字
```

**重要：型号正则表达式应支持字母数字混合后缀**

某些型号的结尾可能包含字母后缀，如 VPL-7001-H1、VPL-7001-H8H11、VPL-7001-HB3。

```python
# 错误：只匹配数字后缀
model_pattern = r'VPL-\d+(?:-\d+)?'  # 会截断 VPL-7001-H1 为 VPL-7001

# 正确：支持字母数字混合后缀
model_pattern = r'VPL-[A-Z0-9\-]+'  # 完整匹配 VPL-7001-H1
```

**重要：文件编码问题**

Python脚本文件中的全角字符（如全角冒号 `：`）可能在某些编码环境下失效。

```python
# 确保文件使用UTF-8编码，在文件头添加：
# -*- coding: utf-8 -*-

# 正则中使用字面量字符而非Unicode转义序列
# 正确（字面量）：
pattern = r'CX-(\d+)Pcs\s+R\$[：:]\s*([\d,]+)(?:Un|Par)'
# 可能有问题（转义序列在字符类中）：
pattern = r'CX-(\d+)Pcs\s+R\$[\uFF1A:]\s*([\d,]+)(?:Un|Par)'
```

**重要：处理跨行价格的情况**

某些PDF布局中，多个产品行可能共享同一行价格：
```
第26行: MY-119 (576 Peças)                          <- 1个产品
第27行: MY-105/JF-96 (360 Peças) MY-106/JF-97 (216 Peças)  <- 2个产品
第28行: R$3,80 R$9,50 R$14,50                       <- 3个价格（为3个产品共用）
```

**重要：处理数量在下一行的情况**

某些PDF布局中，一行中既有完整产品又有数量在下一行的产品：
```
第51行: MY-27 (216 Peças) MY-28 (216 Peças) MY-29/X-129
第52行: (192 Peças)
第53行: R$9,50 R$9,50
```

**正确的提取逻辑（处理跨行价格和跨行数量）：**
```python
def extract_products_from_pdf(pdf_path):
    """提取产品信息 - 修复：处理跨行价格和跨行数量"""
    products = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.strip().split('\n')
            words = page.extract_words()
            
            i = 0
            pending_products = []  # 存储数量在下一行的产品
            
            while i < len(lines):
                line = lines[i].strip()
                
                # ... 跳过无关行 ...
                
                model_qty_pattern = r'([A-Za-z0-9\-/]+)\s*\((\d+)\s*Peças?\)'
                model_qty_matches = list(re.finditer(model_qty_pattern, line))
                
                # 处理待处理的产品（数量在当前行）
                if pending_products:
                    qty_match = re.match(r'^\((\d+)\s*Peças?\)', line)
                    if qty_match:
                        qty = qty_match.group(1)
                        for prod in pending_products:
                            prod['起批量'] = qty
                        pending_products = []
                    else:
                        pending_products = []
                
                if model_qty_matches:
                    # 收集价格
                    all_prices = []
                    j = i + 1
                    
                    while j < len(lines):
                        next_line = lines[j].strip()
                        
                        if re.search(model_qty_pattern, next_line):
                            break
                        
                        price_matches = re.findall(r'R\$([\d,.]+)', next_line)
                        for price_str in price_matches:
                            for word in words:
                                if f'R${price_str}' == word['text'] or price_str in word['text']:
                                    all_prices.append({
                                        'price': price_str,
                                        'x': (word['x0'] + word['x1']) / 2
                                    })
                                    break
                        
                        j += 1

                    # 处理完整匹配的产品
                    for match in model_qty_matches:
                        model = match.group(1)
                        qty = match.group(2)

                        x_center = None
                        y_coord = None

                        for word in words:
                            if word['text'] == model:
                                x_center = (word['x0'] + word['x1']) / 2
                                y_coord = word['top']
                                break

                        if x_center is None:
                            for word in words:
                                if word['text'].startswith(model):
                                    remaining = word['text'][len(model):]
                                    if remaining == '' or not remaining[0].isalnum():
                                        x_center = (word['x0'] + word['x1']) / 2
                                        y_coord = word['top']
                                        break

                        price = ""
                        if all_prices and x_center:
                            best_price = min(all_prices, key=lambda p: abs(p['x'] - x_center))
                            price = best_price['price']

                        products.append({
                            '页码': page_num + 1,
                            '型号': model,
                            '产品名称': '',
                            '起批量': qty,
                            '价格': price,
                            'x_center': x_center,
                            'y_coord': y_coord
                        })
                    
                    # 关键修复：检查是否有型号在同一行但没有数量
                    if model_qty_matches:
                        last_match_end = model_qty_matches[-1].end()
                        remaining_text = line[last_match_end:].strip()
                        
                        if remaining_text:
                            potential_model = remaining_text.split()[0]
                            if re.match(r'^[A-Za-z0-9\-/]+$', potential_model) and len(potential_model) >= 2:
                                # 获取坐标
                                x_center = None
                                y_coord = None
                                for word in words:
                                    if word['text'] == potential_model:
                                        x_center = (word['x0'] + word['x1']) / 2
                                        y_coord = word['top']
                                        break
                                
                                if x_center:
                                    prod = {
                                        '页码': page_num + 1,
                                        '型号': potential_model,
                                        '产品名称': '',
                                        '起批量': '',  # 待填充
                                        '价格': '',
                                        'x_center': x_center,
                                        'y_coord': y_coord
                                    }
                                    pending_products.append(prod)
                                    products.append(prod)

                    i += 1
                else:
                    i += 1
    
    return products
```

### Phase 3: 提取并过滤图片

```python
from PIL import Image
import numpy as np

def is_watermark_or_banner(img_path):
    """检测图片是否为水印、横幅或logo（非产品图片）"""
    try:
        pil_img = Image.open(img_path)
        width, height = pil_img.size
        
        # 尺寸过滤
        if width < 40 or height < 40:
            return True
        
        # 宽高比过滤
        aspect_ratio = width / height if height > 0 else 0
        if aspect_ratio > 4 or aspect_ratio < 0.25:
            return True
        
        # 内容分析
        gray = pil_img.convert('L')
        arr = np.array(gray)
        unique_colors = len(np.unique(arr))
        
        if unique_colors < 30:  # 水印/横幅通常颜色很少
            return True
        
        std_dev = np.std(arr)
        is_large = width > 200 and height > 200
        if is_large and unique_colors < 30 and std_dev < 30:  # 背景轮廓图
            return True
        
        return False
    except Exception:
        return True

def extract_images_filtered(pdf_path, output_dir):
    """提取PDF图片并过滤水印/横幅"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    extracted = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        page_width = page.rect.width
        
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            rects = page.get_image_rects(xref)
            
            if not rects:
                continue
            
            for rect_idx, rect in enumerate(rects):
                x0, y0, x1, y1 = rect
                pdf_width = x1 - x0
                pdf_height = y1 - y0
                
                # 跳过左右边缘的小图标
                margin = 20
                is_in_x_margin = (x0 < margin or x1 > page_width - margin)
                if is_in_x_margin and pdf_width < 80 and pdf_height < 80:
                    continue
                
                img_filename = f"p{page_num+1}_xref{xref}_pos{rect_idx}.png"
                img_path = os.path.join(output_dir, img_filename)
                
                # 避免重复保存同一xref的图片
                if not os.path.exists(img_path):
                    with open(img_path, "wb") as f:
                        f.write(base_image["image"])
                    
                    if is_watermark_or_banner(img_path):
                        os.remove(img_path)
                        continue
                
                # 检查是否已存在相同位置的图片
                is_duplicate = False
                for existing in extracted:
                    if (existing['page'] == page_num + 1 and
                        abs(existing['x_center'] - (x0 + x1) / 2) < 5 and
                        abs(existing['y_center'] - (y0 + y1) / 2) < 5):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    extracted.append({
                        'page': page_num + 1,
                        'xref': xref,
                        'pos': rect_idx,
                        'y': y0,
                        'y_end': y1,
                        'x_center': (x0 + x1) / 2,
                        'y_center': (y0 + y1) / 2,
                        'path': img_path
                    })
    
    doc.close()
    extracted.sort(key=lambda x: (x['page'], x['y']))
    return extracted
```

### Phase 4: 按排分组并匹配图片

```python
from collections import defaultdict

def group_images_by_row(images, page_num, exclude_xrefs=None):
    """按Y坐标将图片分组为排"""
    if exclude_xrefs is None:
        exclude_xrefs = set()
    
    page_images = [img for img in images 
                   if img['page'] == page_num and img['xref'] not in exclude_xrefs]
    
    if not page_images:
        return []
    
    page_images.sort(key=lambda x: x['y_center'])
    
    rows = []
    current_row = [page_images[0]]
    
    for img in page_images[1:]:
        if img['y_center'] - current_row[-1]['y_center'] < 80:
            current_row.append(img)
        else:
            current_row.sort(key=lambda x: x['x_center'])
            rows.append(current_row)
            current_row = [img]
    
    if current_row:
        current_row.sort(key=lambda x: x['x_center'])
        rows.append(current_row)
    
    return rows

def match_products_to_images(products, images, exclude_xrefs=None):
    """将产品与图片匹配（按排和X坐标匹配）"""
    if exclude_xrefs is None:
        exclude_xrefs = {33}  # 默认过滤xref33（常见背景图）
    
    used_images = set()
    page_products = defaultdict(list)
    
    for p in products:
        page_products[p['页码']].append(p)
    
    for page_num in page_products:
        image_rows = group_images_by_row(images, page_num, exclude_xrefs)
        prods = page_products[page_num]
        prod_rows = defaultdict(list)
        
        for p in prods:
            prod_rows[p['排号']].append(p)
        
        for row_idx in sorted(prod_rows.keys()):
            if row_idx >= len(image_rows):
                continue
            
            row_products = prod_rows[row_idx]
            row_images = image_rows[row_idx]
            
            # 按X坐标排序
            row_products.sort(key=lambda x: x.get('x_center', 0) or 0)
            
            # 按X坐标最接近原则匹配
            for prod in row_products:
                prod_x = prod.get('x_center', 0) or 0
                
                best_img = None
                min_diff = float('inf')
                
                for img in row_images:
                    if img['path'] in used_images:
                        continue
                    diff = abs(img['x_center'] - prod_x)
                    if diff < min_diff:
                        min_diff = diff
                        best_img = img
                
                if best_img:
                    prod['image_path'] = best_img['path']
                    used_images.add(best_img['path'])
    
    return products
```

### Phase 5: 导出Excel

```python
def export_to_excel(products, output_path, currency):
    """导出到Excel（含嵌入图片）"""
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as OpenpyxlImage
    import os
    
    wb = Workbook()
    ws = wb.active
    ws.title = "产品清单"
    
    headers = ['序号', '页码', '型号', '产品名称', '起批量', '币种', '价格', '产品图片']
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
    
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 8
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 35
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 10
    ws.column_dimensions['G'].width = 10
    ws.column_dimensions['H'].width = 25
    
    for idx, p in enumerate(products, start=2):
        ws.cell(row=idx, column=1, value=idx - 1)
        ws.cell(row=idx, column=2, value=p.get('页码', ''))
        ws.cell(row=idx, column=3, value=p.get('型号', ''))
        ws.cell(row=idx, column=4, value=p.get('产品名称', ''))
        
        # 起批量：无数据时留空
        qty = p.get('起批量', '')
        ws.cell(row=idx, column=5, value=qty if qty else None)
        
        ws.cell(row=idx, column=6, value=currency)
        
        # 价格：无数据时留空
        price = p.get('价格', '')
        ws.cell(row=idx, column=7, value=price if price else None)
        
        img_path = p.get('image_path', '')
        if img_path and os.path.exists(img_path):
            try:
                img = OpenpyxlImage(img_path)
                img.width = 100
                img.height = 100
                ws.add_image(img, f'H{idx}')
                ws.row_dimensions[idx].height = 80
            except Exception:
                ws.cell(row=idx, column=8, value="图片错误")
    
    wb.save(output_path)
    return output_path
```

## 关键经验总结

### 1. 型号识别

**支持的格式：**
- 字母开头：XP-115, JF-181, WD-90015
- 数字开头含字母：13-1, 510-A, 2109
- 纯数字（长度>=2）：13, 790
- 复合型号（斜杠分隔）：MY-109/MY-20, MY-103/JF-94, WD90022/QY3098
- 带描述词：JF-194 C/ Luz, JF-144 com música
- **字母数字混合后缀**：VPL-7001-H1, VPL-7001-H8H11, VPL-7001-HB3

**重要：斜杠处理策略**
- "/" 可能是复合型号的一部分（MY-109/MY-20），**不应盲目清理**
- "/" 后面跟中文描述时才清理：XL-2401/白18粉18绿12 → XL-2401
- "/" 后面跟型号字母数字时应保留：WD90022/QY3098

**重要：字母后缀处理策略**
- 型号结尾可能包含字母后缀（如 -H1, -HB3, -H8H11）
- **不应**只使用 `-\d+` 匹配后缀，应使用 `[A-Z0-9\-]+` 匹配字母数字混合后缀

**带空格的型号：**
- "JF-194 C/ Luz"：用第一个词（JF-194）做坐标查找，但保留完整名称
- "JF-144 com música"：型号可能跨行，数量在单独一行

**型号正则表达式推荐：**
```python
# 通用型号匹配（支持字母数字混合后缀）
model_pattern = r'VPL-[A-Z0-9\-]+'

# 更通用的型号匹配（支持多种前缀）
model_pattern = r'[A-Z]+-\d+(?:-[A-Z0-9]+)*'
```

### 2. 坐标获取
- 使用 `word['text'] == token` 或 `word['text'].startswith(token + '/')` 匹配
- 避免使用 `token in word['text']`（会匹配到错误位置的词）
- 带空格的型号：用第一个词查找坐标，保留完整名称

**重要：避免startswith导致的错误匹配**

问题案例：JF-55 和 JF-558
- `JF-558.startswith("JF-55")` 返回 True
- 这会导致 JF-55 错误地获取 JF-558 的坐标

**正确的坐标匹配逻辑：**
```python
# 首先尝试精确匹配
x_center = None
y_coord = None

for word in words:
    if word['text'] == model:
        x_center = (word['x0'] + word['x1']) / 2
        y_coord = word['top']
        break

# 如果没有精确匹配，再尝试startswith，但要确保不是其他型号的前缀
if x_center is None:
    for word in words:
        if word['text'].startswith(model):
            # 检查是否是独立型号（后面跟着非字母数字字符或是结尾）
            remaining = word['text'][len(model):]
            if remaining == '' or not remaining[0].isalnum():
                x_center = (word['x0'] + word['x1']) / 2
                y_coord = word['top']
                break
```

### 3. 跨行产品处理

**常见跨行模式：**
| 模式 | 示例 | 处理方法 |
|------|------|----------|
| 数量在下一行 | MY-29/X-129 (120) | 向后查找数量行 |
| 数量单独一行无型号 | (1000 Peças) | 向前查找关联的型号 |
| 数量跨行+中间插入价格 | EQY657 36 caixinhas(216 \n R$100,00 \n Peças) | 合并多行文本，移除价格后解析 |
| 复合型号跨行 | WD90022/ \n QY158SS (168) | 合并相邻行，识别 "/" 连接 |
| 同一行相同型号多次 | M-5 (300) M-5 (220) YJ-20 (240) | 按Y坐标分组去重，按X坐标分配 |

**重要：处理同一行相同型号多次出现的情况**

某些PDF中，同一行可能出现多个相同型号的产品：
```
M-5 (300 Peças) M-5 (220 Peças) YJ-20 (240 Peças)
```

这种情况下，简单的型号→word映射会失败，因为所有"M-5"的word会被混在一起。

**正确的坐标匹配逻辑（处理重复型号）：**
```python
from collections import defaultdict

def get_word_coordinates(words, model_qty_matches):
    """获取每个匹配的word坐标，处理同一行相同型号多次出现的情况
    
    策略：
    1. 按Y坐标分组，找到最可能的行
    2. 在该行范围内按型号分组word
    3. 去重：X坐标相差小于10的视为同一个word
    4. 按match顺序分配word（第n个match对应第n个word）
    """
    # 收集所有匹配型号的word，按型号分组
    words_by_model = defaultdict(list)
    for match in model_qty_matches:
        model = match.group(1)
        for word in words:
            if word['text'] == model:
                words_by_model[model].append(word)
    
    # 按Y坐标分组统计，找到最可能的行
    y_counts = defaultdict(int)
    for model, ws in words_by_model.items():
        for w in ws:
            y_key = round(w['top'] / 50) * 50
            y_counts[y_key] += 1
    
    if y_counts:
        best_y = max(y_counts.keys(), key=lambda k: y_counts[k])
    else:
        best_y = 0
    
    # 筛选该Y组内的word（允许50像素误差）
    filtered_words_by_model = defaultdict(list)
    for model, ws in words_by_model.items():
        for w in ws:
            if abs(w['top'] - best_y) < 50:
                filtered_words_by_model[model].append(w)
    
    # 去重：按X坐标排序，合并接近的（X相差小于10视为同一个）
    for model in filtered_words_by_model:
        ws = filtered_words_by_model[model]
        ws.sort(key=lambda x: x['x0'])
        deduped = []
        for w in ws:
            if not deduped or abs(w['x0'] - deduped[-1]['x0']) > 10:
                deduped.append(w)
        filtered_words_by_model[model] = deduped
    
    # 分配：第n个match对应第n个word
    model_usage_count = defaultdict(int)
    match_idx_to_word = {}
    
    for match_idx, match in enumerate(model_qty_matches):
        model = match.group(1)
        ws = filtered_words_by_model.get(model, [])
        count = model_usage_count[model]
        if count < len(ws):
            match_idx_to_word[match_idx] = ws[count]
            model_usage_count[model] += 1
    
    return match_idx_to_word
```

**跨行解析策略：**
```python
# 合并相邻行文本后再解析
def merge_adjacent_lines(lines, current_idx, look_ahead=2):
    """合并当前行及其后N行的文本"""
    merged = lines[current_idx]
    for i in range(1, look_ahead + 1):
        if current_idx + i < len(lines):
            merged += " " + lines[current_idx + i]
    return merged

# 移除价格干扰后再匹配数量
import re
text_no_price = re.sub(r'R\$\d+[,.]\d+', '', merged_text)
# 然后再用数量正则匹配
qty_match = re.search(r'\((\d+)\s*Peças?\)', text_no_price)
```

### 4. 图片过滤
- 过滤xref33（常见背景图/水印）
- 基于内容分析：唯一颜色<30或标准差<30的可能是水印/背景
- **基于尺寸过滤**：PDF中高度>500像素的通常是全页背景图，应降优先级
- 去重：同一xref的多个位置只保留一个

### 5. 图片匹配策略（关键！）

**核心原则：图片与产品文本在相同的Y坐标范围内**
- 不同PDF布局中，图片可能在产品文本的**上方、下方或同一行**
- **不应**假设"图片必须在产品上方"或"图片必须在产品下方"
- **应该**找"Y坐标最接近产品Y坐标的图片行"

**重要：产品Y坐标和图片Y坐标可能不直接对应**

某些PDF布局中，产品文本的Y坐标和图片的Y坐标不在同一范围：
```
图片排1: y_center=393 (3张图片)
产品文本: y=469-473 (MY-119, MY-105/JF-96, MY-106/JF-97)
图片排2: y_center=623 (3张图片)
```

在这种情况下，产品文本y=469位于图片排1（393）和图片排2（623）之间，应该找Y坐标最接近的图片行。

**正确的图片匹配逻辑：**
```python
def match_products_to_images(products, images):
    """将产品与图片匹配
    
    关键策略：找Y坐标最接近产品Y坐标的图片行（不限定上下关系）
    """
    from collections import defaultdict
    
    page_products = defaultdict(list)
    for p in products:
        page_products[p['页码']].append(p)
    
    for page_num in page_products:
        # 获取该页的所有图片（过滤全页背景图）
        page_images = [img for img in images
                      if img['page'] == page_num
                      and img['height'] < 500]
        
        if not page_images:
            continue
        
        # 按Y坐标分组图片（阈值100像素）
        page_images.sort(key=lambda x: x['y_center'])
        image_rows = []
        current_row = [page_images[0]]
        
        for img in page_images[1:]:
            if img['y_center'] - current_row[-1]['y_center'] < 100:
                current_row.append(img)
            else:
                current_row.sort(key=lambda x: x['x_center'])
                image_rows.append(current_row)
                current_row = [img]
        
        if current_row:
            current_row.sort(key=lambda x: x['x_center'])
            image_rows.append(current_row)
        
        # 为每个产品匹配图片
        for product in page_products[page_num]:
            prod_y = product.get('y_coord', 0) or 0
            prod_x = product.get('x_center', 0) or 0
            
            if not prod_y or not prod_x:
                continue
            
            # 关键：找Y坐标最接近产品Y坐标的图片行（不限定上下关系）
            best_row = None
            best_y_diff = float('inf')
            
            for row in image_rows:
                row_y = row[0]['y_center']
                y_diff = abs(row_y - prod_y)  # 使用绝对值
                if y_diff < best_y_diff:
                    best_y_diff = y_diff
                    best_row = row
            
            # 在最佳行中找X最接近的图片
            if best_row:
                best_img = min(best_row, key=lambda x: abs(x['x_center'] - prod_x))
                
                # 检查X坐标差异是否在合理范围内
                if abs(best_img['x_center'] - prod_x) < 200:
                    product['image_path'] = best_img['path']
    
    return products
```

### 6. 价格分配

**顺序分配陷阱：**
- 不要假设第N行产品对应第N行价格
- 某些页面布局特殊，产品行和价格行可能错位

**安全策略：**
```python
# 先收集所有价格，再按X坐标分配给对应产品
prices = re.findall(r'R\$(\d+[,.]\d+)', price_line)
prices_sorted = sorted(zip(prices, price_words), key=lambda x: x[1]['x0'])

for i, product in enumerate(products_in_row):
    if i < len(prices_sorted):
        product['价格'] = prices_sorted[i][0]
```

**重要：价格单位变体**

不同PDF可能使用不同的价格单位后缀，常见的有：
- `Un`（个/件）
- `Par`（对/双）
- `Kit`（套件）
- `Cx`（箱）
- `Jogo`（套）
- `Pares` / `Par`（双）

**正确的价格正则表达式：**
```python
# 匹配 R$XX,XX 后面跟各种单位
pattern = r'CX-(\d+)Pcs\s+R\$[：:]\s*([\d,]+)(?:Un|Par|Kit|Cx|Jogo|Pares?)'

# 如果单位格式不固定，可以先匹配价格数字，再单独处理单位
price_pattern = r'R\$([\d,]+)'  # 只匹配价格数字
```

### 7. 常见陷阱总结

| 问题 | 案例 | 解决方案 |
|------|------|----------|
| **每行多个产品只提取第一个** | `JF-181 (...) JF-43 (...) JF-44 (...)` 只提取JF-181 | 使用 `re.finditer()` 找到所有匹配，而非 `re.search()` |
| **startswith导致坐标错误** | JF-55 获取了 JF-558 的坐标 | 先精确匹配，startwith时检查后续字符 |
| **跨行价格未正确匹配** | MY-105/JF-96和MY-106/JF-97没有价格 | 收集多行价格，按X坐标匹配 |
| **产品Y坐标和图片Y坐标不对应** | MY-105/JF-96图片匹配错误 | 找Y坐标最接近产品Y坐标的图片行（不限定上下关系） |
| **数量在下一行的产品遗漏** | MY-29/X-129未提取 | 检查行尾剩余文本，使用pending_products机制 |
| **同一行相同型号多次出现** | 第2、3个M-5无图片 | 按Y坐标分组去重，按X坐标分配word |
| **只有型号没有数量的产品** | JF-144 com música未提取 | 识别型号行，使用pending_products机制跨行获取数量和价格 |
| **型号和数量连在一起** | DFXL2207(120 Peças)坐标获取失败 | word匹配时使用startswith(model + '(') |
| **非产品文本被识别为型号** | 2X2被错误提取为产品 | 过滤条件：必须包含连字符或长度>=4 |
| **行尾多个型号未全部提取** | X-156和X-157只提取第一个 | 使用正则提取所有型号，按X坐标分配多个数量 |
| 复合型号被拆分 | MY-109/MY-20 → 只提取MY-20 | 保留"/"作为型号一部分 |
| 带空格型号匹配失败 | JF-194 C/ Luz | 用第一个词查找坐标，保留完整名称 |
| 全页背景图干扰 | JF-203无图片 | 过滤height>500的异常图 |
| 跨行产品遗漏 | 2109,790,JF-412完全跳过 | 合并相邻行文本解析 |
| 数量跨行+价格插入 | EQY657 36 caixinhas(216 R$100,00 Peças) | 移除价格后匹配数量 |
| 价格分配错位 | 第3行产品用第2行价格 | 按X坐标分配，不按行序 |
| 型号合并需拆分 | WD90022/QY3098被当作一个 | 识别"/"连接的独立型号 |
| **价格单位变体遗漏** | VPL-5001系列价格单位是"Par"而非"Un" | 价格正则需匹配多种单位：`(?:Un\|Par\|Kit\|Cx\|Jogo\|Pares?)` |
| **型号含字母后缀被截断** | VPL-7001-H1 被截断为 VPL-7001 | 型号正则使用 `VPL-[A-Z0-9\-]+` 而非 `VPL-\d+(?:-\d+)?` |
| **全角冒号编码问题** | 正则中的 `：` 在某些文件中失效 | 确保Python文件使用UTF-8编码，正则中使用字面量字符 |

**最严重的陷阱：**

1. **未分析PDF结构就编写提取逻辑**
   - 后果：只提取了1/3的产品（如125个而非340个）
   - 预防：必须先运行结构分析代码，确认每行产品数量
   - 修复：使用 `re.finditer()` 替代 `re.search()`

2. **startswith导致的坐标匹配错误**
   - 后果：JF-55获取了JF-558的坐标，导致图片匹配错误
   - 预防：先尝试精确匹配，再使用startswith并验证后续字符
   - 修复：检查 `remaining == '' or not remaining[0].isalnum()`

3. **跨行价格未正确处理**
   - 后果：MY-105/JF-96和MY-106/JF-97等产品没有价格
   - 预防：分析价格行是否被多个产品行共享
   - 修复：收集多行价格，按X坐标最接近原则匹配给对应产品

4. **产品Y坐标和图片Y坐标不直接对应**
   - 后果：MY-105/JF-96和MY-106/JF-97图片匹配错误
   - 预防：检查产品Y坐标是否和图片行的Y坐标在同一范围
   - 修复：找Y坐标最接近产品Y坐标的图片行，不限定上下关系

5. **数量在下一行的产品遗漏**
   - 后果：MY-29/X-129未提取（一行中既有完整产品又有数量在下一行的产品）
   - 预防：检查行尾是否有剩余型号文本未被处理
   - 修复：使用 `pending_products` 机制，在下一行找到数量后填充

6. **同一行相同型号多次出现**
   - 后果：第2、3个M-5等产品无法正确匹配图片
   - 预防：检查是否有相同型号在同一行多次出现
   - 修复：按Y坐标分组找到最佳行，去重后按X坐标顺序分配word给match

7. **只有型号没有数量的产品**
   - 后果：JF-144 com música未提取（数量在隔一行之后）
   - 预防：检查是否有型号行没有对应的数量
   - 修复：使用 `pending_products` 机制，允许跨多行查找数量，同时收集价格

8. **价格单位变体未覆盖**
   - 后果：VPL-5001系列价格单位是"Par"（对/双），正则只匹配"Un"（个），导致价格和起批量全部为空
   - 预防：分析PDF时检查价格行的单位后缀，常见的有 Un、Par、Kit、Cx、Jogo、Pares 等
   - 修复：价格正则使用 `(?:Un|Par|Kit|Cx|Jogo|Pares?)` 而非只匹配 `Un`

9. **型号正则表达式不够灵活**
   - 后果：VPL-7001-H1、VPL-7001-H8H11、VPL-7001-HB3 等含字母后缀的型号被截断为 VPL-7001
   - 预防：型号可能包含字母和数字的混合后缀
   - 修复：型号正则使用 `VPL-[A-Z0-9\-]+` 而非 `VPL-\d+(?:-\d+)?`

10. **文件编码导致正则表达式失效**
    - 后果：同样的正则表达式在独立脚本中能工作，但在主提取脚本中不工作
    - 预防：确保Python文件使用UTF-8编码（文件头加 `# -*- coding: utf-8 -*-`）
    - 修复：正则中使用字面量字符（如 `：`），避免使用Unicode转义序列（如 `\uFF1A`）在字符类中可能不被正确解析的问题

### 8. 提取后验证清单

完成提取后，应进行以下验证：
1. **数量检查**：产品数是否与页面图片行数匹配？
   - 估算：每页产品数 ≈ 行数 × 每行产品数
   - 如果提取数量明显偏少（如只有预期的1/3），检查是否使用了 `re.finditer()`
   
2. **抽样验证**：随机检查5-10个产品的图片是否正确
3. **特殊页面**：检查产品数异常少/多的页面
4. **用户反馈**：请用户指出问题产品，迭代修复
5. **价格完整性检查**：随机抽取几个产品，检查其价格和起批量是否为空
   - 如果有大量产品价格为空，检查价格正则是否覆盖了所有单位变体（Un、Par、Kit等）
6. **型号完整性检查**：检查型号是否被截断
   - 如果型号被截断（如 VPL-7001-H1 变成 VPL-7001），检查型号正则是否支持字母数字混合后缀

**验证示例：**
```python
# 检查每页产品分布
from collections import Counter
page_counts = Counter(p['页码'] for p in products)
for page, count in sorted(page_counts.items()):
    print(f"第{page}页: {count}个产品")

# 如果某页只有1-2个产品，可能是提取逻辑有问题

# 检查价格完整性
empty_price_count = sum(1 for p in products if not p.get('价格'))
print(f"价格为空的产品数: {empty_price_count}/{len(products)}")

# 检查型号是否有截断（同型号前缀的产品过多）
model_prefixes = Counter(p['型号'].split('-')[0] + '-' + p['型号'].split('-')[1] for p in products if '型号' in p)
for prefix, count in model_prefixes.most_common(10):
    if count > 10:
        print(f"型号前缀 {prefix} 有 {count} 个产品，可能有截断问题")
```

## 文件编码最佳实践

Python脚本文件中的非ASCII字符（如全角冒号 `：`）可能在某些编码环境下失效。

**最佳实践：**
1. 在Python文件头添加编码声明：
   ```python
   # -*- coding: utf-8 -*-
   ```

2. 正则表达式中使用字面量字符而非Unicode转义序列：
   ```python
   # 正确（字面量）：
   pattern = r'CX-(\d+)Pcs\s+R\$[：:]\s*([\d,]+)(?:Un|Par)'
   
   # 可能有问题（转义序列在字符类中可能不被正确解析）：
   pattern = r'CX-(\d+)Pcs\s+R\$[\uFF1A:]\s*([\d,]+)(?:Un|Par)'
   ```

3. 创建独立的脚本文件进行测试，避免在命令行中直接运行包含非ASCII字符的Python代码

## 完整示例

```python
# 完整提取流程
def extract_catalog(pdf_path, output_dir="output"):
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. 提取产品信息
    products = extract_products_from_pdf(pdf_path)
    print(f"找到 {len(products)} 个产品")
    
    # 2. 提取图片
    images = extract_images_filtered(pdf_path, output_dir)
    print(f"提取 {len(images)} 张图片")
    
    # 3. 匹配产品与图片
    matched = match_products_to_images(products, images)
    matched_count = sum(1 for p in matched if p.get('image_path'))
    print(f"成功匹配: {matched_count}/{len(matched)}")
    
    # 4. 询问币种
    currency = input("请输入币种代码（如CNY/USD/BRL）: ").strip().upper()
    
    # 5. 导出Excel
    output_excel = os.path.join(output_dir, "产品清单.xlsx")
    export_to_excel(matched, output_excel, currency)
    print(f"导出完成: {output_excel}")
    
    return matched

# 使用
if __name__ == "__main__":
    extract_catalog("/path/to/catalog.pdf")
```
