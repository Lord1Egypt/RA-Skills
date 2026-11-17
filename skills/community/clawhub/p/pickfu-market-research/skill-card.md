## Description:

Runs PickFu consumer research surveys, helps design and publish tests, monitors responses, and produces structured analysis reports with respondent quotes and demographic breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinchen](https://clawhub.ai/user/justinchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run consumer research workflows in PickFu, including survey design, audience targeting, publishing with confirmation, result monitoring, and analysis for product, pricing, brand, listing, and creative decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish surveys, add respondents, and otherwise trigger billable PickFu account actions.

Mitigation: Require explicit user confirmation before publishing or committing respondent additions, and use preview modes when available.

Risk: The CLI fallback runs @pickfu/cli@latest with account credentials, so CLI behavior can change between runs.

Mitigation: Prefer MCP or a pinned, preinstalled PickFu CLI version for controlled deployments.

Risk: Survey creation and media upload may send confidential product concepts, images, or regulated information to PickFu.

Mitigation: Use a tightly scoped PickFu API key and avoid uploading confidential or regulated material unless authorized.

Risk: Survey updates can unintentionally replace tags or alter questions if payloads include unintended fields.

Mitigation: Send only fields meant to change, include the full desired tag set for tag updates, and avoid including questions unless intentionally modifying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justinchen/skills/pickfu-market-research)
- [PickFu Homepage](https://www.pickfu.com)
- [PickFu CLI and Agents](https://agents.pickfu.com)
- [PickFu Docs](https://www.pickfu.com/docs)
- [PickFu Help](https://www.pickfu.com/help)
- [PickFu Pricing](https://www.pickfu.com/pricing)
- [PickFu API Keys](https://app.pickfu.com/settings/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON survey payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use PickFu MCP tools or the PickFu CLI and requires PICKFU_API_KEY or OAuth when not already authenticated.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
