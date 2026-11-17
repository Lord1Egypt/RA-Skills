---
name: linkfox-shopee-store-public
description: Shopee（虾皮）Public 公共模块（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Public 模块全部 6 个接口：get_shops_by_partner、get_merchants_by_partner、get_access_token、refresh_access_token、get_token_by_resend_code、get_shopee_ip_ranges。当用户提到 Shopee Public API、Partner 店铺列表、get_shops_by_partner、OAuth token 交换、refresh_access_token、Shopee IP 白名单 时触发。日常授权流程优先 linkfox-shopee-store-auth；需直接调用 v2.public.* 开放接口时触发本 skill。
---

# Shopee Public 公共模块

Shopee Open Platform **Public 模块**（6 个 API）。**依赖 `linkfox-shopee-store-auth`** 作为同系列前置；部分接口为 Partner 级或 OAuth 级，经 **`POST /shopee/developerProxy`** 转发（`path` 须 `api/v2/public/...`）。

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

Public 模块索引：[v2.public.get_shops_by_partner](https://open.shopee.com/documents/v2/v2.public.get_shops_by_partner?module=104&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. **日常授权 / 已授权店铺 / 读 token** → 优先 `linkfox-shopee-store-auth`（`authorize_url.py` / `authorized_stores.py` / `store_tokens.py`）。

## 可用脚本（6 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `get_shops_by_partner.py` | get_shops_by_partner | GET |
| `get_merchants_by_partner.py` | get_merchants_by_partner | GET |
| `get_access_token.py` | get_access_token | POST |
| `refresh_access_token.py` | refresh_access_token | POST |
| `get_token_by_resend_code.py` | get_token_by_resend_code | POST |
| `get_shopee_ip_ranges.py` | get_shopee_ip_ranges | GET |
| `public_api.py` | 通用入口 | — |

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `get_access_token` | [references/apis/get-access-token.md](./references/apis/get-access-token.md) |
| `get_merchants_by_partner` | [references/apis/get-merchants-by-partner.md](./references/apis/get-merchants-by-partner.md) |
| `get_shopee_ip_ranges` | [references/apis/get-shopee-ip-ranges.md](./references/apis/get-shopee-ip-ranges.md) |
| `get_shops_by_partner` | [references/apis/get-shops-by-partner.md](./references/apis/get-shops-by-partner.md) |
| `get_token_by_resend_code` | [references/apis/get-token-by-resend-code.md](./references/apis/get-token-by-resend-code.md) |
| `refresh_access_token` | [references/apis/refresh-access-token.md](./references/apis/refresh-access-token.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 查 Partner 下已授权店铺
`get_shops_by_partner.py` 或 `get_merchants_by_partner.py`

### 2. OAuth Token 交换（底层开放接口）
`get_access_token.py` / `refresh_access_token.py` 传完整 POST `body`

### 3. IP 白名单配置
`get_shopee_ip_ranges.py` 获取 Shopee 开放平台 IP 段

## Not Applicable

- 用户侧授权流程 → `linkfox-shopee-store-auth`
- 店铺业务 API（订单/商品/物流等）→ 对应业务 skill
- Push 回调配置 → `linkfox-shopee-store-push`

## 算力消耗规则

不消耗算力。

**Feedback:** 见 `references/api.md`。


---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
