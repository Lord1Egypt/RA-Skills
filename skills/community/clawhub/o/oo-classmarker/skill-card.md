## Description:

ClassMarker (classmarker.com). Use this skill for ANY ClassMarker request — searching and reading data. Whenever a task involves ClassMarker, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with a connected ClassMarker account can search and read the groups, links, assigned tests, and recent results available to their API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installation code without a clear approval step; the downloaded installer and hosted connector implementation were not verified. OOMOL is the disclosed intermediary for credentials and requests.

Mitigation: Review setup before enabling it, install a reviewed CLI version yourself, approve changes to other installed agent skills, and use a ClassMarker key limited to the data needed.

## Reference(s):

- [ClassMarker](https://www.classmarker.com)
- [ClassMarker API documentation](https://www.classmarker.com/online-testing/api/developers/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClassMarker ClawHub release](https://clawhub.ai/oomol/skills/oo-classmarker)
- [OOMOL publisher profile](https://clawhub.ai/user/oomol)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured ClassMarker data with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to the ClassMarker data accessible to the connected API key.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
