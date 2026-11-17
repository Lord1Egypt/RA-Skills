## Description:

Monitors adjacent systems, upstream dependencies, and downstream consumers for changes that could affect your current work before they break it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scan nearby dependencies, consumers, schemas, configuration, and recent repository changes before committing, opening a pull request, or investigating unexpected CI failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad visibility into related files, git history, schemas, and configuration around the current work.

Mitigation: Use it only in repositories where that level of agent inspection is acceptable, and limit workspace access when sensitive unrelated files are present.

Risk: Change-detection alerts may be incomplete or misleading if repository history, dependency data, schemas, or configuration files are unavailable.

Mitigation: Review the cited files and commands before acting on an alert, and confirm high-impact findings with normal tests or code review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/peripheral-vision)
- [Publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown alert summaries with concrete review actions and optional shell commands or configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Zero external dependencies and no API calls according to the artifact; repository visibility is required for meaningful analysis.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
