# 受控自进化协议

## 原则

HuahuaDaily 的信号快照、T1/T7/T20/T60 复盘、真实交易复盘、组合回放和服务端回测用于积累证据，不用于在线偷偷调参。ACTIVE 策略是 champion；任何改进先成为 challenger。

```text
champion 信号与真实结果
        ↓
分层归因：信号 / 组合 / 用户目标
        ↓
AI 提出一个可证伪的改进假设
        ↓
时点回放 → walk-forward → 成本与故障压力测试
        ↓
SHADOW 对照
        ↓
用户确认晋升 / 继续观察 / 淘汰 / 回滚
```

## 三本不可变账本

1. **用户政策账本**：目标、风险、资产限制和确认历史；策略不能修改。
2. **策略版本账本**：父版本、唯一变更假设、参数、实验次数、样本区间、结果和状态。
3. **证据账本**：信号快照、后续表现、实际交易、组合回放、数据截止和方法版本。

## 分层复盘

- **信号层**：方向、超额收益、最大不利变动、覆盖率和不同期限校准。
- **组合层**：收益、回撤、波动、换手、费用、现金占用和风险契约违约。
- **用户目标层**：目标缺口、到期流动性、可承受损失和无效交易是否减少。

把“用户没有执行”和“策略建议错误”分开记录。减仓后继续上涨不自动等于错误；若按政策显著降低尾部风险，可能完成了风险目标。

## 允许学习

- AI 在不同市场、袖套和期限的校准表现；
- 哪类证据和反证真正提高判断质量；
- 重复出现的事实错误、叙事偏见和信息遗漏；
- 再平衡带、低频趋势和波动上限的样本外稳定性；
- `fund_trend_consensus_v1` 的覆盖率、共识阈值、软触发线与分阶段减仓步长的样本外稳定性；
- 基金筛选门槛、事件否决和执行摩擦；
- 报告频率是否减少冲动交易。

## 禁止自动学习

- 因短期盈利提高用户风险；
- 因一次亏损改变长期配置；
- 用用户成本训练市场方向；
- 把新闻、诊断正文或产业链叙事直接拟合为金额；
- 根据单一案例新增规则；
- 在同一历史反复搜索后只报告最佳参数；
- 在线修改 ACTIVE 参数、政策或 AI 输出校验合同。
- 因一次止损成功或失败直接修改因子数量、动态换手档位或风险减仓豁免。

## challenger 晋升

必须满足：

1. 只有一个清晰假设或可完成严格消融；
2. 使用当时可见数据，记录全部实验次数；
3. 通过多个起点的 walk-forward；
4. 在费用、确认延迟、缺失数据和不可交易压力下仍稳定；
5. 相对简单基准和 champion 的改善不只来自单一行情；
6. 不增加风险契约违约；
7. 影子模式达到预注册样本量；
8. 用户明确确认后晋升；
9. 可一键回滚。

单个用户数据不足以训练复杂 alpha。用户级学习主要用于目标、现金流、执行摩擦和交互；资产信号依靠更长市场历史和严格样本外研究。

## 策略注册表

使用 `scripts/strategy_registry.py` 保存每个 Huahua 用户隔离的 champion–challenger 状态。它只登记实验和晋升门槛，不运行回测、不给参数自动调优，也不能修改用户政策。

```bash
python3 scripts/strategy_registry.py status --user-id '<uid>'
python3 scripts/strategy_registry.py bootstrap --user-id '<uid>' --version '4.3.0'
python3 scripts/strategy_registry.py register --user-id '<uid>' --input challenger.json
python3 scripts/strategy_registry.py evaluate --user-id '<uid>' --id 'candidate-id' --input evaluation.json
python3 scripts/strategy_registry.py promote --user-id '<uid>' --id 'candidate-id' --user-confirmed
python3 scripts/strategy_registry.py reject --user-id '<uid>' --id 'candidate-id' --reason '样本外不稳定'
python3 scripts/strategy_registry.py rollback --user-id '<uid>' --version '4.3.0' --user-confirmed
```

`promote` 只有在时点数据、walk-forward、全部试验披露、成本与缺失数据压力、硬风险指标、影子样本量和主要指标全部通过，且用户明确确认时才成功。注册表与政策使用同一外部状态根目录，但分别追加事件账本；都不能写进可分发 skill 包。
