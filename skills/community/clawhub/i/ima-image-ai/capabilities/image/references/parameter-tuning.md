# Parameter Tuning

This runtime exposes three practical controls for most image requests:

- `size` through `--size`
- `aspect_ratio` through `--extra-params`
- `n` through `--extra-params`

Ground rules:

- explicit CLI values win over prompt-inferred controls
- the runtime keeps both `size` and `aspect_ratio` when both are present
- the backend validates whether that combination is supported for the chosen model
- larger requests usually cost more credits and take longer, but exact rules come from the live product catalog

## `size`

Use `--size` when you want a direct quality and latency tradeoff.

| Size hint | Good for | Cost / speed trend |
| --- | --- | --- |
| `512px` | fast previews, rough ideation, testing prompts | lowest cost, fastest |
| `1k` | web graphics, social posts, general iteration | low-to-medium cost |
| `2k` | higher-detail mockups, review renders, larger layouts | higher cost, slower |
| `4k` | final-detail passes, print-oriented drafts, premium output | highest cost, slowest |

Examples:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 512px \
  --prompt "poster sketch for a tea brand" \
  --output-json
```

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 2k \
  --prompt "luxury skincare product hero shot" \
  --output-json
```

Best practice:

- start with `512px` or `1k` while exploring prompts
- when you specify controls like `size`, `aspect_ratio`, `n`, or `quality` without forcing a model, the runtime first tries to find a live catalog model that supports those constraints
- move to `2k` or `4k` only after the composition is already working
- if a request fails with an attribute mismatch, retry without custom size first

## `aspect_ratio`

The current CLI does not expose a dedicated `--aspect-ratio` flag. Pass it through `--extra-params`.

| Ratio | Good for | Example syntax |
| --- | --- | --- |
| `1:1` | square social posts, avatars, thumbnails | `--extra-params '{"aspect_ratio":"1:1"}'` |
| `16:9` | wide posters, slides, video thumbnails | `--extra-params '{"aspect_ratio":"16:9"}'` |
| `9:16` | mobile posters, story/reel concepts | `--extra-params '{"aspect_ratio":"9:16"}'` |
| `4:3` | presentation-style graphics, classic layouts | `--extra-params '{"aspect_ratio":"4:3"}'` |
| `3:2` | photo-oriented framing, print-style layouts | `--extra-params '{"aspect_ratio":"3:2"}'` |

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --extra-params '{"aspect_ratio":"16:9"}' \
  --prompt "cinematic electric car launch poster" \
  --output-json
```

Best practice:

- choose the ratio for the destination surface first
- then choose the smallest size that is good enough for that surface
- if you include both `size` and `aspect_ratio`, expect the backend to accept or reject the full combination as a unit

## `n`

The current CLI does not expose a dedicated `--n` flag. Pass it through `--extra-params`.

| `n` | Good for | Tradeoff |
| --- | --- | --- |
| `1` | default production path | cheapest and fastest |
| `2` | light A/B comparison | slightly more cost and wait |
| `4` | broader concept exploration | noticeably higher cost and slower |

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --extra-params '{"n":4}' \
  --prompt "packaging concept for a premium chocolate bar" \
  --output-json
```

Best practice:

- keep `n=1` for first validation runs
- use `n=2` or `n=4` only when the user explicitly wants multiple variants
- expect higher total credit usage and longer waits as `n` increases

## Recommended Combinations

### Fast Prompt Iteration

Use when you are still searching for the right composition or wording.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 512px \
  --prompt "minimal poster for a jazz festival" \
  --output-json
```

### Wide Poster Draft

Use when the output will be shown in a landscape slot.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 2k \
  --extra-params '{"aspect_ratio":"16:9"}' \
  --prompt "epic fantasy game key art, dramatic sky, title-safe framing" \
  --output-json
```

### Mobile Vertical Concepts

Use when you want several candidate layouts for stories or reels.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_image \
  --size 1k \
  --extra-params '{"aspect_ratio":"9:16","n":2}' \
  --prompt "beauty campaign poster, bold typography area at the top" \
  --output-json
```

### Conservative Image-To-Image Restyle

Use when you want to keep the source image recognizable while changing the visual treatment.

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_image \
  --input-images ./example.png \
  --size 1k \
  --prompt "keep the subject and composition, convert to a watercolor illustration" \
  --output-json
```
