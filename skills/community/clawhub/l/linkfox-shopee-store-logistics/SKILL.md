---
name: linkfox-shopee-store-logistics
description: Shopee（虾皮）店铺物流发货（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Logistics 模块全部 46 个接口：get_shipping_parameter、ship_order、get_tracking_number、create_shipping_document、download_shipping_document、get_channel_list 等。当用户提到 Shopee 物流、发货、ship_order、运单号、面单、tracking、揽收地址、物流渠道、READY_TO_SHIP 发货 时触发。即使未明确提及"物流"，只要涉及已授权 Shopee 店铺的发货、面单或物流轨迹查询，也应触发。
---

# Shopee 店铺 Logistics

Shopee Open Platform **Logistics 模块**（46 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/logistics/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/logistics_api.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-logistics-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

Logistics 模块索引：[v2.logistics.get_shipping_parameter](https://open.shopee.com/documents/v2/v2.logistics.get_shipping_parameter?module=95&type=1)

---

## Prerequisites（必须先读）

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`** 并授权店铺。
2. **不要**在本 skill 内实现授权/令牌逻辑。

---

## Core Concepts

- **转发链路**：`developerProxy`（`shopId`/`merchantId` 选店，服务端注入 token）→ 紫鸟 `shopee-proxy` → Shopee API
- **典型发货流程**：`get_shipping_parameter` → `ship_order` → `get_tracking_number` → 面单（`create_shipping_document` → `download_shipping_document`）
- **订单查询**（列表/详情）→ `linkfox-shopee-store-orders`；本 skill 负责**物流发货与面单**
- **店铺级 API**：通常传 **`shopId`**

## 可用脚本（Logistics 模块 46 个 API）

| 分组 | 脚本 |
|------|------|
| 发货 | `get_shipping_parameter.py`、`ship_order.py`、`mass_ship_order.py`、`batch_ship_order.py`、`update_shipping_order.py` |
| 运单/轨迹 | `get_tracking_number.py`、`get_tracking_info.py`、`update_tracking_status.py` |
| 面单 | `get_shipping_document_parameter.py`、`create_shipping_document.py`、`download_shipping_document.py`、`create_shipping_document_job.py` 等 |
| 地址/渠道 | `get_address_list.py`、`get_channel_list.py`、`update_address.py`、`set_address_config.py` |
| Booking | `get_booking_shipping_parameter.py`、`ship_booking.py` 及 booking 面单系列 |
| 通用入口 | `logistics_api.py`（JSON 含 `api` 字段） |

完整列表见 `references/api.md`。共享：`_shopee_logistics_common.py`、`_logistics_endpoints.py`、`_logistics_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `batch_ship_order` | [references/apis/batch-ship-order.md](./references/apis/batch-ship-order.md) |
| `batch_update_tpf_warehouse_tracking_status` | [references/apis/batch-update-tpf-warehouse-tracking-status.md](./references/apis/batch-update-tpf-warehouse-tracking-status.md) |
| `check_polygon_update_status` | [references/apis/check-polygon-update-status.md](./references/apis/check-polygon-update-status.md) |
| `create_booking_shipping_document` | [references/apis/create-booking-shipping-document.md](./references/apis/create-booking-shipping-document.md) |
| `create_shipping_document` | [references/apis/create-shipping-document.md](./references/apis/create-shipping-document.md) |
| `create_shipping_document_job` | [references/apis/create-shipping-document-job.md](./references/apis/create-shipping-document-job.md) |
| `delete_address` | [references/apis/delete-address.md](./references/apis/delete-address.md) |
| `delete_special_operating_hour` | [references/apis/delete-special-operating-hour.md](./references/apis/delete-special-operating-hour.md) |
| `download_booking_shipping_document` | [references/apis/download-booking-shipping-document.md](./references/apis/download-booking-shipping-document.md) |
| `download_shipping_document` | [references/apis/download-shipping-document.md](./references/apis/download-shipping-document.md) |
| `download_shipping_document_job` | [references/apis/download-shipping-document-job.md](./references/apis/download-shipping-document-job.md) |
| `download_to_label` | [references/apis/download-to-label.md](./references/apis/download-to-label.md) |
| `get_address_list` | [references/apis/get-address-list.md](./references/apis/get-address-list.md) |
| `get_booking_shipping_document_data_info` | [references/apis/get-booking-shipping-document-data-info.md](./references/apis/get-booking-shipping-document-data-info.md) |
| `get_booking_shipping_document_parameter` | [references/apis/get-booking-shipping-document-parameter.md](./references/apis/get-booking-shipping-document-parameter.md) |
| `get_booking_shipping_document_result` | [references/apis/get-booking-shipping-document-result.md](./references/apis/get-booking-shipping-document-result.md) |
| `get_booking_shipping_parameter` | [references/apis/get-booking-shipping-parameter.md](./references/apis/get-booking-shipping-parameter.md) |
| `get_booking_tracking_info` | [references/apis/get-booking-tracking-info.md](./references/apis/get-booking-tracking-info.md) |
| `get_booking_tracking_number` | [references/apis/get-booking-tracking-number.md](./references/apis/get-booking-tracking-number.md) |
| `get_channel_list` | [references/apis/get-channel-list.md](./references/apis/get-channel-list.md) |
| `get_mart_packaging_info` | [references/apis/get-mart-packaging-info.md](./references/apis/get-mart-packaging-info.md) |
| `get_mass_shipping_parameter` | [references/apis/get-mass-shipping-parameter.md](./references/apis/get-mass-shipping-parameter.md) |
| `get_mass_tracking_number` | [references/apis/get-mass-tracking-number.md](./references/apis/get-mass-tracking-number.md) |
| `get_operating_hour_restrictions` | [references/apis/get-operating-hour-restrictions.md](./references/apis/get-operating-hour-restrictions.md) |
| `get_operating_hours` | [references/apis/get-operating-hours.md](./references/apis/get-operating-hours.md) |
| `get_pause_status` | [references/apis/get-pause-status.md](./references/apis/get-pause-status.md) |
| `get_shipping_document_data_info` | [references/apis/get-shipping-document-data-info.md](./references/apis/get-shipping-document-data-info.md) |
| `get_shipping_document_job_status` | [references/apis/get-shipping-document-job-status.md](./references/apis/get-shipping-document-job-status.md) |
| `get_shipping_document_parameter` | [references/apis/get-shipping-document-parameter.md](./references/apis/get-shipping-document-parameter.md) |
| `get_shipping_document_result` | [references/apis/get-shipping-document-result.md](./references/apis/get-shipping-document-result.md) |
| `get_shipping_parameter` | [references/apis/get-shipping-parameter.md](./references/apis/get-shipping-parameter.md) |
| `get_tracking_info` | [references/apis/get-tracking-info.md](./references/apis/get-tracking-info.md) |
| `get_tracking_number` | [references/apis/get-tracking-number.md](./references/apis/get-tracking-number.md) |
| `mass_ship_order` | [references/apis/mass-ship-order.md](./references/apis/mass-ship-order.md) |
| `set_address_config` | [references/apis/set-address-config.md](./references/apis/set-address-config.md) |
| `set_mart_packaging_info` | [references/apis/set-mart-packaging-info.md](./references/apis/set-mart-packaging-info.md) |
| `set_pause_status` | [references/apis/set-pause-status.md](./references/apis/set-pause-status.md) |
| `ship_booking` | [references/apis/ship-booking.md](./references/apis/ship-booking.md) |
| `ship_order` | [references/apis/ship-order.md](./references/apis/ship-order.md) |
| `update_address` | [references/apis/update-address.md](./references/apis/update-address.md) |
| `update_channel` | [references/apis/update-channel.md](./references/apis/update-channel.md) |
| `update_operating_hours` | [references/apis/update-operating-hours.md](./references/apis/update-operating-hours.md) |
| `update_self_collection_order_logistics` | [references/apis/update-self-collection-order-logistics.md](./references/apis/update-self-collection-order-logistics.md) |
| `update_shipping_order` | [references/apis/update-shipping-order.md](./references/apis/update-shipping-order.md) |
| `update_tracking_status` | [references/apis/update-tracking-status.md](./references/apis/update-tracking-status.md) |
| `upload_serviceable_polygon` | [references/apis/upload-serviceable-polygon.md](./references/apis/upload-serviceable-polygon.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 单订单发货
1. orders skill 获取 `order_sn`（状态 READY_TO_SHIP）
2. `get_shipping_parameter.py`：`order_sn`
3. `ship_order.py` 传完整 `body`
4. `get_tracking_number.py` 获取运单号

### 2. 打印面单
1. `get_shipping_document_parameter.py`
2. `create_shipping_document.py`
3. `download_shipping_document.py`

## 调用原则

- 先看 **`developerProxy.httpStatus`**，再读 `*Response` 字段
- GET：业务参数放 JSON 顶层（runner 拼 queryString）
- POST：复杂接口传 `body`
- 每个脚本 docstring 含 **官方文档 URL**（`module=95`）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 订单查询/取消/拆单 → `linkfox-shopee-store-orders`
- 退货退款 → `linkfox-shopee-store-returns`
- 店铺信息 → `linkfox-shopee-store-shop`
- 商品 listing → `linkfox-shopee-store-product`
- FirstMile 头程 → `linkfox-shopee-store-first-mile`
- SBS 仓储库存 → `linkfox-shopee-store-sbs`
- FBS 巴西仓储 → `linkfox-shopee-store-fbs`

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
