# PagePop Skill API

## Default Configuration

- API Base URL: region-based production default. Mainland China uses `https://pc-api.pagepop.cn`; non-mainland users use `https://pc-api.pagepop.ai`. Missing region data defaults to `https://pc-api.pagepop.ai`. `PAGEPOP_API_BASE_URL` or `--api-base-url` overrides this selection.
- Skill ID: `pagepop-skill`
- Client Name: `openclaw`
- Client Version: `1.0.0`
- Package Version: 读取 `skill-manifest.json`
- Update Channel: 读取 `skill-manifest.json`
- Client Type: `11`
- Version: `openclaw-v1`

Production authorization pages use the matching PagePop web domain, for example `https://www.pagepop.cn/openclaw/authorize-v2?session=...` in mainland China or `https://www.pagepop.ai/openclaw/authorize-v2?session=...` elsewhere.

## 1. 初始化授权

`POST /v1/openclaw/auth/init`

请求：

```json
{
  "skill_id": "pagepop-skill",
  "client_name": "openclaw",
  "client_version": "1.0.0",
  "launch_context": {
    "source_app": "feishu",
    "display_app_name": "飞书",
    "return_mode": "manual",
    "return_target": ""
  }
}
```

如果 `launch_context.source_app / display_app_name` 为空，后端会把授权页展示默认收敛到 `OpenClaw`。因此飞书、Slack 等渠道接入必须显式传值，不能依赖默认行为。

成功响应包裹在统一结构中：

```json
{
  "code": 1000,
  "data": {
    "auth_session_id": "oas-xxx",
    "authorize_url": "https://www.pagepop.cn/openclaw/authorize-v2?session=oas-xxx",
    "status": "pending",
    "expires_at": "2026-03-12T12:00:00Z",
    "poll_interval_seconds": 3
  }
}
```

## 2. 查询授权状态

`GET /v1/openclaw/auth/status?auth_session_id=oas-xxx`

处理中：

```json
{
  "code": 1000,
  "data": {
    "status": "pending",
    "expires_at": "2026-03-12T12:00:00Z",
    "launch_context": {
      "source_app": "feishu",
      "display_app_name": "飞书",
      "return_mode": "manual",
      "return_target": ""
    }
  }
}
```

授权成功：

```json
{
  "code": 1000,
  "data": {
    "status": "authorized",
    "expires_at": "2026-03-12T12:00:00Z",
    "access_key": "pp_sk_xxx",
    "user": {
      "id": 12345,
      "name": "Alice"
    },
    "launch_context": {
      "source_app": "feishu",
      "display_app_name": "飞书",
      "return_mode": "manual",
      "return_target": ""
    }
  }
}
```

失败时通常会带：

- `reason`
- `metadata.openclaw_reason`

## 3. Skill 更新检查

`GET /v1/openclaw/skill/update?skill_id=pagepop-skill&package_version=2026.04.21-r8&channel=prod`

成功响应：

```json
{
  "code": 1000,
  "data": {
    "current_version": "2026.04.21-r8",
    "latest_version": "2026.04.22-r1",
    "min_supported_version": "2026.04.20-r4",
    "update_level": "recommended",
    "download_url": "https://github.com/pagepop/skills/releases/download/pagepop-skill-v2026.04.22-r1/pagepop-skill-prod-2026.04.22-r1.zip",
    "sha256": "abc123",
    "repo": "pagepop/skills",
    "release_tag": "pagepop-skill-v2026.04.22-r1",
    "published_at": "2026-04-22T10:00:00+08:00",
    "release_notes": [
      "Improve artifact delivery rendering.",
      "Fix authorization return guidance."
    ],
    "message": "A newer PagePop skill package is available."
  }
}
```

`update_level` 约定：

- `none`
- `recommended`
- `required`

如果后端没有配置更新策略，或当前 `skill_id/channel` 没有匹配策略，skill 会把这一步静默视为 `none`，不影响正常授权和调用。

当前这是“更新通知”机制，不是自动安装机制。skill 只输出 `skill_update_available` 或 `skill_update_required` 事件，并携带 `download_url`、`sha256`、`release_tag` 等信息；下载、SHA-256 校验、解压安装、以及重启 skill 进程由宿主或用户完成。

默认情况下，skill 在授权阶段不会持续阻塞轮询这个接口直到浏览器确认完成，而是会先输出授权链接并结束本次运行；宿主应用应先把链接展示给用户，再在用户完成授权后重新调用同一个命令。

