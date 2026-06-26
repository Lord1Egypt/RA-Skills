# MNS 策略参数参考

本文档详细说明 MNS 逆向投资策略的核心参数，包括阈值定义、买入/卖出比例配置、止盈线设置等。这些参数通过 `mns config` 命令动态调整。

---

## 配置层级

MNS 配置采用分层结构，存储于 `~/.mns/config.toml`：

```toml
[settings]
annualized_target_low = 10.0      # 年化止盈线下限(%)
annualized_target_high = 15.0     # 年化止盈线上限(%)
min_holding_days = 45             # 年化收益计算最小天数
min_absolute_profit_days = 120    # 绝对收益止盈最小天数
max_contrarian_weight = 2.0      # 逆向权重上限
report_output_dir = "./reports"   # 报告输出目录

[allocation]
us_stocks = 55.0          # 美股目标配置比例(%)
cn_stocks = 25.0          # A股目标配置比例(%)
counter_cyclical = 20.0   # 逆周期资产配置比例(%)

[thresholds]
extreme_fear = 30.0       # 极度恐慌阈值
fear = 45.0               # 恐慌阈值
neutral = 55.0            # 中性阈值
greed = 70.0              # 贪婪阈值

[buy_ratio]
extreme_fear = 60.0       # 极度恐慌买入比例(%)
fear = 35.0               # 恐慌买入比例(%)
neutral = 0.0             # 中性买入比例(%)
greed = 0.0               # 贪婪买入比例(%)

[sell_ratio]
extreme_greed_target_high = 50.0    # 极度贪婪+高年化卖出(%)
extreme_greed_target_low = 30.0     # 极度贪婪+低年化卖出(%)
extreme_greed_below_target = 20.0  # 极度贪婪+未达标卖出(%)
greed_target_high = 40.0            # 贪婪+高年化卖出(%)
greed_target_low = 25.0             # 贪婪+低年化卖出(%)
neutral_target_high = 15.0          # 中性+高年化卖出(%)

[api]
fear_greed_url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
```

---

## 恐贪指数区间划分

CNN Fear & Greed Index 是一个 0-100 的指数，0 表示极度恐慌（Extreme Fear），100 表示极度贪婪（Extreme Greed）。

### 默认区间配置

| 区间名称 | 指数范围 | 含义 | 买入比例 |
|---------|---------|------|---------|
| Extreme Fear | 0-30 | 市场极度恐慌，逆向买入信号强 | 60% |
| Fear | 30-45 | 市场恐慌，适度买入 | 35% |
| Neutral | 45-55 | 中性，观望不买入 | 0% |
| Greed | 55-70 | 市场贪婪，谨慎持有 | 0% |
| Extreme Greed | 70-100 | 市场极度贪婪，考虑减仓 | 0% |

### 调整阈值

通过修改 `thresholds` 可改变区间边界：

```bash
# 将贪婪阈值从 70 降至 65，使贪婪区间更早触发
mns config thresholds.greed 65.0

# 将极度恐慌阈值从 30 提升至 35，减少极端情况下的买入频率
mns config thresholds.extreme_fear 35.0
```

**注意**: 区间必须保持连续性，建议:
- `extreme_fear < fear < neutral < greed`
- 阈值单位为百分比数值（如 25.0 表示 25）

---

## 买入比例矩阵 (`buy_ratio`)

定义在不同情绪区间下，用多少比例的可用现金进行买入。

### 参数说明

- **可用现金**: `cash_balance + 卖出回笼资金`（买卖互感知）
- **分配方式**: 按 contrarian 权重分配到各资产类别
- **类别配置**: 按 `allocation` 比例分配到美股/A股/逆周期

### 默认配置

| 情绪区间 | 买入比例 | 适用场景 |
|---------|---------|---------|
| extreme_fear | 60.0% | 恐慌极致，重仓抄底 |
| fear | 35.0% | 恐慌情绪，积极建仓 |
| neutral | 0.0% | 中性市场，观望不买入 |
| greed | 0.0% | 贪婪时暂停买入 |

### 调优示例

```bash
# 策略1: 极度贪婪时也可能小幅买入（左侧布局）
mns config buy_ratio.greed 10.0

# 策略2: 中性区间也暂停买入，只在明确的恐慌区间出手
mns config buy_ratio.neutral 0.0

# 策略3: 极端恐慌时加大买入
mns config buy_ratio.extreme_fear 70.0
```

---

## 卖出比例矩阵 (`sell_ratio`)

定义在特定情绪区间和年化收益档位下的卖出比例。卖出逻辑基于 **双准则**:

