# `POST /translation/`

路由：[INTERFACE-ROUTING.md](./INTERFACE-ROUTING.md)。

`zh` / `mw` / `mn` 互译；勿用 `POST /chat/completions/` 代译。取 **`data.tgtText`**。[HTTP-REQUESTS.md](./HTTP-REQUESTS.md) · [SKILL.md](../SKILL.md)

**必填** `from`、`to`、`content`。

```json
{ "from": "zh", "to": "mw", "content": "文本" }
```

## 规则摘要

- **分段与换行**：网关对单次 `content` 自动按 `\n` 切段、超长再切，拼回一个 `data.tgtText`；**通常一次请求带全文**即可，触 `content` 上限再分批。JSON 里用转义 `\n`，勿裸多行入串。
- **方向**：U+1800–U+18AF → 常 `mw→zh`；西里尔块 → `mn→zh`；否则常 `zh→mw`；蒙蒙互转显式 `mn↔mw`。
- **蒙蒙互译 `mn↔mw`**：单次 `POST /translation/`；扣费以响应计费字段为准。
- **响应**：`data.srcText` 仅核对；蒙→中结果为中文，不适用「全程蒙文禁汉字」类 chat 规则。
