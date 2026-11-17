# Quota Checking (MiniMax Token Plan Plus)

How to check MiniMax Token Plan quota before running a music, speech, or
image generation, how to interpret the result, and how to bake the check
into a batch so the run stops instead of failing mid-way. Load this before
any multi-output, quota-sensitive, or batch cloud run.

> **Scope rule (Token Plan Plus, verified 2026-07-30).** The Token Plan
> Plus tier covers **`mmx music`** (generate + cover), **`mmx speech`**
> (synthesize + voices), and **`mmx image`** (generate). It does **not**
> cover `mmx video` — `mmx video generate` is exposed by the CLI but is
> **blocked on Plus** by a 3-hour rolling rate limit even when the
> 5-hour quota has headroom. `mmx video` is **Hailuo** and lives on the
> Max/Ultra plans, not Plus. Use LTX-Video 2.3 Q4 local (Phosphene) for
> SEF work on Plus.
>
> See
> [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
> for the full Token Plan scope and the rate-limit caveats, and
> [`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) for the
> wrapper pattern that surfaces quota snapshots inside receipts.

---

## Quota fundamentals — Luis's Token Plan Plus

The Token Plan Plus quota model has two coupled axes: a 5-hour rolling
window (the real ceiling) and a weekly window (inactive on Plus for
Luis because of his early-adopter tier).

| Window | Limit on Plus | Where to check | Notes |
| --- | --- | --- | --- |
| **5-hour rolling** | ~4,500 M2.7-equivalent calls per 5h | `mmx quota show` / `/v1/token_plan/remains` | The real ceiling. MiniMax documents this as "credit-based"; older docs say 120 RPM, but the 5h pool is what throttles. |
| **Weekly** | Inactive (`current_weekly_status: 3`) | Same endpoint | Luis's early-adopter tier does not enforce the weekly cap. Do **not** pause work because "weekly is close". |
| **API RPM** | 120 RPM | HTTP 429 | Soft ceiling; the Token Plan pool usually trips before RPM does. |

### Coverage by `mmx` subcommand (Plus scope)

| Subcommand | Covered on Plus? | Estimated cost per call | Notes |
| --- | --- | --- | --- |
| `mmx music generate` | ✅ | ~1 unit | Standard song generation; `music-2.6` / `music-2.6-free` |
| `mmx music cover` | ✅ | ~1 unit (sometimes 2) | Cover workflow — melody-preserving. Two-step uploads extra metadata. |
| `mmx speech synthesize` | ✅ | ~1 unit per ~10k characters | TTS, voice cloning, voice design. Long texts may split. |
| `mmx image generate` | ✅ | ~1 unit per image | Image-01; always saves JPEG regardless of extension. |
| `mmx vision describe` | ✅ | ~1 unit | Multimodal VLM — billed against Plus. |
| `mmx search query` | ✅ | ~1 unit | Web search MCP — same pool. |
| `mmx video generate` | ❌ | n/a | Hailuo = Max/Ultra only. **Blocked on Plus** by a 3-hour rolling rate limit, even when the 5h quota is empty. Use local LTX-Video 2.3 Q4 via Phosphene. |

### Cost estimates per operation (field-observed, treat as order-of-magnitude)

These estimates are useful for sizing a batch before you start. **Treat
them as floor values, not actual costs.** Live observation (Luis's
`subscriptions.md` log, 2026-07-25) showed 5 `mmx` invocations consuming
28% of the general quota — an effective cost of ~12.6 units per call.
The floor estimates below assume a single short operation; any non-trivial
vocal generation, long-form TTS, or heavy search query can blow past the
floor by 3–5×.

| Operation | Estimated cost | Source / sanity check |
| --- | --- | --- |
| `mmx music generate` (one song, ~3 min, with lyrics) | **~1 unit** | Single full song fits inside one M2.7-equivalent call; vocal + instrumental pipelines share the same Plus unit. |
| `mmx music cover` (one-step) | **~1 unit** | The one-step cover uploads the audio, ASR-transcribes, then generates in one call. |
| `mmx music cover` (two-step) | **~2 units** | Two-step uploads for `cover_feature_id`, then a generation call. |
| `mmx speech synthesize` (one short clip, < 10k chars) | **~1 unit** | Long narration may split into multiple units; charge roughly per 10k characters. |
| `mmx image generate` (one image) | **~1 unit** | Image-01 default model; cost is independent of resolution within Plus defaults. |
| `mmx vision describe` (one image) | **~1 unit** | Native multimodal VLM on Plus. |

> **Sanity rule.** When you do a quick mental model: every `mmx music`,
> `mmx speech`, `mmx image`, `mmx vision`, and `mmx search` call ≈ **1
> Plus unit** on average — but real cost varies. The dangerous assumption
> is that "1 call = always 1 unit": a long vocal generation, a deep
> search query, or a long-form speech synthesis can burn more. The
> `subscriptions.md` live-test (2026-07-25) showed **5 `mmx` invocations
> consumed 28% of the general quota (~12.6 units per call, 3.5× the naive
> estimate)** — so the actual cost is much higher than the order-of-magnitude
> floor above. **Always run a live `mmx quota show` before any batch >5 calls**
> and abort if headroom is less than 2× the naive estimate.

### Multipliers from the official Token Plan reference

MiniMax's published reference (per `platform.minimax.io` Token Plan page):

> "Estimated assuming ~50K tokens per M3 call (monthly) ~34,000 calls ~
> 102,000 calls ~ 250,000 calls. M2.7 calls (reference)"

Translation for the music/speech/image subset:

- `mmx` calls cost roughly **1 unit** each (M2.7-equivalent).
- Vision / multimodal calls can be slightly more expensive per call when
  the model loads image tokens, but on Plus they still fit comfortably
  inside the 4,500/5h pool.
- The 5-hour window is **rolling** — it does not reset on a clock; it
  slides. So a heavy 4-hour run leaves you with 1 hour of "refill" rather
  than a full reset.

---

## Quota check commands

There are two ways to check the live state: the `mmx` CLI wrapper, and
the underlying HTTP endpoint. Both work; use whichever fits the calling
script.

### 1. The `mmx` CLI

```bash
# Default: human-readable output.
mmx quota show

# Machine-readable for scripts and preflight checks.
mmx quota show --output json
```

The CLI is the simplest path because it handles auth via the existing
`MINIMAX_API_KEY` (or `MINIMAX_CODE_PLAN_API_KEY`) environment variable
and returns the same payload as the HTTP endpoint below.

### 2. The HTTP endpoint

Direct call against the Token Plan remains endpoint. This is what `mmx
quota show` does under the hood; useful when the CLI is missing, when
you want to bypass the CLI's text formatting, or when you want to script
a pre-flight check from a language without a CLI binding.

```bash
curl -s 'https://www.minimax.io/v1/token_plan/remains' \
  -H "Authorization: Bearer $MINIMAX_API_KEY" | jq .
```

**Auth note.** The endpoint accepts the same `MINIMAX_API_KEY` (or
`MINIMAX_CODE_PLAN_API_KEY`) the `mmx` CLI uses. Both env-var names
work because MiniMax's auth layer treats them as the same key in
practice. Luis's setup uses `MINIMAX_CODE_PLAN_API_KEY` (Token Plan
Plus); older guides sometimes reference `MINIMAX_API_KEY`. Verify which
one is set on the host before wiring this into a CI job:

```bash
# Discover which key is exported.
env | grep -i minimax
# Expected (Luis's laptop, 2026-07-30):
# MINIMAX_CODE_PLAN_API_KEY=...
# MINIMAX_API_KEY=...  # optional alias if set
```

### Response format

The response is a JSON object. Field names vary slightly between CLI
versions; the most stable fields are:

```json
{
  "model_remains": [
    {
      "model_name": "music-2.6",
      "current_interval_usage_count": 12,
      "current_interval_status": 3,
      "current_weekly_count": 78,
      "current_weekly_status": 3
    },
    {
      "model_name": "speech-2.8-hd",
      "current_interval_usage_count": 12,
      "current_interval_status": 3,
      "current_weekly_status": 3
    }
  ],
  // Aggregate reading comes from "general" bucket in model_remains[]
}
```

Field-by-field:

| Field | Meaning |
| --- | --- |
| `model_remains[]` | Per-model breakdown. One entry per model the account has touched. |
| `model_name` | The model id (`music-2.6`, `speech-2.8-hd`, `image-01`, etc.). |
| `current_interval_usage_count` | Units consumed in the current 5-hour rolling window. |
| `current_interval_status` | `3` = healthy. Other values indicate throttling; treat anything other than `3` as "do not start a new batch". |
| `current_weekly_count` | Units consumed in the current weekly window. |
| `current_weekly_status` | On Luis's Plus tier this stays `3` (inactive). A value < 3 means the weekly cap is enforced — not the case here. |
| (none — use `general` bucket of `model_remains[]`) | Aggregate across all Plus models. |

### One-line summary

```bash
curl -s 'https://www.minimax.io/v1/token_plan/remains' \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  | jq '[.model_remains[] |
        {model: .model_name,
         interval_used: .current_interval_usage_count,
         interval_status: .current_interval_status,
         weekly_used: .current_weekly_count,
         weekly_status: .current_weekly_status}]'
```

The output is the human-readable table the operator reads before
flipping the "go" switch on a batch.

### What "exhausted" looks like

When the 5h window is drained, `current_interval_status` flips from `3`
to a lower value (commonly `1` or `2` on Plus), and per-model entries
show `current_interval_usage_count` near the model ceiling. HTTP responses to
new `mmx` calls start returning 429 (Too Many Requests) with the body
matching `references/error-handling.md#rate-limits-minimax-specific`.

---

## Pre-flight check pattern

Always snapshot quota **before** a multi-output batch and **between**
items when the batch is large. A pre-flight check is a synchronous
subprocess call (≤30 s); do not background it because the snapshot must
represent the pre-spend state.

### Three-gate decision

```text
1. Quota available?
   └─ snapshot.current_interval_status == 3  → proceed
   └─ any other value                        → abort, report "5h window exhausted"

2. Cost headroom?
   └─ (window_remaining - estimated_batch_cost) >= safety_margin
       → proceed
   └─ otherwise                              → abort, suggest a smaller batch

3. Per-model headroom (only when the batch targets one model)?
   └─ per_model.current_interval_usage_count + estimated_cost <= model_ceiling
       → proceed
   └─ otherwise                              → abort, suggest staggering
```

The safety margin should be at least **+10%** of the estimated cost so a
mid-batch anomaly (network retry, transcoding flake) does not push you
over.

### The pattern in practice

```bash
# Step 1 — Snapshot.
snapshot=$(curl -s 'https://www.minimax.io/v1/token_plan/remains' \
  -H "Authorization: Bearer $MINIMAX_API_KEY")

# Step 2 — Inspect.
status=$(echo "$snapshot" | jq '.model_remains[] | select(.model_name=="general") | .current_interval_status')
used=$(echo "$snapshot"  | jq '.model_remains[] | select(.model_name=="general") | .current_interval_usage_count')
echo "5h window: used=${used} units  status=${status}"

# Step 3 — Gate.
if [ "$status" != "3" ]; then
  echo "ABORT: 5h window not healthy (status=${status})" >&2
  exit 2
fi

# Step 4 — Cost headroom (rough ceiling ≈ 4500; treat 4500 - used as remaining).
remaining=$((4500 - used))
estimated_cost=80  # 80-call batch
if [ "$remaining" -lt $((estimated_cost + 10)) ]; then
  echo "ABORT: insufficient headroom (have ${remaining}, need ${estimated_cost} + 10 margin)" >&2
  exit 2
fi

echo "OK: proceeding with batch (estimated ${estimated_cost} units, ${remaining} headroom)"
```

### When to re-check inside a batch

For a **sequential** batch (this skill's contract — never run MiniMax
generations in parallel from the same session), the rule is:

- One snapshot at the **start** of the batch.
- One snapshot **between items** if the batch is large (> ~50 calls) or
  if any item's duration exceeds ~5 minutes (long generations burn
  window time even when each call costs 1 unit).
