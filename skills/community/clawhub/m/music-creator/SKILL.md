---
name: music-creator
slug: music-creator
description: "AI 音乐创作全流程技能。根据主题和风格创作歌词，通过 MiniMax AI 生成音乐和封面图，Whisper ASR + V2 高精度对齐（纯 Python，无需 espeak-ng）精准校准歌词时序，生成标准 LRC 歌词文件和带歌词同步的播放页面并部署。触发词：创作歌曲、写首歌、生成音乐、AI 音乐、music creator、帮我写首歌、创作音乐、做个音乐。"
version: "2.1.0"
---

# Music Creator — AI 音乐创作技能

从主题到成品播放页面的一站式 AI 音乐创作流程。

## 初始化配置

**首次使用前必须完成以下配置。** Agent（即你）在首次接到音乐创作任务时，应主动引导用户完成配置。

---

### 🤖 Agent Prompt — 首次使用时对用户说的话

> 在你第一次使用音乐创作功能前，需要完成以下初始化配置：
>
> **1. MiniMax API 密钥**
> 我需要一个 MiniMax API Key 来生成歌词、音乐和封面图。请提供你的 API Key。
> 获取地址：https://platform.minimaxi.com
>
> **2. 创作人信息**
> 请告诉我以下信息，用于封面图署名和播放页展示：
> - 艺术家名 / 歌手名
> - 作词人（默认同上）
> - 作曲人（默认同上）
> - 演唱者（默认同上）
> - 制作人（默认同上）
>
> 其他依赖（whisper、ffmpeg、Pillow）我会自行检查并安装，不需要你操作。

用户提供 API Key 后，Agent 执行以下命令完成初始化：

```bash
# 安装 mmx CLI
npm install -g mmx-cli
# 登录 API Key
mmx auth login --api-key <用户提供的API_KEY>
# 验证
mmx text chat --model MiniMax-M2.7 --message "test" --output json
```

用户提供创作人信息后，Agent 在技能目录创建 `config.json`：

```json
{
  "artist": "<艺术家名>",
  "credits": {
    "lyrics": "<作词人>",
    "compose": "<作曲人>",
    "sing": "<演唱者>",
    "produce": "<制作人>"
  }
}
```

如果某个角色与艺术家不同，单独设置对应字段；相同则默认填艺术家名。

---

### 🔧 技术依赖（Agent 自行检查）

以下依赖 Agent 首次运行时自行检测，缺失则自动安装，无需用户参与：

| 依赖 | 检查命令 | 安装命令 |
|------|----------|----------|
| `mmx` CLI | `mmx text chat --help` | `npm install -g mmx-cli` |
| `whisper` | `whisper --help` | `pip install openai-whisper` |
| `aeneas` | `python3 -m aeneas.diagnostics` | `pip install 'numpy<2' && pip install aeneas --no-build-isolation` |
| `espeak-ng` | `espeak-ng --version` | `yum install -y espeak-ng espeak-ng-devel` |
| `ffprobe` | `ffprobe -version` | `apt install ffmpeg` |
| Pillow + 中文字体 | `python3 -c "from PIL import Image"` | `pip install Pillow` |

中文字体检查：`ls /usr/share/fonts/google-noto-cjk/NotoSansCJK-Black.ttc`

Aeneas 安装注意：
- aeneas 需要 `numpy<2`（它依赖已弃用的 `numpy.distutils`）
- aeneas 编译时链接 `libespeak`，但系统提供的是 `libespeak-ng`，需要创建符号链接：`ln -sf /usr/lib64/libespeak-ng.so /usr/lib64/libespeak.so`
- 安装命令：`pip install 'numpy<2' && ln -sf /usr/lib64/libespeak-ng.so /usr/lib64/libespeak.so && pip install aeneas --no-build-isolation`
- 验证：`python3 -m aeneas.diagnostics`

## 依赖

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| `mmx` CLI | 歌词创作、音乐生成、封面图生成 | `mmx text chat --help` |
| `whisper` | ASR 歌词时序识别（Aeneas fallback） | `whisper --help` |
| `aeneas` | 歌词强制对齐（精确时间戳） | `python3 -m aeneas.diagnostics` |
| `espeak-ng` | Aeneas 依赖的 TTS 引擎 | `espeak-ng --version` |
| `ffprobe` | 获取音频时长 | `ffprobe -version` |
| Pillow (PIL) | 封面图文字合成 | `python3 -c "from PIL import Image"` |
| report-expert | 播放页面模板 + 部署 | 技能目录 `music_player_builder.py` |

## 文件目录结构

每首歌创建独立目录，所有相关文件放在一起：

