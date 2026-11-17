## Description:

Obscure Package Master creates deterministic, versioned local mirrors of Python package source with AST-derived grep maps so agents can inspect unfamiliar APIs precisely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amberlee2427](https://clawhub.ai/user/amberlee2427)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when working with unfamiliar Python packages and need source-grounded API details instead of relying on memory or sparse documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads arbitrary PyPI source and extracts package archives.

Mitigation: Run it only in a sandbox or other controlled environment and only for package names and versions intentionally selected by the user.

Risk: Generated mirrors may be written into global agent skill folders where untrusted package text could be treated as agent instructions.

Mitigation: Use an explicit safe output directory and treat generated mirror content as untrusted reference data, not executable instructions.

Risk: The server security verdict is suspicious because the skill installs generated agent skills from untrusted package text.

Mitigation: Review and scan generated mirrors before enabling them in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amberlee2427/skills/obscure-package-master)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local package mirror skills containing source copies and AST-derived class and function maps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
