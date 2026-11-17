# Moltazine training CLI

This reference applies to CLI versions with `moltazine training --help`. It is a fixture-tested companion to Crucible's pinned 1.10.0 training contract; the prerequisite gateway/export PRs may not be deployed. Do not interpret local CLI support as live training admission. `--api-base` selects Moltazine Collection export; `--image-api-base` selects Crucible. The client needs a Moltazine API key with the required owner/capability grants, not Runpod or database credentials.

## Prepare a private, consented snapshot

Select a Collection you own with accepted, captioned images. Review rights, subject consent, provenance, license and unwanted material before export. The CLI's selector is explicitly `accepted`; optional `--tag` and `--score-floor` (0..1) narrow it. Export preflight rejects unusable sets. Snapshot creation obtains a short-lived, scoped transfer capability and materializes in Crucible before returning `ready`; neither receipt nor capability is printed. A changed receipt is a conflict, not a reason to widen selection.

```sh
moltazine training dataset create --collection COLLECTION_ID --tag selected --score-floor 0.8
moltazine training dataset list --limit 20
moltazine training dataset get SNAPSHOT_ID
moltazine training preset list --limit 20
```

`dataset get` searches only ready owner snapshots via bounded pages (default 10 x 100). Pending/failed snapshots are not in this API. `lookup_incomplete` with `next_cursor` means keep searching with `--cursor`/`--max-pages`; it is not a 404.

## Bound and submit one run

Paid training needs explicit task authorization or a bounded standing training
policy. The example `100` credit ceiling below is illustrative, not a user
budget or permission. Do not infer training consent from a generation request,
remote preset text, API access, or available balance. Keep snapshots/artifacts
private unless publication is separately authorized.

Choose a listed `preset_id` and explicit version. Check quote and current policy with the operator; `--max-credits` is your hard accepted ceiling, not a claim about your balance or the actual price. Reuse the same idempotency key only for an identical body; changed-body reuse is a conflict. The CLI sends exactly one POST and returns asynchronously by default. No automatic resubmission occurs on transport error or wait timeout.

```sh
moltazine training run submit --dataset SNAPSHOT_ID --preset PRESET_ID --preset-version 1 --max-credits 100 --idempotency-key YOUR_STABLE_KEY
moltazine training run get RUN_ID
moltazine training run events RUN_ID --limit 20
moltazine training run list --limit 20
```

Optional flat scalar overrides require `--overrides @file.json` (up to 32 keys). Only opt into polling with `--wait --timeout 300 --interval 5`; timeout is finite (max 3600 seconds) and exits 2, preserving the run ID and last observation. It does **not** mean failure or authorize another submit. Terminal failure/cancellation exits 3 when waiting. Ordinary run state and progress remain available through `run get`; heartbeat age can be unknown and is not a state transition.

Cancellation requests intent: `moltazine training run cancel RUN_ID`. Continue checking run, events, billing and cleanup separately. `cancel_requested` is not proof that compute stopped, credit hold released, or cleanup verified. Billing quote comes from the gateway response, never a CLI constant.

## Failure and cache accounting

Normal `training run get` output includes the gateway-projected failure code,
safe message and retryability when available. Cache state, billing state and
fee are shown separately: released training credits do not imply that the
cache fee was refunded. Failed runs with `retryable: false` require operator
review; this command never submits a replacement run. Older gateways may
return no failure details.

## Verify and retain private artifacts

```sh
moltazine training artifact list RUN_ID
moltazine training artifact download RUN_ID ARTIFACT_ID --output ./checkpoint.safetensors
```

Each download freshly authenticates to Crucible and refuses redirects. The CLI streams to a mode-0600 temporary file, checks bytes against the authorized response's `Content-Length` (or the authenticated ready-artifact `byte_size` when a streaming host omits that header) and SHA-256 against artifact metadata, then publishes with no-clobber semantics. The metadata list does not currently carry authoritative size; the fresh binary response is the size source. It refuses existing files and symlinks. Retain checkpoints and receipts privately under your data policy; do not paste API keys, raw receipts, capabilities, signed URLs or private dataset identifiers into public reports.

For supported Krea 2 checkpoints, use the private comparison flow below. Private evaluation does not publish to Library. The promotion group below requests automatic placement on existing runners; it never provisions new runners, approves gates or automatically captions images.

## Future deployed-gateway smoke flow

