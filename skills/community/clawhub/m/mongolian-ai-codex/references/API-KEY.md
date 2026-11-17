# API key handling

Use only `MONGOL_AI_SKILL_API_KEY` with the `Authorization: Bearer` header.

## Rules

- Check whether the variable is non-empty without printing it.
- Never ask the user to paste a key into chat.
- Never save, copy, transform, or echo a key.
- Never read arbitrary shell history or configuration files to find a key.
- Let the user configure the key in their terminal, secret manager, or agent settings.
- If a key was pasted into chat, tell the user to revoke and rotate it. Do not reuse or persist the pasted value.

`MENGGUYU_API_KEY` is deprecated and must not authenticate requests. When it exists without the new variable, stop and tell the user to rename the environment variable.

## Missing-key response

Explain that `MONGOL_AI_SKILL_API_KEY` must be configured locally. Direct the user to [mongol.open-idea.net](https://mongol.open-idea.net) to create a complete key, including any prefix. Do not offer to configure it from a value supplied in chat.

OpenClaw users should configure `skills.entries.mongolian-ai.apiKey`. Claude and Codex users should inject the variable through their normal shell or secret-management workflow.
