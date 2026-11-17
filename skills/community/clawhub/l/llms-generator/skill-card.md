## Description:

Generates a local llms.txt file with a project description, repository identity, and optional ecosystem links and inlined Markdown content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and project maintainers use this skill to create a local llms.txt file so AI agents can find project information and selected links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chosen output file may be overwritten.

Mitigation: Check the output path and preserve any existing file before running the generator.

Risk: Using --full may place private or sensitive source text into llms.txt.

Mitigation: Review the input file and generated llms.txt before publishing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/llms-generator)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [UTF-8 llms.txt file and brief terminal summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local file only; optionally includes the full contents of a supplied Markdown file.]

## Skill Version(s):

1.0.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
