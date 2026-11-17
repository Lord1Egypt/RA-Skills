# Changelog

All notable changes to the **ofox-image-core** skill. Versioning follows SemVer.

This file starts at 1.1.0; earlier versions predate it.

## 1.14.0 — the API key goes to one host, and neither escape hatch can reach past its own job

Three guards, each narrowing a capability this script really had rather than
removing it. New suite: `references/test/keyguard.test.sh` (66 checks), which
constructs the refused input for every rule instead of watching a good input
pass. Written alongside the same change in `ofox-video-core` 1.30.0.

### `--extra-form` will not read local files

`--extra-form K=V` goes straight into curl's `-F`, where a **value** starting
`@` uploads that local file and one starting `<` sends that file's contents as
the field value. `--extra-form "mask=@$HOME/.ssh/id_rsa"` therefore worked:
any file the user could read, uploaded to whatever `API_BASE` points at. The
field name was never the issue, so the rule is on the value.

Both prefixes are refused (exit **1**, before the request). Unaffected: every
ordinary pair, including `k=user@example.com`, `k=a<b` and `k=` — only a value
*starting* with the character is refused. Also unaffected are the script's own
`-F "image=@PATH"` and `-F "image_url=<TEMPFILE"`, which are built from
`--image` / `--image-url`, not from this flag; both are asserted still working
in the new suite.

**What a caller has to do differently:** send images with `--image` or
`--image-url`. And the standing suggestion to try a mask with
`--extra-form "mask=@FILE"` — in `SKILL.md` and `references/api-params.md` —
is withdrawn: masked edits were never established, and establishing them needs
a flag with its own path validation, not a general file-upload hole left open
for the one field that might want it. Both documents now say so.

### `--extra-form` cannot overwrite a field that has a flag either

The value rule above closed the file-read. The **key** rule was the older one
and had gone stale: it refused `image`, `image_url`, `model` and `prompt`
while the same function also builds `quality`, `size`, `n`, `output_format`
and `background` from flags. Those five were reachable, and a second multipart
part with an owned name is not a harmless duplicate — the server picks one of
the two, the value that arrived this way skipped the flag's own validation
(`--quality` is checked per resolved model), and it is appended **after**
`print_edit_estimate` has been computed from the flags.

`n` is the sharp one, because it multiplies the bill. Measured on the dry-run
path before the fix:

```
$ ofox-image.sh edit --image in.png --prompt p --extra-form "n=10" --dry-run
Estimated cost: ROUGH UPPER BOUND ~$0.0164 ...
N 1
FORM_FIELDS image model prompt n
```

One image quoted and reported, ten requested. That is the never-under-quote
rule broken through the escape hatch — the same defect `--extra-json` is
refused for on the generations side, which the comment above it already
claimed this path covered.

All nine owned keys are refused now (exit **1**, before the request and before
the quote). `--extra-form` keeps working for every field with no flag of its
own; a name that merely *contains* an owned one (`n_hint`, `mask_hint`,
`size_note`, `background_music`) is a different field and still passes.

**What a caller has to do differently:** pass `--quality`, `--size`, `--n`,
`--output-format` and `--background` as flags. Sent through `--extra-form`
they now exit 1 instead of quietly changing what was billed.

The test derives the list of owned keys from the script's own `form+=` lines
rather than restating it, and asserts the count, so a flag added without a
matching guard entry turns the suite red with no edit to the test —
`falsifiable-gates.md`'s "the check and the code share one wrong premise" is
exactly how the original four-name list survived review.

### `--extra-json` cannot overwrite a field that has a flag, and cannot be empty

It is merged **last** and its keys **win**, while the cost estimate is printed
**before** the merge — so `--quality low --extra-json
'{"quality":"high","size":"1792x1024"}'` quoted ~0.6 cents for the request
that measured **15.4** cents.

Refused now (exit **1**, before any request):

- `model`, `prompt`, `quality`, `size`, `n`, `output_format`, `background` —
  every field that has a flag. The error names the flag to use instead.
  **This widens one existing rule**: an `n` key in `--extra-json` used to be
  refused only for `google/gemini-3.1-flash-image`, and is now refused for
  every model. The narrower branch was removed rather than left as a check
  that could no longer run.
- an explicitly empty value. The script now records whether the flag was
  *written on the command line*, which is the one thing bash cannot recover
  from the value; omitting it is byte-for-byte what it always was, asserted
  against `--extra-json '{}'` in the new suite. An empty value is never
  anything but a failed command substitution, and it used to mean *every check
  skipped and nothing merged* — the request went out and billed without the
  fields the caller meant to add. (Measured on the sibling video script,
  2026-09-17; the same guard shape existed here.)
- anything that is not a JSON **object**. The merge is jq's `*`, undefined
  between other types: a non-object made the merge fail, the command
  substitution yield an empty payload, and an empty body go out. Validity is
  also now checked with `jq empty` rather than `jq -e .`, which keyed its exit
  status on the *output value* and so reported a valid `null` or `false` as
  "not valid JSON".

Unaffected: `extra_body.provider.type`, and any other field with no flag.
`--extra-json` is also merged through a temp file and `--slurpfile` now
instead of `--argjson`, so a large value is not bounded by `ARG_MAX`.

### `OFOX_API_BASE_URL` must be https, and an override is announced

Still supported — a staging deployment is a legitimate use — but it decides
which host receives the key:

- a non-`https://` base is refused (exit **2**) unless the host is loopback
  (`localhost`, `127.0.0.1`, `[::1]`), which keeps local test servers working;
- a value that is not an http(s) URL at all is refused (exit **2**);
- when it is set, a `NOTE:` on stderr names the host that will receive the
  key. **Relay that line.**

There is no polling-URL counterpart to the video skill's matching fix here,
and that is checked rather than assumed: the new suite asserts that both
authenticated requests are still built from `$API_BASE` and that no URL from a
response body is ever fetched.

### The "`ofox-video-core` isn't installed" paragraph matches the scenario skills again

`SKILL.md`'s approval-gate probe ended by naming `npx skills add
ofoxai/skills` — the whole repo — while the 14 scenario skills were narrowed in
the same uncommitted change to ask for the **one** missing skill and to hand
the command to the user rather than run it. It now says the same thing they do:
one skill, three routes (skills.sh / `npx ofox-skills` / LobeHub-ClawHub), the
user runs it. No behaviour change; `ofox-video-core` 1.30.0 carries the
matching fix for its two shared reference files.

## 1.13.1 — the edit estimate's "upper bound" could be below a known real bill

**Code fix in `references/ofox-image.sh` (`print_edit_estimate`), plus the
test that would have caught it.** Behaviour changes only on the **unmatched**
path; an exact input-size match quotes exactly what it quoted in 1.13.0.

**The defect.** When no measured point matches the request's input size, the
script quotes the dearest one as a `ROUGH UPPER BOUND`. It chose "dearest" by
`output_tokens`. An edit's bill is
`output_tokens x out_rate + input_tokens x img_rate`, and at large input sizes
the second term is most of it — 1508 image tokens is **74%** of the 1792x1008
run's $0.016249. The four measured points run **129 / 229 / 301 / 129** output
tokens and **0.006054 / 0.009182 / 0.013894 / 0.016438** in money, so the
genuinely dearest point has the *equal-lowest* output count and the old key
walked straight past it.

**What a caller has to do differently:** nothing, but re-read any cost table
built from an unmatched edit quote on 1.13.0 or earlier. Measured on a
1400x787 input:

```
before:  ROUGH UPPER BOUND ~$0.0139   (854x480 point)    <- below a known bill
after:   ROUGH UPPER BOUND ~$0.0164   (1792x1008 point)  <- correct
```

A bound that is not the largest known value is not a bound, and this one was
**below a figure this repo had already been billed**. The never-under-quote
rule exists for exactly this.

**Why it survived four anchors: the test was wrong in the same place as the
code.** `edit.test.sh` asserted the unmatched case quotes `301 output` and
never `129 output` — encoding the identical premise that dearest means most
output tokens. When the 1792x1008 point landed the assertion **inverted**, and
began requiring the cheaper point and forbidding the dearest, the exact
opposite of the intent in the comment above it. It had passed all along. A
check cannot catch a bug it also contains.

The assertion is now expressed in **money and derived from the data at run
time** — it computes the dearest measured point's real cost from
`token-anchors.json` and the rate card and asserts the quoted figure is `>=`
it. No token count and no dollar figure is hardcoded, so a fifth anchor keeps
it correct with no edit; swapping one constant for another would only have
moved the mine. Verified by planting the defect: with the key reverted to
`output_tokens` the suite reports

```
FAIL  an unmeasured input was quoted BELOW a known real bill
      quoted=0.0139 dearest=0.016438
