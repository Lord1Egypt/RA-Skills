## Description: <br>
Query Idealista API via idealista-cli (OAuth2 client credentials). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quifago](https://clawhub.ai/user/quifago) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure Idealista API credentials, run idealista-cli commands, search real estate listings, and compute listing statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external idealista-cli repository installed from GitHub. <br>
Mitigation: Review the repository before installing it or pin a known commit for repeatable installation. <br>
Risk: Idealista API credentials may be exposed if stored or committed insecurely. <br>
Mitigation: Prefer environment variables or a secret manager; keep any local config file private and rotate credentials if exposure is suspected. <br>
Risk: Search locations and property criteria are sent to Idealista during normal API use. <br>
Mitigation: Avoid submitting sensitive location or search criteria unless sharing that data with Idealista is acceptable for the intended use. <br>


## Reference(s): <br>
- [idealista-cli GitHub repository](https://github.com/quifago/idealista-cli) <br>
- [Idealista ClawHub page](https://clawhub.ai/quifago/idealista) <br>
- [quifago ClawHub publisher profile](https://clawhub.ai/user/quifago) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples for token management, listing search, and aggregate statistics.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