默认情况下，skill 还会把最近一次成功对话的 `conversation_id` 持久化为本地 `active_conversation_id`。后续 `stream` 调用如果没有显式传 `conversation_id`，会默认继续这轮对话。
同时，skill 会把最近保存过的会话写入本地 `saved_conversations`，供 `Switch chat` 流程选择历史会话。

注意：`stream --goal ...` 表示“提交一轮新的用户请求并拉流”，即使它继续的是同一个 `conversation_id`，也会先调用 `POST /v2/chat`。如果宿主只是想查看已有任务状态、回放已有事件、或在断流后续拉结果，应使用：

```bash
python3 scripts/pagepop_skill.py resume-stream --conversation-id conv_xxx --offset 0
```

`resume-stream` 只调用 `GET /v2/sse/events`，不会提交新的 chat，也不会清理本地 `pending_run`。如果没有显式传 `--offset`，它会使用该 `conversation_id` 本地保存的 `cursor_offset`；没有本地 cursor 时从 `0` 开始。如果没有传 `--conversation-id` 或 `--resume-conversation-id`，它会使用本地 `active_conversation_id`；三者都不存在时会报错。

SSE offset 是当前服务端队列缓存内的 cursor，不是 conversation 维度永久递增的最大值。服务端缓存过期后，下一轮 chat 返回的 `sse_max_offset` 可能小于本地记录，甚至重新从 `0` 或 `1` 开始。skill 会以本轮 `POST /v2/chat` 返回的 `sse_max_offset` 作为拉流起点，并在收到 SSE 事件时把本地 `cursor_offset` 更新为事件中的 offset，即使该 offset 小于本地旧值。

## 4. Chat 提交

`POST /v2/chat`

请求头：

- `X-Pagepop-Skill-Key`
- `X-Pagepop-Skill-Id`
- `X-Pagepop-Client: openclaw`

请求体：

```json
{
  "conversation_id": "",
  "msg": "Generate an investor deck about our AI product",
  "client_type": 11,
  "links": ["https://example.com/reference"],
  "message_id": "uuid",
  "meta": {
    "source": "openclaw",
    "skill_id": "pagepop-skill",
    "artifact_type": "auto"
  },
  "version": "openclaw-v1"
}
```

成功：

```json
{
  "code": 1000,
  "data": {
    "conversation_id": "conv_xxx",
    "sse_max_offset": 0
  }
}
```

## 5. SSE 拉流

`GET /v2/sse/events?conversation_id=conv_xxx&offset=0`

请求头与 chat 相同。

服务端会返回标准 SSE：

### 业务消息

```text
event: message
data: {"conversation_id":"conv_xxx","message_id":"msg_xxx","type":"message","status":"","data":"...","offset":1}
```

### 流控消息

```text
event: control
data: {"conversation_id":"conv_xxx","cmd":"done","offset":12}
```

常见 `cmd`：

- `heartbeat`
- `status`
- `retry`
- `manual_retry`
- `error`
- `done`
- `paused`
- `cancled`

## 6. 本地透传格式

首次使用未授权时，脚本会先输出：

如果当前运行仍在使用默认来源上下文，脚本还会先输出一条面向接入方的 warning：

```json
{
  "kind": "integration_warning",
  "title": "Using default authorization context",
  "message": "This run will label the authorization page as OpenClaw. That is expected for direct OpenClaw usage. If the skill is invoked from Feishu, Slack, or another host app, set source_app and display_app_name before calling auth/init.",
  "action_text": "Configure launch context",
  "result_hint": "For example, set PAGEPOP_SKILL_SOURCE_APP=feishu and PAGEPOP_SKILL_DISPLAY_APP_NAME=飞书 before running auth.",
  "current_source_app": "",
  "current_display_app_name": "OpenClaw"
}
```

如果后端返回了新的版本策略，脚本还会在进入授权或真正发请求前先输出：

```json
{
  "kind": "skill_update_available",
  "current_version": "2026.04.21-r8",
  "latest_version": "2026.04.22-r1",
  "min_supported_version": "2026.04.20-r4",
  "update_level": "recommended",
  "download_url": "https://github.com/pagepop/skills/releases/download/pagepop-skill-v2026.04.22-r1/pagepop-skill-prod-2026.04.22-r1.zip",
  "sha256": "abc123",
  "repo": "pagepop/skills",
  "release_tag": "pagepop-skill-v2026.04.22-r1",
  "published_at": "2026-04-22T10:00:00+08:00",
  "release_notes": [
    "Improve artifact delivery rendering."
  ],
  "message": "A newer PagePop skill package is available."
}
```

