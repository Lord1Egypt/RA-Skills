---
name: hd-notes-skills
description: |
  话袋笔记 - 通过话袋 OpenAPI 新建、更新和搜索个人笔记。

  当以下情况时使用此 Skill：
  (1) 用户要保存内容到笔记：「记一下」「存到笔记」「保存」
  (1.5) 用户要收藏某条笔记：「收藏这条」「收藏一下」
  (2) 用户要更新内容到笔记：「更新一下」「更新笔记」「补充到这条」
  (3) 用户要搜索或查看笔记：「搜一下」「找找笔记」「打开某条笔记」「笔记详情」
  (4) 用户要配置话袋笔记：「配置话袋」「连接话袋笔记」「授权话袋」「怎么填 Key」
version: 1.1.0
homepage: https://clawhub.ai/monkeydb/hd-notes-skills
user-invocable: true
metadata:
  openclaw:
    emoji: "📝"
    primaryEnv: HUADAI_API_KEY
    requires:
      env:
        - HUADAI_API_KEY
    envVars:
      - name: HUADAI_API_KEY
        required: true
        description: 话袋开放平台 API Key（请求头 Authorization）
    baseUrl: "https://openapi.ihuadai.cn/open/api/v1"
    homepage: "https://clawhub.ai/monkeydb/hd-notes-skills"
    repository: "https://github.com/monkeyDB/hd-notes-skills"
---

# 话袋笔记 Skill

## Agent 必读约束

