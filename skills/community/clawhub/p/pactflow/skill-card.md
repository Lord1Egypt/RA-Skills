## Description:

Expert assistant for PactFlow and Pact contract testing, including consumer-driven contracts, provider verification, can-i-deploy workflows, Pact Broker administration, BDCT, CI/CD integration, and Pact test generation or review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinrvaz](https://clawhub.ai/user/kevinrvaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to design, troubleshoot, and automate PactFlow or Pact Broker contract-testing workflows, including consumer and provider tests, deployment safety checks, and CI/CD integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users to configure persistent PactFlow or Pact Broker credentials.

Mitigation: Use least-privilege and preferably short-lived tokens, and keep credentials out of project files and shell profiles when possible.

Risk: The skill references powerful workspace operations such as deleting resources and creating or executing webhooks and secrets.

Mitigation: Require explicit confirmation before destructive or externally triggered operations, and review proposed tool calls before execution.

Risk: Setup guidance may involve MCP and CLI packages that affect local agent capabilities.

Mitigation: Pin MCP and CLI package versions, review install steps before running them, and avoid pipe-to-shell installers.

## Reference(s):

- [SmartBear MCP Server Installation and Configuration](references/mcp-setup.md)
- [Pact Core Concepts](references/pact-concepts.md)
- [End-to-End Contract Testing Workflow](references/workflow.md)
- [Pact CI/CD Setup Guide](references/pact-cicd.md)
- [Pact Consumer Guide](references/pact-consumer.md)
- [Pact Provider Guide](references/pact-provider.md)
- [Bi-Directional Contract Testing](references/bdct.md)
- [PactFlow MCP Tools Reference](references/tools.md)
- [Pact Broker Setup, CLI, and Troubleshooting](references/pact-broker-setup.md)
- [Pact Documentation Index](references/pact-docs-index.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose PactFlow or Pact Broker MCP tool calls and CLI commands for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
