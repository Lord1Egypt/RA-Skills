---
name: Privora · 实时监控 for AI Agents
title: 🔔 Privora · 实时监控 / 黄金实时监控 · 基金净值监控 · 股价预警（越线即飞书/微信 Webhook · 黄金/基金/港股/美股/A股 · AI Agent）
version: 1.0.8
updatedAt: 2026-10-10
keywords:
  - 实时监控
  - 黄金实时监控
  - 黄金监控
  - 基金净值监控
  - 多资产阈值监控
  - 指标监控
  - 股价预警
  - 黄金预警
  - 黄金价格预警
  - 基金预警
  - 基金净值预警
  - 实时告警
  - 指标告警
  - 阈值告警
  - 阈值监控
  - 价格预警
  - 价格提醒
  - 跌破阈值通知
  - webhook
  - webhook notification
  - 飞书
  - 微信
  - 群机器人通知
  - 云端监控
  - metric alert
  - threshold alert
  - price alert
  - AI Agent
  - 多资产告警
  - 港股预警
  - 美股预警
  - A股
  - 股价跌破提醒
description: Privora 实时监控——黄金实时监控 / 基金净值监控 / 多资产阈值告警，给一个已订阅资产字段配一条阈值规则（跌破/突破/等于），越线即飞书/微信/通用 Webhook 通知你；港股/美股/A股同样支持。建渠道→建规则→验证→上线，一份文档 11 步走完；Bearer Token 直连 /agent/skills/execute。
license: MIT-0
metadata:
  {
    "openclaw": {
      "emoji": "🔔",
      "requires": {
        "env": ["LG_AGENT_BASE_URL", "LG_AGENT_TOKEN"]
      },
      "capabilities": {
        "shell": true,
        "network": {
          "outbound": true,
          "hosts": ["privora.cn", "www.privora.cn", "lg-data.cc"],
          "endpoints": ["POST <LG_AGENT_BASE_URL>/agent/skills/execute"]
        }
      }
    }
  }
---

# Privora · 实时告警（一个场景，从零到真正收到通知）

**一句话**：「贵州茅台跌破 1500 就通知我」——本包只做这一件事，端到端。

