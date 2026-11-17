---
name: ppt-to-video
description: |
  将 PPT/PPTX 文件转换为带背景音乐的 MP4 视频。
  支持智能时长（封面1.5s/正文按180字分）、翻页动画（上翻/对角线）、正文页打字机文字渐入效果。
  触发词："PPT转视频"、"PPT生成视频"、"PPT加音乐"、"将PPT做成视频"、"PPT to video"。
---

# PPT to Video（优化版）

将 PPT 文件转换为带背景音乐的 MP4 视频，支持三种视觉优化。

## 触发条件

| 中文触发词 | 英文触发词 |
|---|---|
| PPT转视频 | convert PPT to video |
| PPT生成视频 | PPT to MP4 with music |
| PPT加音乐 / 加BGM | PPT export video |
| 将PPT做成视频 | PPT with typewriter effect |
| 正文页打字机效果 | — |

## 三个核心优化

### ① 智能时长

| 页面类型 | 判断规则 | 时长 |
|---|---|---|
| 封面/过渡页 | 首页、字数 < 50 | **固定 1.5 秒** |
| 封底（末页）| 最后一页 | **固定 4.0 秒**（可通过 `--back-cover-dur` 调整）|
| 正文内容页 | 其他页 | **按 180字/分（=3字/秒）计算，范围 6~8 秒** |

计算公式：`duration = clamp(char_count / 3.0, 6.0, 8.0)`

### ② 翻页动画

通过 ffmpeg `xfade` 滤镜实现，支持四种模式：

| 参数值 | 效果 | 说明 |
|---|---|---|
| `slideup`（默认）| 向上翻页 | 下一页从底部向上推入 |
| `diagtl` | 从右下向左上翻页 | 对角线过渡，视觉更动感 |
| `fade` | 淡入淡出 | 经典交叉溶解 |
| `none` | 无动画 | 直接切换（最快渲染） |

动画时长默认 0.5 秒，可通过 `--transition-dur` 调整。

### ③ 打字机文字渐入

对**正文内容页**启用，封面/过渡页保持静态。

**实现原理：**
- 提取该页文字内容
- 通过 ffmpeg `drawtext` 滤镜逐字显示（每帧增加若干字符）
- 文字居中叠加在背景图上，带半透明底色

**局限性（重要）：**
- 无法完全还原 PPT 原始排版（字体、颜色、精确位置）
- 采用「整页居中 + 半透明底」的简化方案
- 若需完全还原 PPT 排版动画，建议使用 PPT 自带动画 + 屏幕录制

**如需完全还原排版，** 可扩展方案：
1. 用 COM 自动化逐字触发 PPT 动画并截图
2. 或用 manim 等动画库重新渲染

---

## 依赖检查

执行前必须确认以下工具已安装：

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| `python-pptx` | 读取 PPT 文字内容 | `pip install python-pptx` |
| `Pillow` | 图片处理 | `pip install pillow` |
| `ffmpeg` + `ffprobe` | 视频/音频合成 | 见下方 |
| `pywin32` | COM 方案（Windows+PPT）| `pip install pywin32` |
| `pdf2image` + `poppler` | LibreOffice PDF→PNG 方案 | `pip install pdf2image` |

**渲染质量说明：**
- **COM 方案**（Windows）：自动设置 PowerPoint 导出分辨率为 **300DPI**（修改注册表 `ExportBitmapResolution=300`）
- **LibreOffice 方案**：优先使用 **PDF→PNG（300DPI）**，质量最高；失败后后备直接 PNG 导出

**安装 ffmpeg：**
```bash
# Windows（scoop）
scoop install ffmpeg

# macOS（Homebrew）
brew install ffmpeg

# Linux
sudo apt install ffmpeg   # Debian/Ubuntu
```

---

## 执行流程

### Step 1：收集输入参数

向用户确认：

