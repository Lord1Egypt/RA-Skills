## Description:

Reviews C and C++ source files in a specified local directory for production readiness, code quality, and potential vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzy-creator](https://clawhub.ai/user/zhouzy-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local C/C++ projects for memory safety issues, resource management problems, concurrency risks, performance concerns, and modernization opportunities before deployment or merge decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read sensitive local source files or secrets if the target directory is too broad.

Mitigation: Point the skill at the smallest intended C/C++ source directory and exclude repositories or folders that contain secrets or unrelated private files.

Risk: Review output may include incorrect or incomplete code guidance for production changes.

Mitigation: Have maintainers verify findings and test any suggested code changes before merging or deploying them.

## Reference(s):

- [Source repository](https://github.com/zhouzy-creator/local_code_review)
- [ClawHub skill page](https://clawhub.ai/zhouzy-creator/skills/local-code-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with severity-ranked findings and code fix examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file counts, issue summaries, affected file references, final readiness guidance, and before/after code snippets for critical or important issues.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
