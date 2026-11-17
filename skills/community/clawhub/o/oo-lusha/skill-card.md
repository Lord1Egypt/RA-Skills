## Description:

Lusha (lusha.com). Use this skill for ANY Lusha request — searching and reading data. Whenever a task involves Lusha, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Lusha account use this skill to search companies and contacts, enrich previously returned records, and check account usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The missing-command fallback can run a downloaded CLI installer, and the installer payload is unverified.

Mitigation: Review and approve CLI installation separately; do not allow the fallback to execute the downloaded installer automatically.

Risk: The CLI may automatically change agent skills during startup.

Mitigation: Review those changes and set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when appropriate.

Risk: Using the integration gives OOMOL access to the connected Lusha account and submitted queries.

Mitigation: Review the connected account and its permissions, and submit only queries appropriate for that integration.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Lusha API documentation](https://docs.lusha.com/apis/openapi)
- [Lusha](https://www.lusha.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON connector responses with concise textual summaries; shell commands for invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns search previews, enriched company or contact data, or account usage details.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
