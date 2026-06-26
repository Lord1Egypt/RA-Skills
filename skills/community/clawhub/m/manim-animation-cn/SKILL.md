---
name: manim-animation
description: "Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, 数学动画, 动画配音, 动画字幕, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos."
required_tools:
  - name: manim
    install: "pip install manim"
  - name: ffmpeg
    install: "brew install ffmpeg (macOS) / apt install ffmpeg (Linux)"
    notes: "Must include libx264 encoder and libass (for subtitle burn-in)"
  - name: python3
    install: "Python 3.9+ required"
required_packages:
  - "manim"
  - "manim-voiceover[gtts]"
network_access:
  - service: "Google TTS (gTTS)"
    purpose: "Text-to-speech synthesis for voiceover narration"
    required: false
    notes: "Default TTS engine. Can be replaced with offline pyttsx3 if network is unavailable."
---

# Manim Animation: 动画 + 配音 + 字幕 生成器

**Author:** ericksun（孙自翔）

## 概述

本技能使用 Manim Community 生成数学/教育动画，并通过 manim-voiceover 插件集成 TTS 语音旁白和同步字幕。所有处理均在本地运行，无需付费 API。

**核心能力：**
- 🎬 **动画生成**：使用 Manim 创建数学公式、几何图形、图表等动画
- 🎙️ **语音旁白**：通过 manim-voiceover 插件集成 TTS，动画与语音自动同步
- 📝 **字幕系统**：画面内字幕（Manim Text）+ SRT 外挂字幕（ffmpeg 烧录）
- 🔄 **一键流水线**：描述需求 → 生成代码 → 渲染视频 → 烧录字幕

**TTS 引擎（优先 gTTS）：**
- **gTTS**（推荐）：Google 免费 TTS，支持中文，无需 API Key
- **pyttsx3**（备选）：离线 TTS，无需网络
- **Azure/OpenAI/ElevenLabs**（高质量）：需付费 API Key

## 前置条件

### 🔍 一键环境检查

**首次使用前，运行环境检查脚本确认所有依赖已就绪：**

```bash
python3 {SKILL_DIR}/scripts/check_environment.py
```

该脚本检查：
- ✅ Manim Community 安装（`manim` 命令）
- ✅ manim-voiceover + gTTS 插件
- ✅ FFmpeg + libx264 编码器（Manim 硬编码依赖，**必需**）
- ✅ FFmpeg + libass（用于 SRT 字幕烧录）
- ✅ Python 依赖
- ✅ 中文字体可用性

### 必需的系统工具

- **Manim Community**：`pip install manim`
- **FFmpeg（含 libx264 + libass）**：Manim 硬编码使用 `libx264` 编码器渲染视频，字幕烧录需要 `libass`
  - macOS（Homebrew）：`brew install ffmpeg`（默认包含 x264 和 libass）
  - macOS（Conda）：`conda install x264 -c conda-forge`（**⚠️ conda 的 ffmpeg 默认不含 libx264**）
  - Linux：`sudo apt install ffmpeg libx264-dev libass-dev`
- **Python 3.9+** 及 pip

### 必需的 Python 包

```bash
# Core
pip install manim

# Voiceover + TTS
pip install "manim-voiceover[gtts]"
```

### 可选（增强功能）

- **pyttsx3**：离线 TTS（`pip install "manim-voiceover[pyttsx3]"`）

### ⚡ 快速安装

```bash
pip install manim "manim-voiceover[gtts]"

# macOS (Homebrew) — 推荐，自带 libx264 + libass
brew install ffmpeg

# macOS (Conda) — 需额外安装 x264，否则 Manim 渲染会报错 UnknownCodecError: libx264
conda install x264 -c conda-forge

# 验证 ffmpeg 支持 libx264 和 libass
ffmpeg -codecs 2>&1 | grep libx264     # 应显示 encoders: libx264
ffmpeg -filters 2>&1 | grep subtitles  # 应显示 subtitles filter
```

## 工作流程

### 快速开始 — 一键运行

用户描述需求后，使用流水线脚本一键完成：

```bash
python3 {SKILL_DIR}/scripts/run_pipeline.py \
    --scene_file <场景文件.py> \
    --scene_name <SceneName> \
    --quality high \
    --burn_subtitles
```

