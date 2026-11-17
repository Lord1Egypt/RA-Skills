## Description:

Provides an MCP server for Infinite Campus Campus Parent to read student grades, attendance, assignments, messages, documents, and related account data, and to send messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Parents or guardians and their authorized agents use this skill to connect an MCP client to Infinite Campus Campus Parent for retrieving student academic, attendance, fee, food-service, document, and message information, and for sending messages through the portal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive student records, messages, and documents.

Mitigation: Use it only with authorized Campus Parent accounts, confirm before reading messages or downloading documents, and avoid exposing retrieved records beyond the intended user.

Risk: The setup recommends persistent school login credentials and unpinned npm execution.

Mitigation: Prefer a secret manager or runtime environment variables over project-level credential files, and pin reviewed package versions or commits before installation.

Risk: Security evidence marks the release suspicious because it combines sensitive education data access with credential handling.

Mitigation: Review the npm package and source repository before installing, and use the skill only if the publisher and package are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/infinitecampus-mcp)
- [npm package: infinitecampus-mcp](https://www.npmjs.com/package/infinitecampus-mcp)
- [Source repository: infinitecampus-mcp](https://github.com/chrischall/infinitecampus-mcp)
- [fetchproxy fallback extension](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP configuration and commands; installed tools can access sensitive student records, messages, and documents.]

## Skill Version(s):

2.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
