## Description:

Haven Star Chart v2 portal training helps agents gate, validate, and propose star chart submissions with human consent, local graph and math checks, and immutable feed verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and agent operators use this skill to prepare, validate, and submit Haven Star Chart nodes through local gate checks, explicit human approval, and steward ingest before public status is claimed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a user-selected lygo-protocol-stack directory and dynamically loads allowlisted stack modules from that directory.

Mitigation: Use only a trusted lygo-protocol-stack checkout, set LYGO_STACK_ROOT deliberately, and run self_check and gate validation before live operations.

Risk: Submit and ingest commands can create persistent public chart or feed changes when consent flags are used.

Mitigation: Run --i-consent only after explicit user approval, keep steward ingest separate, and verify the immutable feed after changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-haven-star-chart)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [Project Repository URL from Release Metadata](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Live Haven Star Chart](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html)
- [Agent Portal](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html)
- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security Guidance](references/SECURITY.md)
- [SkillSpector Audit Response](references/SKILLSPECTOR_AUDIT.md)
- [Submission Training](references/SUBMISSION_TRAINING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON workflow outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live submit and ingest actions require explicit human approval and consent flags.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