1. **PPT 文件路径**（必填）：`.ppt` / `.pptx`
2. **背景音乐路径**（必填）：`.mp3` / `.wav` / `.m4a`
3. **翻页动画**（可选）：`slideup`（默认）/`diagtl`/`fade`/`none`
4. **打字机效果**（可选）：是否启用（`--typewriter`）
5. **输出路径**（可选）：默认与 PPT 同目录，`.mp4` 扩展名

### Step 2：检查依赖

```bash
ffmpeg -version
python -c "import pptx; import PIL; print('依赖正常')"
```

若缺失，自动安装：`pip install python-pptx pillow`

### Step 3：执行转换

使用 bundled 脚本 `scripts/ppt_to_video.py`：

```bash
python "C:\Users\LENOVO\.workbuddy\skills\ppt-to-video\scripts\ppt_to_video.py" \
  "<PPT路径>" \
  "<音频路径>" \
  --transition slideup \
  --typewriter \
  --cover-dur 1.5 \
  --content-cps 3.0 \
  --content-min 6.0 \
  --content-max 8.0 \
  --fps 25
```

**参数说明：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ppt` | （必填）| PPT/PPTX 文件路径 |
| `audio` | （必填）| 背景音乐文件路径 |
| `--transition` | `slideup` | 翻页动画类型 |
| `--transition-dur` | `0.5` | 翻页动画时长（秒）|
| `--typewriter` | 不启用 | 为正文页启用打字机效果 |
| `--cover-dur` | `1.5` | 封面/过渡页时长（秒）|
| `--content-cps` | `3.0` | 正文页语速（字/秒），3.0 = 180字/分 |
| `--content-min` | `6.0` | 正文页最短时长（秒）|
| `--content-max` | `8.0` | 正文页最长时长（秒）|
| `--fps` | `25` | 输出视频帧率 |
| `--output` | 同目录 `.mp4` | 输出视频路径 |
| `--keep-temp` | 不保留 | 保留临时文件（调试用）|

### Step 4：PPT 转图片（内部逻辑）

脚本按以下**优先级**自动选择渲染方案：

**方案 1 — COM 自动化（Windows + 安装 PowerPoint）：**
- 调用 `win32com.client` 启动 PowerPoint（后台无窗口）
- **自动设置 300DPI 导出分辨率**（修改注册表 `ExportBitmapResolution=300`）
- 每页用 `Slide.Export()` 导出为 PNG（1920×1080）
- **质量最高**，推荐 Windows 用户使用

**方案 2 — LibreOffice PDF→PNG（跨平台，质量最高）：**
- `soffice --convert-to pdf:writer_pdf_Export` 导出 PDF
- `pdf2image.convert_from_path(pdf_path, dpi=300)` 转 PNG
- **质量最高（300DPI）**，后续 ffmpeg 会缩放到 1920×1080

**方案 3 — LibreOffice 直接 PNG 导出（后备）：**
- `soffice --convert-to png` 直接导出 PNG
- 速度较快，质量略低于 PDF→PNG 方案

**三种方案均不可用时的提示：**
```
无法将 PPT 转换为图片。请尝试：
1. 安装 LibreOffice：https://www.libreoffice.org/
2. 或安装 PowerPoint 并确认 pywin32 已安装
```

**渲染质量对比：**

| 方案 | 分辨率 | 质量 | 速度 | 依赖 |
|---|---|---|---|---|
| COM（300DPI）| 1920×1080（原生）| ⭐⭐⭐⭐⭐ | 快 | PowerPoint + pywin32 |
| LibreOffice PDF→PNG（300DPI）| 300DPI → 缩放 | ⭐⭐⭐⭐ | 中 | LibreOffice + pdf2image |
| LibreOffice 直接 PNG | 默认 | ⭐⭐⭐ | 快 | LibreOffice |

### Step 5：视频合成逻辑

**有翻页动画（`slideup`/`diagtl`/`fade`）：**

1. 为每张图片生成独立视频片段（loop + t）
2. 用 ffmpeg `xfade` 滤镜串联所有片段并加入翻页动画
3. 背景音乐按总时长循环叠加
4. 输出 H.264 + AAC 的 MP4 文件

**无翻页动画（`none`）：**

1. 生成 concat demuxer 文本文件
2. 图片按指定时长拼接
3. 背景音乐循环叠加

**打字机效果（需 `--typewriter` 参数）：**

1. 封面/过渡页：原图直接渲染，无效果
2. 正文页：
   - 提取该页文字
   - 用 ffmpeg `drawtext` 滤镜逐字显示
   - 文字居中，带半透明黑色底色
3. 所有页通过 `xfade` 串联翻页动画
4. 叠加循环背景音乐

---

## 输出结果

执行成功后告知用户：

```
✅ 视频已生成：<输出路径>
   共 N 页，总时长：XX.X 秒
   分辨率：1920×1080，帧率：25fps
   翻页动画：slideup（0.5s）
   打字机效果：已启用（正文页）
   背景音乐：<音频文件名>（循环 N 次）
   渲染方案：COM (PowerPoint 原生，300DPI)  ← 新增
