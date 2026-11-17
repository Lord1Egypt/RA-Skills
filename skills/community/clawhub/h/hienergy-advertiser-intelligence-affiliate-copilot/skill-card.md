## Description:

HiEnergy Advertiser Intelligence Affiliate Copilot helps agents use HiEnergy API v1 to research affiliate advertisers, programs, deals, commissions, transactions, contacts, status changes, agencies, tags, categories, and publisher details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyptkarsh](https://clawhub.ai/user/flyptkarsh)

### License/Terms of Use:

MIT-0

## Use Case:

External affiliate marketers, partner marketing operators, and developers use this skill to search HiEnergy data for advertiser intelligence, affiliate program research, deal discovery, transaction reporting, and partner contact lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change account data through contact creation, contact replacement, or publisher update capabilities.

Mitigation: Use least-privilege HiEnergy API keys when available and require human confirmation before any contact creation, reassignment, or publisher update.

Risk: The skill can expose contacts or transaction data available to the configured HiEnergy account.

Mitigation: Review outputs before sharing them and run the skill only in environments appropriate for the account's advertiser, contact, and transaction data.

Risk: Debug scripts may reveal sensitive request or account context in logged environments.

Mitigation: Avoid running debug scripts in shared or retained logs, and do not pass API keys on the command line.

## Reference(s):

- [HiEnergy homepage](https://www.hienergy.ai)
- [HiEnergy API documentation](https://app.hienergy.ai/api_documentation)
- [HiEnergy API key documentation](https://app.hienergy.ai/api_documentation/api_key)
- [Endpoint reference](references/endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with structured result sections and optional Python or shell snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HiEnergy API key; returned data depends on the user's HiEnergy account access.]

## Skill Version(s):

2.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
