---
name: 话袋笔记
description: |
  话袋笔记 - 新建、更新和搜索个人笔记。

  **当以下情况时使用此 Skill**：
  (1) 用户要保存内容到笔记：「记一下」「存到笔记」「保存」「收藏」
  (2) 用户要更新内容到笔记：「更新一下」「更新笔记」
  (3) 用户要搜索或查看笔记：「搜一下」「找找笔记」「打开某条笔记」「笔记详情」
  (4) 用户要配置话袋笔记：「配置话袋」「连接话袋笔记」「怎么填 Key」
metadata:
  openclaw:
    requires: {}
    optionalEnv:
      - HUADAI_BASE_URL
      - HUADAI_API_KEY
      - HUADAI_CLIENT_ID
      - HUADAI_USER_UUID
    baseUrl: "https://openapi.ihuadai.cn/open/api/v1"
    homepage: "https://ihuadai.cn"
---
# 话袋笔记 Skill

## Agent 必读约束

- **唯一 Base URL**：`https://openapi.ihuadai.cn/open/api/v1`（禁止使用其他域名或自行拼接根域）
- **开放 API 文档**：以话袋官方发布为准（此仓库以 `references/` 内文档为最终对接依据）
- **鉴权与必需请求头**：`HUADAI_API_KEY`**（`Authorization`）及 **`HUADAI_USER_UUID`**（`USER-UUID`，与话袋用户 `unique_id` 一致）
- **OAuth（设备码）**：按 [OAuth 授权配置](references/oauth.md) 执行；默认使用服务端预注册的固定 `client_id`，一般**只需要**配置 `HUADAI_BASE_URL` 即可走授权。仅在需要覆盖时才配置 `HUADAI_CLIENT_ID`。
- **调用前检查配置**：若未配置 `HUADAI_API_KEY` / `HUADAI_USER_UUID`（业务请求）或未配置 `HUADAI_BASE_URL`（走 OAuth 时），必须停止调用并引导用户在本地配置；禁止假装成功
- **数据真实性**：所有笔记内容、列表、详情都必须来自 API 响应；禁止编造笔记、ID、space_id 等
- **空结果处理**：API 返回为空/未找到时，必须明确告知“未找到”，并给出下一步（换关键词/缩小范围）
- **写操作确认**：保存/更新等写操作，必须在 API 明确返回成功后再回复“已保存/已更新”
- **群聊/多人限制（若配置 `HUADAI_USER_UUID`）**：
  - `HUADAI_USER_UUID` 与话袋 **`unique_id`** 一致，用于在多人聊天中划定「仅该用户」的笔记边界，保证私密性
  - 当请求者身份无法与 `HUADAI_USER_UUID` 匹配时，必须拒绝访问任何笔记内容与搜索结果
  - 拒绝时只说明需要由 owner 发起请求，不泄露任何数据

---

## 文档索引（references）

> 匹配指令或 API 后，用 **read 工具**读取下表对应 `references/*.md` 获取完整字段、示例与边界说明。错误码与统一响应见 [话袋笔记 API 详细参考](references/api-details.md)。

## 指令路由表

| 指令 | 角色 | 说明 | 详细文档 |
|------|------|------|----------|
| `/huadai config` 或「配置话袋」 | 配置 | 环境变量、`openclaw.json` 注入、请求头约定 | [配置（必须先完成）](references/config.md) |
| `/huadai oauth` 或「授权/连接」 | 授权 | OAuth 2.0 Device Flow、换取 API Key | [OAuth 授权配置（话袋笔记）](references/oauth.md) |
| `/huadai upload` 或「记一下/保存」 | 新建 | 新建 Block 笔记（`upload-block`） | [新建笔记（Upload）](references/upload.md) |
| `/huadai update` 或「更新笔记」 | 更新 | 更新 Block 内容与属性（`update-block`） | [更新笔记（Update）](references/update.md) |
| `/huadai search` 或「搜一下」 | 搜索 | 全文检索 `GET /search` | [搜索笔记（Search）](references/search.md) |

## 自然语言路由（触发规则）

| 用户说法（示例） | 路由 | 详细文档 |
|------------------|------|----------|
| 「新建/上传/保存到笔记」 | Upload | [新建笔记（Upload）](references/upload.md) |
| 「更新/修改笔记」 | Update | [更新笔记（Update）](references/update.md) |
| 「搜/找/检索/有哪些相关笔记」 | Search | [搜索笔记（Search）](references/search.md) |
| 「配置/连接/怎么填 key/报错未配置」 | Config / OAuth | [配置（必须先完成）](references/config.md)、[OAuth 授权配置](references/oauth.md) |

## API 路由表

> 说明：以下为 MVP 参考路径。Base URL 为 `https://openapi.ihuadai.cn/open/api/v1`（与 [配置](references/config.md) 中 `HUADAI_BASE_URL` 一致）。

| 方法 | 路径 | 说明 | 详细文档 |
|------|------|------|----------|
| GET | `/open/api/v1/search` | 全文检索 | [搜索笔记（Search）](references/search.md#全文检索) |
| POST | `/open/api/v1/block/upload-block` | 新建笔记 Block | [新建笔记（Upload）](references/upload.md#新建笔记block) |
| POST | `/open/api/v1/block/update-block` | 更新笔记内容/属性 | [更新笔记（Update）](references/update.md#更新笔记block) |
| （OAuth） | `/open/api/v1/oauth/device/code` 等 | 设备码授权（Device Flow） | [OAuth 授权配置](references/oauth.md) |

统一鉴权、响应包体与错误码分段说明见 [api-details.md](references/api-details.md#统一鉴权与请求头)、[错误码表](references/api-details.md#错误码表code)。

## 通用错误处理（统一策略）

- **未配置/缺失 Key**：停止请求，引导用户配置 `HUADAI_API_KEY`
- **未登录/未授权**：提示需要重新登录/刷新 token（按后端返回的 `code/message` 给出行动建议）
- **无权限（403）**：告知无权限访问该笔记，建议更换关键词或确认账号
- **限流（429）**：提示稍后重试，并进行退避（例如等待数秒后再试）
- **服务异常（5xx/超时）**：提示服务暂不可用，建议稍后重试；不要输出堆栈或内部信息

## 安全规则

- 不在对话中索取、输出或回显 `HUADAI_API_KEY`
- 不输出任何可能识别用户身份的敏感信息（除非用户明确提供并要求使用）
- 禁止在未调用 API 时返回“已保存/已删除/已找到”
- 禁止猜测或生成不存在的笔记 ID

