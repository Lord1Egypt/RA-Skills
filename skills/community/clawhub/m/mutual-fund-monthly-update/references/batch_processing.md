# 批量处理文件夹逻辑

## 功能说明

当用户提供文件夹路径时，AI自动批量处理文件夹中的所有PDF文件。

---

## 触发条件

```
用户输入包含以下关键词：
- "文件夹路径"
- "批量处理"
- "处理这个文件夹"
- 文件路径（以/或盘符开头）

示例：
- "请处理这个文件夹：/Users/yujing/Documents/基金月报/"
- "批量处理：C:\\Users\\yujing\\基金月报\\"
- "/path/to/folder"
```

---

## 处理流程

### 步骤1：扫描文件夹

```python
import os
from pathlib import Path

def scan_folder(folder_path):
    """扫描文件夹，识别PDF和Excel文件"""
    
    folder = Path(folder_path)
    
    # 扫描PDF文件
    pdf_files = sorted(folder.glob("*.pdf"))
    
    # 扫描Excel文件（可能是模板）
    excel_files = sorted(folder.glob("*.xlsx"))
    
    return {
        "pdf_files": [str(f) for f in pdf_files],
        "excel_files": [str(f) for f in excel_files],
        "folder_name": folder.name
    }
```

### 步骤2：批量提取PDF数据

```python
def batch_extract_pdfs(pdf_files):
    """批量提取所有PDF数据"""
    
    all_data = {}  # {基金名: {日期: 数据}}
    
    for pdf_path in pdf_files:
        # 提取PDF数据（文本+OCR）
        data = extract_pdf_complete(pdf_path)
        
        # 识别基金名称和日期
        fund_name = identify_fund_name(data, pdf_path)
        date = identify_report_date(data, pdf_path)
        
        # 存储数据
        if fund_name not in all_data:
            all_data[fund_name] = {}
        
        all_data[fund_name][date] = data
    
    return all_data
```

### 步骤3：识别基金名称

```python
def identify_fund_name(data, pdf_path):
    """识别基金名称"""
    
    # 方法1：从PDF内容中提取
    if "基金名称" in data:
        return data["基金名称"]
    
    # 方法2：从文件名中提取
    filename = Path(pdf_path).stem
    
    # 常见格式：
    # 汇丰亚洲债券_202510.pdf
    # 汇丰亚洲债券-2025年10月.pdf
    # 汇丰亚洲债券.pdf
    
    # 移除日期部分
    import re
    name = re.sub(r'[_\-\s]*\d{4}[_\-\s年]*\d{1,2}[_\-\s月]*', '', filename)
    name = re.sub(r'[_\-\s]*\d{8}', '', name)
    
    return name.strip()
```

### 步骤4：识别报告日期

```python
def identify_report_date(data, pdf_path):
    """识别报告日期"""
    
    # 方法1：从PDF内容中提取
    if "报告日期" in data:
        return data["报告日期"]
    
    # 方法2：从文件名中提取
    filename = Path(pdf_path).stem
    
    import re
    
    # 格式1：202510
    match = re.search(r'(\d{4})(\d{2})', filename)
    if match:
        year, month = match.groups()
        return f"{year}{month}"
    
    # 格式2：2025年10月
    match = re.search(r'(\d{4})年(\d{1,2})月', filename)
    if match:
        year, month = match.groups()
        return f"{year}{month.zfill(2)}"
    
    # 格式3：2025-10
    match = re.search(r'(\d{4})-(\d{2})', filename)
    if match:
        year, month = match.groups()
        return f"{year}{month}"
    
    # 如果无法识别，使用文件修改时间
    import os
    mtime = os.path.getmtime(pdf_path)
    from datetime import datetime
    dt = datetime.fromtimestamp(mtime)
    return dt.strftime("%Y%m")
```

### 步骤5：生成PDF信息Excel（AI格式）

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

def generate_pdf_info_excel(all_data, output_path):
    """生成PDF信息Excel（AI格式）"""
    
    wb = Workbook()
    
    # 删除默认Sheet
    wb.remove(wb.active)
    
    # 按基金名称排序
    sorted_funds = sorted(all_data.keys())
    
    for fund_name in sorted_funds:
        # 创建Sheet
        ws = wb.create_sheet(title=fund_name[:31])  # Sheet名最多31字符
        
        # 获取该基金的所有日期，按时间升序排序
        dates = sorted(all_data[fund_name].keys())
        
        # 写入表头
        ws['A1'] = '指标'
        for i, date in enumerate(dates, start=2):
            ws.cell(row=1, column=i, value=date)
        
        # 收集所有字段（合并所有日期的字段）
        all_fields = set()
        for date in dates:
            all_fields.update(all_data[fund_name][date].keys())
        
        # 写入数据
        row_idx = 2
        for field in sorted(all_fields):
            ws.cell(row=row_idx, column=1, value=field)
            
            for col_idx, date in enumerate(dates, start=2):
                value = all_data[fund_name][date].get(field, "")
                ws.cell(row=row_idx, column=col_idx, value=value)
            
            row_idx += 1
        
        # 应用样式
        apply_styles(ws, row_idx, len(dates) + 1)
    
    # 保存Excel
    wb.save(output_path)
    return output_path

