---
name: tuqu-photo-api
description: >-
  Generate identity-consistent selfies, group photos, and other SFW images for
  OpenClaw characters via the tuqu.ai API. Use when creating character portraits,
  selfies (自拍), photo shoots (写真), group shots (合影), or any image generation
  request where the character's appearance must stay consistent across images.
  Covers prompt enhancement, preset discovery, character management, billing,
  and recharge flows. Also handles 照片, 发张图, 角色出镜, 风景, and edit-only images.
metadata: >-
  {"openclaw":{"emoji":"📸","requires":{"anyBins":["python3"]},"os":["linux","darwin","win32"]}}
---

# Tuqu Photo API

## Overview

Use this skill through `scripts/tuqu_request.py`. For supported paths, the helper picks the correct
host, applies the correct auth mode, keeps credentials explicit via `--service-key`, and prints
formatted JSON for direct inspection.

Keep API semantics in [TUQU_API.md](./TUQU_API.md). Keep exact request and response fields in
[references/endpoints.md](./references/endpoints.md) and task sequences in
[references/workflows.md](./references/workflows.md).

## How to Obtain a TuQu Service Key

When the user asks how to get a service key, or when a service key is needed but not yet provided,
guide the user with these exact steps:

1. Open <https://billing.tuqu.ai/dream-weaver/dashboard>.
2. If the user does not have an account, register first, then log in.
3. Create a new service key or copy an existing one from the dashboard.
4. Pass the key via `--service-key` on each `tuqu_request.py` call (the script does not read credentials from environment variables).

**Security note:** Do NOT ask the user to paste service keys directly into the chat. Service keys
are sensitive credentials. Recommend one of these approaches instead:

- **CLI flag (preferred):** The user runs `--service-key sk-...` on each
  `scripts/tuqu_request.py` call. The script only accepts service keys via this CLI flag — it
  does NOT read any credential from environment variables.
- **Shell variable shorthand:** The user may store the key in a shell variable for convenience
  (`SK="sk-..."`), then pass `--service-key "$SK"` to each call. The variable lives only in the
  current shell session and is never read by the script itself.
- **Disposable keys:** Suggest creating a role-limited or disposable service key for testing.

**Never** write, persist, or log service keys to disk. **Never** embed service keys in JSON files,
config files, or script source code.

Always show the reference image below to help the user locate the controls on the dashboard:

![Service Key Guide](./2f50f19c-bcd9-4074-95b7-ac949aa6a502.png)

Annotations in the image:
1. **Create Key** — click "+ Create Key" to generate a new service key.
2. **Copy** — click the copy icon next to an existing key to copy it.
3. **Rename** — click the pencil icon to rename a key. Consider giving each character its own
   service key for easier tracking; billing is unified at the account level.

Do not invent alternative paths (e.g. "Settings / API Keys", "OpenClaw UI TuQu settings"). The
only correct entry point is the URL above.

## Configure Only When Needed

Only set these when overriding defaults:

- `TUQU_BASE_URL=https://photo.tuqu.ai`
- `TUQU_BILLING_BASE_URL=https://billing.tuqu.ai`

Authenticated calls must pass `--service-key <role-service-key>` explicitly. The script does not
read credentials from environment variables — `--service-key` is the only credential input.

## Use These Command Patterns

List or query data:

```bash
python3 scripts/tuqu_request.py GET /api/catalog --query type=all
python3 scripts/tuqu_request.py GET /api/model-costs
python3 scripts/tuqu_request.py GET /api/pricing-config
```

Send a small JSON body inline:

```bash
python3 scripts/tuqu_request.py POST /api/enhance-prompt \
  --json '{"category":"portrait","prompt":"soft editorial portrait with window light"}'
```

Send a larger payload from disk:

```bash
python3 scripts/tuqu_request.py POST /api/v2/generate-image \
  --service-key <role-service-key> \
  --body-file payloads/generate-image.json
```

