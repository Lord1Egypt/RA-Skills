---
name: human-avatar
description: 使用阿里云 DashScope API 与阿里云 LingMou/灵眸生成多种 AI 视频与语音内容。七种能力：① LivePortrait 人像口播（图+音频→说话视频，两步流程）② EMO 人像口播 ③ AA/AnimateAnyone 全身动画（三步流程）④ T2I 文生图（万相2.x，默认 wan2.2-t2i-flash）⑤ I2V 图生视频（万相2.x，默认 wan2.6-i2v-flash，支持 T2I→I2V 一条龙）⑥ Qwen TTS 文字转语音（自动按场景选模型音色，默认 qwen3-tts-vd-realtime-2026-01-15）⑦ 灵眸数字人模板视频，支持随机模板、公共模板复制与脚本确认。当用户需要制作口播/人像/全身动画/文生图/文生视频/语音合成时触发此技能。
metadata:
  {
    "openclaw": {
      "emoji": "🎭",
      "requires": {
        "bins": ["ffmpeg", "ffprobe"],
        "env": [
          "DASHSCOPE_API_KEY",
          "ALIBABA_CLOUD_ACCESS_KEY_ID",
          "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
          "OSS_BUCKET",
          "OSS_ENDPOINT"
        ]
      }
    }
  }
---

# Human Avatar — 阿里云 AI 视频 & 语音生成

## 能力总览

| 能力 | 脚本 | 模型/接口 | Region | 简介 |
|------|------|---------|--------|------|
| **LivePortrait** | `live_portrait.py` | `liveportrait` | cn-beijing | 人像图 + 音频/视频 → 口播动态视频，两步流程 |
| **EMO** | `portrait_animate.py` | `emo-v1` | cn-beijing | 人像图 + 音频 → 口播，检测+生成两步 |
| **AA** (AnimateAnyone) | `animate_anyone.py` | `animate-anyone-gen2` | cn-beijing | 全身动画，三步：图检测→动作模板→视频生成 |
| **T2I 文生图** | `text_to_image.py` | `wan2.x-t2i` | 多地域 | 文字描述 → 图片，默认 wan2.2-t2i-flash |
| **I2V 图生视频** | `image_to_video.py` | `wan2.x-i2v` | 多地域 | 图片 → 视频，支持 T2I→I2V 一条龙，默认 wan2.6-i2v-flash |
| **Qwen TTS** | `qwen_tts.py` | `qwen3-tts-*` | cn-beijing / 新加坡 | 文字 → 语音，按场景自动选模型和音色，默认 qwen3-tts-vd-realtime-2026-01-15 |
| **灵眸数字人** | `avatar_video.py` | LingMou SDK | cn-beijing | 基于模板的数字人口播视频 |

---

## 快速选择指南

```
需要人像说话（有现成音频/视频）    → LivePortrait
需要人像说话（无音频，先生成语音）  → Qwen TTS → LivePortrait
需要全身跳舞/动作                 → AA (AnimateAnyone)
需要根据文字生成图片               → T2I (text_to_image)
需要根据图片生成视频               → I2V (image_to_video)
需要从零文字到视频（一条龙）        → T2I → I2V（image_to_video --t2i-prompt）
需要企业数字人/模板播报            → 灵眸 (avatar_video)
```

---

## 环境配置

```bash
pip install requests dashscope oss2 scipy numpy
# 灵眸额外:
pip install alibabacloud-lingmou20250527 alibabacloud-tea-openapi
```

```bash
export DASHSCOPE_API_KEY=sk-xxxx               # 北京地域 API Key
export ALIBABA_CLOUD_ACCESS_KEY_ID=xxx         # OSS 上传用
export ALIBABA_CLOUD_ACCESS_KEY_SECRET=xxx
export OSS_BUCKET=your-bucket
export OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
```

> ⚠️ `cn-beijing` 和新加坡地域的 API Key **不互通**，请确认使用正确地域的 Key。
> OSS_ENDPOINT 支持带或不带 `https://` 前缀，脚本自动规范化。

---

## 1. LivePortrait — 人像口播视频

**适用场景**：有人物照片 + 语音内容，快速生成人物说话视频。

**流程**：
```
Step 1: liveportrait-detect (同步)  → pass=true
  ↓
Step 2: liveportrait        (异步)  → video_url
```

**图片要求**：单人正面肖像，人脸清晰，无遮挡
**音频要求**：wav/mp3，< 15MB，1s ~ 3min
**视频输入**：自动提取音频（ffmpeg）

```bash
# 图片 + 音频文件
python scripts/live_portrait.py \
  --image ./portrait.jpg \
  --audio ./speech.mp3 \
  --template normal --download

# 图片 + 视频（自动提取音频）
python scripts/live_portrait.py \
  --image ./portrait.jpg \
  --video ./speech_video.mp4 \
  --template active --download

# 直接用公网 URL
python scripts/live_portrait.py \
  --image-url "https://..." \
  --audio-url "https://..." \
  --mouth-strength 1.2 --download
```

