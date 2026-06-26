# JSON深度比对工具

---
name: json-deep-compare
description: 实现两个JSON文件的深度比对，支持无序列表比对，支持配置忽略字段，将比对差异输出到Excel文件。适用于接口测试数据验证、配置文件对比、数据迁移验证等场景。
---

## 功能说明

- 深度比对两个JSON文件的所有字段
- 支持无序列表（数组）的智能匹配比对
- 支持配置忽略字段（如时间戳、ID等动态字段）
- 支持多种差异类型识别：新增、删除、修改、类型不一致
- 将比对结果输出为结构化的Excel报告
- 支持嵌套JSON对象的递归比对

## 使用方式

### Python脚本方式

```python
from json_deep_compare import compare_json_files, compare_json_objects
import json

# 比对两个JSON文件
result = compare_json_files(
    file1_path="data1.json",
    file2_path="data2.json",
    output_excel="comparison_result.xlsx",
    ignore_fields=["created_at", "updated_at", "id"],  # 忽略字段
    ignore_order=True  # 忽略数组顺序
)

# 或者直接比对JSON对象
with open("data1.json", "r") as f:
    obj1 = json.load(f)
with open("data2.json", "r") as f:
    obj2 = json.load(f)

result = compare_json_objects(
    obj1=obj1,
    obj2=obj2,
    output_excel="comparison_result.xlsx",
    ignore_fields=["timestamp", "request_id"],
    ignore_order=True
)

print(f"差异总数: {result['total_differences']}")
print(f"Excel报告: {result['output_file']}")
```

### 命令行方式

**安装依赖**:
```bash
pip install openpyxl
```

**比对两个JSON文件**:
```bash
python json_compare.py data1.json data2.json
```

**指定输出文件**:
```bash
python json_compare.py data1.json data2.json -o result.xlsx
```

**配置忽略字段**:
```bash
python json_compare.py data1.json data2.json -i "created_at,updated_at,id"
```

**严格模式（数组顺序必须一致）**:
```bash
python json_compare.py data1.json data2.json --strict-order
```

**完整示例**:
```bash
python json_compare.py data1.json data2.json \
    -o comparison.xlsx \
    -i "timestamp,request_id,trace_id" \
    --ignore-order
```

