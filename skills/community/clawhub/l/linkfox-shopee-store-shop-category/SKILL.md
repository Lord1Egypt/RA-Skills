---
name: linkfox-shopee-store-shop-category
description: Shopee（虾皮）店铺分类 Shop Category（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Shop Category 模块全部 7 个接口：add_shop_category、get_shop_category_list、update_shop_category、add_item_list、get_item_list、delete_item_list 等。当用户提到 Shopee 店铺分类、Shop Category、自定义分类、add_shop_category、shop_category_id、分类商品 时触发。即使未明确提及"分类"，只要涉及已授权 Shopee 店铺的 Shop Category 管理，也应触发。
---

# Shopee 店铺分类 Shop Category

Shopee Open Platform **Shop Category 模块**（7 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/shop_category/...`）。

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

Shop Category 模块索引：[v2.shop_category.add_shop_category](https://open.shopee.com/documents/v2/v2.shop_category.add_shop_category?module=101&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. 商品 listing → `linkfox-shopee-store-product`；精选 Top Picks → `linkfox-shopee-store-top-picks`。

## 可用脚本（7 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `add_shop_category.py` | add_shop_category | POST |
| `get_shop_category_list.py` | get_shop_category_list | GET |
| `delete_shop_category.py` | delete_shop_category | POST |
| `update_shop_category.py` | update_shop_category | POST |
| `add_item_list.py` | add_item_list | POST |
| `get_item_list.py` | get_item_list | GET |
| `delete_item_list.py` | delete_item_list | POST |
| `shop_category_api.py` | 通用入口 | — |

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_item_list` | [references/apis/add-item-list.md](./references/apis/add-item-list.md) |
| `add_shop_category` | [references/apis/add-shop-category.md](./references/apis/add-shop-category.md) |
| `delete_item_list` | [references/apis/delete-item-list.md](./references/apis/delete-item-list.md) |
| `delete_shop_category` | [references/apis/delete-shop-category.md](./references/apis/delete-shop-category.md) |
| `get_item_list` | [references/apis/get-item-list.md](./references/apis/get-item-list.md) |
| `get_shop_category_list` | [references/apis/get-shop-category-list.md](./references/apis/get-shop-category-list.md) |
| `update_shop_category` | [references/apis/update-shop-category.md](./references/apis/update-shop-category.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 管理店铺分类
1. `add_shop_category.py` 创建分类
2. `add_item_list.py` 添加商品
3. `get_shop_category_list.py` / `get_item_list.py` 查看分类与商品

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 商品 listing CRUD → `linkfox-shopee-store-product`
- 精选 Top Picks → `linkfox-shopee-store-top-picks`
- 店铺基础信息 → `linkfox-shopee-store-shop`

## 积分消耗规则

不消耗积分。

**Feedback:** 见 `references/api.md`。

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
