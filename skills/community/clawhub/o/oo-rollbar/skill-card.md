## Description:

Search and read Rollbar data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Rollbar projects, items, occurrences, environments, and deploys through a connected Rollbar account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code, and the bundled installers and hosted connector have not been verified.

Mitigation: Review setup before enabling the skill, install a verified CLI release yourself, prevent automatic execution of fallback installers, and review the CLI's automatic agent-skill installation. Connect only the Rollbar account and permissions you intend OOMOL to use.

## Reference(s):

- [Rollbar API reference](https://docs.rollbar.com/reference)
- [Rollbar](https://rollbar.com)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-rollbar)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text summaries and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific Rollbar data; results vary by action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
