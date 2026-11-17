## Description:

Imports local or repository Agent Skills into a Skilder workspace so a team can discover and run them from one governed endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skilder](https://clawhub.ai/user/skilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace admins use this skill to inventory local Agent Skills, confirm which ones to import, and publish approved skill instructions and companion files into a Skilder workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved imports could accidentally include private procedures, credentials, customer data, or internal scripts.

Mitigation: Review the inventory before import, scan candidate files for secrets, and skip any sensitive files instead of uploading them.

Risk: Existing workspace skills could be duplicated or overwritten by unclear import choices.

Mitigation: List existing workspace skills, flag duplicate names, and ask whether to skip or import under a suffixed name before proceeding.

## Reference(s):

- [Skilder Skills Repository](https://github.com/skilder-ai/skills)
- [Skilder MCP Endpoint](https://app.skilder.ai/mcp)
- [Skilder App](https://app.skilder.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, inventories, confirmations, and status reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create remote skill records and attach approved text or script companion files after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
