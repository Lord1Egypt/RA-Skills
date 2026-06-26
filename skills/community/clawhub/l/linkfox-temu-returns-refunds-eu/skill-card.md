## Description: <br>
Provides guidance and helper scripts for Temu EU returns, refunds, and aftersales APIs through the LinkFox gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to inspect and work with Temu EU returns, refunds, return labels, aftersales orders, carrier data, and related token setup. <br>

### Deployment Geography for Use: <br>
Europe <br>

## Known Risks and Mitigations: <br>
Risk: Temu seller tokens and aftersales or order data are sensitive and are routed through LinkFox. <br>
Mitigation: Install only when LinkFox is trusted for this data, use scoped tokens where possible, and avoid placing production tokens in chat or shell history. <br>
Risk: The generic proxy and file-download helpers can reach broad Temu API and download capabilities. <br>
Mitigation: Use the proxy only for the documented returns and refunds workflows and review API type, parameters, and downloaded files before acting on them. <br>
Risk: Saved Temu tokens are stored locally in a weak format. <br>
Mitigation: Treat the local token store as sensitive, restrict filesystem access, use non-production tokens when possible, and rotate tokens after exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-returns-refunds-eu) <br>
- [API reference](references/api.md) <br>
- [Partner EU catalog](references/partner-eu-catalog.md) <br>
- [Temu access token guide](references/access-token.md) <br>
- [Returns and Refunds API index](references/apis/README.md) <br>
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call LinkFox and Temu APIs when users provide valid credentials and request API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
