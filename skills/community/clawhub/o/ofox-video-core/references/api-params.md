# Ofox video API — parameter reference

Source: `https://ofox.ai/docs/api/videos` (verified 2026-08-29). Re-check the
live docs before relying on exact values far in the future — params and
pricing can drift.

This is the parameter surface `references/ofox-video.sh` builds a request
from. Use this table to decide what to pass; the script validates the
common mistakes (bad resolution, bad aspect ratio, out-of-range duration for
Seedance 2.5) before it ever calls the API.

## Create request fields (`POST /v1/videos`)

| Field | Type | Required | `ofox-video.sh` flag | Notes |
|---|---|---|---|---|
| `model` | string | yes | `--model` | Default `bytedance/seedance-2.5`. Run `ofox-video.sh models` for the live list with each model's limits and base price — 12 video models at last check (2026-09-14; it was 8 on 2026-09-02, so treat any count written here as a date-stamped observation, not a constant). |
| `prompt` | string | yes | `--prompt` | Text description of the video. |
| `duration` | integer | no | `--duration` | Seconds, any integer in the chosen model's range. The script enforces each model's real range (Seedance 2.5 4–30, Wan 3.0* 2–30, Wan 2.x 2–15, HappyHorse 3–15, Seedance 2.0* 4–15, **Hailuo 3 4–15**, Hailuo 3 Max 5–15), read from the live model list. Note Hailuo 3 caps at **15s**, half Seedance 2.5's ceiling — a duration a scenario skill picked for the default model may not fit it. |
| `resolution` | string | no | `--resolution` | Validated per model. Seedance 2.5 / Wan 3.0*: `480p` `720p` `1080p`. Seedance 2.0: also `4k` (lowercase, as the API reports it). Wan 2.x / HappyHorse: `720p` `1080p` only. **Hailuo 3: `768p` `2k` only; Hailuo 3 Max: `480p` `768p` only — neither has a `720p` tier at all**, so the `720p` default every scenario skill recommends is rejected locally on both. `2k` is valid (lowercase, on Hailuo 3 only); an uppercase `2K` and `1K` are advertised by **no** video model — an earlier version of this table listed both in error. |
| `aspect_ratio` | string | no | `--aspect-ratio` | Validated per model. Seedance 2.5 / Hailuo 3*: `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` `adaptive`. Wan 3.0*: the same minus `21:9`. Seedance 2.0*: `16:9` `9:16` `1:1` `adaptive`. Wan 2.x / HappyHorse: `16:9` `9:16` `1:1`. `3:2`, `2:3` and `9:21` are supported by **no** video model — an earlier version of this table listed them in error, and they were passing client-side validation only to be rejected by the API. **Attaching a frame changes this field per model** — see below; the script decides and prints a notice either way. |
| `size` | string | no | `--size` | `WIDTHxHEIGHT` (e.g. `1280x720`) — alternative to `resolution`. Don't send both unless you've confirmed the model accepts it; prefer `resolution` for Seedance 2.5. |
| `generate_audio` | boolean | no | `--generate-audio true\|false` | Default `true` server-side. |
| `seed` | integer | no | `--seed` | Ofox documents this as "deterministic generation". **Measured otherwise** — an identical request on a fixed seed returned visibly different clips, and one of three submissions failed outright. See the Seed section below before telling a user a take can be reproduced. |
| `frame_images` | array | no | `--frame-first-image URL\|PATH`, `--frame-last-image URL\|PATH` | Image-to-video via first/last frame. Accepts a remote URL (used as-is) or a local readable file path (auto base64-encoded into a `data:image/<ext>;base64,...` URI). The script builds the `{type, image_url, frame_type}` objects for you — pass either or both flags. |
| `input_references` | array | no | via `--extra-json` | ≤9 images, ≤3 audio clips (each ≤15s), ≤1 video. Element types are `image_url`, `audio_url`, `video_url` — see below. Not exposed as its own flag (structure is nested/varied) — pass `{"input_references": [...]}` through `--extra-json`. **Cannot be combined with `frame_images`** — the script rejects this client-side (`references_conflict`) if you try. **An `image_url` reference works and bills at the t2v rate** — measured 2026-09-16, and it is the `r2v` mode the catalog's `modes` list does not name; see the image section below, including an unexplained aspect-ratio observation. **An accepted `audio_url` does not become the clip's audio** — see the audio section below before building anything on it. |
| `real_person` | boolean | no | `--real-person true\|false` | Default `false`. Routes an **authorized** real-person reference image through Ofox's privacy-preserving preprocessing, which is otherwise refused by the upstream. Ofox documents this for `bytedance/seedance-2.0`, and a single-variable A/B on 2026-09-16 confirmed it lifts the refusal on `bytedance/seedance-2.5` too (byteplus, 480p, 4s, i2v). It is an **authorization mechanism for footage the user has the right to use, not a way past moderation** — see the real-person section below before offering it to anyone. |
| `callback_url` | string | no | `--callback-url` | Must be `https://` and must not point to a private network. |
| `provider` | object | no | `--provider SLUG` | Pins the upstream that serves the job. **Defaults to `byteplus` for `bytedance/seedance-*`** — see below. `--provider auto` sends no pin. `provider.options.<slug>` passthrough is not exposed as a flag; use `--extra-json`. |

`--extra-json` is merged into the built request body last (object merge —
its keys win over anything the flags set), so it's the escape hatch for any
field not exposed as a dedicated flag. It must be a valid JSON **object**; the
script checks both with `jq` before submitting.

### What `--extra-json` will not do (1.30.0)

Because it is merged *last* and *wins*, it could rewrite fields the script had
just validated and priced. Three refusals, all before any request:

| Input | Result |
|---|---|
| `--extra-json ""` written explicitly | error, exit 1. Omitting the flag is unchanged. |
| anything that is not a JSON object (`[…]`, `"s"`, `42`, `null`, `false`) | error, exit 1 — the merge is jq's `*`, which only works between objects |
| a key that has a flag: `model`, `prompt`, `duration`, `resolution`, `aspect_ratio`, `size`, `generate_audio`, `seed`, `real_person`, `callback_url`, `frame_images`, and `provider.type` | error, exit 1, naming the flag to use instead |

Everything else still passes straight through. `input_references` is the main
one, and **`provider.options` still works** — only `provider.type` is refused,
so `{"provider":{"options":{"byteplus":{…}}}}` merges alongside the pinned
type rather than replacing it.

The third rule is the one with money attached: `--duration 4 --resolution 480p
--extra-json '{"duration":30,"resolution":"1080p"}'` quoted 44 cents and would
have submitted a job billing about 7 dollars, because the estimate is printed
from the flags and the merge happens after it.

### 🚨 An empty `--extra-json` used to be treated as "not passed" — and a big `data:` URI produces one silently

