---
name: openclaw-funding-arb
description: 运行和维护 MEXC 股票合约资金费套利机器人，包含毫秒级触发、资金费率阈值过滤、股票白名单过滤、美股常规时段停盘窗口控制、以及未平仓状态持久化恢复。用户提出启动、调参、排障或改造该套利流程时使用本技能。
---

# OpenClaw Funding Arb

使用本技能来运行和修改内置的 MEXC 资金费套利脚本。

## 快速开始

1. 以 `scripts/funding_arb_mexc.py` 作为主脚本来源。
2. 如果用户需要项目内版本，把脚本复制到目标工作目录。
3. 设置必要环境变量后，用 Python 运行脚本。

```powershell
$env:MEXC_API_KEY='your_key'
$env:MEXC_API_SECRET='your_secret'
$env:PYTHONDONTWRITEBYTECODE='1'
python funding_arb_mexc.py
```

## Ubuntu 适配
- 运行环境建议 Python `3.10+`（需要 `zoneinfo`）。
- 在 Ubuntu 上使用 `python3` 和 `export` 方式启动：

```bash
export MEXC_API_KEY='your_key'
export MEXC_API_SECRET='your_secret'
export PYTHONDONTWRITEBYTECODE=1
python3 ~/.codex/skills/openclaw-funding-arb/scripts/funding_arb_mexc.py
```

- 如需自定义状态文件路径，可额外设置：

```bash
export STATE_FILE='/path/to/funding_arb_state.json'
```

## 必要输入

- 设置 `MEXC_API_KEY`。
- 设置 `MEXC_API_SECRET`。

## 核心运行逻辑

- 仅在美股常规交易时段关闭时运行。
- 扫描股票合约并应用白名单过滤。
- 资金费结算前开仓，结算后立刻平仓。
- 按资金费率正负决定方向：正费率开空，负费率开多。
- 仅当绝对资金费率超过阈值时才开仓。
- 持久化未平仓状态，支持重启恢复。

## 关键参数

- `MIN_ABS_FUNDING_RATE`：最小绝对资金费率阈值，默认 `0.0012`（0.12%）。
- `OPEN_LEAD_SEC`：结算前开仓提前秒数。
- `CLOSE_LAG_SEC`：结算后平仓滞后秒数。
- `PRICE_PREFETCH_LEAD_MS`：触发前预取价格提前毫秒数。
- `TIME_OFFSET_MS`：交易所时钟偏移（毫秒）。
- `MAX_PARALLEL_ORDERS`：同一批次并发下单数量上限。
- `STOCK_SYMBOLS`：股票合约白名单（逗号分隔，可覆盖默认值）。
- `STATE_FILE`：未平仓状态持久化文件路径。

## 修改流程

1. 保持 `funding_arb_mexc.py` 逻辑简洁、可预测。
2. 保证两个不变量：
   - 开仓校验不能在结算时间之后发单。
   - 平仓动作必须由已持久化的 opened 状态驱动，不能依赖最新 funding 周期 key。
3. 修改后执行语法检查。

```powershell
python -c "import ast, pathlib; p=pathlib.Path('funding_arb_mexc.py'); ast.parse(p.read_text(encoding='utf-8-sig')); print('AST_OK')"
```

## 故障处理

- 出现 `MISS_OPEN` 代表时序错过，优先调 `PRICE_PREFETCH_LEAD_MS` 和 `TIME_OFFSET_MS`。
- 连续 `OPEN_FAIL` 或 `CLOSE_FAIL` 通常是网络或限频问题，降低并发或适当放宽开/平窗口。
- 如果重启时有未平仓，先从 `STATE_FILE` 恢复并优先完成平仓。
