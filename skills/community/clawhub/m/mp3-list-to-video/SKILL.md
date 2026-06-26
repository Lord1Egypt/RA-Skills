---
name: mp3-list-to-video
description: 将指定文件夹下的所有 MP3 文件拼接成一个 MP4 视频文件，可生成黑色背景视频，也可基于已合并 MP4 生成带歌曲清单、当前歌曲高亮和右侧旋转黑胶唱片动效的菜单背景视频。菜单高亮默认使用智能分段渲染：并行生成关键帧、每首歌开头高帧密度、其余静态区间单帧拉长，避免整段 30fps 慢速重渲染；黑胶唱片作为独立动态层持续旋转，让整体画面不再完全静态。适用于：播放列表合并、批量歌曲拼接、MP3转视频、播放列表转视频、歌曲菜单高亮、黑胶唱片动效、音乐合集视频、分段视频渲染、并行生成菜单视频。当用户提到"拼接歌曲"、"合并MP3"、"播放列表转视频"、"歌曲列表背景"、"当前歌曲高亮"、"黑胶唱片"、"唱片转圈"、"画面太静态"、"生成太慢"、"多线程生成视频"、"batch mp3 to video"、"merge audio files into video"时使用此 skill。
---

# Skill: mp3-list-to-video

将文件夹下的所有 MP3 文件按自然顺序拼接成一个 MP4 视频文件。支持两种输出：

- 黑色背景视频：仅拼接音频，画面为黑色
- 菜单高亮视频：画面显示全部歌曲清单，并根据播放时间高亮当前歌曲，右侧默认叠加持续旋转的黑胶唱片

运行时会自动做依赖检查、输入顺序确认和输出媒体流校验。

## 前提条件

- **ffmpeg**: 必须已安装并可在 PATH 中访问
- **ffprobe**: 必须已安装并可在 PATH 中访问，用于合成后校验输出文件
- **Python 3**: 用于运行合并脚本
- **ffmpeg filters**: 生成菜单和黑胶动效时需要 FFmpeg 支持 `ass`、`rotate`、`overlay` 滤镜

检查依赖：

```bash
which ffmpeg
which ffprobe
python3 --version
ffmpeg -hide_banner -filters | rg ' ass '
ffmpeg -hide_banner -filters | rg ' rotate | overlay '
```

## 输入文件

默认从工作区根目录的 `playlist/` 目录读取所有 `.mp3` 文件，按自然文件名排序后拼接。自然排序会让 `10.xxx.mp3` 排在 `9.xxx.mp3` 后面，而不是排在 `2.xxx.mp3` 前面。

```
playlist/
├── 1.朵.mp3
├── 2.感官先生.mp3
├── 3.I Want It That Way.mp3
└── ...
```

## 输出文件

默认输出到工作区根目录：`playlist_output.mp4`

- 视频格式：MP4 (H.264)
- 分辨率：1920x1080
- 帧率：30fps
- 音频：AAC 44.1kHz stereo
- 视频流：黑色画面（无实际视频内容）

生成菜单高亮视频时，默认输出：

- 最终视频：`playlist_menu_output.mp4`
- 菜单背景视频：`output/playlist_menu_background.mp4`
- 菜单字幕层：`output/playlist_menu.ass`
- 歌曲时间轴：`output/playlist_menu_timeline.json`
- 预览抽帧：`output/playlist_menu_preview_*.png`
- 智能渲染帧：`output/playlist_menu_frames/frame_*.png`
- 智能渲染计划：`output/playlist_menu_frame_plan.json`
- 黑胶唱片 PNG：`output/playlist_vinyl.png`
- 菜单加动效视频：`output/playlist_menu_visual.mp4`

## 使用方法

### 快速开始

生成黑色背景的合并视频：

脚本已包含在 skill 的 `scripts/` 目录下，直接运行：

```bash
python3 scripts/merge_playlist.py
```

在当前工作区直接调用本 skill 中的脚本时：

```bash
python3 .opencode/skill/mp3-list-to-video/scripts/merge_playlist.py
```

基于已生成的 `playlist_output.mp4` 生成带歌曲清单和当前歌曲高亮的版本：

