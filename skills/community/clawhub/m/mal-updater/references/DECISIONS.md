# Decisions

## 2026-03-14 - Core integration direction

### Decision
Build MAL-Updater as a local Orin-hosted integration using:
- Python application/worker
- SQLite state database
- official MAL OAuth + REST API
- Python-side Crunchyroll auth + live fetches

### Why
- the working Crunchyroll path on this host is Python-side
- Python is better for orchestration, mapping logic, sync policy, and future recommendation work
- SQLite is sufficient and simple for local state
- keeping the implementation in one language leaves the repo smaller and easier to maintain

## 2026-03-14 - Sync direction

### Decision
One-way sync first: Crunchyroll -> MyAnimeList.

### Why
- Crunchyroll is the behavioral source of truth for watched progress
- MAL should be updated conservatively as the public-facing tracking layer
- two-way reconciliation adds unnecessary risk early

## 2026-03-14 - Sync policy

### Decision
This is a **missing-data-first** system.

### Rules
- Do not decrease MAL progress automatically.
- Do not overwrite meaningful existing MAL data automatically.
- Treat MAL `status` as missing only when absent/null.
- Treat MAL watched-progress as missing only when list status is absent; `plan_to_watch` + `0` is meaningful and should be preserved.
- Exception: if Crunchyroll proves completed episode progress (`> 0` watched episodes), a MAL `plan_to_watch` entry may be upgraded forward to `watching` or `completed`.
- Suppress `watching` proposals with `0` watched episodes entirely; partial playback without at least one completed episode is not honest enough to auto-write.
- Treat MAL `score` as missing only when null/absent/`0`.
- Treat MAL `start_date` / `finish_date` as missing only when null/empty.
- Only fill dates when the source evidence is trustworthy enough; currently that means `finish_date` may be filled from Crunchyroll `last_watched_at` only when Crunchyroll-derived status is `completed`.
- Do not auto-resolve ambiguous mappings.
- Only auto-approve mappings when the top MAL candidate is an exact normalized-title match, clearly ahead of the runner-up, and there is no contradictory season/episode/installment evidence.
- Expand generic Crunchyroll season labels like `Season 2` / `Part 2` / `2nd Cour` / `Final Season` into `Title ...` search queries before giving up.
- Treat explicit installment cues (season numbers, ordinal seasons, roman numerals, parts, cours, split indexes, `Final Season`) as explainable matching evidence; matching cues can promote a result, conflicting cues must block auto-approval.
- Use stricter exact-title normalization than the similarity scorer so installment-bearing titles like `Part 1` and `Part 2` do not collapse into the same "exact" match.
- When Crunchyroll `season_number` metadata conflicts with an explicit season number inside `season_title`, prefer the human-readable title cue and surface the conflict in rationale instead of silently trusting the integer.
- Keep a default penalty on MAL movie candidates, but waive it when the provider season title itself is an exact movie title; this handles provider collection shells conservatively without making movies broadly preferred.
- Penalize single-episode `special`/`OVA` residue more strongly when Crunchyroll clearly looks like a normal multi-episode series and the provider title did not explicitly ask for auxiliary content.
- If Crunchyroll episode numbering looks aggregated across seasons, do not treat that raw max episode number as a hard contradiction when explicit installment hints line up and the completed-episode count still fits inside the candidate; surface that as explainable `aggregated_episode_numbering_suspected` evidence instead.
- Do not claim episode-title matching exists unless the metadata source is trustworthy enough to explain and maintain. The current official MAL API surface does not expose episode titles directly, so any future episode-title path must be an explicit, justified choice rather than confidence theater.
- Queue conflicts for review.
- Dry-run before live writes.

## 2026-03-14 - Completion semantics

### Decision
Treat Crunchyroll episodes as watched only when the evidence is strong enough to explainable justify it:
- `completion_ratio >= 0.95`, or
- known remaining playback time is `<= 120` seconds, or
- the episode is at least `0.85` complete and a later episode in the same Crunchyroll series was watched afterwards.

### Why
The real local dataset showed that a blind `0.90` ratio threshold was too hand-wavy:
- many credit-skip cases cluster around **80-120 seconds remaining** rather than a single stable ratio
- **725 / 775** episodes in the `0.85-0.95` band were followed by a later watched episode in the same series
- **555 / 775** episodes in that band had `<= 120s` remaining
- only **20 / 775** episodes in that band had neither follow-on evidence nor the short remaining-time signature, so those should stay incomplete by default

