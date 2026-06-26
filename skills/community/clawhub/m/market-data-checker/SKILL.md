---
name: market-data-checker
description: >
  金融市场数据质量校验工具。对 market_data.json 执行全链路数据质量检查。
  支持 10 类校验规则，可扩展，统一返回通过/拒绝 + 原因。
  当用户要求"检查数据质量"、"数据校验"、"检查日报数据"、"数据完整性检查"时使用。
---

# Market Data Checker Skill

## 概述

`market-data-checker` 对每日生成的 `market_data.json` 进行全链路数据质量校验，覆盖 10 类规则，支持自动重试和告警邮件。

## 校验规则

| # | 规则 | 说明 | 严重程度 |
|---|------|------|----------|
| 1 | 非空校验 | 顶层分类、必填字段（price等）不能为空 | 🔴 阻断 |
| 2 | 非 NaN / 非无穷大 | 数值字段不能是 NaN/Inf/-Inf | 🔴 阻断 |
| 3 | 数值类型强校验 | price/change/volume 类型+范围检查 | 🔴 阻断 |
| 4 | 业务范围合理性 | 各品种价格/涨跌幅是否在合理区间 | 🟡 警告 |
| 5 | 涨跌方向一致性 | 相关品种变化方向是否一致（黄金↔美元等） | 🟡 警告 |
| 6 | 脏数据拦截 | 占位符(N/A/--)、HTML标签、控制字符、超长字段 | 🟡 警告 |
| 7 | 语句完整性 | 文本字段是否以句号结尾、必填字段是否齐全 | 🟡 警告 |
| 8 | 数据缺失自动重试 | 文件不存在/解析失败时最多重试 3 次 | ⚙️ 机制 |
| 9 | 连续失败终止链路 | 连续 3 项校验失败 → 终止链路 + 发送告警邮件 | ⚙️ 机制 |
| 10 | 统一返回 | 通过 / 拒绝 + 问题清单（CheckResult 格式） | ⚙️ 机制 |

## 使用方式

### 方式1：一键检查

```bash
python skills/market-data-checker/scripts/check_data.py
```

### 方式2：指定日期

```bash
python skills/market-data-checker/scripts/check_data.py --date 2026-05-16
```

### 方式3：指定文件路径

```bash
python skills/market-data-checker/scripts/check_data.py --file E:\daily\2026-05-16\market_data.json
```

### 方式4：指定重试次数

```bash
python skills/market-data-checker/scripts/check_data.py --retry 5
```

## 输出示例

```
============================================================
  数据质量检查 | 2026-05-16 10:35:22
============================================================

  [1/7] 执行非空校验 ...           ✅ 通过
  [2/7] 执行非NaN/非无穷大校验 ... ✅ 通过
  [3/7] 执行数值类型强校验 ...     ✅ 通过
  [4/7] 执行业务范围合理性校验 ...  ✅ 通过
  [5/7] 执行涨跌方向一致性校验 ...  ⚠️  2 个警告
  [6/7] 执行脏数据拦截 ...         ✅ 通过
  [7/7] 执行语句完整性校验 ...      ✅ 通过

============================================================
  ✅ 检查通过 | 共 7 项，无问题
============================================================
```

```
============================================================
  ❌ 检查拒绝 | 共 3 个问题：

  [业务范围合理性] 欧洲市场 > 德国DAX 30.price
    值：99999.0
    原因：德国DAX 30.price = 99999.0，超出合理范围 [5000, 25000]

  [脏数据拦截] 政策动态.美国 > [0].标题
    值：N/A
    原因：检测到脏数据模式 [占位符]：匹配 ^N/A$

  [语句完整性] 环球市场速览 > 概述
    值：美股三大指数涨跌互现，小幅收涨
    原因：概述未以完整句号结尾
============================================================
```

## 架构

```
check_data.py          # 主入口，MarketDataChecker 类
├── validators/
│   ├── __init__.py
│   ├── null_check.py          # 规则1：非空校验
│   ├── nan_check.py           # 规则2：非NaN/非无穷大
│   ├── type_check.py          # 规则3：数值类型强校验
│   ├── range_check.py         # 规则4：业务范围合理性
│   ├── direction_check.py     # 规则5：涨跌方向一致性
│   ├── dirty_check.py         # 规则6：脏数据拦截
│   └── completeness_check.py   # 规则7：语句完整性
```

## 扩展新的校验规则

1. 在 `validators/` 目录下新建 `xxx_check.py`
2. 继承 `CheckResult` 基类，实现 `check(data: dict) -> CheckResult` 方法
3. 在 `check_data.py` 的 `checkers` 列表中追加新 checker 实例

```python
# validators/example_check.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from check_data import CheckResult

class ExampleChecker:
    def check(self, data: dict) -> CheckResult:
        result = CheckResult()
        # ... 校验逻辑
        return result
```

## 配置文件

全局配置位于 `check_data.py` 顶部的 `CONFIG` 字典：

```python
CONFIG = {
    "MAX_RETRIES": 3,          # 最大重试次数
    "RETRY_DELAY": 2.0,        # 重试间隔（秒）
    "CONSECUTIVE_FAILURES_THRESHOLD": 3,  # 连续失败阈值
    "ALERT_EMAIL": "13045609072@163.com",
    "ALERT_SMTP_HOST": "smtp.163.com",
    "ALERT_SMTP_PORT": 25,
    "ALERT_SENDER": "13045609072@163.com",
    "ALERT_RECIPIENT": "yugi.chong@fubonchina.com",
}
```

## 规则说明

### 规则4：业务范围合理性（RangeChecker）

已内置各主要品种的范围规则：

| 品种 | 价格合理范围 | 涨跌幅合理范围 |
|------|-------------|---------------|
| 道指 | 20000 ~ 60000 | ±15% |
| 标普500 | 1000 ~ 10000 | ±15% |
| COMEX黄金 | 1000 ~ 3000 | ±8% |
| WTI原油 | 20 ~ 200 | ±15% |
| 上证指数 | 1500 ~ 8000 | ±15% |
| 恒生指数 | 10000 ~ 50000 | ±15% |
| USD/CNY | 6.0 ~ 10.0 | ±5% |

范围规则定义在 `validators/range_check.py` 的 `RANGE_RULES` 字典中，后续可随时扩展。

### 规则5：涨跌方向一致性（DirectionChecker）

已内置方向规则：
- **同向**：A股各指数（沪深300与上证）、黄金与白银、欧洲各指数（DAX与CAC40）等
- **反向**：黄金与美元指数

### 规则6：脏数据拦截（DirtyChecker）

检测以下脏数据模式：
- 占位符：`N/A`、`--`、`null`、`{{}}`、`待更新`、`暂无数据`
- HTML残留：`<tag>`、HTML实体（`&nbsp;`等）
- 控制字符：`\x00-\x1f`（除换行/回车外）
- 超长字段：超过各字段类型的长度上限