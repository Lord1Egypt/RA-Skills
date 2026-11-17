## Description:

Rewrites AI-generated text into more natural, channel-specific prose and can detect common AI-sounding phrases without rewriting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odinbot33](https://clawhub.ai/user/odinbot33)

### License/Terms of Use:


## Use Case:

Agents, content editors, and developers use this skill to rewrite AI-generated drafts for Twitter/X, LinkedIn, blog, email, Telegram, or general prose while preserving the core message. They can also run detection-only mode to identify common robotic phrasing before editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for rewriting is sent to Anthropic using the configured API key.

Mitigation: Avoid secrets, regulated data, and confidential drafts unless that external processing is approved.

Risk: Rewritten output may change tone, emphasis, or wording in ways that are unsuitable for publication or downstream automation.

Mitigation: Review rewritten text before publishing it or passing it into another automated workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odinbot33/skills/oee-content-humanizer)
- [Artifact documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text output with Markdown usage examples and command-line options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rewrite mode requires ANTHROPIC_API_KEY and sends submitted text to Anthropic; detection-only mode reports matching AI tell phrases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