```
claw/music/{slug}/
├── index.html          # 播放页面（从模板复制，无需修改）
├── song.json            # 歌曲元信息（标题、副标题、创作人）
├── song.lrc             # 标准 LRC 歌词文件（Aeneas 校准输出）
├── song.mp3             # 音乐文件
├── cover.jpg            # 封面图（Pillow 合成后）
├── lyrics.txt           # 纯文本歌词（无时间）
└── lyrics-timed.json    # 带时序的歌词 JSON（向后兼容保留）
```

- `slug`：歌曲名的小写英文/拼音 slug（如 `nanchangcheng-love`）
- 部署方式：通过 report-expert 技能的 deploy 命令部署（见 Step 7）
- **index.html 是模板的副本，不需要修改**，播放页从 `song.json` 和 `lyrics-timed.json` 动态加载所有信息
- 所有资源通过**相对路径**引用，不使用 base64
- 播放页优先加载 `song.lrc`（标准 LRC），fallback 到 `lyrics-timed.json`，再 fallback 到 `lyrics.txt`

## 完整工作流

按以下 7 个步骤顺序执行：

### Step 1：确认主题与风格

读取 `config.json` 获取创作人信息。

与用户确认以下信息：

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| **主题** | ✅ | 歌曲主题/歌名 | "我爱小微"、"春天的故事" |
| **风格** | ✅ | 音乐风格 | "甜蜜浪漫流行"、"摇滚"、"民谣" |
| **参考信息** | ❌ | 参考图片或文本 | 用户提供的灵感素材 |

如果用户已提供主题和风格，直接进入下一步。如果信息不完整，询问补充。

生成 `slug`（用于目录名）：将歌名转小写，用连字符连接。

### Step 2：收集参考信息（可选）

如果用户提供了：
- **参考图片**：描述图片内容，提取可用于歌词创作的意象和情感元素
- **参考文本**：提炼关键信息、情感基调、故事线索

将参考信息整理为歌词创作的参考摘要（不直接展示给用户）。

### Step 3：创作歌词

使用 MiniMax 文本模型生成歌词：

```bash
mmx text chat --model MiniMax-M2.7 --message "PROMPT" --output json
```

**Prompt 模板：**
```
请为一首{风格}风格的中文歌曲写歌词，主题是《{主题}》。
要求：
1. 歌曲结构标签：[Intro] [Verse 1] [Pre Chorus] [Chorus] [Verse 2] [Pre Chorus] [Chorus] [Bridge] [Chorus] [Outro]
2. 每段 4-6 行，总时长控制在 2-4 分钟
3. {如果有参考信息：参考以下素材融入歌词：{参考摘要}}
4. 歌词要有画面感和故事性，朗朗上口
5. **尽可能押韵**：同一段落内相邻句子尽量押韵（如 AABB、ABAB 或 AAAA），Chorus 部分尤须押韵工整，这是歌曲朗朗上口的关键。优先使用常见韵脚（如 ao/iao、an/ian、eng/ing、ou/iu 等），韵脚要自然不生硬
6. 只输出歌词，不要其他内容
```

将歌词保存到歌曲目录：`{MUSIC_DIR}/lyrics.txt`

### Step 4：生成音乐 + 封面图（并行）

**音乐生成：**
```bash
mmx music generate \
  --prompt "{风格}风格的中文歌曲，主题{主题}" \
  --lyrics-file {MUSIC_DIR}/lyrics.txt \
  --out {MUSIC_DIR}/song.mp3
```

**封面图生成（无文字纯画面）：**
```bash
mmx image generate \
  --prompt "A beautiful album cover art, absolutely no text no words no letters, {风格对应画面的英文描述}, artistic watercolor style, 1:1 square format" \
  --out {MUSIC_DIR}/cover-raw.jpg
```

两者并行执行，节省时间。

**封面图文字合成：**
```bash
python3 scripts/make_cover.py \
  --input {MUSIC_DIR}/cover-raw.jpg \
  --title "{主题}" \
  --artist "{config.artist}" \
  --output {MUSIC_DIR}/cover.jpg
```

> **重要**：AI 图像生成对中文文字渲染会乱码，必须用 Pillow 叠加文字。

### Step 5：ASR + Aeneas 歌词校准

使用 `calibrate_lyrics.py` 脚本完成 Whisper ASR + Aeneas 强制对齐，输出标准 LRC 歌词文件：

```bash
python3 scripts/calibrate_lyrics.py \
  --mp3 {MUSIC_DIR}/song.mp3 \
  --lyrics {MUSIC_DIR}/lyrics.txt \
  --title "{主题}" \
  --artist "{config.artist}" \
  --output {MUSIC_DIR}/song.lrc
```

