## Description:

Helps detect hollow validation in AI agent skills by identifying fake tests that always pass without actually verifying behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, marketplace reviewers, and skill maintainers use this skill to inspect validation commands or test snippets for hollow checks that create a false impression of test coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static analysis may miss sophisticated test theater or validation code that appears substantive while checking trivial behavior.

Mitigation: Use the report as review guidance and confirm that flagged skills include real assertions tied to actual behavior.

Risk: The artifact declares a curl requirement that is not justified by the visible instructions.

Mitigation: Review the runtime requirements before use and remove or constrain network-capable dependencies when they are not needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown validation quality report with findings, evidence, ratings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports classify validation quality as SUBSTANTIVE, WEAK, or HOLLOW.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
