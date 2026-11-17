## Description:

Missing rate limit detector for API codebases that scans Express/Koa/Fastify/NestJS, FastAPI/Flask/Django, Go (gin/chi/echo), Spring Boot, and Ruby (Rack) for 10 classes of unprotected endpoints, including auth routes open to brute force, payment endpoints with no throttle, email/SMS senders without limits, search routes with no query throttle, retry logic without backoff, and admin endpoints without per-IP limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit API codebases for missing or weak rate limiting, then review severity-ranked findings before release or in CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regex proximity checks can produce false positives when rate limiting is enforced by centralized middleware or an abstracted framework pattern.

Mitigation: Treat findings as review prompts and confirm route-level or global protections in the application before labeling an endpoint vulnerable.

Risk: The scanner reads source files under the user-selected path.

Mitigation: Run it locally against the intended repository or file only, and avoid scanning unrelated directories that contain sensitive source material.

Risk: CI gating can block merges when CRITICAL or HIGH findings are heuristic rather than confirmed vulnerabilities.

Mitigation: Review high-severity findings before merge decisions and document intentional exceptions with the artifact-supported ignore comment where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-rate-limit-audit)
- [Canlah AI homepage](https://canlah.ai)
- [ClawHub publisher profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown/text report with severity-ranked findings, remediation notes, and optional CI failure status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports directory or single-file scans, severity filtering, verbose finding context, and CI mode that exits nonzero on CRITICAL or HIGH findings.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
