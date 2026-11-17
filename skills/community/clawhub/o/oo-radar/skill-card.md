## Description:

Radar (radar.com). Use this skill for ANY Radar request — searching and reading data. Whenever a task involves Radar, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use the skill to search Radar and read location data, including autocomplete, geocoding, and nearby place results, through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute a downloaded CLI installer, and its broader effects on the agent environment are unclear.

Mitigation: Review and install a verified oo CLI release separately; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill writes.

## Reference(s):

- [Radar API documentation](https://docs.radar.com/api)
- [Radar](https://radar.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Text, Shell commands]

**Output Format:** [JSON command payloads and Radar responses, with textual results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Radar action and its response schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
