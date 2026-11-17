## Description:

Install, connect, operate, and troubleshoot the host-neutral JS Eyes browser and Skill Runtime from CLI, MCP, or the optional OpenClaw adapter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjszhang](https://clawhub.ai/user/imjszhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use JS Eyes to install, connect, operate, and troubleshoot local browser automation and JS Eyes Skill Runtime integrations across CLI, MCP, and OpenClaw hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local browser automation and JS Eyes runtime support can expose sensitive browser actions when broader authority is enabled.

Mitigation: Use the safe MCP profile where possible, keep raw eval disabled unless the task truly requires it, and require explicit operator intent before enabling sensitive actions.

Risk: Skill install and discovery paths include review-worthy unsafe remote install and broad network-fetch behavior.

Mitigation: Use the staged skills/plan-install plus CLI approval path, review install plans before approval, and avoid untrusted custom registries.

Risk: A local browser automation server can be exposed beyond the intended user if remote binding or anonymous access is enabled.

Mitigation: Keep the server on localhost with token authentication, leave anonymous access disabled, and avoid remote binding unless it is deliberately configured and secured.

Risk: Native Messaging auto-install and skill directory watchers add local integration surface in hardened environments.

Mitigation: Consider disabling Native Messaging auto-install and skill directory watchers where local change monitoring or browser token synchronization is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imjszhang/skills/js-eyes)
- [Project homepage from ClawDIS metadata](https://github.com/imjszhang/js-eyes)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact security documentation](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, diagnosis, and policy-aware operation guidance; it does not produce binary artifacts.]

## Skill Version(s):

2.10.0 (source: server release evidence; artifact frontmatter and package manifests report 2.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
