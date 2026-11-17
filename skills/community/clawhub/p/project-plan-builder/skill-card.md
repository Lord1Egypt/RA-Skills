## Description:

Builds a US project plan with milestones, owners, dependencies and a risk register, and flags the labor and tax rules that vary by state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US operations managers, program managers, and small-to-mid-size project owners use the skill to draft milestone plans, critical paths, risk registers, assumptions, and state-specific labor, licensing, and tax checks.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The scoring script overwrites ranking.md in the selected output folder.

Mitigation: Use a dedicated output folder and review its contents before relying on the report.

Risk: The documented YAML brief and scoring script input format do not match, which can make results unreliable.

Mitigation: Resolve and test the input-format mismatch with representative data before relying on scores.

Risk: US labor, licensing, tax, and contract references may be incomplete or change over time.

Mitigation: Independently verify relevant rules with authoritative sources and qualified reviewers before acting on the plan.

Risk: The optional Windows application is unsigned and is outside this skill bundle's security assessment.

Mitigation: Avoid the optional app unless needed; if you choose to run it, verify its published SHA-256 and do not run it as administrator without a reason.

## Reference(s):

- [US project plan checks](references/project-plan-checks.md)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/project-plan-builder)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Structured project plan and milestone-ranking report in Markdown, with a YAML planning brief template.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft for owner review; preserve unconfirmed values as assumptions and do not send or publish the plan outside the workspace.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
