## Description:

Provides Vitally account lookup and management through the OOMOL-connected oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Vitally users can retrieve account information and create, update, or delete accounts through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions include a remote CLI installer that may run without separate user approval.

Mitigation: Review the CLI and its bundled-skill behavior, then install it yourself before enabling this skill.

Risk: Creating, updating, or deleting accounts changes Vitally data.

Mitigation: Check the target and exact payload/effect with the user before writes, and get explicit approval before deletions.

## Reference(s):

- [Vitally skill on ClawHub](https://clawhub.ai/oomol/skills/oo-vitally)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Vitally homepage](https://www.vitally.io/)
- [Vitally REST API overview](https://docs.vitally.io/en/articles/9880649-rest-api-overview)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Vitally account data and text summaries; oo CLI actions use JSON payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account writes and deletions require user approval as described in the skill.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
