# Tuqu Photo API Skill

A local skill package for working with the Tuqu Dream Weaver photo and billing APIs through a
Python helper that keeps host selection, auth mapping, and JSON handling consistent.

## Quick Start

Set the optional base URL overrides:

```bash
export TUQU_BASE_URL=https://photo.tuqu.ai
export TUQU_BILLING_BASE_URL=https://billing.tuqu.ai
```

Authenticated calls must provide a service key explicitly on each request. Do not rely on a shared
credential environment variable; different OpenClaw roles can carry different keys.

Run the bundled helper from the skill directory:

```bash
python3 scripts/tuqu_request.py GET /api/catalog --query type=all
python3 scripts/tuqu_request.py POST /api/enhance-prompt \
  --json '{"category":"portrait","prompt":"soft editorial portrait with window light"}'
python3 scripts/tuqu_request.py POST /api/v2/generate-image \
  --service-key <role-service-key> \
  --json '{"prompt":"cinematic portrait in warm sunset light"}'
python3 scripts/tuqu_request.py POST /api/billing/balance \
  --service-key <role-service-key>
```

The helper auto-selects the correct host and authentication mode for the supported endpoints,
including `/api/pricing-config`.

## Features

- Covers Tuqu photo generation, preset application, prompt enhancement, catalog lookup, character
  management, history, balance, pricing config lookup, and recharge flows
- Keeps the main `SKILL.md` helper-first so common tasks are expressed as
  `scripts/tuqu_request.py` commands
- Stores API semantics separately in `TUQU_API.md`
- Ships a small Python request helper for repeatable local testing

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
  tuqu-photo-api.skill      Generated skill artifact
```

## Configuration

| Variable | Required For | Notes |
| --- | --- | --- |
| `TUQU_BASE_URL` | Photo, catalog, history, and balance APIs | Defaults to `https://photo.tuqu.ai` |
| `TUQU_BILLING_BASE_URL` | Recharge APIs | Defaults to `https://billing.tuqu.ai` |

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
