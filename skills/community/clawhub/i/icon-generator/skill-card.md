## Description:

Generates app icons, favicons, logos, and brand marks for iOS, Android, and web projects, with multi-size PNG export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external users can use this skill to generate local icon or logo assets and export common app and web icon sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on Pillow for local image generation.

Mitigation: Install dependencies in a virtual environment and pin Pillow before automated or production use.

Risk: The skill creates PNG files in the chosen output directory.

Mitigation: Review the output path before execution and run the skill in a workspace where generated files are expected.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python code and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates PNG icon files locally in the selected output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
