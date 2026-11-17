## Description:

A minimal example skill demonstrating .clawhubignore - the secret.md file should NOT appear in the published version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tshogx](https://clawhub.ai/user/tshogx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this minimal example to verify whether a .clawhubignore-style exclusion prevents private-looking files from being included in a published skill package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package includes secret.md even though the skill states that this file should not be present.

Mitigation: Remove secret.md, verify the ignore configuration, and rebuild from a clean package before distribution.

Risk: Private-looking configuration content may be exposed in published skill files.

Mitigation: Review package contents before installation or release and exclude any private paths, keys, or configuration values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tshogx/skills/hello-example)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill has no executable behavior and provides a short textual ignore-file test.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
