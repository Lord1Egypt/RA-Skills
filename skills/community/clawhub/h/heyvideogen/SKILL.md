---
name: heyvideogen
description: |
  Heygen HyperFrames + MiniMax Hailuo AI 视频自动化生产流水线。
  用户说"做视频"、"生成视频"、"短视频制作"、"视频混剪"、"用 HyperFrames 做"时触发。
  底层用 HyperFrames(HTML+GSAP) 做动画合成 + 渲染引擎，用 MiniMax Hailuo 生成 AI 视频片段，
  用 FFmpeg 做最终混音混画，输出视频号/B站/抖音可发布的 MP4。
  三种内容模式自动切换（Mode A 纯干货 / Mode B 剧情+科普 / Mode C 漫剧型）。
  当用户已有 HyperFrames 项目需要生成 AI 片段，或需要比 Remotion 更简单的 HTML 工作流时也用此技能。
---

# heyvideogen — HyperFrames × MiniMax Hailuo 视频流水线

## 架构概览

```
选题 → 分镜生成 → TTS配音 → MiniMax Hailuo AI片段 → HyperFrames HTML合成 → FFmpeg渲染 → 成品
```

**Videogen（Remotion版）** vs **Heyvideogen（HyperFrames版）**：

| | Videogen | Heyvideogen |
|--|---------|------------|
| 动画渲染 | Remotion + React | HyperFrames + HTML + GSAP |
| 渲染引擎 | `npx remotion render` | `npx hyperframes render` |
| 视频合成 | FFmpeg concat/overlay | HyperFrames CLI (内置 Chrome+FFmpeg) |
| 上手门槛 | 需懂 React | 会写 HTML 就会 |
| AI片段 | MiniMax Hailuo t2v/i2v | MiniMax Hailuo t2v/i2v（完全相同） |
| 字幕 | Remotion 内置 | GSAP + CSS |
| 数字分身 | IMA Key + S2V-01 | 同 Videogen |

---

## 两种工作模式

### 模式一：AI 片段 + HyperFrames 合成（推荐）

**适用**：有分镜、需要 AI 视频片段填充、有大量文字/图表动画的视频。

1. 生成分镜 JSON
2. 调用 MiniMax Hailuo 生成各 clip（第 N 步，见下方）
3. 用 HyperFrames HTML 组织 clips + 动画字幕 + 转场
4. `npx hyperframes render` → MP4

### 模式二：纯 HyperFrames（无 AI 片段）

**适用**：PPT风格、知识讲解、数据图表、配音驱动型视频。

- 直接写 HTML composition
- 用 GSAP 做动画
- TTS + `hyperframes tts` 生成配音
- `hyperframes render`

---

## API 体系（与 Videogen 相同）

| API Key | 开头 | 支持能力 |
|---------|------|---------|
| MiniMax Key | `sk-cp-` | TTS (speech-2.8-hd) ✅、Hailuo 视频生成 ✅ |
| IMA Key | `ima_` | SeeDream 生图、Wan/Kling 视频（数字分身） |

**错误处理：**
```
2056 → usage limit exceeded，跳过该片段继续
其他异常 → 记录错误，换策略继续
```

---

## 三种内容模式（与 Videogen 对齐）

### Mode A — 纯干货型
结构：开场痛点(3s) → 核心要点×3(各12s) → 金句收尾(9s)
视觉：PPT/图表为主，AI点缀关键帧

### Mode B — 剧情+科普型 ✨主打
结构：剧情钩子(8s) → 问题拆解(15s) → 干货×2(各12s) → 升华收尾(10s)
视觉：剧情画面 + 干净科普画面混合

### Mode C — 漫剧/剧情型
结构：起(8s) → 承(12s) → 转(20s) → 合(8s) + 金句收尾
视觉：角色全程驱动，强戏剧冲突

---

## 分镜格式（HyperFrames 版）

```json
{
  "panel_number": 1,
  "scene_type": "剧情场景 | 知识讲解 | 数据展示 | 过渡页",
  "shot_type": "特写 | 近景/中景 | 中景 | 全景 | 远景/建立景 | POV主观视角",
  "camera_move": "固定镜头 | 推进 | 拉出 | 左摇 | 右摇 | 上摇 | 下摇 | 移动摄影",
  "description": "画面文字描述（供AI生成视频用）",
  "video_prompt": "Hailuo视频生成Prompt（镜头控制+主体+氛围+动态+风格）",
  "narration": "旁白/台词",
  "duration": 5,
  "transition": "硬切 | 淡入淡出 | 溶解 | 滑入"
}
```

**Video Prompt 公式：**
```
镜头描述 + 镜头运动 + 主体内容 + 动态元素 + 风格 + 9:16竖屏
```

---

## MiniMax Hailuo 片段生成（与 Videogen 共享）

### 方式一：Python 脚本（推荐）

