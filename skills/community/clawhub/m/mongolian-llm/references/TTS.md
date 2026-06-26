# TTS

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

默认 **`POST /tts/async/`**；极短可 **`POST /tts/`**。**禁用** `POST /tts/stream`。

**调用前**向用户列齐 12 音色：`Kore · Puck · Zephyr · Charon · Fenrir · Aoede · Leda · Orus · Iapetus · Sulafat · Achird · Achernar`。未选按下表；默认不报 `speed`；要快/慢用 **1.2 / 0.8**。`text` 与用户正文须**逐字**一致。异步：`POST /tts/async/` → 约 3～5s 轮询 `GET /tts/async/{jobId}/` 至 `done`，`audioBase64` 解码为 WAV。

| 特征 | voice |
|------|-------|
| 正式/公文 | Kore |
| 新闻/教学 | Iapetus |
| 儿童/故事 | Leda |
| 情感/问候 | Sulafat |
| 日常聊天 | Achird |
| 运动/广告 | Fenrir |
| 轻松娱乐 | Aoede |
| 社媒/活泼 | Puck |
| 诗歌/文学 | Zephyr |
| 纪录片 | Charon |
| 史诗/深沉 | Orus |
| 舒缓/睡眠 | Achernar |
| 其它 | Kore |

`lang` · `speed` · Host/curl 示例：[HTTP-REQUESTS.md](./HTTP-REQUESTS.md)（TTS 节）。交付与计费 [SKILL.md](../SKILL.md)。
