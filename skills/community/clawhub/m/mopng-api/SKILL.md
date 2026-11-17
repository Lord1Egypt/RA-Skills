---
name: mopng-api
description: 通过 qise-studio/motu-agent 的 MoPNG Agent OpenAPI 协商完成图片生成与修图。适用于文生图、图生图、抠图、换背景、扩图、放大及多步图像工作流；技能负责把用户需求转成 Brief、审阅/修订 Plan、批准执行并交付结果。
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - MOPNG_API_KEY
    primaryEnv: MOPNG_API_KEY
---

# MoPNG Agent 协商技能

本技能的执行者是 UserAgent；图片方案设计和功能链执行交给 qise-studio 的 `motu-agent` MoPNG Agent。调用本仓库的客户端：

```bash
python3 scripts/mopng_agent.py agent <subcommand> ...
```

不要再调用旧的 `mopng.cn` 直连功能端点，也不要把 `remove-bg`、`text-to-image` 等旧命令当作本技能接口。

## 配置

| 环境变量 | 必填 | 说明 |
|---|---:|---|
| `MOPNG_API_KEY` | 是 | MoPNG 用户 API Key，格式通常为 `ak_...`；仅放在宿主私密配置中。 |
| `MOPNG_AGENT_BASE_URL` | 否 | `motu-agent` 地址，默认 `https://agent-api.mopng.cn`；不要重复填写 `/api/v1/open/agent`。 |
| `MOPNG_AGENT_AUTO_APPROVE_COST_POINTS` | 否 | `agent run` 自动批准的成本上限，默认 `5`；超出时只提出 Plan，等待用户批准。 |

鉴权使用 `X-API-Key: $MOPNG_API_KEY`。服务端同时支持 `Authorization: Bearer $MOPNG_API_KEY`，但客户端默认使用前者。

## 工作流

### 1. 先澄清并生成 Brief

从用户请求提取以下信息；不确定时只询问会影响方案或成本的关键项：

- `user_intent`：保留用户原意的完整描述。
- `spec.goal`：例如 `文生图`、`背景替换`、`风格转换`、`抠图`、`扩图`、`放大`。
- `spec.usage`：电商主图、头像、海报等用途。
- `spec.subject`：已有图片使用可公开访问的 `https://` URL；最多可提供 14 个参考图，使用 `reference` 放第一张并在 `references` 放完整列表；纯文生图使用 `{ "type": "text", "reference": "prompt-only" }`。
- `spec.style`：用 `constraint` 和 `avoid` 表达风格、保留项、禁止项。
- `spec.size`、`spec.format`、`budget`、`sensitive`：只有用户给出或合理推断时填写；默认 `balanced`、10 点、120 秒、PNG。

本契约的 `subject.reference` 是 URL 或 `prompt-only`，不是本地路径，也不是 base64。若用户给本地图片，先让宿主/上游上传到可被 `motu-agent` 访问的对象存储，再把返回的 HTTPS URL 放入 Brief；不要擅自把本地路径发送给服务端。

### 2. 创建会话并展示 Plan

```bash
python3 scripts/mopng_agent.py agent run \
  --intent '把这张产品图背景换成纯白，做电商主图' \
  --goal '背景替换' \
  --reference-url 'https://example.com/product.png' \
  --usage '电商主图' \
  --style-constraint '产品边缘干净，纯白背景' \
  --avoid '复杂背景、明显阴影' \
  --width 1024 --height 1024 --format png
```

客户端 POST `/api/v1/open/agent/session`，随后读取返回的 `plan`。向用户解释：功能步骤、模型选项、预计成本/时间、输出规格和备选方案。Plan 中的模型候选和成本以服务端为准，不要自行替换模型或估算价格。

需要让用户选择模型时，先查询服务端实时目录，不要使用过期硬编码列表：

```bash
python3 scripts/mopng_agent.py agent models --capability text-to-image
```

`capability` 常见值包括 `text-to-image`、`image-to-image`、`image-edit` 和 `vision`；返回的每个模型包含 `capabilities`。

