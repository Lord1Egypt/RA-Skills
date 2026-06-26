---
name: kuaidi100-logistics
description: 快递100 API 技能，用于查询快递物流相关信息。当用户提到快递单号、物流轨迹、查快递、运费估算、预计到达时间、识别快递公司等需求时，必须使用此技能。支持：查询物流轨迹（query_trace）、识别快递公司（auto_number）、估算运费（estimate_price）、预估寄件送达时间（estimate_time）、预估在途快递送达时间（estimate_time_with_logistic）。即使用户只是随口提到"我的快递到哪了"、"这个单号是什么快递"等，也要主动触发此技能。
---

# 快递100 API 技能

通过 curl 调用快递100 API 接口，实现快递物流查询相关功能。

## 环境变量

- `KUAIDI100_API_KEY`：快递100 API Key（可选，未设置时使用免费额度）

## API 基础地址

```
https://api.kuaidi100.com/stdio
```

## Key 处理规则

- 若环境变量 `KUAIDI100_API_KEY` 已设置且不为空，则使用该值作为 `key` 参数
- 否则将 `key` 参数设为 `null`（字符串）

```bash
KEY="${KUAIDI100_API_KEY:-null}"
```

## 额度耗尽处理

若接口返回内容包含"免费调用额度已耗尽"、"今日免费"、"额度不足"等字样，需告知用户：

