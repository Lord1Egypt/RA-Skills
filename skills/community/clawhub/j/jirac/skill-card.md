## Description:

Manage Jira issues and sprints through the jirac CLI, including search, updates, reporting, and bulk workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mulhamna](https://clawhub.ai/user/mulhamna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Jira users can use the skill to inspect and manage issues, run sprint workflows, and prepare summaries through an authenticated jirac CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk or destructive Jira operations may change many issues or workflow states.

Mitigation: Use the intended account and project, preview the matching issues, and confirm the operation before approving it; review --force examples carefully.

Risk: An attachment may contain content the user did not intend to upload.

Mitigation: Confirm the selected file and its contents before uploading.

Risk: Jira credentials and local configuration are sensitive.

Mitigation: Keep credentials and the local Jira configuration private, and use the intended authenticated profile.

## Reference(s):

- [Install guide](references/install.md)
- [JQL recipes](references/jql.md)
- [Project homepage (Clawdis metadata)](https://github.com/mulhamna/jira-commands)
- [GitHub Releases (Clawdis install metadata)](https://github.com/mulhamna/jira-commands/releases)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON configuration, API calls]

**Output Format:** [Text and Markdown guidance, shell commands, and JSON manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the jirac CLI and configured Jira authentication; jirac-mcp is optional.]

## Skill Version(s):

0.1.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
