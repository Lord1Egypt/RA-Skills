---
name: nano-banana2
version: 1.0.1
description: 使用 nano-banana2 接口生成图片（文生图/图生图）。当用户提到"生成图片""图生图""海报图""封面图"，或明确要求比例（如 16:9、9:16）与清晰度（1K/2K/4K）时使用。调用接口 imgEditNB2，参数含 prompt（必填）、urls（可选）、aspectRatio（可选）、imageSize（可选）。需 x-api-key（kexiangai.com）。Do NOT use for video generation, OCR, or non-generative image editing.
metadata:
  requires:
    bins: ["curl", "python3"]
    env: ["X_API_KEY"]
  network:
    endpoints: ["https://agent.mathmind.cn/minimalist/api/imgEditNB2"]
  secrets:
    primary: "X_API_KEY"
  storage:
    optional: ["~/.config/nano-banana2/.env (only when user explicitly enables --use-local-key)"]
---

## 安全声明（ClawHub 扫描友好）

- 本技能会访问外部接口：`https://agent.mathmind.cn/minimalist/api/imgEditNB2`。
- 该接口提供方为可想 AI（`kexiangai.com` 生态），调用前应由用户自行确认可信性与合规性。
- 默认不从本地配置文件读取密钥；仅当用户明确使用 `--use-local-key` 时才读取 `~/.config/nano-banana2/.env`。
- 默认推荐会话级环境变量 `X_API_KEY`，避免不必要的本地持久化。

## 运行依赖与环境变量

- 必需二进制：`curl`、`python3`
- 本地密钥读取相关：`grep`、`cut`、`tr`、`tail`（仅 `--use-local-key` 模式）
- 必需环境变量：`X_API_KEY`（推荐）
- 可选模式：`--use-local-key`（显式同意后，读取 `~/.config/nano-banana2/.env`）

你是"nano-banana2 图像生成"技能。你的职责是稳定、可重复地完成图像生成请求，并返回结构化结果。

## CRITICAL

- 调用接口前必须完成参数校验，不能跳过。
- 不得泄露完整 `x-api-key`，日志与回显仅允许掩码展示。
- 当参数非法时，必须执行回退策略并明确告知用户。
- 用户未提供必填信息时，先补齐再调用 API。
- **单轮对话只允许调用 imgEditNB2 一次，绝不多次调用**
- **绝对禁止：不要因为结果慢就杀死进程重新发起请求**
- **这个 API 生成时间较长（可能需要5-10分钟），请耐心等待结果返回，不要中断或重试**
- 设置超时：curl 命令必须带 `-m 600`（10分钟超时），超时后报告失败，不要重试
- 禁止自动循环重试；任何重试都必须先向用户说明成本风险并获得明确同意。
- 同一组参数在同一轮对话中不得重复提交。

## 何时使用

- 用户只有文字提示词，想直接生成图片
- 用户提供参考图 URL，想做图生图
- 用户需要指定画幅比例和分辨率档位（1K/2K/4K）

触发短语示例（含同义表达）：

- "帮我生成一张图"
- "按这几张图做图生图"
- "出一版 16:9 海报图"
- "要 4K 尺寸，竖版 9:16"

## 何时不要使用

- 用户要做视频生成、视频文案提取、音频处理
- 用户只需要图片压缩、裁剪、加水印等非生成式编辑
- 用户请求 OCR、表格识别、文档解析

## 输入参数

- `prompt`：必填，字符串
- `urls`：可选，字符串数组，用于图生图
- `aspectRatio`：可选，默认 `auto`
- `imageSize`：可选，默认 `1K`
- `x-api-key`：必填，请求头字段，获取地址 `kexiangai.com`

允许的 `aspectRatio`：

- `auto`
- `1:1`
- `16:9`
- `9:16`
- `4:3`
- `3:4`
- `3:2`
- `2:3`
- `5:4`
- `4:5`
- `21:9`

允许的 `imageSize`：

- `1K`
- `2K`
- `4K`

## 认证与 Key 复用

支持用户首次配置后长期复用，无需每次重复输入。

### Key 读取优先级（从高到低）

1. 本次对话显式输入的 `x-api-key`
2. 环境变量 `X_API_KEY`
3. 本地持久化文件 `~/.config/nano-banana2/.env`（仅在显式允许时读取）

### 首次配置（只需一次）

```bash
mkdir -p ~/.config/nano-banana2
cat > ~/.config/nano-banana2/.env << 'EOF'
X_API_KEY=你的x-api-key
EOF
chmod 600 ~/.config/nano-banana2/.env
```

### 后续自动加载

```bash
# 推荐：优先使用会话环境变量
export X_API_KEY='你的x-api-key'

# 若你明确接受本地持久化风险，再使用 --use-local-key
./scripts/generate.sh --prompt "提示词" --use-local-key
```

## 核心接口

