## Description:

Scaffold LaTeX papers into modular structure. Use for organizing .tex files, generating figure code, and table highlighting. Trigger on LaTeX paper organization, figure management, or academic paper formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[instinct323](https://clawhub.ai/user/instinct323)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to organize LaTeX academic papers into modular source files, generate figure include snippets for assets, and add table highlighting conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asset generator behavior can place unsafe filenames directly into generated LaTeX source.

Mitigation: Use conservative asset filenames, inspect generated .tex files before compiling, and compile with shell escape disabled or in a sandbox.

Risk: Untrusted LaTeX projects or downloaded assets may introduce unsafe content into generated project files.

Mitigation: Review the project and generated snippets before use, especially when assets or source files come from untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/instinct323/skills/latex-scaffold)
- [IEEE conference template](https://ras.papercept.net/conferences/support/files/ieeeconf.zip)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with LaTeX and bash code blocks; helper script output may create .tex files under assets/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated asset .tex files are intended to be reviewed and customized before compilation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
