## Description:

Generate beautiful, professional GitHub README files for your projects with multiple templates, languages, and customization options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to generate starter GitHub README content for projects, with selectable templates, language options, badges, and common documentation sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can overwrite an existing README.md in the current working tree.

Mitigation: Run only in a disposable or backed-up working tree and review the output path behavior before execution.

Risk: The security evidence reports unsafe input handling that could run commands from crafted input.

Mitigation: Avoid untrusted project names, descriptions, or repositories until the sed-based placeholder replacement is fixed.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown README content written to README.md, plus shell status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled shell script writes README.md in the current working tree.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
