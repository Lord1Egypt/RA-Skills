---
name: lunar-converter
description: |
  阴历（农历）与阳历（公历）日期转换工具。
  当用户需要：
  (1) 阴历转阳历（如"阴历2月12是阳历几号"、"2026年阴历生日"）
  (2) 阳历转阴历（如"2026年3月26日是阴历多少"）
  (3) 查询某个阴历日期对应的阳历日期
  (4) 任何阴历阳历相互转换的需求
---

# 阴历转换工具

## 功能

- **阴历转阳历**：输入阴历年月日，返回对应的阳历日期
- **阳历转阴历**：输入阳历年月日，返回对应的阴历日期

## 使用方法

调用 `scripts/lunar.py` 脚本：

### 阴历转阳历

```bash
python scripts/lunar.py lunar2solar <年份> <月份> <日期>
```

示例：查询 2026 年阴历 2 月 12 日对应的阳历
```bash
python scripts/lunar.py lunar2solar 2026 2 12
# 输出: {"result": "2026-03-30"}
```

### 阳历转阴历

```bash
python scripts/lunar.py solar2lunar <年份> <月份> <日期>
```

示例：查询 2026 年 3 月 30 日对应的阴历
```bash
python scripts/lunar.py solar2lunar 2026 3 30
# 输出: {"result": "2026年二月十二"}
```

## 注意事项

- 使用 `lunardate` Python 库（已预装）
- 支持范围：1900-2100 年
- 阴历日期每年对应的阳历可能不同，查询时需指定年份
- 输出为 JSON 格式，方便程序解析
