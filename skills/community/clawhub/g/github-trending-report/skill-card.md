## Description:

Fetches GitHub repository and topic data with the github-discover CLI and helps generate structured trending reports about fast-growing repositories, newly popular projects, and hot topic tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderyi](https://clawhub.ai/user/coderyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical analysts use this skill to generate concise GitHub trending reports that compare growth velocity, newly popular repositories, and active technology topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned global npm package can change the tool behavior over time and may introduce package provenance risk in sensitive environments.

Mitigation: Use a pinned version or project-local installation of github-discover, and review the npm package provenance before running it where sensitive files or credentials are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderyi/skills/github-trending-report)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with inline shell commands and JSON-derived findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository links, star counts, growth estimates, language filters, topic summaries, and short trend analysis.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
