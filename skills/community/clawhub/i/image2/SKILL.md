---
name: image2
version: 1.0.0
description: 使用 image2 接口创建图片生成任务（文生图/参考生图）。当用户提到"生成图片""图生图""海报图""封面图"，或明确要求比例（如 16:9、9:16）时应使用本 skill。调用接口 /api/v1/user_task/asyncCreateWithCost，核心参数含 user_input.modelType（text2img/img2img）、prompt、size、urls（img2img 必填，最多 8 张）。需 x-api-key（kexiangai.com）。Do NOT use for video generation, OCR, or non-generative image editing.
metadata:
  requires:
    bins: ["curl", "python3"]
    env: ["X_API_KEY"]
  network:
    endpoints: ["https://kexiangai.com/api/v1/user_task/asyncCreateWithCost", "https://kexiangai.com/api/v1/user_task/get/passAuth/{id}"]
  secrets:
    primary: "X_API_KEY"
  storage:
    optional: ["~/.config/image2/.env (only when user explicitly enables --use-local-key)"]
---

## 安全声明（ClawHub 扫描友好）

- 本技能会访问外部接口：`/api/v1/user_task/asyncCreateWithCost`。
- 接口提供方为可想 AI（`kexiangai.com` 生态），调用前应由用户自行确认可信性与合规性。
- 默认不从本地配置文件读取密钥；仅当用户明确使用 `--use-local-key` 时才读取 `~/.config/image2/.env`。
- 推荐优先使用会话级环境变量 `X_API_KEY`，避免不必要的本地持久化。

## 运行依赖与环境变量

- 必需二进制：`curl`、`python3`
- 本地密钥读取相关：`grep`、`cut`、`tr`、`tail`（仅 `--use-local-key` 模式）
- 必需环境变量：`X_API_KEY`（推荐）
- 可选环境变量：`IMAGE2_BASE_URL`（默认 `https://kexiangai.com`）

你是 "image2 任务创建与查询" 技能。你的职责是稳定、可重复地创建 image2 图片任务，并在创建成功后主动查询直到返回最终结果。

## CRITICAL

- 调用接口前必须完成参数校验，不能跳过。
- 不得泄露完整 `x-api-key`，日志与回显仅允许掩码展示。
- 用户未提供必填信息时，先补齐再调用 API。
- `img2img` 模式下 `urls` 为必填，且最多 8 张。
- **单轮对话只允许创建一次任务，绝不重复提交同参数任务。**
- **禁止自动循环重试；任何重试都必须先说明可能继续消耗积分并获得用户明确同意。**
- API 创建的是异步任务：本技能必须在创建成功后继续调用查询接口，直到任务结束（成功或失败）。

## 何时使用

- 用户想创建 image2 文生图任务（`text2img`）
- 用户想基于参考图创建任务（`img2img`）
- 用户需要指定比例（如 `1:1`、`3:4`、`16:9`）

触发短语示例：

- "帮我用 image2 生成一张海报"
- "按这几张图做 img2img"
- "给我创建一个 16:9 的封面图任务"
- "生成一张 3:4 的产品图"

## 何时不要使用

- 用户要做视频生成、视频处理或音频处理
- 用户要做 OCR、文档解析、表格识别
- 用户只需要非生成式编辑（裁剪、压缩、加边框等）

## 输入参数

- `x-api-key`：必填，请求头字段，获取地址 `kexiangai.com`
- `cost_type`：固定 `1`
- `business_url`：固定 `gpt-image2/img`
- `user_input.modelName`：默认 `GPT-Image-2`
- `user_input.modelType`：必填，`text2img` 或 `img2img`
- `user_input.prompt`：必填，字符串
- `user_input.size`：必填，比例字符串
- `user_input.urls`：`img2img` 必填，URL 字符串数组，最多 8 项

支持的 `size`：

- `auto`
- `1:1`
- `3:2`
- `2:3`
- `16:9`
- `9:16`
- `4:3`
- `3:4`
- `21:9`
- `9:21`
- `1:3`
- `3:1`
- `2:1`
- `1:2`

## 认证与 Key 复用

支持用户首次配置后长期复用，无需每次重复输入。

### Key 读取优先级（从高到低）

1. 本次对话显式输入的 `x-api-key`
2. 环境变量 `X_API_KEY`
3. 本地持久化文件 `~/.config/image2/.env`（仅在显式允许时读取）

### 首次配置（只需一次）

```bash
mkdir -p ~/.config/image2
cat > ~/.config/image2/.env << 'EOF'
X_API_KEY=你的x-api-key
EOF
chmod 600 ~/.config/image2/.env
```

## 核心接口

详细字段说明见 `references/api-guide.md`。

```bash
curl --location 'https://kexiangai.com/api/v1/user_task/asyncCreateWithCost' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--data '{
  "cost_type": 1,
  "business_url": "gpt-image2/img",
  "user_input": {
    "modelName": "GPT-Image-2",
    "modelType": "text2img",
    "prompt": "为护肤产品生成一张极简海报",
    "size": "3:4"
  }
}'
```

```bash
curl --location 'https://kexiangai.com/api/v1/user_task/get/passAuth/<TASK_ID>' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>'
```

## 工作流（必须按顺序执行）

### Step 1: 收集与补齐输入

- 必填：`prompt`、`modelType`、`size`
- 条件必填：`urls`（当 `modelType=img2img`）
- 必填认证：`x-api-key`（可从优先级策略自动读取）

### Step 2: 参数校验与归一化

- `modelType` 仅允许 `text2img` 或 `img2img`
- `size` 必须在支持列表内
- `prompt` 必须非空
- `img2img` 时：`urls` 必须为 URL 字符串数组，长度 1-8
- `text2img` 时：`urls` 默认为空数组（可省略）

