# OCR

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

**`POST /ocr/`**：默认 `language=mw`，西里尔文稿用 `mn`。

成功取 **`data.text`**。多步串联：再译 → `POST /translation/`（`content` 须变量直通，勿手抄）。

Host / JSON 示例：[HTTP-REQUESTS.md](./HTTP-REQUESTS.md)。交付与计费 [SKILL.md](../SKILL.md)。
