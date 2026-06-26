# 帮记助手 — 参考说明

## 数据存储

### 默认路径（可配置）

- **物品位置**：`~/.memory-assistant/items.json` 或项目内 `.memory-assistant/items.json`
- **定时提醒**：`~/.memory-assistant/reminders.json` 或项目内 `.memory-assistant/reminders.json`

### 物品位置记录格式

```json
{
  "items": [
    {
      "id": "uuid或短id",
      "item": "备用电池",
      "location": "电视柜左侧第二个抽屉",
      "created_at": "2025-03-15T10:30:00Z"
    }
  ]
}
```

### 定时提醒格式

```json
{
  "reminders": [
    {
      "id": "uuid或短id",
      "at": "2025-03-15T15:00:00+08:00",
      "event": "下午三点开会",
      "advance_minutes": 15,
      "notify_at": "2025-03-15T14:45:00+08:00",
      "created_at": "2025-03-15T09:00:00Z",
      "status": "pending"
    }
  ]
}
```

- `at`: 事项发生时间（ISO8601）
- `notify_at`: 实际播报提醒的时间 = at − advance_minutes
- `status`: `pending` | `notified` | `cancelled`

---

## SenseAudio TTS API

### 接口

- **URL**: `https://api.senseaudio.cn/v1/t2a_v2`
- **Method**: POST
- **Headers**: `Authorization: Bearer YOUR_API_KEY`, `Content-Type: application/json`

### 请求体（同步、非流式示例）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | string | 是 | 固定 `SenseAudio-TTS-1.0` |
| text | string | 是 | 待合成文本，最大 10000 字符 |
| stream | boolean | 是 | 流式用 true；一次取整段用 false |
| voice_setting | object | 是 | 见下表 |
| audio_setting | object | 否 | 格式、采样率等 |

**voice_setting**

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| voice_id | string | 是 | - | 如 `male_0004_a`（儒雅道长-平稳） |
| speed | float | 否 | 1.0 | 语速 [0.5, 2.0] |
| vol | float | 否 | 1.0 | 音量 [0, 10] |
| pitch | int | 否 | 0 | 音调 [-12, 12] |

**audio_setting**

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| format | string | "mp3" | mp3, wav, pcm, flac |
| sample_rate | int | 32000 | 8000–44100 |
| channel | int | 2 | 1 或 2 |

### 响应（stream: false）

- `data.audio`: 十六进制编码的音频数据，需 hex 解码为二进制后写入 .mp3/.wav
- `data.status`: 2 表示合成结束
- `extra_info.audio_length`: 时长（毫秒）
- `base_resp.status_code`: 0 为成功

### 免费/尝鲜版常用 voice_id

| 音色 | voice_id |
|------|----------|
| 儒雅道长-平稳 | male_0004_a |
| 可爱萌娃-开心 | child_0001_a |
| 可爱萌娃-平稳 | child_0001_b |
| 沙哑青年-深情 | male_0018_a |

更多见：<https://senseaudio.cn/docs/voice_api>。

### cURL 示例（同步，保存为 mp3）

```bash
# 1. 请求并保存 JSON
curl -X POST https://api.senseaudio.cn/v1/t2a_v2 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "SenseAudio-TTS-1.0",
    "text": "您好，下午三点有会议，请提前准备。",
    "stream": false,
    "voice_setting": { "voice_id": "male_0004_a" }
  }' -o response.json

# 2. 提取 hex 并解码为 mp3
jq -r '.data.audio' response.json | xxd -r -p > reminder.mp3
```

### Python 示例（生成提醒语音并保存）

从 `.env` 加载密钥：在脚本开头 `load_dotenv()`，优先加载 `{baseDir}/.env`（技能目录），否则工作区根目录 `.env`。脚本运行时通过自身所在目录解析 `{baseDir}` 等价路径。

```python
def tts_senseaudio(text: str, out_path: str, api_key: str = None):
    api_key = api_key or os.environ.get("SENSEAUDIO_API_KEY")
    url = "https://api.senseaudio.cn/v1/t2a_v2"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "stream": False,
        "voice_setting": {"voice_id": "male_0004_a"}
    }
    r = requests.post(url, headers=headers, json=body)
    r.raise_for_status()
    data = r.json()
    if data.get("base_resp", {}).get("status_code") != 0:
        raise RuntimeError(data.get("base_resp", {}).get("status_msg", "TTS failed"))
    hex_audio = data.get("data", {}).get("audio")
    if not hex_audio:
        raise RuntimeError("No audio in response")
    with open(out_path, "wb") as f:
        f.write(bytes.fromhex(hex_audio))
    return out_path
```

---

## 时间解析约定

- 「下午三点」→ 当日 15:00（使用用户时区或配置的默认时区）
- 「六点钟和王先生约在和平饭店」→ 当日 18:00，事件摘要可存为「和王先生约在和平饭店」
- 「提前半小时」→ `advance_minutes: 30`
- 未说明提前量时默认 `advance_minutes: 15`

---

## 脚本说明

路径均以 `{baseDir}` 表示本技能所在目录，不暴露 `.cursor/skills` 或绝对路径；执行时由环境将 `{baseDir}` 解析为实际技能根目录。

### speak.py — 语音播报

- **路径**：`{baseDir}/scripts/speak.py`
- **依赖**：`{baseDir}/.env` 或工作区根目录 `.env` 中 `SENSEAUDIO_API_KEY`；`pip install requests python-dotenv`
- **数据**：物品位置从 `get_data_dir()` 下的 `items.json` 读取（项目 `.memory-assistant/` 或 `~/.memory-assistant/`）

| 参数 | 说明 |
|------|------|
| `--text "..."` | 直接合成并可选播放该文本 |
| `--item 物品名` | 从 items.json 查位置，合成「X 在 Y」并可选播放 |
| `--out FILE` | 输出 mp3 路径（默认临时文件） |
| `--play` | 合成后调用系统播放器（macOS: afplay） |
| `--voice ID` | 音色 ID，默认 male_0004_a |

### run_reminders.py — 定时提醒播报

- **路径**：`{baseDir}/scripts/run_reminders.py`
- **依赖**：同上；读取/写入 `reminders.json`（与 speak.py 同一数据目录）

| 参数 | 说明 |
|------|------|
| （无） | 单次检查：播报所有 `notify_at <= 当前时间` 且 `status=pending` 的提醒，并标为 notified |
| `--daemon` | 常驻运行，每 `--interval` 秒（默认 60）检查一次 |
| `--dry-run` | 只打印将播报的提醒，不调用 TTS、不修改状态 |
| `--voice ID` | 音色 ID |
| `--interval N` | daemon 模式下检查间隔（秒） |

**定时执行**：用 cron 每分钟执行一次单次检查，例如：  
`* * * * * cd {baseDir} && python scripts/run_reminders.py`
