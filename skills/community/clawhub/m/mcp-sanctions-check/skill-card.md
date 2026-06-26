## Description: <br>
Check names against the OFAC SDN (Specially Designated Nationals) sanctions list via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance-focused agents use this skill to screen names before payments, onboarding, KYC checks, and international business workflows. It returns sanctions match status with matched OFAC SDN entries and timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README and package metadata identify different npm package scopes. <br>
Mitigation: Verify the intended npm package scope before installation and pin the reviewed package in MCP client configuration. <br>
Risk: Sanctions screening names may contain sensitive personal or business information. <br>
Mitigation: Handle submitted names according to the user's data governance requirements and avoid logging unnecessary query details. <br>
Risk: The tool downloads and caches the OFAC SDN CSV locally for up to 24 hours. <br>
Mitigation: Confirm cache freshness requirements for the deployment context and clear or refresh the cache when current-list checks are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haveblue997/mcp-sanctions-check) <br>
- [OFAC SDN CSV](https://www.treasury.gov/ofac/downloads/sdn.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [MCP tool response containing JSON serialized as text, plus setup configuration guidance in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns match status, matched entries, programs, remarks, and check timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
