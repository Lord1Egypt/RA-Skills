## Description: <br>
Direct-OAuth Google Workspace operator skill. Sends/reads Gmail, manages Calendar events, creates and edits Google Docs/Sheets/Slides, browses Drive folders (including shared ones). Always call the matching tool fresh — never narrate; never assume an earlier result is still current. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-vaughan](https://clawhub.ai/user/jason-vaughan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and agents use this skill to manage a user's authorized Google Workspace account across Gmail, Calendar, Drive, Docs, Sheets, and Slides. It is intended for personal-account-style workflows that require fresh Google API calls and OAuth-backed access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth tokens and sensitive Google account credentials. <br>
Mitigation: Install only for accounts where agent access is intended, review OAuth scopes and token storage, and reauthorize only through the documented OAuth flow. <br>
Risk: The skill can send email, share Drive files, trash Drive files or Gmail messages, and delete calendar events. <br>
Mitigation: Review high-impact actions before execution and require explicit user intent before sharing files or performing destructive operations. <br>
Risk: Google Workspace data can change between turns, making stale results misleading. <br>
Mitigation: Use fresh tool calls for current mail, calendar, Drive, Docs, Sheets, and Slides state instead of reusing earlier results. <br>
Risk: Requests may expose private Workspace content to the agent workflow. <br>
Mitigation: Limit use to appropriate accounts and tasks, rely on Google ACLs, and avoid requesting or sharing content beyond the task scope. <br>


## Reference(s): <br>
- [ClawHub Google Workspace skill listing](https://clawhub.ai/jason-vaughan/google-workspace-operator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text responses with Google Workspace API tool results and links to created or modified resources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OAuth configuration plugins.entries.tangleclaw-google-oauth.enabled and access to the user's authorized Google account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
