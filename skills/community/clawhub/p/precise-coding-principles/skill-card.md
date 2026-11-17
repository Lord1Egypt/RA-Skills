## Description:

A coding-guidance skill based on Andrej Karpathy's four common LLM coding failure modes, helping agents keep non-trivial coding work precise, minimal, scoped, and validation-driven.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmww](https://clawhub.ai/user/nmww)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when writing, reviewing, refactoring, or debugging non-trivial code so the work starts from explicit assumptions, avoids over-engineering, limits unrelated edits, and defines concrete verification criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guidance is mostly Chinese, which may reduce clarity for reviewers or agents configured for another working language.

Mitigation: Review the skill text before deployment and keep user language preferences authoritative during use.

Risk: Coding-guidance skills can make agents over-apply process to simple one-line changes.

Mitigation: Apply the full workflow only to non-trivial coding, review, refactoring, or debugging tasks as stated in the artifact.

## Reference(s):

- [Karpathy Principles Reference](references/karpathy-principles.md)
- [ClawHub Skill Page](https://clawhub.ai/nmww/skills/precise-coding-principles)
- [Andrej Karpathy Skills Reference](https://github.com/forrestchang/andrej-karpathy-skills)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance and concise natural-language recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No commands, persistence, credential use, or hidden data handling are described by the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
