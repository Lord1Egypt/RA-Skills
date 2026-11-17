## Description:

Limits AI model request frequency to a configured maximum per minute, defaulting to five requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazhimin-123](https://clawhub.ai/user/mazhimin-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to enable, disable, adjust, and reset workspace-level request throttling so model calls stay within an intended per-minute limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-level throttling state may continue to affect later model requests after it is enabled or changed.

Mitigation: Confirm the desired limit before enabling the skill, and disable or reset rate-limit-state.json when throttling is no longer intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mazhimin-123/skills/model-rate-limiter)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain text or Markdown with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update rate-limit-state.json fields such as enabled, maxPerMinute, windowMs, and timestamps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
