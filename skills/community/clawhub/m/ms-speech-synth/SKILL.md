---
name: ms-speech-synth
description: 将长文本（最多数千字）使用微软 Edge TTS 分段合成 MP3/WAV 音频。支持单文件和文件夹批量模式，自动降速防限流（可配置 20-30次/分钟），自动清洗 Markdown 格式转为自然朗读，并可选添加背景音乐（片头/片尾纯背景音）。
---

# MS Speech Synth - 微软 TTS 分段合成技能

## 核心能力

将任意长度的中文文本（数千字以上）转换为 MP3 音频，使用**微软 Edge TTS** 音色，通过**分段合成 + PCM 拼接**实现无字符限制语音生成，支持单文件与文件夹批量处理。

可选背景音乐能力：
- 不传 `--bgm`：仅输出人声音频
- 传入 `--bgm`：
  - 片头：仅背景音乐（无人声）
  - 正文：完整人声 + 低音量背景音乐铺底
  - 片尾：仅背景音乐（无人声）

## 工作流程

```text
长文本 → 按句子分chunk（每chunk ≤1200字）
       → edge-tts 每段生成 MP3（每段之间延迟防止超限）
       → miniaudio 解码 MP3 → PCM bytes
       → 拼接所有 PCM
       → 写入 WAV 文件
       → （可选）ffmpeg 添加 BGM 并混音
       → 输出最终 MP3
```

## 工具依赖

| 工具 | 安装 | 用途 |
|------|------|------|
| `edge-tts` | `pip3 install edge-tts` | 微软 TTS 引擎 |
| `miniaudio` | `pip3 install miniaudio` | MP3 解码为 PCM |
| `ffmpeg` | `curl -L .../ffmpeg.zip -o /tmp/ffmpeg.zip && unzip /tmp/ffmpeg.zip -d /tmp/ffmpeg_bin` | WAV 转 MP3、BGM 混音 |

## 速率限制（Rate Limit）

> ⚠️ Edge TTS 是微软必应语音服务的免费接口，**非官方 API**，无正式 SLA。

**限制阈值：**
- 单次请求字符上限：约 **1000–1500 字符**（超出部分可能被服务器静默截断）
- 连续调用：建议不超过 **20–30 次/分钟**
- 超过限制可能触发 `ConnectionResetError`，需等待 30–60 秒恢复

**速率控制参数 `--rate`（每 TTS 请求间延迟）：**

| `--rate` 值 | 实际速率 | 适用场景 |
|-------------|----------|----------|
| `1.5` | 40次/分钟 | 较快，接近上限 |
| `2.0`（默认）| 30次/分钟 | 稳定安全（默认） |
| `3.0` | 20次/分钟 | 保守模式 |

**批量文件夹模式额外策略：** 每文件之间再等待 `--delay` 秒（默认3秒）。

## 使用方式

### 单文件模式

```bash
python3 ~/.openclaw/workspace/skills/ms-speech-synth/scripts/ms_tts_chunked_bgm.py \
  --input "/path/to/input.txt" \
  --output "/path/to/output" \
  --voice "zh-CN-XiaoxiaoNeural"

# 从 Markdown 文件（自动清洗 #标题 **加粗** 等格式）
python3 ~/.openclaw/workspace/skills/ms-speech-synth/scripts/ms_tts_chunked_bgm.py \
  --input "/path/to/notes.md" \
  --output "/path/to/output"
```

### 文件夹批量模式

处理整个文件夹下所有 `.txt` 和 `.md` 文件，自动降速防限流：

```bash
python3 ~/.openclaw/workspace/skills/ms-speech-synth/scripts/ms_tts_chunked_bgm.py \
  --input "/path/to/folder/" \
  --output "/path/to/output_folder/" \
  --delay 3 \
  --rate 2.0
```

### 带背景音乐模式

```bash
python3 ~/.openclaw/workspace/skills/ms-speech-synth/scripts/ms_tts_chunked_bgm.py \
  --input "/path/to/input.txt" \
  --output "/path/to/output" \
  --bgm "/path/to/bgm.mp3" \
  --bgm-intro 5 \
  --bgm-outro 5 \
  --bgm-mid-volume 0.12 \
  --bgm-full-volume 0.8
```

## Python 模块导入

