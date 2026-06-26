## Description: <br>
Temu Compliance Global helps agents work with Temu Partner Global product-compliance APIs through LinkFox gateway scripts and reference docs for compliance metadata, product qualifications, certification uploads, image recognition, and related file operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, commerce operators, and developers can use this skill to prepare and call Temu Global product-compliance workflows, including querying required certifications, uploading product qualification documents, editing compliance attributes, and inspecting compliance labels. It is most useful when an agent needs concise command guidance and request payload structure for the bundled LinkFox Temu scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LinkFox API keys and Temu access tokens, which are sensitive production credentials. <br>
Mitigation: Use a secure secret manager or protected environment variables, avoid pasting tokens into chats or logs, rotate tokens when exposed, and grant only the Temu permissions needed for the compliance workflow. <br>
Risk: The bundled token store can save Temu access tokens in a local plaintext JSON file. <br>
Mitigation: Prefer secret-manager backed workflows when possible; if the local store is used, place it on an encrypted disk or restricted path via TEMU_TOKEN_STORE_PATH and limit filesystem permissions to the current user. <br>
Risk: Generic proxy scripts can submit broad Temu API calls beyond a narrow compliance action. <br>
Mitigation: Prefer the named compliance scripts for routine use, review the requested Temu type and JSON payload before execution, and restrict proxy use to trusted operators who intentionally need broad API access. <br>
Risk: Server security evidence marks the release suspicious because broad proxy and credential utilities need review before use. <br>
Mitigation: Install only when the LinkFox publisher is trusted and the organization intentionally needs Temu Global compliance automation; review the scripts and security guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-compliance-global) <br>
- [API reference](references/api.md) <br>
- [Access token guide](references/access-token.md) <br>
- [Partner Global catalog](references/partner-global-catalog.md) <br>
- [Compliance API index](references/apis/README.md) <br>
- [Temu Partner Global API documentation](https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON request or response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include API request payloads and gateway responses when scripts are executed; calls require a LinkFox API key and a Temu access token or stored storeKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
