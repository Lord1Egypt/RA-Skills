# Manim Animation 技术指南

## 目录

1. [Manim Community 概览](#manim-community-概览)
2. [场景代码结构](#场景代码结构)
3. [配音集成（manim-voiceover）](#配音集成manim-voiceover)
4. [字幕系统](#字幕系统)
5. [常用动画模式](#常用动画模式)
6. [高级技巧](#高级技巧)
7. [排错指南](#排错指南)

---

## Manim Community 概览

Manim Community（manim）是由社区维护的数学动画引擎，源自 3Blue1Brown 的 Grant Sanderson 创建的原版 manimgl。

**核心理念**：用 Python 代码描述数学动画，一切可编程、可版本控制、可自动化。

### 版本选择

| 版本 | 包名 | 特点 |
|------|------|------|
| **Manim Community** | `manim` | 社区维护，文档完善，插件生态丰富 |
| manimgl | `manimgl` | 3B1B 个人版，OpenGL 渲染，实时预览 |

**本 skill 使用 Manim Community（`pip install manim`）。**

---

## 场景代码结构

### 基础场景（纯动画）

```python
from manim import *

class BasicScene(Scene):
    def construct(self):
        # Create objects
        circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
        label = Text("圆形", font_size=24)
        label.next_to(circle, DOWN)

        # Animate
        self.play(Create(circle))
        self.play(Write(label))
        self.wait(1)

        # Transform
        square = Square(side_length=3, color=GREEN, fill_opacity=0.5)
        self.play(Transform(circle, square))
        self.wait(1)
```

### 配音场景（动画 + 语音 + 字幕）

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class NarrationScene(VoiceoverScene):
    def _make_subtitle(self, text_str):
        """Create subtitle with dark background at bottom."""
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

        # Scene 1: Title
        title = Text("标题", font_size=48, color=BLUE)
        sub_text = "欢迎来到演示视频。"
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            # FadeIn(sub) in the FIRST play() to sync subtitle with voice
            self.play(Write(title), FadeIn(sub), run_time=tracker.duration)
        self.play(FadeOut(sub))
        self.wait(0.3)

        # Scene 2: Content
        self.play(FadeOut(title))
        circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
        sub_text = "让我们创建一个圆形。"
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            self.play(Create(circle), FadeIn(sub), run_time=tracker.duration)
        self.play(FadeOut(sub))
        self.wait(0.3)
```

---

## 配音集成（manim-voiceover）

### TTS 引擎对比

| 引擎 | 安装 | 费用 | 网络 | 质量 | 中文 |
|------|------|------|------|------|------|
| **gTTS** | `pip install "manim-voiceover[gtts]"` | 免费 | 需要 | 中等 | ✅ |
| **pyttsx3** | `pip install "manim-voiceover[pyttsx3]"` | 免费 | 不需要 | 较低 | ✅ |
| **Azure** | `pip install "manim-voiceover[azure]"` | 付费 | 需要 | 高 | ✅ |
| **OpenAI** | `pip install "manim-voiceover[openai]"` | 付费 | 需要 | 高 | ✅ |
| **ElevenLabs** | `pip install "manim-voiceover[elevenlabs]"` | 付费 | 需要 | 很高 | ✅ |

### 核心模式

```python
# 1. 初始化 TTS 引擎
self.set_speech_service(GTTSService(lang="zh"))

# 2. voiceover 上下文管理器
with self.voiceover(text="语音文本") as tracker:
    # tracker.duration — TTS 语音时长（秒）
    # tracker.time_until_bookmark("mark1") — 到标记点的时间
    self.play(SomeAnimation(), run_time=tracker.duration)

# 3. 使用书签（bookmark）精确对齐
with self.voiceover(
    text='第一部分，<bookmark mark="A"/>第二部分。'
) as tracker:
    self.play(animation1, run_time=tracker.time_until_bookmark("A"))
    self.play(animation2, run_time=tracker.duration - tracker.time_until_bookmark("A"))
```

### 音频缓存

manim-voiceover 会缓存生成的 TTS 音频到 `media/voiceovers/` 目录：
- 相同文本不会重复生成
- 修改文本后自动重新生成
- 清除缓存：`rm -rf media/voiceovers/`

### SRT 字幕自动生成

manim-voiceover 会自动在视频同目录生成 `.srt` 字幕文件，格式标准，可被任何播放器加载。

---

## 字幕系统

### 方案 1：画面内字幕（Manim Text 对象）

在 Manim 画面内直接渲染字幕文本，作为动画的一部分。

**优点**：无需额外工具，字幕是动画的一部分
**缺点**：不可被播放器开关

```python
def _make_subtitle(self, text_str):
    sub = Text(text_str, font_size=22, color=WHITE, weight=BOLD)
    # Prevent subtitle from overflowing left/right edges
    max_width = config.frame_width - 1.0  # 0.5 margin each side
    if sub.width > max_width:
        sub.scale_to_fit_width(max_width)
    sub.to_edge(DOWN, buff=0.4)
    bg = BackgroundRectangle(sub, color=BLACK, fill_opacity=0.6, buff=0.15)
    return VGroup(bg, sub)

# Usage — FadeIn(sub) must be in the FIRST self.play() to sync with voice
with self.voiceover(text=sub_text) as tracker:
    sub = self._make_subtitle(sub_text)
    self.play(FadeIn(sub), SomeAnimation(), run_time=tracker.duration)
self.play(FadeOut(sub))
```

**⚠️ 字幕溢出保护**：`_make_subtitle()` 中使用 `scale_to_fit_width` 确保长文本不会超出画面左右边界。`font_size=22` 比默认 28 更适合长句子。

**⚠️ 字幕同步**：`FadeIn(sub)` 必须放在 voiceover 块内的**第一个** `self.play()` 调用中，否则字幕会滞后于声音。

### 方案 2：SRT 外挂字幕（ffmpeg 烧录）

使用 manim-voiceover 自动生成的 SRT 文件，通过 ffmpeg 烧录到视频。

**优点**：字幕样式灵活，可单独编辑 SRT 文件
**缺点**：需要 ffmpeg + libass（安装 ffmpeg-full 即可）

```bash
ffmpeg -y -i video.mp4 \
    -vf "subtitles=subtitle.srt:force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,BackColour=&H80000000,BorderStyle=4,MarginV=30'" \
    -c:a copy \
    output_subtitled.mp4
```

### ⚠️ 避免双字幕

**不要** 同时使用画面内字幕（`_make_subtitle`）和 SRT 烧录，否则画面上会出现两层重叠的字幕。

**正确做法**：二选一
- **方案 A（推荐）**：代码内使用 `_make_subtitle()` 渲染字幕，不烧录 SRT。字幕随动画同步，无需额外处理。
- **方案 B**：代码内不渲染字幕，使用 ffmpeg 烧录 SRT。字幕样式可通过 `force_style` 灵活控制。

---

## 常用动画模式

### 标题 + 副标题

```python
title = Text("主标题", font_size=48, color=BLUE)
subtitle = Text("副标题", font_size=28, color=GRAY)
subtitle.next_to(title, DOWN, buff=0.5)

self.play(Write(title))
self.play(FadeIn(subtitle))
self.wait(1)
self.play(title.animate.to_edge(UP), FadeOut(subtitle))
```

### 公式推导

```python
eq1 = MathTex(r"x^2 + y^2 = r^2")
eq2 = MathTex(r"y = \pm\sqrt{r^2 - x^2}")
eq2.next_to(eq1, DOWN, buff=0.5)

self.play(Write(eq1))
self.wait(0.5)
self.play(TransformMatchingShapes(eq1.copy(), eq2))
```

### 图形变换

```python
circle = Circle(radius=1.5, color=RED, fill_opacity=0.5)
square = Square(side_length=3, color=GREEN, fill_opacity=0.5)

self.play(Create(circle))
self.wait(0.5)
self.play(Transform(circle, square))
```

### 坐标系 + 函数图像

```python
axes = Axes(
    x_range=[-3, 3, 1],
    y_range=[-2, 2, 1],
    axis_config={"include_numbers": True}
)
graph = axes.plot(lambda x: np.sin(x), color=YELLOW)
label = axes.get_graph_label(graph, r"\sin(x)")

self.play(Create(axes))
self.play(Create(graph), Write(label))
```

### 分组 + 排列

```python
items = VGroup(
    Square(color=RED),
    Circle(color=GREEN),
    Triangle(color=BLUE),
)
items.arrange(RIGHT, buff=0.8)
items.scale(0.8)

self.play(LaggedStart(*[Create(item) for item in items], lag_ratio=0.3))
```

### 场景过渡

```python
# 淡出所有对象，开始新场景
self.play(*[FadeOut(mob) for mob in self.mobjects])
self.wait(0.3)
```

---

## 高级技巧

### 多场景拼接

一个文件可包含多个 Scene 类，按顺序渲染后用 ffmpeg 拼接：

```bash
# Render all scenes
manim render -qh scenes.py Scene1
manim render -qh scenes.py Scene2
manim render -qh scenes.py Scene3

# Concat
echo "file 'Scene1.mp4'" > list.txt
echo "file 'Scene2.mp4'" >> list.txt
echo "file 'Scene3.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy final.mp4
```

### 自定义字体

```python
Text("自定义字体", font="PingFang SC", font_size=36)
```

### 颜色主题

```python
# Manim 内置颜色常量
RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, PINK, GOLD, WHITE, GRAY
# Hex 颜色
Text("文字", color="#FF6B6B")
```

### LaTeX + Manim 联动

```python
# 行内公式
formula = MathTex(r"E = mc^2", font_size=72, color=YELLOW)
# 带对齐的多行公式
aligned = MathTex(
    r"f(x) &= x^2 + 2x + 1 \\",
    r"&= (x+1)^2"
)
```

---

## 排错指南

### 1. `ModuleNotFoundError: No module named 'pkg_resources'`

**原因**：Python 3.12+ 中 setuptools 变更

**解决**：
```bash
pip install "setuptools>=69.0,<72.0"
```

### 2. `UnknownCodecError: libx264`

**原因**：Manim 硬编码使用 `libx264` 编码器，但当前 ffmpeg 未编译 libx264 支持（常见于 conda 环境的 ffmpeg 默认 `--disable-gpl`）。

**解决**：
```bash
# 方案 A：macOS Homebrew — 安装 ffmpeg-full（推荐，一次性解决 libx264 + libass）
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg-full
brew link --force ffmpeg-full

# 方案 B：Conda 环境 — 安装 x264 包
conda install x264 -c conda-forge

# 验证
ffmpeg -codecs 2>&1 | grep libx264
# 输出应包含: encoders: libx264 libx264rgb
```

### 3. `ffmpeg: No such filter: 'subtitles'`

**原因**：ffmpeg 编译时未包含 libass

**解决**（macOS）：
```bash
# ffmpeg-full 已包含 libass，如已安装则无需额外操作
brew tap homebrew-ffmpeg/ffmpeg
brew install homebrew-ffmpeg/ffmpeg/ffmpeg-full
brew link --force ffmpeg-full

# 验证
ffmpeg -filters 2>&1 | grep subtitles
```

### 4. gTTS 报错 `gTTSError: Connection error`

**原因**：网络无法访问 Google TTS 服务

**解决**：
```python
# 方案 1: 使用代理
import os
os.environ['HTTP_PROXY'] = 'http://proxy:port'

# 方案 2: 切换为离线 TTS
from manim_voiceover.services.pyttsx3 import Pyttsx3Service
self.set_speech_service(Pyttsx3Service())
```

### 5. 中文文字显示为方块

**原因**：系统缺少中文字体

**解决**：
```bash
# Linux
sudo apt install fonts-noto-cjk

# macOS (built-in PingFang SC, usually OK)

# 指定字体
Text("文字", font="Noto Sans CJK SC")
```

### 6. `WARNING: Some options were not used: shortest, metadata`

**原因**：Manim 调用 FFmpeg 时传递了未使用的选项

**解决**：可安全忽略，不影响输出视频。

### 7. 渲染速度慢

**建议**：
- 开发阶段使用 `-ql`（480p15）快速预览
- 最终输出使用 `-qh`（1080p60）或 `-qp`（4K）
- voiceover 音频有缓存，第二次渲染会快很多

### 8. 视频无声音

**检查**：
- 确认使用 `VoiceoverScene` 而非 `Scene`
- 确认调用了 `self.set_speech_service()`
- 确认 voiceover 块内有动画（空块不会产生音频）
- 检查 `media/voiceovers/` 目录是否有 `.mp3` 文件