```

and returns to `passed: 50  failed: 0` when the fix is restored.

**The `generate` path was audited and does not have this shape.** A
generation's cost is `output_tokens x rate` — one term, rate constant per
model — so "most output tokens" and "dearest" are the same ordering by
construction. Confirmed live: an unmatched generate request quotes the 5063
point at `~$0.1519`, the dearest it has. A comment in `print_estimate` now
records that this was checked, and that it stops being safe if a per-point
rate is ever introduced.

Also refreshed: the `UPPER BOUND` explanation printed to the user still listed
only three input sizes and their pixel/token ratios. It now carries all four,
both ratio comparisons, and the reason the selector uses cost rather than
output tokens.

## 1.13.0 — 1.12.0 was wrong: the anchor is complete, and the under-quote never existed

**Data and documentation only. `references/ofox-image.sh` is untouched.**

**This entry retracts a claim 1.12.0 made.** That version recorded the
1792x1008 edit as *unpriceable* — "output tokens never recorded and
unrecoverable, the cost equation has two unknowns left" — filed it in a
purpose-built `unpriceable_observations` list, and published a
never-under-quote disclosure across five files telling callers to read a
`ROUGH UPPER BOUND` on a large input as a **floor**. All of that was wrong,
and it was wrong because the run's full output had scrolled out of the
terminal rather than because anything was actually lost.

The real figures, recovered from the session transcript:

```
USAGE_INPUT_TOKENS 1571   USAGE_INPUT_IMAGE_TOKENS 1508
USAGE_INPUT_TEXT_TOKENS 63   USAGE_OUTPUT_TOKENS 129
USAGE_TOTAL_TOKENS 1700   EDIT_COST 0.016249
```

They self-check three ways — `1508+63=1571`, `1571+129=1700`, and
`63*0.000005 + 1508*0.000008 + 129*0.00003 = 0.016249`, matching the reported
cost to six decimals. The equation was **underdetermined, not unsolvable**:
one more observed value (the text-token count) closes it.

**What a caller has to do differently:**

- **Stop treating a large-input edit quote as a floor.** That instruction is
  withdrawn from `references/pricing.md`, `SKILL.md`, `image-edit` and
  `product-image`. Verified after the fix — a 1792x1008 input now quotes
  `Estimated cost: ROUGH ~$0.0164 (129 output + 1571 input tokens, measured
  2026-09-16 on an input image of 1792x1008 at --quality low)`, against a real
  bill of $0.016249. An exact-pair `ROUGH`, above the real cost, which is
  where the never-under-quote rule wants it.
- ⚠️ **Do not reason about an edit's cost from its output tokens.** The new
  point is what shows why. Ordered by input pixels the counts run **129**
  (320x180), **229** (256x256), **301** (854x480), **129** (1792x1008) — not
  monotonic, with the largest input tying the smallest for the lowest count.
  The **input image** tokens are what track the upload (240 / 256 / 576 /
  1508), and on a large source they are **74%** of the bill. The lever is the
  size of the file you upload.

**What the fourth point still establishes**, unchanged from 1.12.0: the
~1.57 MP output budget is a **budget, not an upsample floor** — 1792x1008 is
1,806,336 px, larger than the 1672x941 it returned, and the output did not
grow. The three earlier points were all smaller than the output and could not
separate those two readings.

**Removed: `unpriceable_observations` and its three guard assertions.** With
its only entry promoted to a real anchor the list is empty, so the assertions
had no input that could make them fail — which is the exact shape
`falsifiable-gates.md` warns about. A container built for one datum, once that
datum turns out not to belong in it, is not infrastructure worth keeping. The
pre-existing assertion that every entry in `additional_measurements` carries
an `input_size` **and** a numeric `output_tokens` is untouched, and it is the
check that caught the mis-filing in the first place.

🚨 **Root cause, now documented: this script writes no sidecar.**
`ofox-video-core` saves a `.json` beside every mp4 with the job id, seed,
prompt and real cost. `ofox-image.sh` writes the image and nothing else —
verified: the three edits behind this anchor have no companion file, while
every video job from the same session has one on disk. The figures
`_how_to_add_a_row` demands are precisely the ones this path never persists,
which is how a complete measurement came to be written up as lost. `SKILL.md`
gains a section telling callers to `tee` every paid run to a log, and
`_how_to_add_a_row` now says so too. **Adding a sidecar to the script is a
separate change and is not made here** — it has to decide a filename, a
schema, and the `--n > 1` case where one call writes several files.

## 1.12.0 — a fourth edit anchor, and an under-quote that turned out not to exist (see 1.13.0)

> ⚠️ **WITHDRAWN IN PART BY 1.13.0.** Everything below about the run being
> *unpriceable* is false: the token counts were never lost, only scrolled out
> of the terminal, and they close the pricing formula exactly. The
> never-under-quote disclosure this entry introduced is withdrawn, and the
> `unpriceable_observations` list it created has been removed. The ~1.57 MP
> budget finding and the non-linear input-token finding stand. Left in place
> rather than rewritten, because a retraction a reader can see is worth more
> than a tidy history.

**Data and documentation only. No script, flag, default or formula changed**
— `references/ofox-image.sh` is untouched, and `edit --dry-run` was re-run
after the change to confirm it still prints an estimate on both a matching and
a non-matching input size.

**A fourth measured edit run recorded** (`references/token-anchors.json`,
`references/pricing.md`): `openai/gpt-image-2`, a real 1792x1008 photograph,
three background-swap edits on 2026-09-17, **1508 input image tokens**,
`EDIT_COST` 0.016249 / 0.016289 / 0.016304, output 1672x941. It is the largest
input measured here, the first real photograph rather than a synthetic
flat-colour test image, and the first where **the input was bigger than the
output** — which is what turns "the endpoint spends ~1.57 MP on the input's
shape" from one of two readings into the surviving one.

⚠️ **What a caller has to do differently, and it is a pricing matter.** That
run's `USAGE_OUTPUT_TOKENS` was never recorded, and it cannot be recovered —
the cost equation has two unknowns left and several integer pairs fit. The
file's own rule forbids a derived figure, so the run is filed under a new
`edit_anchors[model].unpriceable_observations` list that
`edit_anchor_measurements()` never reads — **not** as an anchor. It was first
put in `additional_measurements`, where `references/test/edit.test.sh` failed
on it, because every entry there must carry an `input_size` **and** a numeric
`output_tokens`. The gate was right and the filing was wrong, so the data moved
and the assertion was left untouched. The estimator therefore falls back to the
dearest point it can read:

```
input 1792x1008 -> Estimated cost: ROUGH UPPER BOUND ~$0.0139
real bill for that input size ->                     $0.016249
```

**So on this endpoint a `ROUGH UPPER BOUND` is a floor, not a ceiling, for any
input larger than every measured point** — 17% low here. Until someone spends
1.6 cents re-measuring the pair, quote a large edit as a floor and say so in
the cost table. Nothing was invented to paper over it, and nothing in the
script was changed to work around it.

**Three new assertions in `references/test/edit.test.sh`**, so the new list
cannot become the place incomplete data goes to look complete: an entry must
name its `input_size`, must say `why_this_is_not_an_anchor`, must **not** carry
an `output_tokens` (if it had one it would be an anchor), and must not
duplicate an input size that already exists as a real anchor. Each was
verified by planting the corresponding defect and watching it fail, then
restoring — a check nobody has seen fail is not a check.

Raised, not changed: `print_edit_estimate` picks its "dearest" point by
`output_tokens` alone, while at large input sizes the **input** term is most
of the bill. The three readable points happen to agree today. Per the
chain-order rule in `token-anchors.json`, a change that can move a quoted
price gets raised before it is made.

## 1.11.2 — the frontmatter did not parse, and the installer said nothing

The `description` carried a `: ` (colon then space) inside an unquoted YAML
value. YAML reads that as a nested mapping and rejects the whole block, so
`skills add` **skipped this file entirely** — and reported the count of skills
it found, never the ones it dropped. This skill was uninstallable from
skills.sh while appearing published everywhere else.

Replaced with an em dash, matching the rest of these descriptions. Nothing
else changed. A parse check over every SKILL.md is now a publish gate in
CONTRIBUTING.md, because nothing in this repo had ever parsed its own
frontmatter — which is why this survived.

## 1.11.1 — routing, and a "common case" that stopped being one

No behaviour change, no script change. Two documentation corrections, both of
claims that were true when written and went false without anything in this
repo moving.

### The `MODEL_SOURCE` guidance was predicting an upstream response shape

`SKILL.md` said `openai/gpt-image-2` "never echoes a `model` field", and that
since it became the chain's head on 2026-09-04, **`MODEL_SOURCE request` is
now the common case for a default `generate` call**.

That was first-hand and expensive to learn: the missing field defaulted to the
literal `"unknown"`, matched no rate, and printed no `IMAGE_COST` at all on two
paid calls — the defect 1.3.0's fallback was written to fix.

**Re-checked 2026-09-15 on three real paid calls against the same model — two
probes run while `image-edit` and `product-image` were written (one
`generate`, one `edit`), plus one further minimal `generate --quality low
--size 1024x1024` (196 output tokens, `IMAGE_COST 0.00593` against a
0.59-cent estimate). All three printed `MODEL_SOURCE response`.** The field is
being echoed now.

**Nothing in the script changed and nothing needed to** — both branches were
always handled, and `MODEL_SOURCE` is printed unconditionally so a caller never
has to guess. What changed is the advice: the section no longer tells anyone
which branch to expect, because an upstream response shape is not a stable
fact to anchor a "common case" sentence to. **If you relayed `MODEL_SOURCE`
faithfully you were already right on both days**; if you wrote a prediction of
it into your own skill, that is the thing to go and delete.

### The description pointed plain edit requests here

One clause of the `description` was stale the moment `image-edit` and
`product-image` shipped on the same day.

It read: *"for a plain 'generate an image of...' or 'change this image so
that...' request with no scenario skill available yet, this is the right skill
to use directly."* The conditional was true when it was written and is not any
more — `image-edit` owns "change this image so that…", and `product-image`
owns a set of product images to choose between. An agent picking a skill from
descriptions alone would have been told to come here for a request a scenario
skill now covers properly.

The clause now names the three scenario skills that call into this one
(`image-edit`, `product-image`, `seedance-anime-drama`) and keeps exactly one
direct-use case for a request with no scenario behind it: a plain
text-to-image "generate an image of…".

**What this leaves unchanged:** everything about `edit` itself, and the
direct-use cases that were never in question — naming the Ofox image API,
driving it with specific low-level parameters, or debugging a failed request.

## 1.11.0 — image editing (`POST /v1/images/edits`), and an endpoint that bills you for your typos

New `edit` subcommand. It takes an image you already have and changes it,
which this skill has documented as out of scope since v1 and which was the
thing blocking two scenario skills. Nothing about `generate` changes.

```bash
bash references/ofox-image.sh edit --image ./photo.png \
  --prompt "Replace the background with a beach at sunset. Keep the person unchanged." \
  --dry-run