### Working defaults
- strict completion ratio: `0.95`
- credits-skip remaining-time window: `120` seconds
- follow-on completion floor: `0.85`

## 2026-03-14 - Recommendation priorities

### Highest priority alerts
1. New season released for an anime the user has completed.
2. New dubbed episode released for an in-progress anime the user is currently following.

### Hard recommendation filter
- Do not recommend anime or new episodes that lack English dubs.

## 2026-03-14 / 2026-03-20 - Repo posture

### Decision
Treat `MAL-Updater` as a public repository and keep all tracked artifacts anonymized.

### Rules
- Do not commit real credentials, tokens, API keys, or account identifiers.
- Do not commit host-specific absolute paths, private workspace paths, or machine-local identifiers.
- Use obviously fake placeholders in examples and tests.
- Runtime-generated state may exist under external runtime directories, but it must not be tracked.
- If identifying residue is accidentally committed, history rewrite is an acceptable remediation.

### Why
Public-repo hygiene needs to be part of the project contract, not an afterthought. Future development should assume anything tracked in git may be published and mirrored.

### Related maintainer channel
Operational bugs, usability issues, and feature requests discovered by third-party users should be reported through the authoritative upstream issue tracker:
- <https://github.com/kklouzal/MAL-Updater/issues>

## 2026-03-14 - Project memory habit

### Decision
Use `references/` as project-specific durable memory.

### Why
OpenClaw memory is useful, but project-specific knowledge should live with the project repo.

## 2026-03-14 - Crunchyroll implementation choice

### Decision
Use the Python-side impersonated transport as the primary Crunchyroll auth and live fetch path.

### Why
- it is the path that produced real live account/history/watchlist data on this host
- it reuses the already-proven `curl_cffi` browser-TLS impersonation workaround when needed
- it gets real data into the local pipeline now instead of blocking on alternative transport ideas
- it keeps the repo architecture coherent and smaller

## 2026-03-14 - Crunchyroll incremental boundary posture

### Decision
Treat repeated Crunchyroll fetches as incremental by default.

### Rules
- Persist a local `sync_boundary.json` checkpoint under the resolved runtime state tree (`.MAL-Updater/state/crunchyroll/<profile>/` by default) only after a successful snapshot fetch completes.
- Store only lightweight leading-page markers for watch-history and watchlist, not a second shadow database.
- On the next fetch, stop paging once a previously seen marker appears in the current page; keep the current page, but do not keep walking older pages.
- If the stored boundary belongs to a different Crunchyroll account, ignore it.
- Provide an explicit operator escape hatch (`crunchyroll-fetch-snapshot --full-refresh`) for full pagination when needed.
- Prefer explainable overlap-based stopping over more aggressive heuristics about dates/count deltas/order stability.

### Why
- the recurring durability problem is still fresh full-cycle Crunchyroll paging, especially `watch-history` returning `401` before the run finishes
- an overlap checkpoint directly reduces request count on repeated runs without pretending deleted/reordered remote history is solved
- keeping the boundary file small and local makes the behavior auditable and easy to reset

## 2026-03-20 - Daemon budget backoff posture

### Decision
When the daemon hits a provider budget critical threshold, persist a per-task cooldown window and stop re-checking that task every loop until enough request history ages out of the hourly window.

### Why
- repeated every-loop budget skips create noisy logs without making progress
- recovery should be based on the observed request window, not a hand-wavy fixed sleep
- surfacing `budget_backoff_until` in service state/status makes unattended behavior easier to reason about during debugging

## 2026-03-22 - Adaptive provider failure backoff posture

### Decision
When a daemon task tied to a provider fails, persist an adaptive failure-backoff window with the failure reason and consecutive-failure streak so the lane cools down before retrying instead of immediately thrashing.

### Why
- auth-fragile provider fetches can fail repeatedly for a while after a bad login/session state transition
- every-loop retries create noisy logs and extra pressure without improving recovery odds
- surfacing `failure_backoff_until`, `failure_backoff_reason`, and consecutive failures in service state/status makes unattended debugging clearer

## 2026-03-22 / 2026-03-23 / 2026-03-28 - Provider full-refresh escalation posture

### Decision
Keep provider fetch lanes incremental by default, but let the unattended daemon both:
- persist a provider-specific full-refresh anchor and force a conservative `--full-refresh` sweep whenever `service.full_refresh_every_seconds` elapses (default 24 hours), and
- honor the latest health-check `refresh_full_snapshot` recommendation for a provider so partial-coverage warnings can trigger the next unattended fetch to self-upgrade into a full refresh immediately.