**Measured 2026-09-17, fixed in 1.30.0.** The fix is the first row of the
table above; everything below is the reproduction, kept because the *cause* is
still live — `jq` still dies over `ARG_MAX`, it just cannot cost you a job
silently any more.

The validation was guarded by `if [ -n "$extra_json" ]`. An **empty string was
therefore indistinguishable from the flag never being passed**: no JSON check,
no `references_conflict` check, and **nothing merged into the body**. That is
fine when you meant to pass nothing. The problem is how easily you can mean to
pass something and hand over an empty string anyway.

The usual way: `--extra-json "$(jq -n --arg u "$REF" …)"` where `$REF` is a
`data:` URI built from a real photo. `jq` receives that URI **as a
command-line argument**, so it is bound by `ARG_MAX` (1,048,576 bytes on this
machine). Above the limit `jq` never executes at all — the shell writes one
line to stderr, the command substitution yields **empty**, and everything
downstream proceeds as though you passed no `--extra-json`.

Reproduced end to end with a 1.9 MB PNG (2,515,046-byte data URI):

```
(eval):10: argument list too long: jq
PAYLOAD {"model":"bytedance/seedance-2.5","prompt":"x","duration":8,
         "resolution":"720p","aspect_ratio":"16:9","seed":95234386,
         "provider":{"type":"byteplus"}}
STATUS dry_run
EXIT=0
```

**There is no `input_references` in that payload.** Exit code `0`. Dropping
`--dry-run` submitted a fully billed **plain text-to-video job** that the
caller believed was a reference-to-video job — nothing refused it, nothing
warned, and the delivered clip simply ignored the reference, which looks
exactly like the model "not following" the references.

**The one stderr line was the only signal, and it is easy to miss** — it is
emitted by the shell, not by this script, so it does not carry a script
prefix and it scrolls past above the normal output. That line is still the
only warning you get *before* the script sees the empty value; what changed in
1.30.0 is what happens next:

```
ERROR: --extra-json was given an empty value.
...
EXIT=1
```

**How to not get caught** (1 and 2 still matter — the script can only refuse
the job, it cannot make an oversized argument work):

1. **Build the JSON into a variable first, and check it is non-empty and
   parses**, before it ever reaches the command line.
2. **Keep the encoded image well under `ARG_MAX`.** Downscaling a reference to
   a 768 px long edge puts it in the tens of kilobytes; the measured r2v job's
   two references were 33 KB and 43 KB.
3. **`--dry-run --print-payload` and look for `input_references` in the
   payload with your own eyes.** Free, no network call, and it is the only
   check that actually confirms the field arrived.

```bash
EXTRA="$(jq -n --arg u "$REF" '{input_references:[{type:"image_url",image_url:{url:$u}}]}')"
[ -n "$EXTRA" ] && printf '%s' "$EXTRA" | jq -e . >/dev/null \
  || { echo "extra-json did not build — reference would be dropped silently"; exit 1; }
```

⚠️ **This does not apply to `--frame-first-image` / `--frame-last-image`.**
Those are the script's own job: it encodes the file through a temp file and
`jq --rawfile` / `--slurpfile`, so nothing large ever becomes an argument.
Verified on the same 1.9 MB PNG — the payload really carries the full
2,515,046-byte data URI. **The two paths behave in opposite ways at the same
file size**, which is precisely why the flag path is not evidence about the
`--extra-json` path.

**Script hardening for the empty-string case landed in 1.30.0** (this section
previously said it was deliberately not done, on the grounds that something
might rely on the old behaviour). What made it safe: the script now records
whether the flag was *written*, so "omitted" and "empty" stop being the same
input. Omitting `--extra-json` is byte-for-byte unchanged — asserted in
`references/test/keyguard.test.sh` by comparing the built payload against
`--extra-json '{}'` — and only the explicitly-empty spelling, which was never
anything but a failure, is refused.

## Reference inputs (`input_references`) and video-to-video

Element shapes, per the create-video docs and confirmed for video by a real
accepted request:

```json
{"type": "image_url", "image_url": {"url": "https://example.com/subject.jpg"}}
{"type": "audio_url", "audio_url": {"url": "https://example.com/voice.mp3"}}
{"type": "video_url", "video_url": {"url": "https://example.com/ref.mp4"}}
```

Note the type is `video_url`, **not** `video`. Getting that wrong is not
cosmetic: the cost estimate keys off it, and an earlier version of this script
guessed `video` and therefore quoted the t2v rate for a v2v job (estimated
$0.44, billed $0.56).

**A video reference must be a public web URL.** A small
`data:video/mp4;base64,...` value survived the core's JSON and payload path,
then the current route rejected it before job creation with HTTP 400
`invalid_request`: `reference_video must be provided as a web url`. The
rejected request created no job and was not billed. Unlike `frame_images`, a
local video therefore needs authorized public hosting before this route can
use it.

A working source, if the input is something this API produced: the
`unsigned_urls` link from a completed job. Verified 2026-08-31 — an
unauthenticated ranged GET returned `HTTP 206 video/mp4`, and the upstream
fetched it successfully. Those links are documented as temporary (may expire
within 24h), so this works for a fresh job, not an archival one. A public R2
object was also fetched successfully for the 2026-09-22 experiments below;
its unauthenticated ranged read returned `206`, `video/mp4`, 17,914 bytes.

The shipped core refuses `frame_images` together with `input_references` as
`references_conflict` before estimate or submission. Consequently a caller
using this script cannot combine a video reference with first/last-frame
anchors in one job. This is a client boundary; whether a direct request that
bypasses the core can combine them was not tested.

### An `image_url` reference works — this is `r2v`, and the catalog does not list it

**Measured 2026-09-16.** Until then `input_references` had only ever been sent
with `audio_url` (twice) and `video_url` (once); the image element type had
never been tried from this repo, and every model's
`video_attributes.modes` in the catalog lists `t2v` / `i2v` / `v2v` and
nothing else. The reference-to-video mode is real and the list is the thing
that is incomplete — do not read a missing `modes` entry as a missing
capability. (Do not hand-edit `models-snapshot.json` to "fix" it either; that
file is regenerated by `refresh-snapshot.sh` from the live catalog, so the
correction belongs here.)

Two probes, one free and one paid:

1. **A well-formed but unresolvable URL, free** — `HTTP 400`,
   `error.code: invalid_request`, upstream message `input_references[0]: url
   must be a public HTTPS URL (or data: URI): cannot resolve hostname: …`. The
   server parses the element, knows the type, and reaches DNS. It also names
   `data:` URIs, so **an image reference needs no hosting**, unlike a
   `video_url`. ⚠️ It still has to fit: see "An empty `--extra-json` is
   treated as 'not passed'" above — over `ARG_MAX` the reference is dropped
   silently and the job bills as plain t2v.
