## Description:

Ink helps agents build rich interactive terminal UIs with React components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build React-based terminal UIs, including CLI apps, dashboards, prompts, menus, spinners, progress bars, and tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated example code may add npm dependencies or enable raw keyboard input.

Mitigation: Review generated code and dependency changes before running terminal UI examples.

Risk: Ink applications only work in real terminal environments and may depend on terminal capabilities.

Mitigation: Test generated TUIs in the target terminal and account for raw stdin, viewport, color, and layout support.

## Reference(s):

- [Ink Component API Reference](references/components.md)
- [Ink Hook API Reference](references/hooks.md)
- [Ink Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/openlark/skills/ink-tui)
- [OpenLark publisher profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, TSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated examples target terminal-only Ink apps and should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
