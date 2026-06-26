---
name: gold-price-auto
description: "金价自动汇报 - 每小时自动查询国内外金价并汇报"
version: 1.0.0
---

# 金价自动汇报 Skill

每小时自动查询金价并汇报

## 使用方法

```bash
# 手动执行
./run_gold_price.sh

# 或设置cron每小时执行
# 0 * * * * cd ~/.openclaw/workspace/skills/gold-price-auto && ./run_gold_price.sh
```

## 数据来源
- huangjinjiage.cn (金价查询网)
- 使用 playwright-scraper-skill 获取

## 输出内容
- 黄金9999 价格
- 品牌金价（周大福、老凤祥等）
- 银行金条价格
