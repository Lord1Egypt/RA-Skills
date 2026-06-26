# Word / PDF 翻译

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

- **`POST /word/translation/`** · **`POST /pdf/translation/`**（multipart）
- 字段：`from` · `to` · `mode`（如 `mongolian_only`）· `file` → 成功取 **`data.text`**。

Host / curl / 体积上限：[HTTP-REQUESTS.md](./HTTP-REQUESTS.md)。交付与计费 [SKILL.md](../SKILL.md)。再译下一环节时变量直通 `POST /translation/` 的 `content`。
