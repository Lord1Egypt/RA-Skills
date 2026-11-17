## Description:

健康追踪 tracks water intake, sleep, steps, weight, and basic health statistics in local JSON records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to record daily water intake, sleep, steps, and weight, then summarize current-day and weekly health statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal health logs may be saved locally as plaintext JSON.

Mitigation: Use the skill from a private, non-synced workspace; avoid shared folders; delete health_data.json when records should no longer be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-health)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown summaries with JSON-backed record examples and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores health records in a local plaintext JSON file when the provided code is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
