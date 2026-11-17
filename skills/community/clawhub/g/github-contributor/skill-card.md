## Description:

Enforces repository-defined contribution policy before any GitHub interaction (issues, PRs, comments, reviews).

This skill is ready for commercial/non-commercial use.

## Publisher:

[therealhesreallyhim](https://clawhub.ai/user/therealhesreallyhim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when preparing GitHub issues, pull requests, comments, discussions, or reviews for repositories they do not own, so the interaction follows repository policies, templates, duplicate-search expectations, and maintainer stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly block or delay legitimate GitHub actions when repository policies are missing, ambiguous, security-related, or when required checks cannot be run.

Mitigation: Review the identified stop condition and repository policy evidence before deciding whether to pause, gather more information, or proceed through a maintainer-approved path.

Risk: The skill overstates the authority of some contribution requirements, which can make its refusals stricter than the target repository or platform requires.

Mitigation: Treat the skill as a conservative guardrail and confirm strict refusal cases against the repository's published policy and the user's permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/therealhesreallyhim/skills/github-contributor)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown or plain text guidance for GitHub contribution workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refuse or defer outward GitHub actions when repository policies, templates, duplicate-search requirements, or required checks cannot be satisfied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
