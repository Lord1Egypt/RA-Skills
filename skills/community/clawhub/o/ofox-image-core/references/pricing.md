# Ofox image API pricing

Source: `https://ofox.ai/models/google/gemini-3.1-flash-image` (verified
2026-08-29 for the rate numbers below). Prices can change — re-verify
against the live model page before quoting a number you intend to hold
someone to.

## The rate that applies — settled against a real invoice

The model page states, for `google/gemini-3.1-flash-image` ("Nano Banana
2"):

| Item | Rate |
|---|---|
| Input tokens | $0.5 / M tokens |
| Output tokens | $3 / M tokens |
| Output image | $60 / M (units unclear from the page alone) |

The third row ("output image $60/M") used to be the open question: it could
have priced the image portion of `usage.output_tokens` at $60/M, or those
tokens could have billed as ordinary output at $3/M — a 20x spread.

**A real invoice line settled it on 2026-08-31.** A call reporting
`input_tokens=79, output_tokens=1120` was billed **$0.06723950**, matching
the $60/M reading to eight decimal places:

```
79 * 0.0000005  +  1120 * 0.00006
= 0.0000395     +  0.0672
= 0.06723950                       <- the invoice, digit for digit
```

So: **an image response's output tokens bill entirely at `output_image`, and
the `output` ($3/M) row does not enter into it.** The $3/M rate belongs to
this model's text-generation endpoint, not to `/v1/images/generations`.

## What to do instead

Every real response from `POST /v1/images/generations` includes a real
`usage` object:

```json
"usage": {
  "input_tokens": 14,
  "input_tokens_details": { "text_tokens": 14 },
  "output_tokens": 208,
  "total_tokens": 222
}
```

`ofox-image.sh` prints these three counts and, since the rate question was
settled, an `IMAGE_COST` line computed from them. It reads the rates from the
model list rather than hardcoding them, so a model with different pricing
gets its own figure. When no rates are available (offline, or a model missing
from the list) it prints no cost and says why — the token counts are always
exact, a computed cost is only as good as the rate table behind it.

**Key-name trap**: the two endpoints that publish rates disagree on spelling.
`/v2/models/catalog` calls them `input`/`output`; `/v1/models` — the list the
script actually loads — calls them `prompt`/`completion`. `output_image` is
spelled the same in both. Code reading either source must accept both.

**Which-model trap**: the rate lookup needs a model id, and the obvious place
to get one is the response's `model` field — but `openai/gpt-image-2` does not
send that field at all. The script used to default it to the literal string
`"unknown"`, look `"unknown"` up in the rate table, find nothing, and print
`could not compute a cost` for a request it had built itself. Two real, paid
calls were billed with no cost figure printed. Fixed in
`resolve_response_model()`, which keeps two cases deliberately apart:

| Response's `model` field | Id used for display and pricing | Reported as |
|---|---|---|
| absent / null / empty | the **requested** id | `MODEL_SOURCE request` |
| present, same as requested | the echoed id | `MODEL_SOURCE response` |
| present, **different** | the **echoed** id, plus a stderr warning | `MODEL_SOURCE response` + `MODEL_REQUESTED <asked-for id>` |

The third row is the one not to simplify away. A missing echo is silence and
means nothing was contradicted; a *different* echo means something upstream
routed, aliased or downgraded the request, and the invoice will follow the
model that actually ran. Rewriting it back to the requested id would compute
the cost off the wrong rate card and destroy the only evidence that the swap
happened.

## Verified real example

Real, paid, non-simulated call, 2026-08-29:

```bash
bash skills/ofox-image-core/references/ofox-image.sh generate \
  --model "google/gemini-3.1-flash-image" \
  --prompt "A simple red apple on a white table" \
  --quality low --size 512x512 --out-dir test-output
```

Result:

```
STATUS completed
IMAGE_PATH /path/to/your/project/test-output/ofox_image_20260829213234_6584.png
MODEL google/gemini-3.1-flash-image
SIZE 512x512
QUALITY low
USAGE_INPUT_TOKENS 8
USAGE_OUTPUT_TOKENS 1120
USAGE_TOTAL_TOKENS 1128
EXIT_CODE:0
```

**Size discrepancy found by inspecting the real file**: the response
claimed `"size": "512x512"`, but the actual downloaded PNG — verified with
`file` and `sips -g pixelWidth -g pixelHeight` — is really **1024x1024**.
`google/gemini-3.1-flash-image` appears to ignore the requested/echoed
`size` and always generate at its native 1024x1024 resolution. See
`references/api-params.md` and `SKILL.md` for the full gotcha writeup; the
point here is just that the token counts above are for a 1024x1024 image in
practice, not a 512x512 one, even though every field in the response said
otherwise.

**Cost**, using the formula confirmed on 2026-08-31:
`8 * 0.0000005 + 1120 * 0.00006` = **$0.06720400**. (When this example was
first written the rate question was open and this was recorded as "either
~$0.0034 or ~$0.067"; the invoice check confirmed the higher reading.)

### `mai-image-2.5-flash`'s own `SIZE` mismatch is three-way, not two

The Gemini gotcha above is a two-way mismatch: requested size vs. actual
size, with the response's echo agreeing with the request and both wrong.
`microsoft/mai-image-2.5-flash` — the model this task moved to second in the
chain — has a worse version of the same problem, found through three real,
paid calls made by a scenario skill built on this one (all requesting
`--size 1792x1024`): the response's own `SIZE` line, and the actual saved
file, and the original request each disagreed. Requested `1792x1024`,
response echoed `SIZE 1354x774`, saved file `1344x768` (ratio 1.75) — three
different numbers, not the two the Gemini case shows. Evidence: the `refs/`
entries of `content/ofox-cases/{anime-rooftop-confession,
yunqi-sparkling-ad, sneaker-motion-ad}/case.json` in the downstream
`home-page` project. Full writeup: `SKILL.md`'s `SIZE` gotcha section.

### `openai/gpt-image-2` honours `--size` exactly — and still needed a crop

The model now first in the chain does **not** have either problem above.
Measured 2026-09-04, one real, paid run at `--quality high --size
1792x1024`: the request, the response's own `SIZE` echo and the saved file's
real pixel dimensions all read **1792x1024**. All three agree, where Gemini
gives two numbers and `mai-image-2.5-flash` gives three.

**Honouring the request is not the same as producing a usable aspect ratio,
and that distinction cost a step anyway.** 1792x1024 is 1.75, not 16:9
(1.7778). The frame still had to be cropped to **1792x1008** before it could
be attached to a `bytedance/seedance-2.5` job, because attaching an image
forces `aspect_ratio: adaptive` — the video inherits the frame's own ratio,
so a 1.75 frame delivers a 1.75 clip whatever the video flags say.

So the standing rule holds for every model, and only the *size* of the
correction changes: **measure the delivered file and crop it, whichever model
made it.** What varies is how large the correction is — 16 pixels of height for
`gpt-image-2`, a whole different resolution for the other two. Cropping
only, never padding, so nothing is invented at the edges.

Since 1.6.0 that is a flag rather than a manual step: `--target-aspect W:H`
(or `--target-size WxH`) measures the written file and centre-crops it to
exactly the ratio asked for, failing loudly instead of delivering something
close. It does not change what anything costs — the price follows the `--size`
that gets requested, and the flag only decides *which* size that is, which is
why a dry run has to carry the same flag the real call will. See `SKILL.md`'s
"The size enum cannot express 16:9 or 9:16".

`qwen/qwen-image-3.0-pro` remains unchecked either way.

## Pre-flight estimates: the token anchor table

The formula above needs `usage.output_tokens`, which does not exist until the
response comes back. That is the whole asymmetry with the video side: a video
is priced per second and duration is an input, so a video job can be quoted
exactly before it is submitted; an image cannot.

`generate --dry-run` still has to print something, because the approval gate
requires a number or an explicit "no number, and here is why" — never a
figure the agent invented. What it prints comes from
`references/token-anchors.json`, the measured output-token count of a real
earlier call **with that same model**:

| Model | Measured at `--quality` / `--size` | Measured output tokens | When | Rough cost/image at today's rate | Invoice-checked? |
|---|---|---|---|---|---|
| `google/gemini-3.1-flash-image` | `low` / `512x512` — the one call whose flags were written down; this model ignores `--size` anyway | **1120** | 2026-08-29, 3 calls | ~6.7 cents | **yes** — see the invoice section above |
| `microsoft/mai-image-2.5-flash` | `low` / `1024x1024` | **1024** | 2026-09-02, 2 calls | ~2.0 cents | no — formula only |
| `openai/gpt-image-2` | `low` / `1024x1024` | **196** | 2026-09-02, 3 calls | ~0.6 cents | no — formula only |
| `openai/gpt-image-2` | `high` / `1792x1024` | **5063** | 2026-09-04, 1 call | **~15.4 cents** | no — the job's own reported `IMAGE_COST` |

The sample counts here must match `samples` in `token-anchors.json` — that file
is what the script actually reads, this table only explains it. When they
disagree, the JSON wins and this table is the stale one.

### The pair a row was measured at is part of the number

The second column is not decoration, and the two `gpt-image-2` rows are why.
**Measured 2026-09-04**: the same model that spends 196 output tokens at
`low` / `1024x1024` spends **5063** at `high` / `1792x1024` — 15.4 cents
against 0.6, about **26x**, from changing nothing but those two flags. That
run had been quoted to the user at 0.6 cents beforehand, because the anchor
row carried no record of the pair it came from and the script's lookup
(`.anchors[<model>].output_tokens`) never sees what the caller asked for.

**Fixed in 1.7.0** — raised with the repo owner the way
`token-anchors.json`'s `_what_the_count_does_depend_on` required, and
approved on 2026-09-05. The lookup now selects a measured point by
`--quality` and `--size`, and where the request's own pair has never been
measured it quotes the **dearest** point that model has, labelled `ROUGH
UPPER BOUND` and carrying the pair it borrowed from. Nothing is interpolated
between two points, and nothing is borrowed across models. So the earlier
instruction — "the honest number for a large high-quality frame is the
15.4-cent row, not the figure the script prints" — is now what the script
prints.

What that leaves for a human to know:

- **An omitted `--size`, and `auto` on either flag, take the upper-bound
  path**, because the API picks and no pair can be named in advance. A cheap
  `--quality low` call with no `--size` therefore quotes the 15.4-cent
  ceiling on `gpt-image-2`. That over-quotes on purpose: naming the pair
  (`--quality low --size 1024x1024`) is what gets the 0.6-cent figure back.
- **The ceiling bounds the output-token component only.** The prompt's input
  tokens have always been excluded from the estimate — a fraction of a cent
  on every observed call, and the reason a quoted ~0.1519 sits just under
  the 0.154035 that pair actually billed.
- **`mai-image-2.5-flash`'s 1024 carries the same pair caveat**, measured at
  `low` / `1024x1024` and nowhere else. A scenario skill made three real
  `1792x1024` calls with it (see the `SIZE` section above) and none of their
  token counts was recorded, so the count for that pair is unknown rather
  than assumed to be 1024 — which means a `1792x1024` request on that model
  quotes its single `low` / `1024x1024` point as a ceiling, and that ceiling
  is only a real ceiling if the count does not rise with size on this model
  the way it does on `gpt-image-2`. It probably does rise. Measure it before
  relying on the label there.

One constraint on measuring the missing pairs: **`openai/gpt-image-2` rejects
`--quality standard`** (HTTP 400 at submission, nothing billed — see
`api-params.md`'s error table), so its rows can only ever be anchored at
`low`, `medium`, `high` or `auto`. Since 1.7.0 the script enforces that
itself, so an attempt to measure the disallowed pair fails at `--dry-run`
rather than upstream.

The chain's **preferred** and **second** models (`gpt-image-2` and
`mai-image-2.5-flash`, in that order since the 2026-09-04 reorder — see
"Decision record: the chain was reordered on this finding" below) are both
measured, so a default `generate --dry-run` gives a rough number instead of
"cannot be predicted" — a number measured at `low` / `1024x1024` in both
cases, which is the whole subject of the subsection above. The
**"invoice-checked?"**
column is a separate, weaker-or-stronger claim than the token count next to
it — do not conflate the two:

- The **token count** (1120 / 1024 / 196) is an observation. It came straight
  out of a real response's `usage.output_tokens`.
- The **dollar figure** is that count run through the cost formula
  (`cost = input_tokens * pricing.input + output_tokens * pricing.output_image`,
  confirmed further down this page). The formula itself has only ever been
  checked against a real invoice line for **one** model,
  `google/gemini-3.1-flash-image` (2026-08-31, see above). For the other two
  rows, the dollar figure is what the formula predicts, not what a bill
  confirmed — `token-anchors.json`'s `cost_invoice_checked: false` says this
  explicitly for both. Reading the model page alone left the gemini rate 20x
  ambiguous before an invoice settled it; there is no reason to assume the
  other two vendors' pages are any less ambiguous, so treat their dollar
  figures as **formula-derived estimates**, not verified charges, until a real
  invoice line is checked against each one. Do not flip either `false` to
  `true` without one.

**Decision record: the chain was reordered on this finding.** `gpt-image-2`
uses 196 output tokens against `mai-image-2.5-flash`'s 1024 — so a single image
from `gpt-image-2` is **~3.4x cheaper** at today's rates, the opposite of what
a chain ordered by per-token rate implies. When the decision was taken it was
~4.5x, and `gpt-image-2`'s per-token rate was 15% *higher*; both of those moved
on 2026-09-15 when Ofox cut `mai-image-2.5-flash`'s `output_image` from
0.000026 to 0.0000195, which now makes `gpt-image-2`'s rate 54% higher and the
per-image gap correspondingly smaller. The direction of the conclusion is
unchanged — fewer tokens still beats a lower rate here — but the ratio is a
vendor's number, not ours, and it is quoted here with the date it was true.

On 2026-09-02, with this finding already in front of them, the repo owner
looked at both figures and deliberately kept `mai-image-2.5-flash` first —
see `token-anchors.json`'s chain-order history note for the reasoning at the
time, and its instruction that the next person who wanted to reorder the
chain should raise it first rather than doing it quietly.

**On 2026-09-04 the repo owner did exactly that** and asked for
`openai/gpt-image-2` first instead. `MODEL_CHAIN` in `ofox-image.sh` and the
chain table in `SKILL.md` now reflect that request. Cost was one input to
this decision, not the only one, on both occasions — the reasoning and the
date behind each call are the part worth keeping, not just the final order.

**Do not fill an unmeasured row by scaling another model's token count.**
Different vendor, different tokeniser, no reason to expect a similar count —
and a number derived that way is indistinguishable, in the table the user
approves, from one that was measured. One real call (a few cents) settles it;
nothing else does. Take `USAGE_OUTPUT_TOKENS` verbatim from the printed
output and update both the JSON file and this table.

### What the output-token count depends on — and does not

Measured 2026-09-02, on two prompts with nothing in common ("A simple red
apple on a white table" vs. "A wooden sailboat on a calm lake at sunrise,
wide shot"), both at `--quality low --size 1024x1024`:

| Model | Prompt | input tokens | output tokens |
|---|---|---|---|
| `microsoft/mai-image-2.5-flash` | apple | 14 | 1024 |
| `microsoft/mai-image-2.5-flash` | sailboat | 14 | 1024 |
| `openai/gpt-image-2` | apple | 14 | 196 |
| `openai/gpt-image-2` | sailboat | 14 | 196 |

Byte-identical `output_tokens` for two unrelated prompts, on both models.
Combined with `gemini-3.1-flash-image`'s three real calls (input tokens 8, 51
and 79, output tokens **1120 every time**), the working model is:

**`output_tokens` is fixed by model + size + quality. It does not depend on
prompt content, or on input token count.**

This is exactly what makes a single measured anchor usable for pricing a
*different* prompt later — if the count moved with what was being drawn, an
anchor measured on one prompt would say nothing about the cost of another,
and `--dry-run` would have no honest number to print at all. That said: **this
is two samples per model, not a proof.** It is a working model that has not
yet been contradicted, held with exactly that much confidence. If a future
call ever shows `output_tokens` moving with the prompt (or with `input
tokens`), that is a counterexample, not noise — record it in
`token-anchors.json` and stop trusting the anchor for that model.

`--size` was already known not to move the count for `gemini-3.1-flash-image`
specifically, because that model ignores `--size` outright (see the gotcha
above). What is new here is that content-independence holds across two
*different* vendors that do respect the requested size — so the size/quality
part of "model + size + quality" is doing real work, prompt content is doing
none.

**And "real work" turns out to be an understatement.** Measured 2026-09-04 on
`openai/gpt-image-2`: `low` / `1024x1024` spends 196 output tokens,
`high` / `1792x1024` spends **5063** — about 26x, on the same model, from the
two flags alone. One sample, and it moved **both** flags at once, so it does
not apportion the increase: the pixel count only rose 1.75x while the token
count rose ~26x, which points at `--quality` carrying most of it, but that is
an inference from a single run and not a measurement of either flag on its
own. What it does settle is that a token count quoted without its pair is not
an estimate of anything.

Even a measured anchor is labelled **ROUGH** when it is printed. It is one
model's observed count, not a promise, and it excludes the input-token
component (the prompt), which was a fraction of a cent on every call observed
so far. The exact figure is always `IMAGE_COST`, computed after the fact from
the response's own counts.

## Cost formula (confirmed)

```
cost = usage.input_tokens  * pricing.input/prompt
     + usage.output_tokens * pricing.output_image
```

Both rates come from the model list, per model — never hardcode them, and
never fall back to a guess when they are missing. `ofox-image.sh` implements
this in `image_cost_for()` and prints the result as `IMAGE_COST`.

### Evidence

| Date | input | output | Computed | Invoice |
|---|---|---|---|---|
| 2026-08-31 | 79 | 1120 | 0.06723950 | **$0.06723950** |
| 2026-08-31 | 51 | 1120 | 0.06722550 | (same batch, not itemised separately) |
| 2026-08-29 | 8 | 1120 | 0.06720400 | (not checked at the time) |

The 2026-08-31 row is the one that carries the argument: an exact eight-
decimal match is not a coincidence between two readings 20x apart.

Ofox exposes **no billing endpoint** — `/v1/usage`, `/v1/billing`,
`/v1/credits`, `/v1/account`, `/v1/balance` and their `/v2` equivalents all
answer 404. The invoice figure above came from the console at
`https://app.ofox.ai`. That is why the cost has to be computed client-side
from rates and token counts: there is nothing to query.

## Editing (`POST /v1/images/edits`) — a third term, and two readings of it

An edit bills something a generation does not: **the image you upload**. The
response says so directly, splitting the input for the first time:

```json
"usage": {
  "input_tokens": 608,
  "input_tokens_details": { "image_tokens": 576, "text_tokens": 32 },
  "output_tokens": 301,
  "output_tokens_details": { "image_tokens": 301 },
  "total_tokens": 909
}
```

576 of 608 input tokens were the picture. The catalog publishes a
`pricing.image` rate separate from `pricing.prompt` ($0.000008 against
$0.000005 for `openai/gpt-image-2`), presumably for exactly this. Which leaves
two readings and **no invoice to settle them**:

```
flat   = input_tokens * prompt_rate + output_tokens * output_image
       = 608*0.000005 + 301*0.00003                     = 0.01207
split  = text_tokens * prompt_rate
       + image_tokens * image_rate
       + output_tokens * output_image
       = 32*0.000005 + 576*0.000008 + 301*0.00003       = 0.013798
```

13% apart. `edit_cost_for()` returns the **dearer** and prints a NOTE saying
it did, by the never-under-quote rule — a table that errs high costs a
moment's surprise, one that errs low gets a bill approved that nobody agreed
to. When a model publishes no `pricing.image`, the two readings collapse into
one and the choice is moot.

**Do not let the generations formula's invoice check launder this one.** That
check (the table above) covers one model, on the other endpoint, with no
image-input term in it. Nothing about it transfers here. Both readings stay
unverified until someone reconciles an edit against a console line.

### Measured edits

| Date | Model | Input size | in (img+txt) | out | Output size | Computed |
|---|---|---|---|---|---|---|
| 2026-09-15 | `openai/gpt-image-2` | 854x480 (16:9) | 608 (576+32) | 301 | 1672x941 | 0.013798 |
| 2026-09-15 | `openai/gpt-image-2` | 320x180 (16:9) | 273 (240+33) | 129 | 1672x941 | 0.005955 |
| 2026-09-15 | `openai/gpt-image-2` | 256x256 (1:1) | 289 (256+33) | 229 | 1254x1254 | 0.009083 |
| 2026-09-16 | `openai/gpt-image-2` | 1792x1008 (16:9) | 1571 (1508+63) | 129 | 1672x941 | 0.016249 |

**The fourth row self-checks three ways**, which is worth stating because an
earlier version of this file wrongly recorded its output-token count as lost:
`1508+63 = 1571`, `1571+129 = 1700`, and

```
63*0.000005 + 1508*0.000008 + 129*0.00003 = 0.016249
```

— matching the run's own reported `EDIT_COST` to six decimals. Two sibling
edits of the same file on the same day billed 0.016289 and 0.016304, which
back out to 71 and 74 text tokens with the image and output counts unmoved:
the same "prompt length moves only the text tokens" behaviour the 320x180
replication shows.

⚠️ **Output tokens do not track the input size, and this row is what proves
it.** Ordered by input pixels the counts run **129** (320x180), **229**
(256x256), **301** (854x480), **129** (1792x1008) — not monotonic, and the
largest input ties the smallest for the lowest count. What *does* track the
upload is the input **image** token count: 240, 256, 576, 1508. So at large
input sizes the bill is dominated by the input term — `1508*0.000008 =
0.012064` is **74%** of this run's 0.016249 — and an estimate reasoning from
output tokens is reasoning from the smaller half.

🚨 **Worth raising before another point is added, and now with numbers rather
than in principle**: `print_edit_estimate` selects its "dearest" point by
`output_tokens` alone. Computed per point, the costs are 0.013894 (854x480),
0.006054 (320x180), 0.009182 (256x256) and **0.016438** (1792x1008) — so the
dearest point *by cost* is the one with the **equal-lowest** output-token
count, and the selector would pass over it. For any input with no exact match
the estimate therefore quotes 0.013894 as an "upper bound" over a point known
to bill 0.016438. That is invisible whenever an exact `input_size` match
exists, which is why it survived three points. **The selection key is the
thing to fix, not the data**, and per `_chain_order_history` a change that
moves a quoted price gets raised rather than made quietly.

Two things in that table are worth more than the dollar figures, because they
mean an edit anchor has a **different shape** from a generation anchor:

1. **A near-constant output pixel budget, spent on the input's aspect ratio.**
   The 16:9 inputs returned 1672x941; the 1:1 input returned 1254x1254.
   Those are 1,573,352 and 1,572,516 pixels — 0.05% apart — so the endpoint
   looks like it targets ~1.57 MP and takes the shape from the upload. 1.777
   is also the 16:9 that the generations `size` enum cannot express at all, so
   an edit reaches a ratio a generation cannot request.

   **The 2026-09-17 row is what makes this a budget rather than a floor.**
   The first three inputs were all *smaller* than the output, so "spends
   ~1.57 MP on the input's shape" and "upsamples everything to ~1.57 MP" fit
   them equally well. 1792x1008 is 1,806,336 pixels — larger than the output —
   and still came back 1672x941. The endpoint spends that budget in both
   directions. Same habit as the 1:1 run above: the sample that separates two
   readings is worth more than another sample that fits both.

   The 1:1 run exists because the first two could not establish this. Both
   were 16:9, and "output follows the input ratio" and "output is a fixed
   1672x941" explain two 16:9 samples equally well — the first was written
   down as the finding anyway. One cheap run at a different ratio (0.9 cents)
   settled it. Keep the habit: when every sample shares the value of the
   variable a claim is about, the claim is not yet measured.
2. **Output tokens are not fixed by `(model, quality, output size)`.** All
   three were identical across the two 16:9 runs; the counts were 301 and 129.
   The generation-side working model ("output_tokens is fixed by model + size
   + quality, not by what is being drawn") does **not** hold here. What the
   counts track is the upload, which is why `print_edit_estimate` keys on the
   input image's size.

   A second pattern from the same table has since been **withdrawn**: output
   tokens came to roughly half the input image tokens on both 16:9 runs
   (0.523, 0.538), which was recorded as a pattern worth testing rather than a
   law. The 256x256 run tested it: 229/256 = 0.895. Input image tokens are not
   linear in input pixels either — 256x256 bills 256 while 854x480, with 6.3x
   the pixels, bills 576. Nothing had to change in the script, because the
   pattern was deliberately never implemented as a formula; that decision is
   what made this a free correction instead of a systematic under-quote.

So `print_edit_estimate()` matches an anchor on the **input image's size**,
measured from the caller's own file, rather than on the `(quality, size)` pair
a generation is matched on. No match quotes the dearest point, labelled
`ROUGH UPPER BOUND`. Nothing is interpolated.

### Cheaper inputs are cheaper edits

A directly actionable consequence, and the only lever a caller has here:
downscaling the source from 854x480 to 320x180 took the bill from 1.4 cents to
0.6. If the job does not need the extra input resolution, do not pay for it.

The 1792x1008 point extends that in the other direction without making it
linear: **4.4x the pixels of 854x480 bought 2.6x the image tokens** (1508
against 576), 1.6 cents against 1.4. So the lever is real at both ends and the
ratio is not quotable at either.
