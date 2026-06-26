## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thayyilshihab24](https://clawhub.ai/user/thayyilshihab24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run common Google Workspace tasks from an agent session, including Gmail search and sending, Calendar listing, Drive search, Contacts listing, Sheets operations, and Docs export or reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth setup can grant access to sensitive Google Workspace data and actions. <br>
Mitigation: Grant only the Google OAuth scopes needed for the intended task and review the gog Homebrew tap and upstream project before installation. <br>
Risk: Send, update, append, clear, export, and calendar commands can change or expose account data. <br>
Mitigation: Verify accounts, recipients, document IDs, sheet ranges, and command flags before execution; prefer JSON and no-input modes for scripted runs. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/thayyilshihab24/jkbro24) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may perform real Google Workspace account actions when executed by the user or agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