```

并将生成的 `.mp4` 文件通过 `deliver_attachments` 工具交付给用户。

---

## 常见问题

**Q：提示"ffmpeg 不是内部或外部命令"**
> 需要先安装 ffmpeg 并加入 PATH。参考上方"依赖检查"小节。

**Q：打字机效果没有显示文字**
> 可能是系统字体路径不正确。脚本会自动检测中文字体，若失败则使用 `arial.ttf`。可手动修改 `detect_system_font()` 函数中的字体路径。

**Q：可以不要背景音乐吗？**
> 当前版本必须提供背景音乐。如不需要音乐，可以提供一段静音音频文件：
> ```bash
> ffmpeg -f lavfi -i anullsrc -t 60 -c:a aac silence.aac
> ```

**Q：翻页动画可以每页不同吗？**
> 当前版本所有页面使用同一种翻页动画。如需每页不同，需要修改脚本中的 `xfade` 滤镜参数。

**Q：打字机效果可以还原 PPT 原始排版吗？**
> 当前简化方案无法还原原始排版。如需完全还原，建议使用：
> 1. PPT 自带动画 + 屏幕录制
> 2. 或用 COM 自动化逐字触发动画并截图（复杂，不在本脚本范围内）

---

## 技术备注

- PPT 渲染方案优先级：COM（Windows+PPT）> LibreOffice（跨平台）
- 输出视频采用 H.264 编码（兼容性最好）
- 临时文件默认执行完后自动清理，加 `--keep-temp` 可保留
- 脚本路径：`C:\Users\LENOVO\.workbuddy\skills\ppt-to-video\scripts\ppt_to_video.py`
- 打字机效果使用的 ffmpeg drawtext 参数：
  - `draw='min(int(n*{char_rate}),{chars})'` — 控制逐字显示
  - `enable='gte(t,0)'` — 从 t=0 开始显示
  - `box=1:boxcolor=black@0.5` — 半透明底色

---

## 示例命令

**基础用法（默认上翻动画，无打字机效果）：**
```bash
python ppt_to_video.py presentation.pptx bg_music.mp3 --transition slideup
```

**启用打字机效果：**
```bash
python ppt_to_video.py presentation.pptx bg_music.mp3 --typewriter --transition diagtl
```

**自定义时长参数：**
```bash
python ppt_to_video.py presentation.pptx bg_music.mp3 \
  --cover-dur 2.0 \
  --content-cps 2.5 \
  --content-min 5.0 \
  --content-max 10.0
