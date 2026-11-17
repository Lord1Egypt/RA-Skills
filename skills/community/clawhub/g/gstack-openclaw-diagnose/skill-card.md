## Description:

Structured diagnosis for hard bugs and performance regressions through deterministic feedback loops, reproduction, ranked hypotheses, targeted instrumentation, fixes, regression tests, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilmych](https://clawhub.ai/user/ilmych)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate hard bugs, flaky failures, and performance regressions with a repeatable loop before changing code. It guides the agent toward reproducing the issue, testing ranked hypotheses, adding targeted instrumentation, applying a fix, and verifying cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic artifacts such as HAR files, logs, dumps, or recordings may contain secrets, personal data, or production-sensitive details.

Mitigation: Confirm what will be captured before collection, redact secrets and personal data, and limit artifact retention and access.

Risk: Temporary probes or production instrumentation may remain after diagnosis.

Mitigation: Track temporary instrumentation during investigation and require cleanup after the issue is diagnosed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ilmych/skills/gstack-openclaw-diagnose)
- [Publisher Profile](https://clawhub.ai/user/ilmych)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with proposed tests, instrumentation, code changes, shell commands, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewable debugging plans and implementation guidance; no bundled code executes automatically.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
