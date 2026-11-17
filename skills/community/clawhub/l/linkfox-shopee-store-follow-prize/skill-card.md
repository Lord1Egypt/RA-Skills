## Description:

Shopee（虾皮）关注有礼 Follow Prize skill for managing authorized store Follow Prize campaigns through LinkFox, covering create, list, detail, update, end, and delete operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and operators use this skill to manage Shopee Follow Prize promotions for authorized stores. It helps an agent call LinkFox/Shopee APIs, check campaign state, and create, update, end, or delete Follow Prize campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, end, and delete Shopee Follow Prize campaigns.

Mitigation: Require explicit user confirmation before any campaign mutation and verify the target shop or merchant ID before execution.

Risk: The skill handles LinkFox API keys, phone/SMS login, billing orders, and gateway environment variables.

Mitigation: Prefer session-scoped credentials, avoid persisting API keys in shell startup files where possible, and confirm any payment action before running billing commands.

Risk: The skill saves complete API responses to local JSON files.

Mitigation: Review saved response files for sensitive store or campaign data and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-follow-prize)
- [Skill API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Shopee Follow Prize add_follow_prize documentation](https://open.shopee.com/documents/v2/v2.follow_prize.add_follow_prize?module=113&type=1)
- [Shopee Follow Prize get_follow_prize_list documentation](https://open.shopee.com/documents/v2/v2.follow_prize.get_follow_prize_list?module=113&type=1)
- [Shopee Follow Prize get_follow_prize_detail documentation](https://open.shopee.com/documents/v2/v2.follow_prize.get_follow_prize_detail?module=113&type=1)
- [Shopee Follow Prize update_follow_prize documentation](https://open.shopee.com/documents/v2/v2.follow_prize.update_follow_prize?module=113&type=1)
- [Shopee Follow Prize end_follow_prize documentation](https://open.shopee.com/documents/v2/v2.follow_prize.end_follow_prize?module=113&type=1)
- [Shopee Follow Prize delete_follow_prize documentation](https://open.shopee.com/documents/v2/v2.follow_prize.delete_follow_prize?module=113&type=1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, JSON API parameters, JSON API responses, and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small API responses are printed after being saved; larger responses are summarized with top-level fields, counts, and sample records.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
