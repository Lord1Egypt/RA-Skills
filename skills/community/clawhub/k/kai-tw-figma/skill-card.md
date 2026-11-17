## Description:

Interact with the Figma REST API to read files, export layers/components as images, and retrieve comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kai-tw](https://clawhub.ai/user/kai-tw)

### License/Terms of Use:

MIT

## Use Case:

Developers and design-facing agents use this skill to inspect Figma files, enumerate projects and comments, and export selected layers or components for implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Figma token that may allow the agent to read files, comments, projects, and account metadata available to that token.

Mitigation: Use a least-privilege token, limit access to relevant Figma resources, and run the skill only in trusted agent sessions.

Risk: Layer exports can overwrite existing files in the current working directory when filenames match figma_export_<layer_id>.<format>.

Mitigation: Run exports from a clean directory and check for existing matching filenames before exporting.

## Reference(s):

- [Figma API Documentation](https://www.figma.com/developers/api)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/kai-tw/skills/kai-tw-figma)
- [Kai ClawHub Profile](https://clawhub.ai/user/kai-tw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance, shell commands, JSON API responses, and exported image or document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FIGMA_TOKEN. Exported files are written to the current working directory using figma_export_<layer_id>.<format> filenames.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
