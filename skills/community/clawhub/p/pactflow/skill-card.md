## Description: <br>
Expert assistant for PactFlow and Pact contract testing, covering PactFlow, Pact, consumer-driven contracts, provider verification, can-i-deploy, Pact Broker workflows, BDCT, publishing pacts, deployments, provider states, contract matrices, and CI/CD integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinrvaz](https://clawhub.ai/user/kevinrvaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to design, troubleshoot, and operate PactFlow or Pact Broker contract testing workflows. It helps with MCP setup, consumer and provider test authoring, deployment compatibility checks, BDCT, CI/CD integration, workspace administration, and failure diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or execute broad PactFlow or Pact Broker workspace administration, including delete, webhook, deployment, and secret-related actions. <br>
Mitigation: Install it only for agents that are expected to manage a PactFlow or Pact Broker workspace, require explicit human confirmation for destructive or sensitive actions, and review proposed changes before execution. <br>
Risk: The skill requires sensitive PactFlow or Pact Broker credentials for connected MCP workflows. <br>
Mitigation: Use least-privileged tokens, avoid storing real credentials in project files, and keep MCP configuration out of version control. <br>


## Reference(s): <br>
- [SmartBear MCP Server Installation & Configuration](references/mcp-setup.md) <br>
- [End-to-End Contract Testing Workflow](references/workflow.md) <br>
- [PactFlow MCP Tools Reference](references/tools.md) <br>
- [Pact Core Concepts](references/pact-concepts.md) <br>
- [Pact Consumer Guide](references/pact-consumer.md) <br>
- [Pact Provider Guide](references/pact-provider.md) <br>
- [Message Pact Async & Event-Driven Testing](references/pact-messages.md) <br>
- [Bi-Directional Contract Testing](references/bdct.md) <br>
- [Pact Broker Setup, CLI & Troubleshooting](references/pact-broker-setup.md) <br>
- [Pact Broker Advanced Topics](references/pact-broker-advanced.md) <br>
- [Pact CI/CD Setup Guide](references/pact-cicd.md) <br>
- [Pact Documentation Index](references/pact-docs-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, command examples, configuration snippets, and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or invoke contract-testing_* MCP tool actions that affect PactFlow or Pact Broker workspaces when those tools are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
