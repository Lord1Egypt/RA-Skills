## Description: <br>
Konto helps agents query personal finance data from a Konto API, including bank accounts, investments, assets, loans, transactions, and financial summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelstreet](https://clawhub.ai/user/angelstreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users with a Konto API key use this skill to let an agent retrieve personal finance snapshots, account balances, transactions, investments, assets, loans, and subscription summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Konto API token can grant access to personal financial records. <br>
Mitigation: Keep the API key out of shared terminals, logs, commits, and chat transcripts; restrict token scope when the Konto service supports it. <br>
Risk: Skill outputs may include sensitive balances, transactions, holdings, loans, or subscription details. <br>
Mitigation: Review and redact financial details before sharing agent outputs with other people or systems. <br>


## Reference(s): <br>
- [Konto on ClawHub](https://clawhub.ai/angelstreet/konto) <br>
- [Konto API Reference](artifact/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with bash and curl command examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KONTO_API_KEY and KONTO_URL; returned data may include sensitive personal financial records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
