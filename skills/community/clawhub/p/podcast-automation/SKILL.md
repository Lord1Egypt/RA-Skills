---
name: podcast-automation
description: 播客全流程自动化——抓取、转录、Sonos播放、飞书Wiki归档。Use when user asks to download a podcast, transcribe audio, play on Sonos, or archive podcast notes to Feishu Wiki.
version: 1.0.0
homepage: https://clawhub.ai/skills/podcast-automation
metadata:
  openclaw:
    requires:
      bins: ["whisper", "sonos", "curl"]
    install:
      - id: whisper
        kind: pip
        package: openai-whisper
        bins: ["whisper"]
        label: Install Whisper (pip)
      - id: sonos
        kind: go
        module: github.com/steipete/sonoscli/cmd/sonos@latest
        bins: ["sonos"]
        label: Install sonoscli (go)
---

# Podcast Automation

一站式播客自动化技能，覆盖 **抓取 → 转录 → Sonos 播放 → 飞书 Wiki 归档** 全流程。

## 前提条件

| 依赖 | 用途 | 安装 |
|------|------|------|
| `curl` / `yt-dlp` | 下载播客音频 | `pip install yt-dlp`（可选，curl 可处理直链） |
| `whisper` | 本地语音转录 | `pip install openai-whisper` |
| `sonos` | Sonos 音箱控制 | `go install github.com/steipete/sonoscli/cmd/sonos@latest` |
| 飞书自建应用 | Wiki 归档 | 需开通 `wiki:wiki` 权限，配置 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` |

## 一、抓取播客音频

### 1.1 直链下载

```bash
curl -L -o /tmp/podcast.mp3 "https://example.com/episode.mp3"
```

### 1.2 RSS 解析 + 下载

```bash
# 解析 RSS 获取最新一期音频 URL
AUDIO_URL=$(curl -s "https://feeds.example.com/podcast.rss" \
  | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.fromstring(sys.stdin.read())
ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
enc = root.find('.//item/enclosure')
print(enc.get('url') if enc is not None else '')
")
curl -L -o /tmp/podcast.mp3 "$AUDIO_URL"
```

### 1.3 yt-dlp（支持 YouTube / Spotify 等平台）

```bash
yt-dlp -x --audio-format mp3 -o "/tmp/podcast.%(ext)s" "https://www.youtube.com/watch?v=XXX"
```

## 二、本地转录

```bash
whisper /tmp/podcast.mp3 --model medium --output_format txt --output_dir /tmp/podcast-out
# 转录结果: /tmp/podcast-out/podcast.txt
```

- `--model turbo`：速度优先
- `--model medium`：平衡
- `--model large`：精度优先
- `--task translate`：翻译为英文

## 三、Sonos 播放

```bash
# 发现音箱
sonos discover

# 播放本地或网络音频
sonos play --name "Kitchen" "https://example.com/episode.mp3"

# 音量控制
sonos volume set 20 --name "Kitchen"
```

> 如遇 `no route to host`，确认本地网络权限（macOS 需在隐私设置开启 Local Network）。

## 四、飞书 Wiki 归档

### 4.1 获取 Token

```bash
TOKEN=$(curl -s -X POST \
  'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")
```

### 4.2 创建 Wiki 页面

```bash
SPACE_ID="your_space_id"
RESULT=$(curl -s -X POST \
  "https://open.feishu.cn/open-apis/wiki/v2/spaces/$SPACE_ID/nodes" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"obj_type\":\"docx\",\"node_type\":\"origin\",\"title\":\"播客笔记: Episode Title\"}")
OBJ_TOKEN=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['node']['obj_token'])")
```

### 4.3 写入转录内容

```bash
TRANSCRIPT=$(cat /tmp/podcast-out/podcast.txt)
curl -s -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/$OBJ_TOKEN/blocks/$OBJ_TOKEN/children" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"children\":[{\"block_type\":2,\"text\":{\"elements\":[{\"text_run\":{\"content\":\"$TRANSCRIPT\"}}]}}],\"index\":0}"
```

## 五、完整流程示例

```bash
# 1. 抓取
curl -L -o /tmp/podcast.mp3 "https://cdn.example.com/ep42.mp3"

# 2. 转录
whisper /tmp/podcast.mp3 --model medium --output_format txt --output_dir /tmp/podcast-out

# 3. Sonos 播放
sonos play --name "Living Room" "https://cdn.example.com/ep42.mp3"

# 4. 归档到飞书 Wiki
bash references/scripts/archive-to-wiki.sh \
  --title "EP42: AI与未来" \
  --transcript /tmp/podcast-out/podcast.txt \
  --space-id "$FEISHU_SPACE_ID"
```

## 六、环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `FEISHU_APP_ID` | 飞书自建应用 App ID | 归档时必填 |
| `FEISHU_APP_SECRET` | 飞书自建应用 App Secret | 归档时必填 |
| `FEISHU_SPACE_ID` | 默认归档 Wiki 空间 ID | 归档时必填 |

## 七、触发场景

- 「下载这期播客并转录」
- 「把播客转录存到飞书Wiki」
- 「在Sonos上播放最新一期播客」
- 「抓取RSS并归档全部流程」
