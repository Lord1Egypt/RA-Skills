---
name: music-search
description: Multi-source music search and streaming. Search songs from 10+ platforms and stream to TRTC rooms.
description_zh: "多源音乐搜索与推流，支持10+平台搜索并推流到TRTC房间"
description_en: "Multi-source music search and TRTC streaming from 10+ platforms"
---

# music-search 多源音乐下载技能

支持从多个音乐平台搜索并下载MP3文件。

## 功能

- **多源搜索** - 同时从10个音乐平台搜索歌曲
- **自动下载** - 获取播放链接并下载MP3文件
- **智能切换** - 一个音源失败自动切换到下一个
- **防盗链绕过** - 自动处理各平台的Referer

## 使用方式

```bash
# 默认模式：搜索并返回可在线播放的 URL（不下载）
python3 music_downloader.py "歌曲名"
python3 music_downloader.py "周杰伦 晴天"
python3 music_downloader.py "五月天 伤心的人别听慢歌" --play

# JSON 模式：搜索并返回 JSON 格式结果（推荐，便于脚本解析）
python3 music_downloader.py "周杰伦 晴天" --json

# 下载模式：搜索并下载 MP3 文件到 /tmp/music/
python3 music_downloader.py "周杰伦 晴天" --download
```

### JSON 输出格式

```json
{"artist": "周杰伦", "name": "晴天", "source": "kuwo", "url": "http://..."}
```
失败时：`{"error": "未找到可播放的歌曲"}`

## 直播推流（TRTC StreamIngest 集成）

> 🔴 **直播模式强制规则**：当 `/tmp/trtc_stream/config.json` 存在时（直播模式），搜到歌曲后必须执行 `stream_ingest_client.py` 推流到 TRTC 房间！

### 完整执行示例

```bash
# 1. 上报任务
python3 /tmp/trtc_stream/agent_bus.py task "收到指令：播放晴天"
python3 /tmp/trtc_stream/agent_bus.py exec "搜索音乐：晴天"

# 2. 搜索音乐（使用 --json 输出，便于解析 URL）
python3 $SKILL_DIR/music_downloader.py "晴天 周杰伦" --json

# 3. 从 JSON 中提取字段：
#    - url     → 传给 --url
#    - name    → 传给 --song-name
#    - artist  → 传给 --artist-name

# 4. 推流到 TRTC 房间（不可跳过！）
python3 /tmp/trtc_stream/agent_bus.py info "正在为您播放：晴天 - 周杰伦"
python3 /tmp/trtc_stream/stream_ingest_client.py \
  --url "$URL" \
  --song-name "$NAME" \
  --artist-name "$ARTIST"

# 5. 上报完成
python3 /tmp/trtc_stream/agent_bus.py result "音乐播放已开始"
```

> ⚠️ **自检**：如果你的回复中搜到了歌曲但没有执行 `stream_ingest_client.py`，你正在违反规则。

## 支持的音源 (10个)

| 音源 | 平台 | 优先级 |
|------|------|--------|
| thttt.com | 好听音乐网（酷我源） | 1 |
| kugou.com | 酷狗音乐 | 2 |
| kuwo.cn | 酷我音乐 | 3 |
| netease | 网易云音乐 | 4 |
| qq | QQ音乐 | 5 |
| gequbao.com | 歌曲宝 | 6 |
| 5nd.com | 5nd音乐网 | 7 |
| 1ting.com | 一听音乐 | 8 |
| 9ku.com | 九酷音乐 | 9 |
| musicenc.com | MusicEnc | 10 |

## 工作流程

1. **搜索阶段** - 同时向所有可用音源发送搜索请求
2. **排序** - 按音源优先级整理结果
3. **获取链接** - 调用各平台API获取播放URL
4. **下载** - 使用正确的Referer绕过防盗链
5. **失败重试** - 下载失败自动尝试下一首

## 输出

- 下载成功：返回文件路径，如 `/tmp/music/周杰伦_晴天.mp3`
- 下载失败：返回错误信息

## 注意事项

- 部分平台需要SSL绕过（已自动处理）
- 酷我CDN需要特定的Referer头
- 下载的MP3文件保存在 `/tmp/music/` 目录
- 文件名格式：`歌手_歌名.mp3`

## 依赖

- Python3
- requests 库
- 网络访问权限
