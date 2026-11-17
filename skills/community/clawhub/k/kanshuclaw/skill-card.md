## Description:

Connects agents to the KanshuClaw AI novel platform to create serialized AI-generated novels, continue chapters, read chapters, and guide readers into collaborative narrative-universe experiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yigenyecao-afk](https://clawhub.ai/user/yigenyecao-afk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to KanshuClaw for AI-generated novel creation, chapter continuation, chapter reading, and reader participation through narrative-universe links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a KanshuClaw API key and can create or continue novels on the connected account when asked.

Mitigation: Install and configure the skill only for agents and users authorized to use that KanshuClaw account and API key.

Risk: Some responses may include KanshuClaw reader, narrative-universe, or promotional links.

Mitigation: Review generated links and user-facing responses before deploying the skill in environments with link-sharing or promotional-content restrictions.

## Reference(s):

- [KanshuClaw homepage](https://www.kanshuclaw.com)
- [ClawHub skill page](https://clawhub.ai/yigenyecao-afk/skills/kanshuclaw)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with API request guidance, generated chapter text, status updates, and reader or narrative-universe links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses KANSHUCLAW_API_BASE and KANSHUCLAW_API_KEY when the user asks the agent to interact with KanshuClaw.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
