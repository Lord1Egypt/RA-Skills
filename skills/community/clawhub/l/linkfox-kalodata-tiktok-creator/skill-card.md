## Description:

通过 Kalodata data, this skill helps agents browse TikTok Shop creator leaderboards and fetch a selected creator's profile, sales, audience, content, live, product, shop, and contact metrics by creatorId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, analysts, and e-commerce operators use this skill to discover high-performing TikTok Shop creators by market and time window, then inspect one creator's detailed performance and contact data. It is intended for creator ranking, comparison, and profile lookup workflows rather than product, shop, livestream, or ad campaign management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the skill handles creator queries, account onboarding data, payment actions, and local cached results.

Mitigation: Install only when the publisher is trusted, review the skill before use, and clear local linkfox cache and output files when they may contain contact or business data.

Risk: Authentication and onboarding flows can expose API keys, phone numbers, SMS codes, and billing actions in local terminals or logs.

Mitigation: Prefer self-service key setup, avoid entering SMS codes or API keys in shared terminals, and review payment details before running billing commands.

Risk: The skill allows custom gateway and login URLs through environment variables, which could redirect sensitive requests.

Mitigation: Use the default LinkFox endpoints unless an administrator has explicitly approved alternate gateway or login URLs.

Risk: The artifact describes automatic feedback reporting behavior that may send interaction feedback outside the current workspace.

Mitigation: Disable or remove automatic feedback reporting before deployment if outbound feedback collection is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-kalodata-tiktok-creator)
- [Kalodata-TikTok达人搜索与详情 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries and tables, JSON API responses, saved JSON files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and detail scripts always save full responses under a local linkfox session directory; small responses may also be printed inline, while larger responses are summarized unless --inline is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
