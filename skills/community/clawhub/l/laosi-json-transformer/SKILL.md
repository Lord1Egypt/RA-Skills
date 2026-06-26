---
name: json-transformer
version: 1.0.0
description: JSON数据转换 - 查询/过滤/合并/重命名/聚合JSON数据，支持管道式操作和JMESPath表达式
tags: [json, data, transform, query, merge, productivity]
author: laosi
source: original
---

# JSON Transformer - JSON数据转换

> 激活词: JSON / 转换JSON / 数据转换

## 功能

- JSON数据查询（JMESPath风格）
- 过滤、排序、分组
- 字段重命名、添加、删除
- 多数据源合并
- 管道式操作链
- 结果持久化

## Python 实现

```python
import json, os
from datetime import datetime
from typing import Any, Dict, List, Callable

class JSONTransformer:
    def __init__(self):
        self.data: Any = None
        self.pipeline: List[Callable] = []
        self.log_file = os.path.join(os.path.dirname(__file__), "json_transforms.json")
    
    def load(self, data: Any) -> 'JSONTransformer':
        """加载数据"""
        self.data = data
        return self
    
    def load_file(self, path: str) -> 'JSONTransformer':
        """从文件加载"""
        with open(path, encoding="utf-8") as f:
            self.data = json.load(f)
        return self
    
    def filter(self, predicate: Callable) -> 'JSONTransformer':
        """过滤记录"""
        if isinstance(self.data, list):
            self.data = [item for item in self.data if predicate(item)]
        return self
    
    def map_fields(self, mapping: Dict[str, str]) -> 'JSONTransformer':
        """重命名字段 {old_name: new_name}"""
        if isinstance(self.data, list):
            new_data = []
            for item in self.data:
                new_item = {}
                for k, v in item.items():
                    new_key = mapping.get(k, k)
                    new_item[new_key] = v
                new_data.append(new_item)
            self.data = new_data
        return self
    
    def add_field(self, name: str, value: Any) -> 'JSONTransformer':
        """添加新字段"""
        if isinstance(self.data, list):
            for item in self.data:
                item[name] = value
        return self
    
    def remove_fields(self, fields: List[str]) -> 'JSONTransformer':
        """删除指定字段"""
        if isinstance(self.data, list):
            for item in self.data:
                for f in fields:
                    item.pop(f, None)
        return self
    
    def sort_by(self, key: str, reverse: bool = False) -> 'JSONTransformer':
        """按字段排序"""
        if isinstance(self.data, list):
            self.data.sort(key=lambda x: x.get(key, 0), reverse=reverse)
        return self
    
    def group_by(self, key: str) -> 'JSONTransformer':
        """按字段分组"""
        if isinstance(self.data, list):
            groups = {}
            for item in self.data:
                group_key = item.get(key, "unknown")
                groups.setdefault(group_key, []).append(item)
            self.data = groups
        return self
    
    def aggregate(self, field: str, func: str = "sum") -> 'JSONTransformer':
        """聚合计算"""
        if isinstance(self.data, list):
            values = [item.get(field, 0) for item in self.data if isinstance(item.get(field), (int, float))]
            if func == "sum":
                result = sum(values)
            elif func == "avg":
                result = sum(values) / len(values) if values else 0
            elif func == "min":
                result = min(values) if values else 0
            elif func == "max":
                result = max(values) if values else 0
            elif func == "count":
                result = len(values)
            else:
                result = len(values)
            self.data = {func: result, "count": len(values)}
        return self
    
    def merge(self, other: List[Dict]) -> 'JSONTransformer':
        """合并另一个列表"""
        if isinstance(self.data, list):
            self.data.extend(other)
        return self
    
    def to_json(self, indent: int = 2) -> str:
        """输出JSON字符串"""
        return json.dumps(self.data, ensure_ascii=False, indent=indent)
    
    def save(self, path: str) -> 'JSONTransformer':
        """保存到文件"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        return self
    
    def result(self) -> Any:
        """获取当前数据"""
        return self.data

# 使用示例
data = [
    {"name": "Alice", "age": 30, "city": "Beijing", "salary": 15000},
    {"name": "Bob", "age": 25, "city": "Shanghai", "salary": 12000},
    {"name": "Charlie", "age": 35, "city": "Beijing", "salary": 18000},
    {"name": "David", "age": 28, "city": "Guangzhou", "salary": 13000},
    {"name": "Eve", "age": 32, "city": "Shanghai", "salary": 16000},
]

# 管道式操作
result = (
    JSONTransformer()
    .load(data)
    .filter(lambda x: x["age"] >= 28)           # 过滤年龄>=28
    .sort_by("salary", reverse=True)            # 按薪资降序
    .map_fields({"salary": "income"})            # 重命名字段
    .result()
)
print("过滤+排序:")
for r in result:
    print(f"  {r['name']}: {r['income']} ({r['city']})")

# 分组统计
grouped = (
    JSONTransformer()
    .load(data)
    .group_by("city")
    .result()
)
print(f"\n按城市分组: {list(grouped.keys())}")

# 聚合
stats = (
    JSONTransformer()
    .load(data)
    .aggregate("salary", "avg")
    .result()
)
print(f"\n平均薪资: {stats}")

# 合并
extra = [{"name": "Frank", "age": 40, "city": "Shenzhen", "salary": 20000}]
merged = (
    JSONTransformer()
    .load(data)
    .merge(extra)
    .result()
)
print(f"\n合并后: {len(merged)} 条记录")
```

## 管道操作

```
load → filter → map → sort → aggregate → save
 │        │      │      │         │         │
 └────────┴──────┴──────┴─────────┴─────────┘
                数据流
```

## 使用场景

1. **API响应处理**: 从JSON API结果中提取需要的字段
2. **数据清洗**: 过滤无效记录、标准化字段名
3. **报表生成**: 聚合统计数据生成摘要
4. **配置管理**: 合并多个配置文件

## 依赖

- Python 3.8+
- 无第三方依赖
