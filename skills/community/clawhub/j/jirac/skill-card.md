## Description:

Jira issue management skill for OpenClaw using the jirac CLI. Requires the `jirac` binary to be installed and authenticated before use. Use when listing, viewing, creating, updating, transitioning, commenting on, attaching files to, bulk-editing, cloning, deleting, linking, archiving, moving, changing types of Jira issues, logging work, generating standup or sprint summaries, managing sprint lifecycles, browsing fix versions, scanning Jira mention notifications, rendering markdown to ADF, registering jirac-mcp into MCP clients, or running raw Jira REST calls from agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mulhamna](https://clawhub.ai/user/mulhamna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Jira issues and sprints through the jirac command-line interface, including search, updates, reporting, and workflow operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk-change and archive commands can affect many Jira issues when a query is broad or incorrect.

Mitigation: Preview the matching issues and confirm the JQL is narrowly scoped before running bulk-change or archive recipes.

Risk: Jira credentials, local configuration, and attachment paths may contain sensitive information.

Mitigation: Keep credentials and local configuration private, and confirm selected files are intended and safe to upload before attaching them.

## Reference(s):

- [Installation guide](references/install.md)
- [JQL recipes](references/jql.md)
- [Project homepage](https://github.com/mulhamna/jira-commands)
- [GitHub Releases](https://github.com/mulhamna/jira-commands/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, Markdown, JSON]

**Output Format:** [Markdown with jirac commands, JQL examples, and JSON manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on the active Jira profile and may create or modify Jira data.]

## Skill Version(s):

0.1.10 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
