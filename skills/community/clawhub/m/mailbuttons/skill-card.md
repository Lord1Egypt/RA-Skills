## Description:

Scaffolds a sandboxed, policy-governed email inbox and integration for an AI agent, with human approval required before production promotion or external sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailbuttons](https://clawhub.ai/user/mailbuttons)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a sandbox email inbox, configure governed inbound and outbound email, and scaffold an integration for their agent framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an account-level API key to provision the inbox, so key handling needs review.

Mitigation: Have a person create the sandbox inbox and give the agent only its scoped sandbox token. Review the generated policy, verify the provider's external-send approval controls, and use a verified, pinned MCP server release.

## Reference(s):

- [Mailbuttons developer documentation](https://mailbuttons.com/developers)
- [Claude Agent SDK integration reference](references/claude-agent-sdk.md)
- [LangChain integration reference](references/langchain.md)
- [Plain TypeScript or Python integration reference](references/plain-sdk.md)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown guidance, code examples, and JSON policy configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Integration examples are sandbox-only and read the API key from MAILBUTTONS_API_KEY.]

## Skill Version(s):

0.1.4 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
