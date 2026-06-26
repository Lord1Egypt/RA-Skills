## Description: <br>
CompanyEnrich helps agents search, count, enrich, and find similar company profiles through an OOMOL-connected CompanyEnrich account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to query CompanyEnrich company data, enrich company profiles, find similar companies, and inspect account capabilities through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an authenticated OOMOL account with CompanyEnrich connected credentials. <br>
Mitigation: Use an account and CompanyEnrich connection with the minimum scopes needed, and reconnect only when an auth or connection error requires it. <br>
Risk: Connector actions depend on live schemas and may fail if the user is not signed in, the provider is not connected, credentials expire, or billing credit is unavailable. <br>
Mitigation: Inspect the live action schema before building payloads and follow the documented setup or billing recovery steps only after the matching failure occurs. <br>
Risk: Search and enrichment results come from an external company-data service and may be incomplete or outdated. <br>
Mitigation: Treat returned company data as source data for review and verify business-critical decisions against authoritative records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-companyenrich) <br>
- [CompanyEnrich homepage](https://companyenrich.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions may return JSON data from the CompanyEnrich connector with an execution id in response metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
