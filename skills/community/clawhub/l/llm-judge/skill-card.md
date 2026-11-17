## Description:

Compares two or more code implementations against a spec or requirements document using structured fact gathering, scoring, ranking, and a final verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare competing repository implementations against a shared specification, such as alternative PRs, vendor submissions, or multiple generated solutions. It gathers structured facts, scores functionality, security, tests, overengineering, and dead code, then produces a ranked verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can run test commands from third-party, vendor, or PR repositories.

Mitigation: Run repository tests only in disposable containers or otherwise hardened environments with no secrets, restricted networking, resource limits, and scratch-only write access.

Risk: The skill writes an evaluation report under .beagle in the current workspace.

Mitigation: Run it from the intended workspace and review generated .beagle/llm-judge-report.json before sharing or retaining it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/llm-judge)
- [Fact Schema](references/fact-schema.md)
- [Repo Agent Instructions](references/repo-agent.md)
- [Judge Agent Instructions](references/judge-agents.md)
- [Scoring Rubrics](references/scoring-rubrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summary plus .beagle/llm-judge-report.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report contains repository labels and paths, per-dimension scores, weighted totals, ranking, and verdict.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
