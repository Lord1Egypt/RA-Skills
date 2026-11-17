## Description: <br>
Google Workspace Toolkit Free lets an agent use Gmail, Calendar, and Drive core tools through an OAuth-based command-line workflow without manual Google Cloud Console setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Google account and perform lightweight personal productivity tasks across Gmail, Calendar, and Drive. It is suited to command-line and agent-assisted workflows that need email search and drafts, calendar lookup and event creation, and Drive search or download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may authorize an external command-line tool to read and modify Gmail, Calendar, and Drive data. <br>
Mitigation: Use it only with accounts and data appropriate for agent access, review requested OAuth scopes, and prefer limited scopes when offered. <br>
Risk: Reusable OAuth credentials are stored locally and can persist beyond a single task. <br>
Mitigation: Run it on a trusted single-user machine and clear or revoke credentials after use when continued access is not needed. <br>
Risk: The workflow installs and runs an external package through npm or npx, and the security evidence notes the runtime is not clearly pinned. <br>
Mitigation: Verify the package source and version before installation and avoid running it in sensitive environments without review. <br>
Risk: Drive download behavior can write files to local paths. <br>
Mitigation: Review destination paths and downloaded content before opening or reusing files. <br>


## Reference(s): <br>
- [Google Workspace Toolkit Free ClawHub page](https://clawhub.ai/thcjp/skills/google-workspace-toolkit-free) <br>
- [thcjp ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; agent responses may include text or structured Google Workspace tool results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an external command-line toolkit, OAuth authorization, and locally stored credentials to access Gmail, Calendar, and Drive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
