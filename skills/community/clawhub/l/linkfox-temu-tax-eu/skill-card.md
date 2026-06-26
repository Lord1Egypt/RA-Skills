## Description: <br>
Helps agents call LinkFox-gatewayed Temu Partner EU tax APIs for export reports, Galerie signatures, invoice queries and downloads, merchant report downloads, and invoice uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketplace operations teams use this skill to prepare LinkFox-authenticated Temu EU Tax API requests and interpret responses for VAT invoices, signed downloads, and monthly tax reports. <br>

### Deployment Geography for Use: <br>
Europe (Temu EU site) <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive LinkFox and Temu credentials. <br>
Mitigation: Use dedicated Temu EU tax tokens where possible, keep tokens out of shared prompts and logs, and provide LinkFox credentials through environment variables or secure runtime configuration. <br>
Risk: The artifact includes generic proxy, file-download, and local token-storage scripts broader than the EU tax description. <br>
Mitigation: Review the proxy and file-download scripts before enabling agent execution, restrict allowed API types to the documented EU tax operations, and avoid local token storage unless operationally necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-tax-eu) <br>
- [API reference](artifact/references/api.md) <br>
- [Temu access token authorization](artifact/references/access-token.md) <br>
- [Partner EU tax catalog](artifact/references/partner-eu-catalog.md) <br>
- [Tax API document index](artifact/references/apis/README.md) <br>
- [Temu Partner EU Tax documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require LinkFox and Temu access tokens; scripts can call proxy and file-download endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
