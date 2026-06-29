## Description: <br>
Deterministically generates and previews Minecraft Bedrock add-ons, Bedrock skin packs, and Java Fabric or NeoForge mod artifacts from structured specifications through AgentPMT-hosted tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, server owners, players, and developers use this skill to validate structured Minecraft content specifications, generate installable or source mod artifacts, and preview textures before installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AgentPMT-hosted remote actions and paid credits. <br>
Mitigation: Confirm the user is comfortable with AgentPMT-hosted services and spending credits before invoking paid generation or preview actions. <br>
Risk: Inputs can include uploaded images or artwork for textures and skin packs. <br>
Mitigation: Avoid uploading sensitive files or third-party artwork unless the user has the rights to use that content. <br>
Risk: Generated Minecraft artifacts may be installed into a user's game environment. <br>
Mitigation: Inspect generated .jar, .mcaddon, .mcpack, or source artifacts and review validation reports before installation. <br>


## Reference(s): <br>
- [Minecraft Custom Mod Builder schema](artifact/schema.md) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/minecraft-custom-mod-builder) <br>
- [Related File Management skill](https://clawhub.ai/agentpmt/file-management) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON parameter examples and remote artifact references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote actions can return .mcaddon, .mcpack, .jar, source zip, validation reports, preview PNG file IDs, signed URLs, warnings, and build reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