如果更新已被后端标记为 `required`，脚本会先输出：

```json
{
  "kind": "skill_update_required",
  "current_version": "2026.04.20-r1",
  "latest_version": "2026.04.22-r1",
  "min_supported_version": "2026.04.21-r8",
  "update_level": "required",
  "download_url": "https://github.com/pagepop/skills/releases/download/pagepop-skill-v2026.04.22-r1/pagepop-skill-prod-2026.04.22-r1.zip",
  "sha256": "abc123",
  "repo": "pagepop/skills",
  "release_tag": "pagepop-skill-v2026.04.22-r1",
  "published_at": "2026-04-22T10:00:00+08:00",
  "release_notes": [
    "Improve artifact delivery rendering."
  ],
  "message": "Your installed PagePop skill package is no longer supported."
}
```

随后脚本会立即中断当前命令，要求先升级 skill 包。

随后才会输出：

```json
{
  "kind": "auth_required",
  "auth_session_id": "oas-xxx",
  "authorize_url": "https://www.pagepop.cn/openclaw/authorize-v2?session=oas-xxx",
  "title": "Authorize PagePop before first use",
  "message": "Open the authorization page in your browser and confirm once before using this skill.",
  "action_text": "Open authorization page",
  "result_hint": "After authorization, return to the source app and continue the current request.",
  "is_reauth": false,
  "requires_user_action": true,
  "pause_execution": true,
  "resume_mode": "rerun_same_command",
  "host_instruction": "Display authorize_url to the user and stop this run. After the user completes authorization in the browser, invoke the same skill command again."
}
```

这条 `auth_required` 事件本身就是一个“暂停并交给用户”的信号：

- skill 输出它之后会结束当前运行
- 宿主应用应把 `authorize_url` 交给用户，而不是等待 skill 自己完成授权
- 用户在浏览器确认授权后，再次调用同一个 skill 命令即可

如果显式带了 `--wait-for-authorization`，脚本才会继续输出：

```json
{
  "kind": "auth_polling",
  "auth_session_id": "oas-xxx",
  "status": "pending",
  "expires_at": "2026-03-12T12:00:00Z"
}
```

这个阻塞等待模式主要用于本地命令行调试，不建议作为宿主平台的默认集成方式。

如果本地已有活跃会话，而这次调用没有显式传 `conversation_id`，脚本会先输出：

```json
{
  "kind": "chat_context",
  "mode": "continue",
  "conversation_id": "conv_prev",
  "label": "布偶猫入门指南",
  "last_goal": "先生成一版布偶猫入门指南",
  "saved_conversation_count": 3,
  "actions": [
    {"id": "new_chat", "label": "New chat"},
    {"id": "switch_chat", "label": "Switch chat"}
  ],
  "title": "Continuing current chat",
  "message": "This request will continue your current PagePop conversation by default.",
  "result_hint": "Use New chat for a clean context, or list saved conversations and choose one to continue."
}
```

如果调用方显式传了 `--new-conversation`，脚本会先输出：

```json
{
  "kind": "chat_context",
  "mode": "new",
  "conversation_id": "",
  "label": "",
  "last_goal": "",
  "saved_conversation_count": 3,
  "actions": [
    {"id": "new_chat", "label": "New chat"},
    {"id": "switch_chat", "label": "Switch chat"}
  ],
  "title": "Starting a new chat",
  "message": "This request will start a fresh PagePop conversation without reusing the previous context.",
  "result_hint": "Use New chat for a clean context, or list saved conversations and choose one to continue."
}
```

随后才会真正发起一轮新的 `POST /v2/chat`。

如果只需要继续读取某个已有会话的 SSE，而不是提交新的用户请求，可以调用：

```bash
python3 scripts/pagepop_skill.py resume-stream --conversation-id conv_xxx --offset 12
```

如果省略 `--offset`，skill 会读取本地保存的 `cursor_offset`：

```bash
python3 scripts/pagepop_skill.py resume-stream --conversation-id conv_xxx
```

这会先输出：

```json
{
  "kind": "stream_resumed",
  "conversation_id": "conv_xxx",
  "offset": 12,
  "offset_source": "state",
  "message": "Resuming existing PagePop SSE stream without submitting a new chat request."
}
```

然后直接请求 `GET /v2/sse/events?conversation_id=conv_xxx&offset=12`。这个命令不会调用 `/v2/chat`，适合宿主用于“查状态/续拉/回放结果”。

如果宿主应用需要列出历史会话供用户切换，可以单独调用：

