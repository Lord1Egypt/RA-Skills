## Description:

Map a codebase, decompose requested work into a dependency graph, and run a test-sandwiched multi-agent software pipeline with isolated worktrees, per-wave regression checks, adversarial review, and an explicit quality rubric.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill for substantial builds, fixes, refactors, migrations, or greenfield packages that benefit from repository mapping, dependency-aware planning, isolated implementation attempts, staged regression checks, and reviewable branch handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow delegates broad repository and shell authority to agents.

Mitigation: Run it only against a backed-up, reviewed repository path in a sandboxed host with minimal credentials and network access.

Risk: The workflow can create local branches, tags, commits, worktrees, and a root MAP.md in the target repository.

Mitigation: Inspect the workflow before use, protect any existing root MAP.md, and review the integration branch and retained refs before merging.

Risk: Remote mutation is possible when push options are enabled.

Mitigation: Keep push and pushAgentBranches disabled unless the destination repository and refs are explicitly authorized.

Risk: Risky commands may be built from user- or model-controlled text.

Mitigation: Avoid repository paths containing shell metacharacters until command construction is hardened.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/grade-a-pipeline)
- [README](README.md)
- [Skill Instructions](SKILL.md)
- [Workflow Adapter](examples/grade-a-pipeline.workflow.js)
- [Security Notes](SECURITY.md)
- [Agent Orchestra](https://github.com/AntreasAntoniou/agent-orchestra)
- [Plus Ultra](https://github.com/AntreasAntoniou/plus-ultra)
- [Agent Collaboration Control](https://github.com/AntreasAntoniou/agent-collaboration-control)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell commands, JavaScript workflow output, and repository branches, commits, tags, and files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns integration branch details, wave tags, test history, battery results, grade, unresolved review findings, escalations, pushed refs, cleanup status, and cumulative diff fallback.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
