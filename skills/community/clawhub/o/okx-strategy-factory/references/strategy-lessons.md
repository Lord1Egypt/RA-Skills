# 策略经验库

从已有策略的开发、回测、实盘中提炼的可复用经验。新策略开发时 **必须** 先读本文件。

---

## 一、通用风控模式

所有策略已验证有效的风控层级（按优先级从高到低）：

| 层级 | 机制 | 推荐值 | 来源 |
|------|------|--------|------|
| 1 | 全局 Stop 开关 | — | grid-trading, cl-lp |
| 2 | 熔断器（连续错误→冷却） | 5 错误 → 1h 冷却 | grid-trading, cl-lp |
| 3 | 数据验证（价格/余额/API 返回） | 每次操作前 | 通用 |
| 4 | 止损 / 追踪止损 | 15% / 10% | grid-trading, cl-lp |
| 5 | 仓位限制 | 按策略类型定义上限 | grid-trading |
| 6 | 最小操作间隔 | 30min (交易) / 2h (调仓) | grid-trading, cl-lp |
| 7 | 重复操作保护 | 同向最多 3 次后暂停 | grid-trading |
| 8 | Gas 成本检查 | Gas < 预期收益的 50% | cl-lp |
| 9 | 最小变化阈值 | > 3% (网格) / > 5% (范围) | grid-trading, cl-lp |

**原则**: 新策略不必照搬全部层级，但至少包含 1-4 层（Stop、熔断、数据验证、止损）。5-9 层根据策略类型选取。

---

## 二、多时间框架趋势分析 (MTF)

Grid Trading 首创，CL LP Rebalancer 已成功复用。**推荐所有需要趋势判断的策略复用此模块。**

```
短期 EMA: 5 bars (25min @ 5min K线)  → 快速信号
中期 EMA: 12 bars (1h)               → 方向确认
长期 EMA: 48 bars (4h)               → 趋势过滤
8h 结构检测: 上升/下降/震荡           → 宏观背景
```

**输出**:
- `trend_direction`: bullish / bearish / neutral
- `trend_strength`: 0-1（> 0.3 时激活非对称逻辑）

**复用方式**: 独立函数，输入 K 线数组，输出趋势方向 + 强度。不依赖具体策略逻辑。

---

## 三、波动率自适应

两个策略都使用 K线 ATR + 价格标准差融合的波动率估计，效果优于单一指标。

**ATR 计算**: 24 根 1H K 线 → 24h 波动率窗口

**波动率分级**（CL LP 已验证）:

| 级别 | ATR 范围 | 策略行为 |
|------|----------|----------|
| Low | < 1.5% | 收紧参数，追求资本效率 |
| Medium | 1.5-3% | 平衡配置 |
| High | 3-5% | 放宽参数，减少操作频率 |
| Extreme | > 5% | 防御模式，安全优先 |

**教训**: Grid Trading 的波动率乘数 (VOLATILITY_MULTIPLIER) 在不同趋势下需要差异化——看涨时放宽 (3.0x)，看跌时收紧 (1.0x)。

---

## 四、非对称设计

两个策略都证明了**趋势方向应驱动买卖不对称**：

- **Grid Trading**: 看涨时买网格密、卖网格疏（快买慢卖）；看跌反之
- **CL LP**: 看涨时上方范围宽、下方窄；看跌反之

**激活条件**: `trend_strength > 0.3` 时启用，否则保持对称。

**非对称系数**: Grid 用 0.4，CL LP 用 0.3。新策略建议从 0.3 起步，根据回测调整。

---

## 五、成本管理经验

### Slippage（最大痛点）

Grid Trading 回测暴露了 **6.24% 的 slippage**，直接抵消了交易利润。

**教训**:
- 单笔交易金额越大，slippage 越高 → 控制单笔大小
- DEX swap 天然存在 slippage，无法消除只能管理
- `slippage_tolerance_pct` 设为 1-1.5%，超出时放弃交易

### Gas

CL LP 在 Base 链上 Gas 极低（$0.048/天），但其他链差异巨大。

**教训**:
- 始终检查 `gas_cost < expected_profit * gas_to_fee_ratio`
- Base/Arbitrum/Polygon 的 Gas 成本可忽略，Ethereum L1 需要特别注意
- 调仓/交易前先估算 Gas，不满足则跳过

---

## 六、状态管理模式

两个策略都使用 JSON 文件管理状态，已验证可靠：

```python
state = {
    "positions": [],           # 当前持仓
    "price_history": [],       # 288 根 5min K线 = 24h
    "error_count": 0,          # 熔断计数
    "last_action_time": "",    # 操作间隔控制
    "equity_curve": [],        # 资金曲线
    "trade_log": []            # 交易记录（配对分析用）
}
```

