## Description: <br>
A Microsoft 365 assistant for high-priority mail triage, calendar coordination, stale OneDrive file review, and Teams alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cenralsolution](https://clawhub.ai/user/Cenralsolution) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and administrators use this skill to run delegated Microsoft 365 assistant tasks for Outlook, calendar availability, OneDrive file review, and Teams channel alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad delegated Microsoft 365 permissions can modify mail, calendar or file access, and send Teams messages. <br>
Mitigation: Use only with accounts and tenants where those delegated changes are acceptable, and prefer narrower read-only calendar and file scopes when possible. <br>
Risk: Mailbox or Teams changes may occur without explicit per-action confirmation controls. <br>
Mitigation: Review proposed commands before execution and add explicit confirmations before mailbox updates or Teams posts in production workflows. <br>
Risk: Token cache files can retain delegated access material after use. <br>
Mitigation: Store token caches with owner-only permissions and provide cleanup steps for token_cache.bin after the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Office Secretary Release](https://clawhub.ai/Cenralsolution/office-secretary) <br>
- [Microsoft Graph API](https://graph.microsoft.com/v1.0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Command-line text and JSON responses from Microsoft Graph operations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Microsoft Entra app registration, SECRETARY_CLIENT_ID, SECRETARY_TENANT_ID, and delegated Microsoft 365 permissions.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata; artifact frontmatter metadata.version is 3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
