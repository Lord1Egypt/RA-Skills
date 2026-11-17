## Description:

Evaluate recorded agent replies against explicit required, forbidden and exact text expectations without calling a model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and agent evaluators use this skill to run repeatable checks on recorded agent replies for required, forbidden, and exact text. It helps track regression cases while keeping semantic quality and factual review separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text expectations can pass replies that are factually wrong or semantically inadequate.

Mitigation: Treat results as regression checks and review factual accuracy and semantic quality separately.

Risk: Recorded replies may contain information the user is not authorized to process or share.

Mitigation: Process only replies you are authorized to handle, and review local reports before sharing them.

## Reference(s):

- [Input contract](references/input.md)
- [中文用法](references/zh-CN.md)
- [MochiLab](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-agent-eval-kit)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON report file with per-case results, pass status, and check counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic text checks; does not score semantic quality or call a model.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
