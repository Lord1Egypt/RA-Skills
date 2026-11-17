## Description:

Intelligent budget tracking and financial management library for AI agents, including expense tracking, income management, budgets, savings goals, and SkillBoss API Hub-powered insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let AI agents record transactions, monitor budgets, track savings goals, and produce financial summaries or insights. The skill is intended for programmatic use by agents and bots rather than a frontend application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial records may be stored locally.

Mitigation: Use a restricted CLAWHUB_DATA_PATH, limit filesystem access to the storage directory, and protect backups or exported JSON files.

Risk: Natural-language parsing and AI insights may send spending data to SkillBoss API Hub.

Mitigation: Review data sent to addFromNaturalLanguage() and generateInsights(), and avoid account identifiers, sensitive notes, or unnecessary transaction details.

Risk: The skill depends on an external npm package and API key.

Mitigation: Pin or verify the package version before use and provide SKILLBOSS_API_KEY through a scoped secret mechanism.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/mar-intelligent-budget-tracker)
- [SkillBoss Intelligent Budget Tracker Page](https://skillboss.co/skills/intelligent-budget-tracker)
- [SkillBoss API Hub Endpoint](https://api.skillboss.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript examples, shell commands, API method summaries, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for natural-language parsing and AI insights; CLAWHUB_DATA_PATH can override local storage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
