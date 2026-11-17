# Video pricing

**The script does not read this file.** `ofox-video.sh` fetches live per-second
rates from the catalog endpoint and prints an estimate before it submits
anything. What lives here is the explanation — which model is cheap, why that
matters, and what to watch out for — plus a dated snapshot for reading offline.

For current numbers:

```bash
bash references/ofox-video.sh providers                      # seedance-2.5
bash references/ofox-video.sh providers bytedance/seedance-2.0-mini
```

That reads `GET /v2/models/catalog/{owner}/{slug}?include=provider_price`,
which is public and needs no API key, and prints every upstream's full
resolution x mode price matrix.

## The cheap-to-expensive ladder

Text-to-video, per second, cheapest first. **Snapshot as of 2026-09-22** — treat
the shape as durable and the digits as stale until checked. Promotional rates
can expire without a code change: Seedance 2.5's 1080p promotion ended between
2026-08-30 and 2026-09-22, moving the live rate from $0.48 to $0.60 per second.

| Model | 480p | 720p | 1080p | 4k | Duration |
|---|---|---|---|---|---|
| `bytedance/seedance-2.0-mini` | $0.02 | $0.04 | — | — | 4-15s |
| `bytedance/seedance-2.0-fast` | $0.042 | $0.091 | — | — | 4-15s |
| `bytedance/seedance-2.0` | $0.063 | $0.15 | $0.31 | $1.24 | 4-15s |
| `alibaba/wan-2.7` | — | $0.10 | $0.15 | — | 2-15s |
| `bytedance/seedance-2.5` | $0.11 | $0.24 | $0.60 | — | 4-30s |
| `alibaba/happyhorse-1.1` | — | $0.14 | $0.18 | — | 3-15s |

**Why this table matters even though the script doesn't read it:** at 720p,
`seedance-2.0-mini` is 6x cheaper than `seedance-2.5`. Five 4-second drafts
cost $0.80 on mini versus $4.80 on 2.5. When someone will generate several and
keep one, drafting cheap and rendering the keeper on 2.5 turns a $5 experiment
into a $1 one. That is the whole argument for `batch`, and it survives any
repricing.

Two things to keep straight:

- **Don't switch models on a user's behalf.** A different model is a different
  look, not just a different price. Offer the ladder, let them choose.
- **Image-to-video bills at t2v rates.** The v2v tier applies only when a
  *video* is the input. Verified by a real i2v run billing 4s x $0.11 at 480p.

Video-to-video costs more everywhere it is offered — Seedance 2.5:
$0.14 / $0.30 / $0.71 for 480p / 720p / 1080p.

## Provider does not change the price

Seedance is served by two upstreams (`byteplus`, `volcengine`) and their price
matrices were identical when measured, tier for tier. Pinning one is a region
and moderation decision, never a cost one — see `api-params.md`. The estimate
reads the pinned provider's own card anyway, so if that ever stops being true
the number follows automatically.

## How the estimate is produced

Order of preference: fresh catalog cache (24h) -> live fetch -> stale cache ->
bundled `pricing-snapshot.json` -> **no estimate at all**.

That last rung is deliberate. If no verified rate can be had, the script says
the estimate is unavailable and proceeds — it never prints a number it cannot
back up, because a wrong estimate is worse than no estimate when someone acts
on it before spending. Regenerate the bundled snapshot with
`bash references/refresh-snapshot.sh`.

**Never quote `output_video_per_second` from `GET /v1/models`.** It is not
consistently the cheapest tier or the default tier: for `seedance-2.5` it
reports the 480p rate ($0.11) while the model defaults to 720p ($0.24), which
would understate a default job by more than half.

## Seedance 2.5 pricing

Source: the public model catalog read by `ofox-video.sh providers` (verified
2026-09-22). Prices can change — re-run that command before quoting a number
you intend to hold someone to, particularly for anything beyond a quick
estimate.

## Per-second rate

| Resolution | Text-to-video (t2v) | Video-to-video (v2v) |
|---|---|---|
| 480p | $0.11/s | $0.14/s |
| 720p | $0.24/s | $0.30/s |
| 1080p | $0.60/s | $0.71/s |

- Duration range: 4–30 seconds, any integer.
- Aspect ratios: 21:9 / 16:9 / 4:3 / 1:1 / 3:4 / 9:16 / adaptive.
- Audio is on by default (`generate_audio: true`) and is not billed
  separately in the table above — the per-second rate already covers it.
- "v2v" (video-to-video) applies when the request includes video input
  (e.g. a video in `input_references`); the two Seedance 2.5 scenario
  skills built on `ofox-video-core` use text-to-video and first/last-frame
  image-to-video only, so the **t2v** column is what applies to them.

## Cost formula

**Estimate — show this *before* generating, so the user isn't surprised:**

```
estimated_cost = duration_seconds * price_per_second(resolution, mode)
```

Example: a 5-second, 1080p, text-to-video clip ≈ `5 * 0.60 = $3.00` at the
2026-09-22 rate. Check the live catalog if the number matters.

**Actual — report this *after* generating, don't recompute it:**

```
actual_cost = usage.video_cost   # from the poll response, once status is "completed"
```

`usage.video_cost` is a string with 10 decimal places and is the number of
record — it may differ slightly from the estimate (e.g. rounding, or a
promo rate that changed between estimate and completion). `ofox-video.sh`
prints this value directly (`VIDEO_COST`); never substitute the estimate
for it in a final report to the user.