```

A local file is the primary input; `--image-url` also takes a public URL or a
`data:` URI, but hosting is never a precondition. Shares `generate`'s model
resolution, `--dry-run`, exit codes, geometry flags
(`--target-aspect`/`--target-size`) and absolute-path reporting. The endpoint
is multipart-only — a JSON body is rejected outright — so there is no
`--extra-json` here; `--extra-form KEY=VALUE` is the passthrough, and
`--dry-run` prints a `FORM_FIELDS` line of field **names** where `generate`
prints a payload.

**Which models can edit is a live lookup, not a table.** Each `/v1/models`
entry's `supported_endpoints` already names `/v1/images/edits` or does not, so
that is what the script reads — `models --endpoint edits` lists them, and
`model_unavailable_reason()`/`resolve_model()` now take the endpoint as a
parameter instead of hardcoding one. Confirmed predictive in both directions:
`qwen/qwen-image-3.0-pro` (flag absent) is refused with a new
`endpoint_not_supported`, and seven models carrying the flag ran an edit
across three vendors. No static edit-support list was added, and a test
asserts none appears later. Worth recording that the capability was **not**
where it was first looked for: `image_attributes.supported_params` lists
generation fields only, which reads as "the catalog says nothing about
editing" when the answer is one field over.

**Costs are measured, and `edit` bills something `generate` never does.** Three
real edits on `openai/gpt-image-2`: an 854x480 input cost 0.013798, a 320x180
input 0.005955, and a 256x256 input 0.009083. Edits *do* report `usage`, more richly than
generations — `input_tokens_details` splits the prompt's text from the
uploaded image, and **576 of 608 input tokens on the first run were the
picture**, billed off a `pricing.image` rate the catalog publishes separately
from `pricing.prompt`. That leaves two defensible readings of the same
numbers, 13% apart, with no invoice to settle them; `edit_cost_for()` returns
the **dearer**, per the never-under-quote rule, and says so in a NOTE. New
`edit_anchors` section in `token-anchors.json`, kept separate from the
generation anchors because the same model spent visibly different output
tokens on the two endpoints.

**The estimate is matched on the input image, not on `(quality, size)`.** Two
of the measured points share a model, a quality and a byte-identical 1672x941
output and still differ 2.3x in output tokens — so keying an edit estimate the
way a generation estimate is keyed would key it on the wrong thing. The script
measures the caller's own `--image` and quotes the point measured at that
input size; with no match it quotes the dearest, labelled
`ROUGH UPPER BOUND`. An incidental finding recorded in
`references/api-params.md`: output geometry is a **near-constant ~1.57 MP
budget spent on the input's aspect ratio** — 854x480 and 320x180 both returned
1672x941 (which is 1.777, the 16:9 that `generate`'s `size` enum cannot
express at all) and 256x256 returned 1254x1254, a 0.05% identical pixel count.

A second pattern from the same runs was written down and then **withdrawn
before release**: output tokens looked like roughly half the input image
tokens on the two 16:9 runs (0.523, 0.538). It was recorded as a pattern to
test rather than a law, and deliberately never implemented as a formula; the
256x256 run tested it and it is false (229/256 = 0.895). Input image tokens
are not linear in input pixels either — 854x480 has 6.3x the pixels of
256x256 and bills 2.25x the tokens. Keeping it out of the code is why losing
it cost nothing: an interpolating `print_edit_estimate` would now be quoting
roughly half of what an unmatched input size actually bills.

The 256x256 run was added in review, because the first two could not support
the sentence written from them: both were 16:9, and "output follows the input
ratio" and "output is a fixed 1672x941 for this model" fit two 16:9 samples
equally well. The conclusion survived at 0.9 cents — but until a different
ratio was sent it was the untested half of a two-directional claim, which is
the shape this repo's spec calls out as its sharpest recurring defect.

### ⚠️ The finding that cost the most, and the one to carry elsewhere

**`/v1/images/edits` does not validate parameters the way
`/v1/images/generations` does, and the failure mode is a bill rather than a
free 400.** `generate` gets an unknown `--quality` refused upstream for
nothing. Sending `quality=ultra_not_a_value` to six models on this endpoint —
*as a guard, precisely so the probe would be rejected and therefore free* —
had all six ignore the value, render, and bill.

Two consequences:

- The client-side checks in `edit` are not a round-trip saving the way
  `generate`'s are; they are the only guard. The `--quality` error message
  says so. `edit` deliberately checks against the documented **union** only
  and does **not** apply `model_qualities()`'s per-model enumeration, because
  that set was read off a *generations* refusal and this repo has already been
  bitten by assuming two endpoints of one API behave symmetrically.
- More generally: **a free probe is only free if the thing you expect to
  reject it actually does.** The guarded-probe technique used throughout this
  repo to map an API at zero cost silently spends money against an endpoint
  that ignores unknown parameters. Verify the guard is refused once, on a
  model already known to reject the request for another reason, before fanning
  a guarded probe across a list.

Also new: `edit` reminds the caller on every success to compare the result
against `INPUT_IMAGE` (printed next to `IMAGE_PATH` for that purpose), because
`STATUS completed` cannot distinguish an edit from a redraw of the prompt. On
the runs behind this release it genuinely edits — a UI screenshot asked for one
button colour change came back with every string intact and 58% of all changed
pixels inside the button, 1.1% of the frame — but that is evidence about three
runs, not a property to assume.

Error mapping gains `model_not_found` (404) and `endpoint_not_supported`
(400), both observed, and `print_api_error` now prints `error.param`. Noted in
`api-params.md`: on this endpoint `error.code` is **null** on validation
rejections, so it is neither semantic nor guaranteed — `error.type` remains
the classifier and nothing branches on `code`.

New suite `references/test/edit.test.sh`, 50 cases, free by construction.

### Found in review, before release

**`models-snapshot.json` was regenerated, and that made `edit` work offline at
all.** The bundled snapshot dated from 2026-08-30, before Ofox advertised
`/v1/images/edits` on anything. With a cold cache and no network the script
fell back to it and refused every model in `MODEL_CHAIN` — *"--model
'openai/gpt-image-2' exists but does not serve /v1/images/edits, so it cannot
edit an image"* — confidently, and wrongly, about a model that does. The live
list carries the endpoint on 11 of 16 image models. Same defect class the
video side hit the same day, same fix (`references/refresh-snapshot.sh`), and
the image side had simply never been refreshed.

Regenerating is a behaviour change, so here is what moved:

| | Before (2026-08-30) | After (2026-09-15) |
|---|---|---|
| image models | 14 | 16 — `openai/gpt-image-2.5-flare` and `-sunburst` are new |
| serving `/v1/images/edits` | **0** | 11 |
| qwen ids | `bailian/qwen-image-3.0{,-pro}` | `qwen/qwen-image-3.0{,-pro}`, old ids kept as aliases |
| `microsoft/mai-image-2.5-flash` `output_image` | 0.000026 | **0.0000195** |

Only one price moved, and it moved **down**, so the stale copy had been
*over*-quoting that model offline by 33% — the harmless direction, which is
why nobody noticed. The figure it fed is corrected in `token-anchors.json`
(`cost_per_image` 0.026694 → 0.020038), `pricing.md`, `SKILL.md`'s chain table
and the chain comment in the script: ~2.67 cents/image becomes ~2.0, and
`gpt-image-2`'s advantage over it 4.5x becomes ~3.4x. The token counts behind
those figures are measurements and did not move; only the multiplication did.

`refresh-snapshot.sh` itself had two bugs the refresh exposed. It selected on
`/v1/images/generations` alone, so a future edit-only model would be dropped
and then reported as "not in the Ofox model list"; and it kept only
`pricing.output_image`, so an offline edit estimate lost its entire
input-token component — a measured $0.0138 edit quoted at $0.0090, a **35%
under-quote wearing the exact-match `ROUGH` label rather than a bound**. Both
fixed, and `edit.test.sh` now asserts both against the shipped file.

**`edit.test.sh` was not hermetic.** It warmed the real model list from
`api.ofox.ai` and then pointed the base at an unroutable address, so every
model-support assertion silently tested whichever data source happened to be
present — scoring 39/0, 37/2, 36/3 and 30/9 on repeated runs of one commit.
Now nothing in it reaches the network: behavioural assertions run against a
hand-written fixture catalog installed in the cache, the bundled snapshot is
tested separately and deliberately as *shipped content*, and three closing
assertions check that the base URL was never unset, that no executable line
names the real API, and that the cache stayed in the temp dir. Verified over
repeated runs with an empty `XDG_CACHE_HOME`, a warm real one, `HOME`
relocated, and the outer base URL pointed at production: 50/0 every time.

**`imagecost.test.sh` failed at HEAD for the same root cause** — it asserted a
literal `0.026694`, which is a copy of a rate Ofox owns, and the rate moved.
The expectation is now derived from the loaded list; the invariant under test
was always "the figure follows the model that *ran*", not that specific
number. The one hardcoded figure left is the $0.06723950 invoice line, which
is a fact about a bill that was really paid. That suite also silently could
not reach its own snapshot fallback (the sourced copy resolved `SCRIPT_DIR` to
a temp dir), so it died outright offline while its header claimed otherwise;
it now runs on either rung.

## 1.10.3 — the link to the shared approval gate can miss without the file being gone

Docs only; no change to the script, the tests, the API calls or the billing.
This skill links `../ofox-video-core/references/approval-gate.md` three times.
That relative path resolves only when the core skill's directory is named
after the skill — true for skills.sh, ClawHub and `npx ofox-skills`, and
**false for LobeHub**, which unpacks each skill to
`~/.agents/skills/ofoxai-skills-<name>`. There the file sits under
`ofoxai-skills-ofox-video-core` and the link points at a name nothing uses.
This is the core-to-core half of the same breakage the four scenario skills
carry, and it was missing from the original file list.

"Before you spend" now says the link assumes a directory name, carries a probe
over the five known locations, and — the part that matters — states that a
link which does not resolve is **not** a reason to skip the gate: the rule is
the paragraph above it and the dry run below it either way, and only the
spec's detail travels with `ofox-video-core`.

The "four things a scenario skill must not re-implement" list keeps telling
scenario skills to link the gate rather than paraphrase it, and now adds that
the directory-name caveat travels with the link — a "Where the core skill
lives" probe near the top of a scenario skill is what stops that link reading
as a missing file.

## 1.10.2 — the changelog for 1.10.1 quoted the literal it had just removed

**Changelog text only; no change to the script, the tests, the API calls or
the billing.** The 1.10.1 entry below originally explained the scanner finding
by quoting the old test-fixture literal verbatim, so the published 1.10.1
still carried `suspicious.exposed_secret_literal`. ClawHub's stored scan report
(`clawhub scan download`, staticScan v2.4.26) placed it at `CHANGELOG.md:14`,
the line of the quote. A key-shaped string in prose explaining its own removal
is still a key-shaped string to the scanner.

- **The 1.10.1 entry is reworded in place** to describe the literal without
  reproducing it. This file ships in the bundle and is scanned like any other
  file; nothing key-shaped belongs in it, in any version's entry.
- **What this does *not* fix, and will not**: the same stored report carries a
  second static code for this skill, `suspicious.potential_exfiltration`, at
  `references/ofox-image.sh:302`, with the message that the script "base64-encodes
  a local file and sends it over the network". Line 302 is the decode helper: it
  turns the API's base64 *response* into the image file on disk. Nothing local
  is encoded on that path and nothing is sent. It is a false match on `base64`
  and `curl` sharing one script, and rewriting a correct decode to dodge an
  unpublished heuristic is the bet the 1.10.1 entry declined to make. It stays.
- **Also left alone**: the LLM review (skillSpector 2.3.5) rates the
  refusal-handling section of `references/api-params.md` HIGH for reporting
  that a prompt refused on one model passed unchanged on another. That section
  records a measured result with a bill attached; it stays as written. Expect
  the public page to keep showing `suspicious` for this skill on those two
  grounds — this entry says so rather than claiming otherwise.

## 1.10.1 — the fake key in the tests read as a real one to a scanner

**Test fixtures only; no change to the script, the API calls or the billing.**
ClawHub's public page for this skill showed `suspicious` at high confidence
after the 2026-09-08 publish. The machine reason was a single code —
`suspicious.exposed_secret_literal` from staticScan v2.4.26 — and it was
correct about the pattern even though it was wrong about the risk: every test
file opened by exporting `OFOX_API_KEY` with a 33-character hyphenated literal
written inline — one whose text says, in words, that it is not a real key. A
static scanner matches the shape of the assignment; it does not read the value
and take its word for it.

- **The literal now goes through a variable**, and the variable's name has no
  `KEY` in it: `PLACEHOLDER=placeholder` then `export OFOX_API_KEY="$PLACEHOLDER"`.
  What changed is the *pattern*, not the length — picking a shorter secret-ish
  string would have been betting on a threshold nobody published.
- ⚠️ **`newuser.test.sh` had a worse one.** Its "a present key is not a verified
  key" case set the variable inline to a joke value carrying the `sk-` prefix a
  real OpenAI-style key has — which is exactly what made the string funny and
  exactly what made it scan badly. Same treatment.
- **Nothing about the tests' meaning moved.** The scripts only require the
  variable to be non-empty; the "present but unverified" case only requires it
  to be set. All 4 test files in this skill still pass.
- **What this does *not* fix**: the LLM-written `security.summary` on the same
  verify call reads differently from the machine code — it talks about dotenv
  sourcing and redirectable endpoints. Those are design properties, argued for
  elsewhere in this file, and no reason code is attached to them. This entry
  claims the static-scan code only.

## 1.10.0 — a key the agent was forbidden to load, in a file the user had already pointed at

**Documentation and `check` output only; no change to how a request is built
or billed.** This one came out of a real session on Codex: the user was
asked to `export OFOX_API_KEY`, replied that it was already in `.env`, then
gave the absolute path, then said "just read it" — and was refused all three
times. Nothing was generated. The refusal was correct per the text: the safety
contract's first line read *"`OFOX_API_KEY` is read **only from the shell
environment** — never from a dotenv file"*, and the only reading available to
an agent is that it may not touch the file even on request.

- **The first safety-contract line is split in two, because it was describing
  two different actors in one sentence.** The script's constraint is real and
  stays hard: `ofox-image.sh` parses no dotenv, ever. The agent's constraint was
  collateral damage from sharing the sentence. It now reads separately: you may
  load the key from a dotenv file *once the user has authorized it*, via
  `set -a; . <path>; set +a` in the shell you'll call the script from.
  Authorization is still the precondition — this is not licence to go hunting
  for `.env` files nobody mentioned.
- **The missing-key recovery bullet now carries the same second path.** This is
  the part that actually mattered. An agent hitting a missing key reads the
  nearest instruction, not the contract twelve screens up, and that bullet said
  `export` and only `export`. Splitting the contract alone would have left the
  dead end exactly where it was.
- **`check`'s stderr gained one line for the same reason** — the terminal user
  who runs the script directly was getting the same single-path advice.
- ⚠️ **New warning, because sourcing a dotenv is not as narrow as it looks.**
  `set -a; . <path>; set +a` imports *every* variable in the file. One of them
  is `OFOX_API_BASE_URL`, which `ofox-image.sh` honours (`ofox-image.sh:144`) — a stray value
  there silently redirects every API call in the session to somewhere else.
  Read the file before you source it. The `.env` that prompted this entry
  contained exactly that variable.

## 1.9.1 — the key requirement, moved to the front of a description that gets truncated

Docs only; no script changes, no advice changed. `description` now **opens**
with one sentence: `Requires OFOX_API_KEY — create one at
https://app.ofox.ai.` The dependency itself is unchanged and was already
declared in `metadata.openclaw.requires.env`, which stays exactly as it
was — that is the route ClawHub and openclaw read. Nothing a caller does
changes.

