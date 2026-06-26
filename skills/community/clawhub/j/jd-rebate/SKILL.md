---
name: rebate-assistant
description: 返利宝统一技能。只按 3 个用户场景工作：S01 授权与教程、S02 链接返利、S03 商品搜索。用户说“返利”“教程”“详细教程”“提现教程”“提现10元”“确认提现”“我已授权”“账户余额”等走 S01；发送淘宝、京东、拼多多商品链接走 S02；表达想买什么商品时走 S03。S03 的职责是提取商品搜索信息，调用搜索接口，并返回后续可生成返利链接的商品结果。
---

# 返利宝

## 核心准则

1. 返利宝只有一条主链路：用户给“品” -> 识别 -> 搜索或生成返利链接 -> 返回返利结果。
2. `M01` 的职责是让用户知道返利宝是什么、怎么用、为什么要先做微信授权。
3. `M02` 的职责是承接淘宝、京东、拼多多商品链接，进入返利链接生成链路。
4. `S03` 的职责是识别“用户想买什么商品”，提取搜索信息并直接进入商品搜索链路。
5. `S03` 不是为了展示分词，更不是为了做炫技式槽位输出。
6. 对用户来说，返利宝是一个统一产品，不是多个独立工具。

## 执行硬约束

1. 命中返利宝后，优先调用 `scripts/cli/rebate_assistant_router.js`。
2. 若调用了 `rebate_assistant_router.js`、`m01_operation_guide.js`、`m02_platform_link.js`、`product_search.js` 中任一脚本，脚本标准输出是什么，就向用户原样返回什么。
3. 返回方式必须是一条普通 assistant 对话消息，不能只显示在 `tool output` 折叠面板中。
4. 返回给用户的消息必须使用 md 格式；调用脚本时优先使用 `--format md`。
5. 禁止在脚本输出前后追加解释、总结、润色、转述、商品推荐、返利说明或教程扩写。
6. 禁止在接口失败、未命中商品或未完成授权时自行编造“返利链接”“返利口令”“返利到账说明”。
7. 不要把内部处理过程作为主动面向用户的过程话术；用户发商品链接时，如需先回应再调用脚本，优先说“我先帮你查这个商品有没有返利入口。”脚本最终输出仍按第 2 条原样返回。
8. 即使脚本退出码非 0，只要标准输出已有面向用户的文本，也必须原样返回标准输出，不得因为失败码自行改写话术。

## 路由规则

1. 命中 `返利`、`返利教程`、`教程`、`详细教程`、`提现教程`、`提现10元`、`确认提现`、`我已授权`、`授权完成`、`账户余额` 时，进入 `S01`。
2. 只要消息里出现 `http://` 或 `https://` 商品链接，进入 `S02`。
3. 没有链接，但用户表达购物需求时，进入 `S03`。
4. `S03` 统一走 `product_search.js`。
5. 对话层只调用统一入口脚本 `rebate_assistant_router.js`。

## 当前实现边界

1. `S01` 已是固定话术和固定流程。
2. `S02` 当前已承接平台识别、单商品查询、租约申请和返利链接生成。
3. `S03` 当前统一由 `product_search.js` 承接，输出 `product_search_intent + search_request`，并直接调用商品搜索接口。
4. `S03` 的核心入参只有两个：尽量完整的 `raw_text`，以及可识别时才传的 `platform`。
5. 商品搜索返回结果后，用户再通过商品链接进入 `S02` 完成返利链接生成。

## 核心脚本

### 构建方式

```bash
cd ~/.openclaw/workspace/skills/rebate-assistant
npm install
npm run build
```

构建产物输出到 `scripts/`，供 skill 直接调用。

### 对话入口

- `scripts/cli/rebate_assistant_router.js`

### 场景脚本

- `scripts/cli/m01_operation_guide.js`
- `scripts/cli/m02_platform_link.js`
- `scripts/cli/product_search.js`

### 内部识别与共享逻辑

- `scripts/cli/recognize_platform_link.js`
- `scripts/cli/recognize_precise_product_search.js`
- `src/productSearchProtocol.ts`
- `src/common.ts`

## S01 授权与教程

### 用户场景

用户第一次接触返利宝，或者不知道如何使用，或者需要完成微信授权，或者想看提现说明，或者想查询账户余额，或者要发起提现申请。

### 目标

1. 说明返利宝怎么用。
2. 明确告知：使用返利宝前需要先完成微信授权。
3. 用户授权完成后，能继续进入链接返利或搜索返利主链路。
4. 已授权用户可以查询账户余额。
5. 已授权用户可以先确认提现金额，再提交提现申请。

### 触发示例

- `返利`
- `教程`
- `详细教程`
- `提现教程`
- `提现10元`
- `确认提现`
- `我已授权`
- `账户余额`

### 当前动作

- `start_auth`
- `confirm_auth`
- `detailed_tutorial`
- `withdraw_tutorial`
- `withdraw_prepare`
- `withdraw_confirm`
- `account_balance`

### 提现申请流程

