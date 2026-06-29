## Description: <br>
Scrapingdog helps agents search and read web, Google Search, Google Maps, and Google Scholar data through an OOMOL-connected Scrapingdog account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route Scrapingdog scraping, search, Maps, Scholar, and account-usage requests through the OOMOL connector without handling raw API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scrapingdog requests and results flow through the OOMOL connector account, and queried URLs or search terms may be sensitive. <br>
Mitigation: Install only after trusting OOMOL and the oo CLI, and avoid sending confidential targets or queries unless the connected account and data handling are approved. <br>
Risk: The skill depends on a signed-in OOMOL account, a connected Scrapingdog credential, and sufficient account credit. <br>
Mitigation: Use the documented authentication, connection-renewal, and billing-error paths only when commands fail for those reasons. <br>


## Reference(s): <br>
- [Scrapingdog homepage](https://www.scrapingdog.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-scrapingdog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and meta.executionId when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
