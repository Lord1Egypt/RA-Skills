## Description: <br>
Provides guidance, scripts, and reference material for using LinkFox gateway calls to access Temu Partner US returns, refunds, and after-sales APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and ecommerce operators use this skill to query and process Temu US returns, refunds, after-sales orders, return labels, carriers, signatures, and related return logistics through LinkFox gateway scripts. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LinkFox and Temu seller access tokens and may expose returns, refunds, order, and after-sales data if tokens are mishandled. <br>
Mitigation: Use short-lived tokens from a secure secret manager where possible, avoid sharing tokens in chat or logs, and restrict access to operators who need Temu returns and refunds access. <br>
Risk: The artifact includes generic Temu proxy and file download helpers that can reach broader Temu functionality than the advertised US returns and refunds workflow. <br>
Mitigation: Limit routine use to the documented US returns and refunds scripts, and review any use of generic proxy or download helpers before execution. <br>
Risk: Temu access tokens can be saved in a local token store. <br>
Mitigation: Prefer secure external secret storage or set a protected TEMU_TOKEN_STORE_PATH with appropriate filesystem permissions when local storage is unavoidable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-temu-returns-refunds-us) <br>
- [API reference](references/api.md) <br>
- [Temu access token guide](references/access-token.md) <br>
- [Partner US returns and refunds catalog](references/partner-us-catalog.md) <br>
- [Interface documentation index](references/apis/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON API responses, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LinkFox and Temu seller credentials; scripts may read Temu tokens from a local token store.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
