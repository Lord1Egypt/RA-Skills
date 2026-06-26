## Description: <br>
Manages Amazon seller OAuth authorization, authorized store listing, token refresh, and access-token retrieval for downstream Amazon seller workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, operators, and developers use this skill to authorize Amazon Seller accounts, list linked stores, refresh credentials, and retrieve token data needed by downstream Amazon seller workflows. <br>

### Deployment Geography for Use: <br>
Global, with marketplace region handling for NA, EU, and FE. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Amazon seller authorization data, including access tokens, refresh tokens, seller IDs, authorization URLs, and the LinkFox API key. <br>
Mitigation: Install only when LinkFox is trusted for seller authorization data, keep credentials out of logs and screenshots, and show only masked token values to users. <br>
Risk: Generated authorization links and token-retrieval workflows can expose store access if shared with the wrong person. <br>
Mitigation: Ask for a clear sellerName before creating an authorization URL, confirm the selected store when multiple stores exist, and share authorization links only through trusted user channels. <br>
Risk: Automatic feedback reporting may send operational context outside the main authorization workflow. <br>
Mitigation: Review whether feedback reporting is acceptable in the deployment environment before enabling or relying on this skill. <br>


## Reference(s): <br>
- [Amazon Store Authorization API Reference](artifact/references/api.md) <br>
- [Amazon Store Authorization Flow](artifact/references/authorization-flow.md) <br>
- [Amazon Store Authorization Quick Start](artifact/references/quick-start.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-amazon-store-auth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON API examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return authorization URLs, store lists, refreshed-token status, or masked token details depending on the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
