## Description: <br>
Operates Google Ads through the OOMOL googleads connector for reading, creating, updating, and deleting advertising account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Google Ads accounts through OOMOL, including customer discovery, campaign and ad group mutations, GAQL search, and Customer Match list workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Google Ads campaigns, ad groups, and customer lists. <br>
Mitigation: Review the exact target, payload, and expected account impact before approving write or destructive actions. <br>
Risk: The skill requires OAuth access and sensitive connector credentials managed through OOMOL. <br>
Mitigation: Install only when OOMOL is trusted for the connected Google Ads account and verify the connection scope before use. <br>


## Reference(s): <br>
- [ClawHub Google Ads skill page](https://clawhub.ai/oomol/oo-googleads) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Google Ads homepage](https://ads.google.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL Google Ads connection](https://console.oomol.com/app-connections?provider=googleads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and an execution id under meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
