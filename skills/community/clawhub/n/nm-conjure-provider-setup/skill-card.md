## Description:

Reports which delegation CLIs are installed and authenticated, and installs missing ones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before delegating work to check which provider CLIs are installed and authenticated, diagnose availability issues, and install missing CLIs with confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions reference scripts missing from the inspected artifact, so the release evidence does not establish how setup and installation behave.

Mitigation: Wait to install until the referenced scripts are available for review, as recommended by the release security guidance.

## Reference(s):

- [Provider Setup release on ClawHub](https://clawhub.ai/athola/skills/nm-conjure-provider-setup)
- [Conjure project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Provider status table and concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
