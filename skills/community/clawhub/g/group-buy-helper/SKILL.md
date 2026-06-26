---
name: group-buy-helper
description: Analyze group-buy and bargain campaigns, estimate success probability, and suggest participation strategies
version: 1.0.0
tags: shopping, group-buy, pinduoduo, social-commerce, savings, china
---

# Group Buy Helper - 拼团/砍价助手

Analyze group-buy and bargain campaigns, estimate success probability, and suggest participation strategies. Use when the user asks to 分析拼团、估算砍价成功率、判断是否值得参团、生成拉人分享文案 or assess group-buy outcomes.

## Usage Scenarios

### Scenario 1: Bargain Success Estimation
**User input:** "分析砍价活动，还差 50 元，还有 24 小时，我已经有 30 个朋友帮忙了"
**Expected output:** The skill calculates based on typical per-helper amounts (e.g., new users give higher amounts, existing users give lower amounts), estimates the number of additional helpers needed, and provides: success probability (high/medium/low), recommended actions (continue recruiting / invite new users / consider abandoning), and whether the expected effort is worth the discount.

### Scenario 2: Group-Buy Feasibility Check
**User input:** "拼团成功率，还差 2 人，只剩 3 小时了"
**Expected output:** The skill considers time remaining, number of people needed, and typical group-buy conversion behavior. Provide a probability estimate, recommend whether to continue waiting or pay full price, and offer share-worthy text to recruit the last members.

### Scenario 3: Share Copy Generation
**User input:** "生成分享文案，帮我在微信群拉人拼这个团"
**Expected output:** The skill generates 2-3 ready-to-copy share texts optimized for different social contexts (WeChat group, Moments, direct message). Each includes: what the product is, the discount being offered, a clear call to action, and a note about how many people are still needed. Text is persuasive but not spammy.

## 功能

- 🎯 砍价成功率估算
- 📊 拼团成团概率分析
- 💡 最优策略建议
- 📝 分享文案生成
- ⏰ 活动状态追踪

## 使用

```
分析砍价活动 还差多少
拼团成功率 还差2人
生成分享文案
```

## 输入建议

- 拼团场景：原价、拼团价、还差人数、剩余时间
- 砍价场景：目标价、当前价、已助力人数、每次助力金额（如已知）
- 平台：拼多多 / 淘宝等

## 输出要求

- 明确给出是否建议继续参与
- 给出成功概率或难度等级
- 给出下一步动作建议：继续拉人 / 尽快下单 / 直接放弃
- 需要生成分享文案时，输出可直接复制的文本

## 边界

- 估算结果是策略建议，不应伪装成平台官方概率
- 输入缺少关键字段时，应先提示信息不足
- 已达成目标时，应直接返回完成状态，不继续计算剩余人数
