## Description:

Generate CSS gradient code, preview gradient combinations, and build gradient palettes using bash and Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create, save, preview, and export CSS gradients for web interfaces, including linear, radial, conic, random, and palette-based gradients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Export and preview commands can overwrite existing files at the selected output path.

Mitigation: Choose output paths carefully, avoid sensitive locations, and review existing files before generating exports or previews.

Risk: Generated preview HTML may include untrusted gradient names or CSS values from local records.

Mitigation: Use only trusted gradient names and CSS values, and avoid opening or sharing generated preview HTML from untrusted records.

Risk: Gradient records are stored locally in ~/.gradient/data.jsonl and deletion removes records from that store.

Mitigation: Back up important gradient records before deletion or cleanup operations.

## Reference(s):

- [Gradient on ClawHub](https://clawhub.ai/xueyetianya/skills/gradient)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated CSS, JSON, CSS, SCSS, Tailwind configuration, or HTML preview files depending on the command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores gradient records locally in ~/.gradient/data.jsonl and can write export or preview files to user-selected paths.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