```bash
python3 .opencode/skill/mp3-list-to-video/scripts/add_playlist_menu.py
```

上面的命令默认使用优化后的 `smart` 模式。除非用户明确要求逐帧完整渲染，否则不要使用 `--render-mode full`。

### 自定义配置

脚本支持命令行参数，优先使用参数而不是手改脚本：

```bash
python3 scripts/merge_playlist.py \
  --playlist-dir playlist \
  --output playlist_output.mp4 \
  --temp-dir output
```

可选参数：

- `--playlist-dir`: MP3 输入目录
- `--output`: MP4 输出文件
- `--temp-dir`: 临时文件目录，会写入 `concat_list.txt`
- `--skip-verify`: 跳过合成后的 `ffprobe` 校验，仅在排查问题时使用

菜单高亮脚本支持：

```bash
python3 scripts/add_playlist_menu.py \
  --playlist-dir playlist \
  --source-video playlist_output.mp4 \
  --output playlist_menu_output.mp4 \
  --temp-dir output \
  --render-mode smart \
  --jobs 4 \
  --active-seconds 3 \
  --active-frames 60
```

可选参数：

- `--playlist-dir`: MP3 输入目录，用来计算每首歌时长和歌曲顺序
- `--source-video`: 已合并 MP4，用来复用最终音频
- `--output`: 带菜单高亮的最终 MP4
- `--temp-dir`: 中间文件目录，会写入 ASS 菜单层、背景视频和时间轴 JSON
- `--menu-video`: 单独指定菜单背景视频输出路径
- `--render-mode`: 菜单背景渲染模式，默认 `smart`；可选 `full`
- `--jobs`: `smart` 模式下并行生成菜单帧的任务数
- `--active-seconds`: 每首歌开头按高帧密度生成的秒数，默认 `3`
- `--active-frames`: 每首歌开头高帧密度段生成的帧数，默认 `60`
- `--disable-vinyl`: 禁用右侧旋转黑胶唱片动效
- `--vinyl-size`: 黑胶唱片尺寸，默认 `360`
- `--vinyl-x`: 黑胶唱片左上角 X 坐标，默认 `1480`
- `--vinyl-y`: 黑胶唱片左上角 Y 坐标，默认 `370`
- `--vinyl-rotation-seconds`: 黑胶唱片转一圈所需秒数，默认 `4`
- `--preview-times`: 逗号分隔的抽帧检查时间，例如 `00:00:10,00:05:00,00:34:10`
- `--skip-previews`: 跳过合成后的预览帧抽取
- `--preview-only`: 不重新生成视频，只对已有输出抽取预览帧

只复查已有菜单视频的画面时：

```bash
python3 scripts/add_playlist_menu.py \
  --output playlist_menu_output.mp4 \
  --preview-only \
  --preview-times 00:00:10,00:05:00,00:34:10
```

## 自动检查机制

运行脚本时会自动执行以下检查：

1. **依赖检查**: 确认 `ffmpeg`、`ffprobe` 和 Python 可用，并打印实际路径/版本
2. **输入检查**: 确认 playlist 目录存在，且至少包含一个 `.mp3` 文件
3. **顺序检查**: 打印最终合并顺序，便于确认 `1, 2, ..., 10` 是否正确
4. **输出文件检查**: 确认 MP4 文件存在且大小大于 0
5. **媒体流检查**: 使用 `ffprobe` 确认输出包含 H.264 视频流和 AAC 音频流
6. **规格检查**: 确认视频为 `1920x1080`，音频为 `44100Hz` 双声道
7. **时长检查**: 确认输出时长大于 0，并打印可读时长

菜单高亮脚本还会额外检查：

- `source-video` 是否存在
- FFmpeg 是否支持 `ass`、`rotate`、`overlay` 滤镜
- 每首 MP3 的真实时长
- 每首歌的开始/结束时间，最后一首会对齐 `source-video` 的总时长，避免封装误差导致结尾空白
- 合成后自动抽取预览帧，默认覆盖首歌、第二首相邻两秒和最后一首；相邻帧用于验证黑胶持续旋转
- 计算预览帧 MD5，确认不同时间点的画面不是完全相同，避免高亮没有随时间变化
- `smart` 模式会写出帧计划 JSON，记录 active/static 帧数量和每帧持续时间
- 默认生成 `playlist_vinyl.png` 并叠加旋转动效；最终视频即使当前歌曲不切换，右侧黑胶也会持续运动

