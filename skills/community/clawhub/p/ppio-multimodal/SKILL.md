---
name: ppio-multimodal
description: |
  使用 PPIO 执行多模态任务：文生图、图生图、文生视频、图生视频、TTS、STT。
  适用于：生成图片、生成视频、文字转语音、语音识别。
---

# PPIO 多模态执行

## 配置方式（三选一，按优先级）

### 方式1：配置文件（推荐）

创建文件 `~/.ppio/config.json`：

```json
{
  "api_key": "你的API_Key"
}
```

**一条命令完成配置：**
```bash
mkdir -p ~/.ppio && echo '{"api_key": "你的API_Key"}' > ~/.ppio/config.json
```

### 方式2：环境变量

```bash
export PPIO_API_KEY="你的API_Key"
```

### 方式3：直接传参

在请求中直接提供：`请用 API Key sk_xxx 生成一张图片...`

---

## API Key 读取逻辑

```
1. 检查用户消息中是否包含 API Key（sk_ 开头）
2. 检查配置文件 ~/.ppio/config.json
3. 检查环境变量 PPIO_API_KEY
4. 都没有 → 返回配置引导
```

**配置引导消息（仅在未配置时显示）：**

```
您还没有配置 PPIO 的 API Key。

快速配置（复制运行）：
mkdir -p ~/.ppio && echo '{"api_key": "你的Key"}' > ~/.ppio/config.json

获取 Key：https://ppio.com/settings/key-management
```

---

## 执行流程（重要！）

```
用户请求 → 识别任务 → 获取 Key → ⚠️ 先发提示 → 执行任务 → 返回结果
```

### ⚠️ 必须先发送进度提示

**在调用 API 之前，必须先回复用户一条消息：**

```
🎨 收到！正在为您生成图片...

任务类型：文生图
使用模型：Seedream 5.0 Lite
预计耗时：5-15秒
预计费用：约 ￥0.245

请稍等，生成完成后会立即发送给您 ⏳
```

**这条消息必须在执行 API 调用之前发送！** 这样用户就知道任务已经开始处理，不会以为系统卡住了。

### 不同任务的提示模板

**文生图：**
```
🎨 收到！正在为您生成图片...
使用模型：Seedream 5.0 Lite
预计耗时：5-15秒
```

**文生视频：**
```
🎬 收到！正在为您生成视频...
使用模型：Vidu Q3 Pro
预计耗时：1-3分钟（视频生成较慢，请耐心等待）
```

**TTS：**
```
🔊 收到！正在为您生成语音...
使用模型：MiniMax Speech 2.8 Turbo
预计耗时：5-15秒
```

### 完成后的回复

```
✅ 生成完成！

[图片/视频/音频 URL]

实际消耗：￥0.245
```

### 视频任务的轮询提示

视频生成需要轮询，每 15 秒更新一次状态：

```
🎬 视频生成中...
当前状态：处理中
已等待：30 秒
预计还需：1-2 分钟
```

---

## API 配置

| 配置项 | 值 |
|--------|-----|
| Base URL | `https://api.ppio.com` |
| 鉴权 | `Authorization: Bearer <API_KEY>` |
| 获取 Key | https://ppio.com/settings/key-management |

## 任务类型与端点

| 任务 | 端点 | 模型 |
|------|------|------|
| 文生图 | `/v3/seedream-5.0-lite` | Seedream 5.0 Lite |
| 图片编辑 | `/v3/seedream-5.0-lite` | Seedream 5.0 Lite |
| 文生视频 | `/v3/async/vidu-q3-pro-t2v` | Vidu Q3 Pro |
| 图生视频 | `/v3/async/vidu-q3-pro-i2v` | Vidu Q3 Pro |
| TTS | `/v3/async/minimax-speech-2.8-turbo` | MiniMax Speech 2.8 |
| STT | `/v3/glm-asr` | GLM ASR |
| 任务查询 | `/v3/async/task-result?task_id=xxx` | - |

---

## 执行模板

### 文生图

```bash
curl -X POST "https://api.ppio.com/v3/seedream-5.0-lite" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "描述"}'
```

### 图片编辑

```bash
curl -X POST "https://api.ppio.com/v3/seedream-5.0-lite" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "编辑指令", "reference_images": ["图片URL"]}'
```

### 文生视频

```bash
curl -X POST "https://api.ppio.com/v3/async/vidu-q3-pro-t2v" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "描述", "duration": 4}'
```

### 图生视频

```bash
curl -X POST "https://api.ppio.com/v3/async/vidu-q3-pro-i2v" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "动作描述", "images": ["图片URL"]}'
```

### TTS

```bash
curl -X POST "https://api.ppio.com/v3/async/minimax-speech-2.8-turbo" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "要转换的文字",
    "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0},
    "audio_setting": {"format": "mp3"}
  }'
```

**可用声音：**
- 男声：`male-qn-qingse`（青涩）、`male-qn-jingying`（精英）
- 女声：`female-shaonv`（少女）、`female-yujie`（御姐）

### STT

```bash
curl -X POST "https://api.ppio.com/v3/glm-asr" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file": "音频URL或Base64"}'
```

### 任务结果查询

```bash
curl "https://api.ppio.com/v3/async/task-result?task_id=$TASK_ID" \
  -H "Authorization: Bearer $API_KEY"
```

**状态：** `TASK_STATUS_QUEUED` → `TASK_STATUS_PROCESSING` → `TASK_STATUS_SUCCEED`

---

## 错误处理

| 错误码 | 含义 | 处理 |
|--------|------|------|
| 401 | Key 无效 | 检查配置 |
| 402 | 余额不足 | https://ppio.com/billing 充值 |
| 429 | 请求过快 | 等待重试 |

## 定价

https://ppio.com/pricing
