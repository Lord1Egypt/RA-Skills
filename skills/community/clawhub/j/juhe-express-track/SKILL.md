---
name: juhe-express-track
description: 全球快递物流状态查询。输入快递单号，查询包裹的实时物流轨迹和当前状态，支持顺丰、圆通、申通、中通、韵达、京东、EMS、DHL、FedEx、UPS 等全球上千家快递公司。使用场景：用户说"帮我查一下这个快递到哪了"、"顺丰单号 SF1234567890 的物流"、"查快递 YT1234567890"、"我的包裹到了吗"、"京东快递查询"等。通过聚合数据（juhe.cn）API 实时查询，快递公司编号本地解析无需额外请求。
homepage: https://www.juhe.cn/docs/api/id/43
metadata: {"openclaw":{"emoji":"📦","requires":{"bins":["python3"],"env":["JUHE_EXPRESS_KEY"]},"primaryEnv":"JUHE_EXPRESS_KEY"}}
---

# 全球快递物流查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，支持全球上千家快递公司跟踪服务。

输入快递单号，查询包裹的**实时物流轨迹、当前状态、签收信息**。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [全球快递物流查询 API](https://www.juhe.cn/docs/api/id/43) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_EXPRESS_KEY=你的AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_EXPRESS_KEY=你的AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/express_track.py --key 你的AppKey 快递单号
```

---

## 使用方法

> **注意：`--com` 为必填参数**，接口不支持自动识别快递公司，必须提供快递公司编号。

### 基本查询

```bash
# 使用中文名称（脚本自动转换为编号后传给接口）
python scripts/express_track.py YT1234567890123 --com 圆通

# 使用快递公司编号（直接传给接口）
python scripts/express_track.py YT1234567890123 --com yt
```

输出示例：

```
📦 查询单号: YT1234567890123  快递公司: 圆通速递（yt）

────────────────────────────────────────────────────────
  🛵  圆通速递（yt）  单号: YT1234567890123
  状态: 派件中
────────────────────────────────────────────────────────
  ▶ 2026-03-24 09:30:00
      【上海市】您的快件已由快递员张三(18812345678)派出，请您注意查收

    2026-03-23 22:10:00
      【上海市】快件已到达 上海转运中心

    2026-03-23 10:05:00
      【北京市】快件已从 北京顺义分拨中心 发出
────────────────────────────────────────────────────────
```

### 需要手机号的快递（顺丰、中通、跨越等）

部分快递公司（目前包括顺丰、中通、跨越，未来可能增加）查询时需提供寄件人或收件人手机号后 4 位，二选一即可：

```bash
# 提供寄件人手机号后4位
python scripts/express_track.py SF1234567890 --com 顺丰 --sender-phone 1234

# 提供收件人手机号后4位
python scripts/express_track.py SF1234567890 --com 顺丰 --receiver-phone 5678
```

### 查看所有支持的快递公司

```bash
python scripts/express_track.py --list
```

### 搜索快递公司

```bash
python scripts/express_track.py --search 圆通
python scripts/express_track.py --search fedex
```

---

## 常用快递公司编号速查

| 快递公司 | 编号 | 快递公司 | 编号 |
|---------|------|---------|------|
| 顺丰 | sf | 圆通 | yt |
| 申通 | sto | 中通 | zto |
| 韵达 | yd | 京东快递 | jd |
| EMS | ems | EMS国际 | emsg |
| 德邦 | db | 宅急送 | zjs |
| DHL | dhl | FedEx国际 | fedex |
| UPS国际 | ups | 国通 | gt |
| 汇通（百世） | ht | 极兔速递 | jtsd |

> 完整列表（1000+ 家）请运行 `python scripts/express_track.py --list` 或查阅 `references/express-company-list.json`

---

## AI 使用指南

当用户询问快递物流信息时，按以下步骤操作：

1. **提取查询信息** — 从用户消息中识别快递单号和快递公司
2. **确认快递公司** — `--com` 为必填，接口不支持自动识别。若用户未提及公司，需询问用户；若用户提供了名称，读取本地 `references/express-company-list.json` 查找对应编号（无需联网）
3. **处理手机尾号** — 顺丰（sf）、中通（zto）、跨越（kye）等快递需提供手机号后4位，询问用户选择提供寄件人（`--sender-phone`）还是收件人（`--receiver-phone`）手机尾号；未来可能有更多公司有此要求，遇到 204305 错误码时同样引导用户提供
4. **调用脚本** — 传入单号、`--com` 编号（中文名或编号均可，脚本自动转换）执行查询
5. **解读结果** — 用自然语言总结当前状态，告知用户包裹是否已签收、当前在哪

### 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| 快递单号 | 是 | 快递运单号 | YT1234567890123 |
| `--com` | **是** | 快递公司中文名或编号，脚本自动转为编号传给接口 | 顺丰 / sf |
| `--sender-phone` | 部分必填 | 寄件人手机号后4位，顺丰/中通/跨越等必填其一 | 1234 |
| `--receiver-phone` | 部分必填 | 收件人手机号后4位，顺丰/中通/跨越等必填其一 | 5678 |
| `--list` | 否 | 列出所有支持的快递公司及编号 | — |
| `--search` | 否 | 搜索快递公司编号 | 圆通 |

### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `company` | 快递公司名称 | 圆通速递 |
| `com` | 快递公司编号 | yt |
| `no` | 运单号 | YT1234567890123 |
| `status` | 当前状态数字码 | 1 |
| `status_detail` | 当前状态英文枚举（更准确，优先使用） | IN_TRANSIT |
| `list` | 物流轨迹列表 | [{datetime, remark, zone}] |
| `list[].datetime` | 轨迹时间 | 2026-03-24 09:30:00 |
| `list[].remark` | 轨迹描述 | 快件已到达上海转运中心 |
| `list[].zone` | 所在区域 | 上海市 |

### status_detail 状态枚举对照

| status_detail | 中文含义 |
|---------------|---------|
| PENDING | 待处理 |
| NO_RECORD | 无记录 |
| ERROR | 查询错误 |
| IN_TRANSIT | 运输中 |
| DELIVERING | 派件中 |
| SIGNED | 已签收 |
| REJECTED | 拒收退回 |
| PROBLEM | 疑难件 |
| INVALID | 无效单号 |
| TIMEOUT | 查询超时 |
| FAILED | 投递失败 |
| SEND_BACK | 退件中 |
| TAKING | 已揽件 |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002/10003 | API Key 无效或过期，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/43) 重新申请 |
| `error_code` 10012 | 当日免费次数已用尽，建议升级套餐 |
| `error_code` 204301 | 快递公司编号错误，使用 `--list` 查看支持列表 |
| `error_code` 204302 | 运单号格式错误，请核对单号 |
| `error_code` 204304 | 暂无物流信息，可能刚揽件未录入，建议稍后再查 |
| `error_code` 204305 | 该快递公司需手机尾号，引导用户提供 `--sender-phone` 或 `--receiver-phone`（顺丰/中通/跨越等） |
| 公司名称模糊匹配到多家 | 列出候选公司，引导用户用编号精确指定 |

---

## 快递公司识别技巧

- **单号前缀参考**：SF 开头 → 顺丰（sf）；YT 开头 → 圆通（yt）；STO 开头 → 申通（sto）；JD 开头 → 京东（jd）；但仅供参考，以用户确认的公司为准
- **`--com` 为必填**，接口不支持自动识别，若用户未说明快递公司，应主动询问
- **中文名/编号均可传**，脚本会先在 `references/express-company-list.json` 本地查找对应编号，再传给接口，无需额外联网

---

## 脚本位置

`scripts/express_track.py` — 封装了 API 调用、公司名称模糊匹配、物流轨迹格式化输出和错误处理。

快递公司数据：`references/express-company-list.json` — 包含 1000+ 家全球快递公司的名称与编号对照表，**无需联网**，本地直接读取。

---

## 直接调用 API（无需脚本）

```
GET https://v.juhe.cn/exp/index?key=YOUR_KEY&com=sf&no=SF1234567890&senderPhone=1234
```

参数说明：

| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `key` | 是 | string | API Key |
| `com` | 是 | string | 快递公司编号，只接受编码（如 `sf`、`yt`），不接受中文 |
| `no` | 是 | string | 快递单号 |
| `senderPhone` | 否 | int | 寄件人手机号后4位，顺丰/中通/跨越等必填其一 |
| `receiverPhone` | 否 | int | 收件人手机号后4位，顺丰/中通/跨越等必填其一 |
| `dtype` | 否 | string | 返回格式：`json`（默认）或 `xml` |

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **交通物流**：快递追踪、火车时刻查询、航班动态
- **生活服务**：天气预报、万年历、节假日查询
- **身份核验**：手机号归属地、身份证实名验证
- **金融数据**：汇率、股票、黄金价格
- **网络工具**：IP查询、DNS解析

注册即可免费使用，适合个人开发者和企业接入。
