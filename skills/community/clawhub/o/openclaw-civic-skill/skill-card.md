## Description:

Connect to Civic MCP for 100+ integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[civictechuser](https://clawhub.ai/user/civictechuser)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent discover and call Civic MCP tools for connected services such as Gmail, PostgreSQL, MongoDB, and Box. It supports setup guidance, tool listing, schema lookup, OAuth continuation steps, and tool calls through mcporter or the bundled TypeScript runner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Civic token may let the agent access connected services such as email, databases, and storage.

Mitigation: Use a least-privilege Civic profile and confirm sensitive or mutating actions before allowing the agent to run Civic tools.

Risk: A misconfigured or untrusted CIVIC_URL could send the token to an unintended MCP endpoint.

Mitigation: Keep CIVIC_URL on the official HTTPS Civic endpoint and review the configured URL before use.

Risk: Tool arguments may contain sensitive data that appears in logs or command output.

Mitigation: Avoid passing secrets in tool arguments and review logs or command transcripts for sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/civictechuser/skills/openclaw-civic-skill)
- [Civic Documentation](https://docs.civic.com)
- [Civic Nexus](https://nexus.civic.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing setup and execution guidance may include command output from remote Civic MCP tools.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