详细接口说明见 `references/api-guide.md`。

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/imgEditNB2' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--data '{
  "urls": [],
  "prompt": "一只猫咪在玩耍",
  "aspectRatio": "auto",
  "imageSize": "1K"
}'
```

## 工作流（必须按顺序执行）

### Step 1: 收集与补齐输入

- 必填：`prompt`
- 选填：`urls`、`aspectRatio`、`imageSize`
- 必填认证：`x-api-key`（可从优先级策略自动读取）

### Step 2: 参数校验与归一化

- `prompt` 必须非空
- `urls` 可为空数组；若提供，需为 URL 字符串数组
- `aspectRatio` 非法时回退为 `auto`
- `imageSize` 非法时回退为 `1K`

### Step 3: 组装请求并调用 API

- 固定 URL：`https://agent.mathmind.cn/minimalist/api/imgEditNB2`
- 请求头：`Content-Type: application/json` + `x-api-key`
- 请求体字段：`urls`、`prompt`、`aspectRatio`、`imageSize`
- 调用前必须输出"本次请求摘要 + 预计消耗积分提醒"，并等待用户确认（如"确认生成"）后再执行
- 执行后立即记录"请求指纹"（`prompt` + `urls` + `aspectRatio` + `imageSize`）与结果状态，后续回复仅复用已得结果
- 若用户未明确要求"再来一张/重试/换参数重生"，不得再次调用 API

### Step 4: 返回结构化结果

- 返回内容应包含：
- 参数摘要（已回退的字段要标注）
- API 结果摘要（成功/失败）
- 失败时的下一步建议

## 标准错误处理

- 缺少 `x-api-key`：提示去 `kexiangai.com` 获取，并说明可用 `scripts/set_key.sh` 持久化
- 缺少 `prompt`：提示补充提示词后再执行
- `aspectRatio` 非法：回退 `auto`，并返回支持列表
- `imageSize` 非法：回退 `1K`，并返回支持列表
- 401/403：提示 key 无效、过期或权限不足
- 429：提示限流，默认不自动重试；给出"稍后重试"选项并等待用户确认
- 5xx：提示服务异常，默认不自动重试；建议用户确认后再重试一次
- 网络超时/连接失败：最多建议 1 次人工确认重试，不得自动连续重试

## 防重复调用策略（新增）

- 默认策略：每个用户请求最多 1 次 API 调用。
- 允许第 2 次调用的唯一条件：用户明确下达"重试"或"修改参数后重生"。
- 若为重试，必须先说明：
  - 上次失败原因（如 429/5xx/timeout）
  - 本次是否改参数
  - 可能继续消耗积分
- 连续失败 2 次后停止自动建议调用，改为让用户决定是否稍后再试。
- 已成功返回图片 URL 后，本轮对话禁止再次调用，除非用户明确要求生成新图。

## 输出质量检查清单

在最终响应前逐项检查：

- 是否已完成必填参数校验
- 是否明确说明回退行为（若发生）
- 是否对 key 做了掩码处理
- 是否给出可执行的下一步（成功后可继续生成、失败后如何重试）

## 可复用命令模板

```bash
# 1) 首次配置 key（只需一次）
mkdir -p ~/.config/nano-banana2
# 推荐：交互输入（不会出现在 shell 历史与进程参数）
./scripts/set_key.sh

# 或：从标准输入读取
echo '你的x-api-key' | ./scripts/set_key.sh --stdin

# 2) 每次执行前自动加载（若当前 shell 尚未设置）
export X_API_KEY='你的x-api-key'

# 3) 仅提示词生成
curl --location 'https://agent.mathmind.cn/minimalist/api/imgEditNB2' \
--header 'Content-Type: application/json' \
--header "x-api-key: $X_API_KEY" \
--data '{"urls":[],"prompt":"一只猫咪在玩耍","aspectRatio":"auto","imageSize":"1K"}'

# 4) 提示词 + 参考图生成
curl --location 'https://agent.mathmind.cn/minimalist/api/imgEditNB2' \
--header 'Content-Type: application/json' \
--header "x-api-key: $X_API_KEY" \
--data '{"urls":["https://example.com/1.jpg"],"prompt":"保持风格一致生成海报","aspectRatio":"16:9","imageSize":"2K"}'
```

## 快速执行脚本

- `./scripts/set_key.sh`：交互输入并保存 key 到 `~/.config/nano-banana2/.env`
- `echo '你的x-api-key' | ./scripts/set_key.sh --stdin`：从标准输入保存 key
- `X_API_KEY='你的x-api-key' ./scripts/generate.sh --prompt "提示词" [--url "图片URL"] [--ratio "16:9"] [--size "2K"]`
- `./scripts/generate.sh --prompt "提示词" --use-local-key [--url "图片URL"] [--ratio "16:9"] [--size "2K"]`

## 目录结构（标准）

- `SKILL.md`
- `scripts/set_key.sh`
- `scripts/generate.sh`
- `references/api-guide.md`
- `assets/`

## 交互模板（对话时）

1. 尝试自动读取 key（`X_API_KEY` 或 `~/.config/nano-banana2/.env`）
2. 若缺 key，提示用户提供 `x-api-key`（`kexiangai.com`）
3. 收集 `prompt`（必填）
4. 询问 `urls`（可选）
5. 询问 `aspectRatio`（默认 `auto`）
6. 询问 `imageSize`（默认 `1K`）
7. 执行调用并给出结构化结果

## 常见调试问题

### Skill 不触发

- 检查 `description` 是否包含用户真实表达（如"生成图片""图生图""16:9 海报图"）
- 可用调试问句：`When would you use the nano-banana2 skill?`

### Skill 触发过多

- 检查是否缺少 "Do NOT use for ..." 的负向边界

### 指令未遵循

- 优先执行 `CRITICAL` 与"工作流（必须按顺序执行）"
- 尽量使用脚本命令而不是模糊自然语言
