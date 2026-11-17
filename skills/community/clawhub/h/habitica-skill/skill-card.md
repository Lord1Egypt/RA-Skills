## Description:

Habitica integrates an agent with Habitica's gamified task manager to list, create, update, score, and review tasks, account state, collections, party activity, class skills, quests, and history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyunturn](https://clawhub.ai/user/tonyunturn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent operate a Habitica account through a CLI, including task management, user and inventory review, party chat, quest acceptance, class-skill casting, history lookup, and daily cron execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a Habitica account, including task deletion, scoring, updates, quest acceptance, class-skill casting, cron execution, and party chat posting.

Mitigation: Require explicit user confirmation before destructive, social, batch, cron, quest, or class-skill actions.

Risk: Habitica API tokens provide account access and may be loaded from the user's configuration file.

Mitigation: Keep the API token private, restrict access to the Habitica configuration file, and avoid exposing credentials in prompts, logs, or shared outputs.

Risk: Automated or repeated API calls can affect live Habitica game state and party interactions.

Mitigation: Respect the documented 30-second spacing for automated calls and review planned batch operations before execution.

## Reference(s):

- [ClawHub Habitica skill](https://clawhub.ai/tonyunturn/skills/habitica-skill)
- [Habitica API v3](https://habitica.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Habitica user ID and API token credentials; CLI responses depend on Habitica API state.]

## Skill Version(s):

0.1.3 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
