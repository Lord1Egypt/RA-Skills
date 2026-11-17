## Description:

Use this skill to read and manage Carbone templates through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Carbone users can list templates, categories, and tags, update template metadata, or delete templates through their connected account. The skill requires checking each action's schema and approval for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may make broader changes to the agent environment, and the remote installers were unavailable for review.

Mitigation: Review setup before enabling the skill, prefer a reviewed CLI release, and decide whether to disable automatic skill synchronization before first use.

Risk: Connecting Carbone entrusts OOMOL with the connected account's credentials and requested operations.

Mitigation: Connect only an account you intend to use through OOMOL, inspect each action schema, and approve account changes before execution.

## Reference(s):

- [Carbone homepage](https://carbone.io)
- [Carbone API documentation](https://carbone.io/documentation/developer/http-api/introduction.html)
- [oo CLI project referenced by the skill (not release provenance)](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-carbone)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the connected Carbone account and requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
