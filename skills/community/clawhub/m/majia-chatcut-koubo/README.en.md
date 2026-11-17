# ChatCut Talking Head · Majia Field Edition

![Skill Version](https://img.shields.io/badge/skill-v1.7.0-blue)
[![skills.sh](https://skills.sh/b/maojiebc/majia-chatcut-koubo)](https://skills.sh/maojiebc/majia-chatcut-koubo)

**ChatCut口播 · 马甲实战版 | One-sentence stable cut with recoverable execution**

> A one-sentence path for ordinary creators: clean low-risk talking-head issues, approve a representative sample, extend the approved treatment, and hand back an editable ChatCut timeline.

![v1.7.0 one-sentence workflow](https://raw.githubusercontent.com/maojiebc/majia-chatcut-koubo/main/04-项目设计与路线图/系统架构.png)

## Start in 30 seconds

After installation, say:

```text
$majia-chatcut-koubo Use Majia Stable Cut on the current talking-head video.
```

The Skill first reads the current project, timeline, and sources automatically, asking one focused question only when they cannot be resolved uniquely. It prepares a low-risk representative sample, waits for approval, then applies the same approved strategy to the full A-roll before audio smoothing, basic captions, and verification.

The default output is an editable ChatCut timeline. It does not automatically export or publish a video.

For local development from a GitHub source clone. The lightweight SkillHub package omits tests, fixtures, and CI-only validators; full verification remains bound to the same source commit and CI run:

```bash
npm ci
npm run doctor
npm run koubo -- --help
npm run smoke:one-click:fake
```

## v1.7 session and text safety

The current session selects Hosted/Web or Desktop instructions. Missing, stale, mismatched, or simulated capability observations do not clear preflight. Caption-only and ASR repair requests disable default speech cleanup; local spoken-audio replacement requires exact high-risk approval. Ambiguous text targets require clarification.

Developers can check a declared current session with `npm run preflight -- --session <current-session.json> --json` and compare a supplied official checkout with `npm run check:official -- --checkout <official-checkout>`. These checks do not verify media. See [session and text safety](workflows/session-and-text-safety.md) and the [dated official-source review](https://github.com/maojiebc/majia-chatcut-koubo/blob/main/04-%E9%A1%B9%E7%9B%AE%E8%AE%BE%E8%AE%A1%E4%B8%8E%E8%B7%AF%E7%BA%BF%E5%9B%BE/2026-09-30%E5%AE%98%E6%96%B9%E6%9B%B4%E6%96%B0%E4%B8%8Ev1.7%E8%AE%BE%E8%AE%A1.md).

## Safe defaults

It will:

- route stable, fast, pro, review, and resume intents;
- select one of four deterministic profiles;
- protect numbers, proper nouns, negation, argument chains, and accepted designs;
- auto-apply only evidence-backed low-risk decisions;
- send medium-risk decisions through the sample and high-risk decisions to explicit approval;
- process A-roll before audio smoothing and full captions;
- report structure, visual, audio measurement, human listening, privacy, and approval separately.

It will not:

- restructure ideas or move a hook automatically;
- remove whole sentences or sensitive semantic content without approval;
- add music, motion graphics, B-roll, or generated media by default;
- overwrite manual timeline edits;
- infer visual or listening success from a tool response;
- export or publish without separate authorization.

## Modes and profiles

| User intent | Default profile | Best for |
| --- | --- | --- |
| Stable cut | `balanced-stable` | everyday talking head |
| Fast cut | `tight-short` | 30–90 second drafts |
| Pro, long form | `trust-longform` | 5–30 minute trust content |
| Pro, screen demo | `screen-demo` | screen evidence plus presenter |

Profiles live in [`profiles/`](profiles/). Local preferences may preserve or tighten safety policy, never weaken it.

## Main flow

```text
intent
→ project and source check
→ transcript and risk decisions
→ representative sample
→ user approval or revision
→ full A-roll
→ audio smoothing and captions
→ evidence-separated verification
→ editable timeline and handoff report
```

Sample approval is bound to plan, style, layout, captions, timeline revision, and window scope. Any drift makes it `STALE`.

## Recovery

Run records and checkpoints support cross-session recovery:

- timeout before commit: read back, confirm no write, then retry;
- timeout after commit: read back and avoid a duplicate write;
- partial write: compensate or stop at the latest checkpoint;
- manual edit: preserve it and invalidate the old approval;
- same failure three times: stop and hand off the last safe state.

Local commands:

```bash
npm run run -- --intent "stable cut the current talking head" --dry-run --json
npm run status -- --run-id <run-id>
npm run review -- --run-id <run-id>
npm run approve-decisions -- --run-id <run-id> --decision-id <decision-id>
npm run approve-sample -- --run-id <run-id>
npm run request-revision -- --run-id <run-id> --direction natural
npm run resume -- --run-id <run-id> --timeline-revision <fresh-revision> \
  --reconcile-outcome <blocker-specific-outcome> \
  --evidence-ref <logical:readback-evidence> [--checkpoint-id <checkpoint-id>]
npm run report -- --run-id <run-id>
```

`resume` never treats the revision stored in the manifest as a fresh readback. A blocked run also requires blocker-specific reconciliation evidence; write-related blockers require the latest persisted checkpoint.

In a source clone, `doctor` runs the anonymous fixture audit. In a lightweight registry package it says the fixture audit is not bundled and identifies the scope as `distribution-package`, instead of pretending a local full test ran.

Per-project run records are stored under `.majia-koubo/`, which is ignored by Git.

## Evidence states

The handoff keeps `PASS`, `FAIL`, `UNVERIFIED`, `STALE`, `WAIVED`, `NOT_APPLICABLE`, and `PENDING` distinct. A timeline readback does not prove pixels; a rendered frame does not prove human listening; sample approval does not equal final review approval.

## Current verification boundary

| Capability | v1.7.0 status |
| --- | --- |
| Schemas, profiles, risk policy, state transitions | `PASS` offline |
| timeout-before/after, partial write, manual-edit protection | `PASS` in anonymous sessions with structured simulation evidence |
| starter prompt routing and local CLI | `PASS` offline |
| real ChatCut writes and readbacks | `UNVERIFIED` |
| real rendered pixels, human listening, anonymous production cases | `UNVERIFIED` |

[`reports/live-canary-v1.7.0.json`](reports/live-canary-v1.7.0.json) currently records `stableClaimEligible=false`. Offline simulation is not live evidence. This project will not claim production-proven one-click stable editing until the live gate covers at least five anonymous cases across three lengths, three content shapes, recovery, and manual-edit protection.

## Official ChatCut division of responsibility

ChatCut's current official Skills own project operations, import, transcription, talking-head methods, verification, music, graphics, generation, export, and product help. This package does not copy their parameter tutorials. It adds sequencing, conservative defaults, sample approval, recovery, and evidence-aware handoff.

See [`workflows/official-skill-map.md`](workflows/official-skill-map.md). Current ChatCut tool descriptions remain the source of truth.

## Install

```bash
gh skill install maojiebc/majia-chatcut-koubo
npx skills add maojiebc/majia-chatcut-koubo
npx clawhub install majia-chatcut-koubo
```

The installation slug remains `majia-chatcut-koubo`; the display name is “ChatCut口播 · 马甲实战版”.

## Development gates

Node 24.18.0 is required:

```bash
npm ci
npm run verify
npm audit --audit-level=high
```

Focused checks:

```bash
npm run validate:runtime-contracts
npm run test:orchestration
npm run test:risk-policy
npm run test:run-state
npm run test:starter-prompts
npm run test:cli
npm run smoke:one-click:fake
npm run validate:docs-routing
npm run validate:live-claim
```

The advanced Rule Registry, Creator OS IR, SRT bridge, seven-state visual system, preview approval, recoverable writes, media QA, extensions, and visual candidate governance remain available behind the ordinary creator path.

Caption release validation still requires an explicit profile root:

```bash
node scripts/validate-caption-pages.mjs \
  --strict \
  --profile <profile.source.json> \
  --root <profile-config-root> \
  --input <captions.json>
```

See the [public roadmap](04-项目设计与路线图/公开路线图.md) for engineering order and live evidence gates.

## Maintenance map

- [Start here](01-从这里开始/README.md)
- [Editing methods](02-剪辑方法手册/README.md)
- [Field cases and lessons](03-实操迭代与踩坑/README.md)
- [Architecture and roadmap](04-项目设计与路线图/README.md)

Private terms, project paths, and business content belong only in local configuration and never in the public repository.

## Version history

**V1.7.0 (2026-09-30)** — Declared session preflight, Hosted/Desktop routing, text-target protection, official-source snapshots and drift checks, version-bound live canary selection, and a patched indirect dependency. Real end-to-end remains `UNVERIFIED`.

**V1.6.0 (2026-08-11)** — One-sentence entry, three modes, four profiles, run/status/review/approval/revision/resume/report commands, manifests, decisions, checkpoints, six-part sample fingerprints, recovery, evidence-separated handoff reports, and 11 anonymous fault scenarios. Real ChatCut end-to-end remains `UNVERIFIED`.

**V1.5.0 (2026-07-25)** — Governed optional knowledge and shot-candidate extensions.


See [CHANGELOG.md](CHANGELOG.md) for the full history.

## Author

**Majia (@maojiebc)** · Super Majia

- [GitHub](https://github.com/maojiebc)
- [ClawHub](https://clawhub.ai/p/maojiebc)
- [X](https://x.com/maojiebc)
- [Xiaohongshu](https://xhslink.com/m/4fQMJeHHWKC)
