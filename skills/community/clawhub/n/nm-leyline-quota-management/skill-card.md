## Description:

Tracks quotas, monitors thresholds, and degrades gracefully for rate-limited APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design quota-aware integrations for rate-limited services, including threshold checks, usage recording, graceful degradation, and pre-flight token or cost estimation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate during generic quota or threshold discussions where its leyline-specific patterns are not appropriate.

Mitigation: Confirm the target system has rate, token, cost, or quota-management needs before applying its guidance.

Risk: The related leyline or Claude plugin may include agents, hooks, commands, or persistent quota storage outside this documentation-only artifact.

Mitigation: Review the separate plugin package before installing or enabling behavior beyond this skill.

## Reference(s):

- [Threshold Strategies](modules/threshold-strategies.md)
- [Estimation Patterns](modules/estimation-patterns.md)
- [Clawdis Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with Python and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable behavior.]

## Skill Version(s):

1.9.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
