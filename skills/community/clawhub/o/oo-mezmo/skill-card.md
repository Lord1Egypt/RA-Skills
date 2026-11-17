## Description:

Mezmo (mezmo.com). Use this skill for ANY Mezmo request — searching and reading data. Whenever a task involves Mezmo, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to check Mezmo ingestion status and read usage summaries by time window, app, host, or tag through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions recommend running a downloaded CLI installer without a separate approval or release verification step.

Mitigation: Review and approve CLI installation separately, and prefer a pinned, verified release.

Risk: OOMOL mediates access to the connected Mezmo account.

Mitigation: Review OOMOL's access scopes and credential handling.

## Reference(s):

- [Mezmo API documentation](https://docs.mezmo.com/docs/api)
- [Mezmo homepage](https://www.mezmo.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected read action and requested time window.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