```

**无动画（最快渲染）：**
```bash
python ppt_to_video.py presentation.pptx bg_music.mp3 --transition none
```

---

## 踩坑经验

### xfade offset 计算公式（经过 3 次试错才成功）

**错误写法（不要这样写）：**
```python
# ❌ 错误：只减去一次 transition_dur
offset = cumulative - transition_dur
```

**正确公式：**
```python
# ✅ 正确：第 i 个过渡的 offset
#   = sum(durations[0..i]) - (i+1) * transition_dur
for i, (_, dur, _) in enumerate(durations[:-1]):
    cumulative += dur
    offset = round(cumulative - (i + 1) * transition_dur, 2)
```

**总时长公式：**
```
总时长 = sum(all durations) - (n-1) * transition_dur
```

**验证例子（3 张幻灯片，transition_dur=0.5）：**
- 时长：[1.5, 1.5, 3.0]
- offsets：[1.0, 2.0]
- 总时长：1.5 + 1.5 + 3.0 - 2×0.5 = 5.0 秒 ✓

---

### 音频叠加 `-t` 参数

**错误写法：**
```python
"-t", str(video_dur + transition_dur),   # ❌ 时长会偏长
```

**正确写法：**
```python
correct_total = calc_total_duration(durations, transition_dur)
"-t", str(correct_total),   # ✅ 用 calc_total_duration() 计算
```

**原因：** xfade 过渡会重叠两段视频，总时长会减去 `(n-1) * transition_dur`，音频叠加时必须用这个正确总时长，否则视频末尾会被截断或拉长。

---

### ffmpeg `-t` 与 `-shortest` 混用注意

- 叠加音频时用了 `-stream_loop`，必须配合 `-t` 限制总时长
- `-shortest` 在 `-stream_loop` 存在时**不会生效**（音频被循环拉长了）
- 正确做法：用 `calc_total_duration()` 计算正确总时长，传给 `-t`

---

### PowerPoint 2007（12.0）COM 兼容性

**问题：** `powerpoint.Visible = False` 在 PowerPoint 2007 中抛出 `com_error: (-2147352567, '发生意外。')`

**解决方案：**
```python
try:
    powerpoint.Visible = False
except Exception:
    pass  # PowerPoint 2007 不支持此属性
```

**注册表版本兼容：** `_set_ppt_export_resolution()` 需包含 `"12.0"` 版本号。

**Export 参数兼容：** PowerPoint 2007 的 `Slide.Export()` 支持 4 参数（FileName, FilterName, ScaleWidth, ScaleHeight），与新版一致。代码中保留了 try/except 到 2 参数的降级通路作为兜底。

---

### pix_fmt=yuv444p 兼容性问题

**现象：** 生成视频在某些播放器（Windows 播放器/微信等）无法播放，报 `0x80004005` 错误。

**根因：** ffmpeg xfade `-filter_complex` 合成时，如果没有显式指定 `-pix_fmt yuv420p`，ffmpeg 可能默认输出 `yuv444p` 格式。后续 Step C 使用 `-c:v copy` 直接复制视频流，`yuv444p` 格式会被原样保留到最终 MP4 中。`yuv444p` 虽然质量更高，但兼容性差，很多常见播放器不支持。

**修复（两处 xfade intermediate 合成命令）：**
```python
# ❌ 错误：xfade 合成时缺少 -pix_fmt
cmd += [
    "-filter_complex", filter_complex,
    "-map", prev_label,
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-an",
    intermediate_path
]

# ✅ 正确：显式指定 yuv420p
cmd += [
    "-filter_complex", filter_complex,
    "-map", prev_label,
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-pix_fmt", "yuv420p",   # ← 必须！
    "-an",
    intermediate_path
]
```

**涉及位置：**
- `build_video_with_transitions()` — 翻页动画 intermediate 合成
- `build_video_with_typewriter()` — 打字机效果 intermediate 合成

**教训：** 任何 ffmpeg 中间产物（尤其后续会被 `-c:v copy` 的），都要显式指定 `-pix_fmt yuv420p`，不要依赖 ffmpeg 默认值。

---
