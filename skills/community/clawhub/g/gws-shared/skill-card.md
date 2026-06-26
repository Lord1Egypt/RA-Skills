## Description: <br>
gws CLI: Shared patterns for authentication, global flags, and output formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and agents use this skill as a shared reference for authenticating with the gws Google Workspace CLI and composing commands with global flags, formatting options, pagination, uploads, downloads, and dry-run behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands may access or modify Google Workspace data when a trusted gws binary is configured with privileged credentials. <br>
Mitigation: Use the least-privileged Google account or service account needed, review exact commands before approval, and prefer dry-run behavior for destructive operations. <br>
Risk: Uploads, downloads, broad pagination, writes, or deletes can expose or alter sensitive workspace content. <br>
Mitigation: Confirm write/delete commands with the user, limit paginated reads where practical, and use sanitization for PII or content-safety screening when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-shared) <br>
- [gws CLI repository](https://github.com/googleworkspace/cli) <br>
- [gws CLI issues](https://github.com/googleworkspace/cli/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash command examples and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides command patterns and safety guidance; it does not execute commands itself.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact frontmatter metadata.version is 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
