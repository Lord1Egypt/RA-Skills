# Troubleshooting

When a request fails, use this order:

1. `python3 scripts/ima_runtime_setup.py`
2. `python3 scripts/ima_runtime_doctor.py --task-type text_to_video`
3. `python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models --output-json`

## Authentication Failed (`401`, `Unauthorized`, `Invalid API key`)

Likely causes:

- `IMA_API_KEY` is missing, expired, or copied incorrectly
- the shell session does not have the latest exported key

Recovery:

```bash
echo "$IMA_API_KEY"
python3 scripts/ima_runtime_doctor.py --task-type text_to_video
export IMA_API_KEY="ima_xxxxxxxx"
python3 scripts/ima_runtime_doctor.py --task-type text_to_video
python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models --output-json
```

Regenerate keys from: `https://www.imaclaw.ai/imaclaw/apikey`

## Subscription Required (`4014`, `403`, `requires a subscription`)

Likely causes:

- `ima-pro` (`Seedance 2.0`) was selected on an account without an active plan

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --model-id ima-pro-fast \
  --prompt "simple camera move over a studio product shot" \
  --output-json
```

Upgrade from: `https://www.imaclaw.ai/imaclaw/subscription`

## Insufficient Points (`4008`, `insufficient points`)

Likely causes:

- the selected model or resolution is too expensive for the current balance
- the request uses a longer duration than needed for a first pass

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type reference_image_to_video --list-models --output-json
python3 scripts/ima_runtime_cli.py \
  --task-type reference_image_to_video \
  --model-id ima-pro-fast \
  --reference-images ./example-reference.jpg \
  --prompt "simple product showcase turntable, clean background" \
  --output-json
```

Top up credits from: `https://www.imaclaw.ai/imaclaw/subscription`

## Missing Or Wrong Media Inputs

### `image_to_video`

Wrong:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_video \
  --prompt "animate this"
```

Correct:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_video \
  --input-images ./example.png \
  --prompt "slow push-in with soft motion" \
  --output-json
```

### `first_last_frame_to_video`

Wrong:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type first_last_frame_to_video \
  --input-images ./first.png \
  --prompt "transition between these frames"
```

Correct:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type first_last_frame_to_video \
  --input-images ./first.png ./last.png \
  --prompt "transition between these frames" \
  --output-json
```

### `reference_image_to_video`

At least one reference input is required. For Seedance (`ima-pro`, `ima-pro-fast`), reference images, videos, and audios are all supported.

## Seedance Reference Validation Failed

Likely causes:

- too many reference files
- unsupported `mp4/mov` or `wav/mp3` variants
- video or audio duration is outside `2~15s`
- image/video dimensions or aspect ratio are outside the allowed range
- total input size exceeds the request limit

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type reference_image_to_video --list-models --output-json
python3 scripts/ima_runtime_doctor.py --task-type reference_image_to_video
```

Then retry with:

- fewer reference files
- shorter video/audio clips
- smaller files or lower-resolution media

## Compliance Verification Failed

This applies only to `ima-pro` / `ima-pro-fast` on:

- `image_to_video`
- `first_last_frame_to_video`
- `reference_image_to_video`

Likely causes:

- one or more uploaded/reference assets were rejected by `/open/v1/assets/verify`
- the verification result was still `processing`

Recovery:

```bash
python3 scripts/ima_runtime_doctor.py --task-type reference_image_to_video
python3 scripts/ima_runtime_cli.py --task-type reference_image_to_video --list-models --output-json
```

If the same asset repeatedly fails, replace it with a different source before retrying.

## Parameter Mismatch (`6009`, `6010`, `attribute`, `no matching rule`)

Likely causes:

- the selected model does not accept the current custom parameter combination
- custom `duration`, `resolution`, `mode`, or `model` values do not match a live credit rule

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type reference_image_to_video --list-models --output-json
python3 scripts/ima_runtime_doctor.py --task-type reference_image_to_video
```

If the default request works, add one custom control back at a time.

## Polling Timeout (`timed out`, `2400s`)

Likely causes:

- the prompt is too ambitious for a first pass
- the request uses longer duration or higher resolution than needed
- the service is temporarily slow

Recovery:

```bash
python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models --output-json
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --model-id ima-pro-fast \
  --extra-params '{"duration":5,"resolution":"480p"}' \
  --prompt "simple studio product reveal" \
  --output-json
```

## Network Errors (`Connection timeout`, catalog fetch failure, upload token failure)

Likely causes:

- local network connectivity is unstable
- outbound access to `api.imastudio.com` or `imapi.liveme.com` is blocked
- the service is temporarily degraded

Recovery:

```bash
python3 scripts/ima_runtime_setup.py
python3 scripts/ima_runtime_doctor.py --task-type text_to_video
python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models --output-json
```

## Invalid `--extra-params` JSON

Wrong:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --extra-params '{duration:10}'
```

Correct:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --extra-params '{"duration":10,"resolution":"720p"}' \
  --prompt "wide product teaser" \
  --output-json
```
