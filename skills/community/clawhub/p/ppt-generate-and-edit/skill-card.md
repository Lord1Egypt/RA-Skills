## Description:

Generate and edit PowerPoint files with python-pptx, including slide creation, text replacement, and image replacement while preserving layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zicheng354-tech](https://clawhub.ai/user/zicheng354-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to generate new .pptx presentations from structured slide content and update existing presentations by replacing text or images while preserving slide layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output filenames and paths can be influenced by input, which may allow PowerPoint files to be written outside the intended output folder.

Mitigation: Sanitize output filenames, constrain writes to approved directories, and reject traversal or absolute paths before saving files.

Risk: Generated filenames are timestamp-based and may collide during concurrent or repeated runs.

Mitigation: Use collision-resistant filenames or enforce non-overwrite checks for generated presentations and images.

Risk: The dependency list does not pin python-pptx to a reviewed version.

Mitigation: Pin dependencies before use in shared or sensitive environments.

## Reference(s):

- [README](artifact/README.md)
- [Skill Page](https://clawhub.ai/zicheng354-tech/skills/ppt-generate-and-edit)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [PowerPoint files with JSON-style file paths and replacement logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local .pptx files and returns generated paths; image generation uses a mock backend by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
