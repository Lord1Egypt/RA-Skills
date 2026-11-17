## Description:

Secure M365 Assistant for Triage, Calendar coordination, and Governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cenralsolution](https://clawhub.ai/user/cenralsolution)

### License/Terms of Use:


## Use Case:

Employees and executive assistants can use this skill to triage high-priority Outlook mail, coordinate calendar availability, review stale OneDrive files, and post Teams alerts through delegated Microsoft 365 access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Microsoft Graph write permissions, including scopes that may exceed the minimum needed for some workflows.

Mitigation: Install first with a tenant test account and reduce Graph permissions to the narrowest scopes required for the intended workflows.

Risk: Delegated Microsoft 365 tokens are stored locally in token_cache.bin and can provide account access if exposed.

Mitigation: Treat token_cache.bin as sensitive account access material, keep local file permissions restricted, and revoke or rotate credentials if exposure is suspected.

Risk: Python dependencies are not pinned, which can make installs less reproducible and increase supply-chain review burden.

Mitigation: Pin and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cenralsolution/skills/office-secretary)
- [Microsoft Graph v1.0 endpoint](https://graph.microsoft.com/v1.0)
- [Microsoft identity platform tenant authority](https://login.microsoftonline.com/{tenant_id})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call Microsoft Graph and require delegated Microsoft 365 credentials.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
