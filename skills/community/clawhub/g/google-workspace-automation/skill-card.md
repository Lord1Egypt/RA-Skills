## Description:

Design Gmail, Drive, Sheets, and Calendar automations with scope-aware plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to plan repeatable Google Workspace automations for Gmail, Drive, Sheets, and Calendar, including required OAuth scopes, scheduling, retry behavior, and audit-ready outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plans may recommend OAuth scopes that are broader than the automation requires.

Mitigation: Review the generated scopes before implementation and prefer narrower read-only or file-specific Google scopes where possible.

Risk: CSV exports may contain untrusted action names or services that spreadsheet software could interpret unsafely.

Mitigation: Treat CSV output as untrusted when inputs are user-supplied and avoid opening it directly in spreadsheet software without spreadsheet-safety review.

## Reference(s):

- [Workspace Automation Guide](references/workspace-guide.md)
- [ClawHub skill page](https://clawhub.ai/0x-professor/skills/google-workspace-automation)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON, Markdown, or CSV planning artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes selected OAuth scopes, normalized actions, schedule, retry policy, dry-run status, and output artifact path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
