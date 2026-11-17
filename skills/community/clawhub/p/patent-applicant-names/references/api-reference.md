# 接口速查

环境里没有 Python 时直接用这些。有 Python 的话优先用 `scripts/patentmax_client.py`——字段名归一、计费汇总它都处理好了。

**Base URL** `https://api.ip930.com`
**认证** 所有接口都要 `Authorization: Bearer <API_KEY>`

---

## 按篇取数：直接用公开号

所有按篇取数的接口都收 `pn`（公开号）参数，**不需要先检索换 id**：

```bash
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  "https://api.ip930.com/api/patent?pn=CN109761224A"
```

服务端自己完成内部寻址，这些前置调用**不进用户账单**。

> 也可以传 `id=`（检索结果里那个内部标识），价钱一样。老版本客户端为了躲开
> 「换 id 要先花一次检索钱」而做的落盘缓存，现在没有必要了。

字段名不统一：公开号可能叫 `documentNumber`、`publicationNumber` 或 `pn`。取值时按候选名依次试。

结果列表也有好几种叫法：`patents` / `list` / `data` / `records`。

---

## 每日免费额度

生产密钥每天前 **30 次** `/api/search` 与 `/api/patent` 不扣费（北京时间零点重置），
用完自动转正常计费，不会中断。响应头里能看到：

| 响应头 | 含义 |
| --- | --- |
| `x-patentmax-charged-cents` | 本次实扣（分） |
| `x-patentmax-balance-cents` | 扣完后的余额（分） |
| `x-patentmax-free-used` / `x-patentmax-free-quota` | 今天已用 / 总免费次数 |
| `x-patentmax-idempotent-replay` | `true` 表示这是同一 Idempotency-Key 的重放，未扣费 |

## 超时重试不重复扣费：Idempotency-Key

付费请求可以带 `Idempotency-Key: <你自己取的键>`。同一个键 + 同样的参数再发一次，
服务端直接返回上次的结果、**不再扣费**；同一个键换了参数会被拒（400）；上一次还在处理中返回 409。

```bash
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" -H "Idempotency-Key: task42-search-1"   "https://api.ip930.com/api/search?q=%E6%B5%B8%E6%B2%A1%E5%BC%8F%E6%B6%B2%E5%86%B7&ds=cn&size=20"
```

网络超时、不确定上一次有没有成功时，**用同一个键重发**，不要换键。
`scripts/patentmax_client.py` 已经自动这么做（键由任务 id + 请求参数生成）。

> 用 curl 看这些头要加 `-i`，否则只会打印响应体。

---

## 检索

### GET /api/search — 全球专利检索

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `q` | 是 | 检索式，支持 `AND` / `OR` / `NOT` 和括号，最长 4000 字符 |
| `ds` | 否 | `all` 全球（默认）、`cn` 仅中国 |
| `page` | 否 | 1–100，默认 1 |
| `size` | 否 | 1–50，默认 20 |

```bash
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  --data-urlencode 'q=(固态电池 OR 全固态电池) AND 电解质' \
  --data-urlencode 'ds=all' --data-urlencode 'size=20' \
  -G "https://api.ip930.com/api/search"
```

> 检索式里有中文和括号，一定用 `--data-urlencode -G`，别手工拼 URL。

**¥0.10 / 次**（每天前 30 次免费）

### 整篇专利（优先用这个）

`GET /api/patent?pn=<公开号>` — **¥0.10 / 次**，每天前 30 次免费。

一次返回著录项、权利要求书、说明书全文三块，**计一次价**。
分别去调 detail + claims + fulltext 是 ¥0.15，还多两次往返，没有理由那样做。

```bash
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  "https://api.ip930.com/api/patent?pn=CN109761224A"
```

> 某一块上游取不到时，该字段为 null 并在 `unavailable` 里列出，其余照常返回；
> 三块全取不到才算失败。

### 按字段单取

以下都是 `GET`，都接受 `pn`（公开号）或 `id`：

| 接口 | 返回 | 单价 |
| --- | --- | --- |
| `/api/detail` | 著录项目：标题、申请人、发明人、申请日、公开日、IPC、法律状态 | ¥0.05 |
| `/api/claims` | 权利要求书 | ¥0.05 |
| `/api/fulltext` | 说明书全文（很长） | ¥0.05 |
| `/api/legal` | 法律事件流水 | ¥0.05 |
| `/api/citation` | 引用与被引用，含非专利文献 | ¥0.05 |
| `/api/similar` | 语义相似专利 | ¥0.10 |
| `/api/img` | 摘要附图（二进制图片） | ¥0.05 |
| `/api/pdf` | PDF 全文（二进制） | ¥0.30 |
| `/api/ration` | 统计分析，一次一个维度 Top 20 | ¥0.30 |
| `/api/a/portrait` | 企业画像 | ¥0.30 |

```bash
curl -s -H "Authorization: Bearer $PATENTMAX_API_KEY" \
  "https://api.ip930.com/api/claims?pn=CN109761224A"
```

**只要同时需要两块以上，就用 `/api/patent`**——它一口价，拆开单买反而贵。

---

## 健康检查

```bash
curl -s "https://api.ip930.com/api/v1/health"
```

**不需要密钥**，用来确认网络通不通。

---

## 状态码

| 码 | 含义 | 怎么办 |
| --- | --- | --- |
| 400 | 参数有问题 | 检查必填项和取值范围 |
| 401 | 密钥无效或已撤销 | 确认密钥完整、`Bearer ` 前缀没漏 |
| 402 | 余额不足 | 去控制台充值 |
| 403 | 该密钥无此接口权限 | 换密钥或联系支持 |
| 404 | 没找到这篇专利 | 确认公开号正确且带国别代码，如 `CN109761224A` |
| 409 | 同一个 Idempotency-Key 的请求还在处理 | 等几秒用同一个键重试，不会重复扣费 |
| 429 | 限流 | 生产密钥 600 次/分；沙箱密钥每天 30 次 |

调用失败不扣费。

---

## 两种密钥

| 前缀 | 行为 |
| --- | --- |
| `pm_live_` | 生产密钥，真实数据，从余额按次扣费。**正常使用都用这个** |
| `pm_test_` | 沙箱密钥，检索类每天 30 次，报告类任务返回模拟结果 |

沙箱密钥用于开发阶段验证参数与响应结构，跑不出真实检索结果。

新账户送的是**真实余额**，够跑 500 次检索，直接用生产密钥即可。
