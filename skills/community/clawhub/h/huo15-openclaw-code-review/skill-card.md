## Description:

Reviews GitHub and cnb.cool pull requests across design, implementation, testing, security, and maintainability, then produces Markdown comments that a reviewer can paste into the PR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to review GitHub or cnb.cool pull requests, assess design, implementation, tests, security, and maintainability, and draft Markdown feedback for human submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process PR metadata and diffs from GitHub or cnb.cool, including private repository content if the user provides it.

Mitigation: Use it only with repository content the reviewer is authorized to share with the agent, and avoid including secrets or unrelated sensitive context.

Risk: Generated review comments can be incorrect, incomplete, or misleading if the PR context is missing or the analysis is wrong.

Mitigation: Have a human reviewer inspect and edit the generated Markdown before posting it to a PR.

Risk: The report template includes a branded attribution line that may not be appropriate for every repository or organization.

Mitigation: Review the final Markdown and remove or revise attribution before posting when repository policy requires it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review report with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PR summary, five-dimension ratings, inline comment suggestions, and an overall review recommendation; generated comments require human review before posting.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
