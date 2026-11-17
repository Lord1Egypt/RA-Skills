---
name: meituan-coupon-bot
description: "美团查券机器人。当用户想要搜索美团优惠券、查找外卖到店折扣券、浏览热销榜单或比价时使用。覆盖到店餐饮火锅、咖啡、奶茶、日料、烧烤、快餐等和外卖汉堡、炸鸡、咖啡、奶茶等全品类。关键词：美团、优惠券、查券、搜券、外卖券、到店券、火锅券、咖啡券、奶茶券、比价。"
agent_created: true
---

# 美团查券机器人

本技能通过美团联盟开放 API 实现美团优惠券搜索与比价。覆盖**到店餐饮**（团购美食、火锅、烧烤、日料、快餐、咖啡、奶茶等）和**外卖配送**（快餐、汉堡、咖啡、奶茶、炸鸡等）两大场景。

本技能仅为用户查券和比价提供方便，每条搜索结果直接附带购买链接，用户点击即可跳转到美团下单。

## 核心能力

1. **关键词查券** — 按品类/关键词搜索优惠券，展示价格、销量、品牌，直接附带购买链接
2. **榜单浏览** — 查看今日必推、同城热销等榜单（支持到店/外卖）
3. **外卖查券** — 搜索外卖配送优惠券，直接附带购买链接

> 所有操作通过 `scripts/run.js` 统一入口调用，API 凭证已内置在 `scripts/config.json` 中。

---

## 环境准备（静默执行，不向用户展示）

每次对话中第一次执行本技能功能时，必须先完成环境准备。`RUN_JS` 指向 `<skill_dir>/scripts/run.js`。

```
node "$RUN_JS" init
```

- `ok: true` → 环境就绪，静默继续
- `ok: false` → 根据 `error` 字段告知用户并停止

---

## 意图识别

按顺序判断用户消息，命中即停止：

**第一关 — 外卖意图**：含「外卖/点外卖/送餐/到家」
→ 子流程D（外卖查券/外卖榜单）

**第二关 — 查券意图**：含「查券/搜券/找券/优惠券/有什么券/帮我找」+ 品类词
→ 子流程A（默认到店餐饮）

**第三关 — 榜单意图**：含「排行榜/热销/必推/热门/今日必推/同城热销」
→ 子流程B（默认到店餐饮）

**第四关 — 品类词**：含品类词（火锅/咖啡/奶茶/日料/烧烤/快餐/汉堡/炸鸡/比萨…）
→ 询问「要我帮你搜一下相关的优惠券吗？到店吃还是外卖送？」→ 根据用户回答走子流程A或D

---

## 子流程A：到店关键词查券

### Step A1：提取关键词 + 发起搜索

从用户消息中提取搜索关键词（品类名、菜系名等），调用：

```
node "$RUN_JS" query-coupon --scene dine-in --keyword "<关键词>" --page-size 5 [--page N]
```

解析返回 JSON，提取 `coupons` 数组。

### Step A2：为每条结果生成购买链接

对 `coupons` 数组中的每条优惠券，提取 `productViewSign`、`platform`、`bizLine`，并行调用：

```
node "$RUN_JS" referral-link --product-view-sign "<productViewSign>" --platform <platform> --biz-line <bizLine> --link-type "2"
```

解析每条返回的 `referralLinkMap["2"]`，得到短链接。将这些链接与优惠券信息一起整合展示。

### Step A3：展示搜索结果（含购买链接）

每条券以卡片形式展示，直接附带可点击的购买链接。头像图片 URL 中的尺寸参数用正则替换为 134×134（如 `267h_267w` → `134h_134w`）。

```
🔍 到店搜索「{关键词}」找到 {couponCount} 张券：

**{index}. {brandName}** {name}

💰 售价：¥{sellPrice}　🏷️ 原价：¥{originalPrice}　📊 销量：{saleVolume}

[购买链接]
📱 {referralLinkMap["2"]}

![|134]({headUrl 替换尺寸后})

---
```

展示后询问：「有需要可以查看更多，或者要翻页吗？」

### Step A4：翻页

```
node "$RUN_JS" query-coupon --scene dine-in --keyword "<关键词>" --page-size 5 --page <N+1> --search-id "<上次返回的searchId>"
```

然后重复 Step A2–A3 为翻页结果生成链接并展示。

---

## 子流程B：到店榜单浏览

### Step B1：确定榜单类型

| 用户表达 | list-topic |
|---------|-----------|
| 今日必推/今天推荐 | 2 |
| 同城热销/热卖 | 3 |
| 实时热销/正在热卖 | 5 |

```
node "$RUN_JS" query-coupon --scene dine-in --list-topic <topic> --page-size 5 [--city-id <id>] [--city <城市名>]
```

### Step B2：生成链接并展示

同子流程A的 Step A2–A3，为榜单结果生成购买链接并展示。

---

## 子流程D：外卖查券/外卖榜单

### 外卖品类关键词

外卖搜索支持的品类：**快餐、汉堡、炸鸡、比萨、咖啡、奶茶、饮品、甜品、轻食、沙拉、小吃、米粉、面条** 等。

### Step D1：外卖关键词搜索

```
node "$RUN_JS" query-coupon --scene delivery --keyword "<关键词>" --page-size 5 [--page N]
```

### Step D2：外卖榜单浏览

```
node "$RUN_JS" query-coupon --scene delivery --list-topic <topic> --page-size 5 [--city <城市名>]
```

### Step D3：生成链接并展示搜索结果

对查询结果中的每条外卖优惠券，并行调用 `referral-link` 生成购买链接，然后整合展示：

```
🛵 外卖搜索「{关键词}」找到 {couponCount} 张券：

**{index}. {brandName}** {name}

💰 售价：¥{sellPrice}　🏷️ 原价：¥{originalPrice}　📊 销量：{saleVolume}　🏠 可用门店：{availablePoiNum}家

[购买链接]
📱 {referralLinkMap["2"]}

![|134]({headUrl 替换尺寸后})

---
```

> 外卖券字段 `availablePoiNum` 表示该券可用的外卖门店数量。

展示后询问：「有需要可以查看更多，或者要翻页吗？」

### Step D4：翻页

```
node "$RUN_JS" query-coupon --scene delivery --keyword "<关键词>" --page-size 5 --page <N+1> --search-id "<上次返回的searchId>"
```

然后重复 Step D3 为翻页结果生成链接并展示。

---

## 城市支持

榜单模式支持通过 `--city <城市名>` 指定城市。当前支持的城市编码：

| 城市 | 编码 | 城市 | 编码 | 城市 | 编码 | 城市 | 编码 |
|------|------|------|------|------|------|------|------|
| 北京 | 010 | 上海 | 021 | 广州 | 020 | 深圳 | 0755 |
| 杭州 | 0571 | 成都 | 028 | 重庆 | 023 | 武汉 | 027 |
| 南京 | 025 | 苏州 | 0512 | 西安 | 029 | 长沙 | 0731 |
| 天津 | 022 | 郑州 | 0371 | 青岛 | 0532 | 厦门 | 0592 |

---

## 错误处理

| 场景 | 回复话术 |
|------|---------|
| 搜索无结果 | 「没找到相关优惠券，换个关键词试试？」 |
| API 返回异常 | 「查询服务暂时不可用，稍后重试 😅」 |
| 网络超时 | 「网络开小差了，再试一次？」 |

---

## 联系方式

如有问题或建议，欢迎发送邮件至 jiangxinyu10@meituan.com 反馈。
