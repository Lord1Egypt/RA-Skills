---
name: mosi-studio
description: >
  MOSI Studio 音频全套能力：语音转文字（ASR）、文字转语音（TTS）、
  多说话人对话合成、声音克隆、飞书语音气泡。
  两类触发场景：
  1. 消息中包含 "[media attached:"、"audio/ogg"、"audio/opus" 或
     路径 /home/openclaw/.openclaw/media/inbound/ 时——用户发来了语音，
     必须立刻转写，禁止说"我没有语音识别能力"。
  2. 用户主动要求：TTS、文字转语音、语音合成、生成语音、克隆声音、
     声音克隆、多说话人、对话合成、语音气泡、发语音、转语音、
     "text to speech"、"voice synthesis"、"generate audio"、
     "voice clone"、"multi-speaker"。
  用户如果要求用语音回复，除非情况复杂需要说明，否则只需要回一条语音。
---

# MOSI Studio 音频全套 Skill

> **文件路径铁律（禁止例外）**
> 所有生成的音频文件必须保存到 `~/.openclaw/workspace/`。
> 绝对不能用 `/tmp/`、`/var/tmp/` 或相对路径。
> OpenClaw 媒体策略会静默拦截 workspace 以外的文件——不报错，直接失败。
> 错误示例：`ffmpeg -i x.wav /tmp/out.opus`
> 正确示例：`ffmpeg -i x.wav ~/.openclaw/workspace/out.opus`

支持的能力：

| 功能 | 模型 | 脚本 |
|------|------|------|
| 文字转语音（TTS） | moss-tts | `scripts/mosi_tts.sh` / `mosi_tts.py` |
| 指令式语音生成 | moss-voice-generator | `scripts/mosi_voice_generator.sh` |
| 语音转文字（ASR） | — | `scripts/mosi_asr.sh` |
| 多说话人对话合成 | moss-ttsd | `scripts/mosi_dialogue.sh` |
| 音效生成 | moss-sound-effect | `scripts/mosi_sound_effect.sh` |
| 声音克隆 | — | `scripts/mosi_voice.py` |
| 飞书语音气泡 | — | `scripts/mosi_feishu_voice.sh` |

Base URL：`https://studio.mosi.cn`

---

## 环境准备

### API Key

Key 通过 Kubernetes Secret 注入为 `MOSI_TTS_API_KEY`，对话中不得透露。

```bash
echo "key已配置: $([ -n "$MOSI_TTS_API_KEY" ] \
  && echo yes || echo NO)"
```

### 依赖清单

下表列出本 skill 用到的所有外部工具，以及缺失时的替代方案：

| 工具 | 用途 | 缺失时的处理 |
|------|------|-------------|
| `node` | JSON 处理、base64 解码 | 基础镜像自带，始终可用 |
| `curl` | HTTP 请求 | 基础镜像自带，始终可用 |
| `ffmpeg` | WAV→OPUS 转换（语音气泡必需） | 无法发语音气泡，TTS 仍可用 |
| `ffprobe` | 获取音频时长（随 ffmpeg 一起安装） | 同上 |
| `python3` + `python3-requests` | 声音克隆脚本 | 克隆功能不可用，其他功能正常 |
| `bc` | 浮点数计算 | 用 `awk` 或 `node -e` 替代 |
| `jq` | JSON 解析 | 用 `node -e` 替代 |
| `wget` | 文件下载 | 用 `curl -O` 替代 |
| `sox` | 音频格式分析/转换 | 用 `ffprobe` 替代 |
| `mediainfo` | 媒体文件元信息 | 用 `ffprobe` 替代 |
| `unzip` / `zip` | 压缩包处理 | — |
| `tree` | 目录结构显示 | 用 `ls -R` 替代 |
| `nano` | 文件编辑 | — |

### 一键检查当前环境

```bash
for cmd in node curl ffmpeg ffprobe python3 \
           bc jq wget sox mediainfo unzip zip; do
  printf "%-12s %s\n" "$cmd" \
    "$(which $cmd 2>/dev/null || echo '未安装')"
done
```

### 安装缺失依赖

**推荐方式**：重新构建镜像（`Dockerfile.py3` 已包含全部依赖）：

```bash
# 在项目根目录执行
docker build -f Dockerfile.py3 -t openclaw-custom .
```

**临时安装**（有 root 权限，重启后失效）：

```bash
apt-get update && apt-get install -y --no-install-recommends \
  python3 python3-pip python3-requests \
  ffmpeg bc jq wget sox mediainfo unzip zip tree nano
```

