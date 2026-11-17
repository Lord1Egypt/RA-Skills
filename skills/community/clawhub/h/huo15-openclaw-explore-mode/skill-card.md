## Description:

Deep exploration mode for systematically investigating a codebase, system, or topic in read-only mode before answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need a structured, read-only investigation of an unfamiliar codebase, system, bug, or implementation detail before forming an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to inspect code and git history during exploration.

Mitigation: Use it only in repositories that the installer is comfortable letting the agent read.

Risk: The skill may provide investigation findings or recommendations that affect engineering decisions.

Mitigation: Review cited files and line references before acting on the report.

Risk: Instructions and expected output are primarily in Chinese.

Mitigation: Ask the agent for another language when the report needs to be reviewed by non-Chinese readers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-explore-mode)
- [Skill homepage](https://github.com/zhaobod1/huo15-openclaw-enhance)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown exploration report with file paths, findings, direct answers, and optional recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language instructions and output are expected unless the user requests another language.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
