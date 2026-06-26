## Description: <br>
Google Workspace CLI for Gmail, Calendar, Chat, Classroom, Drive, Docs, Slides, Sheets, Forms, Apps Script, Contacts, Tasks, People, Admin, Groups, and Keep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiroak](https://clawhub.ai/user/iiroak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to operate the gog CLI for Google Workspace workflows, including reading, creating, updating, and deleting resources across Gmail, Calendar, Drive, Docs, Sheets, Admin, and related services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions against Google Workspace data, including sends, deletes, sharing changes, and admin actions. <br>
Mitigation: Use least-privilege OAuth scopes or service accounts, prefer dry-run and command allowlists, and manually confirm sends, deletes, sharing changes, and admin actions. <br>
Risk: OAuth tokens, service-account keys, client secrets, and access tokens may be exposed if pasted into chat logs or command history. <br>
Mitigation: Keep credentials out of agent transcripts, use secret storage or keyring support, and rotate any credential that is exposed. <br>
Risk: CLI flags and subcommands may change across gog versions, which can produce failed or unintended commands. <br>
Mitigation: On command failure or uncertainty, verify syntax with gog help output or gog schema before execution. <br>


## Reference(s): <br>
- [GoG CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/iiroak/gog-complete) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/iiroak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gog CLI, OAuth or service account authentication, and command confirmation for sensitive actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
