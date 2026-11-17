## Description:

Executes Meta Ads campaign management tasks, including creating campaigns, changing budgets, pausing or activating campaigns, duplicating campaigns, and summarizing campaign state when Meta Ads credentials are available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to launch, modify, review, duplicate, pause, activate, and troubleshoot Meta Ads campaigns through the Meta Marketing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable Meta Ads credentials can affect real ad accounts and budgets.

Mitigation: Use a limited, preferably short-lived token stored in secret management and review every campaign or budget change before execution.

Risk: Access tokens may be exposed through chat, command logs, or URLs when curl examples are used.

Mitigation: Do not paste tokens into chat, avoid printing tokens, and rotate the token if it may have appeared in logs or URLs.

Risk: Activating or modifying campaigns without review can cause unintended spend or targeting changes.

Mitigation: Create new campaigns paused, confirm budgets and targeting, and activate only after human review.

## Reference(s):

- [Meta Ads Publisher on ClawHub](https://clawhub.ai/elias-didoo/skills/meta-ads-publisher)
- [Publisher profile](https://clawhub.ai/user/elias-didoo)
- [Didoo AI blog](https://didoo.ai/blog)
- [Meta Graph API endpoint](https://graph.facebook.com/v21.0/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline API request examples, status summaries, and readable tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires META_ACCESS_TOKEN and META_AD_ACCOUNT_ID; campaign-changing operations should be reviewed before activation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
