## Description:

Structured Jupyter notebook prototyping with pipeline integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML engineers use this skill to create standardized Jupyter notebook prototypes and check notebooks for required structure, configuration discipline, data-loading sections, and pipeline usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker script has an input-handling flaw that could run unintended local code if used on a maliciously named notebook file.

Mitigation: Review the skill before installing or running it; run the checker only on trusted notebook paths or fix the script to pass the filename as an argument through a quoted heredoc.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes notebook-structure checklist guidance and a local shell checker for Jupyter notebooks.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
