## Description:

Interact with the desktop GUI by taking screenshots, listing or raising windows, clicking with grid targeting, typing text, and pressing key combinations; all commands return JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zachrouan](https://clawhub.ai/user/zachrouan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and control desktop GUI applications through screenshots, window management, grid-targeted clicks, text entry, and keyboard shortcuts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad screen-viewing, click, and typing control over desktop applications.

Mitigation: Install only when GUI control is intended, keep sensitive windows closed, and require explicit confirmation before form submissions, account changes, purchases, password entry, messages, deletes, or system setting changes.

Risk: Grid-targeted clicks can miss when the target is not aligned with the selected cell crosshair.

Mitigation: Use the documented orient, zoom, click, and verify workflow, and re-orient after screen state changes.

## Reference(s):

- [Gui Tool Skill Page](https://clawhub.ai/zachrouan/skills/gui-tool)
- [zachrouan Publisher Profile](https://clawhub.ai/user/zachrouan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with inline shell commands; gui-tool commands return JSON and may write screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses grid-cell targeting instead of pixel coordinates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
