# Bug 排查与强制重建

## 已修复：表格渲染错乱

### 问题描述

生成的 docx 中表格只有1列，内容被逐字拆分；或列数远超预期（如4列表格变成60+列）。

### 根因

`integrate_report.py` 的 `_flush_table` 函数存在 bug：

```python
# ❌ Bug 代码（v3 早期版本）
def _flush_table(doc, pending_table):
    if pending_table:
        _add_table_to_doc(doc, pending_table)   # ← 传入原始字符串列表！
        pending_table.clear()
```

- `pending_table` 存的是 `['| 列1 | 列2 | 列3 |', ...]`（字符串列表）
- `_add_table_to_doc` 用 `max(len(r) for r in rows)` 计算列数
- 对字符串求 `len()` 得到字符数（17），不是单元格数（3）
- 结果：4列表格 → 63列 → 每个字符占一个单元格 → 彻底错乱

### 修复方案

```python
# ✅ 正确代码（当前版本）
def _flush_table(doc, pending_table):
    if pending_table:
        parsed_rows = _parse_md_table(pending_table)  # ← 新增：先解析为二维数组
        _add_table_to_doc(doc, parsed_rows)           # ← 传入解析后的数组
        pending_table.clear()
```

### 验证方法

```python
from docx import Document
doc = Document('F:/agent/整合报告.docx')
for t in doc.tables:
    print(f'{len(t.rows)} rows x {len(t.columns)} cols')
    # 正常列数：2～8 列
    # 如果看到 15+、30+、60+ 列 → Bug 仍存在
```

---

## 已修复：封面风格比较类型错误

### 问题描述

`plan.json` 中 `cover_style` 为整数（如 `4`），但代码用字符串比较，导致封面始终走通用分支，精美封面不生效。

### 根因

```python
# ❌ Bug 代码
cover_style = plan.get('cover_style', '4')
if cover_style == '4':   # 整数 4 != 字符串 '4'，永远为 False
```

### 修复方案

```python
# ✅ 正确代码
cover_style = str(plan.get('cover_style', '4'))
if cover_style == '4':   # 字符串比较，正常生效
```

---

## 已修复：RGB 颜色赋值错误

### 问题描述

使用 `eval(f'0x{hex_color}')` 赋值颜色，导致 `run.font.color.rgb` 收到整数而非 `RGBColor` 对象，报错崩溃。

### 根因

```python
# ❌ Bug 代码
run.font.color.rgb = eval(f'0x{H1_TEXT}')  # eval('0xFFFFFF') → 16777215 (int)
# ValueError: rgb color value must be RGBColor object, got <class 'int'>
```

### 修复方案

```python
# ✅ 正确代码
from docx.shared import RGBColor  # ← 必须导入
run.font.color.rgb = RGBColor.from_string(H1_TEXT)
```

---

## 已修复：增量缓存导致新代码不生效

### 问题描述

修改 `integrate_report.py` 核心逻辑后重新生成，增量模式跳过所有章节。

### 根因

Python 会缓存 `.pyc` 编译文件。修改 `.py` 后若不删除缓存，导入的仍是旧代码。同时 `content_hashes.json` 也导致跳过重写。

### 修复方案

每次修改代码后，两步都要做：

```bash
# 1. 删除 .pyc 缓存
del "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\lobsterai-skill-zip-long-doc-agent\__pycache__\integrate_report.cpython-311.pyc"

# 2. 删除增量 hash
del F:\agent\chapters\content_hashes.json

# 3. 重新生成
python integrate_report.py
```

---

## 强制重建

### 操作步骤

```bash
# 1. 删除增量缓存和旧报告
del F:\agent\chapters\content_hashes.json
del F:\agent\整合报告.docx

# 2. 删除 .pyc 缓存（修改代码后必须）
del "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\lobsterai-skill-zip-long-doc-agent\__pycache__\integrate_report.cpython-311.pyc"

# 3. 重新生成
cd "C:\Users\Administrator\AppData\Roaming\LobsterAI\SKILLs\lobsterai-skill-zip-long-doc-agent"
python integrate_report.py
```

---

---

## 新增：RGBColor 属性访问方式（python-docx 1.2.0）

### 问题描述

运行 `make_docx.py` 时报错：`AttributeError: 'RGBColor' object has no attribute 'red'`

### 根因

python-docx 1.2.0 的 `RGBColor` 对象不支持 `.red / .green / .blue` 属性访问，须用索引方式。

### 修复方案

```python
# ❌ 错误
'{:02X}{:02X}{:02X}'.format(rgb.red, rgb.green, rgb.blue)

# ✅ 正确
'{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])
```

---

## 新增：封面函数不得修改全局页边距

### 问题描述

`add_cover()` 中设置 `section.left_margin=0` 等代码会沿袭到封面之后的所有页面，导致正文文字撑满整页（无边距）。

### 根因

Word 的 Section 属性是跨页传递的，在封面设置的边距会影响整个文档。

### 修复方案

封面用全屏表格实现背景色即可，**不要**修改 section 的任何 margin 属性。正文边距在 `main()` 里一次性设置。

```python
# ❌ 错误
def add_cover(doc):
    sec = doc.sections[0]
    sec.left_margin=Inches(0)   # ← 会影响所有页面！
    ...

# ✅ 正确：只放表格，不碰 section
def add_cover(doc):
    tbl_ = doc.add_table(rows=1, cols=1)
    cell = tbl_.rows[0].cells[0]
    # 表格填满整页即可，不要动 section margin
```

---

## 新增：文件被占用时自动换名保存

### 问题描述

生成的 docx 文件如果已被 WPS/Word 打开，再次保存会报 `PermissionError`（Permission denied）。

### 修复方案

文件名加 `_v2` 后缀（自动递增），避免覆盖已打开文件。代码中：

```python
out_name = '医院人员定位管理系统_方案.docx'
out_path = os.path.join(out_dir, out_name)
if os.path.exists(out_path):
    # 文件存在，加 v2/v3 ... 避免冲突
    base, ext = os.path.splitext(out_name)
    counter = 2
    while os.path.exists(os.path.join(out_dir, f'{base}_v{counter}{ext}')):
        counter += 1
    out_name = f'{base}_v{counter}{ext}'
    out_path = os.path.join(out_dir, out_name)
```

---

## 新增：write 工具有 50KB 行数限制，大脚本要分块写入

### 问题描述

用 `write` 工具写超过 ~50KB 或 ~2000 行的 Python 脚本时，内容会被截断（只写入了部分代码）。

### 根因

write 工具对单文件有大小限制。

### 修复方案

大脚本分两步写：

```python
# Step 1：写主文件（不包含结尾的 main() 调用）
with open('make_docx.py', 'w', encoding='utf-8') as f:
    f.write(main_content)  # 主体内容

# Step 2：追加结尾部分
closing = """
def main():
    ...  # 结尾内容

if __name__ == '__main__':
    main()
"""
with open('make_docx.py', 'a', encoding='utf-8') as f:
    f.write(closing)
```

---

## 其他常见问题

### 症状：表格内容全是 `|`

`_parse_md_table` 未被调用。请确认 `_flush_table` 中包含 `parsed_rows = _parse_md_table(pending_table)`。

### 症状：增量模式跳过修改的章节

删除 `content_hashes.json` 即可强制全量重建。

### 症状：子Agent写入的txt包含乱码

子Agent输出时设置了错误的 encoding。请确保子Agent保存时使用 `encoding='utf-8'`。