```bash
# t2v — 文生视频
python skills/videogen/scripts/v2/run_pipeline.py gen "选题" --mode auto --duration 60

# 或直接调用 Hailuo
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode t2v \
  --prompt "medium shot, slow push-in, urban city at night, cinematic mood, 9:16 vertical" \
  --duration 6 \
  --output heyvideogen-output/clips/clip_01.mp4

# i2v — 图生视频（关键帧动画化）
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode i2v \
  --prompt "subtle character movement, natural breathing..." \
  --first-frame heyvideogen-output/slides/slide_NN.png \
  --duration 6 \
  --output heyvideogen-output/clips/clip_NN.mp4
```

### 方式二：复用 Videogen 的 TTS Harness

```bash
python skills/videogen/scripts/v2/tts_harness.py "配音文本" \
  --output heyvideogen-output
```

---

## HyperFrames 项目初始化

```bash
cd /root/.openclaw/workspace

# 初始化空白 HyperFrames 项目
npx hyperframes init heyvideogen-project --non-interactive

# 进入项目
cd heyvideogen-project
```

**关键文件结构：**
```
heyvideogen-project/
├── index.html              # 主合成文件
├── compositions/           # 子合成（可选）
│   ├── scene-01.html
│   ├── scene-02.html
│   └── captions.html
├── clips/                  # AI 生成的视频片段
│   ├── clip_01.mp4
│   └── clip_02.mp4
├── voiceover.mp3           # TTS 配音
└── DESIGN.md               # 视觉规范（如有）
```

---

## HTML Composition 写作规范

**前置必读：** `references/html-authoring.md` — HyperFrames 完整 HTML 写作规范

### 核心模板（9:16 竖屏）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8" />
  <title>HeyVideoGen Output</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #000; overflow: hidden; }
  </style>
</head>
<body>
  <div id="main"
    data-composition-id="main"
    data-start="0"
    data-width="1080"
    data-height="1920">

    <!-- AI 视频片段（Track 0） -->
    <video
      id="clip-1"
      data-start="0"
      data-duration="5"
      data-track-index="0"
      src="clips/clip_01.mp4"
      muted playsinline>
    </video>

    <!-- 字幕/文字叠加（Track 1） -->
    <div
      id="caption-1"
      data-start="0.5"
      data-duration="4.5"
      data-track-index="1"
      class="caption-text">
      开场白文字
    </div>

    <!-- 背景音乐（Track 2） -->
    <audio
      id="bgm"
      data-start="0"
      data-duration="57"
      data-track-index="2"
      data-volume="0.3"
      src="voiceover.mp3">
    </audio>

  </div>

  <style>
    /* 字幕样式 */
    .caption-text {
      position: absolute;
      bottom: 200px;
      left: 60px;
      right: 60px;
      font-size: 56px;
      font-weight: 600;
      color: #fff;
      text-align: center;
      text-shadow: 0 4px 20px rgba(0,0,0,0.8);
      font-family: "Inter", "Noto Sans SC", sans-serif;
    }
  </style>

  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });

    // 字幕淡入
    tl.from("#caption-1", { opacity: 0, y: 20, duration: 0.5, ease: "power2.out" }, 0.3);
    // 字幕淡出
    tl.to("#caption-1", { opacity: 0, y: -10, duration: 0.4, ease: "power2.in" }, 4.0);

    window.__timelines["main"] = tl;
  </script>
</body>
</html>
```

### 多场景结构

```html
<!-- 场景1：开场 -->
<video id="scene1-clip" data-start="0" data-duration="5"
  data-track-index="0" src="clips/clip_01.mp4" muted playsinline></video>
<div id="scene1-title" data-start="0.2" data-duration="4.5"
  data-track-index="1" class="title-large">标题</div>

<!-- 场景2：内容（淡入淡出转场） -->
<video id="scene2-clip" data-start="5.5" data-duration="10"
  data-track-index="0" src="clips/clip_02.mp4" muted playsinline></video>
<div id="scene2-point" data-start="5.8" data-duration="9.5"
  data-track-index="1" class="point-card">核心观点</div>

<!-- 转场效果通过 GSAP 实现 -->
```

---

## GSAP 动画规范（与 HyperFrames Skill 对齐）

**参考：** `references/gsap-rules.md`

### 入场动画（每场景必用）

```js
// ✅ 正确：从静态位置淡入
tl.from(".title", { y: 60, opacity: 0, duration: 0.6, ease: "power3.out" }, sceneStart + 0.3);
tl.from(".subtitle", { y: 40, opacity: 0, duration: 0.5, ease: "power2.out" }, sceneStart + 0.5);

// ❌ 错误：不要在非最后场景做退出动画
// 转场本身就是 exit，不需要 gsap.to(..., { opacity: 0 })
```

### 字幕动画

```js
// 字幕逐字出现（卡拉OK效果）
// → 见 references/captions.md

