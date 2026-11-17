## Description:

Deploy a sales pipeline with 4 agents that automate lead prospecting, qualification, outreach, and CRM synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a four-agent Pilot sales pipeline for lead prospecting, qualification, outreach, and CRM synchronization. It provides role-specific setup commands, manifests, data flows, and handshake guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple unpinned automation skills.

Mitigation: Verify each dependency and publisher before running clawhub install.

Risk: User-provided deployment prefixes are used in shell commands and hostnames.

Mitigation: Use only a simple allowlisted prefix before executing generated commands.

Risk: The pipeline can handle lead, email, CRM, Slack, and webhook data.

Mitigation: Scope credentials to the minimum required permissions and confirm peer identities before handshakes.

Risk: The setup writes a persistent ~/.pilot setup manifest.

Mitigation: Review the manifest before use and remove it when the deployment is no longer needed.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-sales-pipeline-setup)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup commands, manifest templates, peer handshakes, and dependency requirements for pilotctl, clawhub, and a running daemon.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
