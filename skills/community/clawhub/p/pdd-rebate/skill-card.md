## Description:

拼多多返利 helps an agent guide users through WeChat authorization, convert Taobao, JD, and Pinduoduo product links into rebate links, search for rebate-eligible products, check rebate balances, and submit withdrawals after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyfile](https://clawhub.ai/user/skyfile)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to receive rebate setup guidance, product search results, rebate links, balance information, and withdrawal flow support for supported Chinese shopping platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to rebate and model-provider services.

Mitigation: Use it only when the configured service and model provider endpoints are trusted.

Risk: The skill uses WeChat/OpenID-linked account data and stores account-linked state locally.

Mitigation: Install it only in workspaces where local files are protected and account-linked data handling is acceptable.

Risk: The skill can submit a withdrawal after a typed confirmation.

Mitigation: Review withdrawal amount and account state before sending the confirmation phrase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyfile/skills/pdd-rebate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown user-facing replies, with JSON available from diagnostic CLI paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product links, rebate links or tokens, balance information, authorization links, and withdrawal status messages when returned by the configured rebate service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
