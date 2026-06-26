---
name: lottery-ssq
description: 双色球选号辅助系统 v2 - 基于历史数据的概率优化选号工具，支持动态冷热周期、AC 值/极距/尾数形态筛选、蓝球细化分析、多策略输出（稳健/均衡/激进）。每期输出 2 注主推 +3 注备选。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3"], "python_packages": ["requests", "beautifulsoup4"] },
      "install": [
        {
          "id": "python-deps",
          "kind": "exec",
          "command": ["pip3", "install", "-q", "requests", "beautifulsoup4"],
          "label": "Install Python dependencies for lottery-ssq"
        }
      ]
    }
  }
---

# 双色球选号系统 v2

## 功能

- 基于 3400+ 期历史开奖数据分析
- 动态冷热周期（10/20/30 期加权）
- AC 值、极距、尾数和形态筛选
- 蓝球细化（分区 + 奇偶 + 遗漏）
- 多策略支持（稳健/均衡/激进）
- 近期走势动态加权
- 每期输出 2 注主推 + 3 注备选

## 使用方法

### 1. 更新历史开奖数据

```bash
python3 scripts/update_ssq_history.py
```

### 2. 生成当期选号结果

```bash
python3 scripts/generate_ssq.py
```

### 3. （可选）回测历史表现

```bash
python3 scripts/backtest_ssq.py
```

## 输出说明

- **主推**：2 注（评分最高）
- **备选**：3 注（评分次高）
- 每注包含：红球 6 码 + 蓝球 1 码、评分、奇偶比、分区、和值、极距、AC 值

## 配置

编辑 `config.json` 可调整：
- 候选池大小
- 冷热周期
- 形态阈值（AC 值、极距、尾数和）
- 默认策略（stable/balanced/aggressive）

## 注意

彩票是随机事件，本系统是纪律化选号工具，不是预测工具。

所有改进仅基于历史统计规律，不保证中奖。

## 文件结构

```
lottery-ssq/
├── config.json                 # 配置文件
├── data/
│   └── ssq_history.csv        # 历史开奖数据
├── scripts/
│   ├── generate_ssq.py        # 选号脚本
│   ├── update_ssq_history.py  # 数据更新脚本
│   └── backtest_ssq.py        # 回测脚本
├── outputs/                    # 选号结果输出
├── backtests/                  # 回测结果输出
├── docs/
│   └── strategy.md            # 策略说明
└── README.md                   # 使用说明
```

## 版本

- v2.0.0 - 动态冷热周期、形态筛选、多策略支持
- v1.0.0 - 基础选号逻辑
