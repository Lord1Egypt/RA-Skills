## Description:

Maps file structure and module organization of a codebase for architecture reviews, refactoring planning, or migration scope estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to map repository layout, identify module boundaries, and collect structural observations before architecture review, refactoring, or migration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger words may cause the skill to run during general codebase conversations and enumerate structure in sensitive repositories.

Mitigation: Confirm the intended analysis root and scope before relying on or sharing structural file enumeration.

Risk: Repository layout and file names may reveal sensitive project details in generated analysis notes.

Mitigation: Review the generated observations before sharing them outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-file-analysis)
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command snippets and structured observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes directory layout, file counts, module organization, and hotspot observations when available.]

## Skill Version(s):

1.9.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