```json
{
  "kind": "conversation_history",
  "active_conversation_id": "conv_prev",
  "items": [
    {
      "conversation_id": "conv_prev",
      "label": "布偶猫入门指南",
      "last_goal": "先生成一版布偶猫入门指南",
      "artifact_type": "rednote",
      "last_activity_at": "2026-04-22T10:00:00Z"
    },
    {
      "conversation_id": "conv_old",
      "label": "露营装备推荐",
      "last_goal": "做一版露营装备推荐",
      "artifact_type": "rednote",
      "last_activity_at": "2026-04-21T09:00:00Z"
    }
  ]
}
```

宿主拿到列表后，可以再用 `--resume-conversation-id <id>` 显式继续某个历史会话。

本地 key 失效需要重授权时，会先输出：

```json
{
  "kind": "access_key_reset",
  "reason": "SKILL_KEY_EXPIRED",
  "message": "Open the authorization page again and confirm once to continue.",
  "backend_message": "skill key expired",
  "title": "PagePop authorization expired",
  "action_text": "Re-authorize PagePop",
  "result_hint": "After authorization, return to the source app and continue the current request.",
  "is_reauth": true
}
```

长耗时阶段，脚本还会补充用户可读的进度事件：

```json
{
  "kind": "progress_update",
  "conversation_id": "conv_xxx",
  "stage": "tool",
  "status": "begin",
  "event": "message",
  "raw_type": "tool_call",
  "name": "finish_work",
  "summary": "PagePop started final artifact generation."
}
```

当脚本从 `finish_work` 或 `artifact` 事件里提炼到产物摘要时，会输出：

```json
{
  "kind": "artifact_update",
  "conversation_id": "conv_xxx",
  "artifact": {
    "source": "finish_work",
    "conversation_id": "conv_xxx",
    "message_id": "msg_xxx",
    "artifact_id": "outline_xxx",
    "artifact_type": "slide",
    "status": "begin",
    "title": "Quarterly review deck",
    "current_version": 2,
    "urls": [
      "https://example.com/slide-1.png",
      "https://example.com/slide-2.png"
    ],
    "ready": false
  }
}
```

当脚本判断该产物已完成时，会再补一条：

```json
{
  "kind": "artifact_ready",
  "conversation_id": "conv_xxx",
  "artifact": {
    "artifact_id": "outline_xxx",
    "artifact_type": "slide",
    "title": "Quarterly review deck",
    "urls": [
      "https://example.com/slide-1.png",
      "https://example.com/slide-2.png"
    ],
    "ready": true
  }
}
```

为了让不同 channel 共用同一份“交付语义层”，脚本还会补一条渠道无关的交付事件：

