# Provisioning Playbook (Auto Install + Permission Setup)

Run this after role confirmation and before final handoff.

## 1) Build provisioning plan
For each role:
- map tools/skills via `capability-matrix.md`
- map permission profile via `permission-profiles.md`
- produce one consolidated plan for user review

## 2) Install skill dependencies (automatic by default)
Default policy: install both **required** and **optional** skills automatically, then present full results to user.

For each skill:
1. search with `skillhub search <keywords>` first
2. if no match/error/rate-limit, fallback to `clawhub`
3. perform security pre-check before install:
   - **primary scanner: `skill-vetter`** protocol
   - inspect source and publisher trust signal
   - inspect version and recency
   - inspect notable risk signals (network access, exec/shell usage, external messaging, credential scope, download-and-execute patterns)
   - classify risk (LOW / MEDIUM / HIGH / EXTREME)
4. if risk is HIGH/EXTREME, mark as `blocked_for_review` and skip auto-install for that item
5. install non-blocked items automatically

No per-item confirmation is required under this policy; instead provide a complete post-install report.
If `skill-vetter` is unavailable, fallback to `yoder-skill-auditor` or manual rule-based review, and record which method was used.

## 3) Apply tool permissions per role
- assign tool whitelist from profile
- keep non-required tools disabled
- keep elevated exec disabled by default
- scope file operations to workspace where applicable

## 4) Configure channel requirements
- map role -> channel identity/bot
- validate binding prerequisites
- mark unresolved mappings as blockers

## 5) Validate readiness
Per role checks:
- tool invocation check (required tools)
- skill availability check (required skills)
- collaboration callback check (delegation + return-path)

Status values:
- ready
- partially_ready (with blockers)
- blocked (must fix before use)

## 6) Return final provisioning report (mandatory full disclosure)
Include:
- requested skills (required/optional)
- installed skills (source, version)
- skipped/blocked skills and exact reason
- security check summary per skill (risk signals)
- permission profiles applied per role
- unresolved blockers
- operator next actions

Also include machine-readable JSON using `security-report-schema.md`.
Use JSON decisions directly for installation gating.
