## Description:

Apple Contacts helps agents search, view, create, update, delete, and organize macOS Contacts records and lists on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bdwelle](https://clawhub.ai/user/bdwelle)

### License/Terms of Use:


## Use Case:

Users and agents on macOS use this skill to look up contact details, create or modify contacts, and manage contact list membership when workflows need local Contacts data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive contact data after the agent host is granted macOS Contacts access.

Mitigation: Install only when Contacts access is appropriate, use narrowly scoped queries, and avoid sharing returned contact details beyond the intended workflow.

Risk: Create, update, delete, and list membership actions can persistently change real Contacts data, especially when a name match is ambiguous.

Mitigation: Manually confirm the exact contact before write actions, prefer stable contact IDs when available, and avoid acting on ambiguous name matches.

Risk: The bundled tests exercise write and delete behavior against the Contacts database.

Mitigation: Run tests only in a disposable or backed-up Contacts environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bdwelle/skills/mac-contacts)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [YAML for search, show, and list results, plus plain-text success and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Contacts permission; write actions can persistently modify the user's Contacts database.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
