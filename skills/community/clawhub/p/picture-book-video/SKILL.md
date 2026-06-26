---
name: picture-book-video
version: 1.1.0
description: >-
  绘本故事脚本 → 视频 mp4（中英文双语版本）。
  自动完成：分镜图生成 → 静态画面/动画 → 串联 → TTS旁白 → ASS字幕 → 最终合成。
  输出中英文两个版本，附带抖音发布所需的标题/描述/话题。
  TTS 优先使用 Qwen3-TTS（本地GPU，6角色音色库），失败回退 Edge TTS。

read_when:
  - 用户说"生成绘本视频"、"做绘本故事"、"绘本视频"
  - 用户提供绘本故事脚本要求生成视频
  - 用户提到"picture-book-video"、"琪琪OPC"、"绘本故事视频"
  - 用户需要为抖音生成儿童故事视频

metadata:
  openclaw:
    emoji: 📚
    priority: high
    category: video-generation
    tags:
      - picture-book
      - children
      - douyin
      - bilingual
      - tts
    conflicts_with: []
---

# 绘本故事视频 (Picture Book Video)

> 将绘本故事脚本 → 中英文双语视频（带字幕+旁白）

**核心流程**:
```
脚本解析 → 分镜图生成 → 画面合成 → 串联 → TTS旁白 → ASS字幕 → 最终视频
  (LLM)     (ComfyUI)    (ffmpeg)   (ffmpeg)  (EdgeTTS)  (脚本)    (ffmpeg)
 Phase 0    Phase 1      Phase 2    Phase 2   Phase 3    Phase 3   Phase 4
```

---

##  执行纪律

1. **Phase 分隔** — Phase 0-1 由 LLM 驱动（内容决策），Phase 2-4 由脚本驱动（技术合成）
2. **BLOCKING 步骤** — Phase 0（脚本评估）和 Phase 1（分镜方案确认）⛔ 必须等待用户响应
3. **禁止跳过确认** — 未经 Phase 1 用户确认，不得调用管线脚本
4. **脚本做技术，LLM 做内容** — 脚本不判断风格、不改写脚本、不做内容决策
5. **串行执行** — Phase 必须按顺序执行，不得跳跃
6. **双语输出** — 每个故事必须生成中文 + 英文两个版本

---

## Phase 0: 脚本评估

🚧 **GATE**: 用户提供了故事脚本

### 0.1 扫描输入

检查用户是否提供了：
- 故事脚本（必需）
- 合集名称（可选）
- 序列号（可选，如 S02E01）
- 合集描述（可选）

### 0.2 完整性评分

| 材料 | 必需 | 评分规则 |
|------|------|----------|
| 故事脚本 | ✅ 必需 | 无则直接报错退出 |
| 合集名称 | ❌ 可选 | 无则使用默认"琪琪的魔法故事屋" |
| 序列号 | ❌ 可选 | 无则自动生成 |
| 合集描述 | ❌ 可选 | 无则留空 |

### 0.3 交互策略

```
脚本完整 → 进入 Phase 1

脚本不完整 → ⛔ BLOCKING，提示用户补充
```

### 0.4 创建项目目录

```bash
PROJECT_NAME="picture-book-$(date +%Y%m%d)-<short-desc>"
PROJECT_DIR="<workspace>/project/${PROJECT_NAME}"
mkdir -p "${PROJECT_DIR}/input/"
mkdir -p "${PROJECT_DIR}/scenes/"
mkdir -p "${PROJECT_DIR}/output/"
mkdir -p "${PROJECT_DIR}/.temp/"

# 拷贝脚本到项目目录
cp <script_file> "${PROJECT_DIR}/input/"
```

---

## Phase 1: 分镜方案

🚧 **GATE**: 脚本评估通过

### 1.1 解析故事脚本

LLM 读取故事脚本，解析为分镜结构。每个分镜包含：
- 场景编号
- 旁白文本
- 画面描述（用于 ComfyUI 生成图片）
- 预计时长

输出格式：
```markdown
# 分镜方案

| 场景 | 旁白 | 画面描述 | 预计时长 |
|------|------|----------|----------|
| 1 | ... | ... | ...s |
...
```

### 1.2 风格确定

默认风格：**蜡笔儿童手绘风格**

LLM 向用户确认：
```
根据故事内容，推荐画面风格：
[1] 蜡笔儿童手绘（默认）
[2] 水彩风格
[3] 剪纸风格
请确认或自选。
```

### 1.3 生成 ComfyUI 提示词

