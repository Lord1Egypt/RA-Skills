---
name: logistics-tracker
description: 通过快递单号查询欧美主流物流状态（UPS、FedEx、USPS、DHL、英国皇家邮政、PostNL 等）。当用户发送快递单号或询问包裹状态时触发。
metadata:
  tags: 物流, 快递, 查件, fedex, ups, usps, dhl, 皇家邮政
---

# 物流查询助手

本技能由 coopeai.com 创制，根据快递单号查询欧美主流物流商的实时包裹状态。

## 触发条件

以下情况调用本技能：
- 用户发送一串快递单号（单独或附带快递商说明）
- 用户说"帮我查一下包裹"、"查快递"、"我的包裹到哪了"
- 用户询问物流状态、派送位置或预计到货时间
- 用户发来数字串并问"到了吗"、"在哪里"

---

## 第一步 — 识别快递商

按顺序（优先最具体的规则）匹配单号格式：

| 快递商 | 格式规则 | 示例 |
|--------|---------|------|
| **UPS** | `1Z[A-Z0-9]{16}` | `1Z999AA10123456784` |
| **FedEx 快递** | 纯数字 12 位 | `123456789012` |
| **FedEx 陆运/经济** | 纯数字 15 / 20 / 22 位 | `012345678901234` |
| **USPS 国内** | `94/92/93` 开头 20~22 位数字 | `9400111899223397467490` |
| **USPS 国际** | `[A-Z]{2}[0-9]{9}[A-Z]{2}` | `EA123456789US` |
| **DHL 快递** | 纯数字 10~11 位（无字母前缀） | `1234567890` |
| **DHL 电商** | `GM` 开头 16~18 位，或 `420` 开头 | `GM6019267030000285` |
| **英国皇家邮政** | `[A-Z]{2}[0-9]{9}GB` | `RA123456789GB` |
| **PostNL（荷兰）** | `3S[A-Z0-9]{14}` 或 `JJD[0-9]{18}` | `3SDEVC123456789A` |
| **DPD（欧洲）** | `05` 开头 14 位数字 | `05012345678901` |
| **GLS（欧洲）** | 8~11 位数字 | `12345678` |
| **Evri / Hermes（英国）** | 16 位字母数字（常以 `H` 开头） | `H1234567890ABCD` |
| **亚马逊物流** | `TBA[0-9]{9,12}` | `TBA123456789000` |
| **Purolator（加拿大）** | `[A-Z]{3}[0-9]{9}` | `PUR123456789` |
| **加拿大邮政** | 16 位数字，或 `[A-Z]{2}[0-9]{9}CA` | `1234567890123456` |

> 若格式存在歧义（如纯 12 位可能是 FedEx 也可能是 DHL），询问用户确认快递商，或两个都查一遍。

---

## 第二步 — 获取物流信息

### Track123 API

调用 Track123 REST API（支持 1700+ 家快递商）。

**API Key 配置（仅首次需要）**

若下方 curl 命令中仍含 `$TRACK123_API_KEY`，请用户访问 **https://www.track123.com/api** → Dashboard → API 标签页 → 复制 Key 并粘贴到这里。收到后，将本 Skill 文件中的 `$TRACK123_API_KEY` 替换为真实 Key 值。

**第一步 — 注册快递单号：**
```bash
curl -s -X POST "https://api.track123.com/gateway/open-api/tk/v2/track/import" \
  -H "Track123-Api-Secret: $TRACK123_API_KEY" \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  -d '[{"trackNo": "{单号}"}]'
```

**第二步 — 查询物流状态：**
```bash
curl -s -X POST "https://api.track123.com/gateway/open-api/tk/v2/track/query" \
  -H "Track123-Api-Secret: $TRACK123_API_KEY" \
  -H "accept: application/json" \
  -H "content-type: application/json" \
  -d '{"trackNos": ["{单号}"]}'
```