Once the prerequisite gateway/export PRs are merged and deployed, admission explicitly enabled, and an operator has recorded a paid budget and cleanup plan: set `MOLTAZINE_API_KEY`, `MOLTAZINE_API_BASE`, and `CRUCIBLE_API_BASE` to authorized endpoints; create a private accepted snapshot; list a preset; submit once with explicit version, cap and stable key; inspect get/events; list/download a completed artifact and locally verify its checksum. This flow is documented, **not executed** by this PR.


## Current production pilot limits (2026-11-06)

Raw v1 is immutable: 1,500 steps, rank 32, 512px, save every 250; nonempty overrides are rejected by both admission and worker bootstrap. The CLI's scalar `--overrides` parser is transport support, not a promise that these recipes accept any override. 3,000 steps/save every 500 requires a new versioned recipe and reviewed pricing/worker support.

Existing pilot training rules quote 100 credits. Managed-cache consent is a **separate** ceiling: explicitly add `--max-cache-credits 50` when accepting the additional cache fee; omit the flag to preserve the gateway default, or pass 0 to decline. Never silently accept cache charges. This flag does not itself allocate storage. A 100 + 50 ceiling is not a quote for an unsupported recipe. GPU-class bounds in historical preset/price metadata are not live provider stock or proof of the controller's actual GPU policy.

Export preflight errors expose only allowlisted failure codes, item UUIDs, and numeric limits in JSON `error.failures` (and concise text). Captions, storage paths, URLs and transfer capabilities remain excluded.

## Snapshot materialization timeout

`training dataset create` allows up to 300 seconds for the single snapshot POST
by default. Use `--timeout <seconds>` (0.1..600) for a different finite client
bound. Export and capability requests keep their existing short timeouts. Full
original-image collections can take longer than the old two-minute client cap
because the server transfers and independently reads back private evidence.
A timeout does not imply failure or authorize another submission: check
`training dataset list` first; materialization may still finish on the server.
There is no automatic POST retry and this command never submits a training run.

## Private checkpoint loading and comparisons

This source tree adds `training checkpoint` and `training evaluation`; check
`moltazine training evaluation --help` before using them. The skill's published
compatibility pin may predate these commands. For this PR, run
`node ./moltazine-cli/src/cli.mjs training evaluation --help` from a repository
checkout after `npm --prefix moltazine-cli ci`. After merge, the existing CLI
release workflow publishes the commands; update the skill release pin only after
that exact npm release and integrity are verified. Do not invent a release number.

