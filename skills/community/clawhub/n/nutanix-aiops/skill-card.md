## Description:

Operates Nutanix Prism Central v4 environments for infrastructure inventory, diagnostics, VM and storage lifecycle, data protection, and upgrades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Infrastructure engineers and operators use this skill to inspect Nutanix Prism Central v4 estates, diagnose cluster health and alerts, and manage VM, storage, network, data protection, and lifecycle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the release suspicious because documented workflows could allow destructive infrastructure changes without fresh operator approval; scan coverage was partial.

Mitigation: For destructive MCP calls, show the dry-run preview and wait for explicit operator approval; use a least-privilege Prism Central account and confirm audit storage is healthy before real writes.

## Reference(s):

- [Capabilities reference](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup and security guide](references/setup-guide.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Project homepage](https://github.com/AIops-tools/Nutanix-AIops)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON, Shell commands, Text]

**Output Format:** [Structured tool results with concise text or Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested Prism Central operation.]

## Skill Version(s):

0.14.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
