## Description: <br>
Plan, audit, and safely execute Google Workspace admin, Gmail, Calendar, Drive, Groups, and user lifecycle work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and Google Workspace operators use this skill to plan and review Workspace migrations, account cleanups, permission audits, group rollouts, mailbox and calendar changes, and GAM, gcloud, or Google API command plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated GAM, gcloud, or Google API commands could affect users, groups, mail, calendars, Drive ownership, or sharing if run without review. <br>
Mitigation: Review all generated commands before execution, require explicit approval for writes, and keep destructive or sharing-change operations behind rollback planning. <br>
Risk: Over-broad OAuth scopes or domain-wide delegation could grant more access than the task requires. <br>
Mitigation: Use the narrowest OAuth scopes possible, prefer read-only scopes during discovery, and confirm service account, client ID, subject user, endpoint, and audit log expectations before writes. <br>
Risk: Bulk changes can be difficult to unwind without captured pre-change state. <br>
Mitigation: Export affected users, groups, permissions, settings, or ownership state and define a rollback plan before approving bulk changes. <br>


## Reference(s): <br>
- [Google Workspace skill page](https://clawhub.ai/patrick-erichsen-2/google-workspace) <br>
- [OAuth scope reference](artifact/references/scopes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown plans with shell command and API call snippets; optional JSON-to-Markdown rollout checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes read-only discovery, placeholders for tenant-specific values, approval gates before writes, rollback exports, and narrow OAuth scopes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