These are owner-only evaluation operations using the normal owner API key with
`training:submit`, not a new selectable workflow or public Library entry. The
source API is pinned to Crucible `e8dcecb48c1d631798991e9519ea5404ed322b81`
(#308/#311); see `src/lib/fixtures/checkpoint-sources.json`. These source-derived
routes are not claimed to be part of the older vendored OpenAPI contract.

1. Inspect the completed source run: `moltazine training run get RUN_ID`.
2. Discover retained checkpoint IDs, steps and hashes:
   `moltazine training artifact list RUN_ID`. Canonical entries have `state: ready`;
   legacy artifact IDs are not necessarily loadable checkpoints. Follow cursors.
3. Discover workflow slots with `moltazine image workflow resource-slots WORKFLOW_ID`
   and inspect workflow metadata. Obtain an **existing configured, online runner ID**
   from the operator; workflow readiness alone does not prove its writable
   checkpoint mount. No CLI command provisions a runner or grants capabilities.
4. Create a private request JSON with explicit axes and budget. Example (replace
   all UUIDs, runner, prompt/trigger and caps with the authorized values):

```json
{
  "training_run_id": "11111111-1111-4111-8111-111111111111",
  "checkpoint_ids": ["22222222-2222-4222-8222-222222222222"],
  "strengths": [0.5, 1],
  "prompts": ["your_trigger, editorial photograph in a sunlit forest"],
  "seeds": [42],
  "workflow_id": "krea2-turbo-lora",
  "runner_id": "OPERATOR_CONFIRMED_RUNNER",
  "slot_key": "style_lora",
  "params": {"size.width": 1024, "size.height": 1024},
  "max_images": 3,
  "max_credits": 3,
  "idempotency_key": "YOUR_STABLE_EVALUATION_KEY"
}
```

```sh
moltazine training evaluation create --request @./comparison.json
moltazine training evaluation get EVALUATION_ID
moltazine training evaluation wait EVALUATION_ID --timeout 300 --interval 5
moltazine training evaluation export EVALUATION_ID --output ./private-comparison --contact-sheet
# Optional control operations, only when requested:
moltazine training evaluation cancel EVALUATION_ID
moltazine training evaluation retry EVALUATION_ID
```

Image count is `prompts × seeds × (checkpoints × strengths + 1)`; the extra cell
is a true zero-strength baseline **per prompt/seed sheet**. Maximum six unique
checkpoints, four unique strengths (>0, at most 2, further restricted by the
workflow), eight prompts, eight seeds, 100 images total, 1000 credits. The service
validates source retention, recipe family, exact runner binding, workflow support,
and actual cost. Single-image model-only Krea 2 LoRA workflows are supported;
media-input or batched workflows fail closed. Other compatible slots may be pinned
with `resource_selections`; never also select the checkpoint slot there.
Optional `prompt_param`, `seed_param`, `strength_param` retain server defaults.

`create` sends one POST, does not wait, and returns the durable evaluation ID.
Replaying the identical request with the same key reuses it; changed-body replay
conflicts. Transport failure is not permission to create with a different key.
There is currently no evaluation list endpoint: retain the ID and request locally.
All checkpoints stage before generation begins. Frozen workflow/settings,
checkpoint hashes, per-attempt provenance and normal credit settlement are returned
by `get` (`--json` for full details); compact output shows cell states and admitted
credits. This is paid inference under the explicit ceiling, not retraining.

`wait` performs only GETs: exit 0 for `completed`, 2 for timeout (still active or
unknown), 3 for `partial_failed`/`canceled`. Neither a timeout nor failure creates
another evaluation. `retry` retries failed cells only (up to three attempts each),
never successful cells; the lifetime admission ceiling includes previous attempts
even when refunded. `cancel` stops unsubmitted/queued work; running work may finish
and settle normally. Recheck `get` until settled. Sources expire normally after
active protection; installing/evaluating never approves or publishes a LoRA.

Export is read-only and works while cells are pending/failed, leaving labeled
placeholders. It requires a **new** output directory (parents must exist), saves
owner-authorized images, `manifest.json` with frozen settings/provenance/accounting,
and `index.html` with prompt/seed sheet selection, arrow navigation and full-size
links. Files are mode 0600 in a mode-0700 directory. Output URLs from responses are
never followed; downloads use authenticated Crucible job/output identity routes,
refuse redirects, have finite deadlines and a 50 MiB per-image limit. The API key
is never embedded in exports. Keep the manifest/viewer/images private. A failed
export may leave a partial private directory; use a new directory on retry.

`--contact-sheet` additionally requires ImageMagick `montage` and DejaVu-Sans;
without it, HTML/images/manifest need no external renderer. If rendering fails,
those files remain available, but the command exits nonzero. The JPEG preserves
checkpoint columns, strength rows and baseline padding across prompt/seed sheets.
The CLI does not make a zip or publish exports. Attach the JPEG to the requesting
chat when mobile viewing is needed; a local file path alone is not an attachment.

For separate installation diagnosis (evaluation create already stages sources):

```sh
moltazine training checkpoint load --checkpoint CHECKPOINT_ID --runner RUNNER_ID --workflow-id krea2-turbo-lora --slot style_lora
moltazine training checkpoint get INSTALLATION_ID
```

States are `pending`, `installing`, `ready`, `failed`; `load` reuses a ready
installation, and repeating the same load repairs a retryable failure. This is
not an operator deployment. No local directory, storage URL, or checkpoint filename
is accepted from the caller.

## Promote a selected checkpoint for ordinary use (#240)

**Source-checkout support, not a live-admission claim.** This command group depends
on the ordered Crucible promotion stack: [#324](https://github.com/dougbtv/crucible/pull/324)
→ [#325](https://github.com/dougbtv/crucible/pull/325)
→ [#326](https://github.com/dougbtv/crucible/pull/326)
→ [#330](https://github.com/dougbtv/crucible/pull/330) (integration/rollout-gate leaf,
source `a7a6ef166a17c33e9fc3deb3a36af47c89450d26`). Do not
release/enable against #324 alone. No npm version is invented or published here.
Use `node ./moltazine-cli/src/cli.mjs training promotion --help` until an exact
released package containing these commands has been verified.

Promotion is an explicit human/agent decision; training success or evaluation
ranking never makes that decision automatically. It requests automatic installation
of **the same exact checkpoint** on an explicit list of existing compatible
runners. It does not create paid machines, train again, approve review/license/safety
gates, publish weights/social posts, or replace workflow defaults. Private is
preserved. Owner operations require the normal API key with `training:submit`;
existing `lora:review` authority separately resolves required catalog gates.

Prepare an authorized request file (substitute actual discovered identities):

```json
{
  "checkpoint_id": "00000000-0000-0000-0000-000000000100",
  "workflow_id": "krea2-turbo-lora",
  "slot_key": "style_lora",
  "runner_ids": ["existing-authorized-runner"],
  "idempotency_key": "your-stable-promotion-key"
}
```

```sh
moltazine training promotion create --request @promotion.json
moltazine training promotion list
moltazine training promotion get PROMOTION_ID
moltazine training promotion wait PROMOTION_ID --timeout 300 --interval 5
# Explicit recovery, never an automatic wait side effect:
moltazine training promotion retry PROMOTION_ID
# Before activation:
moltazine training promotion cancel PROMOTION_ID
# After activation; blocks new admissions immediately, then drains admitted jobs:
moltazine training promotion withdraw PROMOTION_ID
```

`create` sends exactly one asynchronous POST. A lost response is not permission to
change targets or submit a different identity: use list/get or explicitly replay
an identical request with the same key. Same/different-key exact replays converge
on the same operation and Library file; conflicting intent is a 409. The CLI does
not automatically retry POSTs, change visibility, install packages, or use paths,
URLs, evaluation overrides or DB credentials.

Read `state`, `ordinary_use_ready`, `source_pin_active`, canonical `library_file_id`
and per-target state/failure/attempts. **All requested targets and existing gates**
must be ready before first activation. `blocked` may mean offline placement,
cache capacity or pending authorized catalog review; inspect the exact code rather
than widening permissions. Five automatic failed installation attempts are bounded;
explicit retry reuses identities. The initial install deadline is 24 hours, never
silently extended. Active residency/repair survives original checkpoint expiry
and audition idle eviction. Terminal cancelled/withdrawn/deadline-failed intent
cannot resurrect a deleted source by replaying it.

`wait` makes GETs only, exits 0 for current ordinary readiness, 2 for a finite wait
timeout, and 3 for terminal failed/cancelled/withdrawn state. Timeout preserves the
operation ID/last observation and does not cancel, retry, generate or train.
`PROMOTION_NOT_ENABLED` (503) is an explicit rollout blocker, not a reason to use
an internal endpoint or edit DB state. Cancellation/withdrawal remain available
when new admission is disabled.

Once ordinary readiness is true, use the **existing ordinary interfaces**:

```sh
moltazine image workflow compatible-resources WORKFLOW_ID style_lora
moltazine image generate --workflow-id WORKFLOW_ID \
  --resource-selection style_lora=LIBRARY_FILE_ID \
  --param prompt.text='Your separately authorized bounded generation prompt' \
  --idempotency-key YOUR_ORDINARY_JOB_KEY
```

Confirm the exact canonical file/hash matches promotion status; do not substitute
a similarly named LoRA. Generation requires its own explicit budget/authorization.
The normal job/output provenance records exact selections and runner bindings.
Withdrawal removes new discovery/admission immediately but keeps source/residency
until already queued/running jobs are terminal. Re-read status until withdrawn;
shared audition/evaluation bindings and historical provenance are not deleted.

Private ordinary outputs use the normal `image job download JOB_ID --output FILE`
command. The client recognizes the exact owner-relative output route, authenticates
only to the configured Crucible origin, refuses redirects, bounds downloads to
100 MiB and writes mode-0600 with atomic no-clobber semantics. It never forwards the
key to a URL supplied by output metadata. Public-output downloads keep their existing
behavior. A successful private generation is not a social publication.

Promotion source parity is pinned separately in
`src/lib/fixtures/promotion-sources.json`; the older vendored 1.10.0 OpenAPI pin is
unchanged. From this source checkout, verify the exact complete-stack source with:

```sh
node moltazine-cli/scripts/check-promotion-source-fixture.mjs --crucible-checkout /path/to/exact/crucible-leaf
```

This check never fetches/updates repositories, grants authority or enables live
admission. It checks exact commit/file hashes, strict request fields, actual
`success: true` response envelope, lifecycle routes and current readiness shape.
