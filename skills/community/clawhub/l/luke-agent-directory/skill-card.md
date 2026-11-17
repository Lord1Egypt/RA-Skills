## Description:

The directory for AI agent services. Discover tools, platforms, and infrastructure built for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banalit](https://clawhub.ai/user/banalit)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this directory skill to discover AI-agent services, fetch advertised skill.md files, and identify service categories and endpoints for integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to fetch and follow mutable third-party skill.md files.

Mitigation: Treat fetched skill.md content as untrusted documentation, review it before acting, and require explicit approval before commands, file changes, credential use, account changes, payments, or data sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/banalit/skills/luke-agent-directory)
- [ctxly.com homepage](https://ctxly.com)
- [ctxly.com services endpoint](https://ctxly.com/services.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to fetch mutable third-party skill.md files; review fetched content before acting.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0 and artifact _meta.json reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