**Two separate blind spots, measured 2026-09-06 against Codex CLI 0.149.1 with
a project-level install of this repo.** It listed all nine skills, but asked
which environment variables `seedance-product-video` needs before use it
answered that it could not tell from the visible skill metadata. The first
cause is the obvious one: some agents read only the frontmatter's `name` and
`description`, never `metadata`. The second only surfaced on a controlled
retry — same agent, same question, the requirement added to the **end** of the
description and nothing else changed — where the answer did not budge. Pressed
for a verbatim quote, the agent said the description in its context was
truncated and did not include the final sentence; it put its own visible tail
at about 257 characters, and the fragment it could still quote ends at
character 320 of the real text. So the window is roughly 300 characters, and
these descriptions run 828 to 1200. "Reads the description" is not the same as
"reads all of it".

**What that costs, beyond the key.** Inside a ~300-character window the
`Use when ...` trigger examples of all four scenario skills fall outside: they
begin at character 431 (`seedance-ad-creative`), 594
(`seedance-product-video`), 641 (`seedance-anime-drama`) and 690
(`seedance-short-drama`). This skill's own `Load this skill directly only when ...` clause begins at
character 583, likewise outside. A truncating agent has never matched any of them
on an example — it matches on the opening summary alone. Anything that has to
reach such a reader belongs in the first ~300 characters, which is why this
sentence leads instead of trailing, and why it is 58 characters rather than the
106 first drafted: that position is the scarcest space in the skill, and every
character spent there displaces a character of trigger material.