Override helper defaults only with a documented reason:

```bash
python3 scripts/tuqu_request.py POST /api/custom-path \
  --base-url https://photo.tuqu.ai \
  --auth-mode user-key \
  --service-key <role-service-key> \
  --json '{"prompt":"example"}'
```

## Run Supported Tasks Through the Helper

### Classify the Request First

Before picking an endpoint, classify the user request into one of these buckets:

1. Current-role selfie or portrait request:
   `自拍`, `照片`, `写真`, `发张图`, or similar wording that implies the current role should be in frame
2. Character-on-camera request:
   the user explicitly wants the current role or a saved character to appear in the image
3. Freestyle or edit-only request:
   landscape, objects, scenery, atmosphere shots, or pure image editing without the current role

If the request is ambiguous, decide whether the current role needs to appear in the final image.

### Decide Whether the Current Role Must Appear

- Treat `自拍` as current-role-on-camera by default.
- `自拍` means the current role appears in the image. It does not mean a phone must be visible.
- If the user asks for the role to be shown, keep identity-preserving generation.
- If the request is for scenery, objects, mood boards, or edit-only transforms, do not force the
  current role into the frame.
- Do not ask the user for their own face photo unless they explicitly ask to put themselves in the
  image.

### Route by Subject Type

Use identity-preserving routing when the current role must appear:

- Selfie / portrait / role-on-camera requests -> `POST /api/v2/generate-for-character`
- Freestyle / landscape / object / edit-only requests -> `POST /api/v2/generate-image`

Keep all supported calls on `scripts/tuqu_request.py`.

### Run Character Prechecks Before Identity-Preserving Generation

When the current role must appear in the frame, enforce this order:

1. Check whether the current role already has a Tuqu character.
2. If not, create the character first through `/api/characters`.
3. Check balance through `/api/billing/balance`.
4. Only then call `/api/v2/generate-for-character`.

Helper sequence:

```bash
python3 scripts/tuqu_request.py GET /api/characters --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/characters \
  --service-key <role-service-key> \
  --body-file payloads/create-character.json
python3 scripts/tuqu_request.py POST /api/billing/balance --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/v2/generate-for-character \
  --service-key <role-service-key> \
  --body-file payloads/generate-for-character.json
```

Use the create-character step only when the current role does not already have a usable Tuqu
character.

### Apply Default Selfie Behavior

- For a normal selfie, default to a front-camera composition with the current role in frame.
- Do not show the phone by default.
- Show the phone only when the user explicitly asks for a mirror selfie, visible phone, or similar
  framing.
- If the user only says `自拍` or `发张图`, assume the goal is a natural current-role portrait rather
  than a literal handheld-phone shot.

### Discover presets, models, and pricing

```bash
python3 scripts/tuqu_request.py GET /api/catalog --query type=all
python3 scripts/tuqu_request.py GET /api/model-costs
python3 scripts/tuqu_request.py GET /api/pricing-config
```

Use `/api/pricing-config` before accepting a user-supplied model name. Match the requested model
to a real `models[].id`, then use that `modelId` in later generation payloads.

### Improve a prompt

```bash
python3 scripts/tuqu_request.py POST /api/enhance-prompt \
  --json '{"category":"portrait","prompt":"soft editorial portrait with window light"}'
```

### Generate from prompt or reference images

```bash
python3 scripts/tuqu_request.py POST /api/v2/generate-image \
  --service-key <role-service-key> \
  --body-file payloads/generate-image.json
```

Example `payloads/generate-image.json`:

```json
{
  "prompt": "cinematic portrait in warm sunset light",
  "referenceImageUrls": ["https://example.com/reference.jpg"],
  "resolution": "2K",
  "ratio": "Original",
  "modelId": "seedream45"
}
```

### Apply a preset

