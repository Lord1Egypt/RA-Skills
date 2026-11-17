## Description:

Check whether an eval suite can fail. Use when someone asks if their plugin or skill evals are any good, wants a mutation score for a `claude plugin eval` suite, suspects a grader always passes, or wants to know which parts of a skill their evals do not cover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Plugin and skill developers use Litmus to check whether their eval suites reject broken behavior, identify vacuous graders and cases that pass with the plugin removed, and find skill behavior that their evals do not cover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real mutation run invokes `claude plugin eval` once per mutant using the user's credentials and may incur costs.

Mitigation: Review the dry-run estimate first, set a `--max-cost-usd` ceiling, and run with `--yes` only when the run and estimate are accepted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/orensegal/skills/litmus-evals)
- [Project homepage](https://github.com/OrenSegal/litmus)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance, Markdown]

**Output Format:** [Markdown report with mutation findings, scores, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports killed, survived, and inconclusive mutants, flags vacuous graders and null-green cases, and suggests targeted grader changes.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