**动作模板**：
- `normal`（默认，适中动作）
- `calm`（平静，适合新闻播报/讲故事）
- `active`（活泼，适合演唱/活动主持）

---

## 2. Qwen TTS — 文字转语音

**适用场景**：需要从文字生成语音文件（配合 LivePortrait、EMO 等使用）。

**默认模型**：`qwen3-tts-vd-realtime-2026-01-15`

### 场景自动选模型

| 场景 `--scene` | 推荐模型 | 推荐音色 |
|---------------|---------|---------|
| `default` / `brand` | `qwen3-tts-vd-realtime-2026-01-15` | Cherry |
| `news` / `documentary` / `advertising` | `qwen3-tts-instruct-flash-realtime` | Serena / Ethan |
| `audiobook` / `drama` | `qwen3-tts-instruct-flash-realtime` | Cherry / Dylan |
| `customer_service` / `chatbot` / `education` | `qwen3-tts-flash-realtime` | Anna / Ethan |
| `ecommerce` / `short_video` | `qwen3-tts-flash-realtime` | Cherry / Chelsie |

### 可用音色

| 音色 | 特点 |
|------|------|
| `Cherry` | 活泼甜美女声，广告/有声书/配音 |
| `Serena` | 成熟知性女声，新闻/讲解/企业形象 |
| `Ethan` | 稳重亲切男声，教育/纪录片/培训 |
| `Dylan` | 富有表现力男声，广播剧/游戏配音 |
| `Anna` | 温柔亲切女声，客服/助手/日常 |
| `Chelsie` | 年轻清新女声，短视频/电商 |
| `Thomas` | 低沉磁性男声，品牌宣传/广告 |
| `Luna` | 温暖柔和女声，冥想/故事叙述 |

```bash
# 默认生成（qwen3-tts-vd-realtime + Cherry）
python scripts/qwen_tts.py --text "你好，欢迎使用千问语音" --download

# 按场景自动匹配
python scripts/qwen_tts.py --text "今日股市..." --scene news --download
python scripts/qwen_tts.py --text "从前有个..." --scene audiobook --download

# 指令控制语气/风格
python scripts/qwen_tts.py \
  --text "亲爱的同学们..." \
  --model qwen3-tts-instruct-flash-realtime \
  --instructions "语调温和，节奏平稳，适合教学场景" \
  --download

# 查看所有选项
python scripts/qwen_tts.py --list-voices
python scripts/qwen_tts.py --list-models
```

---

## 3. T2I 文生图 — 万相2.x

**适用场景**：根据文字描述生成高质量图片（可后续接 I2V 生成视频）。

```bash
# 默认模型（wan2.2-t2i-flash，快速）
python scripts/text_to_image.py \
  --prompt "一位穿汉服的女性站在桃花林中，电影感，4K，柔和光线" \
  --size 960*1696 --download

# 高质量模型
python scripts/text_to_image.py \
  --prompt "..." --model wan2.2-t2i-plus --size 1280*1280 --download

# 最新模型（万相2.6）
python scripts/text_to_image.py \
  --prompt "..." --model wan2.6-t2i --size 1280*1280 --n 1 --download
```

**模型选型**：
- `wan2.2-t2i-flash`（默认，快速，适合测试）
- `wan2.2-t2i-plus`（质量更高）
- `wan2.6-t2i`（最新，支持更宽高比，同步调用）

**常用尺寸**：`1280*1280`（1:1）/ `960*1696`（9:16 竖版）/ `1696*960`（16:9 横版）

---

## 4. I2V 图生视频 — 万相2.x

**适用场景**：将图片生成为动态视频，支持从文字一条龙到视频。

```bash
# 本地图片 → 视频
python scripts/image_to_video.py \
  --image ./portrait.jpg \
  --prompt "她缓缓转身微笑，裙摆飘动，花瓣轻轻飞舞" \
  --model wan2.6-i2v-flash \
  --resolution 720P --duration 5 --download

# 🔥 一条龙：文字 → 图 → 视频
python scripts/image_to_video.py \
  --t2i-prompt "一位穿汉服的女性站在桃花林中" \
  --prompt "她缓缓转身，花瓣飘落，唯美意境" \
  --download --output result.mp4

# 带背景音乐
python scripts/image_to_video.py \
  --image ./portrait.jpg \
  --audio-url "https://..." \
  --prompt "..." --download
```

**模型选型**：
- `wan2.6-i2v-flash`（默认，含音效，支持5/10s）
- `wan2.5-i2v-preview`（高质量预览版）
- `wan2.2-i2v-plus`（无声，较快）

---

## 5. AA AnimateAnyone — 全身动画

**适用场景**：有人物全身照 + 参考动作视频，生成人物跳舞/动作视频。

**要求**：
- 图片：单人全身正面，头到脚完整，宽高比 0.5~2.0
- 视频：全身入镜，首帧开始即全身可见，mp4/avi/mov，fps≥24，2~60s

**三步流程**：
```
Step 1: animate-anyone-detect-gen2   (同步)  → check_pass=true
  ↓
Step 2: animate-anyone-template-gen2 (异步)  → template_id（约3~5分钟）
  ↓
Step 3: animate-anyone-gen2          (异步)  → video_url（约3~5分钟）
```

