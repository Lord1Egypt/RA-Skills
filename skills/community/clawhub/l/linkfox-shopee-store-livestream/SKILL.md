---
name: linkfox-shopee-store-livestream
description: Shopee（虾皮）直播 Livestream（与 linkfox-shopee-store-auth 同系列），经 /shopee/developerProxy 转发 Shopee Open API Livestream 模块全部 25 个接口：create_session、start_session、add_item_list、get_session_detail、get_session_metric、post_comment、upload_image 等。当用户提到 Shopee 直播、Livestream、创建直播场次、直播商品、直播评论、session_id、upload_image 时触发。即使未明确提及"直播"，只要涉及已授权 Shopee 店铺的 Livestream 场次/商品/互动管理，也应触发。
---

# Shopee 直播 Livestream

Shopee Open Platform **Livestream 模块**（25 个 API）。**依赖 `linkfox-shopee-store-auth`** 选店；经 **`POST /shopee/developerProxy`** 传入 `shopId`（或 `merchantId`），由服务端解析 token 转发（`path` 须 `api/v2/livestream/...`）。

## 调用方式

- **API 端点**：`POST /shopee/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/livestream_api.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
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

Livestream 模块索引：[v2.livestream.upload_image](https://open.shopee.com/documents/v2/v2.livestream.upload_image?module=125&type=1)

---

## Prerequisites

1. 运行 `python scripts/check_auth_dependency.py`；exit code **42** → 先安装 **`linkfox-shopee-store-auth`**。
2. 店铺短视频 Video → `linkfox-shopee-store-video`；图片上传 Media → `linkfox-shopee-store-media`。

## 可用脚本（25 个 API）

| 脚本 | API | Method |
|------|-----|--------|
| `upload_image.py` | upload_image | POST |
| `create_session.py` | create_session | POST |
| `update_session.py` | update_session | POST |
| `start_session.py` | start_session | POST |
| `end_session.py` | end_session | POST |
| `get_session_detail.py` | get_session_detail | GET |
| `add_item_list.py` | add_item_list | POST |
| `delete_item_list.py` | delete_item_list | POST |
| `update_item_list.py` | update_item_list | POST |
| `get_item_count.py` | get_item_count | GET |
| `get_item_list.py` | get_item_list | GET |
| `update_show_item.py` | update_show_item | POST |
| `delete_show_item.py` | delete_show_item | POST |
| `get_show_item.py` | get_show_item | GET |
| `get_like_item_list.py` | get_like_item_list | GET |
| `get_recent_item_list.py` | get_recent_item_list | GET |
| `get_item_set_list.py` | get_item_set_list | GET |
| `get_item_set_item_list.py` | get_item_set_item_list | GET |
| `apply_item_set.py` | apply_item_set | POST |
| `get_session_metric.py` | get_session_metric | GET |
| `get_session_item_metric.py` | get_session_item_metric | GET |
| `get_latest_comment_list.py` | get_latest_comment_list | GET |
| `post_comment.py` | post_comment | POST |
| `ban_user_comment.py` | ban_user_comment | POST |
| `unban_user_comment.py` | unban_user_comment | POST |
| `livestream_api.py` | 通用入口 | — |

## 接口说明（按 API）

入参与响应细节放在 `references/apis/`，SKILL 只保留索引。

| API | 说明文档 |
|-----|----------|
| `add_item_list` | [references/apis/add-item-list.md](./references/apis/add-item-list.md) |
| `apply_item_set` | [references/apis/apply-item-set.md](./references/apis/apply-item-set.md) |
| `ban_user_comment` | [references/apis/ban-user-comment.md](./references/apis/ban-user-comment.md) |
| `create_session` | [references/apis/create-session.md](./references/apis/create-session.md) |
| `delete_item_list` | [references/apis/delete-item-list.md](./references/apis/delete-item-list.md) |
| `delete_show_item` | [references/apis/delete-show-item.md](./references/apis/delete-show-item.md) |
| `end_session` | [references/apis/end-session.md](./references/apis/end-session.md) |
| `get_item_count` | [references/apis/get-item-count.md](./references/apis/get-item-count.md) |
| `get_item_list` | [references/apis/get-item-list.md](./references/apis/get-item-list.md) |
| `get_item_set_item_list` | [references/apis/get-item-set-item-list.md](./references/apis/get-item-set-item-list.md) |
| `get_item_set_list` | [references/apis/get-item-set-list.md](./references/apis/get-item-set-list.md) |
| `get_latest_comment_list` | [references/apis/get-latest-comment-list.md](./references/apis/get-latest-comment-list.md) |
| `get_like_item_list` | [references/apis/get-like-item-list.md](./references/apis/get-like-item-list.md) |
| `get_recent_item_list` | [references/apis/get-recent-item-list.md](./references/apis/get-recent-item-list.md) |
| `get_session_detail` | [references/apis/get-session-detail.md](./references/apis/get-session-detail.md) |
| `get_session_item_metric` | [references/apis/get-session-item-metric.md](./references/apis/get-session-item-metric.md) |
| `get_session_metric` | [references/apis/get-session-metric.md](./references/apis/get-session-metric.md) |
| `get_show_item` | [references/apis/get-show-item.md](./references/apis/get-show-item.md) |
| `post_comment` | [references/apis/post-comment.md](./references/apis/post-comment.md) |
| `start_session` | [references/apis/start-session.md](./references/apis/start-session.md) |
| `unban_user_comment` | [references/apis/unban-user-comment.md](./references/apis/unban-user-comment.md) |
| `update_item_list` | [references/apis/update-item-list.md](./references/apis/update-item-list.md) |
| `update_session` | [references/apis/update-session.md](./references/apis/update-session.md) |
| `update_show_item` | [references/apis/update-show-item.md](./references/apis/update-show-item.md) |
| `upload_image` | [references/apis/upload-image.md](./references/apis/upload-image.md) |

模块总览 / Feedback 见 [references/api.md](./references/api.md)。

## Usage Scenarios

### 1. 创建并开播
1. `upload_image.py` 上传封面/素材
2. `create_session.py` 创建场次
3. `add_item_list.py` 添加商品
4. `start_session.py` 开始直播

### 2. 直播中管理
1. `update_show_item.py` 切换展示商品
2. `get_latest_comment_list.py` / `post_comment.py` 评论互动
3. `get_session_metric.py` 查看数据

## Not Applicable

- 店铺授权 → `linkfox-shopee-store-auth`
- 店铺短视频 Video → `linkfox-shopee-store-video`
- 通用图片/视频上传 Media / MediaSpace → 对应 media skill
- 商品 listing → `linkfox-shopee-store-product`

## 算力消耗规则

不消耗算力。

**Feedback:** 见 `references/api.md`。

---
*For more high-quality, professional cross-border e-commerce skills, visit [LinkFox Skills](https://skill.linkfox.com/).*
