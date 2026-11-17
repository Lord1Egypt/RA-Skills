## Description:

Build and deploy autonomous AI agents using the OpenServ SDK (@openserv-labs/sdk).

This skill is ready for commercial/non-commercial use.

## Publisher:

[issa-me-sush](https://clawhub.ai/user/issa-me-sush)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build TypeScript agents for the OpenServ platform, define runnable or runless capabilities, provision workflows, and run agents locally or in production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes storing wallet and API credentials in plaintext environment files.

Mitigation: Use a sandbox or dedicated project, keep .env out of version control, rotate credentials as needed, and review generated environment handling before deployment.

Risk: The examples include wallet funding and on-chain registration flows with financial implications.

Mitigation: Use a low-value dedicated wallet, avoid funding it until registration is required, and review each transaction before signing.

Risk: The file operation examples include upload and deletion patterns that can affect workspace files.

Mitigation: Add confirmations, path validation, and scope restrictions before enabling file upload or deletion capabilities in production agents.

Risk: The security verdict is suspicious because broad update, file, deletion, and secret-handling patterns need review.

Mitigation: Install only after reviewing the skill, pin package and skill versions where possible, and run it first in a sandbox.

## Reference(s):

- [OpenServ SDK Reference](artifact/reference.md)
- [OpenServ SDK Troubleshooting](artifact/troubleshooting.md)
- [Basic Agent Example](artifact/examples/basic-agent.ts)
- [File Operations Example](artifact/examples/file-operations.ts)
- [ClawHub Skill Page](https://clawhub.ai/issa-me-sush/skills/openserv-agent-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and environment configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for agents that use OpenServ SDK and client packages.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
