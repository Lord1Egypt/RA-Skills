---
name: linkfox-shopee-store-account-health
description: Shopee（虾皮）账户健康 Account Health（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Account Health 模块全部 6 个接口：get_shop_performance、get_metric_source_detail、get_penalty_point_history、get_punishment_history、get_listings_with_issues、get_late_orders。当用户提到 Shopee 账户健康、Account Health、店铺绩效、扣分记录、处罚历史、逾期订单、listing问题 时触发。即使未明确提及"账户健康"，只要涉及已授权 Shopee 店铺的健康指标与处罚数据查询，也应触发。
---

# Shopee 账户健康 Account Health

Shopee Open Platform **Account Health 模块**（6 个 API，均为 GET）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/account_health/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-account-health-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

Account Health 模块索引：[v2.account_health.get_shop_performance](https://open.shopee.com/documents/v2/v2.account_health.get_shop_performance?module=103&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. 订单详情 → `linkfox-shopee-store-orders`；商品 listing → `linkfox-shopee-store-product`。

## 可用脚本（6 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `get_shop_performance.py` | get_shop_performance | GET |
| `get_metric_source_detail.py` | get_metric_source_detail | GET |
| `get_penalty_point_history.py` | get_penalty_point_history | GET |
| `get_punishment_history.py` | get_punishment_history | GET |
| `get_listings_with_issues.py` | get_listings_with_issues | GET |
| `get_late_orders.py` | get_late_orders | GET |
| `account_health_api.py` | 通用入口 | — |

共享：`_shopee_account_health_common.py`、`_account_health_endpoints.py`、`_account_health_api_runner.py`。

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `get_shop_performance` | [references/apis/get-shop-performance.md](./references/apis/get-shop-performance.md) |
| `get_metric_source_detail` | [references/apis/get-metric-source-detail.md](./references/apis/get-metric-source-detail.md) |
| `get_penalty_point_history` | [references/apis/get-penalty-point-history.md](./references/apis/get-penalty-point-history.md) |
| `get_punishment_history` | [references/apis/get-punishment-history.md](./references/apis/get-punishment-history.md) |
| `get_listings_with_issues` | [references/apis/get-listings-with-issues.md](./references/apis/get-listings-with-issues.md) |
| `get_late_orders` | [references/apis/get-late-orders.md](./references/apis/get-late-orders.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查看店铺健康概况
1. auth skill 定位 `shopId`
2. 按 [get-shop-performance.md](./references/apis/get-shop-performance.md) 调用 `get_shop_performance.py`
3. 对失败指标按 [get-metric-source-detail.md](./references/apis/get-metric-source-detail.md) 传 `metric_id` 下钻
4. 用 `get_late_orders.py` / `get_listings_with_issues.py` 定位问题订单或 listing

### 2. 查逾期订单（`get_late_orders`）
1. auth skill 定位 `shopId`
2. 按 [get-late-orders.md](./references/apis/get-late-orders.md) 传参调用 `get_late_orders.py`
3. 按 `late_by_days` 优先处理更紧急的订单

### 3. 查处罚与扣分记录
1. 按 [get-penalty-point-history.md](./references/apis/get-penalty-point-history.md) 查扣分
2. 按 [get-punishment-history.md](./references/apis/get-punishment-history.md) 查处罚（必填 `punishment_status`：`1` 进行中 / `2` 已结束）

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 订单处理 → `linkfox-shopee-store-orders`
- 商品 listing → `linkfox-shopee-store-product`
- 店铺基础信息 → `linkfox-shopee-store-shop`

## 算力消耗规则

不消耗算力。

**Feedback:** 见 `references/api.md`。


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