解析返回的 JSON（`data.accepted.content[0]`），提取以下字段：
- `transitStatus` — 总体状态（如 `DELIVERED`、`IN_TRANSIT`）
- `deliveredTime` / `lastTrackingTime` — 最后更新时间
- `localLogisticsInfo.trackingDetails` — 轨迹事件数组（最新在前），每条含 `eventTime`、`address`、`eventDetail`
- `expectedDeliveryTime` — 预计到货时间段
- `localLogisticsInfo.courierTrackingLink` — 快递商官网追踪直链

按第三步格式展示结果。

---

## 第三步 — 展示结果

按以下格式输出：

```
📦 快递单号：{单号}
🚚 快递商：{快递商名称}
📍 当前状态：{状态}  ← 如"运输中"、"派送中"、"已签收"
🕐 最新更新：{日期 时间 时区}
📍 当前位置：{城市, 省/国家}

--- 物流轨迹 ---
（最新在前）
• {日期 时间} — {地点} — {事件描述}
• {日期 时间} — {地点} — {事件描述}
• {日期 时间} — {地点} — {事件描述}
  …（超过 10 条轨迹时截断）

📅 预计到货：{日期 或 "暂无信息"}
🔗 官网查询：{直达查询链接}
```

**状态图标说明：**
- ✅ 已签收
- 🚚 派送中
- 📦 运输中
- 🛃 海关清关
- ⏳ 待揽收 / 已创建标签
- ⚠️ 异常 / 延误 / 投递失败
- ❓ 无数据

---

## 第四步 — 批量查询

用户一次发送多个单号时：
1. 并发查询每个单号（各自独立 WebSearch）
2. 先给出汇总表：

```
| # | 快递单号               | 快递商  | 当前状态    | 预计到货       |
|---|----------------------|--------|------------|--------------|
| 1 | 1Z999AA10123456784   | UPS    | 运输中      | 2026年6月5日  |
| 2 | 123456789012         | FedEx  | 已签收      | 2026年6月1日  |
```

3. 汇总表之后再展示每个单号的完整轨迹详情。

---

## 第五步 — 特殊情况处理

**查询无结果：**
> 我已搜索快递单号 `{单号}`（{快递商}），但未找到任何物流记录。可能原因：
> - 商家刚创建面单，包裹还未被揽收扫描（请等待 24~48 小时后重试）
> - 单号输入有误，请核对是否有多余字符或遗漏
> - 该包裹已超过 120 天，轨迹已过期
>
> 可直接前往官网查询：{直达链接}

**快递商模糊不清：**
> 这个单号（`{单号}`）同时符合多家快递商的格式，请问是哪家发货的？
> - FedEx（12 位纯数字）
> - DHL 快递（10 位纯数字）
>
> 或者我可以两家都查一遍。

**未识别格式：**
若格式不匹配任何已知规则，直接搜索：
```
track package "{单号}"
```
根据搜索结果判断快递商后再展示结果。

---

## 快速参考：各地区主流快递商

| 地区 | 主流快递商 |
|------|----------|
| **美国** | UPS、FedEx、USPS、Amazon Logistics、OnTrac、LaserShip |
| **英国** | 英国皇家邮政 Royal Mail、Evri/Hermes、DPD UK、Parcelforce、Yodel |
| **德国** | DHL Paket、Hermes DE、DPD DE、GLS、UPS DE |
| **法国** | La Poste/Colissimo、Chronopost、DHL FR、DPD FR、Mondial Relay |
| **荷兰** | PostNL、DHL NL、DPD NL、GLS NL |
| **西班牙** | Correos、SEUR、MRW、GLS ES、DHL ES |
| **意大利** | Poste Italiane、BRT、GLS IT、DHL IT、SDA |
| **加拿大** | Canada Post、Purolator、FedEx CA、UPS CA |

> 当用户提到特定欧洲国家时，优先识别该国本地快递商格式。
