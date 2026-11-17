## Description:

Converts local HTML into editable PPTX presentations by embedding local CSS and mapping common HTML elements and basic styles through pptxgenjs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiustrator](https://clawhub.ai/user/iiustrator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to convert trusted local HTML decks or documents into editable PowerPoint files while preserving common text, image, list, table, and basic style structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling may allow local command execution when conversion inputs or output paths are attacker controlled.

Mitigation: Convert only trusted local HTML and use filenames and output paths that you control until command execution is changed to avoid shell string execution.

Risk: CSS embedding may read unintended local files through uncontrolled stylesheet paths.

Mitigation: Run the skill only on approved local assets and restrict CSS reads to an expected asset directory before using untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iiustrator/skills/html2pptx-complete)
- [Publisher profile](https://clawhub.ai/user/iiustrator)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and PPTX file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs editable 16:9 PPTX files from trusted local HTML inputs; conversion quality depends on supported HTML and CSS features.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
