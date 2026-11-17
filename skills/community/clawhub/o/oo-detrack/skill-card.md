## Description:

Detrack (detrack.com). Use this skill for ANY Detrack request — reading, creating, updating, and deleting data. Whenever a task involves Detrack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read and manage delivery and collection jobs, search Detrack records, and list available depots through their connected Detrack account. It guides the agent to inspect each action's schema and obtain approval before creating, updating, or deleting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified software or introduce broader agent changes through automatic skill synchronization.

Mitigation: Review the CLI release and check or disable automatic agent-skill synchronization before first use, using the publisher's documented control.

Risk: Detrack data may be processed by OOMOL, and job creation, updates, or deletion can change account data.

Mitigation: Confirm OOMOL may process the data and retain user approval for each write or deletion, including its exact target and effect.

## Reference(s):

- [Detrack homepage](https://www.detrack.com)
- [Detrack API V2 documentation](https://detrackapiv2.docs.apiary.io/)
- [oo CLI command reference and synchronization controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON inputs; JSON action responses and user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas determine request fields; create, update, and delete actions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