**没有 root 权限时**：

- 基础 TTS / ASR / 对话合成：只需 `curl` + `node`，脚本可直接运行
- 飞书语音气泡：必须有 `ffmpeg`，无权限时请让用户重建镜像
- 声音克隆：需要 `python3`，无权限时功能不可用

---

## 1. 文字转语音（TTS）

**接口**：`POST /api/v1/audio/speech`
**模型**：`moss-tts`
**输出**：24 kHz WAV，响应中 base64 编码

### Shell 脚本（无额外依赖）

```bash
bash scripts/mosi_tts.sh --text "你好，世界"
# 保存到：~/.openclaw/workspace/tts_output.wav

bash scripts/mosi_tts.sh \
  --text "Hello, world" \
  --voice-id 2001931510222950400 \
  --output ~/.openclaw/workspace/my_audio.wav
```

### Python 脚本（需要 python3 + requests）

```bash
python3 scripts/mosi_tts.py \
  --text "你好，世界" \
  --output ~/.openclaw/workspace/tts_output.wav
```

> **输出路径规则**：必须用 `~/.openclaw/workspace/`，
> workspace 以外的路径会被 OpenClaw 媒体策略拦截。

### 请求参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model` | string | — | 固定 `moss-tts` |
| `text` | string | — | 要合成的文本 |
| `voice_id` | string | — | 公共或自定义声音 ID |
| `expected_duration_sec` | float | 自动 | 目标时长（0.5–1.5× 自然语速） |
| `sampling_params.temperature` | float | 1.7 | 中文 1.7，英文 1.5 |
| `sampling_params.max_new_tokens` | int | 512 | 最大 token 数 |
| `meta_info` | bool | false | 是否返回性能指标 |

### 内置公共声音

| 声音 ID | 名称 | 风格 |
|---------|------|------|
| 2001257729754140672 | 阿树 | 轻松自然（默认） |
| 2001931510222950400 | 程述 | 播客、理性 |
| 2002941772480647168 | 阿宁 | 温柔、暖心 |
| 2020009311371005952 | 台湾女声 | 柔和、治愈 |
| 2020008594694475776 | 北京男声 | 清晰、标准 |
| 2001286865130360832 | 周周 | 独白、讲故事 |
| 2001898421836845056 | 子琪 | 活力、明亮 |
| 2001910895478837248 | 小满 | 甜美、开朗 |
| 2002991117984862208 | 梁子 | 专业、播报 |

---

## 2. 指令式语音生成（Voice Generator）

**接口**：`POST /api/v1/audio/speech`
**模型**：`moss-voice-generator`
**输出**：24 kHz WAV，响应中 base64 编码

通过自然语言描述所需的声音特征，即可生成对应风格的语音。
如果用户需要生成特定的某个名人的声音，可以告诉用户自己需要上网找一段音色，然后用这个音色调用voice clone接口（找不到就算了）。
无需指定 voice_id，用文字描述即可。

### Shell 脚本

```bash
# 播音腔女声
bash scripts/mosi_voice_generator.sh \
  -t "各位观众朋友们大家好，欢迎收看今天的新闻节目。" \
  -i "播音腔女声，专业、清晰、有亲和力，像央视新闻主播"

# 温柔男声
bash scripts/mosi_voice_generator.sh \
  -t "晚安，好梦" \
  -i "一个温柔的男声，轻柔舒缓"

# 有活力的年轻女声
bash scripts/mosi_voice_generator.sh \
  -t "欢迎来到我们的节目！" \
  -i "年轻有活力的女声，热情开朗"

# 指定输出路径
bash scripts/mosi_voice_generator.sh \
  -t "要生成的文字" \
  -i "声音描述" \
  -o ~/.openclaw/workspace/output.wav

# 获取性能指标
bash scripts/mosi_voice_generator.sh \
  -t "测试文本" \
  -i "专业女声" \
  --meta-info
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 固定 `moss-voice-generator` |
| `text` | string | 是 | 要转换成语音的文字 |
| `instruction` | string | 是 | 声音风格描述，如：一个温柔的女声 |
| `sampling_params.temperature` | float | 否 | 采样温度，默认 1.5 |
| `sampling_params.top_p` | float | 否 | 核采样阈值，默认 0.6 |
| `sampling_params.top_k` | int | 否 | Top-K 采样，默认 50 |
| `meta_info` | bool | 否 | 是否返回性能指标，默认 false |

### instruction 描述技巧

描述越详细，生成的声音越符合预期：

```
# 好的描述示例
"播音腔女声，专业、清晰、有亲和力，像央视新闻主播"
"年轻有活力的男声，语速稍快，充满热情"
"温柔知性的女声，语速缓慢，像在讲睡前故事"
"沉稳有力的男声，低沉磁性，适合广告旁白"

