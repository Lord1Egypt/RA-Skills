---
name: linkfox-shopee-store-sbs
description: Shopee（虾皮）SBS 仓储服务（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API SBS 模块全部 5 个接口：get_bound_whs_info、get_current_inventory、get_expiry_report、get_stock_aging、get_stock_movement。当用户提到 Shopee SBS、仓储库存、绑定仓库、get_bound_whs_info、库龄报表、效期报表、库存变动 时触发。即使未明确提及"SBS"，只要涉及已授权 Shopee 店铺的 SBS 仓储与库存数据查询，也应触发。
---

# Shopee SBS 仓储服务

Shopee Open Platform **SBS 模块**（5 个 API，均为 GET）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/sbs/...`）。

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

SBS 模块索引：[v2.sbs.get_bound_whs_info](https://open.shopee.com/documents/v2/v2.sbs.get_bound_whs_info?module=124&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. 物流发货 → `linkfox-shopee-store-logistics`；头程 → `linkfox-shopee-store-first-mile`。

## 可用脚本（5 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `get_bound_whs_info.py` | get_bound_whs_info | GET |
| `get_current_inventory.py` | get_current_inventory | GET |
| `get_expiry_report.py` | get_expiry_report | GET |
| `get_stock_aging.py` | get_stock_aging | GET |
| `get_stock_movement.py` | get_stock_movement | GET |
| `sbs_api.py` | 通用入口 | — |

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `get_bound_whs_info` | [references/apis/get-bound-whs-info.md](./references/apis/get-bound-whs-info.md) |
| `get_current_inventory` | [references/apis/get-current-inventory.md](./references/apis/get-current-inventory.md) |
| `get_expiry_report` | [references/apis/get-expiry-report.md](./references/apis/get-expiry-report.md) |
| `get_stock_aging` | [references/apis/get-stock-aging.md](./references/apis/get-stock-aging.md) |
| `get_stock_movement` | [references/apis/get-stock-movement.md](./references/apis/get-stock-movement.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查看 SBS 仓储概况
1. `get_bound_whs_info.py` 查绑定仓库
2. `get_current_inventory.py` 查当前库存

### 2. 库存分析报表
1. `get_stock_aging.py` 库龄
2. `get_expiry_report.py` 效期
3. `get_stock_movement.py` 变动记录

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 物流发货参数/运单 → `linkfox-shopee-store-logistics`
- 头程绑定 → `linkfox-shopee-store-first-mile`
- 商品 listing → `linkfox-shopee-store-product`
- FBS 巴西仓储 → `linkfox-shopee-store-fbs`

## 积分消耗规则

不消耗积分。

**Feedback:** 见 `references/api.md`。

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
