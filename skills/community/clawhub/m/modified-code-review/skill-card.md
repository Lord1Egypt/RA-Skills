## Description:

Reviews user-modified code changes, provides best-practice recommendations, analyzes the cost-effectiveness of proposed approaches, and outputs a code score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review diffs, pull requests, or specified code changes across correctness, readability, maintainability, performance, security, and test coverage. It produces prioritized recommendations, cost-effectiveness analysis, blockers, and a numeric code quality score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect code changes in the current repository when the review scope is not specified.

Mitigation: Provide a specific diff, pull request, or file list to constrain the review scope and limit unintended code exposure.

Risk: Review recommendations and scores can be incomplete or misleading if the provided diff lacks relevant surrounding context.

Mitigation: Review the findings against project requirements and include important adjacent files, tests, or architecture notes when requesting a review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhiming1999/skills/modified-code-review)
- [Project homepage](https://github.com/wangzhiming1999/oliver-skill)
- [Support issues](https://github.com/wangzhiming1999/oliver-skill/issues)

## Skill Output:

**Output Type(s):** [markdown, guidance, code]

**Output Format:** [Markdown review report with prioritized findings, cost-effectiveness notes, blockers, and a score]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise code examples when they support a recommendation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
