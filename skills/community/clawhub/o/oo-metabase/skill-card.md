## Description:

Operate Metabase through an OOMOL-connected account to find, read, and manage analytics content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and data teams use this skill to search and retrieve Metabase cards, collections, dashboards, and databases, and to invoke other tools exposed by their connected Metabase instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan marked the skill suspicious and partial; the remote installer's contents and effects are unknown, and two local references could not be resolved.

Mitigation: Review and verify the installer and unresolved references before installing; avoid running the installer if its source and effects cannot be confirmed.

## Reference(s):

- [Metabase homepage](https://www.metabase.com)
- [Metabase API documentation](https://www.metabase.com/docs/latest/api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-metabase)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available actions depend on the connected Metabase instance and account permissions; some actions can change or remove content.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
