## Description:

Opencli Content Hunter helps agents use opencli to collect trending and keyword-related content across many web, media, social, finance, design, podcast, and developer platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[judefluen-coder](https://clawhub.ai/user/judefluen-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to choose content platforms, verify opencli and Chrome extension setup, run collection commands, and summarize cross-platform trends or keyword search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install persistent components that reuse Chrome logins.

Mitigation: Review before installing, use a separate Chrome profile or low-risk accounts, and prefer pinned and verified dependency versions.

Risk: Helper scripts and opencli commands can make platform requests beyond a narrow confirmed scope.

Mitigation: Do not run the helper script unless Bilibili and Xiaohongshu test requests are acceptable, and confirm the selected platforms before collection.

Risk: Setup and platform-selection details may be visible in group-chat workflows.

Mitigation: Avoid group-chat use unless everyone in the chat should see setup status and selected platform details.

## Reference(s):

- [Opencli extension releases](https://github.com/jackwener/opencli/releases)
- [Opencli Content Hunter ClawHub page](https://clawhub.ai/judefluen-coder/skills/opencli-content-hunter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown/text guidance with shell command blocks and summarized platform reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup checks, platform-selection prompts, login guidance, collection commands, and trend summaries.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