### Step 3: 组装请求并调用 API

- 固定路径：`/api/v1/user_task/asyncCreateWithCost`
- 固定字段：`cost_type=1`、`business_url=gpt-image2/img`
- 请求头：`Content-Type: application/json` + `x-api-key`
- 调用前先输出"请求摘要 + 预计积分消耗提醒"，并等待用户确认（如"确认创建"）
- 创建成功后，记录任务 `id` 与参数摘要，避免同轮重复提交

### Step 4: 创建成功后立即提示并进入查询

- 先明确输出：任务已创建成功 + 任务 ID
- 紧接着调用查询接口：`/api/v1/user_task/get/passAuth/{id}`
- 对 `task_status` 为 `pending`/`running` 持续轮询
- 轮询间隔建议 5-10 秒，避免过于频繁请求

### Step 5: 直到返回最终结果再结束

- 当 `task_status=success`：返回最终结果（优先 `service_output.imgUrls`、其次 `service_output.imgUrl`）
- 当 `task_status=failed`/`error`/`canceled`：返回失败状态与 `service_output.failReason`
- 达到最大查询次数仍未结束：明确告知超时，并给出继续查询建议

## 标准错误处理

- 缺少 `x-api-key`：提示去 `kexiangai.com` 获取，并说明可用 `scripts/set_key.sh` 持久化
- 缺少 `prompt`：提示补充提示词后再创建
- `modelType` 非法：提示仅支持 `text2img`/`img2img`
- `size` 非法：返回支持列表并要求重选
- `img2img` 缺少 `urls`：提示至少提供 1 张参考图 URL
- `urls` 超过 8 张：提示精简到 8 张以内
- 401/403：提示 key 无效、过期或权限不足
- 429：提示限流，不自动重试
- 5xx：提示服务异常，建议用户确认后重试一次
- 查询阶段超时：提示任务可能仍在执行中，可继续按任务 ID 查询

## 防重复提交策略

- 默认策略：每个用户请求最多 1 次创建调用。
- 允许第 2 次调用的条件：用户明确要求"重试"或"修改参数后重建"。
- 已成功返回任务 ID 后，本轮对话禁止再次提交相同参数。

## 输出质量检查清单

在最终响应前逐项检查：

- 是否已完成必填参数校验
- 是否正确处理了 `img2img` 的 `urls` 约束
- 是否对 key 做了掩码处理
- 是否在创建成功后输出了任务 ID
- 是否已进入查询并持续到最终状态

## 可复用命令模板

```bash
# 1) 首次配置 key（只需一次）
mkdir -p ~/.config/image2
./scripts/set_key.sh

# 2) 会话变量方式（推荐）
export X_API_KEY='你的x-api-key'

# 3) text2img 任务创建
curl --location 'https://kexiangai.com/api/v1/user_task/asyncCreateWithCost' \
--header 'Content-Type: application/json' \
--header "x-api-key: $X_API_KEY" \
--data '{
  "cost_type": 1,
  "business_url": "gpt-image2/img",
  "user_input": {
    "modelName": "GPT-Image-2",
    "modelType": "text2img",
    "prompt": "生成科技风产品海报",
    "size": "16:9"
  }
}'

# 4) img2img 任务创建
curl --location 'https://kexiangai.com/api/v1/user_task/asyncCreateWithCost' \
--header 'Content-Type: application/json' \
--header "x-api-key: $X_API_KEY" \
--data '{
  "cost_type": 1,
  "business_url": "gpt-image2/img",
  "user_input": {
    "modelName": "GPT-Image-2",
    "modelType": "img2img",
    "prompt": "基于参考图生成新品海报",
    "size": "3:4",
    "urls": ["https://example.com/reference.png"]
  }
}'

# 5) 按任务 ID 查询
curl --location "https://kexiangai.com/api/v1/user_task/get/passAuth/${TASK_ID}" \
--header 'Content-Type: application/json' \
--header "x-api-key: $X_API_KEY"
```

## 快速执行脚本

- `./scripts/set_key.sh`：交互输入并保存 key 到 `~/.config/image2/.env`
- `echo '你的x-api-key' | ./scripts/set_key.sh --stdin`：从标准输入保存 key
- `X_API_KEY='你的x-api-key' ./scripts/create_task.sh --mode text2img --prompt "提示词" --size "3:4"`
- `X_API_KEY='你的x-api-key' ./scripts/create_task.sh --mode img2img --prompt "提示词" --size "3:4" --url "https://example.com/1.png"`
- 创建后脚本会自动查询直到任务结束，并输出最终结果

## 目录结构（标准）

- `SKILL.md`
- `scripts/set_key.sh`
- `scripts/create_task.sh`
- `references/api-guide.md`
- `assets/`

## 交互模板（对话时）

1. 尝试自动读取 key（`X_API_KEY`，必要时再走本地 `.env`）
2. 若缺 key，提示用户提供 `x-api-key`（`kexiangai.com`）
3. 收集 `modelType`（`text2img`/`img2img`）
4. 收集 `prompt` 与 `size`
5. 若 `img2img`，收集 `urls`（1-8 张）
6. 明确本次只创建一次任务
7. 调用创建接口，先提示任务 ID，再自动轮询查询接口直到返回最终结果

## 常见调试问题

### Skill 不触发

- 检查 `description` 是否覆盖真实表达（如"生成图片""图生图""16:9 封面图"）
- 可用调试问句：`When would you use the image2 skill?`

### 返回 pending 但用户以为失败

- 强调 `pending` 是正常中间状态
- 创建成功后必须继续查询，直到 `success` 或失败态

### 参数被拒绝

- 优先检查 `modelType`、`size`、`urls` 数量与格式
- 确认 `business_url` 固定为 `gpt-image2/img`
