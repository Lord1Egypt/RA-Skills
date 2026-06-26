# NanoGPT Authentication

Source: https://docs.nano-gpt.com/authentication.md

## API Key
- New key format: `sk-nano-<uuid>`
- Legacy keys: plain UUID (still accepted)
- Auth methods:
  - `Authorization: Bearer <API_KEY>` (recommended)
  - `x-api-key: <API_KEY>`

## Env var convention (for plugin)
`NANOGPT_API_KEY`

## CLI Device Login
For CLI tools — users approve in browser, CLI receives `sk-nano-...` key.
See: https://docs.nano-gpt.com/integrations/cli-login

## Web App
OAuth (GitHub, Google), magic link, email/password, Passkey.

## Best Practices
- Store in env vars — never commit to git
- Use separate keys per app/environment
- Prefer `Authorization: Bearer` over URL params
