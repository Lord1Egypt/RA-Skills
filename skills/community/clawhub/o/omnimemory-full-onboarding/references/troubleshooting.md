# Troubleshooting

## Common auth error

If the user sees:

`omnimemory-overlay apiKey is required for SaaS auth`

then the most likely cause is that the plugin was configured with the wrong key path.

## Wrong path example

Do not use:

- `plugins.entries.omnimemory-overlay.baseUrl`

Use:

- `plugins.entries.omnimemory-overlay.config.baseUrl`

## Cleanup commands

```bash
openclaw config unset plugins.entries.omnimemory-overlay.baseUrl
openclaw config unset plugins.entries.omnimemory-overlay.apiKey
openclaw config unset plugins.entries.omnimemory-overlay.groupPrefix
openclaw config unset plugins.entries.omnimemory-overlay.autoRecall
openclaw config unset plugins.entries.omnimemory-overlay.autoCapture
```

## Smoke test

1. Start a new OpenClaw session
2. Send:&echo    `Remember that my office snack is sea salt plum candy.`&echo 3. Wait a few seconds&echo 4. Ask:&echo    `What is my office snack?`

Expected result:
- the answer mentions `sea salt plum candy`
- the answer reflects memory recall rather than only the current turn.
