---
name: "history-persona-video"
description: "历史人物AI复原竖版短视频制作全流程（素材/配音/卡片/合成/验证）"
---

# history-persona-video — 历史人物AI复原短视频

把历史人物从画像里"拉到现实中"的竖版短视频完整制作流程。已用《AI还原曹操》实测验证（v2 成品：56s / 1080×1920 / 7.8MB）。

## 核心思路

- 不做学术考据，先视觉冲击，再简短史料增加可信度
- 固定时间轴模板（45-60s）：强钩子 → 制造期待 → 过程展示 → 最终揭晓 → 互动结尾
- 用 AI 生图 + TTS 磁性配音 + 低沉史诗 BGM + 大气中文字体（方正粗黑宋简体）
- 每次交付必须加免责声明："基于史料、时代服饰与AI视觉推演的艺术化还原，不代表真实照片"

## 前置环境

- ffmpeg（含 ffprobe）可用
- Python 3 + Pillow
- RunningHub 技能已装（`skills/runninghub/scripts/runninghub.py`），API Key 已配置
- 大气字体：`C:\Windows\Fonts\方正粗黑宋简体.ttf`（复制到 workspace 为 `font_heisong.ttf`，避免 drawtext 冒号转义问题）

## 第一步：素材准备

### 1. 史料与画像调研

用 web_search 收集：
- 正史外貌线索（如《三国志》《世说新语·容止》）→ 塑造可信度
- 传统画像（Wikimedia 公有领域，如《三才图会》）→ 古画像素材
- 时代服饰依据（《续汉书·舆服志》等）→ AI 生图关键词

下载古画像用 Wikimedia `Special:FilePath` URL：
```
https://commons.wikimedia.org/wiki/Special:FilePath/<文件名>?width=800
```

### 2. AI 生图（RunningHub 或 GPT Image 2）

按 9:16 竖版生成 4 张核心画面（1152×2048）：
| 素材 | 内容 | 提示词要点 |
|------|------|-----------|
| 最终还原像 | 人物半身肖像 | 约X岁、时代服饰、真实人像摄影、电影级光影、超写实、暗色背景、庄重 |
| 战乱/氛围图 | 时代背景 | 氛围、史诗感 |
| AI初稿过程图 | 草稿效果 | 未完成、素描感 |
| 诗意图 | 人物代表诗句意境 | 月下/饮酒/剪影等 |

生图命令（RunningHub）：
```bash
py skills/runninghub/scripts/runninghub.py --endpoint <text-to-image端点> --prompt "<提示词>" --param aspectRatio=9:16 -o "media/<人物>/<name>.png"
```

### 3. TTS 配音（磁性男声）

- 端点：`rhart-audio/text-to-audio/speech-2.8-hd`
- **磁性男声：`voice_id=male-qn-qingse`**（低沉有磁性；备选 audiobook_male_2 沉稳）
- 语速：`speed=1.05`（纪录片节奏，中等偏快）
- 成本参考：全文约 ¥0.025，5s 测试 ¥0.002

```bash
py skills/runninghub/scripts/runninghub.py --endpoint rhart-audio/text-to-audio/speech-2.8-hd --prompt "<全文文案>" --param voice_id=male-qn-qingse --param speed=1.05 --param enable_base64_output=false --param english_normalization=false -o "<out>.mp3"
```

⚠️ PowerShell 传长中文文案易出错 → 先把文案写入 txt（UTF-8），用 `Get-Content -Raw -Encoding UTF8` 读入变量再传。

### 4. BGM（低沉史诗感）

- 端点：`rhart-audio/text-to-audio/music-2.5`
- 目标：60s 左右低沉史诗配乐（成本约 ¥0.12）
- 混音时压到配音的 16% 音量

## 第二步：卡片制作（PIL + 大气字体）

用 Python PIL 生成 3 张 1080×1920 卡片：

| 卡片 | 用途 | 内容 |
|------|------|------|
| card_hook.png | 0-5.5s 钩子封面 | 黑底+模糊人物轮廓+大标题+关键词 |
| card_keywords.png | 8-13s 关键词卡 | 史料/五官/须发/冠服/气质 线索 |
| card_compare.png | 结尾对比图 | 古画 vs AI 左右分屏+互动文字 |