**常用选项：**

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--scene_file` | 必需 | Manim 场景 Python 文件 |
| `--scene_name` | 必需 | 场景类名 |
| `--quality` | `high` | 渲染质量：`low`/`medium`/`high`/`production` |
| `--burn_subtitles` | False | 是否用 ffmpeg 烧录 SRT 字幕 |
| `--speed` | `1.35` | 播放倍速（如 1.35 表示加速到 1.35 倍，设为 1.0 则不加速） |
| `--preview` | False | 渲染后自动打开预览 |
| `--output_dir` | `./output` | 输出目录 |

### 完整工作流程（4 步）

#### 步骤 1：理解用户需求并生成 Manim 场景代码

根据用户描述，生成 Manim 场景 Python 文件。场景代码需遵循以下模式：

**无配音模式**（纯动画）：

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        title = Text("标题", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
```

**配音模式**（动画 + 语音 + 字幕）：

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MyScene(VoiceoverScene):
    def _make_subtitle(self, text_str):
        """Create subtitle with dark background at bottom of screen."""
        sub = Text(text_str, font_size=22, color=WHITE, weight=BOLD)
        # Prevent subtitle from overflowing left/right edges
        max_width = config.frame_width - 1.0  # 0.5 margin each side
        if sub.width > max_width:
            sub.scale_to_fit_width(max_width)
        sub.to_edge(DOWN, buff=0.4)
        bg = BackgroundRectangle(sub, color=BLACK, fill_opacity=0.6, buff=0.15)
        return VGroup(bg, sub)

    def construct(self):
        self.set_speech_service(GTTSService(lang="zh"))

        sub_text = "欢迎来到演示"
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            title = Text("演示", font_size=48)
            self.play(Write(title), FadeIn(sub), run_time=tracker.duration)

        self.play(FadeOut(sub))
        self.wait(0.3)
```

**关键模式 — voiceover 上下文管理器：**

```python
with self.voiceover(text="语音文本") as tracker:
    # tracker.duration = TTS 语音时长（秒）
    # 在此块内的动画会与语音自动同步
    self.play(SomeAnimation(), run_time=tracker.duration)
```

`with self.voiceover(text=...) as tracker` 做了三件事：
1. 调用 TTS 引擎生成语音
2. 自动计算语音时长
3. 提供 `tracker.duration` 让动画与语音同步

**字幕最佳实践：**
- 画面内字幕：使用 `_make_subtitle()` 辅助函数，在屏幕底部显示带暗背景的白色粗体文字
- **防止溢出**：`_make_subtitle()` 会自动检测字幕宽度，超出画面时等比缩放（`scale_to_fit_width`），使用 `font_size=22` 以适配长文本
- **字幕同步**：在 voiceover 块内的**第一个** `self.play()` 中就 `FadeIn(sub)`，确保字幕与声音同步出现，不要延后
- 每个 voiceover 块开始时 FadeIn 字幕，结束后 FadeOut
- 字幕文本应与 voiceover text 相同

**⚠️ 避免双字幕：** 如果场景代码中已使用 `_make_subtitle()` 渲染了画面内字幕，则 **不要** 再用 `--burn_subtitles` 烧录 SRT 字幕，否则画面上会出现两层重叠的字幕。两种字幕方案只能选其一：
- 方案 A（推荐）：代码内使用 `_make_subtitle()` 渲染字幕，不烧录 SRT
- 方案 B：代码内不渲染字幕，通过 `--burn_subtitles` 烧录 SRT

#### 步骤 2：配置渲染参数

在场景文件同目录创建 `manim.cfg`：

```ini
[CLI]
quality = high_quality
preview = False

[ffmpeg]
video_codec = h264
```

**质量对照表：**

| 质量 | 标志 | 分辨率 | FPS | manim.cfg 值 |
|------|------|--------|-----|-------------|
| Low | -ql | 480p | 15 | low_quality |
| Medium | -qm | 720p | 30 | medium_quality |
| High | -qh | 1080p | 60 | high_quality |
| Production | -qp | 2160p | 60 | production_quality |

#### 步骤 3：渲染视频

```bash
manim render <scene_file.py> <SceneName>
```

输出路径模式：`media/videos/<file>/<resolution>/<SceneName>.mp4`

#### 步骤 4：烧录 SRT 字幕（可选）

manim-voiceover 会自动在视频同目录生成 `.srt` 字幕文件。使用 ffmpeg 烧录：

```bash
ffmpeg -y -i <video.mp4> \
    -vf "subtitles=<subtitle.srt>:force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,BackColour=&H80000000,BorderStyle=4,MarginV=30'" \
    -c:a copy \
    <output_subtitled.mp4>
