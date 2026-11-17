## Description:

Delivers a daily news digest to a Discord channel via webhook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottll](https://clawhub.ai/user/scottll)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to gather recent AI and technology news, format a five-story digest, and post it to a Discord channel for one-off or scheduled briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post messages to Discord unintentionally if run with the wrong webhook or without confirmation.

Mitigation: Use only an explicit Discord destination and require confirmation before any one-off post or recurring schedule.

Risk: Passing webhook values or story JSON directly through command-line arguments can expose secrets or mishandle news text.

Mitigation: Store the webhook as a secret, restrict it to real Discord webhook URLs, and pass story JSON through a safe file or non-shell argument API.

## Reference(s):

- [AI news generator ClawHub page](https://clawhub.ai/scottll/skills/news-ai-001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON story data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces up to five news story summaries and posts them as a Discord embed through a webhook.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
