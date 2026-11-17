## Description:

Guides agents through safe, behavior-preserving Go refactoring using gopls, Go rewrite tools, coverage-aware testing, and small human-reviewed PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan, execute, and review Go refactors such as renames, extractions, package moves, import-cycle breaks, and staged structural cleanups while preserving behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide repository edits, Go tool execution, git/gh workflow, and sub-agent worktree activity.

Mitigation: Grant it only in repositories where those actions are acceptable, keep human review gates in place, and review every generated diff before merge.

Risk: The install metadata uses Go packages pinned to @latest, which can introduce ordinary tooling supply-chain drift.

Mitigation: Pin Go tool versions in higher-assurance environments and update them through the same review process as other development dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-refactoring)
- [ClawHub publisher profile](https://clawhub.ai/user/samber)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [workflow.md](references/workflow.md)
- [catalog.md](references/catalog.md)
- [go-tooling.md](references/go-tooling.md)
- [safety-net.md](references/safety-net.md)
- [structural.md](references/structural.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, refactoring plans, review notes, and proposed file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce repository edits, staged PR plans, verification commands, and risk-ranked refactoring inventories for Go projects.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
