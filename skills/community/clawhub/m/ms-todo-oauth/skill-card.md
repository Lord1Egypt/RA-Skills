## Description: <br>
Manage Microsoft To Do lists and tasks through a local Python CLI backed by Microsoft Graph OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nathanatgit](https://clawhub.ai/user/nathanatgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage Microsoft To Do lists and tasks through a local CLI, including adding, completing, deleting, searching, exporting, and summarizing task data after OAuth login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Microsoft To Do read/write access and handles OAuth credentials. <br>
Mitigation: Install only if the user accepts that access; prefer caller-owned Azure app credentials and avoid pasting authorization codes or client secrets into shared chats or logs. <br>
Risk: The skill stores OAuth tokens locally in ~/.mstodo_token_cache.json. <br>
Mitigation: Protect the token cache file and delete it or run logout when access is no longer needed. <br>
Risk: Delete commands and -y flags can remove tasks or lists without further confirmation. <br>
Mitigation: Confirm the exact task or list before destructive commands and avoid -y unless the target has already been verified. <br>
Risk: Exported JSON files can contain sensitive task data. <br>
Mitigation: Review exported files as sensitive data and store or delete them according to the user's data-handling expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nathanatgit/ms-todo-oauth) <br>
- [Publisher profile](https://clawhub.ai/user/nathanatgit) <br>
- [Skill documentation](SKILL.md) <br>
- [Quick reference](scripts/QUICK_REFERENCE.txt) <br>
- [Test README](scripts/TEST_README.txt) <br>
- [Microsoft Graph API](https://graph.microsoft.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI returns terminal text and optional JSON exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies, network access to Microsoft Graph, and an interactive OAuth authorization-code login before task operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
