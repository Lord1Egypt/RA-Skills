## Description:

NewsPulse helps agents retrieve and filter cryptocurrency news by topic, importance, and sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gztanht](https://clawhub.ai/user/gztanht)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to query cryptocurrency news, search live RSS feeds, and filter results by coin, topic, importance, or sentiment. It is informational only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use an unpinned remote npx package.

Mitigation: Verify the registry package and pin a reviewed version before installation or execution.

Risk: The main news command displays mock data in a market-news format.

Mitigation: Treat the main news output as demonstration data and verify market-current information from original sources.

Risk: Live RSS search output can include third-party links.

Mitigation: Open links cautiously and confirm the source domain and article accuracy before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gztanht/skills/newspulse)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Package manifest](package.json)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text tables and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm and node; search output may include external RSS links.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
