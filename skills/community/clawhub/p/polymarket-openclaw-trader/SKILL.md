---
name: polymarket-openclaw-trader
description: Reusable Polymarket + OpenClaw trading operations skill for any workspace. Use when the user needs to set up, run, tune, monitor, and deploy an automated Polymarket trading project (paper/live), including env configuration, risk controls, reporting, and dashboard operations.
---

# Polymarket + OpenClaw 自动化交易（可发布通用版）

## 0) 前置条件（先检查）

- Python 3.10+
- 可用的 Polymarket 项目目录（包含 `cli_bot.py` / `web_app.py`）
- 具备合法可交易区域（否则会触发 geoblock）
- 仅在用户明确授权时写入私钥

先确认项目路径（不要写死绝对路径）：

```bash
pwd
ls -la
```

如果用户没有给路径，询问并约定：`<PROJECT_DIR>`。

后续命令都基于：

```bash
cd <PROJECT_DIR>
```

---

## 1) 初始化配置（敏感信息只进 .env）

必须项：

- `POLYMARKET_PRIVATE_KEY`
- `POLYMARKET_WALLET_ADDRESS`
- `EXECUTION_MODE=paper|live`
- `AUTO_TRADE=true|false`
- `LIVE_MAX_ORDERS_PER_DAY=<int>`

可选：

- `POLYMARKET_FUNDER`
- `DISCORD_WEBHOOK_URL`
- `POLYMARKET_HOST`
- `POLYMARKET_CHAIN_ID`
- `POLYMARKET_SIGNATURE_TYPE`

要求：

- 禁止把私钥写进代码或日志
- 对外回复时私钥只可显示“已配置/未配置”，不可回显原文

---

## 2) 启停与巡检

启动：

```bash
nohup env PYTHONUNBUFFERED=1 python3 cli_bot.py loop > logs/runner_v2.log 2>&1 < /dev/null &
```

巡检：

```bash
ps -ef | grep 'python3 cli_bot.py loop' | grep -v grep
tail -n 120 logs/runner_v2.log
```

若进程不在：自动重启并再次验证。

---

## 3) 策略参数（非敏感，建议面板/运行时可调）

优先写入 `runtime/settings.json`：

- `price_move_threshold_pct`
- `volume_spike_multiple`
- `signal_score_threshold`
- `poll_interval_sec`
- `status_every_minutes`

修改后重启策略进程。

---

## 4) 汇报口径（必须真实）

汇报优先使用真实来源：

- 真实持仓、持仓价值、浮动盈亏（钱包查询）
- 机器人账本字段（如 `dailyPnlUsd/openMarkets`）要明确标注为“机器人账本”

禁止将估算余额伪装成真实账户余额。

---

## 5) 下单执行规范

执行前依次检查：

1. 私钥已配置
2. 市场与 token id 可解析
3. 风控阈值通过
4. 执行下单
5. 返回完整结果（成功回执或失败原因）

若返回 geoblock / region restriction：

- 立即停止交易尝试
- 明确告知合规限制
- 不提供绕过区域限制的方法

---

## 6) Web 控制台与部署

本地：

```bash
python3 web_app.py
```

Vercel：

```bash
vercel --prod --yes
```

若 Flask 入口报错，检查是否存在 `app.py` 且内容为：

```python
from web_app import app
```

---

## 7) 持久化与交付

每次关键变更后：

1. 更新项目记忆文件（若工作区有 MEMORY 体系）
2. `git add/commit` 提交
3. 若用户要求，打包 skill：

```bash
python3 <skill_creator_scripts>/package_skill.py <skill_dir> <out_dir>
```

---

## 8) 给最终用户的最小启动指令模板

```bash
cd <PROJECT_DIR>
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# 填写必要环境变量后
nohup env PYTHONUNBUFFERED=1 python3 cli_bot.py loop > logs/runner_v2.log 2>&1 < /dev/null &
```
