[English](README.md) | 中文

# Life Query — 日常生活查询助手

一个 Claude Code Skill，用自然语言查询日常生活信息：快递物流、汇率换算、油价、天气预报。

## 当前能力

- **快递查询** — 输入单号查物流轨迹，支持顺丰、圆通、中通、韵达、京东等主流快递。可使用免费额度或自带快递100凭证直连
- **汇率换算** — 实时和历史汇率查询，支持 30 种货币（CNY/USD/EUR/JPY/GBP/HKD/KRW...）。数据来自欧洲央行 ECB，无需 API Key
- **油价查询** — 全国 31 省市最新 92/95/柴油价格及历史调价记录。数据来自东方财富/国家发改委
- **天气预报** — 全球城市当前天气、多日预报、逐小时详情。数据来自 wttr.in

## 快速开始

```bash
# 查快递
bash scripts/run.sh call courier-track --trackingNumber SF1234567890

# 100 人民币换算成美元、欧元、日元
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --amount 100

# 全国油价（表格格式）
bash scripts/run.sh call oil-price --format table

# 上海 3 天天气预报
bash scripts/run.sh call weather --city Shanghai --days 3 --format table

# 列出所有接口
bash scripts/run.sh list
```

## 安装

```bash
npx clawhub@latest install life-query
```

## 更新日志

- 2026-03-21: refactor — 合并 `apis/` 到 `scripts/`，优化 SKILL.md 结构
- 2026-03-17: feat — 新增天气预报（wttr.in）
- 2026-03-17: feat — 新增汇率查询和油价查询
- 2026-03-17: fix — 移除 API Key 验证，快递查询恢复正常
- 2026-03-14: init — 初始版本，支持快递查询
