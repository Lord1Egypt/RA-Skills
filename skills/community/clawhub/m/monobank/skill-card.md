## Description: <br>
Answer Monobank balance questions by calling the Monobank API directly with a user-supplied per-request API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftadviser](https://clawhub.ai/user/swiftadviser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Monobank account and jar balances with a per-request token, format balances safely, and answer in Ukrainian by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Monobank API token and balance details are sensitive financial data. <br>
Mitigation: Ask for the token only for the current request, call the Monobank API directly, and do not log, store, summarize, forward, or expose the token. <br>
Risk: Raw account identifiers or API errors could reveal private banking details. <br>
Mitigation: Mask account labels, avoid raw identifiers and full IBANs, and summarize API errors without printing sensitive response content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swiftadviser/monobank) <br>
- [Monobank client-info endpoint](https://api.monobank.ua/personal/client-info) <br>
- [Monobank API token page](https://api.monobank.ua/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Concise text response, Ukrainian by default] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-supplied Monobank API token per request; should not store or expose tokens, raw account identifiers, client IDs, webhook URLs, or raw API errors.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
