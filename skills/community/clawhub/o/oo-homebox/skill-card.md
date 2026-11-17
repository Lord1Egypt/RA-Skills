## Description:

Use an OOMOL-connected HomeBox account to inspect, manage, and maintain household inventory through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HomeBox users can search and inspect household inventory, review maintenance information, and create or update records through the oo CLI. The skill also provides delete actions, which require approval before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and add agent skills without clearly explaining those effects.

Mitigation: Use an independently reviewed, version-pinned CLI; disable automatic skill synchronization; retain approval for every HomeBox change or deletion.

## Reference(s):

- [HomeBox](https://homebox.software)
- [HomeBox API documentation](https://homebox.software/en/api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and delete actions require user approval.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
