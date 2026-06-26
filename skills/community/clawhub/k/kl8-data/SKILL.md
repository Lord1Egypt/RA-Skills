---
name: kl8-data
description: Query China Happy 8 (KL8) lottery historical data — latest draw, specific issue, recent draws, and number frequency analysis.
version: 1.0.0
tags:
  - lottery
  - china
  - data
  - kl8
  - statistics
category: "Data & APIs"
os:
  - windows
  - macos
  - linux
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: 🎲
---

# KL8 Lottery Data

Query and analyze China Happy 8 (快乐8/KL8) lottery historical draw data. Includes latest draw, specific issue lookup, recent draws listing, and number frequency analysis.

## Quick Start

```python
import kl8_data

# Get latest draw
kl8_data.get_latest()

# Query specific issue
kl8_data.get_issue("2026097")

# List recent 10 draws
kl8_data.list_recent(10)

# Analyze number frequency
kl8_data.analyze()
```

## API

| Function | Description |
|----------|-------------|
| `get_latest()` | Get the most recent draw result |
| `get_issue(issue)` | Query a specific issue number |
| `list_recent(count=10)` | List recent N draws |
| `analyze()` | Number frequency statistics (hot/cold numbers) |

## Data

Hardcoded draw data from March–April 2026 (issues 2026069–2026097, 29 draws). Each draw has 20 numbers drawn from 1–80. To update with fresh data, edit `KL8_DATA` dict in `kl8_data.py`.

## Source

`kl8_data.py` (98 lines) in this skill directory.

## 触发场景
- 用户说"快乐8"、"KL8"、"福彩"
- 用户说"开奖数据"、"彩票查询"


## B站学习
> 学习时间: 2026-06-01 20:57

- **想学的很多**: 加州大学伯克利分校：双语字幕 Data 8: Foundations of Data Science  数据 8：数据科
  - 关键词: 加州大学伯克利分校, 双语字幕, Data, Foundations, of
- **Ningning不摸鱼**: 轻松解决安卓无法访问data目录问题
  - 关键词: 轻松解决安卓无法访问data目录问题

## B站学习
> 学习时间: 2026-06-01 21:02

- **想学的很多**: 加州大学伯克利分校：双语字幕 Data 8: Foundations of Data Science  数据 8：数据科学基础 2023 年春季
- **Ningning不摸鱼**: 轻松解决安卓无法访问data目录问题
- **匿名用户11233**: 用 Yaesu FTX-1 简单的玩一下 FT8，iPhone iFTx，Type-C线 直连手机

## 融合来源: kl8-data-713e0f
> 融合时间: 自动合并

> 学习时间: 2026-06-01 21:08
- **电脑蓝屏_南京小吧**: 蓝屏终止代码：KERNEL_DATA_INPAGE_ERROR
- **vcbyo**: 安卓13怎么访问data？mt管理器访问不了data？无法使用此文件夹？访问data教学开始
- **迷你枪战精英-指难针**: DATA WING居然隐藏了一个腐败的家庭?!
> 融合时间: 自动合并
> 学习时间: 2026-06-02 07:52
- **bili_32716557996**: 159c7d41-1c97-4efc-8895-9a9de82ad6ac
- **Supermansupe**: 27143d84-e21d-4225-9a7b-67ac7c97ad50
- **Supermansupe**: 27143d84-e21d-4225-9a7b-67ac7c97ad50

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:21

- **想学的很多**: 加州大学伯克利分校：双语字幕 Data 8: Foundations of Data Science  数据 8：数据科学基础 2023 年春季
  https://www.bilibili.com/video/BV19eqHYSEDG
- **匿名用户11233**: 用 Yaesu FTX-1 简单的玩一下 FT8，iPhone iFTx，Type-C线 直连手机
  https://www.bilibili.com/video/BV1xRvhBSEut
- **小猫豆Medoya**: [MCBE]一个视频带你走进物品data！
  https://www.bilibili.com/video/BV13rDtBdEvB

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:34

- **想学的很多**: 加州大学伯克利分校：双语字幕 Data 8: Foundations of Data Science  数据 8：数据科学基础 2023 年春季
  https://www.bilibili.com/video/BV19eqHYSEDG
- **匿名用户11233**: 用 Yaesu FTX-1 简单的玩一下 FT8，iPhone iFTx，Type-C线 直连手机
  https://www.bilibili.com/video/BV1xRvhBSEut
- **小猫豆Medoya**: [MCBE]一个视频带你走进物品data！
  https://www.bilibili.com/video/BV13rDtBdEvB
