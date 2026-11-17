## Description:

Creates HTML slide decks through a guided brief, validates them against the bundled HTML-to-PPTX specification, and converts them into PowerPoint files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqcmj74](https://clawhub.ai/user/cqcmj74)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to produce structured HTML slide decks and convert them to PPTX after validation, especially when they need repeatable deck generation with reusable themes, page templates, and conversion constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The converter can load remote content and local files referenced by slide HTML without tight safety boundaries.

Mitigation: Process only trusted slide HTML and assets; for third-party decks, run conversion in a sandbox or network-isolated environment and avoid absolute or file:// media paths.

Risk: Deck output may include externally sourced or unreviewed media.

Mitigation: Localize and review images and other media before conversion.

Risk: The skill relies on Node tooling and package installation for conversion and validation.

Mitigation: Use deterministic dependency installation from a trusted registry before running the bundled scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cqcmj74/skills/html-slides-to-pptx)
- [SKILL.md](artifact/SKILL.md)
- [HTML slide writing specification](artifact/reference/html-spec.md)
- [Design principles](artifact/reference/design-principles.md)
- [Interview guide](artifact/reference/interview-guide.md)
- [Density tiers](artifact/reference/density-tiers.md)
- [Converter package metadata](artifact/scripts/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files, HTML slides, JSON configuration, validation commands, and PPTX conversion commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; generated decks are expected to pass bundled validation before PPTX conversion.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