**Why character 0 and not the end of the opening sentence.** The first
sentence-ending period sits at character 268 in `ofox-image-core`, 430 in
`seedance-ad-creative` and 593 in `seedance-product-video`. Placed there the
sentence would straddle or clear the window in exactly those three, and
reaching a boundary at all in two of them would mean repunctuating shipped
prose. Character 0 is the only position that is inside the window under both
the 257- and the 320-character reading, for all six skills, without altering a
word of the existing text.

Two readers were never affected and are unchanged by this: Claude Code reads
the description in full, and OpenCode read at least the first 1075 characters
of `seedance-product-video` — it answered `OFOX_API_KEY` correctly even from
the trailing version.

## 1.9.0 — correction: it was the jacket, not the ages; and a refusal that names nothing has to be bisected

Docs only; no script changes.

**Correction to 1.8.0.** That entry said the safety refusal cleared because the
prompt dropped its age numbers, softened minor-coded wardrobe detail and
rewrote a strike as two forces meeting. Three edits went out together, so
nothing was isolated, and the emphasis fell on the two that turn out to have
nothing behind them. A single-variable bisect on 2026-09-06 — a control plus
five steps at
`--quality low --size 1024x1024`, about 0.037 USD billed and the one refused
step free — walked from a prompt known to pass toward the prompt known to fail
and stopped on one word: `cropped`, in `cropped jacket` — a
bare-midriff garment, so most plausibly a sexual-content read, though the
endpoint names no category and that part stays inference. The two prompts
either side of that step are identical byte-for-byte apart from the word, and
one is refused while the other is not.

**Three strengths of result, kept apart.** The setting and the powers were each
swapped on their own in a step that passed, so those two are cleared. The
weapons and the covered faces are not: they came out of the prompt one at a
time and then together while the cause was still being guessed at, and it was
refused every time — enough to say neither is the cause on its own, not enough
to call either safe, because nothing that passed on this model has carried
them. The blade that did get through went through `mai-image-2.5-flash`, a
different filter. The ages and
the blow-landing strike wording are a third case again: every step started from
the retry that had already dropped both, so the bisect inherits them and cannot
speak to either. The entry also states the asymmetry behind all three, which is
what both corrections turned on — a refusal shows what is not sufficient to fix
a refusal, and only a passing call can show a clause is safe, and only for what
that call carried.

Reading back, the 1.8.0 retry that "worked" had also turned `black over-knee
socks` into `dark tights` in the same batch, which is the likelier cause — so
the wardrobe edit was in 1.8.0's list, filed under
"minor-coded" when the evidence now points at the garment itself. **The
age-number and rewritten-strike claims have no isolating evidence in this
repo** and are recorded as untested rather than as advice. If you were
following 1.8.0, the thing to change first on a refused character prompt is the
wardrobe wording, not the subject matter. `SKILL.md`'s one-line pointer at that
row changed with it: it used to send readers there for "what got through on the
retry", which is exactly the attribution being corrected, and now names the
isolated trigger and both repair routes.

**A refusal here carries no category, so guessing is the expensive route.** All
six refusals in that session returned the identical string `Your request was
rejected by the safety system`. Six semantic guesses against that silence all
missed; the five written down afterwards were weapons, the covered face,
realistic combat versus fantasy powers, a rooftop parapet read as self-harm,
and wet clothing clinging to the body. A new
subsection in `references/api-params.md`, "When a refusal names no category,
bisect rather than guess", writes up the procedure that did converge: start
from a prompt that passes, change one thing per call, and bisect inside the
step that fails. It leads with the control — re-running the known-good prompt
unmodified — because a refused control means the filter moved and every
comparison after it is unreadable.

**The escape hatch was real and buried.** `microsoft/mai-image-2.5-flash` had
already been observed producing a bladed character sheet that
`openai/gpt-image-2` refused twice with this same error, but that lived only in
a task record, which is why nobody reached for it during six refusals. The
error table now lists two repair paths for a safety refusal, not one: rewrite
the clause, or re-run unchanged on `--model microsoft/mai-image-2.5-flash`.
About 2.67 cents against 0.6 cents at the cheap pair — usually less than a
third rewrite, and the route to take when the refused element is one the shot
wants to keep.

## 1.8.0 — the safety system has its own error type, and an age number was enough to trip it

Docs only; no script changes. `error.type` on `/v1/images/generations` had
exactly one confirmed value since 2026-08-29, `invalid_request_error`. A real
call on 2026-09-06 returned a second: **`image_generation_user_error`**, HTTP
400, upstream message *"Your request was rejected by the safety system"* with
an Azure request id. Nothing billed.

What tripped it is worth recording because it is ordinary scenario input, not
an edge case. The prompt was an opening frame for an anime fight and named
ages explicitly — `a 17-year-old girl`, `an 18-year-old boy` — while describing
a strike landing on a person (`his right fist … driving forward into her`).
Removing the age numbers (`a young woman` / `a young man`), easing the
minor-coded wardrobe detail, and rewriting the clash as two forces meeting in
the air rather than a blow landing on a body passed on the very next call with
everything else unchanged.

The error table in `references/api-params.md` carries the row; `SKILL.md`'s
claim that `invalid_request_error` was "the only value confirmed so far" is
corrected rather than left to age.

## 1.7.0 — the quote said 0.6 cents, the bill said 15.4, and `--dry-run` had no opinion about `standard`

Two guards, both for failures that already happened on real runs and neither
of which anything in this skill was set up to catch.

**The estimate is pair-aware, and never optimistic.** On 2026-09-04 a scenario
skill generated a real frame at `--quality high --size 1792x1024`, was quoted
**~0.6 cents**, and was billed **15.4 cents** — 5063 output tokens against
the 196 the anchor had been measured at (`low` / `1024x1024`). 26x, on one
model, from two flags; and the flags were on screen directly above the wrong
price, because the lookup read one number per model
(`.anchors[<model>].output_tokens`) and never saw what was requested. The
approval gate faithfully relayed the smaller number, which is the part that
makes this a spend bug rather than a display bug.

