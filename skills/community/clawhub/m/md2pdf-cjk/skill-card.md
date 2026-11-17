## Description:

Markdown to PDF converter with CJK (Chinese/Japanese/Korean) support using WeasyPrint and Noto CJK fonts, with emoji replacement, custom CSS styling, code blocks, and tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shimonxin](https://clawhub.ai/user/shimonxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert Markdown into well-formatted PDF files when Chinese, Japanese, or Korean text, code blocks, tables, and emoji replacement need predictable rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted Markdown through generated HTML and WeasyPrint can expose unsafe HTML, CSS, or resource-loading behavior.

Mitigation: Review the skill before installing for untrusted Markdown; disable raw HTML, sanitize generated HTML and CSS, block file and network resource loading in WeasyPrint, and use explicit output paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with Python, HTML, CSS, and bash snippets; generated PDF files when applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeasyPrint and Noto CJK fonts; recommends absolute output paths under /tmp and checking that the generated PDF exists and is larger than 10KB.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
