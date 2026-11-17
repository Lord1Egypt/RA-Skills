## Description:

Reviews code changes by using an LLM to simulate Jev-style Noul, Score, and Choice primitives and return structured, probability-based findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentforge-cyber](https://clawhub.ai/user/agentforge-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review files, diffs, or commits for security, correctness, maintainability, and performance concerns, with recommendations for when human review is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed code, diffs, and possibly secrets may be sent to the external Kimi CLI available in the environment.

Mitigation: Use the skill on non-sensitive repositories, or add explicit consent, redaction, and a local-only option before using it on private codebases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentforge-cyber/skills/jev-code-review)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Human-readable text or structured JSON review results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags security, correctness, maintainability, performance, and human-review recommendations with configured thresholds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
