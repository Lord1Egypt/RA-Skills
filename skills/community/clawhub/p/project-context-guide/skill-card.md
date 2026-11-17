## Description:

Project Context Guide helps agents analyze codebase structure, dependency and impact relationships, Git history, ownership, and review context for complex software projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamoplum](https://clawhub.ai/user/teamoplum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to understand unfamiliar or legacy codebases, trace implementation decisions, estimate change impact, and identify likely maintainers during onboarding and code review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose source details, Git history, contributor metadata, raw diffs, or ownership information from private repositories.

Mitigation: Review reports before sharing, keep outputs inside approved workspaces, and avoid exporting raw Git history unless necessary.

Risk: The artifact claims automatic sensitive-information redaction, but server security evidence says that redaction is not implemented.

Mitigation: Do not rely on automatic redaction; manually inspect reports for secrets, private code, personal data, and sensitive repository history before distribution.

Risk: Potential collaboration integrations could access external systems such as Slack or similar tools.

Mitigation: Enable external integrations only with administrator approval, least-privilege tokens, and explicit data-handling rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamoplum/skills/project-context-guide)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown and structured JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include code structure, call chains, Git history, contributor metadata, ownership suggestions, and review guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
