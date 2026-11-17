## Description:

Converts HTML presentations, especially frontend-slides output, into editable PowerPoint (.pptx) files while preserving slide structure, text, lists, images, and basic colors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to convert HTML slide decks into editable PPTX files for presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene and stale package metadata require caution before use.

Mitigation: Install and run the skill in a least-privileged project environment, preferably after pinning dependencies or using a reviewed lockfile.

Risk: The converter saves output to the path provided by the caller.

Mitigation: Review the output path before execution to avoid overwriting important files.

Risk: Sensitive or untrusted HTML is parsed locally.

Mitigation: Avoid processing sensitive or untrusted HTML unless the local parsing and dependency risks are acceptable.

Risk: Complex CSS animations, gradients, custom fonts, and absolute positioning may not survive conversion cleanly.

Mitigation: Review the generated PPTX manually and adjust formatting before sharing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/html2pptx)
- [Publisher profile](https://clawhub.ai/user/liberalchang)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local PPTX files from provided HTML input paths; conversion fidelity depends on supported slide structure and CSS.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
