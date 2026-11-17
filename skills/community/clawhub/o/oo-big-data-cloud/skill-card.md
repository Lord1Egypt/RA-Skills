## Description:

BigDataCloud (bigdatacloud.com). Use this skill for ANY BigDataCloud request — searching and reading data. Whenever a task involves BigDataCloud, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to retrieve IP geolocation, network, and timezone data, or to reverse geocode coordinates with timezone data through BigDataCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup uses remote installer payloads that remain unverified.

Mitigation: Review setup and install a verified oo CLI release yourself before relying on the skill.

Risk: CLI startup synchronization can change other agents’ installed skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 if cross-agent skill changes are unwanted.

Risk: IP addresses or coordinates sent for lookups are shared through OOMOL with BigDataCloud.

Mitigation: Submit only IP addresses or coordinates you intend to send to those services.

## Reference(s):

- [BigDataCloud API documentation](https://www.bigdatacloud.com/docs/getting-started)
- [BigDataCloud](https://www.bigdatacloud.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [JSON response data with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