Only advance `last_fetch_mode`, `last_successful_full_refresh_*`, and the full-refresh anchor after a **successful** provider fetch. A failed attempted full refresh must not be recorded as if the canonical resweep already happened.

### Why
- incremental fetches are the right steady-state posture for fragile providers, but unattended sync quality still needs occasional canonical resweeps
- a persisted cadence anchor gives the daemon an explainable, low-complexity way to recover from stale provider state without requiring operators to remember ad-hoc maintenance commands
- wiring health-check maintenance recommendations back into daemon execution closes a real gap between diagnosis and remediation for partial-coverage residue
- surfacing fetch mode plus last successful full refresh in task state keeps the behavior auditable instead of hiding refresh policy in operator folklore
- treating a failed full refresh as successful would silently suppress the very resweep the daemon was trying to obtain

## 2026-03-24 - Generic source-provider budget default posture

### Decision
Keep MAL as its own explicit daemon budget lane, but let non-MAL source providers inherit shared source-provider hourly/backoff/auth-failure defaults unless a per-provider override is configured.

### Why
- the provider architecture should not silently treat every new source provider as if it were Crunchyroll
- shared source-provider defaults make new providers safer to onboard before their final tuned per-provider numbers are known
- explicit per-provider overrides still win, so operators can keep Crunchyroll/HIDIVE-specific tuning where it matters

## 2026-03-23 / 2026-03-27 - Auth-style provider failure cooldown posture

### Decision
Keep adaptive provider failure backoff for all daemon task errors, but classify auth-style provider failures separately and allow a stronger provider-specific cooldown floor for that class. Persist the failure class and effective floor in service state/status.

Auth-style detection should be shared between the daemon/runtime path and the health-check/operator path, and should conservatively treat these residue classes as auth-related:
- repeated `401` / `403` / unauthorized-style failures
- refresh/login failures (`invalid_grant`, token refresh/login failure text)
- missing refresh-token / missing refresh-material residue
- malformed token-payload residue (`did not return ...token...`, non-JSON login/token responses)
- provider session-state auth phases like `auth_failed`

### Why
- repeated auth/login/refresh failures are a different recovery shape than generic subprocess or network residue
- brittle provider auth should cool down longer before retrying so unattended loops stop re-poking broken sessions
- the same auth residue should drive both unattended cooldown behavior and later health-check rebootstrap guidance instead of letting those heuristics drift apart
- surfacing the failure class and floor keeps the daemon's retry posture explainable during debugging instead of hiding it in timing folklore

## 2026-03-22 - Same-title split-bundle suffix posture

### Decision
Allow exact-title split-bundle auto-resolution when the base candidate is an exact TV match and the bundle companion is a same-title TV suffix variant (for example a year-tagged entry like `Title (2009)`), **but only** when provider episode evidence fits the combined bundle length and there is no stronger non-bundle rival nearby.

### Why
- some real MAL franchises split one provider shell across multiple TV entries without advertising a plain `Season 2` / `Part 2` hint
- this residue is still explainable when the provider title is exact, the companion stays in the same normalized title family, and the episode count only makes sense as the combined bundle
- keeping the rule tied to same-title TV suffix companions preserves conservative behavior while removing a class of manual-review busywork

## 2026-03-20 - Supplemental mapping candidate posture

### Decision
Treat hard-coded supplemental MAL candidate IDs as conservative rescue inputs, not as enough evidence by themselves to auto-resolve exact-title overflow cases.

### Why
- supplemental IDs help recover titles that MAL search fails to surface at all
- overflow on top of a supplemental-only hit can still mean a multi-entry bundle or broader franchise residue
- keeping this path conservative preserves explainability and avoids overconfident auto-approval when the search surface was already weak

## 2026-03-27 / 2026-03-28 - Built-in projected-request seed posture

### Decision
Ship explicit built-in projected-request defaults for conservative unattended lanes, but treat those built-ins as **cold-start seeds** rather than permanent hard overrides once the daemon has real observed request history.

This applies to:
- `mal_refresh`
- `sync_apply`
- fetch-mode-specific provider defaults such as Crunchyroll/HIDIVE incremental and full-refresh fetches

If an operator supplies an explicit task-wide override, that override should still beat the shipped seed when no more specific explicit mode override exists.

