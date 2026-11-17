## Description:

Audit an LLM-as-judge with juryrig — position bias, verbosity bias, prompt injection, consistency, and calibration via CLI or HttpJudge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to check LLM judges for bias, prompt-injection susceptibility, consistency, and calibration before relying on their scores or adding CI gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted audits send test cases to the selected provider and may incur charges.

Mitigation: Start with MockJudge and small synthetic cases; use a local endpoint when appropriate and keep secrets and sensitive data out of case files.

Risk: The external dependency was not fully audited, and the security guidance notes a prior API-key forwarding issue for custom endpoints.

Mitigation: Use a reviewed dependency version and endpoint-specific credentials when connecting to third-party services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianalloway/skills/judge-audit)
- [juryrig source and documentation](https://github.com/ianalloway/juryrig)
- [juryrig on PyPI](https://pypi.org/project/juryrig/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell and Python snippets and JSON case fixtures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit findings and pass/fail status depend on the selected judge, test cases, and thresholds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
