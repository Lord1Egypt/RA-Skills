## Description:

Generate social media content and publish to all major platforms from one command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarekhoury](https://clawhub.ai/user/tarekhoury)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Powerpost to have an agent draft, generate media for, schedule, publish, and review analytics for social media posts across connected platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule content to connected social media accounts and may spend PowerPost credits.

Mitigation: Use draft-only or read-only API key scopes unless publication is intended, and review each draft before approving publication or scheduling.

Risk: Prompts, uploaded media, URLs, generated content, API key, and workspace ID are sent to PowerPost to perform the requested workflows.

Mitigation: Install only when this data sharing is acceptable, avoid sensitive inputs, and use the minimum API key scopes needed for the task.

## Reference(s):

- [PowerPost Homepage](https://powerpost.ai)
- [PowerPost API Docs](https://powerpost.ai/docs)
- [PowerPost Support](https://powerpost.ai/contact)
- [ClawHub Skill Page](https://clawhub.ai/tarekhoury/skills/openclaw-powerpost)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples, API request examples, generated social copy, media links, scheduling status, and analytics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PowerPost API key, workspace ID, credits, and connected social accounts; publication and scheduling should be reviewed before approval.]

## Skill Version(s):

0.4.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
