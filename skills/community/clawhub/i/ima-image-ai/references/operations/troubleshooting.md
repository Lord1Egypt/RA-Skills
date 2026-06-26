# Troubleshooting

When a request fails, use this order:

1. `python3 scripts/ima_runtime_setup.py --install` for local dependencies
2. `python3 scripts/ima_runtime_doctor.py --output-json` for environment and API diagnostics
3. `python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json` for live catalog visibility

## Authentication Failed (`401`, `Unauthorized`, `Invalid API key`)

Likely causes:

- `IMA_API_KEY` is missing, expired, or copied incorrectly
- the shell session does not have the latest exported key

Recovery:

```bash
echo "$IMA_API_KEY"
python3 scripts/ima_runtime_doctor.py --output-json
export IMA_API_KEY="ima_xxxxxxxx"
python3 scripts/ima_runtime_doctor.py --output-json
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
```

Regenerate keys from: `https://www.imaclaw.ai/imaclaw/apikey`

## Insufficient Points (`4008`, `insufficient points`)

Likely causes:

- the account balance is too low for the selected model or parameter combination
- the request uses a larger size or more outputs than needed for a first pass

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --prompt "simple studio product photo" \
  --output-json
```

If the recommended default is still too expensive, rerun with a lower-cost `model_id` from `--list-models`.

Top up account credits from: `https://www.imaclaw.ai/imaclaw/subscription`

## Missing Input Image For `image_to_image`

Likely causes:

- `--input-images` was omitted
- the task should have been `text_to_image` instead

Wrong:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --prompt "turn this into an oil painting"
```

Correct:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images ./example.png \
  --prompt "turn this into an oil painting" \
  --output-json
```

## Parameter Mismatch (`6009`, `6010`, `attribute`)

Likely causes:

- the selected model does not accept the current custom parameter combination
- a custom `size`, `aspect_ratio`, or `n` value does not match a live credit rule

Recovery:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --prompt "test image" \
  --output-json
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
python3 scripts/ima_runtime_doctor.py --output-json
```

If the default request works, add one custom control back at a time. If you need to pin a model manually, choose a current live `model_id` from `--list-models`.

## Polling Timeout (`timed out`, `600s`)

Likely causes:

- the prompt is too ambitious for a first pass
- the request uses a large size or multiple outputs
- the service is temporarily slow

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --prompt "simple studio product photo, clean white background" \
  --output-json
```

If you need a cheaper or faster option than the recommended default, rerun with a lower-cost live `model_id` from `--list-models`. Retry the higher-detail request only after the smaller request succeeds.

## Network Errors (`Connection timeout`, `Network unreachable`, catalog fetch failure)

Likely causes:

- local network connectivity is unstable
- outbound access to `api.imastudio.com` or `imapi.liveme.com` is blocked
- the service is temporarily degraded

Recovery:

```bash
python3 scripts/ima_runtime_setup.py
python3 scripts/ima_runtime_doctor.py --output-json
python3 scripts/ima_runtime_cli.py --task-type text_to_image --list-models --output-json
```

If local setup passes but doctor or catalog lookup fails, check network egress to `api.imastudio.com` and `imapi.liveme.com`.

## Invalid `--extra-params` JSON

Likely causes:

- the JSON is not quoted correctly for the shell
- the value is not a JSON object

Wrong:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --extra-params '{n:4}'
```

Correct:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --extra-params '{"n":4,"aspect_ratio":"16:9"}' \
  --prompt "wide poster concept" \
  --output-json
```