## 完整代码

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON深度比对工具
支持无序列表比对、忽略字段配置、Excel输出
"""

import json
import sys
import os
from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


class JSONComparator:
    """JSON深度比对器"""
    
    def __init__(self, ignore_fields: List[str] = None, ignore_order: bool = True):
        """
        初始化比对器
        
        Args:
            ignore_fields: 需要忽略的字段列表（支持点号路径，如 "user.id"）
            ignore_order: 是否忽略数组顺序
        """
        self.ignore_fields = set(ignore_fields or [])
        self.ignore_order = ignore_order
        self.differences = []
        self.current_path = []
    
    def _should_ignore(self, path: str) -> bool:
        """检查字段是否应该被忽略"""
        # 检查完整路径
        if path in self.ignore_fields:
            return True
        # 检查字段名（不考虑路径）
        field_name = path.split(".")[-1] if "." in path else path
        if field_name in self.ignore_fields:
            return True
        return False
    
    def _get_path(self, key: str = None) -> str:
        """获取当前路径"""
        parts = self.current_path.copy()
        if key is not None:
            parts.append(str(key))
        return ".".join(parts) if parts else "root"
    
    def _add_difference(self, diff_type: str, path: str, value1: Any, value2: Any, 
                       description: str = ""):
        """添加差异记录"""
        self.differences.append({
            "type": diff_type,
            "path": path,
            "expected": self._format_value(value1),
            "actual": self._format_value(value2),
            "description": description
        })
    
    def _format_value(self, value: Any) -> str:
        """格式化值为字符串"""
        if value is None:
            return "null"
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)
    
    def _compare_values(self, value1: Any, value2: Any, key: str = None):
        """比对两个值"""
        path = self._get_path(key)
        
        # 检查是否应该忽略
        if self._should_ignore(path):
            return
        
        # 类型不同
        if type(value1) != type(value2):
            self._add_difference(
                "类型不一致", path, value1, value2,
                f"类型不同: {type(value1).__name__} vs {type(value2).__name__}"
            )
            return
        
        # 都是字典
        if isinstance(value1, dict):
            self._compare_dicts(value1, value2)
            return
        
        # 都是列表
        if isinstance(value1, list):
            self._compare_lists(value1, value2, path)
            return
        
        # 基本类型比较
        if value1 != value2:
            self._add_difference(
                "值不同", path, value1, value2,
                f"期望值: {value1}, 实际值: {value2}"
            )
    
    def _compare_dicts(self, dict1: Dict, dict2: Dict):
        """比对两个字典"""
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            path = self._get_path(key)
            
            if self._should_ignore(path):
                continue
            
            if key not in dict1:
                self._add_difference("新增字段", path, None, dict2[key],
                                   f"字段 '{key}' 在第二个JSON中存在，第一个中不存在")
            elif key not in dict2:
                self._add_difference("删除字段", path, dict1[key], None,
                                   f"字段 '{key}' 在第一个JSON中存在，第二个中不存在")
            else:
                self.current_path.append(str(key))
                self._compare_values(dict1[key], dict2[key], key)
                self.current_path.pop()
    
    def _compare_lists(self, list1: List, list2: List, path: str):
        """比对两个列表"""
        if len(list1) != len(list2):
            self._add_difference(
                "数组长度不同", path, list1, list2,
                f"数组长度不同: {len(list1)} vs {len(list2)}"
            )
        
        if self.ignore_order and len(list1) > 0 and isinstance(list1[0], dict):
            # 无序比对：尝试匹配字典元素
            self._compare_unordered_lists(list1, list2, path)
        else:
            # 有序比对
            self._compare_ordered_lists(list1, list2, path)
    
    def _compare_ordered_lists(self, list1: List, list2: List, path: str):
        """有序列表比对"""
        max_len = max(len(list1), len(list2))
        for i in range(max_len):
            self.current_path.append(f"[{i}]")
            if i >= len(list1):
                self._add_difference("新增元素", self._get_path(), None, list2[i],
                                   f"索引 {i} 的元素在第二个列表中存在")
            elif i >= len(list2):
                self._add_difference("删除元素", self._get_path(), list1[i], None,
                                   f"索引 {i} 的元素在第一个列表中存在")
            else:
                self._compare_values(list1[i], list2[i])
            self.current_path.pop()
    
    def _compare_unordered_lists(self, list1: List, list2: List, path: str):
        """无序列表比对（智能匹配）"""
        # 为每个元素生成唯一标识（基于所有字段的哈希）
        def get_element_id(elem):
            if isinstance(elem, dict):
                return json.dumps(elem, sort_keys=True, ensure_ascii=False)
            return str(elem)
        
        # 统计元素出现次数
        from collections import Counter
        count1 = Counter(get_element_id(e) for e in list1)
        count2 = Counter(get_element_id(e) for e in list2)
        
        # 找出差异
        all_ids = set(count1.keys()) | set(count2.keys())
        
        for elem_id in all_ids:
            c1, c2 = count1.get(elem_id, 0), count2.get(elem_id, 0)
            if c1 != c2:
                elem = json.loads(elem_id) if elem_id.startswith("{") else elem_id
                if c1 > c2:
                    self._add_difference(
                        "数组元素数量不同", path, elem, None,
                        f"元素在第一个列表中出现 {c1} 次，第二个列表中出现 {c2} 次"
                    )
                else:
                    self._add_difference(
                        "数组元素数量不同", path, None, elem,
                        f"元素在第一个列表中出现 {c1} 次，第二个列表中出现 {c2} 次"
                    )
    
    def compare(self, obj1: Any, obj2: Any) -> List[Dict]:
        """
        执行比对
        
        Args:
            obj1: 第一个JSON对象
            obj2: 第二个JSON对象
            
        Returns:
            List[Dict]: 差异列表
        """
        self.differences = []
        self.current_path = []
        self._compare_values(obj1, obj2)
        return self.differences


def export_to_excel(differences: List[Dict], output_path: str) -> str:
    """
    将差异导出到Excel
    
    Args:
        differences: 差异列表
        output_path: 输出文件路径
        
    Returns:
        str: 输出文件路径
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "JSON比对结果"
    
    # 设置标题样式
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # 差异类型颜色
    type_colors = {
        "新增字段": "C6EFCE",
        "新增元素": "C6EFCE",
        "删除字段": "FFC7CE",
        "删除元素": "FFC7CE",
        "值不同": "FFEB9C",
        "类型不一致": "B8CCE4",
        "数组长度不同": "E7E6E6",
        "数组元素数量不同": "E7E6E6"
    }
    
    # 写入标题
    headers = ["序号", "差异类型", "字段路径", "预期值", "实际值", "说明"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # 写入数据
    for idx, diff in enumerate(differences, 1):
        row = idx + 1
        ws.cell(row=row, column=1, value=idx)
        ws.cell(row=row, column=2, value=diff["type"])
        ws.cell(row=row, column=3, value=diff["path"])
        ws.cell(row=row, column=4, value=diff["expected"])
        ws.cell(row=row, column=5, value=diff["actual"])
        ws.cell(row=row, column=6, value=diff.get("description", ""))
        
        # 设置差异类型颜色
        fill_color = type_colors.get(diff["type"], "FFFFFF")
        for col in range(1, 7):
            ws.cell(row=row, column=col).fill = PatternFill(
                start_color=fill_color, end_color=fill_color, fill_type="solid"
            )
    
    # 设置列宽
    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 15
    ws.column_dimensions["C"].width = 30
    ws.column_dimensions["D"].width = 40
    ws.column_dimensions["E"].width = 40
    ws.column_dimensions["F"].width = 40
    
    # 添加汇总信息
    ws2 = wb.create_sheet("汇总")
    ws2.cell(row=1, column=1, value="比对汇总").font = Font(bold=True, size=14)
    ws2.cell(row=2, column=1, value="比对时间")
    ws2.cell(row=2, column=2, value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ws2.cell(row=3, column=1, value="差异总数")
    ws2.cell(row=3, column=2, value=len(differences))
    
    # 统计各类型差异数量
    from collections import Counter
    type_counts = Counter(d["type"] for d in differences)
    row = 5
    ws2.cell(row=row, column=1, value="差异类型统计").font = Font(bold=True)
    for diff_type, count in type_counts.items():
        row += 1
        ws2.cell(row=row, column=1, value=diff_type)
        ws2.cell(row=row, column=2, value=count)
    
    wb.save(output_path)
    return output_path


def compare_json_objects(obj1: Any, obj2: Any, output_excel: str = None,
                        ignore_fields: List[str] = None, 
                        ignore_order: bool = True) -> Dict:
    """
    比对两个JSON对象
    
    Args:
        obj1: 第一个JSON对象
        obj2: 第二个JSON对象
        output_excel: 输出Excel文件路径
        ignore_fields: 忽略字段列表
        ignore_order: 是否忽略数组顺序
        
    Returns:
        Dict: 比对结果
    """
    comparator = JSONComparator(ignore_fields=ignore_fields, ignore_order=ignore_order)
    differences = comparator.compare(obj1, obj2)
    
    result = {
        "total_differences": len(differences),
        "differences": differences,
        "output_file": None
    }
    
    if output_excel and differences:
        output_path = export_to_excel(differences, output_excel)
        result["output_file"] = output_path
        print(f"差异已导出到: {output_path}")
    
    return result


def compare_json_files(file1_path: str, file2_path: str, 
                      output_excel: str = None,
                      ignore_fields: List[str] = None,
                      ignore_order: bool = True) -> Dict:
    """
    比对两个JSON文件
    
    Args:
        file1_path: 第一个JSON文件路径
        file2_path: 第二个JSON文件路径
        output_excel: 输出Excel文件路径
        ignore_fields: 忽略字段列表
        ignore_order: 是否忽略数组顺序
        
    Returns:
        Dict: 比对结果
    """
    # 读取JSON文件
    with open(file1_path, 'r', encoding='utf-8') as f:
        obj1 = json.load(f)
    
    with open(file2_path, 'r', encoding='utf-8') as f:
        obj2 = json.load(f)
    
    # 设置默认输出文件名
    if output_excel is None:
        base_name = os.path.splitext(os.path.basename(file1_path))[0]
        output_excel = f"{base_name}_comparison.xlsx"
    
    return compare_json_objects(obj1, obj2, output_excel, ignore_fields, ignore_order)


# 命令行入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="JSON深度比对工具")
    parser.add_argument("file1", help="第一个JSON文件路径")
    parser.add_argument("file2", help="第二个JSON文件路径")
    parser.add_argument("-o", "--output", help="输出Excel文件路径", 
                       default=None)
    parser.add_argument("-i", "--ignore", help="忽略字段，逗号分隔", 
                       default="")
    parser.add_argument("--strict-order", action="store_true",
                       help="严格模式，数组顺序必须一致")
    
    args = parser.parse_args()
    
    # 解析忽略字段
    ignore_fields = [f.strip() for f in args.ignore.split(",") if f.strip()]
    
    # 执行比对
    result = compare_json_files(
        args.file1, 
        args.file2,
        output_excel=args.output,
        ignore_fields=ignore_fields,
        ignore_order=not args.strict_order
    )
    
    print(f"\n比对完成！")
    print(f"差异总数: {result['total_differences']}")
    if result['output_file']:
        print(f"Excel报告: {result['output_file']}")
    else:
        print("未发现差异")
```

## 输出示例

输入文件：
- `data1.json`: 预期数据
- `data2.json`: 实际数据

执行命令：
```bash
python json_compare.py data1.json data2.json -i "timestamp,id" -o result.xlsx
```

Excel输出包含两个工作表：

**工作表1: JSON比对结果**
| 序号 | 差异类型 | 字段路径 | 预期值 | 实际值 | 说明 |
|------|----------|----------|--------|--------|------|
| 1 | 值不同 | user.name | 张三 | 李四 | 期望值: 张三, 实际值: 李四 |
| 2 | 新增字段 | user.email | null | test@example.com | 字段 'email' 在第二个JSON中存在 |
| 3 | 删除字段 | user.age | 25 | null | 字段 'age' 在第一个JSON中存在 |
| 4 | 类型不一致 | status | "active" | true | 类型不同: str vs bool |
| 5 | 数组长度不同 | items | [...] | [...] | 数组长度不同: 3 vs 2 |

**工作表2: 汇总**
- 比对时间: 2024-01-15 10:30:00
- 差异总数: 5
- 差异类型统计:
  - 值不同: 1
  - 新增字段: 1
  - 删除字段: 1
  - 类型不一致: 1
  - 数组长度不同: 1

## 支持的差异类型

| 差异类型 | 说明 | 颜色标识 |
|----------|------|----------|
| 新增字段 | 第二个JSON中有，第一个中没有 | 绿色 |
| 删除字段 | 第一个JSON中有，第二个中没有 | 红色 |
| 新增元素 | 数组中新增的元素 | 绿色 |
| 删除元素 | 数组中删除的元素 | 红色 |
| 值不同 | 字段值不一致 | 黄色 |
| 类型不一致 | 字段类型不同 | 蓝色 |
| 数组长度不同 | 两个数组长度不一致 | 灰色 |
| 数组元素数量不同 | 无序数组中元素数量不同 | 灰色 |

## 注意事项

1. **忽略字段格式**:
   - 简单字段名: `id`, `timestamp`
   - 完整路径: `user.id`, `data.items[0].name`
   - 支持同时忽略字段名和路径

2. **无序列表比对**:
   - 默认启用，适用于接口返回的无序数据
   - 使用 `--strict-order` 禁用，要求数组顺序一致
   - 仅对字典元素数组启用智能匹配

3. **大文件处理**:
   - 建议JSON文件大小不超过100MB
   - 超大文件可能需要较长时间处理

4. **编码问题**:
   - 默认使用UTF-8编码读取文件
   - 如遇编码错误，请确保文件为UTF-8格式

## 依赖安装

```bash
pip install openpyxl
```

## 进阶用法

### 在测试框架中使用

```python
import unittest
from json_deep_compare import compare_json_objects

class APITestCase(unittest.TestCase):
    def test_api_response(self):
        expected = {"status": "success", "data": {"id": 1, "name": "test"}}
        actual = call_api()  # 调用API
        
        result = compare_json_objects(expected, actual, 
                                    ignore_fields=["timestamp", "request_id"])
        
        self.assertEqual(result["total_differences"], 0, 
                        f"发现差异: {result['differences']}")
```

### 批量比对多个文件对

```python
import os
from json_deep_compare import compare_json_files

file_pairs = [
    ("expected1.json", "actual1.json"),
    ("expected2.json", "actual2.json"),
    ("expected3.json", "actual3.json"),
]

for expected, actual in file_pairs:
    output = f"comparison_{expected}.xlsx"
    result = compare_json_files(expected, actual, 
                              output_excel=output,
                              ignore_fields=["created_at"])
    print(f"{expected}: {result['total_differences']} 个差异")
```