合成完成后应看到类似输出：

```text
输出校验通过:
  - 文件大小: 39.2MB
  - 时长: 37:35 (2254.633s)
  - 视频流: h264 1920x1080
  - 音频流: aac 44100Hz 2ch
```

## 实现原理

### 黑色背景合并

1. **扫描 MP3 文件**: 使用 `pathlib` 扫描 `playlist/` 目录，按自然文件名排序
2. **生成 concat 列表**: 创建 FFmpeg concat 格式的文件列表
3. **实时生成黑色视频**: 使用 FFmpeg lavfi 的 color 滤镜实时生成黑色视频流（避免预生成大文件）
4. **拼接音频**: 使用 FFmpeg concat 协议拼接所有 MP3 文件
5. **合并音视频**: 将黑色视频流与拼接后的音频合并为最终 MP4
6. **校验输出**: 使用 `ffprobe` 校验文件大小、时长、视频流和音频流

核心 FFmpeg 命令：

```bash
ffmpeg -y \
  -f concat -safe 0 -i concat_list.txt \
  -f lavfi -i color=black:size=1920x1080:rate=30 \
  -c:v libx264 -preset ultrafast -pix_fmt yuv420p \
  -c:a aac -shortest \
  output.mp4
```

### 菜单高亮背景

1. **读取歌曲时长**: 使用 `ffprobe` 获取每个 MP3 的真实时长
2. **生成时间轴**: 计算每首歌的开始时间和结束时间，例如 `00:00 - 04:45`
3. **生成 ASS 菜单层**: 写入所有歌曲清单，并为每首歌创建只在对应时间段显示的高亮行
4. **生成菜单背景视频**:
   - `smart` 模式：只渲染必要 PNG 帧。每首歌开头 `active-seconds` 内生成 `active-frames` 帧，其余静态段只生成 1 帧并用 concat `duration` 拉长；帧生成会按 `--jobs` 并行执行
   - `full` 模式：回退到整段 30fps 渲染，速度较慢但实现直接
5. **生成黑胶动效层**: 脚本用内置 PNG 写入逻辑生成透明背景黑胶唱片，不依赖 Pillow 或外部素材
6. **叠加旋转黑胶**: 使用 FFmpeg `rotate + overlay` 将黑胶放到菜单右侧，并按 `--vinyl-rotation-seconds` 持续转动
7. **融合原音频**: 将最终视觉视频与 `playlist_output.mp4` 的音频流合并
8. **校验输出**: 确认最终视频包含视频流、音频流、时长和分辨率
9. **抽帧复查**: 从关键时间点抽取 PNG 帧，确认菜单可见且高亮随时间变化

`full` 模式核心 FFmpeg 命令：

```bash
ffmpeg -y \
  -f lavfi -i color=c=0x111214:size=1920x1080:rate=30:duration=2255.2 \
  -vf "ass=filename='output/playlist_menu.ass'" \
  -an -c:v libx264 -preset ultrafast -pix_fmt yuv420p \
  output/playlist_menu_background.mp4

ffmpeg -y \
  -i output/playlist_menu_background.mp4 \
  -i playlist_output.mp4 \
  -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a copy -shortest \
  playlist_menu_output.mp4
```

`smart` 模式的核心思路：

```bash
# 对每个需要的时间点生成一张菜单帧；通过 setpts 让 ASS 按全局时间渲染对应高亮
ffmpeg -y -loglevel error \
  -f lavfi -i color=c=0x111214:size=1920x1080:rate=1:duration=1 \
  -vf "setpts=PTS+300/TB,ass=filename='output/playlist_menu.ass',setpts=PTS-STARTPTS" \
  -frames:v 1 -update 1 output/playlist_menu_frames/frame_00100.png

# 使用 concat duration 拉长静态帧，再统一输出 30fps 标准 MP4
ffmpeg -y \
  -f concat -safe 0 -i output/playlist_menu_frames.txt \
  -vf "fps=30,format=yuv420p" \
  -an -c:v libx264 -preset ultrafast -pix_fmt yuv420p \
  output/playlist_menu_background.mp4

# 黑胶动效层叠加
ffmpeg -y \
  -i output/playlist_menu_background.mp4 \
  -loop 1 -framerate 30 -i output/playlist_vinyl.png \
  -filter_complex "[1:v]format=rgba,rotate='2*PI*t/4':ow=iw:oh=ih:c=none[vinyl];[0:v][vinyl]overlay=1480:370,fps=30,format=yuv420p[v]" \
  -map "[v]" -an -c:v libx264 -preset ultrafast \
  output/playlist_menu_visual.mp4
```