```json
{
  "kind": "artifact_delivery",
  "conversation_id": "conv_xxx",
  "artifact": {
    "id": "artifact_xxx",
    "type": "rednote",
    "title": "Ragdoll Cat Guide",
    "status": "done",
    "pages": 3,
    "current_version": 2,
    "text": "Ragdoll cats are gentle, beautiful, and friendly for first-time cat owners.",
    "text_preview": "Ragdoll cats are gentle, beautiful, and friendly for first-time cat owners.",
    "image_urls": [
      "https://example.com/cover-1.png",
      "https://example.com/cover-2.png"
    ],
    "resource_links": [
      {
        "label": "Export JSON",
        "url": "https://example.com/export.json"
      }
    ],
    "pagepop_project_url": "https://www.pagepop.cn/project?cid=conv_xxx",
    "ready": true
  },
  "presentation": {
    "headline": "Generated \"Ragdoll Cat Guide\"",
    "subtitle": "Rednote Post · 3 pages",
    "summary": "Ragdoll cats are gentle, beautiful, and friendly for first-time cat owners.",
    "preview_images": [
      "https://example.com/cover-1.png",
      "https://example.com/cover-2.png"
    ],
    "actions": [
      "Help me change the color palette",
      "Add one more page about pricing"
    ],
    "resources": [
      {
        "label": "Open in PagePop",
        "url": "https://www.pagepop.cn/project?cid=conv_xxx"
      },
      {
        "label": "Export JSON",
        "url": "https://example.com/export.json"
      }
    ],
    "fallback_text": "Generated \"Ragdoll Cat Guide\"\nRednote Post · 3 pages\nRagdoll cats are gentle, beautiful, and friendly for first-time cat owners.\nOpen in PagePop for the full rendered view: https://www.pagepop.cn/project?cid=conv_xxx"
  },
  "channel_presentations": {
    "preferred": "feishu",
    "slack": {
      "format": "slack_block_kit",
      "fallback_text": "Generated \"Ragdoll Cat Guide\"\nRednote Post · 3 pages\nRagdoll cats are gentle, beautiful, and friendly for first-time cat owners.\nOpen in PagePop for the full rendered view: https://www.pagepop.cn/project?cid=conv_xxx",
      "blocks": [
        {
          "type": "header",
          "text": {
            "type": "plain_text",
            "text": "Generated \"Ragdoll Cat Guide\"",
            "emoji": true
          }
        },
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "Ragdoll cats are gentle, beautiful, and friendly for first-time cat owners."
          }
        },
        {
          "type": "actions",
          "elements": [
            {
              "type": "button",
              "text": {
                "type": "plain_text",
                "text": "Open in PagePop",
                "emoji": true
              },
              "url": "https://www.pagepop.cn/project?cid=conv_xxx",
              "style": "primary"
            }
          ]
        }
      ]
    },
    "feishu": {
      "format": "feishu_interactive_card",
      "fallback_text": "Generated \"Ragdoll Cat Guide\"\nRednote Post · 3 pages\nRagdoll cats are gentle, beautiful, and friendly for first-time cat owners.\nOpen in PagePop for the full rendered view: https://www.pagepop.cn/project?cid=conv_xxx",
      "card": {
        "config": {
          "wide_screen_mode": true
        },
        "header": {
          "template": "blue",
          "title": {
            "tag": "plain_text",
            "content": "Generated \"Ragdoll Cat Guide\""
          }
        },
        "elements": [
          {
            "tag": "div",
            "text": {
              "tag": "lark_md",
              "content": "**Rednote Post · 3 pages**\n\nRagdoll cats are gentle, beautiful, and friendly for first-time cat owners."
            }
          },
          {
            "tag": "action",
            "actions": [
              {
                "tag": "button",
                "text": {
                  "tag": "plain_text",
                  "content": "Open in PagePop"
                },
                "url": "https://www.pagepop.cn/project?cid=conv_xxx",
                "type": "primary"
              }
            ]
          }
        ]
      },
      "media": {
        "preview_image_urls": [
          "https://example.com/cover-1.png",
          "https://example.com/cover-2.png"
        ],
        "image_upload_required": true
      }
    }
  },
  "target": {
    "source_app": "feishu",
    "preferred_channel": "feishu"
  },
  "debug": {
    "conversation_id": "conv_xxx",
    "message_id": "msg_xxx",
    "artifact_id": "artifact_xxx",
    "source": "finish_work",
    "scope_id": ""
  }
}
```

建议 channel 侧这样消费：

- 飞书、Slack 等富渲染宿主：优先读取 `channel_presentations.<source_app>`。
- 飞书图片需要宿主侧上传换取图片 key；skill 只在 `channel_presentations.feishu.media.preview_image_urls` 暴露待上传 URL。
- 飞书不要把通用 `presentation.fallback_text`、`artifact.text`、或 `sse_event.data` 里的裸 URL 直接渲染为 `lark_md`；优先用 `channel_presentations.feishu.card` 的 button `url` 字段。
- skill 会尝试把图片 URL 下载到本地 `PAGEPOP_SKILL_ARTIFACT_DIR`，未配置时默认写入当前工作区的 `.pagepop-artifacts/`。宿主应优先把 `channel_presentations.feishu.media.local_image_messages` 作为飞书图片消息发送，而不是把图片 URL 发成文本。
- 如果宿主或 agent 必须在飞书里输出纯文本，使用 `channel_presentations.feishu.plain_text` 或 `artifact.display_text`。这些字段会移除图片裸 URL，并把其他 URL 中的 `_` 编码为 `%5F`，避免飞书自动链接只截到第一个下划线。
- 原始文本仍保留在 `artifact.text`，仅供调试或导出，不适合作为飞书 `lark_md` 直接发送。
- 不支持富卡片：直接展示 `presentation.fallback_text`
- 轻量富文本：展示 `headline / subtitle / summary / actions`
- richer renderer：展示 `preview_images / resources`，并优先把 `Open in PagePop` 渲染成跳转入口，再把 `debug` 折叠到详情区

脚本不会做产物归一化，只把上游 SSE 包一层 JSON Line 输出：

```json
{
  "kind": "sse_event",
  "event": "message",
  "raw_data": "{\"conversation_id\":\"conv_xxx\",\"offset\":1}",
  "data": {
    "conversation_id": "conv_xxx",
    "offset": 1
  }
}
```

`raw_data` 永远保留原始文本，供宿主应用自行解析。
