## Description:

Generate publication-quality figures for Nature-series journals using Python (matplotlib) or R (ggplot2).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1bai](https://clawhub.ai/user/yang1bai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and scientific authors use this skill to create, polish, or redesign Nature-style multi-panel figures and accompanying figure legends from supplied data or plotting requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-figure command template can run unintended shell commands when given an untrusted or unusual file path.

Mitigation: Use only trusted, normalized input paths, verify the referenced helper script is present and trusted, and avoid interpolating user-controlled paths into shell commands.

Risk: Generated plotting code or commands may be executed with insufficient argument validation.

Mitigation: Prefer reviewing and running generated Python or R code with explicitly validated arguments before execution.

## Reference(s):

- [BioRender](https://biorender.com)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Markdown]

**Output Format:** [Markdown with Python, R, or shell code blocks plus figure legend text and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include runnable matplotlib or ggplot2 code, export instructions for PDF/PNG outputs, and a pre-submission figure verification checklist.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