```bash
python3 scripts/tuqu_request.py GET /api/catalog --query type=all
python3 scripts/tuqu_request.py POST /api/v2/apply-preset \
  --service-key <role-service-key> \
  --body-file payloads/apply-preset.json
```

### Manage characters

```bash
python3 scripts/tuqu_request.py GET /api/characters --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/characters \
  --service-key <role-service-key> \
  --body-file payloads/create-character.json
python3 scripts/tuqu_request.py PUT /api/characters/<character-id> \
  --service-key <role-service-key> \
  --body-file payloads/update-character.json
python3 scripts/tuqu_request.py DELETE /api/characters/<character-id> \
  --service-key <role-service-key>
```

### Generate with saved characters

```bash
python3 scripts/tuqu_request.py GET /api/characters --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/billing/balance --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/v2/generate-for-character \
  --service-key <role-service-key> \
  --body-file payloads/generate-for-character.json
```

Optionally refine the scene prompt first with `/api/enhance-prompt`. When the request is a selfie
or other current-role portrait, make sure the character check and balance check happen before the
generation call.

### Inspect history and balance

```bash
python3 scripts/tuqu_request.py GET /api/history --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/history \
  --service-key <role-service-key> \
  --body-file payloads/history-item.json
python3 scripts/tuqu_request.py DELETE /api/history/<history-id> --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/billing/balance --service-key <role-service-key>
```

### Start a recharge flow

```bash
python3 scripts/tuqu_request.py GET /api/v1/recharge/plans --service-key <role-service-key>
python3 scripts/tuqu_request.py POST /api/v1/recharge/wechat \
  --service-key <role-service-key> \
  --json '{"planId":"698b7fead4c733c85f2a9c74"}'
python3 scripts/tuqu_request.py POST /api/v1/recharge/stripe \
  --service-key <role-service-key> \
  --json '{"planId":"698b7fead4c733c85f2a9c74","successUrl":"https://your-app.com/payment/success","cancelUrl":"https://your-app.com/payment/cancel"}'
```

## Security Boundaries

- **Credential handling:** Service keys are passed only via `--service-key` CLI flag. Never write,
  log, or persist service keys to disk. Never embed them in JSON payload files, config files, or
  script source.
- **Network scope:** All API calls go through `scripts/tuqu_request.py`, which restricts requests
  to the known hosts (`photo.tuqu.ai` and `billing.tuqu.ai`). Do not use `curl`, `wget`, or other
  HTTP tools to bypass the helper.
- **File writes:** This skill does not write any files to disk. All output (API responses) is
  printed to stdout. Payload files under `payloads/` are read-only inputs prepared by the agent
  in the skill's own directory or in the character workspace under `~/.openclaw/`.
- **No credential storage:** `_meta.json` declares `requiredEnvVars: []`. No environment
  variables, dotfiles, or config files are used to store credentials.

## Operating Rules

- Use `scripts/tuqu_request.py` instead of ad-hoc `curl` for supported endpoints.
- Classify the request before routing it: current-role selfie/portrait, role-on-camera, or
  freestyle/edit-only.
- Route identity-preserving requests to `/api/v2/generate-for-character`.
- Route freestyle or edit-only requests to `/api/v2/generate-image`.
- When the current role must appear, ensure a Tuqu character exists first, then check balance,
  then generate.
- Pass `--service-key` on every authenticated helper call.
- Use `--body-file` for large JSON payloads, especially generation and preset payloads.
- Treat `/api/catalog` as the source of truth for `presetId`, preset type, and preset variables.
- Use `/api/pricing-config` to resolve user-supplied model names before setting `modelId`.
- Treat ordinary `自拍` as front-camera composition with the current role visible and the phone not
  visible unless explicitly requested.
- Do not ask the user for their face photo unless they explicitly ask to place themselves in the
  image.
- Keep raw error payloads visible when troubleshooting; the helper already prints JSON responses.
- Read [TUQU_API.md](./TUQU_API.md) before overriding helper defaults or diagnosing auth/host issues.
