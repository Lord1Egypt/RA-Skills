## Description:

Repair the OpenClaw Control UI Skills modal when clicking a skill row does nothing and DevTools shows a showModal InvalidStateError because the dialog is not yet in the document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danrudy33](https://clawhub.ai/user/danrudy33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose and manually patch an OpenClaw dashboard Skills modal timing bug when skill-row clicks fail to open the detail dialog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits a globally installed OpenClaw Control UI bundle, so applying it to the wrong file or build could break the dashboard UI.

Mitigation: Confirm the installed path and current skills-*.js asset filename before editing, and keep a backup or reinstall path available before applying the patch.

Risk: The patch targets a specific modal timing error and may not address unrelated Skills page failures.

Mitigation: Verify DevTools shows the documented showModal InvalidStateError before applying the hotfix, then hard reload and confirm the skill detail modal opens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danrudy33/skills/openclaw-dashboard-skill-modal-patch)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown instructions with shell and JavaScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual hotfix guidance for a local OpenClaw UI bundle; no hidden execution or data access is described by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
