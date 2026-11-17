# Ofox image API — parameter reference

Source: `https://ofox.ai/docs/api/openai/images`,
`https://ofox.ai/models/google/gemini-3.1-flash-image` (verified
2026-08-29). Re-check the live docs before relying on exact values far in
the future — params, model ids, and pricing can drift.

This is the parameter surface `references/ofox-image.sh` builds a request
from. Use this table to decide what to pass; the script validates the
documented value lists and the known `n` + Gemini incompatibility before it
ever calls the API.

## Generate request fields (`POST /v1/images/generations`)

Synchronous — no job id, no polling. The image comes back in the response
body directly, always base64-encoded (no URL option, ever).

| Field | Type | Required | `ofox-image.sh` flag | Notes |
|---|---|---|---|---|
| `model` | string | yes | `--model` (optional flag) | The API field is required; the flag is not — omit it and the script resolves one from its cheapest-first priority chain (`MODEL_CHAIN` in `ofox-image.sh`, the only place that list exists) and reports any fallback. Run `ofox-image.sh models` for the live list — 16 image models as of 2026-09-15, and the script accepts any of them. Documented in depth here: `openai/gpt-image-2`, `google/gemini-3.1-flash-image` (this is "Nano Banana 2" — use this exact model id string, **not** `-preview`; the model catalog page's URL slug differs from the actual API model id), `qwen/qwen-image-3.0-pro`. Others work but their size/quality support is not documented here. |
| `prompt` | string | yes | `--prompt` | Text description of the image. |
| `quality` | string | yes per doc | `--quality` | One of `auto`/`low`/`medium`/`high`/`standard`/`hd` — that is the union across models, and **no model is known to accept all six**. The script requires you to pass one explicitly rather than guessing a safe default, and since 1.7.0 validates it twice: against the union, then against the resolved model's own accepted set where that set has been enumerated first-hand. So `openai/gpt-image-2` + `standard` is now a client-side rejection at `--dry-run` (exit `1`, no call) instead of a submission-time HTTP 400. Where a model has never enumerated its set, the union still stands — see "Confirmed gotcha: supported `--quality` values differ per model" below. |
| `n` | integer | no | `--n` | 1-10, server default 1. **`google/gemini-3.1-flash-image` does not support `n` at all — passing it (even `n: 1`) errors.** The script rejects `--n` client-side whenever the effective model is Gemini, and since 1.14.0 rejects an `n` key set via `--extra-json` for **every** model — `n` has a flag, and a key with a flag cannot come through the escape hatch. |
| `size` | string | no | `--size` | One of `auto`/`1024x1024`/`1536x1024`/`1024x1536`/`256x256`/`512x512`/`1792x1024`/`1024x1792`. **This enum cannot express 16:9 or 9:16** — see the ratio table below. `--target-aspect W:H` / `--target-size WxH` are not API fields: they are client-side, and they pick this value, then crop the written file to the ratio asked for. |
| `input_images` | string[] | no | not exposed — out of scope | URL or base64, 1-3 items, **Qwen only**, for image-to-image. **Any other field name is silently ignored** — the request silently degrades to text-to-image with no error, so get the field name exactly right if you ever add this. Still unexposed, and still rejected when set via `--extra-json`, rather than silently sending a request that would ignore it. **If you want to change an existing image, that is `ofox-image.sh edit` (`POST /v1/images/edits`), not this field** — a different endpoint, working on every model whose catalog entry carries it rather than on Qwen alone. This row stays out of scope because a field name that degrades silently to text-to-image is a trap, not because editing is. |
| `output_format` | string | no | `--output-format` | One of `png`/`jpeg`/`webp`. The script maps `jpeg` to a `.jpg` file extension; `png`/`webp` keep their own extension. Defaults to `png` when not set (the documented example uses `png`, it's lossless, and it's the safest cross-model assumption — the response body itself does not include an explicit format field to infer from). |
| `background` | string | no | `--background` | One of `transparent`/`opaque`/`auto`. No cross-field requirement with `output_format` is documented for this endpoint specifically (some background/format interactions are common in similar APIs, but this hasn't been confirmed here) — the script does not enforce one; if you get an unexpected error combining `background: transparent` with a non-alpha format, that's a starting hypothesis to test, not yet a confirmed rule. |
| `stream` | boolean | no | not exposed — out of scope | Default `false`. `ofox-image.sh` only parses a plain JSON response body, not a streamed one — the script rejects `stream: true` set via `--extra-json`. |
| `extra_body.provider.type` | string | no | via `--extra-json` | `openai`/`azure_foundry`, `gpt-image-2` only. Pass `{"extra_body":{"provider":{"type":"..."}}}` through `--extra-json`. |

`--extra-json` is merged into the built request body last (object merge —
its keys win over anything the flags set), so it's the escape hatch for any
field not exposed as a dedicated flag.

### What `--extra-json` will not do (1.14.0)

Because it is merged *last* and *wins*, it could rewrite fields the script had
just validated and priced. Refusals, all before any request:

| Input | Result |
|---|---|
| `--extra-json ""` written explicitly | error, exit 1. Omitting the flag is unchanged — asserted byte-for-byte against `--extra-json '{}'` in `references/test/keyguard.test.sh`. |
| anything that is not a JSON object (`[…]`, `"s"`, `42`, `null`, `false`) | error, exit 1 — the merge is jq's `*`, which only works between objects |
| a key that has a flag: `model`, `prompt`, `quality`, `size`, `n`, `output_format`, `background` | error, exit 1, naming the flag to use instead |
| `input_images`, `stream: true` | error, exit 1, for the reasons in the rows above |

Everything else still passes through, `extra_body.provider.type` included.

The third row is the one with money attached: the estimate is computed from
the flags, and this merge happens after it — so `--quality low` plus
`--extra-json '{"quality":"high","size":"1792x1024"}'` would quote ~0.6 cents
and send the request that measured **15.4** cents.

Note what that row absorbed: `n` is now refused for **every** model, not only
for `google/gemini-3.1-flash-image` as before. The narrower Gemini-specific
check for `n` in `--extra-json` was removed rather than left as a branch that
could no longer run.

### Confirmed gotcha: supported `--quality` values differ per model

`quality` is required, has no safe default, and **is not the same enum on
every model**. What this repo has actually observed:

| Model | Observed to accept | Observed to reject | Evidence |
|---|---|---|---|
| `openai/gpt-image-2` | `high`; and `low`, `medium`, `auto` per the rejection message's own list | **`standard`** | a real 400 on 2026-09-04 (below), plus a completed `--quality high` run the same day |
| `microsoft/mai-image-2.5-flash` | `standard` | — | the nine images this repo's asset work generated before the 2026-09-04 chain reorder, all on this model, all with `standard` |
| `google/gemini-3.1-flash-image` | `low` | — | the paid run recorded in `references/pricing.md` |

The rejection, verbatim from the run that hit it — `openai/gpt-image-2`,
`--quality standard`, HTTP 400, **nothing billed**:

```
Invalid value: 'standard'. Supported values are: 'low', 'medium', 'high', and 'auto'
```

Four things follow from that one line:

- **A wrong `--quality` costs a round-trip, not money.** Upstream refuses it
  before any image is generated, so it surfaced as `ofox-image.sh` exit `3`
  with the message above, free to fix and retry. The run that hit it
  reported no charge — evidence for, but not a full answer to, "Billing on
  rejection — open question" below.
- **Since 1.7.0 the script does not let that round trip happen for this
  model.** `model_qualities()` in `ofox-image.sh` holds the four values the
  message above enumerates, and `generate` checks `--quality` against the
  model it resolves to — so the combination fails at `--dry-run` with exit
  `1` and an error naming the model, including when the model came from
  `MODEL_CHAIN` rather than from a `--model` the caller typed. The table
  holds **one row**, deliberately: `mai-image-2.5-flash` accepting `standard`
  nine times is evidence a value works, not an enumeration of what it takes,
  and inventing a narrower set for it would reject calls that succeed. A
  false rejection is worse than this 400, which costs nothing but a
  round trip. Models with no enumeration keep the full union.
- **`standard` is not a portable value**, even though it is in the documented
  union and the model that used to head the priority chain accepts it. When
  `MODEL_CHAIN`'s preferred model changed to `openai/gpt-image-2` on
  2026-09-04, the value every previous call in this repo had passed became an
  instant 400 on a default `generate` — a per-model enum silently became a
  breaking change of a default.
- **`hd` has not been accepted by any model here**, and the message above
  omits it from `gpt-image-2`'s four, so expect it to fail there too. That
  expectation is read off the message, not tested.

Only the model **id** is validated against live data (see "The model list"
below); there is no `image_attributes` to check a quality value against, so
this table is the only per-model record and grows one confirmed row at a
time.

## Response (`POST /v1/images/generations`, HTTP 200)

Fixed shape, always base64, no URL option ever:

```json
{
  "created": 1777385517,
  "data": [{ "b64_json": "<base64>", "index": 0 }],
  "model": "openai/gpt-image-2",
  "size": "1024x1024",
  "quality": "low",
  "usage": {
    "input_tokens": 14,
    "input_tokens_details": { "text_tokens": 14 },
    "output_tokens": 208,
    "total_tokens": 222
  }
}
```

| Field | Meaning |
|---|---|
| `data[].b64_json` | Base64-encoded image bytes. `ofox-image.sh` decodes each entry and writes it to its own file; if `n` produced more than one image, filenames get a `_<index>` suffix, otherwise the base name is used as-is. |
| `model` / `size` / `quality` | The values Ofox actually used to generate the image — may not always exactly echo what was requested (e.g. `auto` resolving to a concrete value). The script prints these from the response, not from the request, for exactly this reason. **`model` is not always sent**: `openai/gpt-image-2` omits it entirely, so the script falls back to the requested id and flags that with `MODEL_SOURCE request`; when the field *is* present and names a different model, that one wins for both display and pricing. See `references/pricing.md` § "Which-model trap". |
| `usage.input_tokens` / `usage.output_tokens` / `usage.total_tokens` | Real token counts for this specific generation. The script prints these directly (`USAGE_INPUT_TOKENS`/`USAGE_OUTPUT_TOKENS`/`USAGE_TOTAL_TOKENS`) — never estimate or invent these numbers. It also multiplies them by the model's published rates into an `IMAGE_COST` line; `references/pricing.md` has the formula and the invoice it was verified against. |

There is no documented `output_format`/file-format field in the response
body itself — if you need to know the actual format Ofox produced and you
didn't request one via `output_format`, the safest source of truth is
inspecting the decoded file's own magic bytes (e.g. `file <path>`), not
guessing from any response field.

### The `size` enum cannot express 16:9 or 9:16

Every accepted value, with its true ratio:

| `size` | Ratio | What it actually is |
|---|---|---|
| `1024x1024`, `512x512`, `256x256` | 1.0000 | 1:1, exact |
| `1536x1024` | 1.5000 | 3:2, exact |
| `1024x1536` | 0.6667 | 2:3, exact |
| `1792x1024` | **1.7500** | nearest 16:9, which is 1.7778 |
| `1024x1792` | **0.5714** | nearest 9:16, which is 0.5625 |

**16:9 and 9:16 cannot be requested at all**, on any model, at any quality.
This is not a model defect but a structural gap between this endpoint's
`size` enum and the video API's `aspect_ratio` values, so every 16:9 or 9:16
frame produced here has to be cropped afterwards. There is no flag that
removes the crop; `--target-aspect`/`--target-size` only move it into the
script, which measures the written file and centre-crops to exact integer
multiples of the reduced ratio (`1344x768 → 1344x756`,
`1792x1024 → 1792x1008` — both of them real hand-crops before the flags
existed).

**The consequence lives in the video API, not here.** Attaching an image to
`bytedance/seedance-2.5` forces `aspect_ratio: adaptive`
(`ofox-video-core/references/api-params.md`), so the frame's own ratio
becomes the finished clip's ratio whatever the video flags say. A 1.75 frame
delivers a 1.75 clip, and correcting it costs another video generation. A
ratio error in a two-cent image is billed at the price of the clip it was
attached to.

### Confirmed gotcha: the response's `size` field is not reliable evidence of the real output dimensions

A real, paid call (2026-08-29, `google/gemini-3.1-flash-image`, `size:
512x512` requested) returned `"size": "512x512"` in the response body — but
the actual decoded PNG's real pixel dimensions, verified with `file` and
`sips -g pixelWidth -g pixelHeight` (macOS; `identify` from ImageMagick
works too), are **1024x1024**. The model appears to always generate at its
native 1024x1024 resolution and simply echoes back whatever `size` was
requested, regardless of what it actually produced.

This is confirmed only for `google/gemini-3.1-flash-image`, and
`microsoft/mai-image-2.5-flash` has a worse variant of it — requested
`1792x1024`, response echoed `1354x774`, saved file `1344x768`, three
disagreeing numbers rather than two (`references/pricing.md`).

**`openai/gpt-image-2` does not have the problem**: one real, paid run on
2026-09-04 at `--size 1792x1024` had the request, the response's echo and the
file's real pixels all agree at `1792x1024`. That does not retire the check
below, and the same run is why — 1792x1024 is 1.75, not 16:9, so the frame
still had to be cropped to `1792x1008` before it could be attached to a
`bytedance/seedance-2.5` job, which inherits the attached frame's own ratio
(`aspect_ratio: adaptive` is forced). **Measure the file and crop regardless
of the model**; what changes per model is how big the correction is, not
whether one is needed. `qwen/qwen-image-3.0-pro` is still untested.

`ofox-image.sh`'s printed `SIZE` line is taken directly from the response
body (see the table above), so it inherits this unreliability. Its
`SIZE_ACTUAL` line is measured from the written file with `ffprobe` and is
the one to believe; when the two disagree the script says so on stderr
instead of leaving it to be noticed. **If a caller genuinely needs a
specific output size or ratio guarantee** (a video first frame is the
standard case), pass `--target-aspect`/`--target-size` — the script then
measures the file and crops to the target, or fails loudly. Doing it by hand
means verifying the saved file's real dimensions directly rather than
trusting `SIZE`/the response's `size` field. This is the same "don't trust a documented/response field's claim
about media output without checking the real artifact" pattern as the
`mirror_urls`/`unsigned_urls` and `aspect_ratio: adaptive` lessons in
`.trellis/spec/skills/external-api-integration.md` for the video skill.

## Edit request fields (`POST /v1/images/edits`)

**No longer out of scope.** This endpoint was excluded from `ofox-image-core`
through v1.10.3 and is implemented as `ofox-image.sh edit` from 1.11.0. It
takes an image you already have and changes it, which is a different thing
from `input_images` on the generations endpoint (still unexposed, still
Qwen-only, still silently ignored under any other field name).

Everything below is from real calls made on 2026-09-15, not from
documentation. The rejections cost nothing; the two successes are recorded in
`references/token-anchors.json` under `edit_anchors`.

### It is multipart-only

An `application/json` body with `model` set came back *"You must provide a
model parameter"* — the field was never seen. So the request is built from
`-F` form fields and there is no JSON payload; `ofox-image.sh edit --dry-run`
prints a `FORM_FIELDS` line (names only) where `generate` would print a
payload.

| Field | Type | Required | `ofox-image.sh edit` flag | Notes |
|---|---|---|---|---|
| `image` | file upload | one of these two | `--image PATH` | The primary path, and the one to prefer: it needs no hosting anywhere. Sent as `-F "image=@PATH"`. |
| `image_url` | string | one of these two | `--image-url URL` | A public URL, or a `data:image/...;base64,...` URI — the data URI was **confirmed accepted at validation** (it got past file handling to the model check, where a deliberately bogus model produced `model_not_found`). Sent as `-F "image_url=<tmpfile"`, never as a command-line value: a base64 data URI of any real photo exceeds `ARG_MAX` and would die locally before the network. |
| `model` | string | yes | `--model` (optional flag) | Optional flag, required API field — the script resolves one from `MODEL_CHAIN` **against the edits endpoint** when it is omitted. Which models can edit is not a list in this repo; see below. |
| `prompt` | string | required by the script | `--prompt` | Whether the API requires it is **untested and deliberately so**: the only way to find out is to send an edit without one, and on this endpoint anything not rejected renders and bills. |
| `quality` | string | no | `--quality` | Not required here, unlike generations. Omitting it returned `"quality": "low"`. **Not validated upstream** — see the warning below. |
| `size` | string | no | `--size` | Validated locally for typos only. Whether this endpoint honours it is **untested**. Both measured runs omitted it and got a size derived from the input's aspect ratio. |
| `n` | integer | no | `--n` | 1-10. Multiplies the spend. |
| `output_format` | string | no | `--output-format` | `png`/`jpeg`/`webp`. Unlike generations, the **response echoes this field**, so the script names the saved file from what the API says it wrote and falls back to the request only when the field is absent. |
| `background` | string | no | `--background` | `transparent`/`opaque`/`auto`. The response echoes it (`"opaque"` observed). |
| `mask` | file upload | unknown | **not reachable from this script** | Whether masked/inpainting edits are supported is **not established**, and finding out costs a billed edit per attempt. Until 1.14.0 this row said to try it with `--extra-form "mask=@FILE"`; that spelling is now refused along with every other `@`/`<` value, because it uploads whatever local file it names (see the `--extra-form` note below). Attaching a mask needs its own flag with its own path validation — nobody has written one, so this stays open. |

Input formats are enumerated by the API's own refusal of a `text/plain`
upload: *"Supported file formats are 'image/jpeg', 'image/png', and
'image/webp'."* That is the API enumerating its own set, which is the only
basis on which the script keeps a local copy of it.

### `--extra-form` is for extra FIELDS, and since 1.14.0 only for fields

This endpoint is multipart, so the escape hatch is `--extra-form K=V` rather
than a JSON merge. Two prefixes on the **value** are refused (exit 1, before
the request):

| Value | What curl does with it | Now |
|---|---|---|
| `@path` | uploads the file at `path` | refused |
| `<path` | reads `path` and sends its contents as the field value | refused |
| anything else | sends it as a literal value | unchanged |

`--extra-form "mask=@$HOME/.ssh/id_rsa"` was a working way to make this script
upload any file the user can read to whatever `API_BASE` points at. The field
name did not matter, so the fix is on the value, not on a list of field names.

This does **not** touch the script's own uploads: `-F "image=@PATH"` and
`-F "image_url=<TEMPFILE"` are built from `--image` / `--image-url`, which are
validated paths the script chose, and both are asserted still working in
`references/test/keyguard.test.sh`. An ordinary pair — `k=user@example.com`,
`k=a<b`, `k=` — is unaffected; only a value *starting* with the character is.

The **key** is narrowed too, for the same reason `--extra-json` is on the
generations side: `image`, `image_url`, `model`, `prompt`, `quality`, `size`,
`n`, `output_format` and `background` all have flags, and every one of them is
refused here. A second multipart part with an owned name is not a harmless
duplicate — the server picks one of the two, the value that arrived this way
skipped the flag's validation, and it is appended **after**
`print_edit_estimate` has already been computed from the flags. `--extra-form
"n=10"` printed `N 1`, quoted a single image and asked for ten; `n` multiplies
the bill directly, so that is the never-under-quote rule broken through the
escape hatch. The guard list is extracted from the script's own form builders
by the test suite rather than retyped there, so a flag added without a matching
entry goes red on its own.

### ⚠️ This endpoint does not validate parameters the way generations does — and the failure mode is a bill

`POST /v1/images/generations` rejects a bad `--quality` with a free HTTP 400
(that is the whole basis of the per-model table above). `POST
/v1/images/edits` **does not**. Measured 2026-09-15: `quality=ultra_not_a_value`
was sent to six models as a deliberate guard, on the assumption it would be
refused the way the sibling endpoint refuses it. All six ignored the value,
rendered, and billed.

Two things follow, and the second is the general one:

- **The client-side checks in `ofox-image.sh edit` are not a round-trip
  saving, they are the guard.** On `generate`, a validation check that the API
  would also make saves a few seconds. Here it saves the money. This is the
  one place in this skill where a *false rejection* is arguably better than
  permissiveness, which inverts the rule the `--quality` table above is built
  on — so the script checks `--quality` against the documented **union** only,
  and deliberately does **not** apply `model_qualities()`'s per-model
  enumeration, because that set was read off a *generations* refusal and
  assuming two endpoints of one API behave symmetrically is a mistake this
  repo has already made (see "don't assume two endpoints expose symmetric
  metadata" below and in the spec).
- **A free probe is only free if the thing you expect to reject it does.**
  The technique of pairing a probe with a deliberately-invalid guard
  parameter, used throughout this repo to map an API at $0, silently costs
  money on an endpoint that ignores unknown parameters. Verify that the guard
  itself is refused — on a model you have already established rejects the
  request for a different reason — before fanning a guarded probe out across
  a list.

### Which models can edit is a live lookup, not a table

Each `/v1/models` entry's `supported_endpoints` array names
`/v1/images/edits` or does not, and that is the whole answer. Confirmed
predictive in both directions on 2026-09-15:

| Direction | Evidence |
|---|---|
| array omits it → refused | `qwen/qwen-image-3.0-pro` → `400 endpoint_not_supported`, before any parameter was looked at, nothing billed |
| array carries it → runs | seven models ran an edit: `openai/gpt-image-2`, `google/gemini-2.5-flash-image`, `google/gemini-3-pro-image`, `google/gemini-3.1-flash-image`, `google/gemini-3.1-flash-lite-image`, `microsoft/mai-image-2.5`, `microsoft/mai-image-2.5-flash` |

Four of the eleven models advertising the endpoint are untested
(`microsoft/mai-image-2.5-pro`, `openai/gpt-image-1.5`,
`openai/gpt-image-2.5-flare`, `openai/gpt-image-2.5-sunburst`) and
deliberately stay that way: the flag has been predictive on every model
tested, the script reads it live, and confirming the remaining four costs a
billed edit each for no decision it would change.

Note that `image_attributes.supported_params` is **not** where this lives — it
lists generation fields only (`prompt`, `n`, `size`, `quality`,
`output_format`, `stream`, `user`) and several image models have no
`image_attributes` block at all. Looking there and concluding "the catalog
advertises nothing about editing" is easy to do and wrong; the capability is
one field over. Run `ofox-image.sh models --endpoint edits` for the current
list.

### Response (`POST /v1/images/edits`, HTTP 200)

Same `data[].b64_json` shape as generations, with a richer `usage` and three
echoed fields generations does not send:

```json
{
  "background": "opaque",
  "created": 1789452894,
  "data": [{ "index": 0, "b64_json": "<base64>" }],
  "model": "openai/gpt-image-2",
  "output_format": "png",
  "quality": "low",
  "size": "1672x941",
  "usage": {
    "input_tokens": 608,
    "input_tokens_details": { "image_tokens": 576, "text_tokens": 32 },
    "output_tokens": 301,
    "output_tokens_details": { "image_tokens": 301 },
    "total_tokens": 909
  }
}
```

So **yes, edits report `usage`** — and then some. `input_tokens_details`
splits the prompt's text from the uploaded image, and **the image you upload
is billed**: 576 of those 608 input tokens were the picture. A generation has
no equivalent component. `openai/gpt-image-2` also *does* send `model` on this
endpoint, having never sent it on generations.

### Cost: measured, and quoted as the dearer of two readings

Three real edits, `openai/gpt-image-2`, server-default quality:

| Input | `input_tokens` (image + text) | `output_tokens` | Output size | `EDIT_COST` |
|---|---|---|---|---|
| 854x480 (16:9) | 608 (576 + 32) | 301 | 1672x941 | 0.013798 |
| 320x180 (16:9) | 273 (240 + 33) | 129 | 1672x941 | 0.005955 |
| 256x256 (1:1) | 289 (256 + 33) | 229 | 1254x1254 | 0.009083 |

The catalog publishes a `pricing.image` rate ($0.000008 for `gpt-image-2`)
separate from `pricing.prompt` ($0.000005), which is presumably what the
uploaded image bills at. That leaves two readings of the same numbers and no
invoice to settle them — 608×0.000005 + 301×0.00003 = 0.01207, against
32×0.000005 + 576×0.000008 + 301×0.00003 = 0.013798, **13% apart**.
`edit_cost_for()` returns the dearer, by the never-under-quote rule. Neither
reading has been reconciled against a console billing line, and note that
`image_cost_for`'s formula was only ever invoice-checked on *one* model on the
*other* endpoint, so nothing transfers here by assumption.

**Two findings that contradict what the generations anchors would lead you to
expect**, and both are why an edit estimate is matched on the input image
rather than on `(quality, size)`:

1. **Output geometry: a near-constant pixel budget, spent on the input's
   aspect ratio.** Three runs: 854x480 and 320x180 (both 16:9) returned
   1672x941, and 256x256 (1:1) returned 1254x1254. Those two output sizes are
   1,573,352 and 1,572,516 pixels — 0.05% apart — so the endpoint appears to
   target about 1.57 MP and choose the shape from the upload. Note that
   1672x941 is 1.777, the 16:9 the generations `size` enum *cannot express at
   all*: an edit reaches a ratio a generation cannot request.

   The third run was made during review, because the first two could not
   support the sentence that had been written from them. Both were 16:9, so
   "the output follows the input's ratio" and "the output is a fixed 1672x941
   for this model at this quality" fit the data equally well; only a different
   input ratio separates them. The conclusion survived — but it was an untested
   half of it until a 1:1 input was actually sent.
2. **Output tokens are not fixed by `(model, quality, output size)`.** Those
   three were identical across the two 16:9 runs and the counts were 301 and
   129. They track the upload instead, which is why the estimate is keyed on
   the input image's size. ~~Output tokens land at roughly half the input
   image tokens (0.523, 0.538)~~ — **withdrawn**: written as a pattern to test
   rather than a law, tested at 256x256, and false (229/256 = 0.895). It was
   never implemented as a formula, which is why it cost nothing to lose; had
   `print_edit_estimate` interpolated on it, every unmatched input size would
   now be quoted at about half what it bills. Input image tokens are not
   linear in input pixels either: 256x256 bills 256 tokens and 854x480, with
   6.3x the pixels, bills 576.

### An edit is verifiably an edit, not a redraw of the prompt

Worth stating because `STATUS completed` cannot distinguish the two, and an
endpoint that took an image and ignored it would look identical.

`openai/gpt-image-2`, an 854x480 UI screenshot in, prompt *"Change only the
blue Upgrade plan button to green. Leave every other pixel, all text and the
layout exactly as they are."* Every string in the source survived verbatim —
"Billing Settings", "$29.00", "Seats included 3" — which a text-to-image
generation from that prompt could not have produced. Against the rescaled
source, mean absolute difference was **5.27/255 overall but 84.27 inside the
button**, a region that is 1.1% of the frame and carried **58% of all pixels
differing by more than 40**. Replicated on a second input (a red square at
320x180 → the same square, same position, same size, blue).

## Error handling

### Correction: the error response *shape* was initially mis-assumed from doc prose, not just an unconfirmed code

This skill's original research documented `400 provider_type_unavailable` as
a "confirmed" `error.code` for a provider/model mismatch. **That was wrong**
— it was inferred from Ofox's doc prose describing the scenario in words,
never from an actual response body. A real rejected call (2026-08-29, an
invalid `extra_body.provider.type: "bogus_provider_xyz"` on `gpt-image-2` —
exactly the provider-mismatch scenario that prose was describing) returned:

```json
{
  "error": {
    "message": "unknown provider type: bogus_provider_xyz [ofox.ai]",
    "type": "invalid_request_error",
    "code": 400
  }
}
```

The real shape is `{"error": {"message", "type", "code"}}` — an
OpenAI-SDK-style convention, **different** from the video API's `{code,
message}` shape where `code` genuinely was a semantic string
(`insufficient_credits`, etc). Here, `error.code` is literally the HTTP
status **as a number** (`400`) — not a semantic string, and
`provider_type_unavailable` does not appear anywhere in the real response.
The real classifier is `error.type`. No `usage` field was present on this
rejected response (consistent with, but not 100%-certain proof of, rejected
requests going unbilled).

**On `/v1/images/edits`, `error.code` is not even reliably present.** It is
`404` for `model_not_found` and `400` for `endpoint_not_supported` — the HTTP
status again — but literally `null` on the two validation rejections (missing
image, unsupported mimetype), which instead carry a `param` field the
generations endpoint has never sent. So `error.code` is neither semantic nor
guaranteed, on either endpoint. `error.type` is the classifier; nothing in
`ofox-image.sh` branches on `code`.

`error.message` free text is not a stable contract to branch logic on — the
exact wording can change — but for this endpoint it remains the **primary**
source of diagnostic detail regardless of `error.type`/`error.code`.
`ofox-image.sh` always prints `error.message` (labeled `Upstream message:
...`) alongside `error.type` (primary classifier) and `error.code`
(reference only — usually just echoes the HTTP status here).

| HTTP | `error.type` | `error.code` | Meaning | Confirmed how |
|---|---|---|---|---|
| 400 | `invalid_request_error` | `400` (number, not semantic) | The request was rejected as malformed/unsupported — observed for an unknown/unsupported `extra_body.provider.type`; likely applies to other malformed-request cases too, not yet tested individually. | **Confirmed by a real call** (2026-08-29). |
| 400 | not recorded from the run | not recorded from the run | `openai/gpt-image-2` + `quality: standard` → `Invalid value: 'standard'. Supported values are: 'low', 'medium', 'high', and 'auto'`. Per-model, not endpoint-wide — `microsoft/mai-image-2.5-flash` takes `standard`. No image was produced and nothing was billed. See the `--quality` gotcha above. | **Confirmed by a real call** (2026-09-04). Only the HTTP status and the message were captured; `error.type`/`error.code` were not read off the body, so they are recorded as unknown rather than assumed to be the row above's. |
| 400 | `image_generation_user_error` | not read off the body | The request was rejected by the **safety system** before any image was produced. Seen on `openai/gpt-image-2`. Upstream message: *"Your request was rejected by the safety system"*, plus an Azure request id — and it names **no category**, so it does not tell you which clause did it. Nothing billed. The one trigger isolated so far is a single wardrobe word, `cropped` (as in `cropped jacket`) — most plausibly a sexual-content read, though the API states no category; it fired inside an anime-fight character frame, and what the session says about the rest of that frame comes in three strengths. **Cleared one at a time:** the school setting and the powers, each changed alone in a step that passed. **Not the cause, not cleared:** the weapons and the covered faces — dropping them, separately and then together, left the prompt refused, and no `gpt-image-2` call that passed has carried either. (A blade did get through on `microsoft/mai-image-2.5-flash`, which is a different filter — see the model subsection below.) **Untested:** the explicit ages and the blow-landing strike wording of the original refusal, which the bisect inherited already removed. Two repair paths, and the second is the one that gets forgotten: rewrite the offending clause (see the correction and the bisect procedure below), or **re-run the same prompt on `--model microsoft/mai-image-2.5-flash`**, which produced a bladed character sheet that `openai/gpt-image-2` had refused twice. | **Confirmed by a real call** (2026-09-06); trigger isolated by a five-step bisect the same day, ~0.037 USD. This is the second `error.type` ever observed on this endpoint; until now only `invalid_request_error` had been. |
| 400 | `endpoint_not_supported` | `400` | The model exists but does not serve the endpoint. Verbatim, on `qwen/qwen-image-3.0-pro` + `/v1/images/edits`: *"Model 'qwen/qwen-image-3.0-pro' does not support the /v1/images/edits endpoint on this platform. Please use /v1/chat/completions instead."* Fires **before** any parameter is looked at. Nothing billed. Supersedes the doc-prose-only claim this row used to carry ("Image editing is not supported for model"), which no real response has ever produced. | **Confirmed by a real call** (2026-09-15). |
| 404 | `model_not_found` | `404` | The model id does not exist. *"Model 'openai/definitely-not-a-model' not found"*. Nothing billed. | **Confirmed by a real call** (2026-09-15). |
| n/a (message-only, no distinct type/code documented) | — | — | `google/gemini-3.1-flash-image` + `n` param → errors. | Doc prose only, **not** confirmed by a real call. Prevented client-side by this script before any network call — should never actually be observed against the real API through `ofox-image.sh`. |

**Everything else is unconfirmed for this endpoint as of writing.** This is
deliberate, not an oversight — the research behind this skill had two
real error examples to go on (the provider-type one above, and the
`--quality standard` rejection of 2026-09-04, whose message was captured but
whose `error.type`/`error.code` were not), and inventing a full mapping (the way
`ofox-video-core`'s error table was built from many real, paid test calls
across `/v1/videos`) from that would mean guessing types/codes that might
not exist or might mean something different here. In this repo, "confirmed"
for an error field means **observed in an actual response**, not "described
in the vendor's doc prose" — the `provider_type_unavailable` mistake above is
exactly why that distinction matters. If you hit a new `error.type` (or a
value of `error.code` that isn't just the HTTP status) against the real
endpoint, add a row here and to `print_api_error` in `ofox-image.sh` — don't
guess ahead of that evidence.

### Correction: that refusal was blamed on the ages and on how the strike was written; the trigger was one wardrobe word

The row above used to say the retry passed because the prompt dropped its age
numbers, softened minor-coded wardrobe detail, and rewrote the strike as a
collision between two powers. Three things changed in one edit, so nothing was
isolated — the credit went to the two most plausible-sounding of them, and
neither has anything behind it.

A single-variable bisect on 2026-09-06 (`--quality low --size 1024x1024`,
~0.0075 USD per call) walked from a prompt known to pass toward the prompt
known to fail, changing one thing per step. **The prompt it started from was
the earlier retry that passed** — ages already removed, the strike already
written as two powers meeting — so neither of those two is under test in any
step below; every step inherits them:

| Step | The one change, relative to the step before | Result |
|---|---|---|
| Control | the passing prompt re-run unmodified | passed, 0.00751 USD — the filter itself had not moved |
| A | setting only: school corridor → rainy factory courtyard at night | passed, 0.007555 USD |
| B | powers only: water/fire → lightning/wind | passed, 0.00759 USD |
| C | the girl's hair and wardrobe swapped to the failing version (contains `cropped jacket`) | **refused** |
| D | one word of C: `cropped jacket` → `zip-up jacket` | passed, 0.007455 USD |
| E | D plus the anti-plastic texture paragraph (fabric, metal, light, exposure — no skin clause) | passed, 0.00778 USD |

C and D are byte-for-byte identical apart from that word. So the trigger is
`cropped` — a bare-midriff garment, so most plausibly a sexual-content read,
although the endpoint states no category and that part is inference — and it is
unrelated to the setting and to the powers, each of which was swapped on its own
in a step that passed. The weapons and the covered faces are a weaker result
and are worth keeping separate: they came out of the prompt one at a time and
then together during the guessing phase, and it was refused each time, so
neither is the cause on its own — which is a different statement from either
being safe, since no `gpt-image-2` call that passed has contained them. The one
passing call on record that kept a weapon was on `microsoft/mai-image-2.5-flash`
(below), a different model with a different policy, so it says nothing about
this one.

Reading back, the earlier retry that "worked" had also changed `black over-knee
socks` to `dark tights` in the same batch; that is the likelier cause of the
pass. The wardrobe edit was in
the old row's list of three, filed under "minor-coded" — the right lever,
credited to the wrong property of the garment. **The age numbers and the
rewritten strike have no isolating evidence in this repo either way** — they
may or may not matter, and the honest state is untested.

**What a refusal can and cannot establish.** A refused call shows that removing
whatever you removed was **not sufficient** to clear the refusal. It does not
show that anything still in the prompt is safe. Only a call that **passes**
does that, and only for the clauses that call actually carried. That asymmetry
is what both mistakes in this row's history have in common: a clause was
written up as exonerated on the strength of runs that either never contained
it, or never passed with it. When recording a result here, say which of the
three states it is in — cleared by a passing call that carried the clause,
shown insufficient by a refusal, or untested.

Two practical consequences for a caller. A wardrobe line is worth suspecting
first, ahead of the subject matter, when a character prompt is refused. And a
refusal here is about a phrase, not about the scene — the whole fight generated
fine once the jacket was described differently. That is the fight in the
wording every step inherited, though; the original blow-landing phrasing was
never put back, so it stays untested rather than cleared.

### When a refusal names no category, bisect rather than guess

All six refusals in that session returned the same string, word for word:
`Your request was rejected by the safety system`. No category, no offending
span, no severity. Six semantic guesses were made against that silence and all
six missed; the five written down afterwards were weapons, the covered face,
realistic combat versus fantasy powers, a rooftop parapet read as self-harm,
and wet clothing clinging to the body. The bisect above then found it in five
steps after the control, for about 0.037 USD billed with the refused step
costing nothing — roughly four cents of information against an afternoon of
theories.

So when a refusal carries no category, the cheaper move is to stop reasoning
about which clause offends and start from a prompt that is **known** to pass,
changing one thing at a time toward the target:

1. **Re-run the known-good prompt first.** This is the step that makes
   everything after it interpretable: if the control is refused, the filter has
   tightened and the differences you are about to test mean nothing. It costs
   one cheap call.
2. Move one dimension per call — setting, then action, then wardrobe, then
   style — and keep every other byte fixed.
3. When a step is refused, bisect **inside** that step's diff rather than
   reverting the whole step. C → D above was one word out of a wardrobe
   rewrite.
4. Run the cheap pair (`--quality low --size 1024x1024`) throughout; the filter
   reads the prompt, not the resolution, and the diagnosis transfers to the
   expensive settings you actually wanted.
5. Record the isolated word here. A trigger found and not written down costs
   the same money again.

Where this does not hold: it assumes the filter is deterministic for a given
prompt, which is untested — no prompt in that session was run twice to check
that a refusal repeats. Treat a single refusal on a borderline prompt as weak
evidence, and a refusal reproduced twice as the thing worth bisecting.

### A refusal is not only about the prompt — the model is a variable too

`microsoft/mai-image-2.5-flash` is a confirmed way past a `gpt-image-2` safety
refusal, and it was sitting unused for the whole six-refusal session above
because it had only ever been written down in a task record, not here. From
that earlier run: `openai/gpt-image-2` refused a character sheet holding a
blade twice with this same `image_generation_user_error`; removing the blade
passed, and **keeping the blade while switching to
`microsoft/mai-image-2.5-flash` also passed**. Two upstreams, two safety
policies.

So the repair menu for a safety refusal has two entries, not one: rewrite the
clause, or re-run unchanged with `--model microsoft/mai-image-2.5-flash`.
Switching costs about 2.0 cents against 0.6 cents at
`--quality low --size 1024x1024` (see the model chain in `SKILL.md`), which is
usually cheaper than the third rewrite. It is worth trying the switch early
when the thing being refused is something you would rather keep — a weapon, a
specific garment — and worth bisecting instead when you want to know what the
trigger was, since the switch tells you nothing about that.

## Billing on rejection — open question

Unlike `/v1/videos` (where a rejected create call is confirmed not to
create a billable job), whether a rejected `/v1/images/generations` request
is billed has **not** been confirmed with a real call. `ofox-image.sh`'s
documentation assumes the common pattern (no image produced, no charge) but
flags this explicitly as unverified.

Two rejections have been observed since that was written — the
provider-type one of 2026-08-29 (no `usage` field in the body) and the
`--quality standard` one of 2026-09-04 (reported as costing nothing) — and
both point the same way. Neither has been reconciled against a console
billing line, which is the only thing that would close this, so the question
stays open rather than being quietly marked answered.

## No free verification path

There is no job id and no poll endpoint for this API — every real call
that reaches `api.ofox.ai` either produces billed output or (assumed but
unconfirmed) is free because it was rejected before any image was made.
Unlike `ofox-video-core`, there is no "poll an existing job for free"
option to fall back on if a network call's outcome is ambiguous. If a
`generate` call gets no HTTP response at all (`ofox-image.sh` exit `5`),
the only way to find out what happened is to check
`https://app.ofox.ai`'s usage/billing history — there is nothing to poll
by id.

## The model list (`GET /v1/models`)

Public, keyless and free. `ofox-image.sh` uses it to check `--model`, and
exposes it as `ofox-image.sh models`.

**It does not describe image-model capabilities.** Unlike video models, which
carry a `video_attributes` object with real resolution/duration/aspect-ratio
limits, image entries have no `image_attributes` equivalent, and their
`supported_parameters` list is LLM-shaped (`temperature`, `top_p`,
`max_tokens`, `stop`, `response_format`) rather than the `size`/`quality`/
`background` this endpoint actually takes. So only the model **id** is
validated dynamically here; `--size`, `--quality`, `--output-format` and
`--background` stay hardcoded from the docs. Don't assume symmetry with
`ofox-video-core` — this was checked, and it isn't there.

What each entry does give us: `id`, `aliases`, `is_deprecated`,
`supported_endpoints` (so a video model passed to `--model` is caught with
that reason), and `pricing.output_image`.

Caching and fallback behave exactly as in `ofox-video-core`: fresh cache (24h,
`${XDG_CACHE_HOME:-$HOME/.cache}/ofox/models.json`) → live fetch → stale cache
→ bundled `references/models-snapshot.json` → no check. Every fallback below
"live" prints a NOTE to stderr. An id missing from a **live** list is rejected
locally; missing from a **snapshot** it is passed to the API, since the
snapshot may predate the model. `OFOX_SKIP_MODEL_VALIDATION=1` disables the
check. Regenerate the snapshot with `bash references/refresh-snapshot.sh`.
