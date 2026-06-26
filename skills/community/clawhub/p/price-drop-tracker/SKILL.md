---
name: price-drop-tracker
description: 降价监控+自动下单。用户设置目标价和截止日期后，系统定时轮询飞猪价格，达标后通知或自动下单。Use when user mentions 降价监控, 价格提醒, 等降价, 盯盘, 自动下单, price drop tracking, deal monitoring for hotels/flights/travel products on Fliggy.
---

# Price Drop Tracker — 降价监控助手

## 功能概述

用户看中的酒店套餐/机票/旅游产品觉得贵想等降价，但每天手动查太麻烦。本 skill 让用户设好目标价和截止日期，AI 自动盯盘，降价达标立即通知甚至自动下单。

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| item_url | 否 | 飞猪商品链接（与 item_name+dates 二选一） |
| item_name | 否 | 商品名称（如"济州君悦65平米房套餐"） |
| check_in | 否 | 入住日期 YYYY-MM-DD |
| check_out | 否 | 退房日期 YYYY-MM-DD |
| target_price | 是 | 目标价格（数字，单位元） |
| deadline | 是 | 监控截止日期 YYYY-MM-DD |
| auto_book | 否 | 是否授权自动下单，默认 false |
| notify_mode | 否 | immediate（立即通知）/ daily_summary（每日汇总），默认 immediate |

## 执行流程

### Step 1: 解析输入 & 获取当前价

根据输入类型调用对应 flyai 命令获取当前价格：

**酒店类：**
```bash
flyai search-hotels --dest-name "{城市}" --key-words "{关键词}" --check-in-date "{check_in}" --check-out-date "{check_out}"
```

**航班类：**
```bash
flyai search-flight --from "{出发地}" --to "{目的地}" --depart-date "{date}"
```

**通用搜索：**
```bash
flyai fliggy-fast-search --query "{商品关键词}"
```

从返回 JSON 中提取 `price` 字段作为 current_price。

### Step 2: 创建定时监控任务

使用 qoder_cron 创建 cron 任务，每4小时检查一次：

```json
{
  "action": "add",
  "job": {
    "name": "降价监控-{商品简称}",
    "schedule": { "kind": "cron", "expr": "0 */4 * * *" },
    "payload": {
      "kind": "agentTurn",
      "message": "检查商品 {item_url或搜索关键词} 当前价格。若低于¥{target_price}，通知用户并附购买链接。截止日期{deadline}，若到期未达标发送最终建议。auto_book={true/false}。"
    }
  }
}
```

### Step 3: 定时任务执行逻辑

每次 cron 触发时：

1. 调用 flyai 查当前价
2. 对比 target_price
3. 若 current_price <= target_price：
   - 发送降价通知（含购买链接）
   - 若 auto_book=true 且库存充足，尝试自动下单
4. 若 current_price > target_price：
   - 继续监控（immediate 模式不通知）
5. 若到达 deadline 仍未达标：
   - 发送到期提醒 + 建议方案

### Step 4: 输出格式

**监控确认回执：**
```
✅ 已设置降价监控
   商品：{商品名称}
   当前价：¥{current_price}
   目标价：¥{target_price}（需降{percentage}%）
   监控期：现在 ~ {deadline}
   检查频率：每4小时
   通知方式：{immediate/daily_summary}
   自动下单：{已授权/未授权}
```

**降价通知：**
```
🔥 降价了！{商品名称}
   原价：¥{original_price} → 现价：¥{current_price}
   节省：¥{saved_amount}

   [立即预订]({jumpUrl})
```

**到期提醒：**
```
⏰ 监控到期提醒
   商品：{商品名称}
   当前价：¥{current_price}（距目标¥{target_price}还差¥{diff}）
   建议：
   1. 先订可退款的锁定当前价
   2. 提高目标价至¥{suggested_price}
   3. 延长监控至{new_deadline}
```

## 失败处理

| 场景 | 处理方式 |
|------|---------|
| 商品下架/售罄 | 通知"商品已下架"，调用 fliggy-fast-search 推荐3个相似商品 |
| 价格频繁波动 | 设置稳定阈值：连续2次检查均低于目标价才触发 |
| 目标价过低 | 第3天发送提醒："历史最低价¥{min_price}，是否调整目标？" |
| 临近截止未达标 | 提前24小时发送最终建议 |
| 自动下单失败 | 立即通知"自动下单失败，价格变动为¥{new_price}，是否手动下单？" |
| 监控任务超限 | 限制同时监控5个商品，超出提示先取消已有任务 |
| 飞猪接口限流 | 降级为每6小时检查一次 |

## 与其他 Skill 组合

- **+ seasonal-deal-aggregator**：判断当前是否处于季节性低价区间，动态调整目标价建议
- **+ refund-optimizer**：先订可退款的，同时监控更低价，发现后自动退旧订新
- **+ smart-rebooking**：降价后自动完成退旧订单+订新订单全流程
- **+ flight-hotel-bundler**：监控机酒组合套餐而非单品，对比单订vs套餐哪个更便宜
- **+ budget-splitter**：多人出行时监控总价而非单价

## 使用示例

**示例1：酒店套餐监控**
```
用户：监控济州岛君悦套餐 https://a.feizhu.com/47cMiK，降到3000以下通知我，5月15日前必须订

AI：✅ 已设置降价监控
   商品：济州君悦65平米房含税套餐
   当前价：¥3680
   目标价：¥3000（需降18.5%）
   监控期：现在 ~ 2026-05-15
   检查频率：每4小时
   通知方式：immediate
   自动下单：未授权
```

**示例2：机票降价监控**
```
用户：上海飞济州岛5月1日的机票，现在¥1600太贵了，降到1200以下帮我自动订

AI：✅ 已设置降价监控
   商品：上海→济州岛 2026-05-01
   当前价：¥1600
   目标价：¥1200（需降25%）
   自动下单：已授权
   
   我会每4小时检查一次，达标后自动为你下单。
```

**示例3：多人出行总价监控**
```
用户：我们4个人去济州岛，监控这个套餐总价降到12000以下（人均3000），6月1日前

AI：✅ 已设置降价监控
   商品：济州岛4人套餐
   当前总价：¥14720（人均¥3680）
   目标总价：¥12000（人均¥3000）
   监控期：现在 ~ 2026-06-01
```