2. **Two real images as `data:` URIs**, job
   `0f5c8b4e-8813-40d2-a6bd-9e2d030b6d1e`, seed `638796173`,
   `bytedance/seedance-2.5` on `byteplus`, 4s / 480p, `generate_audio: false`,
   **billed $0.44**. `image1` was a vacuum flask (brushed steel body, copper
   knurled cap, a `KELVIN` wordmark), `image2` a hooded jacket (orange
   shoulder yoke, charcoal body, three orange zip pulls, a triangular sleeve
   patch). The prompt cast them by position: image1 the foreground flask,
   image2 the coat behind it.

Read off the delivered frames at 0.1s and 3.5s: every named feature of both
references is present — the knurled copper cap, the readable `KELVIN`, the
orange yoke against charcoal, all three zip pulls, the sleeve patch — and
**image1 rendered as the flask and image2 as the coat, not swapped**. So the
`image1` / `image2` position tokens are resolved to the attachments in array
order. That had been flagged as this repo's one unverified point about the
identity-reference shape (`prompt-structure.md` → "Identity-reference
example"); it is now a measurement.

Two more things from that job:

- **An image reference bills at the t2v rate** ($0.11/s at 480p): $0.44 for 4
  seconds, quoted and billed the same. It does **not** move the job to the
  video-to-video tier the way a `video_url` does (that is the
  estimated-$0.44 / billed-$0.56 trap recorded above).
- ⚠️ **An aspect-ratio observation nobody can explain yet, n=1.** Neither
  that job nor the plain text-to-video job run the same day passed
  `--aspect-ratio`. The t2v job delivered **854x480, landscape**; this one,
  carrying two **16:9 landscape** reference images, delivered **480x854,
  portrait** — matching neither the default nor the references. It is one
  observation of one job and no mechanism is offered for it here.
  `frame_images` behaves differently and is well measured (the output follows
  the attached frame). **Pass `--aspect-ratio` explicitly when you send image
  references**, rather than finding out afterwards what shape you bought.

What this does not cover: one job, one model, one upstream, 4s/480p, two
images. Nine images, an image mixed with an audio or video element, another
model, and whether the ordering rule survives more than two attachments are
all unmeasured.

### An `audio_url` reference is accepted, fetched, and does not become the audio

**Measured 2026-09-15**, because the field's own limits ("≤3 audio clips, each
≤15s", and a `too_many_references` error code that enumerates "3 audio") read
like a capability and nobody had ever sent one.

Two runs settle it:

1. **A well-formed but unresolvable URL, free** — a rejected create bills
   nothing. `HTTP 400`, `error.code: invalid_request`, upstream message
   `input_references[0]: url must be a public HTTPS URL (or data: URI):
   cannot resolve hostname: lookup … no such host`. So the server parses the
   element, knows the type, and got as far as **DNS resolution** — it tries to
   fetch the file. It also names `data:` URIs as acceptable, so audio needs no
   hosting, unlike a `video_url`.
2. **A real 5-second speech clip as a `data:` URI**, `bytedance/seedance-2.5`,
   job `d8561509-dcc6-4f2c-8864-a193cd239b14`, billed 55 cents. The job
   completed normally — **and the delivered audio track is not the audio that
   was sent.** Compared as RMS envelopes: the input is near-continuous speech,
   the output is sparse, correlation 0.41. The model generated its own track,
   as it does without any reference at all.

So the field is real, validated and fetched; what it is *for* is not what the
limits imply. Concretely:

- **Supplying a voice track and getting it spoken back (lip-sync) does not
  work here.** Not on this model, not through this field.
- **Putting a specific track on the delivered clip is a local mux**, not an
  API parameter: `ofox-video.sh mux-audio clip.mp4 track.mp3`. No call, no
  key, no cost. That is the whole of the answer to "can I supply the audio".
- Whether an audio reference influences *anything* — pacing, mood, cuts — is
  undecided. One run cannot separate "ignored" from "weakly conditioning", and
  the next run of the same request would differ anyway (see the Seed section).
- The catalog's `capabilities.audio_input: false` — `false` on every video
  model — described the outcome better than this parameter table did. When a
  capability flag and a parameter's documented limits disagree, the flag was
  the one worth believing, and it took 55 cents to find that out.

### What v2v did on a known-answer control

Ofox describes a video reference as “Guide subject / style
(reference-to-video), **not precise frame anchors**.” The two experiments here
do not turn that description into a universal frame-lock guarantee. They do
settle two narrower questions that the earlier motionless-cup run could not.

The input was a synthetic 4-second / 480p control with four one-second beats:
a three-bay frontal composition with a red marker moving right; a single-bay
close view with a blue marker rising; an overhead triangular layout with a
green marker moving side to side; and a right-bay view with a yellow marker
exiting right. Those independent composition and direction cues make replay,
reordering, and final-frame copying distinguishable.

Both jobs used `bytedance/seedance-2.5`, `byteplus`, 4 seconds, 480p,
`generate_audio: false`, and seed `314159265`. A dry run immediately before
each create quoted `$0.56`; each completed job billed `$0.56`. That agreement
is evidence for this measured parameter pair, not a permanent rate promise.

#### Structure-preserving rerender

Job `30c3e3e0-ec28-4988-91a2-95b440a24629` asked the model to treat the input
as exact previs, preserve order, timing, framing, layout and directions, and
replace the white-grid treatment with a dark industrial exhibition space.
Manual review of an 8fps contact sheet and frames around every transition found
all four compositions in order, all four motion directions preserved, no
added/reordered beat, and hard boundaries at exactly 1.0, 2.0 and 3.0 seconds.
That meets the pre-registered pass criterion for this control.

#### Continuation

Job `e15cdaef-c1b3-4a23-9ebc-4484be926a1b` described the input as preceding
footage rather than a shot list, required the opening to use the final
right-bay state, prohibited replay of the first three layouts, and asked for a
rightward exit into a newly revealed bay. The output opened from that final
state, the yellow object exited right, the camera revealed further/new bays,
and none of the first three layouts replayed. This is continuation evidence
for that prompt/control pair.

The prompt distinction is load-bearing: a rerender names the whole reference
as structure to preserve; a continuation names only its final state as the
starting point and explicitly prohibits replay. Neither result establishes
photoreal inputs, longer clips, 720p/1080p, another model or provider, several
video references, or simultaneous material/identity images.

The duration ceiling remains 4–30 seconds, and a continuation job returns a
new standalone clip rather than appending the source. `chain` remains the
better measured route for continuity across generated jobs when a frame anchor
is enough: it takes a local file and uses an actual extracted frame rather
than a soft video reference. Use a video reference when the temporal structure
or the source's final-state context is the information the prompt needs.

## `mode` is accepted and has no effect — extend and edit cannot be requested here

**Measured 2026-09-16.** The public Seedance gallery contains prompts run in
an `extend` mode (continue an existing clip past its own length) and an `edit`
mode (change what is inside footage that already exists). Both are written as
a `mode` field on the create request. This repo had been saying, from
inference, that Ofox "does not support" them. The measurement says something
more precise, and the difference matters to anyone debugging:

> **The `mode` field is accepted and discarded.** Job
> `4686f434-16b0-451f-8941-970e5b3d4a15` (seed `123884406`,
> `bytedance/seedance-2.5` on `byteplus`, 4s / 480p,
> `generate_audio: false`) sent `"mode": "this_is_not_a_real_mode_xyz"` —
> a value that cannot possibly be implemented anywhere — inside an otherwise
> ordinary text-to-video request. It returned **HTTP 200**, ran to
> `completed`, delivered a plain 854x480 / 4.04s t2v clip of a white cup on a
> table, and **billed $0.44 at the ordinary t2v rate**.

A garbage value cannot be honoured, so a normal completion is proof the field
was dropped rather than acted on. Whether Ofox never forwards it or the
upstream ignores an unknown key is invisible from here and makes no
difference to a caller: **the parameter does nothing.**

How to say this to a user, and how not to:

| ❌ Don't write | ✅ Write |
|---|---|
| "Ofox does not support extend / edit" | "Measured 2026-09-16 (job `4686f434`): the `mode` field is accepted but has no effect — an invented mode value returns 200 and bills as ordinary text-to-video. So extend and edit cannot be requested through this API" |

The first version implies an error the caller will go looking for and never
see. There is no rejection to catch, no error code to map, and nothing in the
response that differs from an ordinary job.

Three supporting probes, all free (a rejected create is never billed):

| Sent | Result |
|---|---|
| `mode: "extend"` with an unresolvable reference URL | `400`, the URL error only — `mode` triggered no validation |
| `mode: "edit"` with the same unresolvable URL | `400`, byte-identical to the above |
| `mode: "this_is_not_a_real_mode_xyz"`, same scaffold | `400`, **byte-identical to both real values** — the giveaway that nothing was validating the field |

Those three could not settle it on their own: "no validation error" is also
what a field forwarded to a stricter upstream would look like, because the URL
check fires first. Only the paid run above, with a value that could not
possibly work, separated "accepted" from "honoured". **A `200` is not evidence
of support when an unrecognised field is dropped rather than rejected** —
judge the artifact (here: the clip was exactly the requested length, where
`extend` would have produced source + N seconds).

**`duration: -1` fails differently, and earlier.** The gallery's official
`edit` case locks the output to the input's length with `duration: -1`. Sent
here it returns **`HTTP 502` `route_error`** — a different code from every
probe above, raised *before* any reference URL is fetched. So it breaks
routing rather than validation; it is not a usable way to ask for
input-locked duration.

**What to do instead**: extending footage is `chain`, or the frame-out /
generate / join route that the `video-extend-edit` scenario skill wraps (it
may not be installed alongside this one — it is a separate skill, not a file
here). Changing what is inside existing footage has no route through this API
at all — and that is now a measurement, not a guess.

## Upstream providers (`provider.type`)

A model can be served by more than one upstream. Ofox's own words for what
happens when you don't say which:

> When no `provider` field is sent, ofox distributes the request by weight
> across the channels currently serving that model — and which provider serves
> any single request is not predictable.

Re-measured 2026-09-14 across all twelve video models. **Run
`ofox-video.sh providers MODEL` rather than trusting this table** — it is a
dated observation, and the 2026-08-30 version of it is already wrong: every
`alibaba/*` model listed one upstream then and lists two now.

| Model | Upstreams |
|---|---|
| `bytedance/seedance-2.5` | `byteplus`, `volcengine` |
| `bytedance/seedance-2.0` | `byteplus`, `volcengine` |
| `bytedance/seedance-2.0-fast` | `byteplus`, `volcengine` |
| `bytedance/seedance-2.0-mini` | `byteplus`, `volcengine` |
| `alibaba/wan-2.6`, `alibaba/wan-2.7` | `alicloud`, `aliyun` — **two since 2026-09-14; was `aliyun` alone on 2026-08-30** |
| `alibaba/wan-3.0`, `alibaba/wan-3.0-prime` | `alicloud`, `aliyun` |
| `alibaba/happyhorse-1.0`, `-1.1` | `alicloud`, `aliyun` — **two since 2026-09-14** |
| `minimax/hailuo-3`, `-3-max` | `minimax`, `novita` |

This is the rot the "pin the upstream" spec predicted out loud: a model that
serves from one upstream today can serve from two tomorrow, at which point an
unpinned request starts routing by weight and any upstream-dependent
behaviour (moderation above all) becomes irreproducible without a `--provider`
pin. `ofox-video-core` pins only the `bytedance/seedance-*` family by prefix,
so `alibaba/*` and `minimax/*` requests are currently unpinned and route by
weight. Whether those upstreams differ in **moderation** has not been
measured — do not assume either way.

They do differ in **price**, on one model: `alibaba/wan-3.0` charges
`alicloud` 11 cents/s and `aliyun` 8.57 cents/s at 720p, a 28% spread
(measured 2026-09-14; every other model still matches across its upstreams).
An unpinned `wan-3.0` job can therefore be billed at either rate. The
estimate quotes the dearer card, so it does not under-quote — pin with
`--provider aliyun` if you want the cheaper one, and re-check this before
assuming any other model's upstreams price alike.

Tracked with the `minimax/hailuo-3` pinning question (Fizzy #841); nothing
here changes which models get pinned.

### The two that serve Seedance

| | `volcengine` | `byteplus` |
|---|---|---|
| Platform | Volcengine Ark — ByteDance's mainland China platform | BytePlus — ByteDance's platform for markets outside mainland China |
| Moderation | Standard | More permissive |
| Price | identical | identical |

**Pricing is identical across upstreams** — verified tier by tier
(480p/720p/1080p × t2v/v2v). Choosing one is a region, reliability and
moderation decision, never a cost one. Don't let anyone believe otherwise.

Because the two moderate differently, an unpinned job that fails
`output_moderation_failed` may simply have landed on the stricter upstream —
and the user has no way to tell which one they got. That is the main reason
this skill pins by default.

### What the script does

- **Default**: `byteplus` for `bytedance/seedance-*`. This is a prefix rule,
  not a lookup — the 4/4 measurement above makes it accurate, and it keeps the
  common path free of any network call.
- **Single-upstream models get no pin.** With one upstream, weighted routing is
  already deterministic; pinning would change nothing and would only add a
  hardcoded fact that can rot if the model later gains a second upstream.
- **Override**: `--provider volcengine` (mainland, standard moderation),
  `--provider auto` (no pin, back to weighted routing), or `OFOX_VIDEO_PROVIDER`
  for a persistent default. An explicit flag beats the environment variable.
- **Validation**: an unknown slug is rejected locally. A real slug that doesn't
  serve the chosen model is rejected too, naming the ones that do — but only
  when catalog data is at hand. If the catalog can't be reached, the request
  goes through with the pin as given; a check we couldn't run is never a reason
  to block a request (fail open).
- The chosen upstream is printed on the submit line, so it's never a mystery
  which one a given job used.

### Discovering upstreams (`GET /v2/models/catalog/...`)

Public and keyless, like the model list:

```
GET https://api.ofox.ai/v2/models/catalog/{owner}/{slug}?include=provider_price
```

Returns `provider_cards[]`: each upstream, its `provider_type`, and a full
`pricing.video_pricing.tiers[]` matrix of resolution × input_type × price.
`ofox-video.sh providers [MODEL]` prints exactly this. Cached for 24h next to
the model list, per model.

## The model list (`GET /v1/models`)

Public, keyless and free — verified by calling it with `OFOX_API_KEY` unset
(HTTP 200). `ofox-video.sh` fetches it to validate parameters against the model
the caller actually picked, and exposes it as `ofox-video.sh models`.

Each entry carries what the script needs:

```json
{
  "id": "bytedance/seedance-2.5",
  "is_deprecated": false,
  "pricing": { "output_video_per_second": "0.11" },
  "supported_endpoints": ["/v1/videos"],
  "video_attributes": {
    "modes": ["t2v", "i2v", "v2v"],
    "resolutions": ["480p", "720p", "1080p"],
    "default_resolution": "720p",
    "min_duration_seconds": 4,
    "max_duration_seconds": 30,
    "supports_audio": true,
    "aspect_ratios": ["21:9","16:9","4:3","1:1","3:4","9:16","adaptive"]
  }
}
```

**`pricing.output_video_per_second` is not a quote.** It is not consistently
the cheapest tier or the default-resolution tier: `seedance-2.5` reports
`0.11`, which is its 480p rate even though its `default_resolution` is 720p
(really $0.24/s); `seedance-2.0-mini` reports `0.04`, which *is* its 720p rate.
Use it to rank models by rough cost, never to tell a user what they will pay —
that comes from the per-resolution tables in `pricing.md`.

Caching: fresh cache (24h, `${XDG_CACHE_HOME:-$HOME/.cache}/ofox/models.json`)
→ live fetch → stale cache → bundled `references/models-snapshot.json` → no
per-model check at all. Every fallback below "live" prints a NOTE to stderr.
A model id missing from a **live** list is a local error; missing from a
**snapshot** it is passed through to the API, because the snapshot may simply
predate the model. `OFOX_SKIP_MODEL_VALIDATION=1` turns the per-model checks
off. Regenerate the snapshot with `bash references/refresh-snapshot.sh`.

## Image-to-video example (first frame only)

```bash
bash references/ofox-video.sh generate --approved \
  --model bytedance/seedance-2.0 \
  --prompt "Make the dog in the frame start running" \
  --duration 5 \
  --frame-first-image "https://example.com/dog.jpg"
```

A local file path also works and is preferred when available (see below):

```bash
bash references/ofox-video.sh generate --approved \
  --prompt "Make the dog in the frame start running" \
  --duration 5 \
  --frame-first-image "/Users/me/photos/dog.jpg"
```

### An attached frame and `aspect_ratio`: required on seedance-2.5, a default elsewhere

Verified against the real API: with the default model
(`bytedance/seedance-2.5`), attaching `frame_images` and sending any
`aspect_ratio` value other than `adaptive` fails — every documented
aspect ratio (or omitting it) was rejected across multiple real attempts,
while `adaptive` succeeded. That requirement is **specific to
`bytedance/seedance-2.5`**; `bytedance/seedance-2.0` does image-to-video
without it (verified separately, not assumed).

So `adaptive` means two different things depending on the model, and
`ofox-video.sh` keeps them apart. What it sends when a frame is attached:

| Case | Behaviour |
|---|---|
| `bytedance/seedance-2.5` | forces `adaptive`, **overriding** an explicitly-passed ratio — API requirement |
| another model, no `--aspect-ratio` passed | defaults to `adaptive` when that model's catalog entry lists it, so the clip follows the frame's shape |
| another model, `--aspect-ratio` passed | keeps the caller's value. Not an API requirement here, so overriding it would be overreach |
| catalog entry has no `adaptive`, or there is no entry | sends no `aspect_ratio` at all — never invents a value the model may reject |

Every one of those prints a `NOTE:` to stderr, including the ones where
nothing is added: the script never changes, or declines to change, an aspect
ratio silently. Support for `adaptive` is read from
`video_attributes.aspect_ratios` in the catalog described above — the same
cache → live → stale → snapshot ladder, no second hardcoded model list.

Until 2026-09-14 only the first row existed, so naming any other model with a
frame attached sent **no `aspect_ratio` field at all** and the frame's shape
could be quietly lost — a defect you paid for before discovering it.

⚠️ **None of the above is known to apply to `input_references`.** Every row
here is about `frame_images`. The one job run with image references and no
`--aspect-ratio` came back portrait from landscape references — see the
⚠️ under "An `image_url` reference works" — so pass the flag explicitly on
that path instead of assuming this table covers it.

**The converse is now confirmed too: with no image attached,
`--aspect-ratio` controls the output ratio exactly.** Verified 2026-09-05 on
a text-to-video job — `--aspect-ratio 16:9` delivered a file measuring
1280x720 — and again on 2026-09-06, job
`8efeb556-bf38-45ec-940b-a792ef74bfcf`, same flag, same 1280x720. That had
never been cleanly observed before those runs, because every earlier clip in
this repo attached a first frame and was therefore forced to `adaptive`,
where the ratio comes from the image and the flag does nothing. So the flag
is not merely accepted on the t2v path; it is effective, and it is the only
control over frame shape there.

**`--generate-audio false` removes the audio stream, it does not mute it.**
Those runs: the delivered mp4 carried **no audio stream at all**, rather than
a silent track — three times now, on every text-to-video clip this repo has
passed the flag on. Anything downstream that expects every clip to have an audio
stream to work with — a concatenation, an editor's timeline, a probe that
reads stream 1 — has to handle its absence rather than assume silence.

### Local file vs. remote URL reliability

Prefer a local file over a remote URL for `frame_images` when the user has
one. Real testing found a publicly reachable, valid image URL rejected by
the upstream provider with a download-failure-shaped error on more than one
attempt (likely bot/hotlink protection on that host), while the same image
base64-encoded from a local file worked reliably. The script handles the
encoding for you — just pass the local path.

## Poll response (`GET /v1/videos/{id}`)

States: `pending` → `queued` → `in_progress` → terminal (`completed` /
`failed` / `cancelled` / `expired`).

On `completed`:

| Field | Meaning |
|---|---|
| `mirror_urls` | CDN-signed, persistent — the script downloads from here when present. |
| `unsigned_urls` | Upstream original, temporary (may expire within 24h) — used by the script **only when `mirror_urls` is absent or empty**, which does happen on real completed jobs. Once downloaded, the file is local either way, so the expiry window doesn't matter after that. |
| `usage.video_seconds` | Billed duration. **Measured**: for a v2v job with a 4s input and a 4s output this was `4`, not `8` — the input video's duration is *not* added on top. (An earlier version of this table claimed it was; that claim was never measured and is wrong for this case.) The v2v *rate* still applies, which is where the extra cost comes from. |
| `usage.video_cost` | Actual cost, a string with 10 decimal places. The script prints this exactly — never estimate or invent a number here. |

## Listing recent jobs (`GET /v1/videos`)

**Measured 2026-09-16, and it corrects a claim this repo had been repeating:
there *is* a job list.**

```
GET https://api.ofox.ai/v1/videos          -> HTTP 200
GET https://api.ofox.ai/v1/videos?limit=5  -> HTTP 200
GET https://api.ofox.ai/v1/jobs            -> HTTP 404
```

Each entry carries `created_at`, `id`, `model`, `prompt`, `status`,
`unsigned_urls`, `updated_at` and `usage` — enough to tell whether a job
exists, what it is, and what it billed. It needs the API key, unlike
`/v1/models`.

The claim it corrects came from an earlier probe of `/v1/credits`,
`/v1/account` and `/v1/usage` — all 404 — from which this repo concluded there
was no programmatic way to check for a job at all. Those three really are 404;
`/v1/videos` had simply never been tried.

Two things this changes, and one it doesn't:

- **A transport fault on create is now diagnosable from the terminal.** See
  the no-resubmit rule below — this is the recovery step, and it is what the
  rule was missing.
- **A short filename id can sometimes be resolved after all.** The 8-hex stem
  on a downloaded file is a prefix of a real `id`, so listing and matching it
  works *for a job recent enough to still be on the list*. That is a
  convenience, not a guarantee, and the sidecar's full `job_id` is still the
  reliable record — do not stop writing one down because a list exists.
- **It is not a billing endpoint.** `/v1/usage`, `/v1/billing`, `/v1/credits`,
  `/v1/account` and `/v1/balance` all still answer 404
  (`ofox-image-core/references/pricing.md` records that, and it stands). Per-job
  `usage` on a list entry is not an account balance and must not be presented
  as one.

## Output filenames and the metadata sidecar

A completed download is written as `<slug>-<short job id>.<ext>`, plus a
`.json` sidecar with the same stem.

The slug comes from `--name` when the caller gives one, and otherwise from
the job's own `prompt`. The prompt is in every poll response, which is what
makes a bare `poll JOB_ID` in a fresh shell produce a readable name rather
than falling back to the raw id. `--name` is the better source whenever the
caller knows what the shot actually is — a prompt opens on setting and
lighting, so a prompt-derived slug tends to describe the room rather than the
scene.

Both sources are treated as untrusted path input: whitespace collapses to a
dash, control characters and characters illegal on Windows filesystems are
removed, non-alphanumeric runs are trimmed off both ends, and the result is
capped at 40 codepoints — sliced in `jq`, which cuts by codepoint, so CJK text
is never split mid-character regardless of locale.

The short id is 8 hex characters. It exists to keep two runs of the same
prompt from overwriting each other, **not** as a way back to the job: nothing
expands a prefix into a full id. `GET /v1/videos` (above) makes that *nearly*
recoverable — the stem is a prefix of a real `id`, so matching it against a
recent list usually works — but only while the job is still on the list, and
this file said flatly there was no list at all until 2026-09-16. Treat the
list as a rescue, and the sidecar as the record.

| Sidecar field | Source |
|---|---|
| `job_id` | Full id, the handle for `poll` and for reconciling against app.ofox.ai. |
| `status`, `model`, `prompt`, `created_at`, `updated_at` | The poll response. |
| `video_seconds`, `video_cost` | `usage.*` — the real bill, not an estimate. |
| `video_file` | Basename of the video this sidecar describes. |
| `name` | The `--name` given, when there was one. |
| `request` | The create payload as submitted. **Only on the generate path.** |

That last row is the one worth knowing. The poll response reports the model
and prompt but **not `resolution`, `aspect_ratio` or `seed`** — they are
echoed nowhere, so they reach the sidecar only through the create payload.

`generate` has that payload in hand. `create` does not hand it to the
`poll` that follows, because they are separate processes on purpose — that
separation is what stops a short tool timeout from stranding a billable job.
So `create` writes the compacted payload to `<out-dir>/.ofox-request-<job
id>.json`, and `poll` reads it, folds it into the sidecar, and deletes it
once the sidecar is safely written (not before — a failed download would
otherwise have nothing to retry from).

A missing handoff is normal, not an error: polling from a different
`--out-dir`, from another machine, or a job someone else created leaves
none, and the sidecar simply omits `request`, exactly as it did before
handoffs existed.

### Seed

Without `--seed` the script used to send none, leaving the server to pick one
and report it nowhere — so a take could not even be described after the fact.
`generate` and `create` now roll a seed when the caller doesn't supply one
(the same way `batch` always has), send it, and print it as a `SEED <n>` line.
It is random either way; choosing it client-side is what makes it recordable.

Between the seed and the handoff, a sidecar written by `generate`, or by
`create` + `poll` into the same `--out-dir`, holds everything needed to
re-submit the same request at a different resolution.

**The docs call this field "Deterministic generation". It is not, on this
API.** Measured 2026-09-15 on `bytedance/seedance-2.0-mini`, 4s / 480p /
16:9, seed `424242`, one byte-identical prompt, three submissions:
`2e45464c-9ea7-4836-96dd-93dffb5ef58d` and
`ef83ccb8-7147-416f-a4af-e2fb04a618d1` both completed and are visibly
different clips (the subject's position and its pixel area differ by 13x at
t=1s, and again at t=3s), while `cf877512-3faf-42b5-92ad-2e83fa55dabf` failed
`output_moderation_failed` on the same request and was not billed. So a fixed
seed narrows nothing you can promise a user; it records what was asked for.
Measured on that model at that tier — no model has ever been measured
reproducing a take here, including the ones this file previously implied did.

**A byte-identical prompt is necessary but not sufficient.** Two 2026-09-05
jobs on seed `642303335`, identical in every parameter and differing only in
one paragraph's wording, returned visibly different subjects rather than
different takes on one subject
(`1cf5ac46-058f-4615-a47b-067743f76f8c`, `50f623b2-c54a-4d9d-9646-31dd06e2a926`).
That run establishes *changed prompt → changed result*; it says nothing about
the converse, which the 2026-09-15 runs above tested directly and disproved.
The sidecar stores the prompt as submitted so a re-attempt does not depend on
anyone retyping it. `SKILL.md`'s "Re-attempting a shot" has the full
statement.

**Irreproducible content, reproducible dimensions — do not collapse the two.**
Everything above is about what the clip *shows*. The frame size it arrives at
behaves the other way: the same 720x480 (3:2) frame, fed to
`bytedance/seedance-2.5` at 480p in two independent jobs — `35b6aed1` and
`69bc799d` — delivered **794x530 both times**. So "you cannot get the same
clip twice" is true of the picture and false of its geometry, and an editor
planning a join can rely on the size while relying on nothing else. Output
dimensions come from the resolution tier and the frame's ratio; the input's
own pixel dimensions do not carry through.

`frame_images` is replaced by a `frame_images_count` — a resolved
`--frame-first-image` is a base64 data URI that can exceed a megabyte, and
that does not belong in a metadata file.

A sidecar that would be unparseable is discarded with a warning instead of
being left next to the video: a file that looks like a record but isn't is
worse than no file. The video is never failed over a sidecar problem.

## Error codes (`error.code`) and `error.message`

`error.message` free text is not a stable contract to branch logic on — the
exact wording can change — but it can carry a specific, useful detail the
generic mapped explanation doesn't (a real example: a minimum reference-image
width, seen in the message even though `error.code` was the generic
`invalid_request`). `ofox-video.sh` maps every documented `error.code` to
its own fixed, actionable message (see `print_error_message` in the
script), and **always** also prints `error.message` when present, labeled
`Upstream message: ...` — not only when `error.code` is absent/unrecognized.

| HTTP | `error.code` | Meaning |
|---|---|---|
| 400 | `invalid_request` | Missing/invalid parameter. |
| 400 | `invalid_callback_url` | `callback_url` not HTTPS or points to a private network. |
| 400 | `invalid_provider_type` | The provider slug is not one Ofox recognises. |
| 400 | `provider_type_unavailable` | A real slug, but it does not serve this model. `ofox-video.sh providers MODEL` lists the ones that do. |
| 400 | `references_conflict` | Both `frame_images` and `input_references` were sent. |
| 400 | `too_many_references` | Over the 9 image / 3 audio / 1 video reference limits. |
| 400 | `cancel_not_supported` | Upstream can't interrupt this job. |
| 400 | `cancel_failed` | Job already in a terminal state. |
| 401 | `unauthorized` / `invalid_api_key` | Bad or missing key. |
| 401 | `upstream_auth_failed` | Upstream provider auth error (Ofox-side routing issue). |
| 402 | `insufficient_credits` | Account balance too low to create the job. No charge is made. |
| 404 | `not_found` | Job id invalid or not accessible with this key. |
| 404 | `model_not_found` | Model unavailable. |
| 429 | `rate_limited` | Poll too frequently, or upstream rate limit. |
| 502 | `upstream_error` / `route_error` | Provider-side failure. `route_error` is also what a `duration: -1` returns (measured 2026-09-16) — raised before any reference URL is fetched, so an out-of-contract value can surface here rather than as a `400`. See "`mode` is accepted and has no effect" above. |
| 500 | `internal_error` | Platform-side failure. |
| 400 | `input_moderation_failed` | The **input** image/video was rejected before generation — most often a real person's face. Distinct from `output_moderation_failed` below: this happens at submission, so nothing was generated and nothing was billed. |
| n/a (seen on a terminal `failed` job, not a create-time HTTP error) | `output_moderation_failed` | The generated **output** failed a post-generation content check — happens *after* the job ran, not at submission, so it cannot be caught by client-side validation. Verified: the response's `usage` field is `null`/absent, so **this job is not billed**. Safe to retry with a brand-new `generate` call using a different prompt/reference — that's a new request, not a resubmission of the failed one. **The check covers the audio track as well as the picture**: job `1ff72400-0f30-4be1-a417-f52d43955d09` (2026-09-04) failed this way on a prompt that asked for a cello note and a bell chime, with `Upstream message: the output audio may be related to copyright restrictions`; dropping the music and keeping only recorded sound effects passed on the next run. See "Asking for music can fail output moderation on copyright" in `prompt-structure.md`. |

`real_person: true` image validation failures (checked when Ofox fetches
the reference image, not by this script): `bad_data_uri`, `download_failed`,
`unreachable`, `not_image`, `too_large`.

### Real-person reference images are refused by seedance-2.5 image-to-video

**Verified against the real API 2026-08-30.** Feeding a frame containing a
photoreal human into `bytedance/seedance-2.5` image-to-video returns:

```
HTTP 400  error.code: input_moderation_failed
Upstream message: The request failed because the input image 'content[1]'
may contain real person.
```

Nothing is generated and nothing is billed. This is a **submission-time**
rejection, unlike `output_moderation_failed` which happens after a job has
already run.

**The rule is about the attached picture, not about the video's content.**
That distinction is easy to lose and expensive to lose, because losing it
rules out work the API is perfectly happy to do. Measured, all on
`bytedance/seedance-2.5` via `byteplus`:

| What | Status | Evidence |
|---|---|---|
| A photoreal person **in the attached frame** | refused at submission, nothing billed | verified 2026-08-30, the response above |
| A **non-photoreal** character in the attached frame | fine | job `16023efe-48d6-45fe-8fd8-f5c6fbfe6519` — an anime pair as `--frame-first-image`, 20s 720p, completed and billed $4.80 |
| A photoreal person **generated from the prompt text**, no image attached | fine | five text-to-video jobs of 20–30s built entirely around photoreal people, all completed: `844c9145-9b10-4335-9fdc-ec4937793a2f`, `4e5c9581-d462-443b-9663-b1aa6d72f527`, `41f87ac7-d7a6-4c8c-8efd-feb7bdc4818d`, `036ac3a8-6f68-47ad-a553-86a29aa3e5b8`, `38ca8311-5b2d-47d5-a45d-e8ebea0e6312` |
| A photoreal person **generated from the prompt text, in a job that also attaches an object-only frame** | fine | job `ac927785-92ef-4e28-97b9-ff8172ec5554` — first frame holds a product with no person, no foot and no sock in it; a model enters from 4s and stays in frame for seven or eight seconds; 20s 720p, completed and billed $4.80 |

So the productive route for "this exact product, and a person using it" is
the last row: **attach a frame of the object alone so it passes input
moderation, and write the person in the prompt text.** The object's
appearance is locked by the frame; the person is generated freshly, which is
allowed. `seedance-ad-creative` states this as its own route with the
framing discipline that goes with it.

The rest of what this means in practice:

- Any workflow that carries a photoreal human **between shots** — chaining a
  short-drama sequence, reusing a live-action character reference as a frame
  — still hits this wall on Seedance 2.5. Cross-job consistency for a
  live-action character stays text-only.
- Non-photoreal references are unaffected — illustration, anime, product
  shots, landscapes. That is why `seedance-anime-drama`, which reuses a
  generated anime frame, works; the measurement is the second row above.
- `real_person: true` exists precisely for authorized real-person references
  and routes them through Ofox's privacy-preserving preprocessing. **On
  `bytedance/seedance-2.5` it does lift this refusal — measured 2026-09-16,
  the next section.** What it is *for* has not changed, and that is the part
  that matters: it is how a caller asserts a right to use a likeness, not a
  way past the check.

The script maps `input_moderation_failed` to this explanation and names both
options rather than leaving a bare error code.

### `--real-person true` lifts that refusal on 2.5 — for references you are authorized to use

**This is the section other skills should link rather than restate.**

**Measured 2026-09-16 as a single-variable A/B.** The same synthetic
portrait, the same prompt, the same parameters (4s, 480p, image-to-video via
`--frame-first-image`), the same upstream (`byteplus`), submitted twice and
differing only in the flag:

| Request | Result | Billed |
|---|---|---|
| **with** `--real-person true` | job `28eee177-1eab-4852-a72f-d6a2de695672` completed, seed `311954977`, and the delivered clip is the person in the portrait | 44 cents |
| **without it** | `HTTP 400`, `error.code: input_moderation_failed`, upstream message "The request failed because the input image 'content[1]' may contain real person." | nothing |

The control run is the whole point. With only the accepting run there are two
explanations that produce identical evidence — the flag worked, or that
particular portrait never tripped the classifier in the first place. The
control was refused, so the flag is the only variable that moved. And a
refused create bills nothing, so the control cost nothing to run. (This repo
has been burned by the other shape before: see the Seed section, where a
tested proposition was written up as its untested converse.)

#### What the flag is, and what it is not

Ofox's own characterisation, quoted from the error text the API returns:

> `--real-person true`, which routes through Ofox's privacy-preserving
> preprocessing for **AUTHORIZED** real-person references.

It is an **authorization mechanism, not a moderation bypass.** The refusal
asks, in effect, whether the caller has the right to use this person's
likeness; the flag is how a caller asserts that they do, and the upstream
then handles the reference through a preprocessing path built for that case.
Setting it on material the user has no right to use does not make the use
legitimate — it makes a false assertion and then generates the clip, which is
a worse outcome than being refused.

Practically, for any skill that surfaces this:

- **Offer it only when the user has confirmed they may use that likeness**,
  and say what it means while offering it. "You have the rights to this
  person's image" is the precondition, not a formality to skip past.
- **Never write it as "the flag that gets a portrait past the check"**, and
  never reach for it as a reflex retry after `input_moderation_failed`. A
  refusal is not an error to route around.
- **Never set it on the user's behalf** to make a job go through.
- **An identifiable public figure is out regardless.** The flag asserts
  authorization; it cannot create it.

#### What that run does not establish

One A/B is one A/B. All of the following are untested here, and none of them
may be implied:

- **One upstream.** `byteplus` only. `volcengine` was not tried, and the two
  are documented above as moderating differently — so this is byteplus's
  verdict, not the platform's.
- **One tier, one mode, one length.** 480p, 4 seconds, image-to-video with a
  single first frame. Nothing here covers 720p or 1080p, longer durations, a
  last frame, or a real-person image sent through `input_references`.
- **One content class — a *synthetic* portrait.** It was generated for the
  test (the same method as the 2026-09-14 comparison) precisely so that no
  real person's likeness was involved. It trips the same classifier, which is
  what makes it a valid control; it is **not** evidence about how an actual
  photograph of an actual person is handled.
- **Fidelity under preprocessing is unmeasured.** The delivered 480p clip is
  recognisably the same person, and that is all that was checked. Whether the
  privacy-preserving preprocessing softens a likeness at a tier where it would
  show, nobody has looked.
- **One model.** `bytedance/seedance-2.5`. Ofox documents the flag for
  `bytedance/seedance-2.0`; every other model is untested here, including the
  ones scenario skills currently route portraits to.

## The no-resubmit rule

Once a create call gets any HTTP response, that job exists (or was
definitively rejected). `ofox-video.sh` never issues a second create call
for the same invocation:

- **Create call times out / connection error with no HTTP response at all**
  → the script exits `5` and refuses to guess. It genuinely cannot tell
  whether the job was created server-side. **List the recent jobs and look**
  — `GET /v1/videos`, below — then retry manually only if nothing new is
  there. `https://app.ofox.ai` shows the same thing in a browser.
- **Create call gets an HTTP error response** (4xx/5xx with a real body) →
  no job was created (the request was rejected), so fixing the parameters
  and retrying `generate` is safe.
- **Polling is slow, a poll request errors, or the script's own poll loop
  hits its time budget** → the job was already created and is running. The
  fix is `ofox-video.sh poll JOB_ID`, never a new `generate` call for the
  same request — resubmitting creates a second, separately billed job.

**Third bullet, observed rather than reasoned, 2026-09-05 and 2026-09-06.**
Three jobs lost their TLS connection mid-poll (`curl: (35) LibreSSL
SSL_connect: SSL_ERROR_SYSCALL in connection to api.ofox.ai:443`), the script
retried the poll — not the create — after six seconds, and all three
completed normally with their videos downloaded:
`1cf5ac46-058f-4615-a47b-067743f76f8c`,
`50f623b2-c54a-4d9d-9646-31dd06e2a926` and
`8efeb556-bf38-45ec-940b-a792ef74bfcf`, 2.88 USD each. The connection broke;
the jobs never did. Before 2026-09-05 this rule had never been exercised by a
live transport fault at all, and a resubmit at any of those three moments
would have doubled a 2.88 USD spend on a fault that cleared by itself in six
seconds. `SKILL.md`'s "The rule has now survived a real transport fault"
carries the same record.

**First bullet, exercised 2026-09-16 — and this is where the job list earns
its place.** A `create` lost its connection with no HTTP response at all
(`curl (35)` again), so the script exited `5` and refused to guess, correctly.
Previously that was the end of the line from the terminal: the only next step
on offer was "open the dashboard". Instead, `GET /v1/videos` was listed, the
newest entry was still a job from hours earlier, and that settled it — nothing
had been created, so retrying was safe rather than a coin flip. **List,
compare, then decide** is now the documented step, and it strengthens the rule
rather than loosening it: the reason never to blind-retry was that nobody
could tell, and now somebody can.

Three `curl (35)` events happened in that one session — one on a create, two
on polls. The transport layer of this API is genuinely flaky, which is the
best argument that neither the no-resubmit rule nor its recovery step is
over-engineering.
