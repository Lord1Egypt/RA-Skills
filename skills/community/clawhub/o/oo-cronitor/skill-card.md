## Description:

Manage Cronitor monitors through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to inspect, create, update, and delete monitors in a connected Cronitor account. It guides users to check each action's input schema and seek confirmation before changes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified remote code and may add agent skills without clearly disclosing those effects.

Mitigation: Review setup first, use a separately approved and verified oo CLI release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if startup skill synchronization is unwanted.

Risk: Monitor changes and deletions can affect Cronitor account data.

Mitigation: Retain user approval for monitor changes and deletions, confirming the exact action and target before execution.

## Reference(s):

- [Cronitor API documentation](https://cronitor.io/docs/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Cronitor skill release](https://clawhub.ai/oomol/skills/oo-cronitor)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [CLI commands with JSON request payloads and response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes action-specific schemas and confirmation guidance for changes and deletions.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