1. **年化收益止盈**: 当持仓年化收益率达标且处于可卖出情绪区间
2. **绝对收益止盈**: 当持仓绝对收益 ≥ 30% 且持有天数足够长

### 收益档位定义

- `target_high`: 年化收益 ≥ `annualized_target_high`（默认 15%）
- `target_low`: 年化收益 ≥ `annualized_target_low`（默认 10%）但 < target_high
- `below_target`: 年化收益 < target_low（仅在极度贪婪时考虑部分卖出）

### 默认卖出矩阵

| 情绪区间 | target_high | target_low | below_target |
|---------|-------------|------------|--------------|
| extreme_greed | 50% | 30% | 20% |
| greed | 40% | 25% | 0% |
| neutral | 15% | 0% | 0% |
| fear/extreme_fear | 0% | 0% | 0% |

### 配置路径

```bash
# 查看卖出配置
mns config sell_ratio

# 调整极度贪婪时的高收益卖出比例
mns config sell_ratio.extreme_greed_target_high 70.0

# 调整贪婪时的中等收益卖出比例
mns config sell_ratio.greed_target_low 30.0

# 启用中性区间的部分止盈
mns config sell_ratio.neutral_target_high 20.0
```

---

## 止盈线参数 (`settings`)

### `annualized_target_low` (默认 10.0)

年化收益率的下限阈值。当持仓年化收益 ≥ 此值且处于可卖出情绪区间时，触发部分卖出建议。

### `annualized_target_high` (默认 15.0)

年化收益率的上限阈值。当持仓年化收益 ≥ 此值时，卖出比例达到该情绪区间的最大值。

**调优示例**:

```bash
# 保守止盈：年化 8% 就开始卖
mns config settings.annualized_target_low 8.0
mns config settings.annualized_target_high 12.0

# 激进止盈：年化 20% 才开始卖
mns config settings.annualized_target_low 15.0
mns config settings.annualized_target_high 25.0
```

### `min_holding_days` (默认 45)

最小持有天数。持仓天数小于此值时，不计算年化收益率（显示为 N/A），避免短期波动误导。

### `min_absolute_profit_days` (默认 120)

绝对收益止盈的最小天数。只有持仓天数 ≥ 此值且绝对收益 ≥ 30% 时，才触发绝对收益止盈。

**目的**: 避免短期投机操作，确保长期持有才能享受"坐过山车保护"。

---

## 逆向权重参数 (`settings`)

### `max_contrarian_weight` (默认 2.0)

逆向权重的上限。防止浮亏过大的标的获得过多资金，导致过度集中风险。

**权重公式**:
```
weight = min(max_contrarian_weight, max(1.0, cost_price / current_price))
```

**调优示例**:

```bash
# 降低权重上限，避免过度集中
mns config settings.max_contrarian_weight 1.5

# 提高权重上限，更激进抄底
mns config settings.max_contrarian_weight 3.0
```

---

## 资产配置参数 (`allocation`)

定义买入资金在不同资产类别间的目标分配比例。

### 默认配置

| 类别 | 比例 | 说明 |
|------|------|------|
| us_stocks | 55% | 美股（如 QQQ, SPY） |
| cn_stocks | 25% | A股（如沪深300成分股） |
| counter_cyclical | 20% | 逆周期资产（如黄金ETF, 债券） |

### 注意事项

- 配置比例之和必须为 100%
- 这是**目标参考比例**，非强制约束
- 实际分配还会受 contrarian 权重影响

### 调整示例

```bash
# 查看当前配置
mns config allocation

# 调整美股占比
mns config allocation.us_stocks 60.0
mns config allocation.cn_stocks 30.0
mns config allocation.counter_cyclical 10.0
```

---

## 买入资金分配: Contrarian 权重详解

MNS 的买入资金不是平均分配，而是采用 **逆向权重**：

```
weight_i = min(max_contrarian_weight, max(1.0, cost_price_i / current_price_i))
```

### 权重计算示例

假设 Fear 区间可用买入资金 30,000 元，有两个美股持仓：

| 资产 | 成本价 | 当前价 | 浮亏/浮盈 | 权重计算 | 权重 |
|------|--------|--------|----------|---------|------|
| QQQ  | 450.00 | 460.50 | +2.3%    | min(2.0, max(1.0, 450/460.5)) = 1.0 | 1.0 |
| AAPL | 180.00 | 150.00 | -16.7%   | min(2.0, max(1.0, 180/150)) = 1.2 | 1.2 |