为每个场景生成 Flux 文生图提示词，遵循风格规范。

### 1.4 保存分镜方案

生成 `<PROJECT_DIR>/scene_plan.md` 和 `<PROJECT_DIR>/scene_prompts.json`

### 1.5 方案确认

⛔ **BLOCKING** — 向用户展示分镜方案，等待确认：

```
请确认：
1. 确认生成 → 进入 Phase 2
2. 修改第X场景 → 重新生成 → 再次确认
```

---

## Phase 2: 画面生成

🚧 **GATE**: Phase 1 用户已确认

### 2.1 生成分镜图片

使用 ComfyUI 技能生成每个场景的图片：

```bash
python3 <SKILL_DIR>/scripts/generate_scenes.py \
  --prompts "<PROJECT_DIR>/scene_prompts.json" \
  --output-dir "<PROJECT_DIR>/scenes/" \
  --style "crayon"
```

### 2.2 生成封面

```bash
python3 <SKILL_DIR>/scripts/stage_cover.py \
  --output "<PROJECT_DIR>/scenes/cover.png" \
  --title "<标题>" \
  --subtitle "<合集名>" \
  --episode-id "<序列号>" \
  --brand "琪琪的魔法故事屋" \
  --qiqi "~/.openclaw/workspace/characters/qiqi_default.png" \
  --width 1920 --height 1080
```

### 2.3 画面验证

检查所有场景图片是否生成成功，分辨率是否为 1920x1080。

---

## Phase 3: 音频与字幕

🚧 **GATE**: Phase 2 完成

### 3.1 生成中文 TTS

**优先 Qwen3-TTS**（本地GPU，音色克隆+设计），**失败回退 Edge TTS**：

```bash
# 方式1: Qwen3-TTS（首选）
python3 ~/.openclaw/workspace/skills/tts-qwen3/scripts/qwen_tts.py \
  --text "<中文旁白全文>" \
  --voice narrator_teacher \
  --output "<PROJECT_DIR>/narration_cn.wav" \
  --fallback-edge true

# 方式2: Edge TTS（回退，自带 SRT）
python3 <SKILL_DIR>/scripts/tts.py \
  --text "<中文旁白全文>" \
  --output "<PROJECT_DIR>/narration_cn.mp3" \
  --srt "<PROJECT_DIR>/narration_cn.srt" \
  --voice zh-CN-XiaoyiNeural \
  --rate=-15%
```

**角色音色映射**（Qwen3-TTS）：
| 脚本角色 | --voice 参数 | 说明 |
|---------|-------------|------|
| 旁白/叙事 | narrator_teacher | 温暖女声 |
| 琪琪对话 | qiqi_clone | 克隆音色 |
| 小男孩 | boy_child | 活泼8岁 |
| 小女孩 | girl_child | 甜美7岁 |
| 大人男 | adult_male | 沉稳 |
| 大人女 | adult_female | 优雅 |

### 3.2 生成英文 TTS

```bash
python3 <SKILL_DIR>/scripts/tts.py \
  --text "<英文旁白全文>" \
  --output "<PROJECT_DIR>/narration_en.mp3" \
  --srt "<PROJECT_DIR>/narration_en.srt" \
  --voice en-US-JennyNeural \
  --rate=-15%
```

### 3.3 生成中文 ASS 字幕

```bash
python3 <SKILL_DIR>/scripts/srt_to_ass.py \
  --srt "<PROJECT_DIR>/narration_cn.srt" \
  --output "<PROJECT_DIR>/subtitles_cn.ass" \
  --font-size 80
```

### 3.4 生成英文 ASS 字幕

```bash
python3 <SKILL_DIR>/scripts/srt_to_ass.py \
  --srt "<PROJECT_DIR>/narration_en.srt" \
  --output "<PROJECT_DIR>/subtitles_en.ass" \
  --font-size 80
```

---

## Phase 4: 视频合成

🚧 **GATE**: Phase 3 完成

### 4.1 运行完整管线

