# Model generation

The API runner uses the `APISROUTER_API_KEY` environment variable and the fixed public APIsRouter
endpoint. It produces JSON status records, which the Agent should inspect after every command.

## Discover and plan

```sh
node "$SKILL_DIR/scripts/generate.mjs" models
```

This reads the authenticated model catalogue. Choose only a model available to that account and
implemented by this runner. A catalogue entry is not a delivery or balance check.

Video request example:

```json
{
  "kind": "video",
  "model": "seedance-2.0-mini",
  "prompt": "A gentle close-up of rain on green leaves. Slow push in, calm natural light.",
  "seconds": 5,
  "resolution": "720p",
  "ratio": "9:16"
}
```

Supported video request tuples:

| Model | Seconds | Resolution | Ratio |
| --- | --- | --- | --- |
| seedance-2.0-fast | 4 | 480p | 16:9 |
| seedance-2.5 | 4 | 480p | 16:9 |
| seedance-2.0-mini | 5 | 720p | 9:16 |

The runner rejects other video fields. The route has no reference-image/video/audio, first/last
frame or voice-control contract. The 3 October 2026 Mini verification returned a landscape
1280x720 video despite the ratio above. Inspect every delivered file and disclose such differences.

Image request example:

```json
{
  "kind": "image",
  "model": "gpt-image-2",
  "prompt": "A ceramic cup on a pale green studio backdrop, soft window light.",
  "resolution": "1k",
  "size": "1:1"
}
```

Image tiers are `1k`, `2k` and `4k`; `size` is a supported aspect ratio. Add `images` as an array of
local PNG/JPEG/WebP paths relative to the request JSON for an edit (at most eight, each at most
20 MiB). One output is requested per
submission. Current support is validated by the script; unsupported fields fail before a POST.
An earlier release check received HTTP503 for GPT Image 2. Treat service availability as a live
fact and preserve the error rather than manufacturing an image or silently switching accounts.

## Submit once, then recover by receipt

Review the number of jobs, their specifications, current account pricing and the user's accepted
scope. Installing this Skill or listing it free does not authorize unlimited model spending.

```sh
node "$SKILL_DIR/scripts/generate.mjs" submit \
  --request requests/shot-01.json --job jobs/shot-01.json --confirm-cost
node "$SKILL_DIR/scripts/generate.mjs" poll --job jobs/shot-01.json
node "$SKILL_DIR/scripts/generate.mjs" collect \
  --job jobs/shot-01.json --output assets/shot-01.mp4
```

The submit command reserves the job file before contacting the API. Reusing it will not repeat
the paid request. Keep the receipt when work is queued or a session is interrupted. Poll an
acknowledged video job at a reasonable interval, usually 10–20 seconds, until it completes or the
user's waiting scope is reached. Resume the same job later instead of submitting a replacement.

Images arrive synchronously; their returned data is retained in the job for collection. Videos
return a `task_id` and are queried through `/videos/tasks/{task_id}`. Collection downloads the
existing result to a new local path without forwarding the account key to the download server.

A timeout or malformed acknowledgement can leave submission outcome unknown. Inspect the
account/task evidence before deciding on another paid request. HTTP authentication, permission,
quota and service failures are distinct from local rendering failures. Preserve the structured
error code and known task identity, without copying raw credentials or signed download URLs into
chat. Do not automatically retry a paid POST.
