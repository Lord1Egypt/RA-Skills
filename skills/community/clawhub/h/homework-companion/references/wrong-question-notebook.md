# 错题本规范与 Excel 生成模板

当孩子做错题目时，按本规范记录，并生成可累积、可按知识点筛选的 Excel 错题本。

---

## 一、字段定义

| 字段 | 说明 | 示例 |
|:---|:---|:---|
| 日期 | 记录当天 YYYY-MM-DD | 2026-07-29 |
| 学科 | 数学/语文/英语/科学 | 数学 |
| 学段 | 小学低段/高段/初中/高中 | 小学高段 |
| 题目标题 | 一句话概括 | 长方形周长求面积 |
| 题目原文 | OCR 识别的题目全文 | 一个长方形周长24cm… |
| 孩子答案 | 孩子给出的错误答案 | 长8宽4 |
| 错误原因 | 归类 + 简述 | 概念混淆：把"周长一半"当成长 |
| 正确思路 | 标准解法步骤（简洁） | 周长/2=12→长+宽=12→… |
| 知识点标签 | 用于筛选复习 | 周长与面积, 和差问题 |
| 难度 | ★~★★★ | ★★ |
| 掌握状态 | 待巩固/已掌握 | 待巩固 |
| 复习次数 | 重练过的次数 | 0 |

---

## 二、Excel 生成（Python 模板）

使用 WorkBuddy 的 Python 环境生成/追加 `.xlsx`。首次创建文件，之后追加新行。

```python
# -*- coding: utf-8 -*-
import os
from openpyxl import Workbook, load_workbook

XLSX_PATH = "错题本.xlsx"
HEADERS = ["日期","学科","学段","题目标题","题目原文","孩子答案",
           "错误原因","正确思路","知识点标签","难度","掌握状态","复习次数"]

def append_record(record: dict):
    """record 键需对应 HEADERS（除复习次数外由调用方提供，复习次数默认0）"""
    if os.path.exists(XLSX_PATH):
        wb = load_workbook(XLSX_PATH)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "错题本"
        ws.append(HEADERS)
    row = [record.get(h, "") for h in HEADERS[:11]] + [record.get("掌握状态", "待巩固"), 0]
    ws.append(row)
    # 自动调整列宽，方便阅读
    for col, h in enumerate(HEADERS, start=1):
        ws.column_dimensions[chr(64 + col)].width = 16 if h != "题目原文" and h != "正确思路" else 40
    wb.save(XLSX_PATH)
    return XLSX_PATH
```

> 安装依赖：`pip install openpyxl`（在 WorkBuddy 隔离环境中执行）。

---

## 三、使用约定

1. **同一份文件累积**：错题本应跨会话保留，新错题追加到同一 `错题本.xlsx`，不每次新建。
2. **知识点可筛选**：生成后告知家长"可在 Excel 里按『知识点标签』筛选，考前针对性重练"。
3. **复习闭环**：孩子重做对的题，把"掌握状态"改为"已掌握"，"复习次数"+1。
4. **隐私**：错题本只存题目与学习数据，不存孩子真实姓名、学校等身份信息。
5. **输出路径**：默认保存到用户工作目录，生成后告知完整路径，可一键打开。