def apply_styles(ws, row_count, col_count):
    """应用样式"""
    
    # 标题行样式
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    
    for col in range(1, col_count + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # 边框
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row in range(1, row_count + 1):
        for col in range(1, col_count + 1):
            ws.cell(row=row, column=col).border = thin_border
    
    # 列宽
    ws.column_dimensions['A'].width = 20
    for col in range(2, col_count + 1):
        ws.column_dimensions[chr(64 + col)].width = 15
```

### 步骤6：检查并应用用户模板

```python
def check_and_apply_template(excel_files, all_data):
    """检查是否有用户模板，如果有则应用"""
    
    if not excel_files:
        return None
    
    # 识别模板文件（通常是名称包含"模板"或"template"的文件）
    template_file = None
    for excel_file in excel_files:
        if any(keyword in excel_file.lower() for keyword in ['模板', 'template', '更新']):
            template_file = excel_file
            break
    
    if not template_file:
        # 如果没有明显模板，使用第一个Excel文件
        template_file = excel_files[0]
    
    # 学习模板结构
    template_structure = learn_template(template_file)
    
    # 批量填充数据
    output_path = fill_template_with_batch_data(template_file, all_data)
    
    return output_path
```

---

## 数据结构

### all_data 结构

```python
all_data = {
    "汇丰亚洲债券": {
        "202510": {
            "基金名称": "汇丰亚洲债券基金",
            "报告日期": "202510",
            "久期": 5.89,
            "到期收益率": 0.0554,
            "基金规模": 28.93,
            "行业分布": {
                "金融": 0.25,
                "能源": 0.15,
                ...
            },
            "地区分布": {...},
            "信用评级分布": {...},
            "十大持仓": [...],
            ...
        },
        "202511": {...},
        "202512": {...}
    },
    "摩根亚洲债券": {
        "202511": {...},
        "202512": {...}
    },
    ...
}
```

---

## 输出文件

### 文件命名规则

```
PDF信息Excel：{文件夹名}_PDF信息提取_{时间戳}.xlsx
用户模板Excel：{文件夹名}_已填充_{时间戳}.xlsx

示例：
基金月报_PDF信息提取_20260313_163000.xlsx
基金月报_已填充_20260313_163000.xlsx
```

### 输出位置

```
默认输出到：
- 原文件夹路径下（推荐）
- 或 /root/.openclaw/media/outbound/（远程环境）
```

---

## 错误处理

### 情况1：文件夹路径不存在

```
AI回复：
❌ 文件夹路径不存在：{路径}

请检查路径是否正确。
```

### 情况2：文件夹中没有PDF文件

```
AI回复：
⚠️ 文件夹中没有找到PDF文件：{路径}

发现文件：
- {file1.xlsx}
- {file2.docx}
- ...

请确认文件夹中包含PDF文件。
```

### 情况3：部分PDF提取失败

```
AI回复：
⚠️ 部分PDF提取失败：

成功：
- 汇丰亚洲债券_202510.pdf ✓
- 汇丰亚洲债券_202511.pdf ✓

失败：
- 损坏的文件.pdf ✗（文件损坏）
- 加密的文件.pdf ✗（需要密码）

已生成可用数据的Excel。
```

---

## 性能优化

### 批量处理优化

```python
# 使用多进程加速（可选）
from multiprocessing import Pool

def batch_extract_pdfs_parallel(pdf_files, workers=4):
    """并行提取PDF数据"""
    
    with Pool(workers) as pool:
        results = pool.map(extract_pdf_complete, pdf_files)
    
    # 整理结果
    all_data = {}
    for pdf_path, data in zip(pdf_files, results):
        fund_name = identify_fund_name(data, pdf_path)
        date = identify_report_date(data, pdf_path)
        
        if fund_name not in all_data:
            all_data[fund_name] = {}
        
        all_data[fund_name][date] = data
    
    return all_data
```

### 进度反馈

```python
def batch_extract_with_progress(pdf_files):
    """带进度反馈的批量提取"""
    
    total = len(pdf_files)
    all_data = {}
    
    for i, pdf_path in enumerate(pdf_files, start=1):
        print(f"正在处理：{i}/{total} - {Path(pdf_path).name}")
        
        data = extract_pdf_complete(pdf_path)
        fund_name = identify_fund_name(data, pdf_path)
        date = identify_report_date(data, pdf_path)
        
        if fund_name not in all_data:
            all_data[fund_name] = {}
        
        all_data[fund_name][date] = data
    
    return all_data
```

---

## 示例对话

### 完整流程示例

```
用户：请处理这个文件夹：/Users/yujing/Documents/基金月报/

AI：正在扫描文件夹...

📁 文件夹：基金月报
├── PDF文件：15个
└── Excel文件：1个（可能是模板）

正在提取PDF数据（15个文件）...

✅ 提取完成：
- 汇丰亚洲债券：3个月（202510、202511、202512）
- 摩根亚洲债券：2个月（202511、202512）
- 中银香港全天候中国：2个月（202511、202512）
- 博时新兴市场：1个月（202512）
- 华夏海外收益：2个月（202511、202512）
- 南方多元配置：2个月（202511、202512）

正在生成Excel...

✅ PDF信息Excel已生成（AI格式）
  - Sheet 1: 汇丰亚洲债券（3个月数据）
  - Sheet 2: 摩根亚洲债券（2个月数据）
  - Sheet 3: 中银香港全天候中国（2个月数据）
  - Sheet 4: 博时新兴市场（1个月数据）
  - Sheet 5: 华夏海外收益（2个月数据）
  - Sheet 6: 南方多元配置（2个月数据）

✅ 用户模板Excel已生成（按模板格式填充）

[发送两个Excel文件]
```

---

## 技术依赖

### 额外依赖

```python
# 文件扫描
import os
from pathlib import Path

# 多进程（可选）
from multiprocessing import Pool

# 日期处理
from datetime import datetime
```

### 兼容性

```
- macOS: /Users/xxx/
- Linux: /home/xxx/
- Windows: C:\\Users\\xxx\\
- 相对路径: ./folder/
- 绝对路径: /full/path/to/folder/
```
