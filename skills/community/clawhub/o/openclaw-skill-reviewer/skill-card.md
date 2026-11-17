## Description:

Audits OpenClaw skills for package validity, content quality, functional correctness, and adherence to skill design best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to review OpenClaw skill packages before release, checking package validity, SKILL.md quality, functional alignment with OpenClaw specifications, and best-practice adherence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example validator path is hardcoded to one user's filesystem and may not exist or may point to the wrong tool in another environment.

Mitigation: Confirm or replace validator paths before running commands, especially when reviewing skills from untrusted sources.

## Reference(s):

- [OpenClaw Specifications](references/openclaw-specs.md)
- [Skill Design Best Practices](references/best-practices.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and checklist-style review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validator command examples for local skill review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
