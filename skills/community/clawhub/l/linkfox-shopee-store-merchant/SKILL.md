---
name: linkfox-shopee-store-merchant
description: Shopee（虾皮）跨境商户信息（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Merchant 模块全部 6 个接口：get_merchant_info、get_shop_list_by_merchant、get_merchant_warehouse_list、get_merchant_warehouse_location_list、get_warehouse_eligible_shop_list、get_merchant_prepaid_account_list。当用户提到 Shopee 商户、merchantId、跨境卖家、CNSC、商户下店铺列表、get_merchant_info、商户仓库、预付账户 时触发。即使未明确提及"商户"，只要涉及已授权 Shopee 跨境商户的信息查询或下属店铺列表，也应触发。
---

# Shopee 商户 Merchant

Shopee Open Platform **Merchant 模块**（6 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/merchant/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill-name>-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考

Merchant 模块索引：[v2.merchant.get_merchant_info](https://open.shopee.com/documents/v2/v2.merchant.get_merchant_info?module=93&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权。
2. **不要**在本 skill 内实现授权/令牌逻辑。
3. Merchant 为**商户级** API，须传 **`merchantId`**；主要面向**跨境卖家**。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **商户 vs 店铺**：本 skill 查商户信息及下属店铺；单店资料见 `linkfox-shopee-store-shop`
- **全球商品**：商户下全球 listing 见 `linkfox-shopee-store-global-product`
- **典型用法**：`get_merchant_info` 确认 region/currency → `get_shop_list_by_merchant` 列出授权店铺

## 可用脚本（Merchant 模块 6 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `get_merchant_info.py` | get_merchant_info | GET |
| `get_shop_list_by_merchant.py` | get_shop_list_by_merchant | GET |
| `get_merchant_warehouse_location_list.py` | get_merchant_warehouse_location_list | GET |
| `get_merchant_warehouse_list.py` | get_merchant_warehouse_list | GET |
| `get_warehouse_eligible_shop_list.py` | get_warehouse_eligible_shop_list | GET |
| `get_merchant_prepaid_account_list.py` | get_merchant_prepaid_account_list | GET |
| `merchant_api.py` | 通用入口（JSON 含 `api` 字段） | — |

共享：`_shopee_merchant_common.py`、`_merchant_endpoints.py`、`_merchant_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `get_merchant_info` | [references/apis/get-merchant-info.md](./references/apis/get-merchant-info.md) |
| `get_merchant_prepaid_account_list` | [references/apis/get-merchant-prepaid-account-list.md](./references/apis/get-merchant-prepaid-account-list.md) |
| `get_merchant_warehouse_list` | [references/apis/get-merchant-warehouse-list.md](./references/apis/get-merchant-warehouse-list.md) |
| `get_merchant_warehouse_location_list` | [references/apis/get-merchant-warehouse-location-list.md](./references/apis/get-merchant-warehouse-location-list.md) |
| `get_shop_list_by_merchant` | [references/apis/get-shop-list-by-merchant.md](./references/apis/get-shop-list-by-merchant.md) |
| `get_warehouse_eligible_shop_list` | [references/apis/get-warehouse-eligible-shop-list.md](./references/apis/get-warehouse-eligible-shop-list.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查商户信息与下属店铺
1. auth skill 定位 `merchantId`
2. `get_merchant_info.py`：name、region、currency、授权过期
3. `get_shop_list_by_merchant.py`：`page_no=1`、`page_size=100`

### 2. 仓库与预付账户
- `get_merchant_warehouse_list.py` / `get_merchant_warehouse_location_list.py`
- `get_warehouse_eligible_shop_list.py`
- `get_merchant_prepaid_account_list.py`

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层（runner 拼 queryString）
- 每个脚本 docstring 含 **官方文档 URL**（`module=93`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 单店信息 → `linkfox-shopee-store-shop`
- 全球商品 → `linkfox-shopee-store-global-product`
- 单店 listing → `linkfox-shopee-store-product`
- 订单 → `linkfox-shopee-store-orders`
- Public 模块（`get_merchants_by_partner` 等）→ 非本 skill

## 算力消耗规则

不消耗算力。

**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
