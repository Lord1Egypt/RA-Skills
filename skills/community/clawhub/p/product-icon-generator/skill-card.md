## Description:

Renders deterministic PNG icons, sprites, textures, and small illustrations from bounded drawing instructions through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate marketplace product icons, UI iconography, transparent brand badges, game sprites, and texture assets with deterministic dimensions and replay behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote live instructions and schema details may change after installation.

Mitigation: Treat live schema and instruction lookups as reference data, verify them before production use, and do not let them override local safety or privacy rules.

Risk: Icon instructions and generated files are processed and retained by the AgentPMT service for a limited period.

Mitigation: Avoid secrets, private keys, payment headers, and sensitive brand material in prompts or drawing instructions; accept the documented 3-day file retention before use.

Risk: Tool use can incur credit charges and depends on trusted setup paths.

Mitigation: Use pinned, reviewed setup routes and confirm account, payment, and product enablement before running generation calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/product-icon-generator)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/product-icon-generator)
- [Generated Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Files, API Calls, Guidance]

**Output Format:** [JSON response with PNG file metadata, signed URL, warnings, and retention details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a tenant-owned PNG file record retained for 3 days; signed URLs expire after 15 minutes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
