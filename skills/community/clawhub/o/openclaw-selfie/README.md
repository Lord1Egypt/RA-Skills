# OpenClaw Selfie

Generate identity-consistent selfies, group photos, and other SFW images for OpenClaw characters
via the [tuqu.ai](https://tuqu.ai) API. Characters look the same across every generated image —
whether it's a portrait, a group shot, a stylized scene, or a preset-driven creation.

## Installation

### Option 1: Install from ClawHub (recommended)

```bash
clawhub install openclaw-selfie
```

Or with the native OpenClaw command:

```bash
openclaw skills install openclaw-selfie
```

### Option 2: Install from source

```bash
git clone https://github.com/<your-username>/tuqu-photo-skill.git
cp -r tuqu-photo-skill ~/.openclaw/skills/openclaw-selfie
```

### Prerequisites

| Requirement | Details |
| --- | --- |
| Python | 3.8+ (`python3` must be in your PATH) |
| tuqu.ai service key | One per OpenClaw role — obtain from [tuqu.ai](https://tuqu.ai) |
| Network access | The skill calls `photo.tuqu.ai` and `billing.tuqu.ai` |

### Verify Installation

```bash
# Should return a JSON catalog of available presets
python3 scripts/tuqu_request.py GET /api/catalog --query type=all

# Should return model list and pricing info
python3 scripts/tuqu_request.py GET /api/pricing-config
```

If both return valid JSON, the skill is ready. For authenticated calls (image generation, balance
checks, etc.), also pass your service key:

```bash
python3 scripts/tuqu_request.py POST /api/billing/balance --service-key <your-service-key>
```

### Optional: Override Default Hosts

Only needed if you run a custom tuqu.ai deployment:

```bash
export TUQU_BASE_URL=https://photo.tuqu.ai            # default
export TUQU_BILLING_BASE_URL=https://billing.tuqu.ai/dream-weaver  # default
```

## Quick Start

Once installed, just talk to your OpenClaw character naturally:

- **"来张自拍"** — generates a selfie with the current character's face
- **"拍张合影"** — generates a group photo with the character
- **"换个赛博朋克风格"** — applies a cyberpunk preset to the generation
- **"查看余额"** — checks the remaining token balance

The skill automatically classifies requests, picks the right endpoint, and preserves character
identity when needed.

### Manual API calls

```bash
# Enhance a prompt before generation
python3 scripts/tuqu_request.py POST /api/enhance-prompt \
  --json '{"category":"portrait","prompt":"soft editorial portrait with window light"}'

# Generate an image
python3 scripts/tuqu_request.py POST /api/v2/generate-image \
  --service-key <your-service-key> \
  --json '{"prompt":"cinematic portrait in warm sunset light"}'

# Generate with character identity preservation
python3 scripts/tuqu_request.py POST /api/v2/generate-for-character \
  --service-key <your-service-key> \
  --body-file payloads/generate-for-character.json
```

## Features

- **Identity-consistent generation** — characters look the same across all generated images
- Covers photo generation, preset application, prompt enhancement, catalog lookup, character
  management, history, balance, pricing config lookup, and recharge flows
- All API calls go through a single helper script (`scripts/tuqu_request.py`) that handles host
  selection, auth mapping, and JSON formatting
- API semantics documented separately in `TUQU_API.md` for maintainability

## Repository Layout

```text
SKILL.md                    Main skill instructions
TUQU_API.md                 API-specific host/auth/task guidance
references/
  endpoints.md              Endpoint request and response details
  workflows.md              Task-oriented API workflows
scripts/
  tuqu_request.py           Local request helper
tests/
  test_tuqu_request.py      Helper unit tests
dist/
  openclaw-selfie.skill      Generated skill artifact
```

## Configuration

| Variable | Required For | Notes |
| --- | --- | --- |
| `TUQU_BASE_URL` | Photo, catalog, history, and balance APIs | Defaults to `https://photo.tuqu.ai` |
| `TUQU_BILLING_BASE_URL` | Recharge APIs | Defaults to `https://billing.tuqu.ai/dream-weaver` |

Authenticated requests pass `--service-key <role-service-key>` instead of reading a shared
credential from the environment. The helper maps that value to `userKey`, `x-api-key`, or bearer
`serviceKey` based on the endpoint.

## Common Tasks

- Discover presets and styles:
  `python3 scripts/tuqu_request.py GET /api/catalog --query type=all`
- Improve a prompt before generation:
  `python3 scripts/tuqu_request.py POST /api/enhance-prompt --json '{"category":"portrait","prompt":"..."}'`
- Generate from text or reference images:
  `python3 scripts/tuqu_request.py POST /api/v2/generate-image --service-key <role-service-key> --body-file payloads/generate-image.json`
- Generate from a preset with source images:
  `python3 scripts/tuqu_request.py GET /api/catalog --query type=all`, then
  `python3 scripts/tuqu_request.py POST /api/v2/apply-preset --service-key <role-service-key> --body-file payloads/apply-preset.json`
- Generate with saved characters:
  `python3 scripts/tuqu_request.py GET /api/characters --service-key <role-service-key>`, then
  `python3 scripts/tuqu_request.py POST /api/v2/generate-for-character --service-key <role-service-key> --body-file payloads/generate-for-character.json`
- Check credits:
  `python3 scripts/tuqu_request.py POST /api/billing/balance --service-key <role-service-key>`
- Resolve model names and pricing:
  `python3 scripts/tuqu_request.py GET /api/model-costs` and
  `python3 scripts/tuqu_request.py GET /api/pricing-config`
- Start a recharge flow:
  `python3 scripts/tuqu_request.py GET /api/v1/recharge/plans --service-key <role-service-key>`,
  then `python3 scripts/tuqu_request.py POST /api/v1/recharge/wechat --service-key <role-service-key> --json '{"planId":"..."}'`
  or `python3 scripts/tuqu_request.py POST /api/v1/recharge/stripe --service-key <role-service-key> --json '{"planId":"...","successUrl":"...","cancelUrl":"..."}'`

## Documentation

- [Skill instructions](./SKILL.md)
- [API notes](./TUQU_API.md)
- [Endpoint reference](./references/endpoints.md)
- [Workflow recipes](./references/workflows.md)

## Development Notes

- Use `scripts/tuqu_request.py` instead of ad-hoc `curl` when possible.
- Keep `SKILL.md` focused on helper operations and keep API semantics in `TUQU_API.md`.
- Keep the helper's supported path list aligned with the documented capabilities.
- Keep credential handling explicit per request so multiple roles can use different service keys safely.
- Treat `dist/` as generated output.

## License

No license file is currently included in this repository.
