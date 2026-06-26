## Description: <br>
Search for premium domains for sale across Afternic, Sedo, Atom, Dynadot, Namecheap, NameSilo, and Unstoppable Domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[julianengel](https://clawhub.ai/user/julianengel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, domain buyers, and marketplace researchers use this skill to query whether a candidate domain appears for sale across major domain marketplaces and inspect listing details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain searches are sent to a third-party API, which may expose confidential or unreleased domain ideas. <br>
Mitigation: Avoid querying sensitive domain candidates when query privacy matters. <br>
Risk: Formatted output depends on jq being available in the runtime environment. <br>
Mitigation: Install jq for formatted JSON output or remove the jq pipe from the example command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/julianengel/premium-domains) <br>
- [Publisher profile](https://clawhub.ai/user/julianengel) <br>
- [DomainDetails marketplace search API example](https://api.domaindetails.com/api/marketplace/search?domain=example.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl to call an external domain marketplace API; jq is optional for formatted JSON output.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