抽帧复查命令：

```bash
ffmpeg -y -loglevel error \
  -ss 00:05:00 \
  -i playlist_menu_output.mp4 \
  -frames:v 1 -update 1 \
  output/playlist_menu_preview_0500.png
```

## 注意事项

### 1. 文件排序

默认按自然排序（如 `1.mp3`, `2.mp3`, `10.mp3`），适合带数字前缀的播放列表。脚本中的排序逻辑：

```python
import re
files.sort(key=natural_key)
```

### 2. FFmpeg  concat 协议

使用 `-f concat -safe 0` 格式拼接音频文件，要求：
- 所有 MP3 文件编码参数一致（采样率、声道数）
- 文件列表使用绝对路径避免路径问题

### 3. 性能优化

- 使用 `-preset ultrafast` 加速视频编码（牺牲少量压缩率）
- 黑色视频通过 lavfi 实时生成，无需预生成临时文件
- 音频统一转为 AAC，提升 MP4 兼容性
- 菜单高亮视频默认使用 `smart` 模式，避免整段 30fps 重渲染
- `smart` 模式下，长静态区间只生成 1 帧，通过 concat `duration` 保持时长
- 黑胶唱片动效在菜单背景完成后单独叠加，因此不会被 smart 模式的静态帧优化冻结
- `--jobs` 控制并行生成帧的 ffmpeg 进程数；机器负载过高时调低，CPU 空闲时可调高
- 如果用户明确需要所有时间点逐帧渲染，使用 `--render-mode full`

推荐默认策略：

- 不需要动画时，保留默认 `--active-seconds 3 --active-frames 60`
- 如果只想极速生成静态菜单，可使用 `--active-seconds 0 --active-frames 1`
- 如果高亮切换需要更细腻，可提高 `--active-frames`
- 如果机器发热或并行进程太多，可降低 `--jobs`

### 4. 手动复查命令

如果需要在脚本外手动复查黑色背景合并输出，使用：

```bash
ls -lh playlist_output.mp4 output/concat_list.txt
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height,sample_rate,channels \
  -of default=noprint_wrappers=1 \
  playlist_output.mp4
sed -n '1,20p' output/concat_list.txt
```

菜单高亮视频复查重点：

```bash
ls -lh playlist_menu_output.mp4 output/playlist_menu_background.mp4 output/playlist_menu.ass output/playlist_menu_timeline.json
ls -lh output/playlist_menu_frame_plan.json output/playlist_menu_frames.txt output/playlist_vinyl.png output/playlist_menu_visual.mp4
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height,sample_rate,channels \
  -of default=noprint_wrappers=1 \
  playlist_menu_output.mp4
python3 scripts/add_playlist_menu.py --preview-only --preview-times 00:00:10,00:05:00,00:34:10
```

验收标准：

- `playlist_menu_output.mp4` 同时包含视频流和音频流
- 视频分辨率为 `1920x1080`
- 时间轴 JSON 中每首歌有 `start_text` 和 `end_text`
- `smart` 模式下，帧计划 JSON 中应包含 active/static 帧数量
- 帧计划中的 `duration_sum` 应接近 `total_duration`
- 预览帧文件存在，且多个时间点的 MD5 不完全相同
- 打开一个中间时间点预览帧，当前歌曲行应高亮，时间列和歌名列之间应有清楚间距
- 默认预览会抽取第二首歌内相邻 1 秒的两帧，MD5 应不同，以确认黑胶唱片持续旋转

### 5. 扩展方向