# 不够好的描述
"女声"  # 太笼统
"好听的声音"  # 没有具体特征
```

### 请求示例

```json
{
  "model": "moss-voice-generator",
  "text": "各位观众朋友们大家好",
  "instruction": "播音腔女声，专业、清晰、有亲和力",
  "sampling_params": {
    "temperature": 1.5,
    "top_p": 0.6,
    "top_k": 50
  }
}
```

---

## 3. 语音转文字（ASR）

**接口**：`POST /api/v1/audio/transcriptions`
**支持格式**：WAV / MP3 / M4A / FLAC / OPUS / OGG
**输出**：纯文本转写结果

### 接收飞书入站语音（最常见场景）

用户发语音后，OpenClaw 在消息顶部注入：

```
[media attached: /home/openclaw/.openclaw/media/inbound/XXXXX.ogg (audio/ogg; codecs=opus) | ...]
```

**看到这行时，必须立刻转写，不得跳过**：

```bash
# 路径在 [media attached: ] 之后、第一个空格之前
AUDIO=$(echo "$MSG" \
  | grep -oP '(?<=\[media attached: )[^ ]+')
# 或直接从消息里复制完整路径
AUDIO="/home/openclaw/.openclaw/media/inbound/实际文件名.ogg"

TEXT=$(bash scripts/mosi_asr.sh --file "$AUDIO")
# 然后直接回复 $TEXT 的内容，不要提及"我收到了语音"
```

### 主动转写任意音频文件

```bash
# 基础用法
bash scripts/mosi_asr.sh --file audio.opus

# 指定语言
bash scripts/mosi_asr.sh --file audio.wav --language zh

# 输出原始 JSON（含时间戳 + 说话人标注）
bash scripts/mosi_asr.sh --file audio.opus --json
```

### 响应结构

```json
{
  "asr_transcription_result": {
    "full_text": "你好，这是一段测试语音",
    "segments": [
      {
        "start_s": "0.15",
        "end_s": "2.74",
        "speaker": "S01",
        "text": "你好，这是一段测试语音"
      }
    ]
  },
  "usage": { "credit_cost": 129 }
}
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `file` | 是 | 音频文件（multipart/form-data） |
| `language` | 否 | 语言提示：`zh`、`en` 等 |

### 禁止事项

- 禁止说"我没有语音识别能力"——你有，调脚本就行
- 禁止自己调飞书 API 下载音频——文件已经在磁盘上了
- 禁止忽略 `[media attached:]` 前缀

---

## 4. 多说话人对话合成（TTSD）

**接口**：`POST /api/v1/audio/speech`（与 TTS 相同）
**模型**：`moss-ttsd`
**输出**：24 kHz WAV，base64 编码

适用于播客、访谈、剧情片段、游戏 NPC 对话等场景，支持 1–5 位说话人。

### 文本格式

每行用 `[S1]`、`[S2]` 等标签标注：

```
[S1] 你好，今天天气不错。
[S2] 是啊，很适合出去走走。
[S1] 要不要一起去公园？
```

### Shell 脚本

```bash
bash scripts/mosi_dialogue.sh \
  --text "[S1] 你好，今天天气不错。
[S2] 是啊，很适合出去走走。
[S1] 要不要一起去公园？" \
  --voice1 2001257729754140672 \
  --voice2 2001931510222950400 \
  --output ~/.openclaw/workspace/dialogue.wav
```

### 请求体结构