**分配结果**:
- QQQ: `30000 × (1.0 / 2.2) = 13,636 元`
- AAPL: `30000 × (1.2 / 2.2) = 16,364 元`

浮亏资产获得更高权重，符合"越跌越买"的逆向逻辑，但权重上限防止过度集中。

### 高浮亏排除机制

当持仓浮亏 ≥ 30% 时，该标的会被**排除加仓列表**，避免"越亏越买"的基本面恶化风险。

---

## 卖出决策双准则详解

### 准则1：年化收益 + 情绪区间

当同时满足以下条件时触发：
1. 当前情绪在可卖出区间（neutral 及以上）
2. 持仓年化收益 ≥ `annualized_target_low`
3. 持仓天数 ≥ `min_holding_days`

卖出比例根据年化收益档位和情绪区间从 `sell_ratio` 矩阵查出。

### 准则2：绝对收益止盈

当满足以下条件时触发：
- 绝对收益 = (当前价 - 成本价) / 成本价 ≥ 30%
- 持仓天数 ≥ `min_absolute_profit_days`（默认 120 天）

**目的**: 锁定长期盈利，即使年化收益率因持有时间较长而降低。

---

## 风险警告机制

当持仓浮亏 ≥ 20% 时触发风险警告，建议根据市场情绪差异化处理：

| 情绪环境 | 建议操作 |
|---------|---------|
| Extreme Fear/Fear | 可能是加仓机会 |
| Neutral | 审视基本面 |
| Greed/Extreme Greed | 紧急审视（别人赚钱你还在亏） |

---

## 完整参数调优工作流

### 1. 查看当前配置

```bash
mns config

# 查看特定分组
mns config buy_ratio
mns config sell_ratio
mns config settings
```

### 2. 运行回测验证

```bash
# 查看可调参数
mns backtest params

# 运行默认配置回测
mns backtest run

# 测试新参数组合
mns backtest run --config my_strategy.toml
```

### 3. 调整参数

```bash
# 每次只调整 1-2 个参数
mns config buy_ratio.extreme_fear 60.0

# 观察 report 变化
mns report
```

### 4. 备份配置

```bash
mns config > config_backup_$(date +%Y%m%d).toml
```

---

## 配置路径速查表

| 配置路径 | 说明 | 默认值 |
|---------|------|--------|
| `settings.annualized_target_low` | 年化止盈下限(%) | 10.0 |
| `settings.annualized_target_high` | 年化止盈上限(%) | 15.0 |
| `settings.min_holding_days` | 年化收益最小天数 | 45 |
| `settings.min_absolute_profit_days` | 绝对收益最小天数 | 120 |
| `settings.max_contrarian_weight` | 逆向权重上限 | 2.0 |
| `settings.report_output_dir` | 报告输出目录 | ./reports |
| `allocation.us_stocks` | 美股目标比例(%) | 55.0 |
| `allocation.cn_stocks` | A股目标比例(%) | 25.0 |
| `allocation.counter_cyclical` | 逆周期比例(%) | 20.0 |
| `thresholds.extreme_fear` | 极度恐慌阈值 | 30.0 |
| `thresholds.fear` | 恐慌阈值 | 45.0 |
| `thresholds.neutral` | 中性阈值 | 55.0 |
| `thresholds.greed` | 贪婪阈值 | 70.0 |
| `buy_ratio.extreme_fear` | 极度恐慌买入(%) | 60.0 |
| `buy_ratio.fear` | 恐慌买入(%) | 35.0 |
| `buy_ratio.neutral` | 中性买入(%) | 0.0 |
| `buy_ratio.greed` | 贪婪买入(%) | 0.0 |
| `sell_ratio.extreme_greed_target_high` | 极度贪婪高收益卖(%) | 50.0 |
| `sell_ratio.extreme_greed_target_low` | 极度贪婪低收益卖(%) | 30.0 |
| `sell_ratio.extreme_greed_below_target` | 极度贪婪未达标卖(%) | 20.0 |
| `sell_ratio.greed_target_high` | 贪婪高收益卖(%) | 40.0 |
| `sell_ratio.greed_target_low` | 贪婪低收益卖(%) | 25.0 |
| `sell_ratio.neutral_target_high` | 中性高收益卖(%) | 15.0 |

---

## 风险提示

- **参数调优需结合实际市场环境**: 回测结果是历史数据，不代表未来表现
- **避免频繁调整**: 每次调整后至少观察 1-2 个月的实盘表现
- **分散投资**: `max_contrarian_weight` 可防止单一标的过度集中

---

**文档版本**: v0.5.8 | **更新日期**: 2026-04-21
