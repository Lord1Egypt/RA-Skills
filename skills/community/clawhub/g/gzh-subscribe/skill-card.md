## Description:

Tracks WeChat Official Account posts and prepares daily reports, with an Alipay recharge flow available when API credits run low.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users can follow selected WeChat Official Accounts, review recent posts and engagement metrics, and receive a daily HTML digest. They can group subscriptions for competitor monitoring, industry discovery, or general reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted article content can run scripts in generated reports.

Mitigation: Prefer a corrected version before enabling HTML reports or daily scheduling.

Risk: Scheduling and payment setup have concrete safety gaps.

Mitigation: Require separate approval for payment-tool installation and recharge, and verify the recipient and amount in Alipay.

Risk: The API key may be stored in plaintext when using macOS scheduling.

Mitigation: Account for plaintext API-key storage before enabling macOS scheduling.

## Reference(s):

- [RedFox API key setup](https://redfox.hk/settings/api-keys?source=clawhub)
- [Alipay recharge workflow](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, HTML files]

**Output Format:** [Terminal tables and HTML daily reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include post dates, authors, titles, summaries, engagement metrics, and source links.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
