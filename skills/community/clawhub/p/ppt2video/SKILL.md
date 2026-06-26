---
name: ppt-to-video
description: Convert PowerPoint presentations into narrated videos with Chinese voiceover, synchronized subtitles, and page-by-page audio sync. Use this skill when the user uploads a PPT file and wants a video explainer, training video, or course video generated from slides.
---

# PPT to Video Generator

将PPT课件自动转换为带中文旁白、同步字幕、音画精确对齐的讲解视频。

## 触发场景

- 用户上传PPT文件并要求生成视频
- 需要制作课程讲解视频、培训视频、演示视频
- 提到 "PPT转视频"、"课件视频"、"讲解视频"

## 核心原则

1. **PPT画面为主**：PPT本身已包含标题和要点，不叠加额外文字动画（避免重叠）
2. **音画精确同步**：每页独立音频，画面时长 = 音频精确时长
3. **字幕安全区**：底部15%独立区域，不与PPT画面重叠
4. **中文全流程**：旁白、字幕均为简体中文

## 工作流程

### Step 1: 提取PPT图片

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os

prs = Presentation("input.pptx")
output_dir = "public/slides"
os.makedirs(output_dir, exist_ok=True)

for i, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            image = shape.image
            filepath = os.path.join(output_dir, f"slide_{i:02d}.{image.ext}")
            with open(filepath, "wb") as f:
                f.write(image.blob)
            print(f"Slide {i}: {filepath}")
            break
```

**注意**：如果PPT是文字型（非图片型），需要额外截图或导出为图片。

### Step 2: 编写逐页讲解词

**原则**：
- 每页5-10秒讲解词
- 口语化，避免书面语
- 关键数据要强调
- 与PPT内容对应，不添加PPT上没有的信息

**格式**：
```
页1：今天聊AI视频的双轨实践
页2：感性路线Seedance用AI画画，理性路线Remotion用代码控制
页3：Seedance四大能力，但单次只支持四到十五秒
...
```

### Step 3: 生成逐页音频

**关键**：每页独立生成音频片段，不要生成一条全长音频

```bash
cd audio/pages
edge-tts --voice zh-CN-XiaoxiaoNeural --text "今天聊AI视频的双轨实践" --write-media p01.mp3
edge-tts --voice zh-CN-XiaoxiaoNeural --text "感性路线Seedance用AI画画" --write-media p02.mp3
# ... 每页一条
```

**推荐语音**：`zh-CN-XiaoxiaoNeural`（女声，专业清晰）

### Step 4: 测量音频时长并计算帧数

```bash
for f in p*.mp3; do
  duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  frames=$(python3 -c "print(int(float('$duration') * 24 + 0.5))")
  printf "%s: %.3fs = %d frames\n" "$f" "$duration" "$frames"
done
```

**计算公式**：`frames = int(duration_seconds * 24 + 0.5)`

### Step 5: 创建Remotion项目

**项目结构**：
```
remotion-ppt-video/
├── src/
│   ├── index.tsx          # registerRoot
│   └── PPTVideo.tsx       # 主组件
├── public/
│   ├── slides/            # PPT图片
│   │   ├── slide_01.png
│   │   └── ...
│   └── audio/             # 逐页音频
│       ├── p01.mp3
│       └── ...
├── audio/
│   └── pages/             # 音频源文件
├── out/                   # 输出目录
├── remotion.config.ts
└── tsconfig.json
```

**PPTVideo.tsx 核心结构**：

```typescript
const SLIDES = [
  { img: 'slides/slide_01.png', text: '今天聊AI视频的双轨实践', audio: 'audio/p01.mp3', frames: 75 },
  // ... 每页对应一条
];

// 计算累计起始帧
const starts: number[] = [];
let acc = 0;
for (const s of SLIDES) {
  starts.push(acc);
  acc += s.frames;
}
export const TOTAL_FRAMES = acc;
```

**布局规范**：
- PPT画面：上部85%，`objectFit: 'contain'`
- 字幕区：底部15%，独立深色背景 `#0a0a14`
- 分隔线：`borderTop: '1px solid rgba(255,255,255,0.06)'`
- 页码指示器：右上角，当前页橙色 `#ff6b35`

**Sequence使用**：
```typescript
<Sequence from={starts[index]} durationInFrames={slide.frames}>
  <Audio src={staticFile(slide.audio)} volume={0.95} />
  <SlideScene ... />
</Sequence>
```

### Step 6: 渲染视频

```bash
npx remotion render src/index.tsx ppt-video out/video.mp4 --overwrite --concurrency=1
```

**VPS优化参数**：
- 分辨率：854×480（内存友好）
- 帧率：24fps
- 并发：1（避免OOM）

## 关键技术点

### 音画同步

| 问题 | 解决方案 |
|------|---------|
| 旁白跨页 | 每页独立音频 |
| 画面切换与旁白不对齐 | `durationInFrames = 音频秒数 × fps` |
| 字幕与旁白不同步 | 每页字幕严格对应该页旁白 |

### 字幕安全区

```
┌─────────────────────────┐
│                         │
│    PPT画面 (85%)        │
│    完整显示，无遮挡      │
│                         │
├─────────────────────────┤  ← 分隔线
│    字幕安全区 (15%)     │
│    独立底色，不重叠      │
└─────────────────────────┘
```

### PPT画面处理

- 如果PPT文字已渲染为图片：直接提取使用
- 如果PPT是文字+形状：导出为PNG/截图
- 画面始终 `objectFit: 'contain'` 保持比例
- 背景色：`#0f0f1a`（与字幕区 `#0a0a14` 区分）

## 输出规范

- **格式**：MP4 (H.264)
- **分辨率**：854×480
- **帧率**：24fps
- **音频**：AAC，单声道或立体声
- **字幕**：内嵌画面（底部15%区域）

## 常见问题

**Q: PPT提取出来没有文字？**
A: PPT可能是图片型（文字已渲染为图像），需要用OCR识别或重新制作文字层。

**Q: 音频总时长超过90秒？**
A: 精简讲解词，每页控制在5-8秒。关键信息优先，细节可省略。

**Q: 渲染时内存不足？**
A: 降低分辨率到854×480，帧率24fps，并发设为1。

**Q: 字幕和PPT底部文字重叠？**
A: 检查是否正确设置了85%/15%分区。PPT画面必须在85%区域内。

**Q: 音画不同步？**
A: 确认每页独立音频，且 `durationInFrames` 精确等于音频时长×fps。不要用单条全长音频。

## 参数速查

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| fps | 24 | 流畅且节省资源 |
| 分辨率 | 854×480 | VPS安全渲染 |
| 画面比例 | 85% | 上部PPT画面 |
| 字幕比例 | 15% | 底部字幕安全区 |
| 语音 | zh-CN-XiaoxiaoNeural | 女声，专业 |
| 淡入时长 | 0.3秒 | 画面自然过渡 |
| 字幕淡入延迟 | 0.2秒 | 画面先出现 |
