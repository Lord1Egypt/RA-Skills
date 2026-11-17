# The approval gate

**One spec, shared by every Ofox skill in this repo** — `ofox-video-core`,
`ofox-image-core`, and every scenario skill built on them, whatever it is
called (`seedance-*`, `keyframe-animation`, `product-demo`, and any added
later — the rule is about spending someone's money, not about a name). They
link here rather than each restating the rule, because four paraphrases of
"show the price first" drift into four different rules, and the one that
drifts is the one that spends someone's money without asking.

It lives in `ofox-video-core/references/` because that is the one skill every
scenario in this repo depends on. If you are reading a skill that links here
and the link missed, the rule below still applies either way, and there are
two reasons it can miss. The link is written as `../ofox-video-core/...`,
which is how skills.sh, ClawHub and `npx ofox-skills` name the directory;
LobeHub unpacks each skill as `ofoxai-skills-<name>`, so there it is
`../ofoxai-skills-ofox-video-core/...` and the file is present under a name
the link doesn't use — the skill's own "Where the core skill lives" section
(called "Where the two core skills live" in a skill that uses both) has the
probe that finds it. Only if that probe comes back empty was the
skill really installed without `ofox-video-core`. Installing it is the user's
call, not yours — hand over the command rather than running it: skills.sh is
`npx skills add ofoxai/skills --skill ofox-video-core`, this repo's wrapper is
`npx ofox-skills ofox-video-core`, and on LobeHub or ClawHub it is
`ofox-video-core` from the same publisher. Ask for the one missing skill
rather than the whole repo, and give all three routes — naming one installer
tells a user of the other two to abandon theirs.

## The rule

**Never send a billable request until the user has seen a cost table and
said yes.**

Not "mentioned the price in a sentence". A table, then an explicit yes, then
the spend. The user is not only approving a number — they are approving a
model, a prompt, a resolution and a quantity, any of which can waste the
money more thoroughly than a wrong price would.

## `--approved`: the rule has a hook in the tool now

`ofox-video.sh` **refuses to run a billable subcommand without `--approved`**
(since `ofox-video-core` 2.0.0). The four it covers are `generate`, `create`,
`batch` and `chain` — the only ones that reach a request that bills. Free
subcommands are untouched, `poll` deliberately included: it is how a job you
have already paid for gets collected, so gating it would strand money rather
than protect it.

So the flow is now three commands' worth of shape rather than two:

1. `--dry-run` produces the number. It needs no `--approved` and no API key.
2. The table goes in front of the user, and the user says yes.
3. The same command runs again with `--dry-run` swapped for `--approved`.

**Be exact about what this flag is, in anything you write for a user.** It
records a stance; it cannot prove one. Nothing in a shell script can observe
the conversation you had, and an agent can type `--approved` without having
shown anyone a price — exactly as it could previously just run the command.
What changed is that skipping this spec is no longer the default behaviour: it
now has to be written into the command, where a transcript shows it and a
reviewer can object. **Do not write "approval is enforced".** The rule above
is still the rule, and it is still yours to follow.

`ofox-image.sh` has no equivalent flag today. The rule binds there in exactly
the same way; only the reminder is missing.

## The table

Every row is one billable unit. Required columns:

| Model ID | Type | Parameters | Unit price | Qty | Est. cost |
|---|---|---|---|---|---|
| `bytedance/seedance-2.5` | video (t2v) | 8s, 720p, 16:9 | 24 cents/s | 1 | ~$1.92 |

- **Model ID** — the full id that will actually be sent, resolved before the
  table is printed. Never "the default" or "the cheapest one"; if a fallback
  happened, name the model that won and say what it replaced (see below).
- **Type** — `image`, or `video (t2v)` / `video (i2v)` / `video (v2v)`. What
  the job is and what tier it bills at are two different facts, and the table
  needs both: an image-to-video job bills at the **t2v** tier (verified by a
  real i2v run billing 4s x $0.11 at 480p — the t2v rate, not the v2v $0.14),
  and only a *video* input moves a job to v2v, where 1080p Seedance 2.5 is
  $0.71/s against t2v's $0.60/s. Take the tier from the dry run, never from
  an assumption about which input types "ought to" cost more.
- **Parameters** — whatever moves the price or the result: duration,
  resolution, aspect ratio, size, quality, takes, seed if pinned.
- **Unit price** — per second for video, per output token for an image.
- **Est. cost** — copied from the script's own estimate line. Not recomputed.

**Show the full prompt with the table, not just the price.** The user is
paying for the prompt — what the character looks like, how the camera moves,
whether their dialogue survived word for word. A clip that costs exactly what
you quoted and shows a character they never pictured is still a wasted job.
Put the prompt text in the message, in full, next to the table.

## Where the numbers come from

**Only from the script's `--dry-run` output. Never from your own
arithmetic.**

The two scripts live in two different skills, so the path depends on where
you are running from. From a scenario skill's own directory:

```bash
bash ../ofox-video-core/references/ofox-video.sh generate --dry-run \
  --prompt "..." --duration 8 --resolution 720p
bash ../ofox-image-core/references/ofox-image.sh generate --dry-run \
  --prompt "..." --quality high
```

Those two lines assume each core sits beside the scenario skill under its own
name. Under a LobeHub-style install the sibling is
`../ofoxai-skills-ofox-video-core` (and `../ofoxai-skills-ofox-image-core`);
substitute whatever the calling skill's core-location probe printed — the
section is "Where the core skill lives", or "Where the two core skills live"
in a skill that uses both. A quote that can't be produced because the path
missed is not a reason to skip the gate — resolve the path and quote it.

From inside `ofox-video-core` or `ofox-image-core` itself, its own script is
`references/ofox-<video|image>.sh`. There is no `references/ofox-image.sh`
under `ofox-video-core` — that path fails with "no such file", which is a
confusing way to discover you skipped the quote.

Both print exactly one `Estimated cost:` line, always — including when they
cannot produce a figure, in which case the line says why. Relay whichever
line you get. Multiplying a rate by a duration yourself is how a table ends
up quoting a tier the job will not actually bill at.

`--dry-run` validates everything, resolves the model, builds the payload and
stops before the request. Nothing is submitted, nothing is billed, and no
`OFOX_API_KEY` is needed — pricing is exactly what someone does *before*
signing up.

The estimate a *real* run prints appears microseconds before the request goes
out. By the time you could relay it, the job exists and is billable. That is
what `--dry-run` is for.

This is also why `--dry-run` is never behind `--approved`: the quote is how
the number being approved gets produced, so a gate in front of it would close
the only route through itself.

### When there is no estimate

**Show the table anyway, write "cannot be predicted — `<reason>`" in the cost
column, and still wait for a yes.** Approving an unknown price is the user's
call to make; skipping the gate because the number is missing is not.

This is the normal case for images: an image bills per output token, and the
token count only exists once the response comes back. `ofox-image.sh` can only
produce a figure for a model whose token count was measured on a real earlier
call (`ofox-image-core/references/token-anchors.json`), and it labels that
figure **ROUGH**. Relay it as rough. Never present it as a quote, and never
borrow one model's measured token count for another model — a borrowed number
is indistinguishable from a measured one and is worth less than no number.

**There is no flat per-image price, and a ROUGH figure is only valid for the
`--quality`/`--size` pair its anchor was measured at.** Measured 2026-09-04:
`openai/gpt-image-2` spends 196 output tokens at `low` / `1024x1024` and
**5063** at `high` / `1792x1024`, so the same model is about 0.6 cents or
15.4 cents depending on two flags — and a real approval table quoted the
0.6-cent figure for a frame that billed 15.4, because the script then looked
up one count per model and printed it whatever the flags were.

**Since `ofox-image-core` 1.7.0 the lookup is pair-aware, so the estimate
line is now the thing to relay verbatim — including its label.** Two shapes,
and the label is not decoration:

- `ROUGH ~$X (… measured <date> at --quality <q> --size <s>)` — measured at
  the pair this request actually sends. Relay as rough.
- `ROUGH UPPER BOUND ~$X (… measured <date> at --quality <q> --size <s>)` —
  nothing has been measured at the request's own pair, so the figure is the
  **dearest** point that model has, quoted as a ceiling. Say "ceiling" in the
  table, and name the pair the line names — it is the pair the number came
  from, not the one being requested. `auto` for either flag, and an omitted
  `--size`, take this path too, since the API picks and no pair can be named.

Two things not to do. **Do not substitute a figure of your own** for the one
the line printed — hand-correcting a pair the script already matched is how a
table drifts back to being wrong. And **do not quietly drop an `UPPER BOUND`
to a cheaper measured point** because it looks closer to the request; nothing
is interpolated between measured points, and the ceiling is deliberately
high. Where the estimate reads `Weak ceiling`, that model has exactly one
measured pair, so the "bound" is the dearest by default rather than one
anyone has tested — pass that sentence through too. The anchors and their
recorded pairs are in `ofox-image-core/references/token-anchors.json`.

### When a model fell back

The image chain is a priority, not a lock: if the preferred model is
unavailable, the script drops to the next one and reports
`MODEL_FALLBACK_FROM`, `MODEL_FALLBACK_REASON` and `MODEL_PRICE_DELTA`. All
three go in front of the user, alongside the model actually chosen. "We are
using B instead of A because A is deprecated, and B costs 1.8x more per
output token" is a fact the user may want to act on — by picking a different
model, or by not spending at all.

When the price gap cannot be quantified, `MODEL_PRICE_DELTA` says which of
the two models has no published rate. Relay that as it stands; do not round
it up into "it costs more" — an unknown gap is not a known one.

If instead you get `MODEL_CHAIN_EXHAUSTED`, nothing in the chain is usable
and the model in the table is one the script expects the API to reject. Say
that plainly before asking for approval. A yes to a job that cannot run is
not consent to the retry you would pick afterwards.

## Batches get an itemised table, not one total

Multiple takes, multiple shots, multiple keyframes: **one row each, plus a
total row.** A total on its own hides the shape of the spend, and the shape
is the decision. Four 480p drafts and one 1080p master can come to nearly the
same money and mean completely different things.

When one usable clip is the goal, say plainly that the **total** is what that
clip cost — `BATCH_COST_TOTAL`, not `BATCH_COST_PER_TAKE`. If one take in
four is usable, the per-take figure understates its cost by 4x.

**A batch that runs concurrently has to be quoted before it starts, because
there is no longer a partway through it.** `ofox-video.sh batch` submits every
take up front and then waits for them in parallel (since 1.15.0). That does
not change the total by a cent, and it does take away one thing the old serial
version had: with takes submitted one at a time and waited for in turn, a user
watching a bad take land could interrupt before the next was billed. Now the
whole total is committed within seconds of the command running. The exchange
is a batch that takes one clip's wall clock instead of N, and the price of it
is that the cost table is the only place the run can still be stopped.
`batch --dry-run` prints exactly one `Estimated cost:` line for the whole
batch plus the `CONCURRENCY` it would use; that is the number the table gets
rows for, and the yes has to arrive before the command runs at all.

## Two-phase flows: two approvals

A skill that generates an image and then feeds it into a video (today:
`seedance-anime-drama`) asks **twice**, not once.

The reason is not politeness. Phase 2's prompt depends on what phase 1
produced: the video opens on that exact image. Before the image exists, the
user cannot tell whether it is worth paying to animate — and for a skill
whose entire selling point is character consistency, what the character looks
like is only knowable by looking at it.

- **Approval 1 (image)**: the image table, plus a heads-up of roughly what
  phase 2 will cost, so nobody agrees to a first step without knowing the
  size of the second.
- **Approval 2 (video)**: the video table, plus **what phase 1 actually
  billed** and the **running total**. Quote the video phase at the tier the
  dry run reports for the job as configured, first frame attached and all.

If the user rejects phase 2, phase 1's spend still happened. Say so; do not
present the image as free because the video never ran.

## Afterwards: the actual bill

An estimate is never a bill. Once the job finishes, report the real figure
the script printed — `VIDEO_COST` from the job's own usage, `IMAGE_COST`
computed from the response's own token counts — as money (`$1.92`), not as a
raw ten-decimal string. If the actual differs noticeably from the estimate,
say so rather than letting the earlier number stand.

## What counts as approval

- An explicit yes to **this** table. Not "sounds good" to an earlier,
  different plan.
- Approval is for the table shown. Change the model, resolution, take count,
  duration or prompt afterwards and it is a **new** table needing a new yes —
  those are the four things that move the price and the one thing that
  decides whether the output is usable.
- A user who says "just do it, stop asking" has approved the current job.
  Take them at their word for that job; quote the next one anyway if it costs
  materially more.
- Silence is not approval. Neither is the absence of an objection.

## Why this exists at all

`ofox-image-core` used to refuse to default `--model`, on the grounds that the
image models differ ~4x in price and picking one would silently pick a price
on the user's behalf. It now defaults to the cheapest available model, and
**this gate is the exchange**: the price is put in front of the user before
every spend, default or not, so the default no longer decides anything
quietly. Weaken the gate and that trade stops holding.
