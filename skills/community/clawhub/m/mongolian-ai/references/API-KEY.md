# API Key

- **`MONGOL_AI_SKILL_API_KEY`**：配合 `Authorization: Bearer`，请求 `https://mongol.open-idea.net/api/v1`；登录后在「API Key」页创建。
- **禁止**索要 Key、把 Key 贴进聊天、用 `openclaw config get` 验真（输出脱敏）。

```bash
openclaw config set env.MONGOL_AI_SKILL_API_KEY "<完整API Key>"
openclaw gateway restart
```

或 `%USERPROFILE%\.openclaw\.env` / `~/.openclaw\.env`：`MONGOL_AI_SKILL_API_KEY=<Key>` 后重启。

未配置提示全文：[BEHAVIOR-RULES.md](./BEHAVIOR-RULES.md)。
