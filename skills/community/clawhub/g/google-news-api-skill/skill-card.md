## Description:

This skill helps agents retrieve structured Google News results through the BrowserAct API using search keywords, time filters, and item limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to collect current news items for topic research, trend tracking, competitor monitoring, PR monitoring, daily summaries, and market research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and task data may be sent to BrowserAct and Google News without clear user control.

Mitigation: Confirm the query, time filter, and item limit before running, and use the skill only for searches the user is comfortable sharing with those services.

Risk: The artifact includes unsafe guidance that may lead users to paste the BrowserAct API key into chat.

Mitigation: Configure BROWSERACT_API_KEY locally or through a secret manager and do not request or transmit the key in chat.

Risk: Long-running polling may continue longer than intended.

Mitigation: Monitor task status and stop the run manually if polling continues too long.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/google-news-api-skill)
- [BrowserAct Console](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON news results with terminal status logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY; polling may continue for several minutes.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
