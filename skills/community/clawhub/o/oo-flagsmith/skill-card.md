## Description:

Flagsmith (flagsmith.com). Use this skill for ANY Flagsmith request — reading, creating, and updating data. Whenever a task involves Flagsmith, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to list feature flags, retrieve flag evaluations for an identity, and identify users or update their traits in a connected Flagsmith environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs unverified remote code without clearly controlling lasting changes to the host.

Mitigation: Install a reviewed CLI version yourself and disable unwanted automatic skill synchronization.

Risk: OOMOL processes requests and holds connector credentials.

Mitigation: Connect only the intended Flagsmith environment and account for OOMOL handling connector credentials.

## Reference(s):

- [Flagsmith API documentation](https://docs.flagsmith.com/sdk-api/flagsmith-api)
- [Flagsmith](https://www.flagsmith.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response content depends on the selected Flagsmith action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