关键实现：
- 主字体 `font_heisong.ttf`（方正粗黑宋简体，大气），点缀用 `simkai.ttf` 楷体
- 主标题 100-110px，正文 40-60px，副标题楷体
- 钩子卡背景：最终还原像 GaussianBlur(30) + 压暗（Brightness 0.28）叠在近黑底上
- 对比卡：`ImageOps.fit` 左右各半（古画 | AI还原）

## 第三步：视频合成（ffmpeg）

### 时间轴模板（按配音时长动态对齐）

以曹操版实测切点（配音 56.27s）为基准：
```
0-5.5s   S1 钩子（card_hook 缓慢推近 zoompan）
5.5-8s   S2 古画像快闪（两张各1.25s，轻微 zoom）
8-13s    S3 关键词卡
13-20s   S4 AI初稿缓慢放大
20-27s   S5 五官修正（初稿→还原像 xfade 交叉溶解 1.5s）
27-40s   S6 最终揭晓（还原像推近 + 大气字体字幕）
40-50s   S7 诗意图（对酒当歌类 + 大字字幕）
50-56.3s S8 互动结尾（对比图 + "英雄，还是枭雄？下一期想看X还是Y？"）
```
若新配音时长不同，按比例缩放各段，保证总时长=配音时长。

### 分段生成要点

- 统一 `-r 30 -c:v libx264 -pix_fmt yuv420p -an`
- 推近动效：`zoompan=z='min(zoom+0.0008,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=<帧数>:s=1080x1920:fps=30`
- **drawtext 字幕必须用相对路径字体 + cwd=workspace**（Windows 冒号转义坑：`C:` 会被当选项分隔符，方案=把字体复制到工作目录用 `font_heisong.ttf`）
- 多输入片段（S5 交叉溶解）用 `-filter_complex`，不能用 `-vf`

### 拼接与混音

```bash
# concat 拼接
ffmpeg -y -v error -f concat -safe 0 -i concat_list.txt -c copy video_silent.mp4
# 混音：配音1.0 + BGM 0.16，normalize=0 + volume=2.0 提升响度
ffmpeg -y -v error -i video_silent.mp4 -i peiyin.mp3 -i bgm.mp3 \
  -filter_complex "[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo,volume=1.0[vo];[2:a]aformat=sample_fmts=fltp:channel_layouts=stereo,volume=0.16[bg];[vo][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,volume=2.0[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest video_final.mp4
```

## 第四步：质量验证（必做）

1. **ffprobe**：确认时长=配音时长、1080×1920、h264+aac
2. **关键帧亮度**（视觉模型不可用时用 PIL）：
   ```python
   ffmpeg -i video.mp4 -vf "fps=1/7" check_%02d.png
   # PIL ImageStat：钩子帧 mean低但 max=255（黑底白字），其余帧 mean>30 无黑屏
   ```
3. **音量**：`volumedetect` 确认 mean≈-20dB、max≈-0.5dB（无爆音）
4. 抽查文字是否渲染：钩子帧标题区 max=255 即白色大字已渲染

## 交付规范

- 输出 `video_<人物>_FINAL.mp4` 到 `media/<人物>/`
- 交付时附上：时长/分辨率/音色/字体/成本明细
- 固定结尾互动句式："你觉得更像英雄，还是枭雄？下一期想看X还是Y？"（按人物调整）
- 记住免责声明

## 成本参考（曹操版实测）

| 项目 | 成本 |
|------|------|
| 配音（全文磁性男声） | ¥0.025 |
| BGM（60s 史诗配乐） | ¥0.12 |
| 图片（4张 2K 竖版） | 约 ¥0.06 |
| TTS 音色测试 | ¥0.002/次 |
| 合计 | 约 ¥0.3/条 |

## 已验证参数速查

- 磁性男声：`male-qn-qingse`；沉稳有声书：`audiobook_male_2`
- 大气字体：方正粗黑宋简体（`font_heisong.ttf`）；楷体点缀：`simkai.ttf`
- TTS 端点：`rhart-audio/text-to-audio/speech-2.8-hd`
- BGM 端点：`rhart-audio/text-to-audio/music-2.5`
- 画质：1152×2048 生图 → 1080×1920 输出

## 脚本模板文件

本技能建议同目录维护：
- `scripts/make_cards.py` — 卡片生成（参数化：人物名、标题、关键词、古画/AI图路径）
- `scripts/make_video.py` — 分段+拼接+混音全流程（参数化：各段素材、配音、BGM、字幕文字）
