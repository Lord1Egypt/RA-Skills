## Description:

OpenClaw Kilo Agent coordinates the Kilo CLI for heavy coding tasks, browser automation, session management, and MCP-assisted workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sabyaghosh](https://clawhub.ai/user/sabyaghosh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate complex codebase work, browser automation, and session-managed execution to Kilo from OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-approval can allow Kilo to perform file writes, authenticated browsing, form submission, deletion, publishing, or external-account actions without a separate checkpoint.

Mitigation: Use an isolated workspace or low-privilege account and require separate confirmation before those actions.

Risk: The Puppeteer MCP dependency is invoked through an executable package command and may change if it is not pinned and reviewed.

Mitigation: Pin and review the MCP server package before use, especially for browser sessions that may expose accounts or secrets.

Risk: Browser automation can expose real sessions, credentials, or sensitive page content to the delegated agent workflow.

Mitigation: Avoid real browser sessions and secrets unless the environment is isolated and the task has been reviewed.

## Reference(s):

- [Kilo CLI Setup and Configuration](references/setup-guide.md)
- [Kilo CLI Workflow for OpenClaw](references/workflow.md)
- [ClawHub skill page](https://clawhub.ai/sabyaghosh/skills/openclaw-kilo-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kilo CLI commands, MCP configuration guidance, session-management steps, and task summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