```

**⚠️ 双字幕陷阱**：如果场景 Python 代码中已经用 `_make_subtitle()` 渲染了画面内字幕，就 **不要** 再烧录 SRT 字幕，否则会出现两层重叠字幕。

**注意**：ffmpeg 需要 libass 支持。macOS 用 `brew install ffmpeg` 通常已包含。Conda 环境需额外安装 `conda install x264 -c conda-forge`。

#### 步骤 5：加速视频（可选）

使用 ffmpeg 对视频进行倍速处理，默认加速到 1.35 倍：

```bash
SPEED=1.35
ffmpeg -y -i <input.mp4> \
    -filter_complex "[0:v]setpts=PTS/${SPEED}[v];[0:a]atempo=${SPEED}[a]" \
    -map "[v]" -map "[a]" \
    <output_fast.mp4>
```

**注意**：加速应在最终输出步骤执行。如果场景代码已有画面内字幕（`_make_subtitle`），加速输入应使用原始视频（非 SRT 烧录版），避免双字幕。`run_pipeline.py` 的 `--speed` 参数已自动处理此逻辑。

## Manim 常用动画速查

### 创建/显示动画
- `Write(text)` — 书写文字
- `Create(mobject)` — 绘制形状
- `FadeIn(mobject)` / `FadeOut(mobject)` — 淡入淡出
- `DrawBorderThenFill(mobject)` — 先画边框再填充

### 变换动画
- `Transform(source, target)` — 变形
- `ReplacementTransform(source, target)` — 替换变形
- `TransformMatchingShapes(source, target)` — 形状匹配变形

### 移动/缩放
- `mobject.animate.to_edge(UP)` — 移动到边缘
- `mobject.animate.shift(RIGHT * 2)` — 平移
- `mobject.animate.scale(2)` — 缩放
- `Rotate(mobject, angle=PI)` — 旋转

### 常用对象
- `Text("文字", font_size=48, color=BLUE)` — 文字
- `MathTex(r"e^{i\pi}+1=0")` — LaTeX 公式
- `Circle(radius=1, color=RED)` — 圆
- `Square(side_length=2, color=GREEN)` — 正方形
- `Arrow(start, end)` — 箭头
- `NumberPlane()` — 坐标平面
- `Axes(x_range, y_range)` — 坐标轴

### 分组与排列
- `VGroup(obj1, obj2)` — 垂直分组
- `group.arrange(RIGHT, buff=0.5)` — 水平排列
- `BackgroundRectangle(obj, color=BLACK, fill_opacity=0.6)` — 背景矩形

## 已知问题与解决方案

### ⚠️ libx264 编解码器缺失（最常见问题）

**症状**：`UnknownCodecError: libx264`

**根因**：Manim 在 `scene_file_writer.py` 中**硬编码**使用 `libx264` 编码器（无法通过 config/cfg 覆盖），但 conda 环境的 ffmpeg 编译时 `--disable-gpl`，不包含 GPL 许可的 libx264。

**解决**：
```bash
# Conda 环境（最常见场景）
conda install x264 -c conda-forge
# 安装后 conda-forge 的 ffmpeg 会自动重新链接 x264 库

# 验证
ffmpeg -codecs 2>&1 | grep libx264
# 应输出包含: encoders: libx264 libx264rgb
```

**注意**：`brew install ffmpeg` 安装的 ffmpeg 自带 x264，但 conda 环境优先使用自己安装的 ffmpeg，不会使用 Homebrew 版本。

### setuptools 兼容性
`manim-voiceover` 依赖 `pkg_resources`，Python 3.12+ 可能报错：
```bash
pip install "setuptools>=69.0,<72.0"
```

### ffmpeg 缺少 libass
SRT 字幕烧录需要 libass。macOS：
```bash
brew install ffmpeg
# 验证
ffmpeg -filters 2>&1 | grep subtitles
```

Linux：
```bash
sudo apt install libass-dev
# 可能需要重新编译 ffmpeg
```

### gTTS 网络问题
gTTS 需要访问 Google TTS 服务，如网络不通可切换为 pyttsx3 离线引擎：
```python
from manim_voiceover.services.pyttsx3 import Pyttsx3Service
self.set_speech_service(Pyttsx3Service())
```

### 中文字体
Manim 使用系统字体渲染 `Text` 对象，确保系统有中文字体：
- macOS：PingFang SC（系统自带）
- Linux：`sudo apt install fonts-noto-cjk`
- 指定字体：`Text("文字", font="PingFang SC")`

## 相关资源

- **GitHub 仓库**：https://github.com/hzsunzixiang/manim-animation-skill
- **Manim 技术指南**：`references/manim_guide.md` — 详细的 Manim + voiceover + 字幕技术文档
- **环境检查脚本**：`scripts/check_environment.py` — 一键检查所有依赖
- **渲染流水线脚本**：`scripts/run_pipeline.py` — 一键渲染 + 字幕烧录