**教训**:
- 状态文件必须原子写入（先写 tmp 再 rename），防止中断导致损坏
- 价格历史保留 24h 足够（288 根 5min），更长周期用 API 按需拉取
- 交易记录要保留完整的 round trip（买卖配对），便于 Iteration Agent 分析

---

## 七、回测指标基线

| 指标 | Grid Trading v4 | CL LP v1 | 建议门槛 |
|------|-----------------|----------|----------|
| Sharpe Ratio | — | 29.67 | > 1.0 |
| Max Drawdown | — | 2.72% | < 声明值 |
| Win Rate | — | 85.7% | > 40% |
| Profit Factor | — | 7.5 | > 1.5 |
| Gas/Revenue | 高 | 0.22% | < 50% |
| Slippage 实际 | 6.24% | 0.35% | < 声明值 |
| 在范围时间 (LP) | N/A | 99.3% | > 90% |

**注意**: CL LP 的指标异常优秀，部分因为回测期间市场条件理想（中等波动 + 温和趋势）。新策略不应以此为基准，而应以 Gate 最低要求（Sharpe>1.0, WR>40%）为目标。

---

## 八、适用市场条件

两个策略的共同发现：

| 市场状态 | 表现 | 应对 |
|----------|------|------|
| 震荡 / 低波动 | ✅ 最佳 | 正常运行 |
| 中等波动 + 温和趋势 | ✅ 良好 | 非对称模式激活 |
| 高波动 | ⚠️ 可接受 | 放宽参数，降低频率 |
| 极端波动 / 闪崩 | ❌ 风险高 | 建议暂停或进入防御模式 |
| 持续单边行情 | ❌ 不适合 | 网格策略天然逆势，LP 面临 IL |

**建议**: 新策略的 `risk-profile.json` 中 `market_conditions.not_applicable` 必须明确列出不适用场景。

---

## 九、执行架构模式

### onchainos CLI — 运行时依赖

所有策略的链上操作通过 `onchainos` 二进制执行。本地 `Agentic Wallet/onchainos` (arm64)，VPS `/usr/local/bin/onchainos` (amd64)。onchainos 更新频繁，独立测试。

onchainos 的能力已作为 Claude Code Skill 安装（`okx-dex-swap`、`okx-agentic-wallet` 等），策略开发时按 skill 名称调用，接口细节以 skill 文档为准。

**与 onchainos 协作的经验教训**:
- `wallet send` 用 UI 单位（"0.1" ETH），`swap` 系列用最小单位（wei）—— 混用必出错
- EVM swap 需要先 `approve` 再 `swap`，Solana 不需要
- `gateway simulate` 可在不上链的情况下预检交易，建议大额操作前必做
- `security token-scan` 可检测蜜罐，新策略接入未知 Token 前应先扫描
- onchainos 更新后，策略的 CLI 调用方式可能变化，部署前需验证兼容性

### 通用执行架构

```
Cron (5min) → Python 脚本 → onchainos CLI → OKX Web3 API → Chain
                  ↓                              ↓
            state.json (本地)              Wallet (TEE signing)
                  ↓
          Discord 通知 (via OpenClaw)
```

**标准 CLI 入口**（所有策略应统一）：

```bash
python3 {strategy}.py tick      # 主循环（cron 调度）
python3 {strategy}.py status    # 当前状态
python3 {strategy}.py report    # 日报
python3 {strategy}.py close     # 完全退出（仅部分策略需要）
```

---

## 十、常见陷阱

| 陷阱 | 策略 | 后果 | 预防 |
|------|------|------|------|
| 硬编码 Token 地址 | 通用 | 换链时全部失效 | config.json 外置 |
| 不校验 API 返回 | 通用 | 空数据导致异常交易 | 数据验证层 |
| 止损和追踪止损冲突 | Grid | 两者同时触发导致重复平仓 | 互斥检查 |
| 调仓过于频繁 | CL LP | Gas + slippage 吃掉收益 | anti-churn 保护 |
| 价格历史不足就计算 ATR | 通用 | 波动率估计偏差大 | 最少 24 根 K 线才启用 |
| 忽略 decimal 差异 | 通用 | ETH(18) vs USDC(6) 计算错误 | 统一转换层 |
| 混用 UI 和最小单位 | 通用 | onchainos 不同命令单位不同，混用导致金额错误 | 查阅 cli-reference 确认每个命令的单位 |
| 回测用理想 slippage | Grid | 实盘 slippage 远高于预期 | 回测加入随机 slippage 模型 |
| onchainos 版本不兼容 | 通用 | 更新后 CLI 参数变化导致策略报错 | 部署前验证 onchainos 版本兼容性 |

---

## 更新记录

- 2026-03-20: 初始版本，从 grid-trading v4 和 cl-lp-rebalancer v1 提取