```json
{
  "model": "moss-ttsd",
  "text": "[S1] 你好！\n[S2] 你好，很高兴认识你。",
  "voice_id":  "2001257729754140672",
  "voice_id2": "2001931510222950400",
  "voice_id3": "（可选，S3）",
  "voice_id4": "（可选，S4）",
  "voice_id5": "（可选，S5）"
}
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `text` | 完整对话文本，每行以 `[S1]`/`[S2]`/… 开头 |
| `voice_id` | S1 的声音 ID（必填） |
| `voice_id2`–`voice_id5` | S2–S5 的声音 ID（按需添加） |
| `expected_duration_sec` | 目标总时长（可选） |

---

## 5. 音效生成

**状态**：API 接口暂未公开（截至 2026-03）

`moss-sound-effect` 模型存在，但 `studio.mosi.cn` 上还没有可用的
REST 接口。通过 `/api/v1/audio/speech` 调用会返回：

```json
{
  "code": 4000,
  "error": "Invalid Request: unsupported model for /audio/speech: moss-sound-effect"
}
```

`mosi_sound_effect.sh` 已预留，待接口上线后可直接使用。
预期请求结构：

```json
{
  "model": "moss-sound-effect",
  "prompt": "heavy rain with distant thunder",
  "duration_sec": 10
}
```

关注 `studio.mosi.cn/docs` 获取接口上线通知。

---

## 6. 声音克隆

从短音频（建议 10–120 秒）创建自定义声音。

### 接口清单

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/files/upload` | 上传音频文件 |
| POST | `/api/v1/voice/clone` | 从上传文件创建声音 |
| GET | `/api/v1/voices` | 列出所有自定义声音 |
| GET | `/api/v1/voices/{voice_id}` | 获取声音详情 |

### 完整流程

```bash
# Step 1：上传音频（WAV/MP3/M4A/FLAC，最大 100 MB）
python3 scripts/mosi_voice.py upload --file my_voice.wav
# => File ID: 1234567890

# Step 2：克隆
python3 scripts/mosi_voice.py clone \
  --file-id 1234567890 \
  --text "可选的转写文本，提供后质量更好"
# => Voice ID: abc123def

# Step 3：在 TTS 中使用克隆声音
bash scripts/mosi_tts.sh \
  --text "这是我的克隆声音" \
  --voice-id abc123def

# 列出所有声音
python3 scripts/mosi_voice.py list --status ACTIVE

# 获取声音详情
python3 scripts/mosi_voice.py get --voice-id abc123def
```

> `mosi_voice.py` 需要 `python3` + `requests`，
> 缺失时参考"环境准备"章节安装。

### 声音状态说明

| 状态 | 含义 |
|------|------|
| `ACTIVE` | 可正常使用 |
| `INACTIVE` | 已禁用 |
| `FAILED` | 克隆失败 |
| `DELETED` | 已删除 |

---

## 7. 飞书语音气泡

> **直接用一键脚本，不要自己管理中间文件。**
> 脚本内部已将所有路径固定在 `~/.openclaw/workspace/`。

### 一行命令搞定

```bash
bash scripts/mosi_feishu_voice.sh \
  --text "你好，世界" \
  --chat-id <CHAT_ID>
```

`<CHAT_ID>` 从入站消息 context 中获取：
群聊用 `GroupSubject` / `oc_xxxxxxxx`，私聊用 `From` / `ou_xxxxxxxx`。

可选指定声音：

```bash
bash scripts/mosi_feishu_voice.sh \
  --text "你好" \
  --chat-id oc_xxxx \
  --voice-id 2001931510222950400
```

### 脚本内部流程

1. TTS → `~/.openclaw/workspace/tts_output.wav`
2. ffmpeg：WAV → `~/.openclaw/workspace/tts_output.opus`
3. ffprobe 获取时长（毫秒）
4. 用 `$FEISHU_APP_ID` / `$FEISHU_APP_SECRET` 获取 tenant_access_token
5. 上传 OPUS 到飞书（`file_type=opus`）
6. 发送语音消息（`msg_type=audio`）

需要 ffmpeg：`apt-get install -y ffmpeg`

---

## 接口限额

| 限制项 | 数值 |
|--------|------|
| TTS RPM | 5 次/分钟 |
| 音效 RPM | 5 次/分钟 |
| 对话合成 RPM | 5 次/分钟 |
| 输出格式 | 24 kHz WAV（base64） |
| TTS 超时 | 600 秒 |
| 最大文本长度 | 约 1 小时音频 |

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `MOSI_TTS_API_KEY not set` | Secret 未注入 | 检查 K8s Secret |
| `{"code":4020}` | 余额不足 | 充值 MOSI 账户 |
| `{"code":4029}` | 触发限速 | 等待 60 秒后重试 |
| `{"code":5002}` | 声音不存在 | 确认 voice status 为 ACTIVE |
| `{"code":5004}` | 请求超时 | 将文本切分为更短片段 |
| `LocalMediaAccessError` | 输出路径被拦截 | 必须用 `~/.openclaw/workspace/` |
| `ffmpeg: not found` | 未安装 | `apt-get install ffmpeg` 或改用纯 sh 脚本 |
| `python3: not found` | 未安装 | TTS 用 `mosi_tts.sh`；声音克隆需安装 python3 |
