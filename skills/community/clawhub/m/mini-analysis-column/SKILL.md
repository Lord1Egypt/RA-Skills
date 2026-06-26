---
name: analysis_column
description: 统计分析csv文件中某一列的表现
version: 0.1.1
triggers:
  - "analysis_column"
  - 评分效果
  - "帮我看看csv文件的表现"
---

# analysis_column

统计分析 CSV 文件中某一列的表现，支持数值列的统计计算。

## 功能

- 数值列：计算最大值、最小值、平均值

## 依赖

需要先安装依赖：
```bash
pip install pandas
```

## 使用方法

```bash
python scripts/compute.py --file <CSV文件路径> --rowkey <列名> [--debug]
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| --file | 是 | CSV 文件路径 |
| --rowkey | 是 | 要分析的列名（必须是数值列） |
| --debug | 否 | 开启调试模式，显示更多信息 |

## 示例

```bash
python scripts/compute.py --file data.csv --rowkey score
```

输出：
```
程序调用成功
最大值: 1000
最小值: 1
平均值: 505.77
```

## 注意事项

- CSV 文件需要包含表头
- 目前仅支持数值列的统计计算
- 字符串列暂不支持
