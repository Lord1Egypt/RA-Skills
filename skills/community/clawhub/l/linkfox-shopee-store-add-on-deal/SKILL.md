---
name: linkfox-shopee-store-add-on-deal
description: Shopee（虾皮）加购优惠 Add-On Deal（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Add-On Deal 模块全部 14 个接口：add_add_on_deal、get_add_on_deal_list、add_add_on_deal_main_item、add_add_on_deal_sub_item、update_add_on_deal、end_add_on_deal 等。当用户提到 Shopee 加购优惠、Add-On Deal、主商品加购、add_add_on_deal、add_on_deal_id、满额加购 时触发。即使未明确提及"加购"，只要涉及已授权 Shopee 店铺的 Add-On Deal 活动管理，也应触发。
---

# Shopee 加购优惠 Add-On Deal

Shopee Open Platform **Add-On Deal 模块**（14 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/add_on_deal/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-shopee-store-add-on-deal-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

Add-On Deal 模块索引：[v2.add_on_deal.add_add_on_deal](https://open.shopee.com/documents/v2/v2.add_on_deal.add_add_on_deal?module=111&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. 限时折扣 → `linkfox-shopee-store-discount`；套装优惠 → `linkfox-shopee-store-bundle-deal`；Voucher → `linkfox-shopee-store-voucher`。

## 可用脚本（14 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `add_add_on_deal.py` | add_add_on_deal | POST |
| `add_add_on_deal_main_item.py` | add_add_on_deal_main_item | POST |
| `add_add_on_deal_sub_item.py` | add_add_on_deal_sub_item | POST |
| `delete_add_on_deal.py` | delete_add_on_deal | POST |
| `delete_add_on_deal_main_item.py` | delete_add_on_deal_main_item | POST |
| `delete_add_on_deal_sub_item.py` | delete_add_on_deal_sub_item | POST |
| `get_add_on_deal_list.py` | get_add_on_deal_list | GET |
| `get_add_on_deal.py` | get_add_on_deal | GET |
| `get_add_on_deal_main_item.py` | get_add_on_deal_main_item | GET |
| `get_add_on_deal_sub_item.py` | get_add_on_deal_sub_item | GET |
| `update_add_on_deal.py` | update_add_on_deal | POST |
| `update_add_on_deal_main_item.py` | update_add_on_deal_main_item | POST |
| `update_add_on_deal_sub_item.py` | update_add_on_deal_sub_item | POST |
| `end_add_on_deal.py` | end_add_on_deal | POST |
| `add_on_deal_api.py` | 通用入口 | — |

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_add_on_deal` | [references/apis/add-add-on-deal.md](./references/apis/add-add-on-deal.md) |
| `add_add_on_deal_main_item` | [references/apis/add-add-on-deal-main-item.md](./references/apis/add-add-on-deal-main-item.md) |
| `add_add_on_deal_sub_item` | [references/apis/add-add-on-deal-sub-item.md](./references/apis/add-add-on-deal-sub-item.md) |
| `delete_add_on_deal` | [references/apis/delete-add-on-deal.md](./references/apis/delete-add-on-deal.md) |
| `delete_add_on_deal_main_item` | [references/apis/delete-add-on-deal-main-item.md](./references/apis/delete-add-on-deal-main-item.md) |
| `delete_add_on_deal_sub_item` | [references/apis/delete-add-on-deal-sub-item.md](./references/apis/delete-add-on-deal-sub-item.md) |
| `end_add_on_deal` | [references/apis/end-add-on-deal.md](./references/apis/end-add-on-deal.md) |
| `get_add_on_deal` | [references/apis/get-add-on-deal.md](./references/apis/get-add-on-deal.md) |
| `get_add_on_deal_list` | [references/apis/get-add-on-deal-list.md](./references/apis/get-add-on-deal-list.md) |
| `get_add_on_deal_main_item` | [references/apis/get-add-on-deal-main-item.md](./references/apis/get-add-on-deal-main-item.md) |
| `get_add_on_deal_sub_item` | [references/apis/get-add-on-deal-sub-item.md](./references/apis/get-add-on-deal-sub-item.md) |
| `update_add_on_deal` | [references/apis/update-add-on-deal.md](./references/apis/update-add-on-deal.md) |
| `update_add_on_deal_main_item` | [references/apis/update-add-on-deal-main-item.md](./references/apis/update-add-on-deal-main-item.md) |
| `update_add_on_deal_sub_item` | [references/apis/update-add-on-deal-sub-item.md](./references/apis/update-add-on-deal-sub-item.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 创建加购优惠
1. `add_add_on_deal.py` 传完整 `body`
2. `add_add_on_deal_main_item.py` / `add_add_on_deal_sub_item.py` 添加主商品与加购商品
3. `get_add_on_deal_list.py` 确认状态

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 限时折扣 Discount → `linkfox-shopee-store-discount`
- 套装优惠 Bundle Deal → `linkfox-shopee-store-bundle-deal`
- 商品 listing → `linkfox-shopee-store-product`

## 算力消耗规则

不消耗算力。

**Feedback:** 见 `references/api.md`。


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
