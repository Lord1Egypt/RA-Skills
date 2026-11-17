## Description:

Detect disposable and temporary email addresses - validate emails and check domains against known throwaway services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to validate signup or lead email addresses, check whether domains are associated with disposable email services, and support anti-abuse workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unpinned remote npm bridge.

Mitigation: Prefer a pinned, reviewed mcp-remote version or another controlled deployment method before using the skill in a sensitive environment.

Risk: Email-checking workflows send submitted email addresses or domains to a third-party Pipeworx service.

Mitigation: Only submit addresses or domains you are allowed to share with Pipeworx's service, and assess privacy requirements before deployment.

## Reference(s):

- [Pipeworx disify homepage](https://pipeworx.io/packs/disify)
- [Pipeworx disify MCP gateway](https://gateway.pipeworx.io/disify/mcp)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-disify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool-call examples and configuration snippets.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
