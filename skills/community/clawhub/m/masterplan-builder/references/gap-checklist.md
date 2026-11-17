# Planning & Governance Gap Checklist

These are standard-industry planning artifacts that a masterplan is incomplete without — separate from the code-level production standards in `production-standards.md`. Treat a missing item here as a Blocker or Major gap in the plan, not an optional extra, unless the section explicitly says it can be skipped.

## Risk register
- At least the top 5 project risks identified (technical, scope, resourcing, external/vendor), each with likelihood, impact, and a concrete mitigation — "we'll figure it out" is not a mitigation.
- Missing entirely = Blocker for any project beyond a trivial script.

## Cost & budget
- Infra/hosting cost estimated at launch scale and at stated year-one scale, not just "cheap to start."
- Per-call cost called out explicitly for any metered third-party API (LLM/AI APIs especially — these can dominate cost at scale and are frequently missed).
- One-time costs (store fees, certificates, licenses, design assets) listed.
- If a budget ceiling exists, confirm it was actually respected by the tech-stack choices made earlier — a mismatch here is a Major gap that should send the plan back to the tech-stack section.

## Security threat model
- Trust boundaries mapped: what's public-facing, what's internal, where user input enters.
- Each boundary walked through against spoofing, tampering, repudiation, information disclosure, denial of service, and privilege escalation (STRIDE) with a stated defense for each that applies.
- Decision recorded on whether a third-party audit/pen test gates launch.
- Missing entirely on anything handling user data, auth, or payments = Blocker.

## Reliability targets
- Uptime/availability target stated (or explicitly "not applicable") for anything that's a running service.
- RTO/RPO stated for anything with a database or persistent state — how fast must it recover, how much data loss is tolerable.
- Incident definition and response expectation stated.

## Versioning & release policy
- Versioning scheme named (semver or equivalent) and what counts as breaking.
- Backward-compatibility and deprecation policy stated for anything with external consumers (a public API, an SDK, a file format others depend on).

## Team & roles
- Ownership per layer named if it's a team project. Skip cleanly for solo/personal projects — do not force a RACI table on a one-person project.

## Post-launch maintenance & support
- Explicit answer on who maintains this after launch and how often dependencies get updated — "ships and gets abandoned" is a valid answer if that's genuinely the case, but it must be a stated decision, not a silent gap, because it changes how much operational automation is worth building now.

## Vendor lock-in / exit strategy
- For every major third-party dependency the project can't easily live without (cloud provider, auth provider, payment processor, model API): the cost of switching away later is named, and a decision is recorded on whether that's acceptable or whether it justifies an abstraction layer now.

## Infrastructure as code
- Explicit decision recorded: IaC (with named tool) vs manual console management. Defaulting to manual by omission (never having asked) is a gap.

## Analytics & KPI tracking
- Concrete success metrics named (not "we'll check analytics later") and instrumenting them is present as a line item in the build roadmap, not assumed to happen automatically.

## Market & competitive context
- Only required for commercial projects — skip cleanly for internal/personal/non-commercial ones.
- Nearest existing alternatives named, and what this project does differently, feeding back into feature prioritization.

## Self-audit before finalizing
Before the masterplan file is written as final, walk it against this checklist and `production-standards.md` end to end and list, internally, anything that still reads as a Blocker or Major gap. Fix those in the draft. Do not deliver a masterplan you know still has a Blocker or Major gap open — that defeats the purpose of the plan being the single source of truth. Minor/Polish-level gaps can be noted in the plan's Open Questions section instead of blocking delivery.

Specifically check every phase of the build roadmap for two failure patterns that are easy to miss because they don't look wrong at a glance:
- **Dead code left behind** — does any phase introduce code/config/flags that a later phase makes obsolete without an explicit "remove X" step? A roadmap that only ever adds and never removes accumulates dead code by construction. Every phase that supersedes earlier work must say so and say to delete what it replaces.
- **Silent failure paths** — does any error-handling, fallback, retry, or degraded-mode behavior specified anywhere in the plan lack a stated way to observe it (log/metric/alert)? A fallback that isn't observable is indistinguishable from success until it causes a real incident — treat any such gap as a Major finding, not a nitpick.
