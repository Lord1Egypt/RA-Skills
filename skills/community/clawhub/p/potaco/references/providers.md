# Providers

Potaco supports built-in `openai`, `fal`, `vercel`, plus aliases and `custom` endpoints.

## Provider Support Matrix

| Feature | openai | fal | vercel | custom |
|---------|--------|-----|--------|--------|
| Generation | Yes | Yes | Yes | Yes |
| Editing | Yes | Yes | No | Yes |
| Model discovery | GET `/v1/models` | GET `api.fal.ai/v1/models` | GET `/v1/models` | GET `/v1/models` |
| Auth header | `Bearer <key>` | `Key <key>` | `Bearer <key>` | `Bearer <key>` |
| Requires `--base-url` | No | No | No | Yes |

Built-in provider names use preset base URLs. Any other provider name, including an alias using a built-in adapter type, must provide `--base-url` or `base_url`.

## Provider notes

- `openai`: base `https://api.openai.com/v1`, bearer auth, gen/edit via Images API, discovery filters to known image IDs (`gpt-image-2`).
- `fal`: base `https://fal.run`, discovery `https://api.fal.ai/v1/models?category=image`, auth `Key <api-key>`, edits use `<model-id>/image-to-image`.
- `vercel`: base `https://ai-gateway.vercel.sh/v1`, bearer auth, generation only, discovery filters `type == "image"`, model IDs use `provider/model`.
- `custom`: no default base URL, bearer auth, assumes OpenAI-compatible `/v1/images/generations`, `/v1/images/edits`, and `/v1/models`.

Vercel verification:
1. `GET /v1/models` to confirm the endpoint is reachable (5xx = fail).
2. `GET /v1/models/openai/gpt-image-2/endpoints` to validate the API key (401/403 = invalid).

## Custom provider security

- Confirm the base URL is trusted before configuring it. Prompts, images, masks, model names, and generated content may be sent to this endpoint.
- Prefer HTTPS for remote endpoints. Use local HTTP endpoints only when the user explicitly intends to target a local service.
- Do not use `--force` unless the user accepts skipping provider verification.
- Never configure credentials yourself unless the user explicitly asks you to start interactive auth or perform non-interactive credential setup. Otherwise instruct them to run `potaco auth add custom` interactively.
- Avoid non-interactive credential setup unless explicitly approved.

Setup:

```sh
potaco auth add custom
```

The base URL is stored in config after setup. Model discovery lists model IDs only; generation is assumed available and edit capability is configured by the user per model.
