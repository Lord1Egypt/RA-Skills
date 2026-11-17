## Description:

OCC (Origin Controlled Computing) provides cryptographic proof of OpenClaw agent actions and helps users install, configure, and audit those proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeargento](https://clawhub.ai/user/mikeargento)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and configure the OpenClaw OCC plugin, verify audit trails, and understand proof status for agent tool activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run npm tools that are not pinned in the artifact.

Mitigation: Use pinned package versions and install only after confirming trust in the publisher.

Risk: The OpenClaw extension records metadata for every tool action.

Mitigation: Use stub mode or a self-hosted notary in sensitive environments.

Risk: Self-hosted notary deployment can require Cloudflare-related authority.

Mitigation: Avoid running npm or OpenClaw as root and use narrowly scoped Cloudflare credentials.

## Reference(s):

- [OCC for OpenClaw documentation](https://occprotocol.com/openclaw)
- [openclaw-occ npm package](https://www.npmjs.com/package/openclaw-occ)
- [openclaw-occ source](https://github.com/mikeargento/occ-core/tree/main/packages/occ-core/examples/openclaw-occ)
- [Notary proof payload source](https://github.com/mikeargento/occ-core/blob/main/packages/occ-core/examples/openclaw-occ/lib/notary.js)
- [Skill release page](https://clawhub.ai/mikeargento/skills/openclaw-occ)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include install commands, configuration snippets, audit commands, and interpretation guidance.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
