## Description:

Convert Markdown text to HTML and other formats. Use for documentation generation, content formatting, and text transformation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to convert Markdown documents to HTML, generate a table of contents, and transform Markdown content from files or standard input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can preserve attacker-controlled scripts or dangerous links when processing untrusted Markdown.

Mitigation: Use the skill only with trusted Markdown, review generated HTML before opening it, and avoid opening output from untrusted documents in a privileged browser context.

Risk: The security verdict is suspicious because converter output remains unsafe until escaping, URL validation, and capability documentation are fixed.

Mitigation: Review before installing, scan the package before deployment, and address HTML escaping, URL validation, and capability documentation before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/markdown-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands]

**Output Format:** [Markdown guidance with command-line examples and generated HTML or plain text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read Markdown from a file, inline input, or standard input and can write converted output to a file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
