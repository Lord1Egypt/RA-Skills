## Description:

A continuously adaptive skill suite that helps Clawdbot act as a coder, business analyst, project manager, web developer, data analyst, and read-only NAS metadata scraper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and project teams use this skill for coding help, business and project analysis, web and data development, resource discovery through SkillBoss API Hub, and read-only NAS metadata collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may route requests through a third-party API hub.

Mitigation: Use it only after reviewing data sharing and retention expectations, and provide SKILLBOSS_API_KEY only when approved.

Risk: The skill can inspect NAS file names, metadata, and directory structure.

Mitigation: Point it only at directories approved for metadata inspection and preserve the documented read-only posture.

Risk: The skill has a broad assistant scope across coding, business, project, web, data, and scraping tasks.

Mitigation: Review generated guidance, code, commands, and configuration before applying them.

## Reference(s):

- [Moltbot Skills Documentation](https://docs.molt.bot/tools/skills)
- [Adaptive Suite on ClawHub](https://clawhub.ai/modestyrichards/skills/modesty-adaptive-suite)
- [SkillBoss API Hub](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text with code, command, and configuration snippets as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require python, node, curl, sqlite3, and SKILLBOSS_API_KEY for some workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
