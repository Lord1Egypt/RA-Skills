## Description:

Generates a PNG mind map from Markdown notes using free (auto), center, or horizontal layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawyer-shi](https://clawhub.ai/user/sawyer-shi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and external users use this skill to convert Markdown notes or outlines into PNG mind maps with automatic, radial, or left-to-right layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PNGs and saved copies of input Markdown are written under mind_map_output, which may retain sensitive note content.

Mitigation: Use non-sensitive input or direct output to an approved location, and review or delete generated Markdown copies after use.

Risk: First run may download and cache a CJK font from GitHub under ~/.cache/mind-map-skill.

Mitigation: For offline or privacy-sensitive environments, preinstall a suitable local CJK font or disable the download path before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sawyer-shi/skills/mind-map-skill)
- [Mind Map Skill Reference](artifact/reference.md)
- [Mind Map Skill Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Text]

**Output Format:** [PNG image file plus saved Markdown input path and a text status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under mind_map_output, date-grouped by default, with selected layout, tree depth, total node count, PNG path, and saved input Markdown path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
