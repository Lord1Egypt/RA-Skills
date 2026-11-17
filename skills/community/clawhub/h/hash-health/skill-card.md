## Description:

Hash Health supports personal nutrition tracking, meal logging, medication management, and daily health dashboards for food, meal, nutrition, calorie, macro, medication, and health-tracking requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devak208](https://clawhub.ai/user/devak208)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to connect an agent to their Hash Health account for meal logging from text or images, daily nutrition review, meal history, medication management, and nutrition chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send and save sensitive food, nutrition, health, and medication-related data through the configured Hash Health endpoint.

Mitigation: Install only when users are comfortable with that data flow and configure the token through OpenClaw environment settings rather than chat.

Risk: Casual food or health statements may be processed or logged without a separate confirmation step.

Mitigation: Review the skill behavior before deployment and inform users which phrases trigger immediate logging or processing.

## Reference(s):

- [Hash Health homepage](https://hash-claude-mcp.vercel.app)
- [Hash Health skill page](https://clawhub.ai/devak208/skills/hash-health)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with request examples and concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HASH_HEALTH_TOKEN and sends food, meal, nutrition, and medication-related data to the configured Hash Health endpoint.]

## Skill Version(s):

1.0.9 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
