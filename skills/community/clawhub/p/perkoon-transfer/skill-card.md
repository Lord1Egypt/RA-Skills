## Description:

Perkoon Transfer helps agents send and receive explicitly selected files between agents, humans, and pipelines using Perkoon CLI, MCP, A2A, or browser automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-vy](https://clawhub.ai/user/alex-vy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to transfer selected files from an agent to a human, another agent, or a processing pipeline. It provides guidance for Perkoon MCP tools, pinned CLI commands, A2A JSON-RPC calls, and browser automation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser automation path can execute remote code fetched from Perkoon.

Mitigation: Prefer the MCP or pinned CLI path; review browser automation scripts before running them.

Risk: Command-line passwords can expose sensitive transfer secrets.

Mitigation: Avoid command-line passwords for sensitive transfers and use safer secret handling where the host supports it.

Risk: Receiving files into an existing directory or from unknown session codes can mix or overwrite local files.

Mitigation: Receive into a fresh empty directory when possible and require confirmation for sensitive files or unfamiliar session codes.

Risk: The skill transfers user-selected files outside the local agent environment.

Mitigation: Confirm the exact file path before sending and avoid sensitive directories unless the user explicitly approves.

## Reference(s):

- [Perkoon homepage](https://perkoon.com)
- [Perkoon A2A agent card](https://perkoon.com/.well-known/agent.json)
- [Perkoon agent integration guide](https://perkoon.com/llms.txt)
- [Perkoon automation docs](https://perkoon.com/automate)
- [Perkoon CLI package](https://www.npmjs.com/package/perkoon)
- [Perkoon MCP package](https://www.npmjs.com/package/@perkoon/mcp)
- [ClawHub skill page](https://clawhub.ai/alex-vy/skills/perkoon-transfer)
- [ClawHub publisher profile](https://clawhub.ai/user/alex-vy)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls, code]

**Output Format:** [Markdown with bash, JSON, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pinned package versions, JSON event handling, transfer status checks, and confirmation guidance for file paths and session codes.]

## Skill Version(s):

2.1.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
