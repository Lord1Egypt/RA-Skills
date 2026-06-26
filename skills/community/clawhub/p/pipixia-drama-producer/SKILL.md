---
name: pipixia-drama-producer
description: 皮皮虾职场短剧全流程制作技能。用于为「皮皮虾」（机械龙虾AI-bot）职场短剧生成镜头视频、剪辑成片、配音配乐并发布到飞书群。完整流程：图生视频(I2V) → ffmpeg规范化+剪辑 → TTS配音 → BGM混音 → 飞书媒体消息发送。当用户提到制作皮皮虾短剧、生成新镜头、剪辑视频、配音配乐、或将视频/音频发送到飞书群时激活。
---

# 皮皮虾短剧制作技能

完整的职场动物短剧制作流程，从剧本到飞书发布。

## 环境变量配置

使用前请设置以下环境变量：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `FEISHU_APP_ID` | ✅ | 飞书应用 App ID（发送消息用） |
| `FEISHU_APP_SECRET` | ✅ | 飞书应用 App Secret |
| `FFMPEG` | 可选 | ffmpeg 路径（默认从 PATH 查找） |
| `FFPROBE` | 可选 | ffprobe 路径（默认从 PATH 查找） |
| `EDGE_TTS` | 可选 | edge-tts 路径（默认从 PATH 查找 `node-edge-tts`） |

**飞书应用权限要求**：`im:message:send`、`im:file`、`im:image`

## 角色与剧本参考

详见 `references/drama-reference.md`，包含：
- 角色设定与prompt模板
- ffmpeg关键命令速查
- TTS音色对照表
- 飞书API速查

## 核心工作流

### 第一步：生成镜头（I2V图生视频）

```python
# 必须用 reference_type="first_frame"，不要用 "subject"
gen_videos([{
    "image_file": "/workspace/lobster_robot.png",
    "output_file": "/workspace/shot.mp4",
    "prompt": "cute orange lobster robot [动作], ...",
    "reference_type": "first_frame"
}])
```

### 第二步：规范化 + 砍首秒

每个图生视频第一秒是原图静帧，必须裁掉：

```bash
python3 scripts/normalize_and_trim.py input.mp4 output_trim.mp4 --trim 1
```

### 第三步：剪辑合并

```bash
# 写concat列表，用Python避免shell语法问题
python3 -c "
clips = ['clip1_trim.mp4', 'clip2_trim.mp4', ...]
with open('/tmp/concat.txt', 'w') as f:
    for c in clips: f.write(f\"file '{c}'\n\")
"
ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -c copy output.mp4
```

**剪辑技巧**：
- 在关键台词后插入1.5s反应镜头（增加喜剧节奏）
- 砍掉所有图生视频开头静帧（-ss 1）

### 第四步：TTS配音

```bash
node-edge-tts -t "台词内容" -f output.mp3 -v zh-CN-YunxiaNeural -l zh-CN
```

⚠️ TTS台词时长不能超过对应视频片段时长，过长需用 `atempo=1.1~1.2` 加速：
```bash
ffmpeg -y -i input.mp3 -filter:a "atempo=1.15" output.mp3
```

### 第五步：混音（配音+配乐）

使用 `mix_audio.py` 将多条TTS台词按时间轴叠加，并加入BGM：

```bash
python3 scripts/mix_audio.py \
  --video drama_cut.mp4 \
  --bgm bgm_sneaky.mp3 \
  --bgm-volume 0.25 \
  --output drama_dubbed.mp4 \
  --lines "0.3:tts_line1.mp3" "5.1:tts_line2.mp3" "12.0:tts_line3.mp3"
```

BGM推荐下载地址（Kevin MacLeod CC BY 3.0）：
```bash
curl -sL "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Sneaky%20Snitch.mp3" -o bgm.mp3
```

### 第六步：发送到飞书

```bash
# 提取封面
ffmpeg -y -i video.mp4 -ss 00:00:00.5 -frames:v 1 -update 1 cover.jpg

# 发送视频（媒体气泡），chat_id 为目标群组 ID
bash scripts/send_video.sh video.mp4 cover.jpg <chat_id>

# 发送音频语音消息
bash scripts/send_audio.sh "要播报的文字" <chat_id> "zh-CN-YunxiaNeural"
```

## 依赖工具

| 工具 | 环境变量 | 默认值 |
|------|----------|--------|
| ffmpeg | `FFMPEG` | `ffmpeg`（PATH） |
| ffprobe | `FFPROBE` | `ffprobe`（PATH） |
| edge-tts | `EDGE_TTS` | `node-edge-tts`（PATH） |
| 飞书凭证 | `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 无（必填） |

## 版本管理惯例

每次重要修改用v2/v3...命名输出文件，保留历史版本方便回退：
- `drama_ep1_v1.mp4` → `drama_ep1_v2.mp4` → ...
- 在工作目录记录每个版本的剪辑结构
