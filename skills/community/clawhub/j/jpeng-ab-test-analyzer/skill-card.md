## Description:

Analyze A/B test results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics teams use this skill to run A/B test analysis workflows and return structured JSON results for automation or reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires AB_API_KEY, but the evidence does not identify the authenticated service or data handling path.

Mitigation: Confirm the service behind AB_API_KEY and whether experiment data is sent externally before using the skill.

Risk: Secrets may be exposed if the API key is pasted into shared files, shell history, or logs.

Mitigation: Store AB_API_KEY in a secure secret manager or local environment and avoid committing or logging it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-ab-test-analyzer)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON result expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described analyzer returns JSON results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
