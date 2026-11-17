## Description:

Автономная управленческая сводка бизнеса без ключей: счета, остатки, обороты, платежи, ограничения, налоги, документы, доверенности, карты, наличные, QR, тарифы, ликвидность, риски и действия на сегодня.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladbigbrain](https://clawhub.ai/user/vladbigbrain)

### License/Terms of Use:

MIT-0

## Use Case:

Business leaders and operators use this skill to get a concise Russian-language view of company cash, obligations, operational risks, documents, cards, cash, QR payments, tariffs, liquidity, and next actions from a packaged local demo/test snapshot. The skill is read-only and does not perform banking operations or modify data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad business, money-related, or numbered follow-up prompts.

Mitigation: Install it only for workspaces where a Russian-oriented business-summary assistant over packaged demo/test data is expected, and review broad activations before relying on the response.

Risk: The packaged snapshot includes test-contour and artificial demo data rather than real company data.

Mitigation: Treat generated summaries as demo/test-context guidance and keep source attribution visible so readers can distinguish get_data API test data from mock data.

Risk: Users may ask the skill to perform banking or account-management actions it cannot execute.

Mitigation: Keep responses read-only: answer from confirmed snapshot facts, explain unavailable actions plainly, and avoid stating that a banking action was performed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vladbigbrain/skills/operational-director)
- [Bundled business snapshot](artifact/assets/get_data.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Russian Markdown summaries with source attribution, backed by compact JSON snapshot data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only local snapshot; requires python3; no API keys or credential environment variables are required.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