### Why
- fresh installs should not treat routine daemon lanes like zero-cost mysteries before the first real run lands
- once a lane has observed request history, synthetic shipped defaults should stop pinning budget behavior to folklore instead of evidence
- keeping built-ins seed-like preserves the repo's current direction: conservative, explainable cold starts first, then learned host-specific behavior as soon as real data exists

## 2026-03-25 - Bursty learned-request projection posture

### Decision
When a daemon lane has no explicit projected-request percentile configured, keep the default smoothed-history projection for ordinary lanes but automatically switch to a conservative learned `p90` baseline once the recent observed request history is clearly bursty.

### Why
- unattended budget gating should react before a spiky lane surprises the provider limit
- requiring manual percentile tuning for every lane is unnecessary operator busywork
- auto-switching only after several observed runs keeps the default path simple for stable lanes while making burstier ones safer by default

## 2026-03-24 - Task-level daemon budget override posture

### Decision
Keep provider/shared budget defaults as the baseline, but allow optional per-task daemon budget overrides for hourly limit, warn/critical cooldown floors, and auth-failure cooldown floors. Persist the effective budget scope (`task` vs `provider`) in service state/status.

### Why
- some daemon lanes share a provider but do not deserve the same throttling posture (for example MAL token refresh vs aggregate apply)
- per-task overrides let operators tune the risky/expensive lane without inventing fake provider identities
- surfacing the effective budget scope keeps cooldown decisions explainable during unattended debugging

## 2026-03-24 - First-pass projected request budgeting posture

### Decision
Teach daemon budget gates to look at projected per-run request cost, not only the current hourly count. Use explicit `service.task_projected_request_counts` overrides when present; otherwise reuse the lane's last observed request delta (including fetch-mode-specific deltas for incremental vs full-refresh provider fetches). Persist the projection source/count in service state/status so unattended skips remain explainable.

### Why
- raw current-hour counts alone react too late for chunky lanes whose next run is what would actually push the provider over warn/critical budget
- last-observed request deltas are a cheap, local, provider-agnostic signal that improves pacing without inventing fake precision or requiring a large planning subsystem
- explicit per-task overrides still matter for operators who know a lane's expected cost better than one recent observed run
- persisting projection source/count keeps the gate auditable instead of feeling like invisible daemon magic

## 2026-03-24 - Smoothed observed request projection posture

### Decision
When a lane does not have an explicit configured projected request count, keep a short rolling observed request-delta history and derive projections from a smoothed average instead of blindly trusting only the most recent run. Prefer fetch-mode-specific history (`incremental` vs `full_refresh`) when available, then fall back to overall lane history, then finally to the legacy last-run delta.

### Why
- one unusually expensive unattended run should not immediately become the whole budget policy for the next run
- fetch-mode-specific smoothing preserves the useful distinction between incremental and full-refresh provider cost without needing a larger forecasting subsystem
- preserving the legacy last-run fallback keeps cold-start behavior simple while letting repeated runs become more stable
- persisting the projection source still keeps daemon pacing explainable during debugging

## 2026-03-25 - Tunable learned request projection posture

### Decision
Keep the learned observed-request projection path configurable per task: allow each lane to override its observed-history window and optionally use a percentile baseline instead of the default smoothed mean. Prefer the same fetch-mode-specific history split (`incremental` vs `full_refresh`) when present.

### Why
- different daemon lanes have different burst shapes, so one fixed five-sample mean is too blunt as the project grows
- conservative percentile baselines let fragile/high-cost fetch lanes pace themselves without forcing every quieter lane into worst-case budgeting
- keeping the tuning task-scoped preserves explainability and avoids inventing hidden provider-wide heuristics too early
- bounded per-task history windows keep the state small and auditable while still letting operators smooth or tighten learning where it matters

## 2026-03-25 - Shipped provider pacing defaults posture

### Decision
Ship opinionated daemon pacing defaults for the currently supported source providers instead of leaving those numbers only in example config. Keep shared source-provider defaults as the fallback for unknown/new providers, but seed built-in provider tables for:
- Crunchyroll: deeper learned request-cost history, conservative percentile projection, and stronger warn/critical/auth-failure cooldown floors
- HIDIVE: quieter hourly budget plus provider-specific backoff/auth-failure floors

### Why
- the repo's own likely-next-step had already converged on provider defaults being justified for the current providers
- supported providers now have enough operational character to deserve safer built-in posture without requiring every operator to rediscover the same settings
- keeping unknown providers on the generic source-provider fallback preserves extensibility while making today's unattended installs safer out of the box

## 2026-03-26 / 2026-03-29 - Shipped `sync_apply` task-default posture

