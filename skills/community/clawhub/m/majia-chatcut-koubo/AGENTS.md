# Repository delivery policy

For every completed development increment in this repository:

1. Run the relevant focused checks and the full release gate when practical.
2. Commit only the intended, verified changes.
3. Fast-forward the local `main` branch to the verified commit.
4. Push `main` to `origin`.
5. Read back the GitHub `main` commit and confirm it exactly matches local `HEAD`.

A development increment is not complete until the GitHub `main` readback succeeds. If authentication, branch protection, CI, network access, or divergence prevents the push, report the work as not fully delivered and state the exact blocker.

This policy treats GitHub `main` as the formal code backup. It does not authorize automatic ClawHub releases, media uploads, video-platform publishing, or other external business actions.

## V1.7 product contract

- Optimize the ordinary creator path first: the starter prompt must route to `run`, `review`, or `resume` without requiring users to understand the internal engine.
- Keep official ChatCut Skills as the source of truth for product operations and current tool parameters. This repository adds sequencing, defaults, approvals, recovery, and reporting.
- Persist cross-session state through the Run Manifest and checkpoints. Never infer a successful write from a timeout; reconcile by reading the current timeline first.
- Treat whole-sentence removal, numbers, proper nouns, negation, restructuring, privacy uncertainty, generated media, export, and publishing as high risk. They require explicit approval.
- A representative sample approval must bind plan, style, layout, captions, timeline revision, and the sample-window fingerprint. Its exact scope must match the current sample; drift makes the approval stale.
- Keep structural, visual, audio-measurement, human-listening, privacy, sample-approval, and final-review evidence separate in the handoff report.
- The default delivery is an editable ChatCut timeline at `review_ready`; do not add music, motion graphics, B-roll, generated media, export, or publishing by default.
- Offline fake-session checks never upgrade real ChatCut evidence. Public claims must follow `reports/live-canary-v1.7.0.json` and `npm run validate:live-claim`.

For orchestration changes, run the relevant focused tests plus:

```bash
npm run validate:runtime-contracts
npm run test:orchestration
npm run test:risk-policy
npm run test:run-state
npm run test:starter-prompts
npm run smoke:one-click:fake
npm run validate:docs-routing
```

- Bind Hosted and Desktop to their own current instructions. Never silently fall back between surfaces.
- A supplied session observation checks a declared contract only; it does not establish login, project access, media quality, or production eligibility. Refresh observations when the session or tool schema changes.
- Caption display, source transcript repair, speech cuts, and spoken audio replacement are different targets. Caption-only and transcript-only requests must not trigger A-roll cleanup. Spoken replacement is independently high risk.
- Review official source drift with `npm run check:official`; source review never upgrades live canary evidence.