```bash
# 中文版
python3 <SKILL_DIR>/scripts/pipeline.py \
  --scenes-dir "<PROJECT_DIR>/scenes/" \
  --audio "<PROJECT_DIR>/narration_cn.mp3" \
  --ass "<PROJECT_DIR>/subtitles_cn.ass" \
  --output "<PROJECT_DIR>/output/<episode_id>_cn.mp4" \
  --title "<标题>" \
  --subtitle "<合集名>" \
  --episode-id "<序列号>" \
  --brand "琪琪的魔法故事屋" \
  --qiqi "~/.openclaw/workspace/characters/qiqi_default.png" \
  --cover-duration 4.0 \
  --fade-duration 0.8

# 英文版
python3 <SKILL_DIR>/scripts/pipeline.py \
  --scenes-dir "<PROJECT_DIR>/scenes/" \
  --audio "<PROJECT_DIR>/narration_en.mp3" \
  --ass "<PROJECT_DIR>/subtitles_en.ass" \
  --output "<PROJECT_DIR>/output/<episode_id>_en.mp4" \
  --title "<英文标题>" \
  --subtitle "<英文合集名>" \
  --episode-id "<序列号>" \
  --brand "琪琪的魔法故事屋" \
  --qiqi "~/.openclaw/workspace/characters/qiqi_default.png" \
  --cover-duration 4.0 \
  --fade-duration 0.8
```

### 4.2 生成抖音发布描述

```markdown
# 抖音发布描述

## 中文版
- 标题：{中文标题}｜{合集名}
- 描述：{故事简介}
- 话题：#儿童故事 #{合集名} #睡前故事 #绘本动画

## 英文版
- 标题：{English Title}｜{English Series}
- 描述：{English synopsis}
- 话题：#英语启蒙 #磨耳朵英语 #{合集名} #儿童英语
```

### 4.3 质量验证

检查：
- 视频文件存在且 > 10MB
- H.264 + AAC 编码
- 1920×1080 分辨率
- 时长与音频匹配
- 字幕完整显示

---

##  抖音发布

视频生成后，使用 `douyin-browser-publish` 技能发布：

```bash
# 中文版
使用 douyin-browser-publish 技能发布：
- 视频：<PROJECT_DIR>/output/<episode_id>_cn.mp4
- 标题：{中文标题}｜{合集名}
- 话题：#儿童故事 #{合集名} #睡前故事 #绘本动画

# 英文版
使用 douyin-browser-publish 技能发布：
- 视频：<PROJECT_DIR>/output/<episode_id>_en.mp4
- 标题：{English Title}｜{English Series}
- 话题：#英语启蒙 #磨耳朵英语 #{合集名} #儿童英语
```

---

## 🛠️ 依赖要求

```bash
# 必需
python3 --version       # 3.8+
ffmpeg -version         # 5.0+
edge-tts --version      # 7.0+

# ComfyUI（文生图）
cd ~/ComfyUI && ~/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188

# 琪琪角色图
~/.openclaw/workspace/characters/qiqi_default.png
```

---

## ️ 故障排除

| 问题 | 解决 |
|------|------|
| ComfyUI 未启动 | `cd ~/ComfyUI && LD_LIBRARY_PATH=~/comfyui-venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:$LD_LIBRARY_PATH ~/comfyui-venv/bin/python main.py --listen 127.0.0.1 --port 8188` |
| TTS 失败 | 检查网络；文本超长时分段合成 |
| 字幕截断 | 检查 srt_to_ass.py 的 max_chars 设置（默认 24） |
| 视频合成失败 | 检查 ffmpeg 版本；检查场景图片存在 |

---

## 📁 输出文件

每个故事生成后，项目目录包含：

```
<PROJECT_DIR>/
├── input/
│   └── <script_file>          # 原始脚本
├── scenes/
│   ├── cover.png              # 封面（含琪琪角色）
│   ├── scene_01.png           # 场景图
│   ├── scene_02.png
│   └── ...
── narration_cn.mp3           # 中文旁白
├── narration_cn.srt           # 中文 SRT
├── subtitles_cn.ass           # 中文 ASS 字幕
── narration_en.mp3           # 英文旁白
├── narration_en.srt           # 英文 SRT
├── subtitles_en.ass           # 英文 ASS 字幕
├── output/
│   ├── <episode_id>_cn.mp4    # 中文视频
│   └── <episode_id>_en.mp4    # 英文视频
── scene_plan.md              # 分镜方案
├── scene_prompts.json         # ComfyUI 提示词
└── douyin_publish.md          # 抖音发布描述
```

---

## 🔗 相关技能

- **comfyui-image-video**: ComfyUI 文生图/视频生成
- **tts-qwen3**: Qwen3-TTS 本地语音合成（琪琪OPC首选）
- **tts-cosyvoice**: Edge TTS 语音合成（回退方案）
- **douyin-browser-publish**: 抖音视频发布
- **keynote-video**: PPT 转视频

---

*版本: v1.0 | 基于 琪琪OPC 项目管线 | 参考 keynote-video 架构*
