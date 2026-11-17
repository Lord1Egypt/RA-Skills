## Description:

Render compact generic data tables to PNG images with json-render-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sorphwer](https://clawhub.ai/user/sorphwer)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to turn arbitrary structured rows and columns into compact table screenshots for non-ticket reporting and visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may install unpinned global npm and Playwright tooling, creating persistent host changes.

Mitigation: Use the skill in a controlled environment, preinstall reviewed pinned tooling when possible, and require explicit approval before running global install commands.

Risk: Table screenshots can be clipped or oversized if viewport dimensions do not match the rendered content.

Mitigation: Tune viewport width and height for the dataset and enable full-page screenshots when row count or wrapping is variable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sorphwer/skills/json-render-table)
- [compact-table-template.md](references/compact-table-template.md)
- [compact-table-spec.template.json](references/compact-table-spec.template.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands, JSON render configuration, and PNG output paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The rendered artifact is normally a PNG file; Base64 output is used only when explicitly requested.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
