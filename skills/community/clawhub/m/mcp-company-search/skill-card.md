## Description: <br>
Searches corporate registries across multiple jurisdictions via the L402 API to find companies by name and jurisdiction for due diligence, compliance, and business research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Compliance analysts, investigators, and developers use this skill to search company registry records by jurisdiction and company name, and to list supported jurisdictions for due diligence, KYC, partner verification, and business research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The npm package name and setup examples differ across artifact files, which may cause users to install an unintended package. <br>
Mitigation: Verify the intended npm package before installation and pin the exact package version in MCP client configuration. <br>
Risk: Company names and jurisdictions submitted through the skill are sent to an external Nautdev/L402 API provider. <br>
Mitigation: Avoid submitting sensitive investigation targets unless sharing those queries with the provider is acceptable for the workflow. <br>
Risk: The documented environment variable differs between metadata and implementation, which may lead to unexpected default endpoint use. <br>
Mitigation: Use the implementation-supported NAUTDEV_BASE_URL when overriding the default API endpoint and validate configuration before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/haveblue997/mcp-company-search) <br>
- [Publisher profile](https://clawhub.ai/user/haveblue997) <br>
- [Default Nautdev API endpoint](https://api.nautdev.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, shell commands, guidance] <br>
**Output Format:** [MCP tool responses with JSON-formatted text and setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requests require a jurisdiction code and company name; jurisdiction listing has no parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