```python
from scripts.ms_tts_chunked_bgm import synthesize_text, synthesize_file, synthesize_dir

# 单文件
result = synthesize_file(
    "/path/to/input.txt", "/path/to/output",
    voice="zh-CN-XiaoxiaoNeural",
    rate_limit_delay=2.0,
    speed=1.0,
)

# 单文件 + BGM
result = synthesize_file(
    "/path/to/input.txt", "/path/to/output",
    bgm_path="/path/to/bgm.mp3",
    bgm_intro=5.0,
    bgm_outro=5.0,
    bgm_mid_volume=0.12,
    bgm_full_volume=0.8,
)

# 批量文件夹
results = synthesize_dir(
    input_dir="/path/to/folder/",
    output_dir="/path/to/output/",
    voice="zh-CN-XiaoxiaoNeural",
    delay=3.0,
    rate_limit_delay=2.0,
    speed=1.0,
)
```

## 关键参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--voice` | `zh-CN-XiaoxiaoNeural` | 微软中文女声（晓晓） |
| `--chunk` | `1200` | 每段最大字符数（建议 1000-1500） |
| `--delay` | `3.0` | 批量模式：每文件间延迟秒数 |
| `--rate` | `2.0` | 每 TTS 请求间延迟秒数（2s=30次/分钟，3s=20次/分钟） |
| `--speed` | `1.0` | 语速倍率（1.0=正常，0.8=稍慢，1.5=较快） |
| `--ffmpeg` | 自动查找 | FFmpeg 路径（转 MP3、BGM 混音） |
| `--bgm` | 空 | 可选背景音乐文件路径 |
| `--bgm-intro` | `5.0` | 片头纯背景音乐时长（秒） |
| `--bgm-outro` | `5.0` | 片尾纯背景音乐时长（秒） |
| `--bgm-mid-volume` | `0.12` | 正文阶段背景音乐铺底音量 |
| `--bgm-full-volume` | `0.8` | 片头/片尾峰值音量 |
| `--bgm-loop` | 始终开启 | 当前脚本默认循环背景音乐，长度不足时自动循环（暂无关闭开关） |

### 其他可用声音

```text
zh-CN-XiaoxiaoNeural   # 晓晓 - 推荐女声
zh-CN-YunxiNeural      # 云希 - 男声
zh-CN-YunyangNeural    # 云扬 - 新闻风格
zh-HK-HiuMaanNeural    # 香港粤语
zh-TW-HsiaoYuNeural    # 台湾女声
```

## Markdown 格式清洗

输入文件为 `.md` 时，自动将格式控制符转为自然朗读：

| 原始格式 | 转换效果 |
|----------|----------|
| `# 我是标题` | 读标题并在末尾加停顿（`……`） |
| `## 小标题` | 读标题并在末尾加停顿（`……`） |
| `### 本节标题` | 读标题并在末尾加停顿（`……`） |
| `- 要点` / `* 要点` | `第X点：xxx` |
| `> 引用` | `引用：xxx` |
| `**加粗**` | 保留文字（去格式符） |
| `` `代码` `` | `代码：xxx` |
| `[文字](url)` | 读链接文字 |

## 分段策略

三级保护机制，防截断设计：

1. **按句子边界拆分**：按 `。！？；，` 切句
2. **累积到 chunk_size**：组合成不超过 `chunk_size` 的 chunk
3. **超长句二次切分**：按 `顿号 → 逗号 → 空格` 顺序继续切分

**chunk_size 建议值：**
- 800 字：推荐默认值（更稳妥，优先避免漏读/吞字）
- 1000 字：平衡速度与稳健性
- 1200 字：可用但在复杂长句中风险更高

## 默认音量曲线（启用 BGM 时）

```text
0s                5s                     total-5s              total
|-----------------|----------------------|---------------------|
0 -> full         full -> mid            mid                   mid -> full -> 0
```

## 时长说明

- 不启用 `--bgm`：成品时长约等于人声时长。
- 启用 `--bgm`：成品总时长约等于 `片头 + 人声正文 + 片尾`。

## 注意事项

1. `edge-tts` 有速率限制，建议保持 20–30 次/分钟
2. 批量任务建议保持 `--delay 3` + `--rate 2.0` 默认组合
3. `chunk_size` 不建议超过 1500
4. 传 `--bgm` 时必须有可用 `ffmpeg`
5. 背景音乐长度不足时会自动循环（当前无关闭开关）
6. Markdown 输入会先清洗再朗读
