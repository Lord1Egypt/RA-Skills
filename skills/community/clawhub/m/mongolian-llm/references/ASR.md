# ASR

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

默认 **`POST /audio/async/`** + 轮询 **`GET /audio/async/{jobId}/`**；极短可 **`POST /audio/`**（multipart `file`）。

成功取 **`data.text`**。多步串联：再译 → `POST /translation/`（变量直通 `content`）。

Host / 同步·异步示例：[HTTP-REQUESTS.md](./HTTP-REQUESTS.md)。交付与计费 [SKILL.md](../SKILL.md)。
