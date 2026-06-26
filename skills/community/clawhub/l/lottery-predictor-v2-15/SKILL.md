---
name: lottery-predictor-v2.15
description: 基于 V2.15 数学模型的双色球预测工具，包含均值回归、正态分布、大数定律、卡方检验等 7 种算法，提供红球 TOP10 和蓝球 TOP4 推荐。
license: MIT
compatibility: Python 3.8+, SQLite3
metadata:
  {"openclaw": {"requires": {"bins": ["python3", "sqlite3"], "env": ["LOTTERY_DB_PATH"]}, "primaryEnv": "LOTTERY_DB_PATH"}}
---

# 🎰 彩票预测技能（V2.15 数学模型）

基于高等数学的双色球预测工具，整合 7 种经典数学模型，提供科学的号码推荐。

## 核心算法

### 7 种数学模型
1. **均值回归模型**（权重 25%）- 极端值向平均值回归
2. **正态分布模型**（权重 22%）- 和值分布预测
3. **大数定律**（权重 18%）- 历史频率估计
4. **卡方检验**（权重 15%）- 冷热号判断
5. **马尔可夫链**（权重 8%）- 状态转移概率
6. **时间序列**（权重 7%）- 近期趋势分析
7. **泊松分布**（权重 5%）- 连号/同尾号概率

### 模型特点
- ✅ 基于 3430+ 期历史数据
- ✅ 纯离线分析，无 API 调用
- ✅ 自动防错（阻止跨期预测）
- ✅ 输出可解释性报告

## 可用工具

### predict_lottery
预测下一期彩票号码

**参数：**
- `issue` (string, 必需): 预测期号，格式 YYYYNNN（如 2026035）
- `lottery_type` (string, 可选): 彩种类型，默认 "ssq"（双色球）
- `top_n` (integer, 可选): 推荐红球数量，默认 10

**返回：**
- `red_top10`: 红球推荐 TOP10
- `blue_top4`: 蓝球推荐 TOP4
- `combos`: 推荐组合（3 组）
- `analysis`: 分析报告

### get_prediction_history
获取历史预测记录

**参数：**
- `limit` (integer, 可选): 返回记录数，默认 10

### verify_prediction
验证预测准确率（开奖后使用）

**参数：**
- `issue` (string, 必需): 期号
- `actual_numbers` (array, 必需): 实际开奖号码

## 定价策略

- **免费：** 3 次/月（体验核心功能）
- **付费：** ¥29/月（无限次 + 高级功能）
- **性价比：** 市场最低价（竞品¥50-200/月）

## 使用示例

```
帮我预测双色球 2026035 期
```

```
用 lottery-predictor-v2.15 预测下一期
```

```
查看上期预测准确率
```

## 环境要求

需要设置以下环境变量：
- `LOTTERY_DB_PATH`: 彩票数据库路径（默认：~/.openclaw/workspace/projects/caipiao/data/caipiao.db）

## 输出说明

### 红球推荐
- TOP10 号码池（按概率排序）
- 第一梯队（6 码）：均值回归 + 正态分布
- 第二梯队（4 码）：大数定律 + 卡方检验

### 蓝球推荐
- TOP4 号码（按概率排序）
- 每个号码附带模型依据

### 推荐组合
- 第 1 组：均值回归组合
- 第 2 组：正态分布组合
- 第 3 组：大数定律组合

## 注意事项

⚠️ **重要声明：**
- 彩票是随机游戏，模型不能保证准确
- 历史数据参考，过去表现不代表未来
- 理性购彩，建议小额娱乐
- 购彩决策请自行判断

## 数据来源

- 数据库：SQLite（~/.openclaw/workspace/projects/caipiao/data/caipiao.db）
- 历史期数：3430+ 期
- 数据更新：每周二、四、日开奖后自动更新

## 版本历史

### V2.15（当前版本）
- ✅ 均值回归权重提升
- ✅ 正态分布权重提升
- ✅ 大数定律权重提升
- ✅ 卡方检验权重提升
- ✅ 自动防错机制

### V2.7
- 7 种数学模型整合

### V2.5
- 初始版本

## 相关文件

- 预测脚本：`scripts/v2.15_prediction.py`
- 验证脚本：`scripts/verify_prediction.py`
- 回测脚本：`scripts/backtest.py`
- 完整文档：`references/v2.15_documentation.md`

## 支持

- 问题反馈：~/.openclaw/workspace/skills/lottery-predictor-v2.15/issues.md
- 更新日志：~/.openclaw/workspace/skills/lottery-predictor-v2.15/CHANGELOG.md
