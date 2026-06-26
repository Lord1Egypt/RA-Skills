---
name: hailuo-video
description: MiniMax Hailuo 视频生成技能 - 使用 S2V-01 模型进行主体参考视频生成。可以生成视频、查询任务状态、下载视频文件。
metadata:
  homepage: https://platform.minimax.com
  openclaw:
    emoji: 🎬
    requires:
      env:
        - MINIMAX_API_KEY
      bins:
        - curl
      config:
        - ~/.openclaw/openclaw.json
    primaryEnv: MINIMAX_API_KEY
user-invocable: true
---

# MiniMax Hailuo Video Skill

使用 MiniMax Hailuo S2V-01 模型进行主体参考视频生成。

## 环境配置

API Key 从以下优先级获取：
1. 环境变量 `MINIMAX_API_KEY`
2. 配置文件 `~/.openclaw/openclaw.json` 中的 `skills.hailuoVideo.apiKey`

如需手动设置，在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "skills": {
    "hailuoVideo": {
      "apiKey": "your-api-key-here"
    }
  }
}
```

## API 端点

| 操作 | 方法 | 端点 |
|------|------|------|
| 生成视频 | POST | `https://api.minimax.chat/v1/video_generation` |
| 查询状态 | GET | `https://api.minimax.chat/v1/query/video_generation?task_id=xxx` |
| 下载视频 | GET | `https://api.minimax.chat/v1/files/retrieve?file_id=xxx` |

## 功能

### 1. 生成视频 (S2V-01 主体参考)

```bash
# 使用主体参考图生成视频
curl -s "https://api.minimax.chat/v1/video_generation" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "S2V-01",
    "prompt": "人物描述动作",
    "subject_reference": [
      {
        "type": "character",
        "image": ["https://example.com/character.jpg"]
      }
    ]
  }'
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `model` | 是 | 使用 `S2V-01` |
| `prompt` | 是 | 视频描述，最大2000字符 |
| `subject_reference` | 是 | 主体参考图数组 |
| `subject_reference[].type` | 是 | 固定为 `character` |
| `subject_reference[].image` | 是 | 图片URL数组（目前仅支持单张） |
| `prompt_optimizer` | 否 | 是否自动优化prompt，默认true |
| `aigc_watermark` | 否 | 是否添加水印，默认false |
| `callback_url` | 否 | 回调通知地址 |

**图片要求：**
- 格式：JPG, JPEG, PNG, WebP
- 大小：小于 20MB
- 尺寸：短边 > 300px，长宽比在 2:5 和 5:2 之间

### 2. 查询任务状态

```bash
curl -s "https://api.minimax.chat/v1/query/video_generation?task_id=YOUR_TASK_ID" \
  -H "Authorization: Bearer $MINIMAX_API_KEY"
```

**状态返回值：**
| 状态 | 说明 |
|------|------|
| `Preparing` | 准备中 |
| `Queueing` | 队列中 |
| `Processing` | 生成中 |
| `Success` | 成功 |
| `Fail` | 失败 |

成功响应示例：
```json
{
  "task_id": "176843862716480",
  "status": "Success",
  "file_id": "176844028768320",
  "video_width": 1920,
  "video_height": 1080,
  "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

### 3. 下载视频

获取到 `file_id` 后，调用文件获取接口：

```bash
curl -s "https://api.minimax.chat/v1/files/retrieve?file_id=YOUR_FILE_ID" \
  -H "Authorization: Bearer $MINIMAX_API_KEY"
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1002 | 触发限流 |
| 1004 | API Key 错误 |
| 1008 | 余额不足 |
| 1026 | 输入内容涉及敏感 |
| 1027 | 生成内容涉及敏感 |
| 2013 | 参数错误 |
| 2049 | 无效 API Key |

## 使用示例

### 生成皮皮虾视频

```bash
# 1. 生成视频
RESPONSE=$(curl -s "https://api.minimax.chat/v1/video_generation" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "S2V-01",
    "prompt": "一只可爱的小龙虾机器人双手举起做惊讶状，橙色大钳子微微发抖，机械尾巴左右摆动，踉跄着向前冲去",
    "subject_reference": [
      {
        "type": "character",
        "image": ["https://example.com/pipipixia.jpg"]
      }
    ]
  }')

TASK_ID=$(echo $RESPONSE | jq -r '.task_id')
echo "Task ID: $TASK_ID"

# 2. 等待一段时间后查询状态
sleep 60
STATUS=$(curl -s "https://api.minimax.chat/v1/query/video_generation?task_id=$TASK_ID" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" | jq -r '.status')

echo "Status: $STATUS"

# 3. 如果成功，获取文件ID并下载
if [ "$STATUS" = "Success" ]; then
  FILE_ID=$(curl -s "https://api.minimax.chat/v1/query/video_generation?task_id=$TASK_ID" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" | jq -r '.file_id')
  
  # 下载视频
  curl -s "https://api.minimax.chat/v1/files/retrieve?file_id=$FILE_ID" \
    -H "Authorization: Bearer $MINIMAX_API_KEY" \
    -o video.mp4
fi
```

## 注意事项

1. 视频生成通常需要 1-3 分钟
2. 建议使用轮询查询任务状态，间隔 30-60 秒
3. 主体参考图必须包含清晰的人物面部
4. Prompt 应描述期望的动作和场景