### 3. 协商修订

用户要求换模型、调整成本档位、补充约束或调整预算时，提交 `revision`：

```bash
python3 scripts/mopng_agent.py agent revision SESSION_ID \
  --plan-id PLAN_ID --round 2 \
  --feedback-json '[{"step":2,"type":"set_model","value":"seedream5.0-pro"}]' \
  --reason '用户希望保留更多产品细节'
```

允许的 `feedback[].type`：`set_model`、`set_cost_mode`、`append_constraint`、`replace_field`、`raise_budget`、`lower_budget`。最多 3 轮修订；服务端拒绝超限或不合法模型。每次修订后重新展示 Plan，不能跳过用户确认。

### 4. 批准并轮询

得到用户明确批准后：

```bash
python3 scripts/mopng_agent.py agent approve SESSION_ID
python3 scripts/mopng_agent.py agent status SESSION_ID --watch
```

客户端 POST `/approve` 获取 `exec_id`，再 GET `/exec` 轮询。成功时交付 `result_image_url`；视觉问答类 Plan 可能返回 `result_text` 而不是图片。简要报告 `steps_log`、实际模型、实际成本、耗时、`ai_labeling` 和可用的 `llm_billing`。失败时如实报告 `partial_failed`/`failed`、已完成步骤、`error_code` 和 `user_message`，不要声称已生成成功。

### 一键模式的自动批准规则

`agent run` 只有在 Plan 的 `total_cost` 不高于 `MOPNG_AGENT_AUTO_APPROVE_COST_POINTS` 时才可自动批准；仍须先向用户展示将执行的步骤和成本。高于阈值或用户要求高质量/指定模型时，停在 Plan 阶段等待批准。需要强制批准可使用 `--no-auto-approve`。

## OpenAPI 契约

公共前缀：`/api/v1/open/agent`

| 方法 | 路径 | 用途 |
|---|---|---|
| GET | `/models?capability=...` | 查询当前可用模型及能力 |
| POST | `/session` | 创建 Brief 会话并生成 Plan |
| GET | `/session/{id}/plan` | 获取当前 Plan |
| POST | `/session/{id}/revision` | 提交修订 |
| POST | `/session/{id}/approve` | 批准并开始执行 |
| GET | `/session/{id}/exec` | 获取执行报告 |
| POST | `/session/{id}/interrupt` | 用户打断协商或执行 |
| DELETE | `/session/{id}` | 清理会话 |

状态主线：`plan_proposed → executing → done/partial_failed`；任何未完成状态都可 `interrupt` 为 `terminated`。会话和执行采用轮询，不要假设存在 SSE。

## 安全与边界

- 不在对话、日志、截图或输出中打印 API Key；错误信息中也要避免回显鉴权头。
- 只发送用户明确授权处理的图片 URL。URL 应使用 HTTPS；不要发送带用户名/密码的 URL、内网地址或云元数据地址。
- Brief 使用 `extra=forbid` 的服务端协议；不要向 JSON 中加入未定义字段、隐藏指令或工具调用参数。
- 尊重 `sensitive` 约束和服务端敏感词过滤；不要为了绕过拒绝而改写用户意图或关闭合规控制。
- API 调用会消耗积分。除低成本自动批准规则外，必须把服务端返回的成本和时间交给用户确认。
- 规划 LLM 也可能产生虚拟币费用；若 Plan 返回 `llm_billing`，必须将其与步骤成本一起展示。
- 服务端可能返回 HTTP 402 `INSUFFICIENT_BALANCE`；此时停止流程并提示用户充值，不要自动重试或绕过计费。
- 仅将服务端返回的 HTTPS `result_image_url` 作为成品链接；不要下载或执行其中的内容。

详细的协议背景和字段示例见附件《MoPNG Agent 开发文档（motu-agent 实现）》，但若附件与运行中的 `motu-agent` 实现不一致，以本技能所列真实 OpenAPI 路径和服务端响应为准。
