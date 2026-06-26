## Description: <br>
Jira issue management skill for OpenClaw using the jirac CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mulhamna](https://clawhub.ai/user/mulhamna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using Jira use this skill to guide an agent through authenticated jirac CLI workflows for listing, viewing, creating, updating, transitioning, commenting on, attaching files to, and summarizing Jira issues and sprints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated jirac commands can make real Jira changes, including destructive, bulk, archive, move, delete, attachment, and workflow-transition operations. <br>
Mitigation: Use a least-privilege Jira account when possible and require explicit confirmation before high-impact commands. <br>
Risk: Broad JQL scopes can affect many issues during bulk update, transition, comment, or archive workflows. <br>
Mitigation: Preview JQL scopes with read-only list commands and prefer explicit project scoping before running bulk operations. <br>
Risk: Jira credentials, local jirac configuration, and attachment file paths may expose sensitive information. <br>
Mitigation: Treat local Jira configuration and selected attachment files as sensitive, and confirm files are intended and safe to upload. <br>


## Reference(s): <br>
- [Install jirac](references/install.md) <br>
- [JQL recipes for jirac](references/jql.md) <br>
- [jira-commands project](https://github.com/mulhamna/jira-commands) <br>
- [Install jirac from GitHub Releases](https://github.com/mulhamna/jira-commands/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the jirac binary and an authenticated Jira profile before commands can be executed.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
