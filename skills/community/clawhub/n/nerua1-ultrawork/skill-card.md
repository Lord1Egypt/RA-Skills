## Description:

Parallel execution engine - run multiple tasks simultaneously for speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Ultrawork to delegate multiple independent OpenClaw tasks to parallel subagents, collect their results, and reduce total execution time when the tasks do not depend on one another.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work to multiple agents or models that may modify repository files in parallel.

Mitigation: Use it only in trusted repositories, review the resulting changes before accepting them, and reserve it for independent tasks that do not depend on each other's outputs.

Risk: The advertised verification can run repository-controlled npm build and test scripts.

Mitigation: Review package scripts first or run the skill in a contained environment before allowing automatic build or test verification.

Risk: The release security verdict is suspicious.

Mitigation: Review the skill before installation and treat its cancellation and verification behavior as requiring human oversight.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerua1/skills/nerua1-ultrawork)
- [Publisher profile](https://clawhub.ai/user/nerua1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash command examples and summarized task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include task status summaries, selected model tiers, build and test status, and combined results from parallel subagents.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
