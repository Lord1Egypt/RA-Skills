## Description: <br>
A Markdown guide comparing agent commerce protocols including x402, ACP, AP2, MPP, TAP, UCP, MCP, and A2A, with feature matrices, benchmark discussion, migration paths, and multi-protocol gateway examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical decision makers use this guide to compare agent commerce protocol options and plan integrations, migrations, and protocol-agnostic gateway designs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes runnable commerce and payment API examples that may involve live payments, signing operations, wallet identifiers, OAuth tokens, or payment credentials. <br>
Mitigation: Use sandbox accounts, fake data, tightly scoped test keys, and review every endpoint and request before running any example. <br>
Risk: Supplying production Stripe keys, signing keys, OAuth tokens, wallet credentials, or merchant credentials could expose sensitive accounts or authorize unwanted transactions. <br>
Mitigation: Do not provide production credentials just to read the guide; keep secrets out of prompts and use isolated test credentials only when intentionally testing code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-protocol-wars-comparison) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint referenced by examples](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python, JSON, shell command, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide content; examples reference wallet, signing, OAuth, and payment credentials supplied by the user.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
