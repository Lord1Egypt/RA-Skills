# PriceTide Release Notes

## Short Description

判断商品现在该不该买，识别短期低点、等待价值和活动窗口，而不是只做哪里便宜的比较。

## Marketplace Card Copy

Title:
- PriceTide

Alternate title:
- 购买时机官

Short description:
- 购物时机判断 skill：告诉用户现在买、等等看、先关注等活动，还是不值得追这个价

Install hook:
- 不是比哪里便宜，而是判断现在该不该买

## Announcement Copy

PriceTide 不是再做一个价格比较器。

它解决的是很多用户在购物里更真实、也更高频的犹豫：
- 现在买还是等等
- 这是不是短期低点
- 值不值得为了优惠再等一轮
- 是直接下单，还是先关注下一波活动

也就是说，它把购物建议从“空间维度”升级到了“时间维度”。

相邻 skill 在回答：
- 买哪个更值
- 在哪买更合适
- 怎么下单最划算

而 PriceTide 回答的是：
- 现在是不是该动手

这一版默认把结论收敛到四种 verdict：
- `现在买`
- `等等看`
- `先关注，等活动`
- `不值得追这个价`

它不满足于解释价格，而是把价格线索、活动节奏、等待收益和等待成本一起折算成一个行动建议。

## Suggested Tags

- latest
- shopping
- buy-timing
- price-history
- wait-or-buy
- deal-timing
- ecommerce
- taobao
- jd
- pdd

## Suggested Repo Name

- `openclaw-skill-pricetide`

## Preflight

```bash
cd /absolute/path/to/pricetide
clawhub whoami
bash /absolute/path/to/codex/tmp/validate_clawhub_skill_dir.sh .
```

## Publish Command

### One command

```bash
cd /absolute/path/to/pricetide
sh scripts/publish.sh
```

### Manual command

```bash
clawhub publish /absolute/path/to/pricetide \
  --slug pricetide \
  --name "PriceTide" \
  --version "1.0.0" \
  --changelog "Launch PriceTide, a buy-timing decision skill that judges whether the current price is a buy-now window, a wait candidate, an event-watch case, or not worth chasing." \
  --tags "latest,shopping,buy-timing,price-history,wait-or-buy,deal-timing,ecommerce,taobao,jd,pdd"
```
