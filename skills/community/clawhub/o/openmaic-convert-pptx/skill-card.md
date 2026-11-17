## Description:

Converts OpenMAIC course JSON into PPTX presentations, with optional speaker notes and basic slide styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taizhouchen](https://clawhub.ai/user/taizhouchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenMAIC users use this skill to export existing OpenMAIC course content as shareable PPTX files, optionally including speaker notes for presentation delivery or offline review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The exporter loads dependencies from the selected OpenMAIC installation path.

Mitigation: Use only a trusted and verified OpenMAIC installation path, and avoid --openmaic-path values that point to untrusted directories.

Risk: The test script can install npm dependencies inside an external OpenMAIC project.

Mitigation: Do not run the automatic test dependency installation in a real OpenMAIC project unless dependency changes have been reviewed.

Risk: Speaker notes may include sensitive course content.

Mitigation: Use --no-notes before sharing exported PPTX files externally when notes should not be disclosed.

Risk: Wildcard PPTX cleanup guidance can remove unrelated presentation files.

Mitigation: Delete only the exact generated PPTX file instead of running wildcard cleanup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taizhouchen/skills/openmaic-convert-pptx)
- [Publisher profile](https://clawhub.ai/user/taizhouchen)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)
- [Usage examples](artifact/USAGE_EXAMPLE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated PPTX files may include speaker notes unless disabled with --no-notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