- **A measurement at the request's own `--quality` and `--size` is quoted
  as-is**, and the line now carries the pair: `measured 2026-09-04 at
  --quality high --size 1792x1024`. The pair travels with the price into the
  approval table, so someone reading only the quote can see whether it
  belongs to what they asked for.
- **When no measurement exists at that pair, the DEAREST point the model has
  is quoted, labelled `ROUGH UPPER BOUND`**, with the pair it borrowed from.
  Nothing is interpolated between two measured points, and nothing is ever
  borrowed across models — that rule is unchanged and still tested.
- **`auto`, and an omitted `--size`, take the bound path.** The API picks in
  both cases, so there is no pair to match and matching one anyway is exactly
  the optimism that cost the 15.4 cents. **Consequence worth knowing: a cheap
  `--quality low` call with no `--size` now shows `gpt-image-2`'s 15.4-cent
  ceiling rather than its 0.6-cent point.** Naming the pair
  (`--quality low --size 1024x1024`) is what gets the exact figure back. An
  over-quote labelled a ceiling is recoverable; an under-quote that has
  already been approved is not.
- **A ceiling built on one sample says so.** `microsoft/mai-image-2.5-flash`
  has exactly one measured point, so its "bound" for a large high-quality
  frame is 2.66 cents — a figure a real bill could plainly exceed if its token
  count climbs with size the way `gpt-image-2`'s does. The line prints a
  second `Weak ceiling` note in that case and says to measure the pair rather
  than lean on the label. Two-point models do not get the caveat, because a
  caveat printed unconditionally is a caveat nobody reads.
- Data: `references/token-anchors.json`'s `quality`/`size` fields are now
  load-bearing rather than documentation, and `additional_measurements[]` is
  read as real points rather than as a note — `gpt-image-2`'s 5063-token entry
  is what the ceiling above is made of. A measured point with no pair recorded
  can no longer be priced against a request at all, and a test fails if one
  appears. The file's own instruction to raise this change with the repo owner
  rather than make it quietly was followed; approved 2026-09-05.