不是 API 参考手册。如果你需要行情查询 / 回测 / 模拟交易 / 流程编排等其它能力，去装完整版 [`privora-cn-quant`](https://clawhub.ai/guangfuwu/privora-cn-quant)（97 个 skillId）。本包只有 [§7](#7-本包-20-个-skill-速查) 列出的 **20 个 skillId**，够用且不多。

---

## 0. 还没有 Privora 账号？先别急着找 Token

本包做的事其实是**持续监控**——盯着一个资产字段，越线就通知你；飞书 / 微信 Webhook 只是通知的方式（产品里这个功能页面叫"指标告警" / Metric Alert，同一件事，两种叫法，别被术语绕晕）。核心动作（建规则、上线）都是**写操作**，需要 Bearer Token + `realtime-alerting` preset + 一个已订阅的数据资产（见 [§2](#2-开始之前)）——如果你是第一次听说 Privora，直接往下翻会在 §2 撞到"要 Token"的门槛，而你可能连有没有你要的资产都还不知道。按下面顺序走，不用先注册：

1. **30 秒看有没有你要的资产（不需要注册 / 不需要 Token）**——打开 [privora.cn/marketplace](https://privora.cn/marketplace?utm_source=clawhub&utm_medium=agent_skill&utm_campaign=privora-alert)，或装完整版 [`privora-cn-quant`](https://clawhub.ai/guangfuwu/privora-cn-quant) 用它的匿名预览 skill（`marketplace.item.list` / `dashboard.data.get` / `dataasset.get` / `dataasset.data.get`，全只读，见其 SKILL.md §🌐 匿名预览）。最快的验证点：「SGE 黄金白银市场」看板匿名可读、当天价格 + 走势，30 秒就能确认黄金这条线真的在动，值不值得配一条监控规则。**基金目前没有等价的匿名可读看板，样本可能不新鲜**——想确认基金资产新不新鲜，注册后用 `dataasset.metadata.get` 查 `lastUpdated` 更准，别只凭匿名预览下结论。港股 / 美股 / A股 同样在覆盖范围内。
2. **确认平台上有你要的资产之后再注册**——去 [privora.cn/register](https://privora.cn/register?utm_source=clawhub&utm_medium=agent_skill&utm_campaign=privora-alert)。**这一步必须由你本人在浏览器里完成——Agent 不能替你注册、也不能替你 mint Token**（跟 §Token 使用建议同一条铁律：Token 创建是 operator 动作）。
3. **登录后去 [privora.cn/profile/tokens](https://privora.cn/profile/tokens?utm_source=clawhub&utm_medium=agent_skill&utm_campaign=privora-alert)，建 Token 时勾选 `realtime-alerting` 场景按钮**（对应本包 [§7](#7-本包-20-个-skill-速查) 的 18 个 scope）。
4. **拿到 Token、订阅了资产之后，回到 [§2](#2-开始之前) 继续**——四个前置条件到这时应该已经全部满足。

已经有 Token、已经订阅了资产？跳过本节，直接看 §2。

---

## 1. 做什么 / 不做什么

**做什么**：给一个已订阅的数据资产的某个字段配一条阈值规则（GT/GTE/LT/LTE/EQ/NEQ），跨越阈值时通过飞书 / 微信 / 通用 Webhook 通知操作者——本质上是**持续监控**，通知只是触发后的动作。**资产类型不限**——黄金、基金、港股、美股、A股皆可，只要资产已订阅、字段是数值型（本文档跑的是 A股示例，只是因为好懂，不代表覆盖范围）。**"实时"这个词对黄金成立**（SGE 黄金白银市场看板匿名可读、当天更新）；**基金目前没有等价的匿名可验证实时看板**——"基金监控"准确，但先别自己加"实时"两个字，除非你已经用 `dataasset.metadata.get` 确认过目标基金资产的更新频率。

**不做什么**：
- 不是数据接入包——资产必须已经可见（订阅/接入是 `privora-cn-quant` 或 web 端 `/marketplace` 的事）。
- 不设 `dashboardId`——告警绑定资产，不绑定 dashboard。
- 不做 on-call / 升级链路，只有一条通知。
- **没有任何删除类操作**——"不想再吵了"用 `metric.alert.snooze`（暂停到某个时间）或 `metric.alert.toggle`（关闭），永远不是 delete。本包的 20 个 skill 里没有 `metric.alert.delete`。
- 只支持 WEBHOOK 渠道；一次跑一条规则。
- **不自己跑轮询循环**——评估由平台后台进程负责（[§6](#6-上线后由平台自动评估)），本包只负责把规则配对、配上线。

**三重证明**（`success:true` 不算数，下面三条都要拿到才算配完）：

1. **渠道证明**（在规则存在之前）：`plugin.webhook.send` 返回 `success:true`，且用户确认在群里看到了测试消息。
2. **规则证明**：`metric.alert.test` 返回 `triggered:true, webhookSent:true`。**但这条证明不能，也不该，在用户的真实阈值上直接拿到**——[§3 步骤 6-9](#3-完整流程11-步) 解释为什么，以及怎么绕过去。
3. **持久化证明**：`metric.alert.get` 显示 `enabled:true` + 真实阈值；`metric.alert.logs` 里能看到规则证明那一次的 `TRIGGERED` 记录。**这条不是第二次 `triggered:true`**——真实阈值上线后，只有市场真的跨过阈值那天才会再触发一次；在那之前，"持久化证明"就是收尾的全部内容，别让用户干等一条不会来的消息。

---

## 2. 开始之前

四个前置条件，一次性检查完，不是每次调用前的仪式：

1. **一个 Bearer Token**（`Authorization: Bearer lgatk_...`），环境变量 `LG_AGENT_TOKEN`。
2. **Token 上有 `realtime-alerting` preset**——去 `/profile/tokens` 创建/编辑 Token 时勾选这个 preset（对应 18 个 scope，见 [§7](#7-本包-20-个-skill-速查)）。
3. **至少一个可见的数据资产**——本包不做资产接入；[§3 步骤 1](#3-完整流程11-步) 会检查，没有就 ⛔ STOP。
4. **一个 WEBHOOK 数据源，或一个能贴的 webhook URL**（飞书群机器人 / 微信群机器人 / 通用 webhook 均可）——没有就在 [§3 步骤 3](#3-完整流程11-步) 用 `alert.channel.create` 建一个。

⛔ **STOP — 缺 scope**：如果任何调用返回 `403` 且 `message` 提到 `scope_insufficient` / 类似字样，不要猜测原因、不要重试——直接告诉用户：*"你的 Token 缺 `realtime-alerting` 这套权限，去 `/profile/tokens` 给这个 Token 补上 `realtime-alerting` preset（或者新建一个带这个 preset 的 Token）。"* 只在这时才调 `auth.token.introspect`（`GET /api/public/agent/token-introspect`，无参数）确认到底缺哪个 scope——它是 403 的诊断工具，不是每次调用前都要跑的仪式。

---

## 3. 完整流程（11 步）

贯穿全程的例子：贵州茅台（`stock_num=600519`），资产 `stock_day`（`assetId=1`），字段 `close_price`，用户想要的规则是**跌破 1500 通知我**。

### 步骤 1 — 确认资产可见

```bash
scripts/lg_agent_exec.sh dataasset.list
```

在返回的 `data[]` 里找目标资产（按 `assetName` 匹配，如 `stock_day`）。

⛔ **STOP — 无资产**：如果 `data` 是空数组，或者用户要的资产根本不在列表里——不要猜一个 `assetId` 硬调后面的步骤（会拿到 403 或者规则挂在错误资产上）。直接告诉用户：*"你还没有可用的数据资产，去 `/marketplace` 订阅一个（或者用 `privora-cn-quant` 里的资产接入流程）。"* 到此为止，不要往下走。

### 步骤 2 — 确认要监控的字段真实存在

```bash
scripts/lg_agent_exec.sh dataasset.schema.get id=1
```

在返回的列清单里确认 `close_price` 存在、类型是数值。**字段名拼错（如 `closePrice` / `close`）不会在这一步报错，但会在 [步骤 6](#步骤-6--用真实当前值推一个必然越线的占位阈值) 或规则创建后的评估里安静地查不到值**——现在核对一次比事后排查便宜。

### 步骤 3 — 确定通知渠道

```bash
scripts/lg_agent_exec.sh datasource.list dsType=WEBHOOK
```

`data[]` 非空 → 挑一个 `dsName`，跳到步骤 5。**没有** → 建一个：

```bash
scripts/lg_agent_exec.sh alert.channel.create label=茅台告警群 url=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx platform=FEISHU
```

`{"success":true,"dsName":"webhook_a1b2c3","label":"茅台告警群","platform":"FEISHU","host":"open.feishu.cn"}`

记住这里的 `dsName`（**不是** `label`，下面所有地方都要用 `dsName`）。`url` 不在允许的主机列表里、或明显不安全，会直接 `success:false` 拒绝创建——换一个真实的群机器人 webhook 地址重试。

### 步骤 4 — 渠道证明（在规则存在之前）

```bash
scripts/lg_agent_exec.sh plugin.webhook.send dataSourceName=webhook_a1b2c3 text="Privora 渠道测试：能看到这条就说明配置对了"
```

**失败注意**：这个接口失败时返回 **HTTP 502**（不是常见的 `200 + success:false`），`message` 是上游错误、`response` 是原始响应体——多半是 URL 已失效或签名密钥（`signToken`）配错，回步骤 3 重新建渠道。

成功后**必须让用户确认**在对应的群里真的看到了这条消息——`success:true` 只代表 Privora 把请求发出去了，不代表群机器人真的推送成功（比如群机器人被移出群、URL 指向了别的群）。这是三重证明的第一重。

### 步骤 5 — 读当前值

```bash
scripts/lg_agent_exec.sh dataasset.data.get id=1 filter_column=stock_num filter_value=600519 order_by=day_id order_direction=desc size=1
```

`{"success":true,"data":[{"day_id":"20260807","stock_num":"600519","close_price":"1568.00"}],"totalElements":1}`

当前 `close_price=1568.00`，用户要的规则是"跌破 1500"（`operator=LT threshold=1500`）——**此刻不会触发**，这正是前瞻式告警的常态，也是接下来两步要绕开的问题。

### 步骤 6 — 用真实当前值推一个必然越线的占位阈值

`metric.alert.test` 会跳过 disabled / snooze / silence / rate-limit / staleness / dedup 六道闸门（[§5](#5-为什么它没响--六道闸门)），**但绕不开比较本身**——阈值仍然是 1500，价格仍然是 1568，`LT` 判定仍然是 false。这意味着**在用户的真实阈值上，`metric.alert.test` 天然拿不到 `triggered:true`**，前瞻式告警的"验证它确实会响"这件事没法在真实阈值上完成。

解法：不改变 `operator`，改一个**当前必然为真**的占位阈值。价格 1568、操作符 `LT`，就选一个明显更大的数字，比如 `9999999`——`close_price < 9999999` 现在肯定是 true。用 `metric.alert.evaluate-now` 先干跑一遍确认：

```bash
scripts/lg_agent_exec.sh metric.alert.evaluate-now assetId:=1 fieldName=close_price operator=LT threshold=9999999 filterCondition="stock_num='600519'" messageTemplate='${ruleName}：${fieldName}=${value}，阈值 ${threshold}（${operator}）'
```

`{"success":true,"threshold":"9999999","operator":"LT","wouldTrigger":true,"currentValue":"1568.00","previewMessage":"undefined：close_price=1568.00，阈值 9999999（LT）"}`

`wouldTrigger:true` 且有 `previewMessage`——SQL、字段、filter 都对得上。（`ruleName` 这一步还没值，渲染成 `undefined` 是预期的——规则还没创建，下一步会带上真实 `ruleName`。）

⚠️ **反直觉提醒——这一步的通过不能保证下一步会成功**：`metric.alert.evaluate-now` 只是试跑，**不执行**下一步 `metric.alert.create` 落库时才会做的"多实体资产必须有 filterCondition/scope"校验（见步骤 7）。也就是说，对某些资产，哪怕漏填 `filterCondition`，`evaluate-now` 也可能照样返回 `wouldTrigger:true`——干跑通过只证明 SQL/字段对得上，**不等于** `create` 会接受同一份参数去落库。别把这一步的绿灯当成"配置一定能建成功"的证明。

### 步骤 7 — 建规则，但先不上线（`enabled:false`）

⚠️ **`filterCondition` 对多实体资产是必填，不是可选**——schema 上标的是 `required:false`，但如果目标资产是"一行一个标的/账户"（比如本例的 `stock_day`，一张表混着全市场股票），漏填 `filterCondition`（且没传 `scopeFilters`）会被后端判定为"这条规则会不分青红皂白地评估任意一行"，直接拒绝创建，返回 **HTTP 400**：

> `Validation Failed: this asset holds multiple entities (e.g. one row per instrument/account) — or its schema could not be verified — and no scope was set, so the rule could evaluate one arbitrary row. Add a scope filter, or resubmit with confirmWholeTable=true to alert on the whole table intentionally.`

照抄本文档示例不会撞上这个 400（示例的 `filterCondition="stock_num='600519'"` 全程都在），但**换成用户的另一个资产、且忘记带上等价的 filterCondition 时会**——这是本包最常见的真实失效点。撞上后按这个恢复路径重试，不要猜列名：

1. `dataasset.schema.get id=<assetId>`——从列清单里找出能唯一定位一行的实体列（如 `stock_num` / `account_id`）。
2. `dataasset.data.get id=<assetId> size=1`（可加排序/过滤）——读一个该列的真实值。
3. 把 `filterCondition` 拼成 `"<实体列>='<真实值>'"`（字符串值记得加引号，见 §8）再重试 `metric.alert.create`。

（文案里提到的 `confirmWholeTable=true` 是另一条路——故意放弃按行区分、把整张表当一个整体评估——但那不是本包的场景：本包永远是"某一个标的/账户"的告警，该用 `filterCondition`，不要用 `confirmWholeTable` 图省事。）

```bash
scripts/lg_agent_exec.sh metric.alert.create ruleName=茅台跌破1500 assetId:=1 fieldName=close_price operator=LT threshold=9999999 filterCondition="stock_num='600519'" webhookDsName=webhook_a1b2c3 messageTemplate='${ruleName}：${fieldName}=${value}，阈值 ${threshold}（${operator}）' enabled:=false
```

`{"success":true,"data":{"ruleCode":"a1b2c3d4e5f6...","ruleName":"茅台跌破1500","enabled":false,"threshold":"9999999","operator":"LT"},"message":""}`

记住 `ruleCode`。**`enabled:=false` 是这一步的核心**——占位阈值现在已经落库了，平台的后台评估进程（[§6](#6-上线后由平台自动评估)）随时可能扫到这条规则；如果规则是启用状态，占位阈值会被当成真规则触发一次误报。`enabled:false` 让这条规则在阈值改对之前对平台"不可见"。

**绝不可以跳过 `enabled:=false` 直接用真实阈值创建再改**——先建后改中间那段时间，同样会被平台扫到并可能误报，这不是"更简单的写法"，是同一个坑换了个位置。

### 步骤 8 — 规则证明：`metric.alert.test`

```bash
scripts/lg_agent_exec.sh metric.alert.test ruleCode=a1b2c3d4e5f6...
```

`{"success":true,"threshold":"9999999","operator":"LT","triggered":true,"currentValue":"1568.00","message":"茅台跌破1500：close_price=1568.00，阈值 9999999（LT）","webhookSent":true}`

`triggered:true` + `webhookSent:true`——这是三重证明的第二重。这一步发的是**真实 webhook**（步骤 4 用的同一个 `dsName`），去群里确认收到了这条消息，消息内容应该跟这次响应的 `message` 一致。**`isTest` 不会写 `lastTriggeredAt` / `firesToday`，不占用户真规则的静默期/频次配额**——这条测试消息不影响真实阈值上线后的第一次统计。

### 步骤 9 — 改成用户的真实阈值

```bash
scripts/lg_agent_exec.sh metric.alert.patch ruleCode=a1b2c3d4e5f6... threshold=1500
```

`{"success":true,"message":"Alert rule patched","ruleCode":"a1b2c3d4e5f6..."}`

`metric.alert.patch` 是字段掩码——只有 `threshold` / `webhookDsName` / `messageTemplate` / `templateEngine` 四个字段可改，`enabled` 传了会被拒绝（`FIELD_NOT_PATCHABLE`），这是设计如此：改 `enabled` 只能走下一步的 `metric.alert.toggle`，两件事故意分开，避免一次调用同时改了"规则内容"和"是否上线"。

**这一步之后、下一步之前，规则仍然是 `enabled:false`**——阈值已经是真的了，但还没上线，平台评估进程还是看不到它。

### 步骤 10 — 上线

> **步骤 9 必须先于步骤 10 完成。** 反过来先 `toggle` 再 `patch`，会打开一段"规则以占位阈值 `9999999` 武装"的窗口——proc 3196 可能在真实阈值落地前扫到这条规则并按占位阈值触发一次误报。这跟步骤 7 警告的"先建成 armed 再改阈值"是同一个坑换了个位置，不是更简单的写法。**不确定这条规则是否已经 patch 过，先 `metric.alert.get` 看一眼 `threshold`，确认它已经是用户的真实阈值（不是占位值），再决定要不要调 `toggle`。**

```bash
scripts/lg_agent_exec.sh metric.alert.toggle ruleCode=a1b2c3d4e5f6...
```

`{"success":true,"data":{"ruleCode":"a1b2c3d4e5f6...","enabled":true,"threshold":"1500"},"message":""}`

**`toggle` 是翻转（flip），不是"设为 true"**——它把当前的 `enabled` 状态反过来。这条规则此刻是 `false`，翻转一次变 `true`，正确。**如果因为超时/重试对同一条规则多调了一次 `toggle`，会把它翻回 `false`，且不会报错**——不要在没有确认当前状态的情况下重试 `toggle`；不确定就用下一步的 `metric.alert.get` 先看一眼再决定要不要调。

### 步骤 11 — 持久化证明

```bash
scripts/lg_agent_exec.sh metric.alert.get ruleCode=a1b2c3d4e5f6...
scripts/lg_agent_exec.sh metric.alert.logs ruleCode=a1b2c3d4e5f6... limit:=5
```

`metric.alert.get` 应显示 `enabled:true` 且 `threshold:"1500"`；`metric.alert.logs` 里应该能看到步骤 8 那次 `TRIGGERED` 记录（`isTest:true`）。**到这里就是配置完成——不要再等一次 `triggered:true` 才敢跟用户说配完了**。真实阈值是 1500、现价是 1568，规则现在是"武装但还没触发"的正常状态；只有市场真的跌破 1500 那天，用户才会收到第一条真实通知。跟用户说清楚这一点，否则他们会以为配置失败。

---

## 4. 分支决策表

| 场景 | 怎么处理 |
|---|---|
| `dataasset.list` 返回空 | ⛔ STOP，指向 `/marketplace`（步骤 1） |
| 403 + scope 相关 message | ⛔ STOP，指向 `/profile/tokens` 补 `realtime-alerting`（§2） |
| 已有 WEBHOOK 数据源 | 跳过 `alert.channel.create`，直接用现成 `dsName`（步骤 3） |
| 用户阈值方向是"跌破"（LT/LTE） | 占位阈值取一个明显**大于**当前值的数字（步骤 6） |
| 用户阈值方向是"突破"（GT/GTE） | 占位阈值取一个明显**小于**当前值的数字，其余流程不变 |
| 用户阈值方向是"等于"（EQ） | 大数占位法在这里**不成立**——`field EQ 9999999` 平凡为假，不是平凡为真。占位阈值必须直接取步骤 5 读到的**当前值原样字符串**（如 `1568.00`）：**不要重新格式化数字、不要补零或去零**，字符串要跟响应里的 `close_price` 值逐字节一致，否则在非数值字段上会落到后端的字符串精确比较分支而判不等 |
| 用户阈值方向是"不等于"（NEQ） | 跟 LT/GT 一样用大数占位法（如 `9999999`）即可——只要保证明显不等于当前值，`field NEQ 9999999` 就是平凡为真 |
| 当前值恰好已经在用户阈值的"触发侧" | 仍然按 6-10 步走一遍——不要因为"反正现在就该触发"而用真实阈值直接建成 `enabled:true`，误报窗口的风险不看阈值"看起来"是否安全 |
| `metric.alert.test` 返回 `triggered:false` | 检查 `filterCondition` 是否正确限定了这一行——`stock_day` 是多股票合表，忘记 filter 会聚合到别的行 |
| `webhookSent:false` | 这是发送失败，不是评估被跳过；`webhookError` / HTTP 502 的 `response` 里有上游原文，见 [§8](#8-已知坑) |
| `metric.alert.create`（或 `update`）返回 400，`message` 含 `"this asset holds multiple entities"` | 资产是多实体资产，漏填了 `filterCondition`——见[步骤 7](#步骤-7--建规则但先不上线enabledfalse)的恢复路径：`dataasset.schema.get` 找实体列 → `dataasset.data.get size=1` 读真实值 → 拼 `filterCondition="<列>='<值>'"` 重试。**别用文案里提到的 `confirmWholeTable=true`**——那是故意放弃按行区分，不是本包场景。**`metric.alert.evaluate-now` 对同一份配置试跑不会拦这个**，干跑绿灯不代表 `create` 会接受 |

---

## 5. 为什么它没响 —— 六道闸门

规则上线后"为什么没通知我"是这个场景最常见的追问。下面六道闸门**都是设计，不是故障**——评估按顺序检查，第一个命中就跳过（不发 webhook）。诊断都用 `metric.alert.get`（看规则当前状态）+ `metric.alert.logs`（看最近几次评估的 `status` / `errorMessage`）。

| 闸门 | 症状 | 诊断 | 修法 |
|---|---|---|---|
| **disabled** | 规则存在，从来没触发过 | `metric.alert.get` 的 `enabled` 是 `false` | `metric.alert.toggle`（先确认当前是 `false` 再调，见步骤 10 的翻转警告） |
| **snooze** | 之前触发过，突然安静了 | `metric.alert.get` 的 `snoozedUntil` 是未来时间 | 等它过期自动恢复，或 `metric.alert.unsnooze` 立即恢复 |
| **silenceMinutes** | 刚触发过一次，短时间内又该触发却没发 | `metric.alert.logs` 最近一条 `SKIPPED`，`errorMessage` 类似 `in silence period` | 默认 60 分钟，防轰炸设计；等静默期过去，或建规则时把 `silenceMinutes` 调小 |
| **maxFiresPerDay** | 当天已经收到好几条，之后不再收到 | `metric.alert.logs` 当天最后一条 `SKIPPED`，`errorMessage` 类似 `daily limit reached` | 默认每天 10 次，隔天自动重置；或建规则时调大 `maxFiresPerDay` |
| **maxStaleSeconds（数据太旧）** | `enabled:true`、阈值也对，但从不触发 | `metric.alert.logs` 出现 `SKIPPED_STALE`，`errorMessage` 带 `last_data_refresh_at=... 秒前, threshold=...秒`（日线资产是 `grain=DAILY, deadline=...`） | **不传 `maxStaleSeconds` 时平台按资产粒度推导**：日线资产（`latest_partition_value` 是 8 位 yyyyMMdd）按交易日历判断，漏掉一整个交易日的预期落地才算过期，周末和长假不会误跳（2027 年起在补录节假日数据前除外）；其他资产仍是系统默认 1800 秒（30 分钟）。显式传 `maxStaleSeconds` 永远优先，但它是固定秒数，表达不了周末和长假——日线资产**别传** `90000` 之类的值。`metric.alert.evaluate-now` 的返回里有 `freshness.wouldBeSkippedStale`，能提前告诉你真评估会不会被跳过；**该字段缺失表示无法判断（资产不可见、探针无结果或出错），不表示数据新鲜** |
| **数据去重（dedup）** | 数据没变时没有重复通知，看起来像"漏评估" | `metric.alert.logs` 连续 `SKIPPED`，`errorMessage` 是 `data freshness unchanged since last evaluation` | 设计如此：`last_data_refresh_at` 跟上次记录值逐字节相同就跳过，日批资产因此**每次 ETL 更新最多评估一次，不是每次平台轮询都评估一次**——数据没动就不用再算一遍 |

`metric.alert.test`（步骤 8）会跳过以上全部六道闸门（包括 staleness 和 dedup）——规则证明这一步永远能拿到真实结果，但也意味着"测试能过"不代表"上线后一定按时响"，闸门要单独核对。

---

## 6. 上线后由平台自动评估

规则上线（`enabled:true`）之后，评估不需要你、也不需要 Agent 去发起——平台有一个后台进程（`metric_alert_poll`，process 3196）会定期自动扫描所有启用的规则并调用跟生产评估一样的逻辑（同样过 [§5](#5-为什么它没响--六道闸门) 的六道闸门）。**本文档不写具体的轮询周期**——那个数字没有经过实测确认，写一个可能过期或错误的数字，比不写更危险。你不需要、也不应该自己搭一个循环去反复触发评估模拟"实时监控"——那是平台已经在做的事，重复做只会消耗 `maxFiresPerDay` 配额、可能撞上静默期。

---

## 7. 本包 20 个 skill 速查

`realtime-alerting` preset 授予 18 个 scope；其中两个 scope 各多解锁一个 skillId（`metric.alert.list` 额外解锁 `metric.alert.logs`，`metric.alert.test` 额外解锁 `metric.alert.evaluate-now`），所以总共可调用 **20 个 skillId**。**不含任何 `delete`**（也不含 `metric.alert.evaluate` / `metric.alert.system.evaluate`——那两个是生产级"立即真实评估"，留给平台自己的后台进程，本包不需要也不授予）。

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `dataasset.list` | GET | 列出可见数据资产 | 🟢 |
| `dataasset.get` | GET | 获取资产详情 | 🟢 |
| `dataasset.schema.get` | GET | 获取资产 schema（核对字段名） | 🟢 |
| `dataasset.metadata.get` | GET | 获取资产新鲜度等富元数据 | 🟢 |
| `dataasset.data.get` | GET | 查资产数据（读当前值） | 🟢 |
| `datasource.list` | GET | 列出数据源（`dsType=WEBHOOK` 找通知渠道） | 🟢 |
| `alert.channel.create` | POST | 创建一个 WEBHOOK 通知渠道 | 🔴 |
| `plugin.webhook.send` | POST | 手动发一条 webhook（渠道测试） | 🟡 |
| `metric.alert.list` | GET | 列出告警规则 | 🟢 |
| `metric.alert.get` | GET | 获取单条规则详情（持久化证明） | 🟢 |
| `metric.alert.logs` | GET | 拉取规则的评估历史（持久化证明） | 🟢 |
| `metric.alert.create` | POST | 创建规则（配 `enabled:false` 建占位规则） | 🟡 |
| `metric.alert.update` | PUT | 全量替换规则（一般用 `patch` 就够） | 🟡 |
| `metric.alert.patch` | PATCH | 部分更新（改真实阈值/渠道/模板） | 🟡 |
| `metric.alert.toggle` | PUT | 翻转启用状态（上线用这个） | 🟡 |
| `metric.alert.test` | POST | 手动测一次（真实 webhook，跳过六道闸门） | 🟡 |
| `metric.alert.evaluate-now` | POST | 对未落库的规则配置试跑（不落库不发信） | 🟡 |
| `metric.alert.snooze` | PUT | 暂停到指定时间 | 🟡 |
| `metric.alert.unsnooze` | PUT | 取消暂停 | 🟡 |
| `metric.alert.acknowledge` | PUT | 标记"已知晓"（v1 仅记录，不影响后续评估） | 🟢 |

---

## 8. 已知坑

- **`metric.alert.toggle` 是翻转不是置位**——见步骤 10。重试前先 `metric.alert.get` 确认当前状态。
- **`webhookDsName` ≠ 渠道的 `label`**——`alert.channel.create` 返回的是服务端生成的 `dsName`（如 `webhook_a1b2c3`），后续所有地方（`plugin.webhook.send` 的 `dataSourceName`、`metric.alert.create`/`patch` 的 `webhookDsName`）都要用这个值，不是你传的 `label`。
- **`previewMessage` 只在 `wouldTrigger:true` 且 `messageTemplate` 非空时才会出现**——`wouldTrigger:false` 时响应里根本没有这个 key，不是空字符串。
- **`metric.alert.patch` 严格拒绝 `enabled` / `ruleCode` / `fieldName` / `assetId`**——传了直接 `success:false, code:"FIELD_NOT_PATCHABLE"`，且**一个字段都不会被改**（不是"跳过非法字段，其余照常"）。只改得动 `threshold` / `webhookDsName` / `messageTemplate` / `templateEngine`。
- **`plugin.webhook.send` 失败时 HTTP 状态码是 502，不是 200**——跟本包其它接口"200 + success:false"的约定不一样，只检查状态码会把它误判成"网络/平台故障"而不是"webhook 配置错误"。
- **`filterCondition` 是原始 SQL `WHERE` 片段**——字符串字面量要自己加引号（`stock_num='600519'`，不是 `stock_num=600519`），漏引号会被当成列名解析报 SQL 错误，不是"过滤不生效"这么温和。
- **`stock_day` 是合表**——同一张表混着 A 股全部股票的行，忘记用 `filterCondition` 限定 `stock_num`，`LATEST` 聚合会去抓"任意"一行的最新数据，不会报错，只会给你一个看似合理但对不上的值。
- **`filterCondition` 对多实体资产是隐性必填**——schema 标 `required:false`，但资产是"一行一个标的/账户"时漏填会在 `metric.alert.create`/`update` 落库时被 400 拒绝（`message` 含 `this asset holds multiple entities`），且 **`metric.alert.evaluate-now` 不执行这道校验**——干跑 `wouldTrigger:true` 不代表 `create` 会接受同样的参数。400 文案与恢复路径见[步骤 7](#步骤-7--建规则但先不上线enabledfalse)。

---

## 9. 安全与责任

- **Webhook 是站外副作用，平台不可撤销**——一旦触发，消息已经发到飞书/微信群里了，没有"撤回"操作。步骤 4/8 都会真实发消息，测试前告知会收到消息的人。
- **本包不含任何删除类操作**——想让规则"消失"用 `snooze`（临时）或 `toggle` 关闭（长期），管理员才能真正删除。
- **告警评估结果是供人审查的信号，不是投资建议**——跌破/突破阈值只是数值比较，不代表买卖判断。
- **最小化授权**——`realtime-alerting` 这 18 个 scope 是本场景刚好够用的集合；渠道已经建好时，不需要额外保留 `alert.channel.create`。
- **本包脚本额外做了一层客户端拒绝**——`scripts/lg_agent_exec.sh` 在打包时会生成一份从 `realtime-alerting` preset 派生的 skill 白名单，调用表外的 skillId 会被本地直接拒绝。这是打包诚实性检查，**不是安全边界**——本地可被编辑/删除绕过，真正且唯一不可绕过的授权判定始终在服务端 scope 校验。
- 想要行情 / 回测 / 模拟交易 / 流程编排等本包之外的能力，去装完整版 [`privora-cn-quant`](https://clawhub.ai/guangfuwu/privora-cn-quant)，不要为了这些能力给这个 Token 加签额外 scope——按场景拆分的 Token 更容易审计谁能做什么。