> 今日免费调用额度已耗尽。您可前往 [快递100 API 开放平台](https://api.kuaidi100.com) 注册账号并获取专属 API Key，然后将 Key 更新到环境变量 `KUAIDI100_API_KEY` 中即可继续使用。

---

## 工具列表

### 1. query_trace — 查询快递物流轨迹

**触发场景**：用户询问某快递单号的物流状态、快递到哪了、轨迹查询等。

**参数**：
- `kuaidiNum`（必填）：快递单号
- `phone`（可选）：手机号，顺丰速运、顺丰快运、中通快递必填

**curl 调用**：
```bash
KEY="${KUAIDI100_API_KEY:-null}"
RESULT=$(curl -s "https://api.kuaidi100.com/stdio/queryTrace?key=${KEY}&kuaidiNum=${快递单号}&phone=${手机号}")
echo "$RESULT"
```

> 若手机号为空则省略 `phone` 参数：
> ```bash
> RESULT=$(curl -s "https://api.kuaidi100.com/stdio/queryTrace?key=${KEY}&kuaidiNum=${快递单号}")
> ```

---

### 2. auto_number — 识别快递公司

**触发场景**：用户想知道某快递单号属于哪家快递公司，或需要在调用其他接口前识别快递公司编码。

**参数**：
- `kuaidiNum`（必填）：快递单号

**curl 调用**：
```bash
KEY="${KUAIDI100_API_KEY:-null}"
RESULT=$(curl -s "https://api.kuaidi100.com/stdio/autoNumber?key=${KEY}&kuaidiNum=${快递单号}")
echo "$RESULT"
```

---

### 3. estimate_price — 估算运费

**触发场景**：用户询问从某地寄快递到某地的费用、运费是多少等。

**参数**：
- `kuaidicom`（必填）：快递公司编码（小写），支持：
  - 顺丰：`shunfeng`
  - 京东：`jd`
  - 德邦快递：`debangkuaidi`
  - 圆通：`yuantong`
  - 中通：`zhongtong`
  - 申通：`shentong`
  - 韵达：`yunda`
  - EMS：`ems`
- `recAddr`（必填）：收件地址，如 `广东深圳南山区`
- `sendAddr`（必填）：寄件地址，如 `北京海淀区`
- `weight`（必填）：重量（kg，不带单位），默认 `1`

**curl 调用**：
```bash
KEY="${KUAIDI100_API_KEY:-null}"
RESULT=$(curl -s --get "https://api.kuaidi100.com/stdio/estimatePrice" \
  --data-urlencode "key=${KEY}" \
  --data-urlencode "kuaidicom=${快递公司编码}" \
  --data-urlencode "recAddr=${收件地址}" \
  --data-urlencode "sendAddr=${寄件地址}" \
  --data-urlencode "weight=${重量}")
echo "$RESULT"
```

---

### 4. estimate_time — 预估寄件送达时间

**触发场景**：用户寄件前询问预计几天到、送达时间等（尚未寄出，无物流轨迹）。

**参数**：
- `kuaidicom`（必填）：快递公司编码（小写），支持：
  圆通`yuantong`、中通`zhongtong`、顺丰`shunfeng`、顺丰快运`shunfengkuaiyun`、京东`jd`、极兔速递`jtexpress`、申通`shentong`、韵达`yunda`、EMS`ems`、跨越`kuayue`、德邦快递`debangkuaidi`、EMS-国际件`emsguoji`、邮政国内`youzhengguonei`、国际包裹`youzhengguoji`、宅急送`zhaijisong`、芝麻开门`zhimakaimen`、联邦快递`lianbangkuaidi`、天地华宇`tiandihuayu`、安能快运`annengwuliu`、京广速递`jinguangsudikuaijian`、加运美`jiayunmeiwuliu`
- `from`（必填）：出发地，如 `广东省深圳市南山区`
- `to`（必填）：目的地，如 `北京市海淀区`
- `orderTime`（可选）：下单时间，格式 `yyyy-MM-dd HH:mm:ss`，默认当前时间
- `expType`（可选）：业务/产品类型，如 `标准快递`

**curl 调用**：
```bash
KEY="${KUAIDI100_API_KEY:-null}"
RESULT=$(curl -s --get "https://api.kuaidi100.com/stdio/estimateTime" \
  --data-urlencode "key=${KEY}" \
  --data-urlencode "kuaidicom=${快递公司编码}" \
  --data-urlencode "from=${出发地}" \
  --data-urlencode "to=${目的地}")
echo "$RESULT"
```

> 若需传 `orderTime` 或 `expType`，追加对应 `--data-urlencode` 参数即可。

---

### 5. estimate_time_with_logistic — 预估在途快递送达时间

**触发场景**：用户查询了物流轨迹（query_trace）后，询问还需多久到达、预计几号能到等，通常在 `query_trace` 之后调用。

**参数**：
- `kuaidicom`（必填）：快递公司编码（同 estimate_time，见上方支持列表）
- `from`（必填）：出发地，如 `广东省深圳市南山区`
- `to`（必填）：目的地，如 `北京市海淀区`
- `orderTime`（必填）：取 query_trace 返回的**最早**物流轨迹时间，格式 `yyyy-MM-dd HH:mm:ss`
- `logistic`（必填）：历史物流轨迹 JSON 数组，取自 query_trace 返回数据，格式：
  ```json
  [{"time":"2025-12-29 12:43:35","context":"您的快件已到达快递驿站，请及时取件","status":"投柜或驿站"},{"time":"2025-12-29 08:48:27","context":"【河北省承德市隆化县】的郭工正在派件","status":"派件"}]
  ```

**curl 调用**：
```bash
KEY="${KUAIDI100_API_KEY:-null}"
RESULT=$(curl -s --get "https://api.kuaidi100.com/stdio/estimateTime" \
  --data-urlencode "key=${KEY}" \
  --data-urlencode "kuaidicom=${快递公司编码}" \
  --data-urlencode "from=${出发地}" \
  --data-urlencode "to=${目的地}" \
  --data-urlencode "orderTime=${下单时间}" \
  --data-urlencode "logistic=${物流轨迹JSON}")
echo "$RESULT"
```

---

## 结果处理

所有接口均直接返回 Markdown 格式内容，**无需额外处理，直接将结果返回给用户即可**。

## 典型调用流程

```
用户询问快递还需多久到
  → 1. query_trace 查询物流轨迹（获取快递公司、轨迹数据）
  → 2. estimate_time_with_logistic 预估剩余时间（携带轨迹数据）
  → 返回结果给用户
```