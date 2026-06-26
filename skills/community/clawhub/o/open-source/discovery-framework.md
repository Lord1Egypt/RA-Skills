# Discovery Framework - Open Source

Use this when comparing open source candidates for adoption.

## Step 1: Candidate Capture

Collect 3-7 options with direct links to source repository and docs.

Minimum data per project:
- Primary use case fit
- License type
- Last release date
- Maintainer responsiveness
- Required runtime dependencies

## Step 2: Weighted Scoring

Score each dimension from 1-5, then compute weighted total.

| Dimension | Weight | What good looks like |
|-----------|--------|----------------------|
| Functional fit | 30% | Solves core use case without heavy custom patches |
| Maintainer health | 20% | Regular releases, issue triage, clear roadmap |
| Security posture | 15% | Advisories handled, dependency hygiene, signed releases |
| Operational burden | 15% | Clear install/upgrade path, observability, backup model |
| Ecosystem fit | 10% | Integrates with user's stack and team skills |
| Exit cost | 10% | Data portability and migration realism |

## Step 3: Recommendation Format

Always provide:
1. Best default choice
2. Conservative fallback
3. High-control option (often self-host or fork)

For each choice include:
- Why it fits
- Main risk
- First implementation step

## Red Flags

- No release in >12 months with unresolved critical issues
- Single maintainer with no backup and no governance signal
- Weak upgrade documentation or no migration guidance
- License ambiguity for intended commercial use
