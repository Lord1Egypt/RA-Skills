---
name: gold-price-fetcher
description: 通过京东金融 API 获取实时金价，返回带时间戳的完整信息。当用户查询金价、询问今日金价、获取实时金价时触发此技能。
---

# 金价查询技能

## 触发场景

当用户需要查询实时金价时激活，例如：
- "查询今日金价"
- "现在金价多少"
- "获取实时金价"
- "金价最新是多少"

## 功能说明

1. 调用京东金融 API 获取实时金价
2. 解析返回结果中的 `minimumPriceValue` 字段
3. 返回带时间戳的完整信息（格式：2026-04-04 19:14 金价：568.50 元/克）
4. 缓存上一次查询结果，避免频繁请求

## API 信息

- **接口地址**: https://ms.jr.jd.com/gw2/generic/CreatorSer/newh5/m/getFirstRelatedProductInfo
- **请求方式**: GET
- **参数**:
  - circleId=13245
  - invokeSource=5
  - productId=21001001000001

## 使用方法

直接运行脚本获取金价：

```bash
python scripts/fetch_gold_price.py
```

## 缓存机制

- 缓存文件：`cache/last_price.json`
- 记录上次查询时间和金价
- 可用于对比金价变化

## 输出示例

```
2026-04-04 19:14 金价：568.50 元/克
```
