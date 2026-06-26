---
name: pans-churn-predictor
description: |
  AI算力销售客户流失预警工具。分析用量趋势、支持ticket、合同状态，识别流失风险客户。
  支持风险分级、原因分析、挽回建议生成。
  触发词：流失预警, 客户健康度, 续约风险, churn prediction, 客户成功
---

# pans-churn-predictor - 客户流失预警工具

## 功能概述

AI算力销售客户流失预警系统，通过多维度数据分析识别流失风险客户，生成挽回建议。

## 核心能力

### 1. 流失信号检测

- **用量下降**：连续3个月用量下降
- **任务减少**：训练/推理任务数持续减少
- **支持增加**：支持ticket数量异常增加
- **合同风险**：合同到期前90天无续约动作
- **竞品调研**：检测到竞品调研行为

### 2. 风险等级

- 🔴 **高风险**：多个信号同时触发
- 🟡 **中风险**：单一信号触发
- 🟢 **正常**：无明显风险信号

### 3. 挽回建议

针对不同流失原因，生成个性化挽回策略。

## 使用方法

```bash
# 分析所有客户
python3 ~/.qclaw/skills/pans-churn-predictor/scripts/churn.py --analyze

# 分析指定客户
python3 ~/.qclaw/skills/pans-churn-predictor/scripts/churn.py --client "客户名称"

# 列出高风险客户
python3 ~/.qclaw/skills/pans-churn-predictor/scripts/churn.py --list

# 显示流失原因
python3 ~/.qclaw/skills/pans-churn-predictor/scripts/churn.py --client "客户名称" --reason

# 生成挽回建议
python3 ~/.qclaw/skills/pans-churn-predictor/scripts/churn.py --client "客户名称" --suggest
```

## 数据存储

客户数据存储在 `~/.qclaw/skills/pans-churn-predictor/data/` 目录下：

- `clients.json` - 客户基础信息
- `usage_history.json` - 用量历史数据
- `tickets.json` - 支持ticket记录
- `contracts.json` - 合同信息

## 典型场景

1. **日常健康检查**：每日运行 `--list` 查看高风险客户
2. **深度分析**：对单个客户运行 `--analyze --reason --suggest`
3. **续约前预警**：合同到期前90天自动提醒
4. **季度复盘**：分析流失趋势，优化客户成功策略