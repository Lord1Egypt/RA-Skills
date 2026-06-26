# 开放 API 服务

> 来源：https://lxmusic.toside.cn/desktop/open-api
> 从 v2.7.0 起支持开放 API 服务

启用该功能后，将会在本地启动一个 HTTP 服务，提供以下接口供第三方软件调用。

**提示：** 若你要实时获取播放器状态，强烈建议使用 SSE 接口来获取状态，而不是通过轮询的方式重复调用状态接口。

---

## 获取播放器状态

- **接口地址：** `/status`
- **请求方法：** GET
- **响应格式：** JSON

### 请求参数

| 参数名 | 描述 |
|--------|------|
| filter | 过滤返回的字段，可选。可用字段看下方响应数据格式的字段名，多个字段用 `,` 分隔。默认值：`status,name,singer,albumName,lyricLineText,duration,progress,playbackRate` |

### 响应数据格式

| 字段名 | 描述 |
|--------|------|
| status | 播放器状态：`playing`、`paused`、`error`、`stoped` |
| name | 歌曲名 |
| singer | 艺术家 |
| albumName | 专辑名 |
| duration | 歌曲总时长（秒） |
| progress | 歌曲播放进度（秒） |
| playbackRate | 播放速率 |
| picUrl | 歌曲封面图片链接（HTTP 链接或 Data URL） |
| lyricLineText | 当前播放歌词文本 |
| lyricLineAllText | 当前播放歌词及扩展歌词文本（翻译、罗马音等，使用换行符分割） |
| lyric | 当前歌曲 LRC 歌词文本 |
| tlyric | 当前歌曲翻译 LRC 歌词文本（如果有） |
| rlyric | 当前歌曲罗马音 LRC 歌词文本（如果有） |
| lxlyric | 当前歌曲 Any Listen 歌词文本（如果有） |
| collect | 当前歌曲是否已收藏 |
| volume | 音量 |
| mute | 是否静音 |

### 响应示例

```json
{
  "status": "playing",
  "name": "天使的翅膀",
  "singer": "徐誉滕",
  "albumName": "李雷和韩梅梅",
  "duration": 214.543673,
  "progress": 5.051338,
  "playbackRate": 1,
  "picUrl": "http://xxx",
  "lyricLineText": "徐誉滕 - 天使的翅膀"
}
```

---

## 获取当前 LRC 歌词

- **接口地址：** `/lyric`
- **请求方法：** GET
- **响应格式：** UTF-8 编码的 LRC 文本

### 响应示例

```
[ar:安琥]
[ti:天使的翅膀]
[by:]
[al:全年伤感歌曲大盘点2]
[offset:0]
[00:00.0]徐誉滕 - 天使的翅膀
[00:05.50]词：徐誉滕
[00:10.100]曲：徐誉滕
[00:15.150]落叶随风将要去何方
```

---

## 获取当前歌曲所有类型歌词

- **接口地址：** `/lyric-all`
- **请求方法：** GET
- **响应格式：** UTF-8 编码的 JSON

### 响应示例

```json
{
  "lyric": "...",
  "tlyric": "...",
  "rlyric": "...",
  "lxlyric": "..."
}
```

---

## 播放器状态订阅（SSE）

SSE 事件流接口。本接口接受一个普通的 HTTP GET 请求，只是请求会保持长链接状态。播放器的状态在变更时通过文本事件流的形式将其实时返回。

**测试命令：**
```bash
curl -N http://127.0.0.1:23330/subscribe-player-status
```

- **接口地址：** `/subscribe-player-status`
- **请求方法：** GET
- **响应格式：** SSE 文本事件流

### 请求参数

| 参数名 | 描述 |
|--------|------|
| filter | 过滤返回的字段，可选。默认值：`status,name,singer,albumName,lyricLineText,duration,progress,playbackRate` |

### 事件名称

| 事件名 | 描述 |
|--------|------|
| status | 播放器状态 |
| name | 歌曲名 |
| singer | 艺术家 |
| albumName | 专辑名 |
| duration | 歌曲总时长（秒） |
| progress | 歌曲播放进度（秒） |
| playbackRate | 播放速率 |
| picUrl | 歌曲封面图片链接 |
| lyricLineText | 当前播放歌词文本 |
| lyricLineAllText | 当前播放歌词及扩展歌词文本 |
| lyric | 当前歌曲 LRC 歌词文本 |
| tlyric | 当前歌曲翻译 LRC 歌词文本 |
| rlyric | 当前歌曲罗马音 LRC 歌词文本 |
| lxlyric | 当前歌曲 Any Listen 歌词文本 |
| collect | 当前歌曲是否已收藏 |
| volume | 音量 |
| mute | 是否静音 |

### 响应示例

```
event: status
data: "playing"

event: name
data: "交换余生"

event: singer
data: "林俊杰"

event: albumName
data: "幸存者 Drifter"
```

---

## 播放器控制

| 接口地址 | 描述 | 参数 |
|----------|------|------|
| `/play` | 播放 | 无 |
| `/pause` | 暂停 | 无 |
| `/skip-next` | 下一曲 | 无 |
| `/skip-prev` | 上一曲 | 无 |
| `/seek` | 调整播放进度 | `offset` |
| `/volume` | 调整音量 | `volume`（值：1-100） |
| `/mute` | 调整静音 | `mute`（值：`true` / `false`） |
| **`/collect`** | **收藏当前歌曲** | 无 |
| **`/uncollect`** | **取消收藏当前歌曲** | 无 |

---

## 相关链接

- Scheme URL 文档：[Scheme URL 支持](/desktop/scheme-url)
- 更多 API 需求：[GitHub Issues](https://github.com/lyswhut/lx-music-desktop/issues?q=is%3Aissue+)
