## Description:

Turns standard PowerPoint decks into cleaner ultra-wide layouts without stretching text, while preserving editable content, reading order, and visual hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[standed](https://clawhub.ai/user/standed)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, presentation authors, and agents use this skill to analyze existing PPTX structure and produce an editable first-pass ultra-wide relayout that preserves text shape, grouped blocks, and reading order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted PPTX files may expose users to XML/ZIP parsing hardening gaps.

Mitigation: Use trusted decks or run the scripts in a sandbox until XML parser and ZIP size-limit hardening are added.

Risk: The relayout script writes a derived PPTX to the output path the user provides.

Mitigation: Choose a new output filename and keep a copy of the source deck before running the script.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/standed/skills/ppt-ultrawide-relayout)
- [Reference Style Notes](references/reference-style.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with bash commands, JSON layout analysis, and editable PPTX output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a derived editable PPTX file and can produce JSON or pretty-printed layout dumps when its bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
