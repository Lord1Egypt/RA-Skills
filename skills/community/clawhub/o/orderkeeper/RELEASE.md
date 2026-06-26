# OrderKeeper Release Notes

## Short Description

购物后链路管家，帮你盯订单时限、售后动作、价保窗口、保修路径和客服沟通话术。

## Marketplace Card Copy

Title:
- 收货总管

Alternate title:
- OrderKeeper

Short description:
- 购物后链路管家，帮你盯订单时限、售后动作、价保窗口、保修路径和客服沟通话术

Install hook:
- 不是帮你买，而是帮你把买完之后的麻烦事接住

## Announcement Copy

`收货总管（OrderKeeper）` 不是购物前的判断 skill。

它解决的是更靠后的、也更容易让人掉链子的那一段：
- 这单现在该退款、换货、补发、赔偿，还是先观望
- 哪个时限最危险，再拖就超时
- 现在要留哪些证据
- 客服第一句话应该怎么说
- 收据、保修、订单结果怎么串起来

所以它的定位很明确：

`不是帮你买，而是帮你把“买完之后的麻烦事”接住。`

默认它会给出：
- After-Sales Verdict
- Clock And Window
- Evidence To Save Now
- Recommended Move
- Customer Service Script
- After-Sales Card

也就是说，它不是在复述订单状态，而是在把售后动作收成一个可执行结论。

## Official Launch Post

今天做了一个我很喜欢的新 OpenClaw skill：`收货总管（OrderKeeper）`。

很多购物 skill 都在解决买前问题：
- 值不值得买
- 应该在哪里买
- 这一单怎么下最优
- 这个 seller 风险高不高

但用户真正开始花时间的，往往是买完之后：
- 缺件了
- 发错货了
- 到货延迟
- 商品有质量问题
- 价保快过期
- 发票和保修链路不清楚
- 客服该怎么说最省事

所以 `收货总管` 做的不是买前判断，而是买后接盘。

它会直接把问题压成：
- 现在最该处理的动作
- 最危险的时限
- 必须保留的证据
- 可直接发送的客服话术
- 订单 / 收据 / 保修 / 结果的一张售后卡

我给它定的一句话文案是：

`从签收到维权，全程不掉链子的购物后援。`

如果你也经常遇到“不知道现在该退、该换、该等，还是该去谈价保”的情况，这个 skill 会很顺手。

## Suggested Tags

- latest
- shopping
- post-purchase
- after-sales
- refund
- exchange
- reshipment
- price-protection
- warranty
- receipt
- customer-service

## Suggested Repo Name

- `openclaw-skill-orderkeeper`

## Manual Publish Command

```bash
clawhub publish /absolute/path/to/orderkeeper \
  --slug orderkeeper \
  --name "收货总管" \
  --version "1.0.0" \
  --changelog "Launch 收货总管 (OrderKeeper), a post-purchase order and after-sales skill that flags deadlines, chooses whether to refund, exchange, reship, compensate, or wait, generates customer-service scripts, and ties order, receipt, warranty, and outcome into one card." \
  --tags "latest,shopping,post-purchase,after-sales,refund,exchange,reshipment,price-protection,warranty,receipt,customer-service"
```