### Decision
Ship built-in daemon task defaults for the aggregate MAL `sync_apply` lane instead of leaving that lane's conservative posture only in example config. Seed built-in task tables for:
- hourly limit: `48`
- projected request count: `8`
- learned request-history window: `3`
- learned projected-request percentile: `0.9`
- warn cooldown floor: `900s`
- critical cooldown floor: `1800s`
- auth-failure cooldown floor: `2400s`

### Why
- `sync_apply` is the first MAL lane that clearly behaves like a higher-cost/riskier aggregate task than the provider-level MAL defaults imply
- once the lane has real observed request history, a conservative built-in learned percentile keeps MAL write budgeting from drifting back to mean-smoothed optimism on fresh unattended installs
- fresh unattended installs should inherit a conservative aggregate-apply posture even before an operator copies optional example settings into their runtime config
- keeping the defaults task-scoped preserves the clean provider/task split while making the most meaningful shipped lane safer out of the box

## 2026-03-26 - Fetch-mode task projection defaults posture

### Decision
Keep the existing task-level projected-request override table, but add an optional fetch-mode-specific task table for lanes whose incremental and full-refresh cost differ materially. Ship the first built-in default for `sync_fetch_hidive` full refresh at `71` projected requests.

### Why
- some fetch lanes are cheap incrementally but materially more expensive when forced into `--full-refresh`, so a single task-wide configured projection is too blunt
- cold-start unattended budgeting should not treat a known heavy full-refresh lane as zero-cost just because local history has not been learned yet
- keeping the override task-scoped and fetch-mode-scoped preserves explainability without inventing a larger forecasting subsystem
- HIDIVE already has enough observed local shape to justify one concrete shipped full-refresh default while leaving other lanes on learned history until they have equally solid evidence

## 2026-03-26 - Crunchyroll full-refresh projection default posture

### Decision
Extend the built-in fetch-mode task projection defaults to ship a conservative `sync_fetch_crunchyroll` full-refresh projected-request cost of `55`.

### Why
- Crunchyroll full refreshes are materially heavier than the lane's ordinary incremental fetches, so cold-start budgeting should not have to pretend the first overdue resweep costs zero requests
- the daemon already has mode-specific budget behavior and downgrade-to-incremental logic, so shipping a concrete Crunchyroll full-refresh default lets those controls act earlier on fresh unattended installs instead of waiting for local history to be learned
- keeping the default task-scoped and mode-scoped preserves explainability and leaves ordinary incremental Crunchyroll pacing on the existing task/provider learned-history path
- this mirrors the earlier HIDIVE full-refresh default and closes the most obvious remaining gap in the repo's own shipped provider-fetch posture

## 2026-03-27 - Incremental fetch projection default posture

### Decision
Extend the built-in fetch-mode task projection defaults so the ordinary unattended provider fetch path also starts with a conservative non-zero request-cost estimate. Ship built-in incremental projected-request defaults of `4` for both:
- `sync_fetch_crunchyroll`
- `sync_fetch_hidive`

### Why
- the daemon already ships built-in full-refresh fetch costs, but fresh installs were still treating the ordinary incremental fetch path as effectively zero-cost until enough local history accumulated
- live runtime on this host has now repeatedly settled both Crunchyroll and HIDIVE incremental fetch lanes around `4` requests, which is stable enough to justify a small shipped seed value
- a low non-zero incremental default makes cold-start budget gating more honest without forcing operators to pre-tune config or waiting for the first few unattended runs to teach the daemon something it already broadly knows
- keeping the defaults task-scoped and mode-scoped preserves explainability and leaves room for learned history or host-specific overrides to take over once local evidence exists

## 2026-03-26 - Budget-blocked full-refresh downgrade posture

### Decision
When an unattended provider fetch is due for `full_refresh` because of cadence or health recommendations but that heavier run is budget-blocked, immediately retry the budget check for `incremental` mode and run the cheaper fetch when it fits. Keep the full-refresh anchor/reason overdue so the heavier resweep still happens later once budget allows.

### Why
- a heavy overdue full refresh should not starve the entire fetch lane when a cheaper incremental pass would still keep fresh progress/watchlist data moving
- fetch-mode-specific projected-cost defaults are only truly useful if the daemon can act differently on them instead of turning every overdue full refresh into repeated no-op skips
- preserving the overdue full-refresh anchor/reason keeps the behavior conservative and explainable instead of silently forgetting that a broader resweep is still needed
