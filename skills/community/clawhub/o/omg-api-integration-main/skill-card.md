## Description:

Use this reference when integrating with the OMG game API, including signature authentication, wallet-mode selection, game entry, transfers, reports, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willwin0801](https://clawhub.ai/user/willwin0801)

### License/Terms of Use:

MIT

## Use Case:

Developers integrating OMG game services can use this guide to choose a wallet model, implement the related API flows, and troubleshoot authentication, transaction, and reporting issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposure of signing keys could compromise authenticated API requests.

Mitigation: Protect real signing keys.

Risk: Incorrect wallet integration could cause unintended live transfers or player balance changes.

Mitigation: Verify endpoints through the merchant account and test wallet behavior outside production before authorizing live transfers or player return changes.

## Reference(s):

- [OMG API Quick Start](https://docs.omgapi.cc/kuai-su-kai-shi/quickstart.md)
- [OMG API Error Codes](https://docs.omgapi.cc/kuai-su-kai-shi/tong-yong-cuo-wu-ma.md)
- [OMG Online API Debugger](https://docs.omgapi.cc/openapi-jie-kou-zai-xian-tiao-shi/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with API tables, JSON examples, and Go code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
