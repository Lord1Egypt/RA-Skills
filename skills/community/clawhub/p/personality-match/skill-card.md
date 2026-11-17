## Description:

Take a personality test and get your bot badge, then invite your human to see how well you match!

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiansiyu0210](https://clawhub.ai/user/tiansiyu0210)

### License/Terms of Use:


## Use Case:

External users invoke this skill to have an AI bot answer a short personality quiz, receive a multilingual badge, and share a matching link with a human user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends generated personality answers, bot name/personality context, locale, and a Telegram-token-derived identifier to a third-party API.

Mitigation: Review the publisher's consent, retention, deletion, and endpoint ownership documentation before installing or invoking the skill.

Risk: The skill stores or reuses an external botId and encourages sharing a match link.

Mitigation: Confirm users understand the external sharing flow and validate links before distributing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiansiyu0210/skills/personality-match)
- [Publisher profile](https://clawhub.ai/user/tiansiyu0210)
- [Personality questions API](https://aimatchforyou-production.up.railway.app/api/bot/questions)
- [Personality quiz submission API](https://aimatchforyou-production.up.railway.app/api/bot/quiz)
- [Match experience site](https://youandai.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown response with badge details, match link, and optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the detected locale and may include a persistent botId and shareable match link returned by the external API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
