# ImageForge Troubleshooting

ImageForge errors are returned as JSON with `error` and `message` fields. Messages are redacted before display, but agents must still avoid echoing secrets.

## `missing_config`

Cause: API key, model, or an edit image path is missing; the API URL is fixed to NextAI Code.

Fix first-use configuration by having the agent run the readiness gate:

```bash
python3 "$IMAGE_FORGE_SCRIPT" ensure-ready
```

If configuration is missing, `ensure-ready` opens the setup page. The user registers/logs in at `https://www.nextai-code.com`, gets an API Key, then fills API key and default model in the browser page. The API URL is shown as locked. The setup server listens only on `127.0.0.1`, uses a one-time token URL, and shuts down after saving. Do not ask normal users to configure `PATH` or run setup manually.

Do not continue the current ImageForge flow until preflight passes.

Check current local status:

```bash
python3 "$IMAGE_FORGE_SCRIPT" doctor
```

Check whether ImageForge is allowed to proceed:

```bash
python3 "$IMAGE_FORGE_SCRIPT" preflight
```

If `preflight` fails, do not continue the image task through local rendering or any other fallback. Configure ImageForge first.

## `auth_failed`

Cause: the provider returned `401` or `403`.

Fix:

- Confirm the API key was created at `https://www.nextai-code.com`.
- Confirm the key is valid for image generation and editing.
- Prefer updating the key through the secure prompt or `IMAGE_FORGE_API_KEY`.
- Do not paste the key into logs, Git, or replies.

## `provider_rejected` or `protocol_error`

Cause: the provider rejected the request, returned invalid JSON, omitted `data`, or omitted `data[].b64_json`.

Fix:

- Confirm NextAI Code is reachable and implements OpenAI-compatible `/v1/images/generations` and `/v1/images/edits`.
- Confirm the configured model is accepted by NextAI Code.
- Confirm the requested `--size`, `--quality`, and `--n` values are supported by that provider.
- For URL-only responses, use a NextAI Code configuration that returns `data[].b64_json`.

## `multi_image_unsupported`

Cause: the provider rejected an edit request with multiple `--image` values.

Fix:

```bash
python3 "$IMAGE_FORGE_SCRIPT" edit --brief '<approved brief>' --image '<path>' --prompt '<instruction>'
```

Use one image path unless the target provider has been validated for multi-image edits.

## `network_error`

Cause: DNS, TLS, routing, proxy, firewall, timeout, or provider availability failure.

Fix:

- Confirm the machine can reach the fixed NextAI Code API URL.
- Check corporate proxy, VPN, and firewall settings.
- Retry after transient provider/network incidents.
- Run `doctor` to verify the configured host without exposing secrets.

## `version_check_unavailable`

Cause: Git or remote origin lookup is unavailable.

Fix:

```bash
python3 "$IMAGE_FORGE_SCRIPT" check-version
```

If it remains unavailable, continue using generate/edit normally. Version checks degrade safely and never block generation or editing.

When an update is available, the version-check output includes:

```bash
npx skills update image-forge
```

## Secret hygiene checklist

- Store API keys only in `~/.config/image-forge/secrets.json` or `IMAGE_FORGE_API_KEY`.
- Keep `.image-forge/config.json` limited to non-secret project configuration.
- Never commit API keys, shell history snippets, logs, or agent replies containing secrets.
- Never store API keys in `image-forge/`, `SKILL.md`, reference docs, agent metadata, or Git.
- Redact provider errors before sharing them.