**工作流程：**
1. **Whisper ASR**：对 mp3 做 ASR 识别，获取 segment 级别时间戳（作为 fallback）
2. **Aeneas 强制对齐**：将歌词文本与 mp3 做全文强制对齐，获取每行歌词的精确 begin 时间
3. **时间戳合并**：aeneas 时间优先，aeneas 异常/缺失时用 whisper fallback，都没有则线性插值
4. **生成 LRC**：输出标准 `[mm:ss.xx]歌词` 格式，Section 标签格式为 `[mm:ss.xx][Section]`

**注意**：Aeneas 全文对齐理论上能覆盖重复段落，但如果结果不理想，可检查 `/tmp/calibrate-{slug}/` 下的中间文件手动调整。

### Step 6：生成播放页面

使用 report-expert 技能中的 `music_player_builder.py` 模板（需安装 report-expert 技能）：

```bash
python3 {REPORT_EXPERT_DIR}/music_player_builder.py \
  --mp3 {MUSIC_DIR}/song.mp3 \
  --cover {MUSIC_DIR}/cover.jpg \
  --title "{主题}" \
  --subtitle "{副标题}" \
  --lrc {MUSIC_DIR}/song.lrc \
  --output {MUSIC_DIR}/index.html \
  --download-filename "{主题}.mp3"
```

> `{REPORT_EXPERT_DIR}` 为 report-expert 技能的安装目录，通常是 `~/.openclaw/workspace/skills/report-expert/`。

**文件引用方式**：模板生成的 HTML 通过相对路径 `song.mp3` 和 `cover.jpg` 引用同目录文件，不使用 base64 嵌入。

### Step 7：部署（需安装 report-expert 技能）

将歌曲的所有文件（播放页 + 静态资源）复制到 report-expert 的 `dist/` 工作目录，然后通过 `deploy.py` 注册索引并 `sync_to_deploy()` 统一推送。

```bash
REPORT_DIR="{REPORT_EXPERT_DIR}/dist/music/{slug}"
mkdir -p "$REPORT_DIR"

# 复制所有歌曲文件到 report-expert dist/
cp {MUSIC_DIR}/index.html "$REPORT_DIR/"
cp {MUSIC_DIR}/song.mp3 "$REPORT_DIR/"
cp {MUSIC_DIR}/cover.jpg "$REPORT_DIR/"
cp {MUSIC_DIR}/song.json "$REPORT_DIR/"
cp {MUSIC_DIR}/song.lrc "$REPORT_DIR/"
cp {MUSIC_DIR}/lyrics.txt "$REPORT_DIR/"
cp {MUSIC_DIR}/lyrics-timed.json "$REPORT_DIR/"  # 向后兼容保留

# 注册到索引并同步部署
cd {REPORT_EXPERT_DIR}
python3 deploy.py add "music/{slug}/index.html" \
  --title "{主题} - 原创音乐" \
  --desc "AI 创作{风格}歌曲：{主题}" \
  --category other

python3 -c "from lib.config import sync_to_deploy; sync_to_deploy()"
```

> 部署的站点地址和 URL 由 report-expert 技能的配置（TOOLS.md）决定，本技能不耦合具体站点信息。
>
> `sync_to_deploy()` 会将 `dist/` 下所有文件（包括 mp3、jpg 等静态资源）同步到部署目录，无需单独处理。

## 输出

完成后的交付物：
1. **播放页面**：由 report-expert 部署，具体 URL 取决于 report-expert 配置
2. **MP3 文件**：`{MUSIC_DIR}/song.mp3`（可单独发送）
3. **封面图**：`{MUSIC_DIR}/cover.jpg`（可单独发送）

## 封面图画面风格映射

| 音乐风格 | 画面描述（英文 Prompt） |
|----------|------------------------|
| 流行/甜蜜 | dreamy romantic scene, pink purple gradient, cherry blossom petals, couple silhouette |
| 摇滚 | electric energy, dark stage, neon lights, guitar silhouette, dramatic lighting |
| 民谣 | peaceful countryside, sunset, acoustic guitar, warm golden light |
| 古风 | Chinese ink painting style, mountains mist, bamboo, plum blossom, moon |
| 电子/DJ | futuristic neon city, abstract light trails, geometric shapes, cyberpunk |
| 嘻哈 | urban street scene, graffiti wall, boombox, bold colors |
| R&B | smooth jazz club, saxophone, warm candlelight, velvet curtains |
| 儿歌/欢快 | colorful playground, balloons, sunshine, cartoon animals, bright colors |
