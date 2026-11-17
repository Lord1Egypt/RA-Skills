## Description:

Find hiking trails from easy walks to challenging mountain treks, including difficulty levels, elevation, duration, packing guidance, and related travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to find hiking trails, mountain treks, and easy walks by city, then format live flyai CLI results into human-readable Markdown with booking links and practical trip details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and run an unpinned third-party travel CLI globally.

Mitigation: Install the CLI in an isolated environment, pin the package version, and review the package source and permissions before use.

Risk: The workflow makes external travel lookups and prioritizes booking links.

Mitigation: Treat booking results as third-party commercial links, verify destinations before purchase, and avoid using the skill where external travel-service calls are not approved.

Risk: The runbook allows local logs that may retain raw user travel queries.

Mitigation: Disable persistent logging where possible, redact sensitive query details, and periodically remove local execution logs.

Risk: The skill scope extends beyond hiking into broader travel booking services.

Mitigation: Review activation rules and limit deployment to contexts where broader travel booking behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/hiking-trails)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [Parameter and output templates](references/templates.md)
- [Scenario playbooks](references/playbooks.md)
- [Fallback procedures](references/fallbacks.md)
- [Execution log schema](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, comparison tables, booking links, and concise fallback messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires city-name input and a working flyai CLI; output should be based on CLI results rather than model training data.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
