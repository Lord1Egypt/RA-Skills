## Description:

Tracks Bilibili short-drama content, filters popular works by likes, clusters themes, and generates a local HTML daily report with creative trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Short-drama creators, MCN operators, production teams, and content strategists use this skill to monitor Bilibili short-drama trends, compare themes, and prepare daily creative trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically open locally generated HTML built from third-party data.

Mitigation: Review generated reports before broad use and require HTML escaping, URL validation, a restrictive content security policy, and an option to disable browser auto-open.

Risk: Queries and the API key are sent to redfox.hk.

Mitigation: Use only a revocable RedFoxHub API key and verify its scope, validity period, and reset process before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/playlet-bili-feed)
- [Core Workflow](references/core_workflow.md)
- [Usage Examples](references/examples.md)
- [RedFoxHub](https://redfox.hk/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown trend report, shell commands, configuration guidance, and generated local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; generated reports are saved locally and may open in a browser.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