```bash
# 本地文件（自动转换格式 + 上传 OSS）
python scripts/animate_anyone.py \
  --image ./portrait_fullbody.jpg \
  --video ./dance.mp4 \
  --download --output result.mp4

# 以图片为背景生成
python scripts/animate_anyone.py \
  --image ./portrait.jpg --video ./dance.mp4 \
  --use-ref-img-bg --video-ratio 9:16 --download

# 跳过 Step2（已有 template_id）
python scripts/animate_anyone.py \
  --image ./portrait.jpg \
  --template-id "AACT.xxx.xxx" --download
```

> 格式自动转换：视频 webm/mkv/flv → mp4；图片 webp/heic → jpg；fps<24 → 24fps

---

## 6. EMO — 人像口播（旧版）

**注意**：推荐优先使用 LivePortrait，EMO 适合对口型精度要求高的场景。

```bash
python scripts/portrait_animate.py \
  --image ./portrait.jpg \
  --audio ./speech.mp3 \
  --download
```

---

## 7. 灵眸数字人 — 企业级模板视频

**适用场景**：企业数字人播报、模板化新闻视频、上传人物图片并结合口播脚本生成模板播报视频。

### 新工作流（优先无 `template_id`）

- 若用户**给了 `template_id`**：直接使用该模板生成
- 若用户**没给 `template_id`**：
  1. 先列出账号下已有播报模板
  2. 如果有模板，**随机选择一个模板**来创作
  3. 如果没有模板，再尝试获取公共模板并**复制最多 3 个公共模板**到当前账号
  4. 从复制结果里随机选择一个继续生成
- **但要注意**：公共模板复制成功后，复制出的模板不一定立刻就是“可直接生成视频”的成熟模板；有些复制结果仍是草稿，可能缺少有效片段、素材或变量绑定，需要在灵眸侧补完
- 若用户只给了图片和“做个口播视频”的要求，但**没有明确脚本**：先向用户确认口播文案，再继续生成

### 当前脚本能力

`scripts/avatar_video.py` 现在支持：
- `--list-templates`：列出账号下已有模板
- `--list-public-templates`：列出公共模板（SDK 1.7.0+）
- `--copy-public-templates`：复制最多 3 个公共模板（SDK 1.7.0+）
- 不传 `--template-id`：随机选择一个已有模板
- 当本地模板为空时：自动尝试复制公共模板作为兜底
- `--show-template-detail`：查看模板详情与可替换变量
- 自动把输入文案填入模板里的 text 变量（优先 `text_content` / `test_text`）
- 当公共模板复制后直接生成失败时，明确报错提示用户该模板仍需完善，而不是静默失败

```bash
# 列出现有模板
python scripts/avatar_video.py --list-templates

# 列出公共模板（SDK 1.7.0+）
python scripts/avatar_video.py --list-public-templates

# 手动复制最多 3 个公共模板（SDK 1.7.0+）
python scripts/avatar_video.py --copy-public-templates

# 不指定 template_id，自动随机选一个已有模板来播报
python scripts/avatar_video.py \
  --text "大家好，欢迎收看今天的科技新闻。" \
  --download

# 指定 template_id
python scripts/avatar_video.py \
  --template-id "BS1b2WNnRMu4ouRzT4clY9Jhg" \
  --text "大家好，欢迎收看今天的科技新闻。" \
  --download

# 查看随机选中的模板详情
python scripts/avatar_video.py \
  --show-template-detail \
  --text "这是一段测试播报文案"
```

### 对话式使用约定

当用户说：
- “用这张图做一个口播视频”
- “帮我做个数字人口播”
- “上传图片，做个播报视频”

按下面流程执行：
1. 判断用户是否已经给出可直接播报的文案/脚本
2. 如果没有，就先追问一句：**“口播的具体文案是什么？你也可以只给我要点，我来帮你整理成适合播报的脚本。”**
3. 拿到脚本后，调用灵眸流程：优先随机已有模板；无本地模板时再尝试公共模板复制
4. 如果用户上传了人物图片，但当前模板式灵眸接口并不需要该图片，明确告诉用户：这一路径主要依赖模板；若要强制使用用户图片做人像口播，应改走 LivePortrait / EMO

---

## API 参考文档

- **LivePortrait**: https://help.aliyun.com/zh/model-studio/liveportrait-api
- **EMO** (emo-detect + emo-v1): [references/emo-api.md](references/emo-api.md)
- **AA** (Animate Anyone): [references/aa-api.md](references/aa-api.md)
- **T2I** (文生图V2): https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference
- **I2V** (图生视频): https://help.aliyun.com/zh/model-studio/image-to-video-api-reference/
- **Qwen TTS**: https://help.aliyun.com/zh/model-studio/qwen-tts-realtime
- **灵眸** (LingMou): [references/lingmou-api.md](references/lingmou-api.md)
- **OSS 上传**: [references/oss-upload.md](references/oss-upload.md)