**`--quality` is validated against the model that will actually run.** It was
validated against the union of every model's values (`auto low medium high
standard hd`), so `standard` passed validation, passed `--dry-run`, and then
died at submission with `Invalid value: 'standard'. Supported values are:
'low', 'medium', 'high', and 'auto'` — the day `MODEL_CHAIN`'s head became
`openai/gpt-image-2` (2026-09-04). Five copy-pasteable commands across two
other skills shipped broken that way and a dry run caught none of them. Now
the combination fails at `--dry-run`, exit `1`, no network call, nothing
billed.

- **The error names the model even when nobody named it.** With no `--model`
  passed the id comes from `MODEL_CHAIN`, and an error about
  `openai/gpt-image-2` is unconnectable to anything the user typed unless it
  says where the model came from. It says so, and offers both fixes: an
  accepted `--quality`, or pinning a `--model` that takes the value —
  naming `microsoft/mai-image-2.5-flash` specifically when the value is
  `standard`.
- **The whitelist has exactly one row, and that is the design, not a TODO.**
  `openai/gpt-image-2`'s four values come from the API's own enumeration, read
  verbatim off the 400. Everything else keeps the full union: what exists for
  the other models is evidence that a value *works* (`standard` on
  `mai-image-2.5-flash`, nine real runs; `low` on
  `google/gemini-3.1-flash-image`, three) — not an enumeration of what they
  take. **A false rejection here is worse than the 400 it would prevent**: the
  400 costs a round trip and no money, while a false rejection blocks the work
  outright with no way around it short of editing the script. So an absence of
  evidence stays permissive, and `model_qualities()` gains a row only when a
  model has enumerated its own set. A test asserts the row count, so the next
  row has to be argued for.

- Documentation: `SKILL.md` rewrites "The estimate is rough, and sometimes
  impossible" around the three-outcome line shape and the four selection
  rules, replaces the per-model `--quality` pass/fail table with one that
  separates first-hand enumeration from the permissive fallback, and adds a
  fourth scenario-skill "do not re-implement this" item covering both the
  per-image price and the `--quality` value — the two things those five broken
  commands had hardcoded. `references/api-params.md` and
  `references/pricing.md` carry the same correction against the fields and the
  anchor table they belong to; `pricing.md`'s "neither is fixed by this
  write-up" is now a record of what was fixed and what is still on a human.
- Tests: 149 cases, up from 108. `dryrun.test.sh` gains 25 — the verbatim
  bug reproduction (`--quality high --target-aspect 16:9`) now quoting the
  5063-token point and explicitly *not* the 196-token one, the pair printed in
  the line, an unmeasured pair taking the labelled ceiling, `auto` and omitted
  `--size` doing the same, no interpolation between 196 and 5063, the weak
  single-sample ceiling, one estimate line on every path, and every anchor
  carrying its pair. `validation.test.sh` gains 16 — `standard` and `hd`
  rejected for `gpt-image-2`, all four of its enumerated values still
  accepted, the rejection reachable with no `--model` and naming the resolved
  model and its origin, `standard` still accepted on the model that takes it
  and on unenumerated models, `hd` still accepted where nothing was observed,
  the union check still firing first, `check` still working with no model in
  hand, and the one-row table asserted. No existing assertion was changed;
  one existing case's **input** moved from `--quality standard` to
  `--quality low --size 1024x1024`, because that input is now invalid by
  design and an omitted size is deliberately unmatchable — the assertion and
  its `0.0059` figure are untouched.

## 1.6.0 — 16:9 was never requestable, and the third agent to hand-crop a frame is one too many

**The size enum this API accepts contains no 16:9 and no 9:16 entry, and
cannot.** `1792x1024` is 1.7500 against 16:9's 1.7778; `1024x1792` is 0.5714
against 9:16's 0.5625. That is not a model defect and no flag removes it — it
is a structural gap between this endpoint's `size` enum and the video API's
`aspect_ratio` values, so **every 16:9 or 9:16 frame this skill has ever
produced was cropped by hand afterwards**, and three separate agents
re-derived "measure the file, then crop" from first principles before anyone
wrote the fact down. Nothing in this skill said it. That is what 1.6.0 fixes,
in the script rather than in advice.

- **`--target-aspect W:H` and `--target-size WxH`: state the ratio you
  actually need, and the script keeps it.** It picks the request size from the
  enum (for 16:9, `1792x1024` — 98.4% of the pixels survive the crop, against
  `1536x1024`'s 84.4%), generates, **measures the written file with
  `ffprobe`**, and centre-crops to exact integer multiples of the reduced
  ratio. Both crops previously done by hand fall out of that one rule:
  `1344x768 → 1344x756` and `1792x1024 → 1792x1008`. `--target-size` adds a
  pixel floor — cheapest accepted size that clears it, then scaled down to
  exactly those pixels. Never scaled up.
- **Why this was worth code and not a paragraph: `adaptive` turns a two-cent
  mistake into a video bill.** Attaching an image to `bytedance/seedance-2.5`
  forces `aspect_ratio: adaptive`, so the frame's own ratio becomes the
  finished clip's ratio whatever the video flags say. A 1.75 frame delivers a
  1.75 clip, and the correction is another paid generation. An
  almost-right image is the expensive outcome here, not the safe one — which
  is why a target that cannot be met **fails loudly** (exit `1` when no
  accepted size can cover it, exit `3` when the delivered file comes back too
  small) rather than emitting a frame that is 0.03% off and looks fine.
- **`SIZE_ACTUAL`, on every run, whether or not a target was set.** The
  response's own `size` field has now been wrong on two of the three models
  measured, and on `microsoft/mai-image-2.5-flash` it is a *three-way*
  mismatch — requested `1792x1024`, response said `1354x774`, file measured
  `1344x768`, three separate paid runs. So the script measures the file
  itself, prints it as its own line, and says on stderr when the two
  disagree. `openai/gpt-image-2` honouring `--size` exactly is **one run**
  (2026-09-04) and is recorded as one observation, not a guarantee — and that
  same run still needed a crop, because 1792x1024 is not 16:9 either.
  Honouring the request is not the same as producing a usable ratio.
- **`IMAGE_PATH` is still the file to attach, and the original still exists.**
  With a target, the cropped frame takes the plain output name and the API's
  untouched bytes are kept beside it as `<name>-uncropped.<ext>`, reported as
  `IMAGE_PATH_UNCROPPED`. An existing caller parsing `IMAGE_PATH` therefore
  gets the correct-ratio file without changing a line, and a human who wants
  a different crop still has the original. If the crop fails the plain name is
  never written at all — there is no state in which a wrong-ratio frame sits
  where the right one was promised.
- **An explicit `--size` is respected, never silently replaced.** It is only
  warned about, and only when it cannot cover a `--target-size`. The
  selection runs when `--size` was omitted.
- **`ffmpeg`/`ffprobe` are required only by the two new flags**, and are
  checked **before anything is spent** (exit `2`, the same class as a missing
  `curl`). They are not a new dependency for this repo —
  `ofox-video-core` already measures and cuts media with them — and `check`
  deliberately does not test for them, so a caller who never crops is
  unaffected. The failure message names the install command *and* the way
  out: drop the flag and everything else, `--dry-run` pricing included, still
  works.
- Documentation: `SKILL.md` gains "The size enum cannot express 16:9 or 9:16"
  with the full ratio table, the `adaptive` propagation consequence, and a
  per-model measurement table replacing the prose version; the scenario-skill
  rules gain a third "do not re-implement this" item for the crop step, since
  a scenario skill producing a video first frame should treat one of the two
  target flags as mandatory. `references/api-params.md` carries the same
  ratio table against the `size` field it belongs to.
- Tests: `references/test/targetsize.test.sh`, 45 cases — the enum's lack of a
  16:9 entry asserted rather than assumed, the two real hand-crops as
  regression cases, the size-selection choice per ratio and per pixel floor,
  exactness of the cropped ratio, both loud failures, the explicit-`--size`
  warning, malformed and conflicting targets, and the missing-`ffmpeg` guard
  including the case where no target flag is set and `ffmpeg` must not matter.
  The three existing suites pass unchanged (63 cases), for a total of 108.

## 1.5.0 — one real run on the new default model: 26x the estimate, a 400 on `standard`, and an exact `--size`

**A single paid `openai/gpt-image-2` run on 2026-09-04 — `--quality high
--size 1792x1024`, `USAGE_OUTPUT_TOKENS 5063`, `IMAGE_COST 0.154035` — billed
15.4 cents against this repo's own 0.6-cent estimate. About 26x.** Nothing
malfunctioned to produce that: the anchor said 196 output tokens, the script
printed the anchor, and the anchor had been measured at `low` / `1024x1024`
with nothing on the row recording that fact. Three findings came out of the
one run; all three are written down here, and **no behaviour changed** — the
only edit to `references/ofox-image.sh` is its comments, and all 63 tests in
`references/test/` still pass untouched.

- **Anchors now record the `--quality`/`--size` pair they were measured at.**
  `references/token-anchors.json` gains a `quality` and a `size` field on all
  three anchors, and `openai/gpt-image-2` gains an `additional_measurements`
  entry for the new point (5063 output tokens at `high` / `1792x1024`,
  `cost_per_image` 0.154035, `samples` 1, `cost_invoice_checked` **false** —
  the figure is the job's own reported `IMAGE_COST`, not an invoice line; the
  formula behind it is still reconciled against a real bill on
  `google/gemini-3.1-flash-image` only). The 196-token point is kept intact
  rather than corrected: it is still true for the pair it was measured at,
  which is exactly the point. A new `_what_the_count_does_depend_on` note
  states the rule the run bought — **an anchor is only valid for the pair it
  was measured at** — and `_how_to_add_a_row` now requires the pair to be
  recorded with any new count.
- **Deliberately *not* fixed: the lookup.** `.anchors[<model>].output_tokens`
  is still what `--dry-run` prints for every request, whatever quality and
  size it asks for, so the 26x gap is now documented rather than closed.
  Teaching it to select a point by pair — or to default to the dearest
  measured point — changes what every caller is quoted, which makes it a
  product decision, not a typo; `token-anchors.json` says to raise it the way
  `_chain_order_history` requires a chain reorder to be raised. Until then
  `SKILL.md` and `references/pricing.md` both tell the caller to read the
  anchor's own `quality`/`size` before relaying the line, and to quote the
  measured point that matches the run they are about to make.
- **No per-image figure in this skill is unqualified any more.** Every place
  that quoted "~0.6 cents" or "~2.67 cents" — the chain table in `SKILL.md`,
  the anchor table in `references/pricing.md`, the `MODEL_CHAIN` comment's
  own reasoning — now names the pair the figure belongs to. The chain table
  also carries the limit on its own ranking: the 4.5x gap between the top two
  models was measured at one pair only, and the 26x spread *within* one model
  is larger than it, so "which model is cheaper" is a narrower claim than it
  reads as.
- **`--quality` is a per-model enum, and `standard` is not portable.** The
  same run's first attempt was refused outright: `openai/gpt-image-2` +
  `--quality standard` → HTTP 400, `Invalid value: 'standard'. Supported
  values are: 'low', 'medium', 'high', and 'auto'`, **nothing billed**. That
  value had worked on every image call this repo had ever made — nine of them
  — and became an instant 400 the moment 1.4.0 moved `gpt-image-2` to the
  head of the chain: a per-model enum turning a default change into a
  breaking one. `SKILL.md`'s "Required flags" and
  `references/api-params.md` now carry a per-model pass/fail table, and
  `SKILL.md`'s own `--dry-run` example passes `high` instead of `standard`,
  since a dry run cannot catch this (the script validates `--quality` against
  the union of all models' values, so the rejection can only come from the
  API). The new error-table row records the status and the message and marks
  `error.type`/`error.code` as **not captured**, rather than borrowing the
  values from the row above it.
- **`gpt-image-2` honours `--size` exactly — and still needed a crop.**
  Request, response echo and the saved file's real pixels all read
  `1792x1024`, where `google/gemini-3.1-flash-image` disagrees two ways and
  `microsoft/mai-image-2.5-flash` three. This answers the open question 1.4.0
  asked someone to re-observe. It changes nothing about the standing advice,
  and the same run is why: 1792x1024 is 1.75, not 16:9, so the frame had to be
  cropped to `1792x1008` before a `bytedance/seedance-2.5` job would inherit
  the right ratio (an attached frame forces `aspect_ratio: adaptive`).
  **Measure the file and crop regardless of model** — what varies per model is
  how large the correction is, not whether one is needed.
- **1.4.0's "`gpt-image-2` has no output samples in this repo yet" is
  retired.** It has one, and the two surprises above are what it produced.
  One run is still one run: pin `--model microsoft/mai-image-2.5-flash` if the
  look matters more than the price for a given use case.
- `references/pricing.md`'s anchor table said `gpt-image-2` was measured on
  2 calls where `token-anchors.json` says 3. Corrected to 3, per that table's
  own rule that the JSON wins.

## 1.4.0 — the priority chain's order reversed: `gpt-image-2` first

**`MODEL_CHAIN` now resolves to `openai/gpt-image-2` by default, not
`microsoft/mai-image-2.5-flash`.** New order:
`openai/gpt-image-2 microsoft/mai-image-2.5-flash
google/gemini-3.1-flash-lite-image microsoft/mai-image-2.5`.

This is a deliberate reversal of a deliberate decision, not an unreviewed
reorder. On 2026-09-02, with `gpt-image-2` already shown to cost ~4.5x less
per image than `mai-image-2.5-flash` despite its higher per-token rate
(196 output tokens against 1024, measured that day), the repo owner looked
at both figures and kept `mai-image-2.5-flash` first anyway — recorded in
`references/token-anchors.json`'s chain-order history note, along with the
instruction that the next person who wanted to reorder the chain should
raise it first. On 2026-09-04 the repo owner did exactly that and asked for
`gpt-image-2` first instead. This release carries out that request.

- **`SKILL.md`'s priority-chain table is now ranked by measured cost per
  image**, not by the rate card's per-output-token price — the two rankings
  disagree, and the table used to be ordered by the wrong one. A new "The
  2026-09-04 reversal" subsection records the history above in the skill's
  own docs, not only here.
- **`MODEL_SOURCE request` is now the common case for a default `generate`
  call**, not an edge case — `openai/gpt-image-2` never echoes a `model`
  field, and it is now the model a default call resolves to.
- **A new, unrelated `SIZE` finding surfaced while re-checking this
  default**: `microsoft/mai-image-2.5-flash` — now second in the chain —
  was found, through three real calls made by a downstream scenario skill,
  to disagree with itself on `--size` three ways at once (requested
  `1792x1024`, response echoed `1354x774`, saved file `1344x768`), not just
  the two-way mismatch already documented for `google/gemini-3.1-flash-image`.
  Neither `SIZE` finding has been checked against `gpt-image-2`; both
  `SKILL.md` and `references/pricing.md` now say so and ask for a fresh
  observation the next time a scenario skill generates with the new
  default. `gpt-image-2` also has no generated-output samples in this repo
  at all yet — its measured figures are token counts, not a look at what it
  draws.
- **Test coverage moved with the default**: `dryrun.test.sh`'s assertions
  that the default `generate --dry-run` resolves to and prices the chain's
  preferred model now target `gpt-image-2`'s own anchor (196 tokens, ~0.6
  cents) instead of `mai-image-2.5-flash`'s; the anti-borrow check now
  guards against either previous default's token count (1120 or 1024)
  leaking into the new one's estimate.
- `references/token-anchors.json`'s `_why_the_cheapest_measured_model_is_not_first`
  note is renamed `_chain_order_history` and now records both decisions —
  keeping mai-flash first on 2026-09-02, then reversing that on 2026-09-04 —
  rather than only the first one. The rule it carries is unchanged: raise a
  reorder before making it.

## 1.3.0 — the chain's top models are measured, and a missing `model` echo no longer costs you the cost

**Bug fix: `openai/gpt-image-2` runs printed no `IMAGE_COST` at all.** Its
responses carry no `model` field. The old code defaulted that to the literal
string `"unknown"`, looked `"unknown"` up in the rate table, found nothing, and
reported `could not compute a cost` — for a request the script had built itself
from a model id it knew. Two real, paid calls were billed with no cost figure.

The fallback deliberately keeps two cases apart rather than collapsing them:

- **No `model` field** (absent, `null` or empty) — nothing was contradicted, the
  upstream just didn't echo. The **requested** id is used for display and
  pricing, and the new `MODEL_SOURCE request` line says so, so nobody reads the
  `MODEL` line as something the API confirmed.
- **A `model` field naming a different id** — that is an upstream route, alias
  or downgrade. The **echoed** id wins for both display and pricing, a warning
  goes to stderr, and `MODEL_REQUESTED` records what was asked for. Rewriting it
  back to the requested id would price the call off the wrong rate card and
  erase the only evidence the swap happened.

**New output lines**: `MODEL_SOURCE` (`response` | `request`) on every
successful generate, and `MODEL_REQUESTED` only when it differs from `MODEL`.
`MODEL_SOURCE` is unconditional for the same reason `Estimated cost:` is — an
agent can relay a line it was told to expect, but cannot notice one that was
never printed.

**Token anchors for the chain's top two models** (`references/token-anchors.json`),
so a default `generate --dry-run` now quotes a rough figure instead of "cannot
be predicted": `microsoft/mai-image-2.5-flash` 1024 output tokens (~$0.0267/image),
`openai/gpt-image-2` 196 (~$0.0060/image). Both measured 2026-09-02 at
`--quality low --size 1024x1024`.

- **The count does not depend on the prompt.** Two unrelated prompts produced
  byte-identical `usage` on both models; Gemini's three calls reported 1120
  output tokens at input lengths of 8, 51 and 79. `output_tokens` looks fixed by
  model + size + quality — which is the whole reason one anchor can price a
  later run with a different prompt. Two samples per model, not a proof.
- **The dollar figures are formula-derived and invoice-unchecked.** Only
  `google/gemini-3.1-flash-image` has ever been reconciled against a real bill;
  `cost_invoice_checked` records that per row and must not be flipped without an
  invoice line. The model page alone once supported two readings 20x apart.
- **Cheaper per token is not cheaper per image.** `gpt-image-2` costs 15% more
  per output token than `mai-image-2.5-flash` and **4.5x less per image**
  (196 tokens vs 1024). `MODEL_CHAIN` was ordered on the per-token rate; it is
  not reordered here on two samples, but `SKILL.md` and `references/pricing.md`
  now flag that the rate card is the wrong thing to rank on.

## 1.2.0 — a default model, a `--dry-run`, and the gate that pays for both

**Behavior change: `--model` is now optional.** Omit it (or pass `auto`) and
the script walks a cheapest-first priority chain and uses the first model that
is actually available. Passing `--model <id>` still pins any model, exactly as
before, so existing callers are unaffected.

- **The chain lives in one place**, `MODEL_CHAIN` in `references/ofox-image.sh`:
  `microsoft/mai-image-2.5-flash` → `openai/gpt-image-2` →
  `google/gemini-3.1-flash-lite-image` → `microsoft/mai-image-2.5`, cheapest
  first by the catalog's `output_image` rate. Skills built on this one resolve
  a model by calling the script; none of them keeps a copy of the list.
- **Fallback is reported, never silent.** A preferred model that is missing
  from the model list, doesn't serve `/v1/images/generations`, or is
  deprecated gets skipped, and the run prints `MODEL_FALLBACK_FROM`,
  `MODEL_FALLBACK_REASON` and `MODEL_PRICE_DELTA` ("1.80x the preferred rate").
- **The model is resolved before anything is quoted.** There is deliberately
  no path where the model is chosen after a price was approved.
- **New `--dry-run`**, matching `ofox-video-core`'s: validate, resolve the
  model, create and check `--out-dir`, build the payload, print the estimate,
  then return — before the `POST`. Nothing submitted, nothing billed, and no
  `OFOX_API_KEY` required, so a job can be priced before signing up.
- **The estimate is honest about being rough, or refuses.** Images bill per
  output token and the count only exists in the response, so the figure is
  anchored to a real measured call with the *same* model, from the new
  `references/token-anchors.json`, and is labelled `ROUGH`. A model with no
  measurement gets "cannot be predicted" and the reason — never another
  model's token count, which in an approval table would be indistinguishable
  from a measured one. Exactly one `Estimated cost:` line either way, printed
  on a real run too.
- `google/gemini-3.1-flash-image` is the only measured anchor so far (1120
  output tokens). The chain's top two models are recorded as **awaiting
  measurement**, which is why a default `generate --dry-run` says the cost
  cannot be predicted today. Two real calls fix that; nothing else does.
- **Why a default is acceptable now, when 1.1.0 documented refusing one as
  deliberate:** the objection was that defaulting silently picks a price. The
  new shared approval gate
  (`ofox-video-core/references/approval-gate.md`) puts the resolved model and
  its cost in front of the user before every spend, so it no longer does. That
  reasoning is written into SKILL.md next to the default, not just here.
- `models` now prints the chain and the model it resolves to right now.
- **An unquantifiable price gap names the right model.** When one of the two
  rates is missing, `MODEL_PRICE_DELTA` says which model lacks a published
  rate. It no longer blames the preferred model in every case, and no longer
  claims the missing rate was "part of why it was skipped" — `resolve_model`
  never looks at pricing when deciding what to skip, so that reason could
  not be true. A wrong reason in an approval table is worse than no reason.
- **A chain with nothing usable in it says so on stdout.** That case sets
  `MODEL_CHAIN_EXHAUSTED` (not the fallback fields — nothing was fallen back
  *to*), so the caller can tell the user that the model in the table is one
  the script already expects the API to reject. Previously the reason was
  recorded internally and dropped from the structured output, leaving only
  stderr prose.
- New `references/test/dryrun.test.sh` (25 cases: the dry run's early return,
  the single estimate line, every fallback reason, each price-delta branch,
  the exhausted chain, and that no anchor is ever borrowed across models).
  Free by construction.

## 1.1.0 — every image model Ofox serves, not a hardcoded three

- **`--model` is checked against the live model list.** It was previously
  matched against three hardcoded ids, so the script locally rejected the other
  eleven models the API actually serves — `openai/gpt-image-1.5`,
  `google/gemini-3-pro-image`, `volcengine/doubao-seedream-5.0-pro`,
  `microsoft/mai-image-2.5` and the rest all failed before a request was made.
- A model that exists but doesn't serve `/v1/images/generations` (a video
  model, say) is now rejected with that specific reason.
- **New `models` subcommand**: lists the image models and their per-output-token
  price. No API key needed — `GET /v1/models` is public.
- Same fallback ladder as `ofox-video-core`: fresh cache (24h) → live → stale
  cache → bundled `references/models-snapshot.json` → no check. Every fallback
  is announced. An unknown id is rejected against a live list but deferred to
  the API when only a snapshot is available.
- **Unchanged on purpose**: `--size`, `--quality`, `--output-format` and
  `--background` stay hardcoded from the docs. Unlike the video API, the models
  endpoint exposes no per-model capability data for image models — there is no
  `image_attributes` to match `video_attributes` — so only the model id can be
  validated dynamically.
- `--model` stays required with no default, now documented as deliberate: the
  image models differ roughly 4x in price with no obvious winner, so defaulting
  would silently pick a price.
- New `references/refresh-snapshot.sh` and `references/test/validation.test.sh`
  (18 cases; accept cases warm the model cache from the real endpoint and then
  point the API base somewhere unroutable, so no case can reach the real
  generations endpoint even with a live key exported).
- Frontmatter: top-level `version` and `metadata.openclaw.homepage`/
  `envVars`/`primaryEnv` for ClawHub.