- A **final** snapshot at the end so the receipt log records the
  post-spend state.

For interactive single-shot generation (one `mmx music generate` call),
a pre-spend snapshot is enough; the post-call state is the receipt.

### Interaction with the `mmx_recipe` pattern

The `mmx_recipe` wrapper attaches the snapshot to the receipt when
`check_quota=True`. See
[`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) § The
pattern structure § block 3 (QUOTA SNAPSHOT). The v1.1.5 roadmap item
17 plans to fold the same shape into `scripts/generate_with_retry.py`,
and item 18 plans to surface `mmx quota show` via `check_environment.py`
— both land the same pre-flight gate inside the existing scripts.

---

## Quota costs per operation — practical table

This table is the operator's working reference when sizing a batch.
Numbers are field-observed estimates; round up when in doubt.

| Operation | Per-call cost | Batch cost (10 items) | Batch cost (50 items) | Notes |
| --- | --- | --- | --- | --- |
| `mmx music generate` | ~1 unit | ~10 units | ~50 units | Standard song generation. The dominant cost in any music batch. |
| `mmx music cover` (one-step) | ~1 unit | ~10 units | ~50 units | Melody-preserving. |
| `mmx music cover` (two-step) | ~2 units | ~20 units | ~100 units | Preprocess + generate. |
| `mmx speech synthesize` (short) | ~1 unit | ~10 units | ~50 units | One clip < ~10k chars. |
| `mmx speech synthesize` (long, 30k chars) | ~3 units | ~30 units | ~150 units | Roughly per 10k chars. |
| `mmx image generate` | ~1 unit | ~10 units | ~50 units | Image-01. Always JPEG regardless of extension. |
| `mmx vision describe` | ~1 unit | ~10 units | ~50 units | Used in vision QA. |
| `mmx search query` | ~1 unit | ~10 units | ~50 units | Web search MCP. |
| `mmx video generate` | **n/a** (blocked on Plus) | — | — | Hailuo is Max/Ultra only. Do **not** include in Plus cost estimates. |

### Real-world batch examples

| Workflow | Items | Estimated cost | % of 4,500-unit 5h pool |
| --- | --- | --- | --- |
| 10-song album (lyrics + generate) | 10 | ~10 units | 0.2% |
| 20-cover run (one-step) | 20 | ~20 units | 0.4% |
| 50-image thumbnail pack | 50 | ~50 units | 1.1% |
| 100-song batch with lyrics + verification + cover variants | 100 | ~150–200 units | ~4% |
| A "burn the night" 1,000-generation loop | 1,000 | ~1,000 units | ~22% |
| Five back-to-back 500-unit batches in one 5h window | 2,500 | ~2,500 units | ~56% |

The **56%** scenario is the realistic ceiling — it leaves 44% headroom
for retries, vision QA, and any analysis calls. Going higher risks a
mid-batch 429.

### Cache / repeated-prompt caveat

If you send the **same prompt + flags** repeatedly, MiniMax may return
a cached MP3 faster, but the call still consumes 1 unit per generation.
Plan cost by **calls made**, not by **unique outputs delivered**.

---

## Error handling

Quota-related errors land in three buckets. Each has a distinct recovery
shape.

### Bucket 1 — HTTP 429 (rate limited)

The most common mid-batch symptom. The response body looks like:

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "Token Plan 5h window exhausted",
    "code": 429
  }
}
```

**Recovery:**

1. **Stop the batch immediately.** Do not retry the same call — it
   will hit the same pool.
2. Snapshot quota: `mmx quota show --output json`.
3. If `current_interval_status != 3`, **wait for the 5-hour window to
   refill**. The window is rolling, not fixed-clock, so partial refill
   happens continuously.
4. If `current_interval_status == 3` but the call still 429'd, the
   per-model ceiling was hit (rare on Plus). Wait 60 seconds, retry
   with reduced concurrency.
5. **Never** retry inside the same shell without a 60-second sleep —
   the `generate_with_retry.py` wrapper already retries on transient
   markers; do not stack retries on top.

### Bucket 2 — `current_interval_status != 3`

The snapshot itself shows the window is not healthy. This is the
**pre-flight abort** signal — no call should fire.

**Recovery:**

1. **Do not start a new batch.** Print the snapshot to the operator and
   abort.
2. If the operator says "proceed anyway", force-snapshot every 5
   minutes and re-gate; the window will refill.
3. If `current_weekly_status != 3` (rare on Luis's Plus), **never**
   proceed — that is the weekly cap, and waiting is the only fix.

### Bucket 3 — Network / auth errors that *look* like quota

| Symptom | Likely cause | Test |
| --- | --- | --- |
| All calls fail with auth error | API key revoked | `mmx auth status` or test with a fresh `MINIMAX_API_KEY` |
| 429 with body "rate_limit_exceeded" but quota looks fine | Per-model RPM ceiling | Wait 60 seconds, retry one call |
| `mmx` hangs and times out | Network or DNS | `curl -I https://api.minimax.io` to test connectivity |
| `mmx quota show` returns `error: <not json>` | CLI version mismatch | Update CLI; field names differ across versions |

### Retry strategies — what to use and what to avoid

| Strategy | When | Notes |
| --- | --- | --- |
| `generate_with_retry.py` (built-in) | Transient `code 5/6`, timeout, network markers | The skill's wrapper already handles this. Do **not** add a second retry layer. |
| Single 60-second back-off after a 429 | After the batch stops | The 5h window slides continuously; partial refill usually opens the gate within minutes. |
| Exponential back-off (60 → 120 → 240s) | Inside a long batch when 429s recur | Add only at the **batch wrapper** level, not the per-call level. |
| Auto-retry on the same call without sleep | **Never** | Burns through retry budget without recovering the pool. |
| Switch to `music-2.6-free` mid-batch | Quota budget pressure | Lower quality but cheaper path; valid fallback when the operator agrees. |
| Switch to local ACE-Step | Quota completely exhausted | `music-craft`'s local backend is the documented off-ramp. |

---

## Integration with `mmx_recipe`

For the wrapper/composition patterns that consume a quota snapshot, see
[`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) § "Reference
implementation" and the `QuotaSnapshot` / `preflight` examples there. The
canonical helper lives at `scripts/check-quota.py` (verified against
`mmx` CLI v1.0.16 — see the previous section).

> ⚠️ Earlier versions of this doc embedded an inline Python example that
> read `data["total_remains"]["current_interval_usage_count"]`. That
> field does not exist in v1.0.16's JSON (the schema is
> `model_remains[].current_interval_usage_count` with a "general" bucket
> serving as the Plus aggregate). Use `scripts/check-quota.py` or read
> the wrapper in `references/mmx-recipe-pattern.md` for the corrected
> shape.

## Troubleshooting

### `mmx: command not found`

The CLI is missing from `$PATH`.

- Install the MiniMax CLI per the official install guide, then restart
  the shell so PATH updates.
- On Windows PowerShell, run `Get-Command mmx` after install; PATH
  updates may not apply until the terminal is reopened.
- The `mmx_quota_show` helper returns `{"error": "mmx binary not found
  on PATH"}` instead of raising, so a missing CLI degrades the check to
  "no evidence", not a hard failure.

### `mmx quota show` returns non-JSON or fails

- Older CLI versions return a human-readable table only. Upgrade the
  CLI or pass `--output json` (the flag was added in mid-2026).
- A `502 Bad Gateway` from MiniMax means the Token Plan endpoint is
  temporarily down; retry after a minute.
- A `401 Unauthorized` means the API key is invalid or revoked. Check
  `MINIMAX_API_KEY` / `MINIMAX_CODE_PLAN_API_KEY` and regenerate from
  the MiniMax dashboard if needed.

### Quota looks full but `mmx music generate` returns 429

Two common causes:

1. **Per-model ceiling hit.** The `total_remains.current_interval_status`
   is `3` (overall healthy), but the per-model entry for `music-2.6`
   shows `current_interval_usage_count` near the model-specific ceiling. Wait
   60 seconds, retry. The model-level pool refills faster than the
   overall pool on Plus.
2. **Documented RPM ceiling.** MiniMax documents 120 RPM as the API
   limit. A burst of 120+ calls within a minute trips this even when
   the 5h pool is empty. The skill's contract — sequential, not
   parallel — prevents this for normal usage.

### The HTTP endpoint returns 200 but the JSON has no `model_remains`

Some CLI / account combinations return `{"code": 0, "data": {...}}` or
a similar wrapper. Read the response and pick the right path:

```bash
curl -s 'https://www.minimax.io/v1/token_plan/remains' \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  | jq 'if has("model_remains") then .model_remains else .data.model_remains end'
```

### Quota looks exhausted but a generation still succeeds

The window is **rolling** — it slides continuously. Refill happens
gradually rather than on a fixed clock. A generation that succeeds
immediately after a "window exhausted" snapshot is the rolling window
re-opening by a small amount between the snapshot and the call.

### Repeated identical prompts hit a "cached" path

Sending the same prompt + flags repeatedly does **not** skip the quota
counter on Plus. Each call costs 1 unit even when the output is cached.
If the goal is to re-render the same song, snapshot the existing MP3
and re-issue `mmx music generate` with a fresh `--seed` (when the
model supports it) or accept that you are paying for the call.

### `mmx video generate` keeps 429ing on Plus

This is **expected**. Plus does not cover `mmx video`; the 3-hour rolling
rate limit is enforced even when the 5h pool is empty. The
`current_interval_status` for video may show `1` permanently. Switch
to local LTX-Video 2.3 Q4 via Phosphene for SEF work on Plus.

### Why does the snapshot sometimes disagree with the operator dashboard?

The CLI/endpoint reads the live Token Plan pool. The dashboard may lag
by 1–2 minutes due to caching. When in doubt, trust the snapshot — it
is what `mmx` will gate against on the next call.

### Why did the weekly status move from `3` to something lower?

On Luis's Plus tier, weekly is inactive (`current_weekly_status: 3`).
If the field flips, it usually means MiniMax changed the schema. Check
the field names with `jq '.total_remains | keys'` and update the script
to match.

---

## Related references

- [`references/mmx-recipe-pattern.md`](mmx-recipe-pattern.md) — typed
  `MMXReceipt`, `dry=True`, `check_quota=True`, and the quota snapshot
  attachment contract.
- [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
  — Token Plan scope, sequential-run rule, output-file handling.
- [`references/error-handling.md`](error-handling.md) — `429` recovery,
  Token Plan 3.0 mechanics, anti-sparse, and per-flag failure modes.
- [`references/setup-and-preflight.md`](setup-and-preflight.md) — the
  environment check that runs before the first generation. Roadmap
  **v1.1.5 item 18** plans to fold quota into this script.
- [`scripts/check_environment.py`](../scripts/check_environment.py) —
  existing environment preflight; planned to expose `--quota` (item 18).
- [`scripts/generate_with_retry.py`](../scripts/generate_with_retry.py)
  — the skill's wrapper; planned to expose `MMXReceipt`-shaped return
  and `--dry` flag (item 17).
