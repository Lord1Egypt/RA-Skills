## Description:

Dependency-free template engine with variable substitution, conditionals, loops, and multi-language support for iFlow skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sylvanxiao](https://clawhub.ai/user/sylvanxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building iFlow skills use this toolkit to render small templates and localize agent-facing content without adding external dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template-file loading can read files outside the intended template directory if callers pass unsafe template paths.

Mitigation: Use trusted, fixed template names or map external template IDs to known files before calling load_template or render_file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sylvanxiao/skills/iflow-template-toolkit)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Rendered template text and translated strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external runtime dependencies; file-based template rendering depends on caller-supplied paths.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