此 skill 为第一阶段实现（仅拼接音频）。后续可扩展：
- 添加专辑封面作为背景画面
- 添加歌曲名、时间轴等文字叠加
- 生成歌词卡拉OK动画视频（参考 song-movie-generater skill）
- 支持更多音频格式（m4a, flac 等）

菜单高亮视频当前使用静态列表和当前歌曲高亮。可继续扩展：

- 根据专辑封面生成背景图
- 添加播放进度条
- 当前行添加淡入淡出或指示图标
- 歌曲较多时分页显示
- 将黑胶中心标签替换为专辑封面

## 故障排查

### ffmpeg: command not found

安装 ffmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 输出视频时长为 0

脚本会自动用 `ffprobe` 检查时长。如果失败：

- 检查 `output/concat_list.txt` 是否包含所有 MP3
- 检查 FFmpeg 命令是否包含 `-shortest` 参数
- 单独用 `ffprobe playlist_output.mp4` 查看输出媒体信息

### 文件顺序不正确

检查脚本打印的“合并顺序”。脚本使用自然排序，推荐输入文件使用数字前缀，例如 `1.xxx.mp3`、`2.xxx.mp3`、`10.xxx.mp3`。

### 输出校验失败

脚本会直接列出失败项，例如缺少视频流、缺少音频流、时长为 0、分辨率不符或采样率不符。先查看脚本打印的错误，再用“手动复查命令”确认具体媒体流信息。

### 菜单文字无法显示中文或日文

菜单脚本默认使用 macOS 上常见的 `Hiragino Sans GB`。如果目标机器没有该字体，修改 `scripts/add_playlist_menu.py` 中的 `FONT_NAME`，或安装支持中日文的字体。修改字体后运行 `--preview-only` 抽帧确认中文、日文和英文都正常显示。

### 菜单文字太挤或重叠

菜单脚本中的布局常量控制文字位置：

- `NUMBER_X`: 序号列
- `TIME_X`: 时间列
- `TITLE_X`: 歌名列
- `ROW_START_Y`: 第一行纵向位置
- `ROW_HEIGHT`: 行高

如果时间和歌名贴得太近，优先调大 `TITLE_X`。调整后先运行：

```bash
python3 scripts/add_playlist_menu.py --preview-only --preview-times 00:05:00
```

如果已改动 ASS 生成逻辑且需要完整重渲染，再运行完整菜单生成命令。

### 智能渲染速度或质量不合适

默认参数针对“每首歌开头 3 秒生成 60 帧，其余静态段 1 帧”的场景：

```bash
python3 scripts/add_playlist_menu.py \
  --render-mode smart \
  --jobs 4 \
  --active-seconds 3 \
  --active-frames 60
```

调整建议：

- 生成太慢：降低 `--active-frames` 或 `--jobs`
- 开头动画/高亮过渡不够细：提高 `--active-frames`
- 机器 CPU 足够：提高 `--jobs`
- 怀疑 concat 或时间轴问题：临时使用 `--render-mode full` 回退整段渲染

### 黑胶唱片位置或速度不合适

默认黑胶参数：

```bash
python3 scripts/add_playlist_menu.py \
  --vinyl-size 360 \
  --vinyl-x 1480 \
  --vinyl-y 370 \
  --vinyl-rotation-seconds 4
```

调整建议：

- 唱片挡住菜单文字：调大 `--vinyl-x` 或调小 `--vinyl-size`
- 唱片太靠右或超出画面：调小 `--vinyl-x`
- 转得太快：调大 `--vinyl-rotation-seconds`
- 转得太慢：调小 `--vinyl-rotation-seconds`
- 不需要动效：使用 `--disable-vinyl`

### ffmpeg 不支持 ass 滤镜

菜单高亮视频依赖 `ass` 滤镜。检查：

```bash
ffmpeg -hide_banner -filters | rg ' ass '
```

如果没有输出，需要安装带 `libass` 的 FFmpeg。

## 相关 Skills

- **song-movie-generater**: 生成带歌词卡拉OK动画的视频，功能更丰富
- **gequbao-downloader**: 从歌曲宝下载 MP3，配合此 skill 可实现"下载+拼接"完整流程