// 简洁字幕
tl.from(".caption", { opacity: 0, y: 20, duration: 0.4 }, start + 0.2);
tl.to(".caption", { opacity: 0, duration: 0.3 }, end - 0.3);
```

### 转场（必须）

```js
// 场景1→2：淡入淡出
// clip-1 淡出（最后0.5秒）
tl.to("#clip-1", { opacity: 0, duration: 0.5 }, 4.5);
// clip-2 淡入（紧接）
tl.from("#clip-2", { opacity: 0, duration: 0.5 }, 5.0);
```

---

## 竖屏字号规范（9:16 · 1080×1920）

| 元素 | 字号 | 说明 |
|------|------|------|
| 主标题 | 72-96px | 前三秒抓眼球 |
| 二级标题 | 36-48px | 竖屏最佳阅读尺寸 |
| 正文/字幕 | 48-64px | 视频号最小可读底线 |
| 标签/注释 | 20-24px | 最小底线 |

---

## 完整流水线命令

### Step 1：初始化项目

```bash
cd /root/.openclaw/workspace
npx hyperframes init heyvideogen-project --non-interactive
cd heyvideogen-project
mkdir -p clips chunks slides compositions
```

### Step 2：生成分镜

```bash
python skills/videogen/scripts/v2/run_pipeline.py analyze "选题内容"
# 输出 storyboard.json
```

### Step 3：生成 TTS

```bash
python skills/videogen/scripts/v2/tts_harness.py \
  "$(cat storyboard.json | jq -r '.panels[].narration | select(. != null)' | paste -sd ' ')" \
  --output heyvideogen-output
```

### Step 4：生成 AI 视频片段

```bash
# 根据 storyboard.json 中的 video_prompt 批量生成
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode t2v \
  --prompt "$(cat storyboard.json | jq -r '.panels[0].video_prompt')" \
  --duration 6 \
  --output heyvideogen-project/clips/clip_01.mp4

# 多片段循环...
```

### Step 5：写入 HTML Composition

参考 `templates/apple-style/` 模板，写入 `index.html`

### Step 6：渲染

```bash
npx hyperframes lint
npx hyperframes render --output heyvideogen-output/final.mp4 --fps 30 --quality standard
```

### Step 7：合并音频

```bash
ffmpeg -y \
  -i heyvideogen-output/final.mp4 \
  -i heyvideogen-output/voiceover.mp3 \
  -c:v copy -c:a aac -b:a 192k -shortest \
  heyvideogen-output/video_final.mp4
```

### Step 8：压缩（视频号限制）

```bash
ffmpeg -y -i heyvideogen-output/video_final.mp4 \
  -c:v libx264 -crf 24 -preset fast \
  -c:a aac -b:a 96k \
  -movflags +faststart \
  heyvideogen-output/video_compressed.mp4
```

---

## 输出目录

```
heyvideogen-project/
├── index.html              # HyperFrames 主合成
├── compositions/           # 子合成
├── clips/                  # MiniMax Hailuo AI 片段
│   ├── clip_01.mp4
│   └── ...
├── voiceover.mp3           # TTS 配音
├── storyboard.json         # 分镜 JSON
├── DESIGN.md               # 视觉规范（如有）
└── heyvideogen-output/
    ├── video_final.mp4     # 合并后
    └── video_compressed.mp4 # 压缩后（发送用）
```

---

## 数字分身（与 Videogen 相同）

```bash
# ① 生成分身形象
python skills/ima-all-ai/scripts/ima_create.py \
  --task-type text_to_image \
  --model-id doubao-seedream-4.5 \
  --prompt "A professional Asian male tech speaker..." \
  --output heyvideogen-project/digital_host.png

# ② S2V-01 图生视频
python skills/minimax-multimodal/scripts/video/generate_video.py \
  --mode ref \
  --prompt "Person turns to camera, speaks with confidence" \
  --subject-image heyvideogen-project/digital_host.png \
  --duration 6 \
  --output heyvideogen-project/digital_host.mp4

# ③ HyperFrames overlay（用 CSS 定位在右下角）
```

---

## 触发词

- "做视频"、"生成视频"、"短视频制作"、"视频混剪"
- "用 HyperFrames 做"、"heygen 视频"
- "把[选题]做成视频"
- 主动触发：当 videogen 技能响应时，可推荐用 heyvideogen 替代

## 与 Videogen 的选择策略

| 场景 | 推荐技能 |
|------|---------|
| 需要大量精确动画/流程图/代码高亮 | Videogen（Remotion） |
| 需要 HTML 简单组合 + AI 片段 | **Heyvideogen** |
| 需要比 Remotion 更低的学习门槛 | **Heyvideogen** |
| 已有 HyperFrames 项目需要接 AI 片段 | **Heyvideogen** |
| 数字分身 + 复杂交互动画 | Videogen |
| 纯干货/PPT风 / 数据图表型 | 两者皆可，Heyvideogen 更快 |

---

## 参考文件索引

- `references/html-authoring.md` — HyperFrames HTML 写作完整规范（必读）
- `references/gsap-rules.md` — GSAP 动画规则（含 wrapper 规范、repeat 禁止等）
- `references/captions.md` — 字幕/卡拉OK效果
- `references/transitions.md` — 转场效果（含 video wrapper 规范）
- `references/tts.md` — TTS 工作流
- `templates/apple-style/` — Apple 风格竖屏模板
- `examples/storyboard-example.json` — 示例分镜
