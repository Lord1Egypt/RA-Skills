---
name: linkfox-shopee-store-returns
description: Shopee（虾皮）店铺退货退款（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Returns 模块全部 15 个接口：get_return_list、get_return_detail、confirm、dispute、offer、accept_offer、upload_proof、get_reverse_tracking_info 等。当用户提到 Shopee 退货、退款、return_sn、退货列表、确认退货、退货争议、dispute、逆向物流 时触发。即使未明确提及"退货"，只要涉及已授权 Shopee 店铺的退货/退款查询或处理，也应触发。
---

# Shopee 店铺 Returns

Shopee Open Platform **Returns 模块**（15 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/returns/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考

Returns 模块索引：[v2.returns.get_return_list](https://open.shopee.com/documents/v2/v2.returns.get_return_list?module=102&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权店铺。
2. **不要**在本 skill 内实现授权/令牌逻辑。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **退货 vs 订单**：订单查询见 `linkfox-shopee-store-orders`；本 skill 处理**退货/退款/争议**
- **典型流程**：`get_return_list` → `get_return_detail` → `confirm` / `offer` / `dispute`
- **店铺级 API**：通常传 **`shopId`**

## 可用脚本（Returns 模块 15 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `get_return_list.py` | get_return_list | GET |
| `get_return_detail.py` | get_return_detail | GET |
| `confirm.py` | confirm | POST |
| `dispute.py` | dispute | POST |
| `get_available_solutions.py` | get_available_solutions | GET |
| `offer.py` | offer | POST |
| `accept_offer.py` | accept_offer | POST |
| `convert_image.py` | convert_image | POST |
| `upload_proof.py` | upload_proof | POST |
| `query_proof.py` | query_proof | GET |
| `get_return_dispute_reason.py` | get_return_dispute_reason | GET |
| `cancel_dispute.py` | cancel_dispute | POST |
| `get_shipping_carrier.py` | get_shipping_carrier | GET |
| `upload_shipping_proof.py` | upload_shipping_proof | POST |
| `get_reverse_tracking_info.py` | get_reverse_tracking_info | GET |
| `returns_api.py` | 通用入口（JSON 含 `api` 字段） | — |

共享：`_shopee_returns_common.py`、`_returns_endpoints.py`、`_returns_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `accept_offer` | [references/apis/accept-offer.md](./references/apis/accept-offer.md) |
| `cancel_dispute` | [references/apis/cancel-dispute.md](./references/apis/cancel-dispute.md) |
| `confirm` | [references/apis/confirm.md](./references/apis/confirm.md) |
| `convert_image` | [references/apis/convert-image.md](./references/apis/convert-image.md) |
| `dispute` | [references/apis/dispute.md](./references/apis/dispute.md) |
| `get_available_solutions` | [references/apis/get-available-solutions.md](./references/apis/get-available-solutions.md) |
| `get_return_detail` | [references/apis/get-return-detail.md](./references/apis/get-return-detail.md) |
| `get_return_dispute_reason` | [references/apis/get-return-dispute-reason.md](./references/apis/get-return-dispute-reason.md) |
| `get_return_list` | [references/apis/get-return-list.md](./references/apis/get-return-list.md) |
| `get_reverse_tracking_info` | [references/apis/get-reverse-tracking-info.md](./references/apis/get-reverse-tracking-info.md) |
| `get_shipping_carrier` | [references/apis/get-shipping-carrier.md](./references/apis/get-shipping-carrier.md) |
| `offer` | [references/apis/offer.md](./references/apis/offer.md) |
| `query_proof` | [references/apis/query-proof.md](./references/apis/query-proof.md) |
| `upload_proof` | [references/apis/upload-proof.md](./references/apis/upload-proof.md) |
| `upload_shipping_proof` | [references/apis/upload-shipping-proof.md](./references/apis/upload-shipping-proof.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查退货列表与详情
1. `get_return_list.py`：`page_no`、`page_size`
2. `get_return_detail.py`：`return_sn`

### 2. 处理退货
1. `get_available_solutions.py`：`return_sn`
2. `confirm.py` 或 `offer.py`：POST `body`
3. 如有争议：`dispute.py` / `cancel_dispute.py`

### 3. 凭证与逆向物流
- `upload_proof.py` / `query_proof.py`
- `get_reverse_tracking_info.py`

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层
- POST：复杂接口传 `body`
- 每个脚本 docstring 含 **官方文档 URL**（`module=102`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 订单查询/取消 → `linkfox-shopee-store-orders`
- 正向物流发货 → `linkfox-shopee-store-logistics`
- 商品 listing → `linkfox-shopee-store-product`

## 积分消耗规则

不消耗积分。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
