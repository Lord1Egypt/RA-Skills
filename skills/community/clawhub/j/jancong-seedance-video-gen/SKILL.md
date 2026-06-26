---
name: seedance-video-gen
description: 使用火山引擎 Seedance 2.0 系列模型（doubao-seedance-2-0 / doubao-seedance-2-0-fast）通过方舟平台 API 生成高质量 AI 视频。支持文生视频、图生视频、视频参考、音频参考等多模态内容生成，适用于用户要求生成/制作/创建视频、文生视频、图生视频、AI 生视频以及泛化表述如"帮我做一个视频""用 AI 生成一段视频"等场景。
---

# Seedance 视频生成 Skill

使用火山引擎方舟平台的 **Seedance 2.0** 系列 AI 模型生成高质量视频。

## 支持的模型

| 模型 ID | 特点 | 适用场景 |
|---------|------|---------|
| `doubao-seedance-2-0-260128` | 标准版，质量更高 | 高质量商业视频、精细画面 |
| `doubao-seedance-2-0-fast-260128` | 快速版，速度更快 | 快速预览、批量测试 |

## 工作流程

### Step 1: 准备请求参数

根据用户需求构建 API 请求体：

**必需参数：**
- `model`: 模型名称（从上表选择）
- `content`: 多模态内容数组，至少包含一个 text 类型元素

**可选参数：**
- `generate_audio`: 是否同时生成音频/语音 (true/false)
- `ratio`: 视频比例 `"16:9"` | `"9:16"` | `"1:1"`（默认 16:9）
- `duration`: 视频时长秒数，范围 5-11（默认 10）
- `watermark`: 是否添加水印 (true/false)

### Step 2: 构建 content 数组

`content` 数组支持以下类型的多模态输入：

```jsonc
{
  "content": [
    // 1. 文本提示词（必需）
    {
      "type": "text",
      "text": "详细的视频描述提示词..."
    },

    // 2. 参考图片（可选，可多个）
    {
      "type": "image_url",
      "image_url": { "url": "https://example.com/image.jpg" },
      "role": "reference_image"
    },

    // 3. 参考视频（可选，用于参考运镜/构图风格）
    {
      "type": "video_url",
      "video_url": { "url": "https://example.com/video.mp4" },
      "role": "reference_video"
    },

    // 4. 参考音频/背景音乐（可选）
    {
      "type": "audio_url",
      "audio_url": { "url": "https://example.com/audio.mp3" },
      "role": "reference_audio"
    }
  ]
}
```

> **注意**: 图片、视频、音频 URL 必须是公网可访问的地址。如果用户提供本地文件，需要先上传到 OSS 或使用 Base64 编码。

### Step 3: 提交生成任务

调用 `scripts/generate_video.py` 脚本提交异步任务：

```bash
python3 ~/.workbuddy/skills/seedance-video-gen/scripts/generate_video.py \
  --model doubao-seedance-2-0-fast-260128 \
  --prompt "你的视频描述" \
  --ratio 16:9 \
  --duration 10 \
  [--image-url "https://..."] \
  [--video-url "https://..."] \
  [--audio-url "https://..."] \
  [--generate-audio] \
  [--no-watermark]
```

或者直接使用 curl 调用 API（见 references/api_reference.md）。

API 返回任务 ID：
```json
{ "id": "cgt-20260410162021-xxxxx" }
```

### Step 4: 轮询任务状态

提交后任务为异步处理，需轮询查询状态：

```bash
python3 ~/.workbuddy/skills/seedance-video-gen/scripts/query_task.py <task_id>
```

或直接 curl：
```bash
curl -X GET "{ARK_API_URL}/api/v3/contents/generations/tasks/{task_id}" \
  -H "Authorization: Bearer {API_KEY}"
```

**状态值：**
| 状态 | 含义 | 操作 |
|------|------|------|
| `pending` | 排队中 | 继续等待 |
| `running` | 生成中 | 继续等待 |
| `completed` | 完成 | 获取结果 |
| `failed` | 失败 | 查看错误信息 |

**完成时的响应包含：**
- `video_result.video_url`: 生成的视频地址
- `video_result.cover_image_url`: 封面图地址

### Step 5: 下载并展示结果

任务完成后：
1. 下载视频文件到工作目录
2. 使用 preview_url 或 open_result_view 展示给用户
3. 告知用户视频路径和基本信息

## 提示词撰写建议

参考 `references/prompt_guide.md` 获取完整的提示词撰写指南。核心原则：

1. **明确主体和动作**: 描述清楚谁在做什么
2. **指定镜头语言**: 运镜方式（推拉摇移）、视角（第一人称/俯拍等）
3. **时间轴描述**: 用时间戳分段描述不同时段的画面变化，如 `0-2 秒：xxx；3-5 秒：xxx`
4. **风格关键词**: 明确视觉风格（写实/动漫/电影感等）
5. **音效描述**: 如果 generate_audio=true，可在提示词中描述音效和配音需求
6. **参考素材说明**: 当有图片/视频参考时，在提示词中指明如何使用这些素材

## 环境配置

脚本从环境变量读取以下配置：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `ARK_API_KEY` | 方舟平台 API Key | （必填） |
| `ARK_API_URL` | 方舟 API 地址 | `https://ark.cn-beijing.volces.com` |

确保在使用前已设置 `ARK_API_KEY` 环境变量。