1. `提现教程`、`怎么提现`、`提现规则` 只返回 `withdraw_tutorial`。
2. `我要提现`、`提现`、`全部提现` 进入 `withdraw_prepare`，先查询账户余额；可提现金额低于 1.00 元时直接说明暂不可提现，可提现金额满足最低提现条件时再询问用户要提现多少钱。
3. `提现10元`、`申请提现10元` 进入 `withdraw_prepare`，先校验金额和可提现余额，不直接提交提现。
4. `withdraw_prepare` 在金额合法时必须返回固定二次确认话术，头部提醒用户先关注小马享生活公众号，否则无法顺利领取微信红包。
5. 用户回复 `确认提现` 或 `确定提现` 后进入 `withdraw_confirm`，再调用 `/v1/withdraw/apply`。
6. 提现失败时返回固定失败话术，并附上公众号关注链接。

### 调试入口

```bash
node ~/.openclaw/workspace/skills/rebate-assistant/scripts/cli/m01_operation_guide.js --action <action> --format md
```

`withdraw_prepare` 调试时需要带原始消息：

```bash
node ~/.openclaw/workspace/skills/rebate-assistant/scripts/cli/m01_operation_guide.js --action withdraw_prepare --raw-message '提现10元' --format md
```

可用 `action`：

- `start_auth`
- `confirm_auth`
- `detailed_tutorial`
- `withdraw_tutorial`
- `withdraw_prepare`
- `withdraw_confirm`
- `account_balance`

## S02 链接返利

### 用户场景

用户直接给淘宝、京东、拼多多商品链接，希望获得返利。

### 目标

1. 识别链接所属平台。
2. 承接商品链接，进入返利链接生成链路。
3. 让用户不需要理解平台规则，只需要发链接。

### 触发示例

- `https://item.jd.com/100012043978.html`
- `https://e.tb.cn/...`
- `https://mobile.yangkeduo.com/...`

### 当前边界

1. 只处理淘宝、京东、拼多多商品链接。
2. 链接场景直接承接商品查询、推广位租约和返利链接生成。
3. 对于淘宝短链、混合文案、口令链接，优先保留用户原始消息给后端识别。

### 调试入口

```bash
node ~/.openclaw/workspace/skills/rebate-assistant/scripts/cli/m02_platform_link.js --raw-message '<用户原始消息>' --format md
```

## S03 商品搜索

### 用户场景

用户没有给链接，而是直接说自己想买什么。

### 目标

1. 识别用户真正想买的商品。
2. 抽取尽量完整的商品信息，作为搜索接口的 `raw_text`。
3. 能识别平台时传 `platform`，识别不到就不传。
4. 搜索到商品后，用户再把商品链接发来进入返利链接生成链路。

### 适用输入

- 品牌 + 型号
- 品牌 + 商品名
- SKU / 编码
- 完整商品标题
- 类目 + 预算
- 类目 + 场景 / 人群 / 送礼对象

### 示例

- `李宁 行川2SE`
- `京东 iPhone 15 Pro Max 256G`
- `我想买一双袜子`
- `推荐个 300 左右的耳机`
- `适合送女朋友的礼物`
- `100 以内儿童水杯`

### 调试入口

```bash
node ~/.openclaw/workspace/skills/rebate-assistant/scripts/cli/product_search.js --raw-message '<用户原始消息>' --format md
```

## S03 统一输出

`S03` 当前统一输出两层结构：

1. `product_search_intent`
2. `search_request`

### product_search_intent

表示识别后的商品意图。

关键字段：

- `intent_mode`
- `query_text`
- `query_tokens`
- `brand`
- `series`
- `model`
- `sku`
- `product_name`
- `category`
- `attributes`
- `specs`
- `price_min`
- `price_max`
- `price_target`
- `crowd`
- `usage_scene`
- `gift_target`
- `platform_hint`
- `sort_hint`

### search_request

表示可直接给后续商品搜索接口使用的统一入参。

结构如下：

```json
{
  "ready": true,
  "intent_mode": "search",
  "keyword": "袜子",
  "search_terms": ["袜子"],
  "filters": {
    "brand": null,
    "series": null,
    "model": null,
    "sku": null,
    "product_name": "袜子",
    "category": "袜子",
    "attributes": [],
    "specs": [],
    "price_min": null,
    "price_max": null,
    "price_target": null,
    "crowd": null,
    "usage_scene": null,
    "gift_target": null,
    "platform_hint": null,
    "sort_hint": null
  }
}
```

## 统一入口

正常对话只使用下面这个脚本：

```bash
node ~/.openclaw/workspace/skills/rebate-assistant/scripts/cli/rebate_assistant_router.js --raw-message '<用户原始消息>' --format md
```

路由结果：

1. `S01` -> `m01_operation_guide.js`
2. `S02` -> `m02_platform_link.js`
3. `S03` -> `product_search.js`

## 文档约束

1. 后续文档继续只围绕 `S01 / S02 / S03` 三个用户场景展开。
2. 不再把大量兼容脚本、历史代理脚本写进主规范。
3. 不再为了测试展示去扩写分词说明、长篇样例、重复状态表。
4. 如果后续接中台搜索接口，优先改 `search_request` 对接方式，不推翻场景结构。
