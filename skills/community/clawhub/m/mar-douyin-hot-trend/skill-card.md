## Description:

Fetches Douyin hot trend and hot search data, including ranked titles, popularity values, links, labels, content types, and cover image URLs when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, social media operators, and marketing analysts use this skill to retrieve current Douyin hot-list items for trend monitoring, content analysis, and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests through the SkillBoss/HeyBoss API service using SKILLBOSS_API_KEY.

Mitigation: Run it only in environments where that service is trusted with the key, scope the key narrowly when possible, and rotate it after testing or incident response.

Risk: Automation scripts include unsafe command execution when arguments are not trusted.

Mitigation: Do not pass user-controlled arguments to scripts/get-hot-trend.js; constrain trend limits to validated numeric values before execution.

Risk: A Telegram chat_id is hard-coded in generated automation output.

Mitigation: Remove or replace the chat_id before connecting automation to messaging tools or publishing generated output.

Risk: Douyin web endpoint structure and access controls may change or throttle frequent requests.

Mitigation: Monitor failed fetches, handle empty or changed response shapes, and avoid high-frequency polling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-douyin-hot-trend)
- [ClawHub publisher profile](https://clawhub.ai/user/marjoriebroad)
- [Douyin hot search endpoint](https://www.douyin.com/aweme/v1/hot/search/list/)
- [HeyBoss API endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files]

**Output Format:** [Plain text and Markdown summaries with JSON trend records emitted by Node.js commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and SKILLBOSS_API_KEY; the default command returns up to 50 ranked trend items unless a limit is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
