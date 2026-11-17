## Description:

Minecraft Custom Mod Builder helps agents generate and verify structured Minecraft Bedrock add-ons, Bedrock skin packs, and Fabric or NeoForge projects through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to create installable or source Minecraft mod projects from structured specifications, then check runtime behavior, visual proof, and install readiness before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party hosted service may receive Minecraft specifications, images, and optional source archives.

Mitigation: Avoid confidential code, private assets, credentials, wallet secrets, and payment headers in prompts, archives, and logs; review AgentPMT setup and storage terms before use.

Risk: Some supported client and ESP-style features can be used for multiplayer cheating, griefing, or surveillance.

Mitigation: Use these capabilities only in authorized, test, single-player, or server-owner-approved contexts and decline requests intended for abuse.

Risk: The server security review flagged the release for review before installation, including mutable setup commands.

Mitigation: Prefer pinned installation commands or trusted OpenClaw installation paths, and review and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/minecraft-custom-mod-builder)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/minecraft-custom-mod-builder)
- [Minecraft Custom Mod Builder schema](artifact/schema.md)
- [AgentPMT account setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [AgentPMT no-account setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces remote build, preview, capability, and polling requests; installable artifacts should be delivered only after runtime and visual checks pass.]

## Skill Version(s):

1.0.8 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