- **唯一 Base URL**：`https://openapi.ihuadai.cn/open/api/v1`。禁止使用其他域名，禁止重复拼接 `/open/api/v1`。
- **鉴权方式**：业务 API 仅使用请求头 `Authorization: <HUADAI_API_KEY>`。
- **API Key 来源**：用户需先在 [话袋开放平台](https://ihuadai.cn/desktop/openai) 创建 API Key。如果用户未配置，引导用户创建并配置 `HUADAI_API_KEY`。
- **数据真实性**：所有笔记内容、搜索结果、笔记 ID 都必须来自 API 响应。禁止编造「已保存」「已找到」「已更新」。
- **写操作确认**：只有 API 返回 `code=200` 后，才能回复用户已保存或已更新。
- **更新笔记约束**：`unique_id` 必须来自搜索结果或用户明确提供，禁止猜测或生成已有笔记 ID。
- **密钥安全**：不要在对话中要求用户粘贴 API Key，不要回显、记录、总结或展示 `HUADAI_API_KEY`。

## 快速开始：配置 API Key

如果还没有配置 `HUADAI_API_KEY`，引导用户：

- 打开 https://ihuadai.cn/desktop/openai 创建 API Key
- 设置环境变量：`export HUADAI_API_KEY=<你的Key>`

## 文档索引

| 文档 | 内容 | 何时读取 |
|------|------|----------|
| [API 参考](references/api.md) | 完整请求体、curl 示例、响应判断、错误码 | 需要构造 API 调用或处理错误时 |

## 指令路由表

| 指令 | 角色 | 说明 | 详细文档 |
|------|------|------|----------|
| `/huadai config` 或「配置话袋」 | 配置 | 引导用户到开放平台创建并配置 API Key | [API 参考](references/api.md) |
| `/huadai upload` 或「记一下/保存」 | 新建 | 新建 Block 笔记 | [API 参考](references/api.md#新建笔记) |
| `/huadai update` 或「更新笔记」 | 更新 | 搜索确认目标后更新 Block 内容 | [API 参考](references/api.md#更新笔记) |
| `/huadai search` 或「搜一下」 | 搜索 | 关键词检索笔记 | [API 参考](references/api.md#搜索笔记) |

## 自然语言路由

| 用户说法（示例） | 路由 | 执行方式 |
|------------------|------|----------|
| 「授权话袋」「连接话袋笔记」「配置话袋」「怎么填 Key」 | Config | 不调用业务 API，引导配置 `HUADAI_API_KEY` |
| 「新建/上传/保存/写入到笔记」「记一下」 | Upload | `POST /block/upload-block` |
| 「更新/修改笔记」「补充到这条」 | Update | 先确认 `unique_id`，再 `POST /block/update-block` |
| 「搜/找/检索/有哪些相关笔记」 | Search | `GET /search` |

## API 路由表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/search` | 关键词搜索笔记 |
| GET | `/block/:unique_id` | 获取单条笔记详情 |
| POST | `/block/upload-block` | 新建笔记 |
| POST | `/block/update-block` | 更新笔记 |

完整 URL 等于 Base URL + 路径。例如：`https://openapi.ihuadai.cn/open/api/v1/search`。

## 执行规则

### 搜索笔记

- 调用 `GET /search?query=<关键词>&page=1&size=10`。
- 无结果时明确回复「未找到」，不要编造类似笔记。
- 从响应中提取关键信息展示给用户：
  - `unique_id` — 笔记唯一标识（更新/查详情时需要）
  - `content` — Quill Delta 数组，提取 `insert` 字段拼接为纯文本摘要
  - `create_time` / `update_time` — Unix 时间戳，可转为可读时间
  - `type` — 笔记类型
- 展示结果时优先给标题/摘要/`unique_id`，方便用户选择要更新哪条。
- 如果结果超过一页（`total > size`），提示用户缩小搜索范围或翻页。

### 获取笔记详情

- 调用 `GET /block/:unique_id` 查看笔记完整内容。
- 仅在用户明确要求查看某条笔记详情，或需要获取完整内容用于更新时使用。

### 新建笔记

- 为新笔记生成新的 `unique_id`，格式：`b_<unix_time>_<random8>`。
- 普通文本笔记使用 `type=1`。
- `content` 直接传 Markdown 字符串。后端会自动转为 Quill Delta，无需手动构建数组。
- `create_time` 使用当前 Unix 秒。
- `status=1` 表示正常笔记。
- `is_collect=0` 表示非收藏笔记（必填，`0`=否 `1`=是）。
- `is_todo=0` 表示非待办笔记（必填，`0`=否 `1`=是）。

### 更新笔记

- 更新前必须确认目标 `unique_id`。
- 如果用户没有提供明确 `unique_id`，先搜索，再让用户确认或选择最匹配的一条。
- `content` 传更新后的完整 Markdown 字符串。
- `status=1` 表示正常笔记。
- `is_collect=0` 表示非收藏笔记（必填，`0`=否 `1`=是）。
- `is_todo=0` 表示非待办笔记（必填，`0`=否 `1`=是）。
- 不要只发送「追加内容」并假装已合并，除非 API 请求体确实包含最终要保存的内容。

## 脚本调用指引

本 Skill 提供了 `scripts/` 目录下的辅助脚本。在环境中配置了 `HUADAI_API_KEY` 后，可以直接执行：

```bash
# 搜索笔记
./scripts/search.sh "关键词"

# 新建笔记
./scripts/upload.sh "笔记内容（Markdown）"

# 更新笔记
./scripts/update.sh <unique_id> "新内容"
```

Agent 可优先选择调用脚本而非手动拼接 curl。脚本已处理参数校验、错误处理和响应格式化。

## 通用错误处理

| code | 处理方式 |
|------|----------|
| 200 | 成功。写操作可回复已保存/已更新 |
| 400001 | API Key 无效，引导用户重新创建并配置 API Key |
| 400003 | 无权限访问该资源 |
| 400018 | 笔记不存在，提示重新搜索确认 |
| 400024 | 需要有效会员，引导用户在话袋开通对应权益 |
| 500000 | 服务异常，提示稍后重试 |

## 安全规则

- 不输出 API Key。
- 不保存 API Key 到笔记正文。
- 不在未调用 API 或 API 未成功时声称操作完成。
- 不猜测已有笔记 ID、用户身份、隐藏内容。
- 不泄露搜索结果以外的任何用户数据。
