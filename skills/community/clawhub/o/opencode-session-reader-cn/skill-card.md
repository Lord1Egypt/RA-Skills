## Description: <br>
Reads a local OpenCode SQLite database to query sessions, inspect messages, and review schema details across project directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufei-png](https://clawhub.ai/user/wufei-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local OpenCode sessions, messages, projects, and schema information with read-only SQLite queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local OpenCode database queries can expose private conversations, tokens, credentials, or other sensitive session data. <br>
Mitigation: Keep queries scoped to session, message, part, and project inspection; avoid account and control_account tables unless explicitly administering credentials, and do not paste raw dumps or secrets into shared chats or logs. <br>
Risk: Direct database modification can damage local OpenCode state. <br>
Mitigation: Use sqlite3 read-only mode for inspection and create a backup before any intentional administrative database work. <br>


## Reference(s): <br>
- [OpenCode SQLite Schema Reference](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/wufei-png/opencode-session-reader-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local database inspection guidance; generated queries and message dumps may contain private session data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
