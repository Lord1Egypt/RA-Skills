## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liang0591](https://clawhub.ai/user/liang0591) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and run gog commands for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. It is useful for command-line workflows that search, send, list, export, or update workspace data after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gog CLI may require broad Google OAuth access for Workspace services. <br>
Mitigation: Review the OAuth consent scopes, use the least-privileged account practical, and revoke the OAuth token when access is no longer needed. <br>
Risk: Commands can send email, create or modify calendar events, and update or clear Sheets data. <br>
Mitigation: Confirm mail sends, calendar changes, and Sheets update or clear operations before execution. <br>
Risk: Installation depends on a third-party Homebrew tap and the gog CLI binary. <br>
Mitigation: Install only if the Homebrew tap and gog CLI are trusted. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/liang0591/gog-1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON output flags for scripting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
