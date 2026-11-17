---
name: lottery-cn-research
description: |
  中国福利彩票与体育彩票的研究工具 skill。当用户研究双色球、大乐透、3D、排列3/5、
  七乐彩、快乐8、七星彩等彩种, 需要以下任一类能力时使用: 玩法规则与奖金速查、历史开奖
  数据抓取与统计分析(冷热号/遗漏/奇偶/和值/连号/重号)、按策略生成选号方案(机选/热号/
  冷号/均衡 + 过滤缩水)、或计算中彩票概率与期望收益(EV)。触发词示例: "双色球概率"、
  "大乐透历史数据分析"、"帮我机选几注"、"彩票返奖率"、"遗漏值怎么看"、"快乐8怎么算"。
agent_created: true
---

# 中国彩票研究助手（lottery-cn-research）

> 中文名称：中国彩票研究助手 ｜ 机器标识（name）：`lottery-cn-research`
> 说明：skill 的内部 `name` 字段按规定须为小写连字符 ASCII（不可为中文），此处中文名为展示名。

## Overview

本 skill 提供对中国福利彩票与体育彩票主流数字型彩种(双色球、大乐透、3D、排列3/5、
七乐彩、快乐8、七星彩)的 four 类研究能力: 规则速查、历史数据统计分析、选号方案生成、
中奖概率与期望收益计算。所有脚本仅依赖 Python 标准库, 可离线运行(自带样例数据)。

**核心立场**: 彩票每期独立随机, 任何统计、策略、缩水都**不改变中奖概率**, 期望收益长期恒为负。
本 skill 仅供研究、学习概率统计与娱乐参考, 严禁作为"稳赚"或投资建议。

## When to use

- 用户询问某彩种"怎么玩 / 规则 / 奖金多少 / 几开奖"。
- 用户想看历史开奖的冷热号、遗漏、奇偶、和值等统计。
- 用户要"机选几注 / 热号选号 / 缩水过滤"。
- 用户问"中奖概率多少 / 返奖率 / 期望收益 / 值不值得买"。
- 用户需要把开奖数据整理成可分析的格式。

## Core capabilities (workflow)

### 0. 准备数据(可选)
若用户已有开奖数据, 直接整理成归一化 JSON(见 `references/data_sources.md`); 否则用抓取脚本:
```bash
python scripts/fetch_history.py --game ssq --count 100 --out ssq_history.json
# 或导入本地文件
python scripts/fetch_history.py --local existing.json --out ssq_history.json
```
- 在线源(opencai 等)可能变动或被网络限制; 失败时按提示改用 `--local`。
- 自带 `assets/sample_ssq.json`(30 期)可直接试用分析/生成脚本。

### 1. 规则速查
直接查阅 `references/games.md` 回答玩法、开奖时间、奖级与奖金; 复杂概念见
`references/analysis_methods.md`(冷热、遗漏、和值、缩水原理)。

### 2. 概率与期望(无需历史数据)
```bash
python scripts/probability.py --game ssq                 # 双色球
python scripts/probability.py --game dlt --jackpot 10000000
python scripts/probability.py --all                       # 全部彩种概要
```
- 双色球/大乐透用超几何分布精确计算各奖级概率; 3D/排列等按组合计算。
- 浮动奖用估算奖池(`--jackpot`, 各彩种有合理默认值); 不同投注方式(直选/组选等)分别列返奖率。

### 3. 历史数据统计分析
```bash
python scripts/analyze.py --data ssq_history.json --window 30
python scripts/analyze.py --data ssq_history.json --json stats.json
```
输出每号码池的频率、冷热号、当前/历史最大遗漏、奇偶比、大小比、和值分布、平均连号/重号/质数数。

### 4. 选号方案生成
```bash
python scripts/generate.py --game ssq --count 5                      # 随机机选
python scripts/generate.py --game ssq --count 5 --strategy hot --data ssq_history.json
python scripts/generate.py --game dlt --count 3 --strategy balanced --odd-range 2,3 --sum-range 80,130
```
- 策略: `random` / `hot`(热号加权) / `cold`(遗漏回补加权) / `balanced`(均衡+默认过滤)。
- 过滤(缩水): `--odd-range` / `--big-range` / `--sum-range` / `--consec-range` / `--prime-range`。
- `--seed` 可复现; 多池彩种(双色球/大乐透)自动分别生成红蓝/前后区。

## Resources

### scripts/
- `lottery_core.py` — 彩种配置 `GAME_CONFIG`、数据加载 `load_normalized`、组合数/超几何分布工具(被其他脚本 import)。
- `fetch_history.py` — 多源抓取历史开奖, 输出归一化 JSON; 支持 `--local` 导入。
- `analyze.py` — 频率/冷热/遗漏/奇偶/大小/和值/连号/重号/质数 统计, 文本 + 可选 JSON。
- `generate.py` — 机选/热号/冷号/均衡 选号 + 过滤缩水。
- `probability.py` — 各奖级精确概率与期望收益(EV)计算。

### references/
- `games.md` — 各彩种玩法、开奖时间、奖级与奖金(已对照官方规则核对)。
- `data_sources.md` — 归一化数据格式、在线源端点、本地导入说明。
- `analysis_methods.md` — 统计指标定义与选号/缩水方法论, 含随机性纠偏。

### assets/
- `sample_ssq.json` — 30 期双色球示例数据, 用于离线试用 `analyze.py` / `generate.py`。

## Notes / caveats
- 奖金、开奖时间会随官方调整; 以 `references/games.md` 为研究基线, 重大决策查官方公告。
- 公开数据接口(openxai/500/官方)路径常变且可能受网络限制; 在线抓取失败时改用本地文件。
- 所有概率/EV 为数学事实; 所有统计/选号为描述性偏好, 均不提升中奖概率。
- 始终向用户强调理性购彩: 量力而行, 不倍投、不借贷、不沉迷。
