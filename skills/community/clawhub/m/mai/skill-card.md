## Description: <br>
Mai is an AI shopping matchmaking skill for OpenClaw and Hermes that helps merchants publish products and manage stock while helping buyers discover, compare, discuss, review, and create trackable orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants and buyers use Mai to coordinate local-first or registry-backed shopping workflows, including catalog publishing, product discovery, buyer-seller messages, inventory-aware orders, and PSP custody record tracking. Operators can use it for private marketplace workflows or public pilots after applying the documented registry, payment, and deployment controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mai stores local marketplace data and can connect to a configured registry. <br>
Mitigation: Install it only for intended commerce workflows, review what catalog, order, and message data is pushed, and protect registry API keys. <br>
Risk: Registry writes can publish catalog data or create buyer messages, orders, and payment custody records. <br>
Mitigation: Use the documented confirmation controls for write actions and require HTTPS for remote registries; reserve localhost HTTP only for development. <br>
Risk: The bundled demo payment provider is not real money movement or escrow. <br>
Mitigation: Use a licensed payment service provider for live funds and do not claim payment success, release, refund, or escrow without PSP or external evidence. <br>


## Reference(s): <br>
- [Mai Data Schema](references/data-schema.md) <br>
- [Public Deployment Checklist](references/public-deployment.md) <br>
- [Mai Registry API](references/registry-api.md) <br>
- [Mai Transaction Model](references/transaction-model.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/mai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local JSON marketplace state, registry API keys, HTTPS registry URLs, and explicit confirmation flags.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence, SKILL.md frontmatter, package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
