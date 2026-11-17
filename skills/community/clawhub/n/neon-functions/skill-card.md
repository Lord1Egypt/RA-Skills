## Description:

Helps developers build, deploy, and manage long-running Node.js HTTP functions on Neon branches, including APIs, streaming services, webhooks, MCP servers, and scheduled or storage-triggered jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build and operate long-running Node.js HTTP backends alongside Neon databases. It provides implementation guidance for APIs, agents, streaming connections, webhooks, MCP servers, and scheduled or storage-triggered work.

### Deployment Geography for Use:

AWS us-east-1, us-east-2, eu-central-1, and ap-southeast-1 regions

## Known Risks and Mitigations:

Risk: The security review flagged a potentially exposed data-count example and an unpinned setup command.

Mitigation: Consider the suspicious verdict before installing and review those flagged examples; verify the setup command's source and version before running it.

Risk: The scan fully inspected only 4 of 9 components, and some references had analysis limits, so it could not assess all content.

Mitigation: Review the remaining skill and reference content before relying on it, especially before running commands or applying deployment guidance.

## Reference(s):

- [Neon Functions overview](https://neon.com/docs/compute/functions/overview.md)
- [Neon Functions authentication](https://neon.com/docs/compute/functions/authentication.md)
- [Function Triggers reference](artifact/references/function-triggers.md)
- [Production hardening guidance](artifact/references/production-hardening.md)
- [MCP server guidance](artifact/references/mcp.md)
- [ClawHub release page](https://clawhub.ai/andrelandgraf/skills/neon-functions)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript and JavaScript examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.9 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
