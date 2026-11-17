## Description:

Mindflow converts text, Markdown files, and TXT files into image-based mind maps with configurable output format and resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newtoolai](https://clawhub.ai/user/newtoolai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use Mindflow to turn notes, articles, scripts, Markdown, or TXT files into concise mind map Markdown and rendered image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML-to-image rendering step can execute active HTML while browser isolation is weakened.

Mitigation: Run the skill only in an isolated workspace or container with minimal filesystem access and preferably no network access.

Risk: Untrusted Markdown or HTML may produce unsafe or misleading rendered content.

Mitigation: Avoid untrusted inputs where possible and review generated intermediate HTML before rendering images.

Risk: Runtime dependencies are installed by package name in the artifact instructions.

Mitigation: Pin and review markmap and Puppeteer dependencies before use.

## Reference(s):

- [Mindflow ClawHub Skill Page](https://clawhub.ai/newtoolai/skills/mindflow)
- [newtoolai Publisher Profile](https://clawhub.ai/user/newtoolai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown instructions with generated mind map image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Markdown is constrained to 300 tokens and four hierarchy levels; image output defaults to PNG and may be rendered as PNG or JPEG.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
